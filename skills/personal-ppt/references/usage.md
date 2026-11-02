# Configuration and CLI reference

Run commands with the absolute path to `scripts/personal.py`; examples assume
the current directory contains that script. All commands return JSON. Errors
use stderr and exit 1. Python 3.10+ is required. Configuration tools use only
the standard library and make no network calls.

```sh
python personal.py list
python personal.py doctor
python personal.py resolve --profile report --style clean
python personal.py init --profile learning-sharing --style editorial --title "Team learning" --source /local/facts.md --output /local/jobs/learning-01
python personal.py resolve --pack-root /local/company-pack --profile incident-review --style clean
```

## Private packs

Keep company files outside the distributed skill directories. A pack contains
`profiles/<id>.json` and/or `styles/<id>.json`. A selected file in the private
pack takes precedence; absent identifiers fall back to the bundled catalog.
Parent profiles are resolved with the same precedence. Dictionaries merge
recursively; lists replace rather than append. Cycles and more than 20 parents
are rejected. A missing explicit category fails rather than selecting a default.

Profile example (`profiles/incident-review.json`):

```json
{
  "id": "incident-review",
  "label": "Incident review",
  "extends": "general",
  "audience": "Service owners and operators",
  "objective": "Explain causes and reduce recurrence",
  "sections": ["Impact", "Timeline", "Evidence", "Contributing factors", "Actions"],
  "required_evidence": ["Distinguish confirmed observations from hypotheses"],
  "acceptance": ["Action owners and dates are supplied or marked missing"]
}
```

IDs use lowercase alphanumeric segments separated by single hyphens. A profile
requires `id`, `label`, resolved `audience` and nonempty `sections`. Other
fields are agent guidance. Styles require `id`, `label` and `palette`; colors
are six-digit hex without `#`. Font lists are preferences, not proof those
fonts are installed. Private styles can extend bundled styles.

`request.json` embeds resolved configuration and local source SHA256 hashes.
It does not copy source content. Source paths are host-local and must be rebound
when migrating a job. The release tool never packages jobs or private packs.

## Installation and migration

A release contains `skills/personal-ppt` and `skills/ppt-master`. Extract it,
then run the bundled installer with an explicit destination:

```sh
python skills/personal-ppt/scripts/install.py --bundle /path/to/extracted-release --dest /path/to/project/.opencode/skills
```

For a Codex installation use its configured skills directory instead. The
installer validates the release manifest before copying, rejects existing
target skill folders and never merges or overwrites them. Updates require a
separately chosen destination or a deliberate manual backup/migration.

Installation copies skills only. Run `personal.py doctor` afterward. Engine
dependency requirements remain in `ppt-master/requirements.txt` with optional
features documented there. The v0.1 source release does not include Python,
binary wheels, fonts or rendering executables. Obtain target-OS dependencies
through the approved internal mirror or an independently prepared offline
wheel bundle. Do not copy this development machine's Python environment.

OpenCode model configuration and credentials stay outside the release. Verify
tool calls, context handling, image input (if needed), Chinese fonts and PPTX
rendering on the actual GLM deployment. Without image input, visual review
requires a human or an approved local vision service.

## Publishing the personal source release

From the repository, invoke `python skills/personal-ppt/scripts/release.py --output /path/personal-ppt-0.1.0.zip`.
It packages the pinned, Git-tracked upstream skill files plus the explicitly
listed personal source files. It rejects changes to tracked upstream files and
does not sweep untracked local files into the bundle. This is an integrity
manifest, not a publisher signature or supply-chain audit.
