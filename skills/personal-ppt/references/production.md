# Production and delivery

This layer adds dependency discovery and delivery evidence to the sibling
engine. It does not replace engine routing, confirmation, SVG authoring,
quality gates, or native chart/table contracts.

## Environment

Use a dedicated Python 3.10+ environment. Resolve all paths on the target host.
The commands below assume the personal skill directory is the current directory;
agents should expand paths absolutely before running them.

```sh
python -m venv .venv
# Activate .venv using the target shell, then:
python -m pip install -r requirements-core.txt
python -m playwright install chromium
python scripts/personal.py doctor
```

Installation requires explicit external-network authorization or an approved
internal package source. It never runs automatically during a closed-corpus job.
`doctor` distinguishes generation and browser modules and reports package
versions. Module discovery alone does not verify Chromium binaries, fonts,
PowerPoint licensing, desktop-session access, or rendering. Test them with the
actual sample. Do not treat a sandbox COM/session error as a missing PowerPoint
installation. Use an authorized interactive desktop environment when required.

## Full run

1. Resolve profile/style and persist the personal job with source hashes.
2. Run the engine attribution guard and select its one route. Initialize a
   separate engine workspace and import local material. Record its path in the job.
3. Complete planning and the selected route's gates. Preserve source qualifiers,
   distinguish scenario data, and keep brand/style/layout separate.
4. Calibrate fonts, start live preview, author SVGs, run the early and final
   gates when the selected route requires them. Repair all blocking findings.
5. If visual review is requested, render and inspect every SVG page through
   the engine visual-review stage. Inspect the actual images, not just logs.
6. Author/split notes when enabled. Run `finalize_svg.py`, then the full
   `svg_to_pptx.py` CLI, serially. Use `--no-animations` when all motion is off;
   disabling custom animations alone does not disable the default fade transition.
   Never bypass exporter gates with an imported
   low-level converter function.
7. Render the resulting PPTX through the destination presentation application.
   SVG/browser previews do not prove native PowerPoint fidelity.
8. Run the package audit, inspect every rendered page, repair at the owning
   layer, then repeat affected checks/export/render. Record remaining limits.

On Windows with installed PowerPoint:

```powershell
powershell -NoProfile -File scripts/render_powerpoint.ps1 -Pptx C:/decks/sample.pptx -Output C:/decks/render-v1
python scripts/audit_pptx.py C:/decks/sample.pptx --expected-pages 8 --require-notes --render-dir C:/decks/render-v1
```

The renderer opens the deck read-only and refuses an existing output directory.
It closes only its own deck and does not quit a session with existing decks.
It records PowerPoint version, page raster dimensions, PPTX hash and PNG hashes.
It never closes unrelated user presentations. PowerPoint may display desktop
dialogs; unattended service accounts are not a supported COM environment.

The audit checks ZIP integrity, page count, native text presence per page,
notes when requested, render roster and file hashes. It reports pictures and
text separately; native text does not prove every object is editable. It never
approves visual quality automatically. Keep a separate review record naming
each inspected image and its findings. Re-export invalidates previous render
evidence even when the filename is unchanged.

When PowerPoint is unavailable, use an installed local office renderer if the
target environment permits it and label the renderer honestly. Do not claim
PowerPoint fidelity from a browser, an imported screenshot, or XML inspection.
If no renderer runs, deliver a draft with visual review explicitly incomplete.

## Offline transfer

The source release excludes environments, browser binaries, output decks,
company materials and credentials. Transfer these separately through approved
channels. A Windows wheelhouse is not a Linux wheelhouse.

On a connected machine matching the target OS, CPU and Python version:

```sh
python -m pip download -r requirements-core.txt --dest wheelhouse
python -m pip freeze > environment-observed.txt
```

On the offline host:

```sh
python -m pip install --no-index --find-links wheelhouse -r requirements-core.txt
```

Pin and archive the dependency versions actually accepted by that host;
`environment-observed.txt` is evidence, not a portable environment lock.
Provision the matching Playwright browser cache separately and set
`PLAYWRIGHT_BROWSERS_PATH` to its local location. Provision a PPTX renderer and
licensed/available Chinese fonts separately. Then rerun the complete sample.
Configure GLM/OpenCode credentials only in the host's secret configuration,
never in the skill, release ZIP, profile JSON, sample or log.

## Reference-driven extension

For company reference decks, first inventory their page roles and render them.
Separate recurring brand rules (fonts, colors, logo, footer), visual treatment,
layout patterns and use-case narrative. Record reference filenames/page numbers
for each proposed rule. Use the engine Create Template route for reusable
workspaces; a style JSON alone cannot represent a PowerPoint master.
Validate a cover, a dense content page and a diagram/table page before broad
adoption. Keep extracted private packs outside the source release. Add one
profile per genuine purpose; do not hard-code the company taxonomy in scripts.

## Evidence boundaries

The 0.2 sample exercises Chinese editable text, simple shapes, multiple page
compositions, notes, static gates, browser preview and Windows PowerPoint render.
It does not validate native data charts, template preservation, animation,
external images, Linux/LibreOffice, or an actual GLM/OpenCode session. Test each
of those with a representative deck before claiming support on a target host.
