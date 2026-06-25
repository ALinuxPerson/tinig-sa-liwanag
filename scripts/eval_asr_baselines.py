#!/usr/bin/env python3
"""
One-command ASR baseline evaluation.

Runs the existing switch-region WER scorer over every baseline prediction
directory in data/predictions/asr/.

Usage:
    python3 scripts/eval_asr_baselines.py
    python3 scripts/eval_asr_baselines.py --ref data/annotations
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import score  # noqa: E402


def iter_pairs(ref_dir, hyp_dir):
    for fn in sorted(os.listdir(ref_dir)):
        if not fn.endswith(".json"):
            continue
        ref_path = os.path.join(ref_dir, fn)
        hyp_path = os.path.join(hyp_dir, fn)
        if os.path.exists(hyp_path):
            yield ref_path, hyp_path


def score_model(ref_dir, hyp_dir):
    totals = {
        "overall": score.Counts(),
        "switch": score.Counts(),
        "mono": score.Counts(),
    }
    pair_buckets = {}
    clips = 0

    for ref_path, hyp_path in iter_pairs(ref_dir, hyp_dir):
        ref_tokens, langs = score.load_reference(ref_path)
        hyp_tokens = score.load_hypothesis(hyp_path)
        overall, switch, mono = score.score_clip(ref_tokens, langs, hyp_tokens, pair_buckets)
        for name, one in (("overall", overall), ("switch", switch), ("mono", mono)):
            totals[name].errors += one.errors
            totals[name].words += one.words
        clips += 1

    return clips, totals, pair_buckets


def pct(value):
    return f"{value * 100:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default=os.path.join(ROOT, "data", "annotations"))
    ap.add_argument("--pred-root", default=os.path.join(ROOT, "data", "predictions", "asr"))
    args = ap.parse_args()

    if not os.path.isdir(args.ref):
        sys.exit(f"Reference directory not found: {args.ref}")
    if not os.path.isdir(args.pred_root):
        sys.exit(f"Prediction root not found: {args.pred_root}")

    models = [
        name for name in sorted(os.listdir(args.pred_root))
        if os.path.isdir(os.path.join(args.pred_root, name))
    ]
    if not models:
        sys.exit(f"No model prediction directories found under {args.pred_root}")

    print("ASR baseline WER")
    print("Reference:", os.path.relpath(args.ref, ROOT))
    print()
    print(f"{'model':<24}{'clips':>7}{'overall':>12}{'switch':>12}{'mono':>12}{'switch penalty':>17}")
    print("-" * 84)

    had_missing = False
    for model in models:
        hyp_dir = os.path.join(args.pred_root, model)
        clips, totals, _ = score_model(args.ref, hyp_dir)
        if clips == 0:
            had_missing = True
            print(f"{model:<24}{0:>7}{'MISSING':>12}{'MISSING':>12}{'MISSING':>12}{'MISSING':>17}")
            continue

        overall = totals["overall"].wer()
        switch = totals["switch"].wer()
        mono = totals["mono"].wer()
        penalty = switch - mono if totals["mono"].words else 0.0
        print(
            f"{model:<24}{clips:>7}"
            f"{pct(overall):>12}{pct(switch):>12}{pct(mono):>12}{pct(penalty):>17}"
        )

    print()
    print("Notes:")
    print("- Current repository predictions are worked examples, not final benchmark results.")
    print("- Replace data/predictions/asr/<model>/*.json with real Whisper/MMS outputs to reproduce final reported WER.")
    print("- The scorer reports switch-region WER, monolingual WER, and switch penalty.")

    sys.exit(1 if had_missing else 0)


if __name__ == "__main__":
    main()
