#!/usr/bin/env python3
"""Personal PPT - Build a pinned source-only release.

Usage: python release.py --output FILE.zip
Examples: python release.py --output /local/releases/personal-ppt-0.1.0.zip
Dependencies: Standard library and Git. See ../references/usage.md.
"""

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

PERSONAL_FILES = (
    'SKILL.md', 'README_CN.md', 'upstream.json', 'LICENSE',
    'references/usage.md', 'references/production.md', 'requirements-core.txt',
    'scripts/personal.py', 'scripts/install.py', 'scripts/release.py',
    'scripts/audit_pptx.py', 'scripts/render_powerpoint.ps1',
    'profiles/general.json', 'profiles/report.json', 'profiles/learning-sharing.json',
    'profiles/technical-solution.json', 'profiles/retrospective.json',
    'styles/clean.json', 'styles/editorial.json',
)


def build_release(output):
    skill = Path(__file__).resolve().parents[1]
    repo = skill.parents[1]
    metadata = json.loads((skill / 'upstream.json').read_text(encoding='utf-8'))
    pin = metadata['commit']
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args])
    git('cat-file', '-e', pin + '^{commit}')
    # Personal commits may advance HEAD. Only tracked engine modifications,
    # deletions and renames relative to the pin invalidate the base. Additive
    # tests are not shipped: release membership comes from the pinned tree.
    if git('diff', '--diff-filter=DMRT', pin, '--', 'skills/ppt-master'):
        raise ValueError('Tracked upstream engine modifications found; review before release.')
    tracked = git('ls-tree', '-r', '--name-only', '-z', pin, 'skills/ppt-master').decode().split('\0')
    paths = [p for p in tracked if p]
    paths += ['skills/personal-ppt/' + rel for rel in PERSONAL_FILES]
    payload = {}
    for rel in paths:
        path = repo / rel
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'Missing or linked release source: {rel}')
        payload[rel] = path.read_bytes()
    manifest = {**metadata, 'kind': 'source-only',
                'files': {rel: hashlib.sha256(data).hexdigest() for rel, data in payload.items()}}
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for rel, data in payload.items():
            archive.writestr(rel, data)
        archive.writestr('manifest.json', json.dumps(manifest, indent=2) + '\n')
    return {'archive': str(output), 'files': len(payload),
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'kind': 'source-only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build_release(args.output), indent=2))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
