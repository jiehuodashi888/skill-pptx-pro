#!/usr/bin/env python3
"""Personal PPT - Audit delivered PPTX structure and render provenance.

Usage: python audit_pptx.py FILE --expected-pages N [--render-dir DIR] [--require-notes]
Examples: python audit_pptx.py deck.pptx --expected-pages 8 --render-dir rendered
Dependencies: Standard library. See ../references/production.md.
"""

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(path: Path, expected_pages: int, render_dir: Path | None = None,
          require_notes: bool = False) -> dict:
    """Validate package evidence; never infer visual approval from PNG existence."""
    errors = []
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f'Corrupt ZIP member: {bad}')
        slides = sorted((n for n in archive.namelist()
                         if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                        key=lambda n: int(re.search(r'(\d+)\.xml$', n).group(1)))
        if len(slides) != expected_pages:
            errors.append(f'Expected {expected_pages} slides, found {len(slides)}')
        records = []
        for i, name in enumerate(slides, 1):
            tree = ET.fromstring(archive.read(name))
            texts = [t.text or '' for t in tree.findall('.//a:t', NS)]
            note_name = f'ppt/notesSlides/notesSlide{i}.xml'
            notes_text = []
            if note_name in archive.namelist():
                notes_tree = ET.fromstring(archive.read(note_name))
                for shape in notes_tree.findall('.//p:sp', NS):
                    placeholder = shape.find('.//p:ph', NS)
                    if placeholder is not None and placeholder.get('type') == 'body':
                        notes_text += [t.text or '' for t in shape.findall('.//a:t', NS)]
            if require_notes and not ''.join(notes_text).strip():
                errors.append(f'Slide {i}: speaker notes missing')
            records.append({'page': i, 'text_runs': len(texts),
                            'editable_text': bool(''.join(texts).strip()),
                            'pictures': len(tree.findall('.//p:pic', NS)),
                            'text': texts, 'notes_present': bool(''.join(notes_text).strip())})
    artifact_hash = sha256(path)
    render_status = 'not_checked'
    if render_dir:
        manifest = json.loads((render_dir / 'render-manifest.json').read_text(encoding='utf-8-sig'))
        if manifest.get('pptx_sha256') != artifact_hash:
            errors.append('Rendered images belong to a different PPTX')
        pages = manifest.get('pages', [])
        if [p.get('page') for p in pages] != list(range(1, expected_pages + 1)):
            errors.append('Render roster is missing, duplicated or out of order')
        for page in pages:
            image = (render_dir / page['file']).resolve()
            if not image.is_relative_to(render_dir.resolve()):
                raise ValueError('Render path escapes its directory')
            if not image.is_file() or sha256(image) != page.get('sha256'):
                errors.append(f'Render missing or changed: {page["file"]}')
        render_status = 'verified' if not errors else 'failed'
    return {'schema_version': 1, 'pptx_sha256': artifact_hash, 'pages': records,
            'structure_status': 'passed' if not errors else 'failed',
            'render_status': render_status, 'visual_review': 'requires_human_or_agent_inspection',
            'errors': errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', type=Path)
    parser.add_argument('--expected-pages', type=int, required=True)
    parser.add_argument('--render-dir', type=Path)
    parser.add_argument('--require-notes', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.expected_pages < 1:
            raise ValueError('expected-pages must be positive')
        result = audit(args.pptx, args.expected_pages, args.render_dir, args.require_notes)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if not result['errors'] else 1
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
