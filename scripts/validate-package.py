#!/usr/bin/env python3
"""Validate the content-only Music Project Management plugin package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

PLUGIN_ID = "music-project-management"
PLUGIN_VERSION = "0.1.0"
HOME_ID = "music-producer-assistant"
SKILL_ID = "music-project-management"
HOST_FEATURE = "independent_program_homes_v1"
REPOSITORY = "https://github.com/johnjallday/music-project-management"
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


class ValidationError(Exception):
    """Raised when package validation fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read valid JSON from {path}: {exc}") from exc
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def require_keys(value: dict[str, Any], required: set[str], allowed: set[str], label: str) -> None:
    missing = sorted(required - value.keys())
    extra = sorted(value.keys() - allowed)
    require(not missing, f"{label} is missing keys: {', '.join(missing)}")
    require(not extra, f"{label} has unsupported keys: {', '.join(extra)}")


def contained_path(root: Path, raw: str, label: str) -> Path:
    require(bool(raw) and not os.path.isabs(raw), f"{label} must be a non-empty relative path")
    require("\\" not in raw and "%" not in raw, f"{label} contains an unsupported path character")
    candidate = (root / raw).resolve(strict=False)
    try:
        common = Path(os.path.commonpath((root, candidate)))
    except ValueError as exc:
        raise ValidationError(f"{label} escapes the package root") from exc
    require(common == root, f"{label} escapes the package root")
    return candidate


def validate_tree(root: Path) -> None:
    required_files = {
        root / ".claude-plugin" / "plugin.json",
        root / ".ori-plugin" / "plugin.json",
        root / "README.md",
        root / "skills" / SKILL_ID / "SKILL.md",
        root / "scripts" / "validate-package.py",
    }
    for path in required_files:
        require(path.is_file(), f"required package file is missing: {path.relative_to(root)}")

    prohibited = (
        ".mcp.json",
        ".codex-plugin",
        "agents",
        "artifacts",
        "bin",
        "blueprints",
        "commands",
        "hooks",
        "services",
        "setup-quests",
    )
    for name in prohibited:
        require(not (root / name).exists(), f"content-only package must not contain {name}")

    for path in root.rglob("*"):
        if path.name == ".git" or ".git" in path.parts:
            continue
        require(not path.is_symlink(), f"package path must not be a symlink: {path.relative_to(root)}")


def validate_claude_manifest(root: Path, manifest: dict[str, Any]) -> None:
    required = {"name", "version", "description", "author", "homepage", "repository", "keywords", "skills"}
    require_keys(manifest, required, required, "Claude plugin manifest")
    require(manifest["name"] == PLUGIN_ID, "Claude manifest has the wrong plugin name")
    require(manifest["version"] == PLUGIN_VERSION and SEMVER_PATTERN.fullmatch(manifest["version"]), "Claude manifest has an invalid version")
    require(manifest["homepage"] == REPOSITORY and manifest["repository"] == REPOSITORY, "Claude manifest repository identity is inconsistent")
    require(isinstance(manifest["description"], str) and manifest["description"].strip(), "Claude manifest description is required")
    require(isinstance(manifest["keywords"], list) and all(isinstance(item, str) and item for item in manifest["keywords"]), "Claude manifest keywords must be strings")
    skill_root = contained_path(root, manifest["skills"], "Claude manifest skills path")
    require(skill_root == (root / "skills").resolve(), "Claude manifest must point at the canonical skills directory")


def validate_role(role: dict[str, Any], expected_id: str) -> None:
    allowed = {"id", "label", "description", "required", "capability_id", "primary", "role", "type", "system_prompt", "skills"}
    required = {"id", "label", "required", "system_prompt"}
    require_keys(role, required, allowed, f"Home role {expected_id}")
    require(role["id"] == expected_id and ID_PATTERN.fullmatch(role["id"]), f"unexpected Home role identity: {role.get('id')}")
    require(isinstance(role["required"], bool), f"Home role {expected_id} required must be boolean")
    require(isinstance(role["system_prompt"], str) and role["system_prompt"].strip(), f"Home role {expected_id} needs a system prompt")
    require("scope" not in role, f"Home role {expected_id} must not declare project scope")


def validate_home(home: dict[str, Any]) -> None:
    allowed = {
        "schema_version", "version", "id", "station_name", "station_description",
        "default_primary_name", "hire_title", "hire_description", "disabled_message",
        "suggestion_required_capabilities", "roles", "stages", "reflection",
        "allowed_project_attachments",
    }
    required = allowed
    require_keys(home, required, allowed, "assistant program Home")
    require(home["schema_version"] == 1 and home["version"] == 1, "Home schema/version must be 1")
    require(home["id"] == HOME_ID and ID_PATTERN.fullmatch(home["id"]), "Home identity is invalid")
    require(home["station_name"] == "Music Production Home", "Home station name is inconsistent")
    require(home["suggestion_required_capabilities"] == [], "Home suggestions must not require a project-provider capability")

    roles = home["roles"]
    require(isinstance(roles, list) and len(roles) == 2, "Home must declare exactly its two owned roles")
    require(all(isinstance(role, dict) for role in roles), "Home roles must be objects")
    role_by_id = {role.get("id"): role for role in roles}
    require(set(role_by_id) == {"portfolio_manager", "sample_library_manager"}, "Home role identities are inconsistent")
    validate_role(role_by_id["portfolio_manager"], "portfolio_manager")
    validate_role(role_by_id["sample_library_manager"], "sample_library_manager")
    manager = role_by_id["portfolio_manager"]
    require(manager["required"] is True and manager.get("primary") is True, "Portfolio Manager must be the required Home primary")
    require(manager.get("skills") == [SKILL_ID], "Portfolio Manager must bind only the packaged management skill")
    sample_manager = role_by_id["sample_library_manager"]
    require(sample_manager["required"] is False and not sample_manager.get("primary", False), "Sample Library Manager must remain optional and non-primary")
    require(sample_manager.get("capability_id") == "sample-library", "Sample Library Manager must retain the reviewed add-on boundary")
    require(not sample_manager.get("skills"), "Sample Library Manager must not claim a packaged runtime skill")

    stages = home["stages"]
    require(isinstance(stages, list) and [stage.get("id") for stage in stages] == ["helper", "collaborator"], "Home learning stages are inconsistent")
    for stage in stages:
        require_keys(stage, {"id", "label", "description", "accepted_completion_threshold"}, {"id", "label", "description", "accepted_completion_threshold"}, f"stage {stage.get('id')}")
    reflection = home["reflection"]
    reflection_keys = {"minimum_projects", "cadence_hours", "max_projects", "max_events_per_project", "max_candidates", "max_evidence", "rubric"}
    require(isinstance(reflection, dict), "Home reflection must be an object")
    require_keys(reflection, reflection_keys, reflection_keys, "Home reflection")
    require(reflection["minimum_projects"] >= 3 and reflection["cadence_hours"] >= 24, "Home reflection bounds are unsafe")

    attachments = home["allowed_project_attachments"]
    require(attachments == [{
        "provider_plugin_id": "reaper-plugin",
        "blueprint_id": "reaper-song",
        "project_team_id": "reaper-song-team",
        "project_team_schema_version": 1,
        "min_project_team_version": 1,
        "max_project_team_version": 1,
    }], "Home attachment allowlist must contain only the reviewed REAPER project-team contract")

    serialized = json.dumps(home).lower()
    for forbidden in ("reaper_live_control", "runtime_provider", "entrypoint", "setup_quest", "command", "filesystem_root"):
        require(forbidden not in serialized, f"Home declaration contains forbidden project/runtime authority: {forbidden}")


def validate_ori_manifest(manifest: dict[str, Any], claude: dict[str, Any]) -> None:
    required = {"schema_version", "name", "version", "protocol", "requires_host_features", "capabilities", "services", "blueprints", "assistant_program_homes"}
    require_keys(manifest, required, required, "Ori plugin manifest")
    require(manifest["schema_version"] == 1, "Ori contribution schema must be 1")
    require(manifest["name"] == claude["name"] == PLUGIN_ID, "manifest plugin names do not match")
    require(manifest["version"] == claude["version"] == PLUGIN_VERSION, "manifest plugin versions do not match")
    require(manifest["protocol"] == {"min": 1, "max": 1}, "Ori protocol range must be exactly v1")
    require(manifest["requires_host_features"] == [HOST_FEATURE], "Ori package must require the independent Home host feature")
    require(manifest["capabilities"] == [], "music package must not install a capability")
    require(manifest["services"] == [], "music package must not contain a runtime service")
    require(manifest["blueprints"] == [], "music package must not contain a project blueprint")
    homes = manifest["assistant_program_homes"]
    require(isinstance(homes, list) and len(homes) == 1 and isinstance(homes[0], dict), "Ori package must contain exactly one Home declaration")
    validate_home(homes[0])


def validate_skill(root: Path) -> None:
    path = root / "skills" / SKILL_ID / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "skill must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 4, "skill frontmatter is not terminated")
    frontmatter = text[4:end]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    require(fields.get("name") == SKILL_ID, "skill frontmatter name does not match its package identity")
    require(bool(fields.get("description")), "skill frontmatter description is required")
    require("reaper_live_control" not in text, "portable Home skill must not require REAPER live control")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.expanduser().resolve()

    try:
        require(root.is_dir(), f"package root does not exist: {root}")
        validate_tree(root)
        claude_path = root / ".claude-plugin" / "plugin.json"
        ori_path = root / ".ori-plugin" / "plugin.json"
        claude = load_json(claude_path)
        ori = load_json(ori_path)
        validate_claude_manifest(root, claude)
        validate_ori_manifest(ori, claude)
        validate_skill(root)
    except (OSError, ValidationError) as exc:
        print(f"package validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"validated {PLUGIN_ID} {PLUGIN_VERSION}")
    print(f"claude_manifest_sha256={sha256(claude_path)}")
    print(f"ori_manifest_sha256={sha256(ori_path)}")
    print(f"skill_sha256={sha256(root / 'skills' / SKILL_ID / 'SKILL.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
