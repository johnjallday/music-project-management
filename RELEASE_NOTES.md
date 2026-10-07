# Release notes

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
