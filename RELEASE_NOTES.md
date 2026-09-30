# Release notes

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
