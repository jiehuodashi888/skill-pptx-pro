#!/usr/bin/env python3
"""Personal PPT - Profile and job preparation tools.

Usage: python personal.py list | resolve | init | spec-init | sdd-check | doctor
Examples: python personal.py resolve --profile report --style clean
Dependencies: Python standard library. See ../references/usage.md.
"""

import argparse
import copy
import hashlib
import importlib.util
import importlib.metadata
import json
import re
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def merge(parent, child):
    """Deep-merge maps; replace lists and scalars rather than appending."""
    result = copy.deepcopy(parent)
    for key, value in child.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def load_config(root, kind, name, fallback=None, chain=()):
    if kind not in ('profiles', 'styles') or not isinstance(name, str) or not ID.fullmatch(name):
        raise ValueError(f'Invalid {kind} identifier: {name!r}')
    if name in chain:
        raise ValueError('Inheritance cycle: ' + ' -> '.join((*chain, name)))
    if len(chain) >= 20:
        raise ValueError('Inheritance exceeds 20 levels')
    path = Path(root) / kind / f'{name}.json'
    if not path.is_file() and fallback:
        path = Path(fallback) / kind / f'{name}.json'
    if not path.is_file():
        raise ValueError(f'Unknown {kind}: {name}. Add a config file or select an existing identifier.')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('id') != name:
        raise ValueError(f'{path}: id must match its filename')
    if not isinstance(data.get('label'), str) or not data['label'].strip():
        raise ValueError(f'{path}: label must be nonempty text')
    parent = data.get('extends')
    if parent is not None:
        data = merge(load_config(root, kind, parent, fallback, (*chain, name)), data)
    data.pop('extends', None)
    for field in ('sections', 'required_evidence', 'acceptance', 'layout_hints'):
        if field in data and (not isinstance(data[field], list) or
                              not all(isinstance(x, str) for x in data[field])):
            raise ValueError(f'{path}: {field} must be a list of strings')
    if kind == 'profiles':
        if not isinstance(data.get('audience'), str) or not data.get('sections'):
            raise ValueError(f'{path}: profile needs audience and nonempty sections')
    else:
        palette = data.get('palette')
        if not isinstance(palette, dict) or not palette:
            raise ValueError(f'{path}: style needs a palette')
        if any(not isinstance(v, str) or not re.fullmatch(r'[0-9A-Fa-f]{6}', v)
               for v in palette.values()):
            raise ValueError(f'{path}: palette values must be six-digit hex colors without #')
    return data


def resolve(profile, style, pack_root=None, base_root=SKILL_ROOT):
    root = Path(pack_root) if pack_root else Path(base_root)
    return {
        'schema_version': 1,
        'profile': load_config(root, 'profiles', profile, base_root),
        'style': load_config(root, 'styles', style, base_root),
        'policy': {'external_services': False, 'adaptation': 'style-guided-redesign',
                   'editable_text': True, 'data_backed_charts_when_requested': True},
    }


def engine_path(skill_root=SKILL_ROOT):
    engine = Path(skill_root).resolve().parent / 'ppt-master'
    for rel in ('SKILL.md', 'scripts/svg_to_pptx.py'):
        if not (engine / rel).is_file():
            raise ValueError('Missing engine. Install personal-ppt and ppt-master as sibling skill folders.')
    return engine


def init_job(output, title, selection, sources):
    """Create an exclusive job containing resolved config and source fingerprints."""
    if not title.strip():
        raise ValueError('Title must not be empty')
    source_records = []
    for source in sources:
        path = Path(source).resolve()
        if not path.is_file():
            raise ValueError(f'Missing local source file: {source}')
        source_records.append({'path': str(path), 'sha256': digest(path)})
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError(f'Job already exists; choose a new directory: {output}')
    output.mkdir(parents=True, exist_ok=False)
    request = {'schema_version': 1, 'title': title, 'selection': selection,
               'sources': source_records, 'status': 'prepared-not-generated'}
    (output / 'request.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n',
                                       encoding='utf-8')
    (output / 'outline.md').write_text(
        '# Outline\n\nNot authored yet. Derive the outline from the supplied facts and selected purpose.\n',
        encoding='utf-8')
    return {'job': str(output), 'status': request['status']}


SPEC_HEADINGS = (
    'Intent', 'Audience and use', 'Inputs and evidence', 'Deck plan',
    'Visual direction', 'Acceptance criteria', 'Decisions and open questions',
    'Delivery and validation',
)

UNRESOLVED_SPEC_FIELDS = (
    'Business or communication outcome:',
    'Core message the audience should retain:',
    'Out of scope:',
    'Presentation setting, duration and presenter:',
    'Language and accessibility requirements:',
    'Target page count:',
    'Per-page title, takeaway and supporting evidence:',
    'Brand constraints and approved template path, if any:',
    'Layout or visual motifs to preserve:',
    'Redesign freedom and any elements that must remain native/editable:',
    'Deliverables and destination:',
    'Known limitations or waived checks:',
)


def spec_template(request):
    """Build the human-authored contract for a single deck job."""
    profile = request['selection']['profile']
    style = request['selection']['style']
    sources = request.get('sources', [])
    source_lines = '\n'.join(f'- `{record["path"]}` (SHA256: `{record["sha256"]}`)'
                             for record in sources) or '- No local sources supplied.'
    sections = '\n'.join(f'- {section}' for section in profile.get('sections', []))
    evidence = '\n'.join(f'- {item}' for item in profile.get('required_evidence', []))
    acceptance = '\n'.join(f'- {item}' for item in profile.get('acceptance', []))
    return f'''# Deck Specification: {request["title"]}

Status: draft

This document is the source of truth for this deck job. Complete the sections
below, review it with the requester, then change `Status: draft` to
`Status: approved` before generation. A material change after approval should
return the status to `draft` and record the reason under Decisions.

## Intent

- Business or communication outcome:
- Core message the audience should retain:
- Out of scope:

## Audience and use

- Primary audience: {profile.get("audience", "")}
- Presentation setting, duration and presenter:
- Language and accessibility requirements:

## Inputs and evidence

{source_lines}

Required evidence from the selected profile:
{evidence or '- No additional profile requirement.'}

Facts without a local source must be marked as assumptions, not presented as verified.

## Deck plan

Selected profile: `{profile.get("id", "")}` — {profile.get("label", "")}

Suggested sections; edit into a page-level narrative before generation:
{sections}

- Target page count:
- Per-page title, takeaway and supporting evidence:

## Visual direction

Selected style: `{style.get("id", "")}` — {style.get("label", "")}

- Brand constraints and approved template path, if any:
- Layout or visual motifs to preserve:
- Redesign freedom and any elements that must remain native/editable:

## Acceptance criteria

{acceptance or '- Define observable acceptance criteria.'}

- Every page has a clear takeaway and readable hierarchy.
- Final PPTX has editable text and required speaker notes.
- Page count, source handling and visual constraints are checked before delivery.

## Decisions and open questions

- Decision / owner / date:
- Open question or explicitly accepted assumption:

## Delivery and validation

- Deliverables and destination:
- Required checks: engine checks, PowerPoint render, `audit_pptx.py`, and page-by-page visual review.
- Known limitations or waived checks:
'''


def init_spec(job):
    job = Path(job).resolve()
    request_path = job / 'request.json'
    if not request_path.is_file():
        raise ValueError(f'Missing job request: {request_path}')
    spec_path = job / 'spec.md'
    if spec_path.exists():
        raise FileExistsError(f'Specification already exists; edit it instead: {spec_path}')
    request = json.loads(request_path.read_text(encoding='utf-8'))
    if not isinstance(request, dict) or not isinstance(request.get('selection'), dict):
        raise ValueError(f'Invalid job request: {request_path}')
    spec_path.write_text(spec_template(request), encoding='utf-8')
    return {'job': str(job), 'spec': str(spec_path), 'status': 'draft'}


def check_sdd(job):
    """Check whether the job's specification is ready to enter generation."""
    job = Path(job).resolve()
    spec_path = job / 'spec.md'
    if not spec_path.is_file():
        raise ValueError(f'Missing specification: {spec_path}. Run spec-init first.')
    text = spec_path.read_text(encoding='utf-8')
    status = re.search(r'^Status:\s*(.+?)\s*$', text, re.MULTILINE)
    missing = [heading for heading in SPEC_HEADINGS if f'## {heading}' not in text]
    unresolved = [field for field in UNRESOLVED_SPEC_FIELDS
                  if re.search(r'^-\s*' + re.escape(field) + r'\s*$', text, re.MULTILINE)]
    approved = bool(status and status.group(1).strip().lower() == 'approved')
    return {
        'job': str(job), 'spec': str(spec_path),
        'status': status.group(1).strip() if status else 'missing',
        'required_sections_present': not missing,
        'missing_sections': missing,
        'unresolved_fields': unresolved,
        'ready_to_generate': approved and not missing and not unresolved,
        'next_step': ('Proceed with the selected engine workflow and retain this specification with the job.'
                      if approved and not missing and not unresolved else
                      'Complete the specification, review it with the requester, then set Status: approved.'),
    }


def doctor():
    engine = engine_path()
    modules = {name: importlib.util.find_spec(name) is not None
               for name in ('pptx', 'PIL', 'lxml', 'yaml', 'xlsxwriter', 'pathops', 'uharfbuzz',
                            'flask', 'playwright')}
    packages = ('python-pptx', 'Pillow', 'lxml', 'PyYAML', 'XlsxWriter', 'skia-pathops',
                'uharfbuzz', 'Flask', 'playwright')
    versions = {}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return {'engine': str(engine), 'python': sys.version.split()[0], 'modules': modules,
            'versions': versions,
            'generation_dependencies_ready': all(modules[n] for n in
                ('pptx', 'PIL', 'lxml', 'yaml', 'xlsxwriter', 'pathops', 'uharfbuzz')),
            'browser_preview_modules_ready': modules['flask'] and modules['playwright'],
            'missing_modules': [n for n, present in modules.items() if not present],
            'renderers': {name: shutil.which(name) for name in ('soffice', 'pdftoppm')},
            'powerpoint_probe': 'Not tested. Use render_powerpoint.ps1 on a real PPTX on Windows.',
            'fix': 'Install requirements-core.txt into an isolated environment; install Playwright Chromium separately.',
            'note': 'Discovery only. Browser binaries, font rendering and COM access need real execution. '
                    'No export, visual approval or provider connection is implied.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    listing = sub.add_parser('list')
    listing.add_argument('--pack-root', type=Path)
    for command in ('resolve', 'init'):
        p = sub.add_parser(command)
        p.add_argument('--profile', required=True)
        p.add_argument('--style', required=True)
        p.add_argument('--pack-root', type=Path)
        if command == 'init':
            p.add_argument('--output', required=True, type=Path)
            p.add_argument('--title', required=True)
            p.add_argument('--source', action='append', default=[], type=Path)
    for command in ('spec-init', 'sdd-check'):
        p = sub.add_parser(command)
        p.add_argument('--job', required=True, type=Path)
    sub.add_parser('doctor')
    args = parser.parse_args(argv)
    try:
        if args.command == 'doctor':
            result = doctor()
        elif args.command == 'list':
            roots = [SKILL_ROOT] + ([args.pack_root] if args.pack_root else [])
            result = {kind: sorted({p.stem for root in roots for p in (root / kind).glob('*.json')})
                      for kind in ('profiles', 'styles')}
        elif args.command == 'spec-init':
            result = init_spec(args.job)
        elif args.command == 'sdd-check':
            result = check_sdd(args.job)
        else:
            result = resolve(args.profile, args.style, args.pack_root)
            if args.command == 'init':
                result = init_job(args.output, args.title, result, args.source)
        # ASCII-safe JSON survives Windows pipes with different code pages.
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
