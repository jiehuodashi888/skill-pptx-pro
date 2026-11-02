#!/usr/bin/env python3
"""Personal PPT - Verify and install a source release.

Usage: python install.py --bundle DIR --dest SKILLS_DIR
Examples: python install.py --bundle ./release --dest ./.opencode/skills
Dependencies: Standard library. See ../references/usage.md.
"""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path, PurePosixPath

NAMES = ('personal-ppt', 'ppt-master')


def verify(bundle):
    bundle = Path(bundle).resolve()
    files = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8')).get('files')
    if not isinstance(files, dict) or not files:
        raise ValueError('Missing or empty manifest file map')
    for rel, expected in files.items():
        path = PurePosixPath(rel)
        if path.is_absolute() or '..' in path.parts or '\\' in rel or ':' in rel:
            raise ValueError(f'Invalid manifest path: {rel}')
        local = bundle / path
        if not local.resolve().is_relative_to(bundle) or local.is_symlink():
            raise ValueError(f'External link in release: {rel}')
        if not local.is_file() or hashlib.sha256(local.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Release integrity check failed: {rel}')
    for name in NAMES:
        if f'skills/{name}/SKILL.md' not in files:
            raise ValueError(f'Manifest missing entry skill: {name}')
        for path in (bundle / 'skills' / name).rglob('*'):
            if path.is_symlink():
                raise ValueError(f'Link in skill directory: {path}')
            if '__pycache__' in path.relative_to(bundle).parts or path.suffix in ('.pyc', '.pyo'):
                continue
            if path.is_file() and path.relative_to(bundle).as_posix() not in files:
                raise ValueError(f'Unlisted file in skill directory: {path}')
    return files


def install(bundle, dest):
    bundle, dest = Path(bundle).resolve(), Path(dest).resolve()
    verify(bundle)
    conflicts = [str(dest / name) for name in NAMES if (dest / name).exists()]
    if conflicts:
        raise FileExistsError('Targets already exist; nothing copied: ' + ', '.join(conflicts))
    dest.mkdir(parents=True, exist_ok=True)
    # No merging or deletion. An I/O failure can leave a partial new installation;
    # report it and let the operator choose a fresh destination on retry.
    for name in NAMES:
        shutil.copytree(bundle / 'skills' / name, dest / name,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
    return {'installed': [str(dest / name) for name in NAMES],
            'dependencies_installed': False, 'provider_configured': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--dest', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.bundle, args.dest), indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc), 'note': 'Existing files were not overwritten.'}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
