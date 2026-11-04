import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / 'skills' / 'personal-ppt' / 'scripts' / 'release.py'


class ReleasePackagingTests(unittest.TestCase):
    def test_release_uses_verifiable_engine_source_when_pin_is_not_local(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / 'personal-ppt.zip'
            result = subprocess.run(
                [sys.executable, str(RELEASE), '--output', str(archive)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['kind'], 'source-only')
            with zipfile.ZipFile(archive) as package:
                self.assertIn('skills/personal-ppt/references/spec-sdd.md', package.namelist())


if __name__ == '__main__':
    unittest.main()
