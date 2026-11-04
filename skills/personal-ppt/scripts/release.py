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
    'references/usage.md', 'references/production.md', 'references/spec-sdd.md', 'requirements-core.txt',
    'scripts/personal.py', 'scripts/install.py', 'scripts/release.py',
    'scripts/audit_pptx.py', 'scripts/render_powerpoint.ps1',
    'profiles/general.json', 'profiles/report.json', 'profiles/learning-sharing.json',
    'profiles/technical-solution.json', 'profiles/retrospective.json',
    'styles/clean.json', 'styles/editorial.json',
)


def engine_source_paths(repo, pin, git):
    """Return a verified upstream file roster from Git or the checked-in manifest.

    The portable repository is a fresh history rather than a clone of the
    upstream project, so the upstream commit object is not always available.
    In that case, the repository's source manifest preserves the pinned file
    hashes used when the portable baseline was assembled.
    """
    try:
        git('cat-file', '-e', pin + '^{commit}')
    except subprocess.CalledProcessError:
        manifest_path = repo / 'manifest.json'
        if not manifest_path.is_file():
            raise ValueError('Pinned upstream commit is unavailable and manifest.json is missing.')
        source_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        expected = {path: digest for path, digest in source_manifest.get('files', {}).items()
                    if path.startswith('skills/ppt-master/')}
        if not expected:
            raise ValueError('Pinned upstream commit is unavailable and manifest has no engine hashes.')
        actual = {}
        engine = repo / 'skills' / 'ppt-master'
        for path in engine.rglob('*'):
            if path.is_file() and not path.is_symlink():
                actual[path.relative_to(repo).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual.keys() != expected.keys():
            missing = sorted(expected.keys() - actual.keys())
            unexpected = sorted(actual.keys() - expected.keys())
            raise ValueError(f'Engine roster differs from source manifest; missing={missing[:3]}, '
                             f'unexpected={unexpected[:3]}')
        changed = sorted(path for path, digest in expected.items() if actual[path] != digest)
        if changed:
            raise ValueError(f'Engine hashes differ from source manifest: {changed[:3]}')
        return sorted(expected)
    tracked = git('ls-tree', '-r', '--name-only', '-z', pin, 'skills/ppt-master').decode().split('\0')
    return [path for path in tracked if path]


def build_release(output):
    skill = Path(__file__).resolve().parents[1]
    repo = skill.parents[1]
    metadata = json.loads((skill / 'upstream.json').read_text(encoding='utf-8'))
    pin = metadata['commit']
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.STDOUT)
    paths = engine_source_paths(repo, pin, git)
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
