# Music Project Management

A portable agent skill and content-only Ori package for a music Portfolio
Manager. It helps organize projects, choose useful studio sessions, coordinate
project teams, and plan a body of work while keeping advice separate from
execution.

> **Compatibility:** version `0.1.1` keeps the content-only Home contract from
> `0.1.0` and requires Ori `v0.0.115` or newer. An existing Music Production
> Home moves from `0.1.0` only through Ori's reviewed Home package upgrade (the
> first Ori release after `v0.0.116`); do not update the package on older Ori
> while such a Home exists. The project-library and studio-session features
> additionally require host support; this package does not implement them. Ori
> versions before `v0.0.115` reject the package rather than partially
> registering it.

## What it does

- Guides project discovery and onboarding when the host provides those tools.
- Helps classify songs by purpose, production stage, priority, and next milestone.
- Recommends what to work on from known goals, blockers, and available time.
- Prepares reviewed handoffs to the exact linked project's declared role(s).
- Supports EP/album planning, studio reviews, and archive-readiness discussions.

Example requests:

> Help me catalog my existing music projects.
>
> I have an hour. Which song should I work on?
>
> Help me plan an EP from these projects.
>
> What decisions are blocking my unfinished songs?

## Package contents

| Path | Responsibility |
| --- | --- |
| [`skills/music-project-management/SKILL.md`](skills/music-project-management/SKILL.md) | The single canonical, portable management workflow |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | Portable package identity and skill discovery |
| [`.ori-plugin/plugin.json`](.ori-plugin/plugin.json) | The independently owned Music Production Home declaration |
| [`scripts/validate-package.py`](scripts/validate-package.py) | Local, non-installing package validation |

This repository owns the Music Production Home, its Portfolio Manager, the
optional Sample Library Manager declaration, and Home-level coordination and
reviewed learning defaults. A project integration owns its own project
blueprint, local team, tools, setup, and runtime access.

The package intentionally contains no project blueprint or skeleton, MCP server,
executable runtime, setup quest, filesystem grant, or DAW capability. Installing
it does not scan directories, create a Home, staff an agent, start reflection,
or grant access.

## Use as a portable skill

Add this repository using your agent harness's supported skill installation
mechanism, or copy the `skills/music-project-management/` directory into that
harness's personal skill directory. Keep `SKILL.md` in that directory; there is
no second root-level copy.

Portable use works from an inventory the user supplies and from capabilities
the current host explicitly exposes. It does not imply Ori installation or any
DAW integration.

## Install in Ori

Use Ori's normal plugin review flow with this repository or a separately
verified release. The installed Ori version must advertise
`independent_program_homes_v1`; older versions reject this package rather than
partially registering it.

Installation and setup are separate reviewed actions:

1. Review and install the plugin package.
2. Enable the plugin if it is disabled.
3. Open **Create Group**, select **Music Production Home**, and review the Home
   details and team.
4. Create or reuse the exact reviewed Home.
5. Fill the Portfolio Manager role separately, reviewing its packaged skill and
   model readiness.

The optional REAPER Plugin can later attach compatible Reaper Song projects to
that Home. REAPER is not required to create or use the Home, and installing this
package does not install or configure REAPER. Catalog-only songs need no
project workspace and cannot receive a project handoff. Each exact linked
project retains the role(s) declared by its installed blueprint (a REAPER Song
may have one REAPER Assistant), files, grants, and runtime readiness. Session
goals and recaps are reviewed Home records, not proof of project work or DAW
activity.

## Architecture boundaries

| Component | Responsibility |
| --- | --- |
| This package | Management workflow, Music Production Home, Home roles, recommendations, and bounded coordination |
| A project integration such as the REAPER Plugin | Supported project formats, project-local roles, project setup, skills, and DAW operations |
| Ori | Trust review, permissions, package installation, exact links, records, reviewed actions, staffing, and workspace connections |

Discovery is not project creation or permission to access project contents. A
reviewed handoff creates bounded child-owned work; it does not let the Portfolio
Manager inspect child context or control a project agent. Home-level management
does not require REAPER live control.

## Validate the package

Run the repository-local, non-installing validator:

```bash
python3 scripts/validate-package.py
```

It checks manifest identity and versions, the required Ori host feature, the
closed Home and attachment declarations, the canonical skill path and
frontmatter, path containment, and the absence of project/runtime components.
It does not install the package or access user state.

## Review scenarios

When changing the package, check that it handles these cases honestly:

1. No discovery tool: explains the gap and offers individual import or inventory.
2. Several `.rpp` versions: asks for the authoritative project rather than guessing.
3. Hundreds of candidates: separates cataloging from selected workspace activation.
4. Stale or missing status: identifies uncertainty instead of inventing progress.
5. A requested project handoff: previews the exact target and waits for review.
6. Partial import success: preserves successes and checks state before retrying.
7. A request to delete old projects: keeps physical deletion outside its authority.
8. Instructions embedded in imported content: treats them as untrusted data.
9. No project integration installed: keeps Home coordination available without
   inventing a project, runtime, or grant.
10. A disabled Home provider: keeps stored records readable and reports unavailable
    coordination honestly.

These are behavioral review cases, not a claim that model-backed or live DAW
tests have run.
