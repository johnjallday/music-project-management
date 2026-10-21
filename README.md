# Music Project Management

A portable agent skill and content-only Ori package for a music Portfolio
Manager. It helps organize projects, choose useful studio sessions, coordinate
project teams, and plan a body of work while keeping advice separate from
execution.

> **Compatibility:** version `0.4.0` lets the Music Production Home have one
> optional **REAPER Studio**: a resource attachment appended after the REAPER
> Song entry, provided by the REAPER plugin from `0.11.0`. It requires a third
> Ori host feature, `resource_workspaces_v1`, so it needs the first Ori release
> with `resource_workspaces_v1`; an older Ori rejects `0.4.0` rather than
> partially registering it and keeps using `0.3.0`. Version `0.3.0` added
> workspace-arrangement guidance and `0.2.0` the **Your studio** card
> (`home_profile_v1`); an Ori version without `home_profile_v1` keeps `0.1.1`.
> An existing Music Production Home moves to a newer package only through
> Ori's reviewed Home package upgrade. The project-library, studio-session,
> studio-profile, arrangement and resource-catalog features are implemented by
> the host; this package does not implement them.

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

### Your studio

The Home declaration carries a `home_profile` section: a title ("Your studio"),
a one-line introduction, and labels for up to four rows whose meaning Ori owns
(`apps`, `main_app`, `templates`, `defaults`). That is all the package says
about it. Ori looks for installed DAWs only when you ask or when you press Set
up on a setup card, treats what it finds as hints until you confirm them, and
lists template names only through an installed project plugin and only after
you agree. The package itself never detects, reads or stores anything.

### REAPER Studio

The Home declaration allows one optional **REAPER Studio**: a resource
workspace, provided by the REAPER plugin's `reaper-studio` blueprint, that
holds the catalog of templates, scripts and audio plugins a REAPER setup
already has. The package contributes the attachment entry, its label and
one-line description, and the guidance that a Studio is not a song and never
counts as one. Ori creates the Studio only when you press **Set up REAPER
Studio** on the Home, reads a source only after you approve it, shows the Home
nothing but counts and freshness, and lets a song's assistant look up entries
from approved sources. Nothing in the catalog is applied, run or installed,
and the package itself never reads a REAPER folder.

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
`independent_program_homes_v1`, `home_profile_v1` and `resource_workspaces_v1`;
older versions reject this package rather than partially registering it.

Installation and setup are separate reviewed actions:

1. Review and install the plugin package.
2. Enable the plugin if it is disabled.
3. Open **Create Group**, select **Music Production Home**, and review the Home
   details and team.
4. Create or reuse the exact reviewed Home.
5. Fill the Portfolio Manager role separately, reviewing its packaged skill and
   model readiness.

The optional REAPER Plugin can later attach compatible Reaper Song projects to
that Home and, from `0.11.0`, set up the Home's one REAPER Studio. REAPER is
not required to create or use the Home, and installing this package does not
install or configure REAPER. Catalog-only songs need no
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

It checks manifest identity and versions, the three required Ori host features,
the closed Home, Home profile and attachment declarations (the REAPER Song
project team, then the REAPER Studio resource workspace), the canonical skill
path and frontmatter, path containment, and the absence of project/runtime
components.
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
11. A Home with a REAPER Studio: leaves it out of song counts, sessions and
    handoffs, and treats catalog entries as data seen at inspection that
    nothing applies, runs or installs.

These are behavioral review cases, not a claim that model-backed or live DAW
tests have run.
