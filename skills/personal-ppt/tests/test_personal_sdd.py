import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'personal.py'
SPEC = importlib.util.spec_from_file_location('personal_ppt', SCRIPT)
PERSONAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PERSONAL)


class PersonalSddTests(unittest.TestCase):
    def make_job(self, root):
        source = root / 'facts.md'
        source.write_text('Only local facts.', encoding='utf-8')
        selection = PERSONAL.resolve('general', 'clean')
        job = root / 'job'
        PERSONAL.init_job(job, 'Test deck', selection, [source])
        return job

    def approve_and_complete(self, spec_path):
        text = spec_path.read_text(encoding='utf-8').replace(
            'Status: draft', 'Status: approved', 1)
        for field in PERSONAL.UNRESOLVED_SPEC_FIELDS:
            text = text.replace(field, field + ' Completed for test.', 1)
        spec_path.write_text(text, encoding='utf-8')

    def test_new_spec_is_draft_and_not_ready(self):
        with tempfile.TemporaryDirectory() as temporary:
            job = self.make_job(Path(temporary))
            result = PERSONAL.init_spec(job)
            self.assertEqual(result['status'], 'draft')
            check = PERSONAL.check_sdd(job)
            self.assertFalse(check['ready_to_generate'])
            self.assertEqual(check['status'], 'draft')
            self.assertTrue(check['required_sections_present'])
            self.assertIn('Target page count:', check['unresolved_fields'])

    def test_approved_complete_spec_is_ready(self):
        with tempfile.TemporaryDirectory() as temporary:
            job = self.make_job(Path(temporary))
            PERSONAL.init_spec(job)
            spec_path = job / 'spec.md'
            self.approve_and_complete(spec_path)
            check = PERSONAL.check_sdd(job)
            self.assertTrue(check['ready_to_generate'])
            self.assertEqual(check['missing_sections'], [])
            self.assertEqual(check['unresolved_fields'], [])

    def test_missing_section_blocks_generation(self):
        with tempfile.TemporaryDirectory() as temporary:
            job = self.make_job(Path(temporary))
            (job / 'spec.md').write_text('Status: approved\n\n## Intent\n\nFilled.\n', encoding='utf-8')
            check = PERSONAL.check_sdd(job)
            self.assertFalse(check['ready_to_generate'])
            self.assertIn('Deck plan', check['missing_sections'])


if __name__ == '__main__':
    unittest.main()
