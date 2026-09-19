# Music Project Management

A standalone agent skill for a music Portfolio Manager: organize projects,
choose useful studio sessions, coordinate project teams, and plan a body of work.
DAW-independent, with an explicit separation between advice and execution.

## What it does

- Guides project discovery and onboarding when the host provides those tools.
- Helps classify songs by purpose, production stage, priority, and next milestone.
- Recommends what to work on from known goals, blockers, and available time.
- Prepares reviewed handoffs to individual project Producers.
- Supports EP/album planning, studio reviews, and archive-readiness discussions.

Example requests:

> Help me catalog my existing music projects.
>
> I have an hour. Which song should I work on?
>
> Help me plan an EP from these projects.
>
> What decisions are blocking my unfinished songs?

## Architecture

| Component | Responsibility |
| --- | --- |
| This skill | Management workflow, evidence handling, recommendations, and coordination |
| DAW integration, such as the REAPER Plugin | Supported project formats and DAW-specific operations |
| Host, such as Ori | Permissions, discovery tools, records, reviewed actions, and workspace connections |

Installing the skill does **not** implement recursive directory scanning, create
an import catalog, grant filesystem access, or control a DAW. It checks for
available operations and explains gaps instead of inventing tools.

In Ori, the primary intended user is the Portfolio Manager in Music Production
Group. Project Producers and specialists keep their own scope and authority.
The REAPER integration's existing individual-folder import can be used when
available; recursive discovery and batch cataloging require additional host
support. No REAPER integration is needed for advice from a supplied inventory.

## Use

The skill entry point is [`SKILL.md`](SKILL.md). Add this repository as a skill
source using your agent harness's supported installation mechanism, or copy its
`SKILL.md` into a `music-project-management/` directory under that harness's
skill directory. Installation alone grants no tools or permissions.

The repository is initially documentation-only: no executable scripts, runtime
dependencies, scanning service, automatic agent binding, or scheduled jobs.

## Boundaries

- Discovery is not workspace creation or permission to access project contents.
- Cataloging references existing projects; it does not move or rewrite them.
- Ambiguous versions need review, not an automatic newest-file selection.
- A task handoff does not start execution.
- Archiving a portfolio record does not archive or delete physical files.
- User project records belong in their workspace, not in this repository.

## Review scenarios

When changing the skill, check that it handles these cases honestly:

1. No discovery tool: explains the gap and offers individual import or inventory.
2. Several `.rpp` versions: asks for the authoritative project rather than guessing.
3. Hundreds of candidates: separates cataloging from selected workspace activation.
4. Stale or missing status: identifies uncertainty instead of inventing progress.
5. A requested project handoff: previews the exact target and waits for review.
6. Partial import success: preserves successes and checks state before retrying.
7. A request to delete old projects: keeps physical deletion outside its authority.
8. Instructions embedded in imported content: treats them as untrusted data.

These are behavioral review cases, not a claim that agent-runtime tests have run.
