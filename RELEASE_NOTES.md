# Release notes

## 0.4.0 — REAPER Studio

- The Music Production Home allows one optional **REAPER Studio**: a second
  entry appended after `reaper-song` in `allowed_project_attachments`, naming
  the REAPER plugin's `reaper-studio` blueprint and `reaper-studio-team`
  (team schema `1`, version `1`–`1`) with `workspace_kind: "resource"`, the
  label "REAPER Studio" and a one-line description. A Studio is a resource
  workspace that holds the catalog of templates, scripts and audio plugins a
  REAPER setup already has. It is not a song and never counts as one.
- Requires the Ori host feature `resource_workspaces_v1` in addition to
  `independent_program_homes_v1` and `home_profile_v1`, so this release needs
  the first Ori release with `resource_workspaces_v1`. An older Ori rejects
  `0.4.0` rather than partially registering it and keeps using `0.3.0`.
  Setting a Studio up also needs the REAPER plugin `0.11.0` or newer; with an
  older REAPER plugin the Home allows the Studio and Ori reports the missing
  blueprint.
- The Portfolio Manager prompt and the skill gain the Studio guidance: the
  Studio holds the catalog, the Home shows only counts and freshness, song
  assistants may look up entries the owner approved, and nothing is applied,
  run or installed. Both stay within their budgets (2,000 and 7,000 UTF-8
  bytes); a few existing sentences were condensed to make room and every
  boundary phrase the validator checks is kept.
- The package stays content-only. It declares words; Ori creates the Studio,
  reviews and reads sources, stores the catalog, renders the owner view and
  authorizes lookups. The package never reads a REAPER folder.
- Home `schema_version` and `version` stay `1`. Roles, stages, reflection
  bounds, the four-row profile and the `reaper-song` entry are byte-identical
  to `0.3.0`; only the Portfolio Manager prompt text changed.
- An existing Music Production Home moves to `0.4.0` only through Ori's
  reviewed Home package upgrade (its additive resource attachment class). The
  review says "Adds REAPER Studio to this Home. Nothing is created or read
  until you set it up. Once set up, assistants in this Home's projects can
  look up entries from sources you approve." The upgrade creates, staffs and
  inspects nothing.
- The validator pins the third host feature and exactly two attachments,
  `reaper-song` then `reaper-studio` with the resource fields, and checks the
  new guidance phrases in the prompt and the skill.

## 0.3.0 — Workspace arrangement guidance

- The skill gains an **Arrange the workspace** section and the Portfolio
  Manager prompt is extended to match: goal-first, evidence-first proposals
  made of catalog-only entries, user-named logical collections and selected
  project activations; conversational correction; incomplete-coverage
  reporting; and a fallback when arrangement tools are not advertised.
- File modification time is described as observed activity, not musical
  progress. Purpose, quality, stage and authoritative version stay unknown
  until the user says. Sample and export folders are not treated as songs.
- A proposal is inert. A catalog-only entry is not a link, grouping is not
  file movement, and scans, source reads, staffing, task execution and DAW
  action each keep their own capability and approval.
- No manifest field, host feature, protocol range or Home declaration
  shape/schema changed; the Portfolio Manager role prompt did change.
  Required features stay `independent_program_homes_v1` and `home_profile_v1`;
  Home schema/version stay `1`. Roles, stages, reflection bounds, the REAPER
  attachment and the four-row profile are unchanged from `0.2.0`.
- The skill is condensed to under 7,000 UTF-8 bytes and the Portfolio Manager
  prompt stays under 2,000, so a planning turn fits the host's per-turn budget.
  The validator enforces both bounds. Workflows and boundaries are unchanged.
- Existing Homes move to `0.3.0` only through Ori's reviewed package upgrade.

## 0.2.0 — Your studio

- The Music Production Home declares a **Your studio** card: the DAWs found on
  this Mac, your main DAW, your project templates, and the defaults a new song
  starts from. The package supplies only the card's title, its one-line
  introduction and the four row labels (`home_profile` on the Home
  declaration). Ori owns what each row stores, looks for installed
  applications, and asks before anything is read.
- The package stays content-only. It contains no detection, no file access and
  no runtime. Template names are listed only by an installed project plugin
  that offers that read (the REAPER Plugin from `0.10.0`), and only after you
  agree on a setup card or in the Home's review dialog.
- The Portfolio Manager and each linked project's assistant are told what the
  card holds. A detected value is a hint; a value you confirmed or set is an
  instruction.
- Requires the Ori host feature `home_profile_v1` in addition to
  `independent_program_homes_v1`. An Ori version without it rejects this
  release instead of partially registering it, and keeps using `0.1.1`.
- An existing Music Production Home moves to `0.2.0` only through Ori's
  owner-reviewed Home package upgrade. The review says "Adds a Your studio card
  to this Home. Nothing is detected or read until you open it." Approved
  library folders, staffing and learnings are kept; the card starts empty with
  a **Detect** button.
- Home schema/version stay `1`. Roles, stages, reflection bounds, the exact
  REAPER attachment allowlist and the packaged skill are unchanged from
  `0.1.1`.
- After a Home has a studio profile, do not open it with an Ori version from
  before `home_profile_v1`: that version does not know the record and drops it
  the next time it saves the Home.

## 0.1.1 — Guidance update

- Align the portable skill, packaged Portfolio Manager prompt, and README with
  installed project-local role declarations. REAPER Song's newer blueprint can
  have one REAPER Assistant, not an assumed Producer/specialist roster.
- Keep catalog-only entries separate from exact Assistant Project Links and
  distinguish reviewed Home session goals/recaps from child task or DAW progress.
- Retain the content-only Home schema/version `1`, exact attachment allowlist,
  host feature, and no automatic project or filesystem authority. Only the
  Portfolio Manager prompt and the packaged skill text change.
- New installs still require Ori `v0.0.115` or newer.
- An existing Music Production Home moves to `0.1.1` only through Ori's
  owner-reviewed Home package upgrade (ori-agent #573, in the first Ori release
  after `v0.0.116`). It keeps approved library folders and replaces a staffed
  Portfolio Manager's prompt only if it was never edited. On Ori `v0.0.116` or
  older, do not update this package while a Music Production Home exists: those
  versions cannot move the Home and leave it read-only.

## 0.1.0 — Independent Music Production Home

- Publish the content-only Music Project Management package and its canonical
  `music-project-management` skill.
- Declare the independently owned `music-producer-assistant` Music Production
  Home, required Portfolio Manager, optional Sample Library Manager, stages,
  reflection bounds, and exact REAPER project attachment authorization.
- Require Ori host feature `independent_program_homes_v1`. Ori `v0.0.115` or
  newer is required for stable use; `v0.0.115-rc.1` was the compatible host
  used for coordinated release validation.
- Keep the package content-only: no project blueprint, runtime service, setup
  quest, filesystem grant, MCP server, Workspace Surface, or REAPER dependency.
- Installation does not create or migrate a Home, staff an agent, scan files,
  start reflection, or grant access. Existing combined REAPER-owned Homes are
  not adopted or rewritten.

This release does not claim model-backed execution, production installation,
or live DAW validation. Those remain host- and user-reviewed actions.
