# AGENTS.md

Guidance for an agent session working in this repository. It is authoritative
for what this package is, how it is validated and released, and where the
boundary with Ori lies. Start the session inside a worktree of this repository
so this file and `.claude/settings.json` apply.

## What this repository is

`music-project-management` is a content-only Ori package and a portable agent
skill. Four files are the product:

| File | Role |
| --- | --- |
| `skills/music-project-management/SKILL.md` | The portable Portfolio Manager workflow |
| `.claude-plugin/plugin.json` | Portable identity: name, version, skill discovery |
| `.ori-plugin/plugin.json` | The Music Production Home declaration that Ori installs |
| `scripts/validate-package.py` | The only check; CI runs the same command |

There is no runtime, MCP server, blueprint, setup quest, filesystem grant or
DAW capability, and the validator rejects every one of them. Ori
(`github.com/johnjallday/ori-agent`) is the host: it implements the project
library, studio sessions, the studio profile and every reviewed action. This
package only declares words, roles and bounds. `AGENTS.md`, `.claude/` and
`.github/` are repository tooling, not package content.

## Checkouts and worktrees

- Main checkout: `/Users/jjdev/Projects/music-project-management`, kept on
  `main`. Use it to read and to `git fetch`; never commit there.
- Work happens in its own worktree under
  `/Users/jjdev/Projects/music-project-management-worktrees/<name>`, on a
  branch cut from `origin/main`:

  ```bash
  git -C /Users/jjdev/Projects/music-project-management fetch origin
  git -C /Users/jjdev/Projects/music-project-management worktree add \
    ../music-project-management-worktrees/<name> -b <type>/<name> origin/main
  ```

- `release-v0.1.1` is a clean candidate that Ori's harness specs stage. Leave
  it alone.
- `tasks/` is ignored. Checklists (`tasks/tasks-<feature>.md`), findings and
  evidence live there and never land in a commit.
- This repository is never added to an Ori session with `/add-dir`, and an
  Ori builder never edits this checkout. A session here never edits Ori or
  the REAPER plugin.

## Validate

```bash
python3 scripts/validate-package.py
```

It is non-installing and reads no user state. It pins the package version
(`PLUGIN_VERSION`), the two required host features, the Home identity
(`music-producer-assistant`, the station name, exactly two roles, the stages,
the reflection bounds, the one REAPER attachment and the four-row
`home_profile`), the skill's frontmatter and boundary phrases, path containment
and the absence of runtime components. When a change needs a new value, change
the validator in the same commit; a validator that no longer matches the
manifests is a red CI on every push to `main` and every pull request.

## Versions

Bumping the package version touches all of these, in one commit:

- `.claude-plugin/plugin.json` `version`
- `.ori-plugin/plugin.json` `version`
- `scripts/validate-package.py` `PLUGIN_VERSION`
- the `README.md` compatibility note
- a new `## <version> — <title>` section at the top of `RELEASE_NOTES.md`

The Home's `schema_version` and `version` stay `1`; Ori's reviewed floor
expects Home schema `1`, so a schema change is an Ori contract change first.
The package version follows semver: a new required host feature or a changed
Home declaration is a minor bump.

## Release

`release.yml` is dispatched by hand:

```bash
gh workflow run release.yml -f version=v<X.Y.Z>
```

It must run from `main`, requires the tag to equal the manifest version, runs
the validator, creates the annotated tag, and publishes a deterministic
`git archive` tarball plus checksum through the `release` environment. A
release is immutable: the workflow refuses an existing tag at a different
commit and refuses to replace an existing release.

A builder session never dispatches the release, never pushes a tag and never
runs `gh release`. It lands the version bump on `main` through a pull request;
the owner releases afterwards. Ori's reviewed floor for this package
(`MinimumVersion` and `FallbackCommit` in Ori's
`internal/reviewedintegration/entries.go`) is bumped by the Ori integration
owner once the release exists, in Ori, never from here.

## Contract with Ori

- `requires_host_features` in `.ori-plugin/plugin.json` must list features
  that exist as constants in Ori's `internal/plugin/surface_descriptor.go`.
  Today: `independent_program_homes_v1` and `home_profile_v1`. A new feature
  is an Ori change first; this package may require it only once an Ori
  release advertises it, and the README compatibility note names that Ori
  version.
- `protocol` stays `{min 1, max 1}`.
- `allowed_project_attachments` names exactly the REAPER plugin's
  `reaper-song` blueprint and `reaper-song-team` v1. Changing it changes the
  REAPER contract too.
- The skill text keeps its boundary phrases (catalog-only, exact link,
  declared role, goal or recap) because the validator and Ori's harness specs
  look for them.

When a feature spans repositories, the Ori integration owner writes the
`Cross-Repository Contract` section of the Ori task list (host features,
versions, releases, candidate path, order) and tells this session which fields
changed. This session keeps its own `tasks/tasks-<feature>.md` and does not
read the Ori checklist.

## How Ori tests a candidate

From an Ori worktree:

```bash
./scripts/music-home-demo.sh serve --source /path/to/this/worktree
./scripts/music-home-demo.sh test  --source /path/to/this/worktree
./scripts/reaper-demo.sh test --music-source /path/to/this/worktree --install-order music-first
```

The harness refuses a dirty worktree and stages the committed `HEAD` tree into
a disposable sandbox, so commit before handing the path over; uncommitted
edits are invisible to it. Nothing is installed under the real `HOME`. A
candidate staged this way is evidence for an Ori task; the published release
and the reviewed floor are later, separately approved states.

## Commits and pull requests

- The branch prefix says intent: `feature/`, `fix/`, `docs/`, `chore/`.
- Commit subjects are present tense and specific ("Add the Your studio card
  labels", not "Updates").
- Pull requests target `main` and are squash-merged, so the PR title is the
  durable message. The PR body states what changed in the manifests, the
  validator and the skill, and which Ori version the package now requires.
- Push and open the PR only when the owner asks. Never force-push `main`.
