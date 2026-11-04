---
name: personal-ppt
description: Use when creating or redesigning editable PPTX with reusable personal or company use-case profiles and independently selected visual styles, including extensible categories and local-only reference material.
---

# Personal PPT

This is the personal entry layer for the sibling `ppt-master` engine. Resolve
this file's directory as `PERSONAL_ROOT`; resolve the engine as
`PERSONAL_ROOT/../ppt-master`. Both must travel together. If either is missing,
read [installation instructions](references/usage.md); do not substitute a
different installed engine silently.

## Prepare the request

Read [usage](references/usage.md) for CLI syntax and configuration contracts.
For a new deck, major redesign, template extraction or profile/style change, read
[Specs and SDD](references/spec-sdd.md). Create the job specification with
`spec-init`; do not begin generation until `sdd-check` reports
`ready_to_generate: true`. Minor, already-approved corrections may be recorded
in the existing job specification without creating a new repository spec.
Use a callable local Python 3.10+ executable; never assume a developer's path.
Run `scripts/personal.py list` to discover bundled profiles and styles. If the
user supplies a private pack, pass its explicit path with `--pack-root`.

Keep four decisions separate: use-case profile (argument and audience), style
(visual language), brand (fixed identity constraints), layout (page structure).
The bundled profiles are examples, not the complete taxonomy. An explicitly
requested unknown category is an error: ask for its definition or explicit
selection of another category. Never silently map it to report or general.
If no category is requested, propose a suitable known profile and state the
choice. The same style may serve any profile.

Resolve the chosen profile and style, then use `init` to persist `request.json`
and source hashes in a new job directory. The initial `outline.md` is an empty
planning artifact, not completed content. Read the actual local source files.
Record brand constraints and explicit template workspace paths in the job
alongside the request. Do not infer a template path from a style label.

Treat the approved job `spec.md` as the delivery contract. Keep its source,
audience, page narrative, visual constraints and acceptance criteria aligned
with the engine design brief. When scope changes materially, return the spec to
draft and get it approved again before continuing.

## Local-only policy

By default, use a closed local corpus. Do not call web research, fetch remote
URLs or images, use hosted image/speech generation, upload files, or install
dependencies from external registries during a deck job. Use local assets and
native shapes. If facts or assets are missing, report what is missing and
request local material or use clearly marked omissions; never invent data.

An explicit user opt-in can permit a particular external service for the job;
record the service and scope in `request.json` before using it. A GLM endpoint
configured by the host is a separate model-service setting: do not configure
or change it automatically. This policy is not a network firewall and cannot
guarantee the host itself never communicates externally.

## Execute with the engine

Read the sibling engine's `SKILL.md`, run its attribution check, and read its
route selector. Honor this request's closed-corpus restriction when an upstream
step would otherwise require internet research or image acquisition. If that
step cannot complete locally, report the unmet prerequisite instead of bypassing
checks or accessing external services.

Select the engine route from user intent:

- New deck or style-guided redesign: Generate PPTX. Feed resolved narrative
  sections, evidence requirements, palette and visual hints into the engine's
  communication contract and design brief. Style JSON is guidance, not a
  registered template workspace. Layout hints are suggestions, not a mandatory
  identical page sequence. Preserve user-specified brand constraints.
- Distill reusable styles/brands/layouts from reference decks: Create Template.
  Read and render the original references; label extracted rules as proposals
  until the user validates sample pages. Keep company results in the supplied
  private location. Do not copy old business facts into unrelated new decks.
- Preserve a native deck while replacing selected content: Edit Native PPTX.
  Do not reinterpret style-guided redesign as strict preservation, or vice versa.

Keep profile/style selection and authored outline in the personal job, and
record the engine workspace path there. Use the engine's own project initializer
for its workspace; the personal job folder is not a substitute engine project.
When moving a job, rebind missing source paths explicitly and verify hashes.

## Deliver and improve

Read [production and delivery](references/production.md) for dependency setup,
full-run evidence, native PowerPoint rendering and offline transfer. Run the
expanded `doctor` before a real job; missing modules and renderer failures are
different readiness states. Never install dependencies without authorization.

Run the selected engine's checks and inspect rendered pages. Separate editable
text/shapes from native data-backed charts. If chart data must be editable,
select and validate the engine's native-chart/table export. Do not promise all
embedded artwork is editable. Report unavailable renderers or unverified fonts.

Deliver PPTX, preview when available, retained source/configuration and any
unresolved issues. `init`, `resolve` and a passing configuration test do not
mean a deck was generated or visually approved. No GLM/OpenCode compatibility
claim is valid until an actual target-environment run passes.

After export, use `scripts/render_powerpoint.ps1` on a Windows PowerPoint host,
then `scripts/audit_pptx.py` with the expected page count and render directory.
Inspect every final PNG and record page-specific findings separately. The audit
checks provenance and structure only; a successful audit is not visual approval.

For a new category, add a profile file in the user's chosen pack; for a visual
change, add or modify a style. Keep business categories out of exporter code.
Save approved preferences in the private pack, not in the upstream engine.
