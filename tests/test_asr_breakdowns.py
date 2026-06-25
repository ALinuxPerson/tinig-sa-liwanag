import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_asr_breakdowns.py"
SPEC = importlib.util.spec_from_file_location("analyze_asr_breakdowns", SCRIPT)
breakdowns = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(breakdowns)


class AsrBreakdownsTest(unittest.TestCase):
    def test_scores_clip_and_token_language_buckets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            ref_dir = root / "ref"
            hyp_dir = root / "hyp"
            ref_dir.mkdir()
            hyp_dir.mkdir()
            (ref_dir / "clip_001.json").write_text(
                json.dumps({
                    "clip_id": "clip_001",
                    "domain": "market",
                    "switch_type": "HIL+EN",
                    "speaker": {"id": "spk_test"},
                    "tokens": [
                        {"text": "Pila", "lang": "hil"},
                        {"text": "budget", "lang": "en"},
                    ],
                }),
                encoding="utf-8",
            )
            (hyp_dir / "clip_001.json").write_text(
                json.dumps({"text": "pila extra badyet"}),
                encoding="utf-8",
            )

            summary = breakdowns.summary_to_json(
                breakdowns.score_one_dataset("test", ref_dir, hyp_dir)
            )

        self.assertEqual(summary["clip_count"], 1)
        self.assertEqual(summary["overall"]["errors"], 2)
        self.assertEqual(summary["by_speaker"]["spk_test"]["errors"], 2)
        self.assertEqual(summary["by_domain"]["market"]["clips"], 1)
        self.assertEqual(summary["by_token_language"]["en"]["errors"], 1)
        self.assertEqual(summary["by_token_language"]["hil"]["errors"], 0)
        self.assertEqual(summary["unattributed_token_language_insertions"], 1)


if __name__ == "__main__":
    unittest.main()
