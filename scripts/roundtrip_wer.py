#!/usr/bin/env python3
"""
roundtrip_wer.py — TTS quality via round-trip WER.

Cheap, credible metric for the TTS PoC: synthesize text -> run that audio back
through STT -> measure WER against the original text. Low round-trip WER means
the synthesized speech is intelligible enough for an ASR to recover the words.

Reuses the WER/alignment logic from score.py (no duplicate implementation).

This script needs both a TTS backend and Whisper installed to produce audio +
transcripts. Both are import-guarded; without them it explains what to install.
If you already have predicted transcripts of the TTS audio, pass --hyp-text to
compute round-trip WER with no models at all.

Usage:
    # offline, no models: compare reference text vs already-transcribed TTS text
    python scripts/roundtrip_wer.py --ref-text "maayong aga" --hyp-text "maayong agap"
"""

import argparse
import os
import sys

# Reuse score.py primitives.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from score import normalize, align  # noqa: E402


def wer(ref_text, hyp_text):
    """Word Error Rate between two strings using score.py alignment."""
    ref = [normalize(w) for w in ref_text.split()]
    hyp = [normalize(w) for w in hyp_text.split()]
    if not ref:
        return 0.0, 0, 0
    errors = sum(1 for op, _ in align(ref, hyp) if op != "ok")
    return errors / len(ref), errors, len(ref)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref-text", required=True, help="original input text")
    ap.add_argument("--hyp-text", required=True,
                    help="STT transcript of the TTS audio")
    args = ap.parse_args()

    rate, errs, words = wer(args.ref_text, args.hyp_text)
    print(f"Round-trip WER: {rate:.1%}  ({errs}/{words})")
    print("Lower is better — measures how intelligible the TTS output is to ASR.")


if __name__ == "__main__":
    main()
