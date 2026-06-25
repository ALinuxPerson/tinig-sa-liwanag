import csv
import os
import subprocess
import unittest


ROOT = os.path.dirname(os.path.dirname(__file__))
NON_NATIVE = os.path.join(ROOT, "data", "extensions", "non_native_eval")
PRIMARY_ANNOTATIONS = os.path.join(ROOT, "data", "annotations")


class NonNativeEvalTest(unittest.TestCase):
    def test_manifest_has_20_quarantined_slots(self):
        manifest = os.path.join(NON_NATIVE, "manifest.csv")
        with open(manifest, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 20)
        self.assertEqual({row["speaker_fluency"] for row in rows}, {"non_native"})
        self.assertEqual({row["recording_status"] for row in rows}, {"planned"})
        self.assertTrue(all(row["clip_id"].startswith("nonnat_") for row in rows))

    def test_non_native_not_in_primary_annotations(self):
        names = os.listdir(PRIMARY_ANNOTATIONS)
        self.assertFalse(any(name.startswith("nonnat_") for name in names))

    def test_readiness_validator_accepts_planned_only_state(self):
        proc = subprocess.run(
            ["python3", "scripts/validate_non_native_eval.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("manifest_rows=20", proc.stdout)
        self.assertIn("status=planned_only", proc.stdout)


if __name__ == "__main__":
    unittest.main()
