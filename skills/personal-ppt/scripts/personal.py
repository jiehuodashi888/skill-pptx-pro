#!/usr/bin/env python3
"""Personal PPT - Profile and job preparation tools.

Usage: python personal.py list | resolve | init | doctor
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
    sub.add_parser('doctor')
    args = parser.parse_args(argv)
    try:
        if args.command == 'doctor':
            result = doctor()
        elif args.command == 'list':
            roots = [SKILL_ROOT] + ([args.pack_root] if args.pack_root else [])
            result = {kind: sorted({p.stem for root in roots for p in (root / kind).glob('*.json')})
                      for kind in ('profiles', 'styles')}
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
