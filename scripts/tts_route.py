#!/usr/bin/env python3
"""
tts_route.py — Per-word language router for code-switched TTS (PoC).

Tags each word of a code-switched Hiligaynon-Tagalog-English sentence, then
routes it down the right synthesis path so pronunciation doesn't collapse:
  - hil / tl words -> Hiligaynon G2P (g2p_hil) -> phoneme-input TTS path
  - en words       -> English TTS path

The actual TTS backend (MMS-TTS / Coqui / F5-TTS) is OPTIONAL and import-guarded.
Without it, this script still prints the routing + phoneme plan (the PoC value),
and only synthesizes audio when a backend is installed.

Language tagging here is a lightweight lexicon/heuristic stub — the gold tags
come from human annotators per SCHEMA.md. This router is for *inference-time*
synthesis, not for building the benchmark labels.

Usage:
    python scripts/tts_route.py "Nag-grocery ko kahapon kay super traffic"
    python scripts/tts_route.py --infile data/tts_samples.txt --out-dir out/tts
"""

import argparse
import os
import sys

# Make g2p_hil importable when run from repo root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from g2p_hil import g2p  # noqa: E402

try:
    # Any phoneme/multilingual TTS backend can slot in here.
    import TTS  # type: ignore  # Coqui  # noqa: F401
    HAVE_TTS = True
except ImportError:
    HAVE_TTS = False

# Tiny heuristic lexicon for the PoC router. Real labels come from annotators.
EN_HINT = {
    "grocery", "traffic", "late", "meeting", "online", "deadline", "okay",
    "weekend", "load", "signal", "phone", "laptop", "i", "was", "the", "and",
}
TL_HINT = {"super", "talaga", "kasi", "naman", "grabe", "ang", "ng", "sobrang"}


def tag_word(word):
    """Return 'en', 'tl', or 'hil' for a single token (heuristic PoC)."""
    w = word.lower().strip(".,!?")
    if w in EN_HINT:
        return "en"
    if w in TL_HINT:
        return "tl"
    return "hil"


def route_sentence(text):
    """Return a list of (word, lang, path, phonemes_or_None)."""
    plan = []
    for word in text.split():
        lang = tag_word(word)
        if lang == "en":
            plan.append((word, lang, "english-tts", None))
        else:  # hil or tl -> Hiligaynon G2P path
            plan.append((word, lang, "hil-g2p-tts", g2p(word)))
    return plan


def synthesize(plan, out_path):
    """Synthesize audio if a TTS backend is present; else no-op with a note."""
    if not HAVE_TTS:
        print(f"  (TTS backend not installed -> skipping audio for {out_path})")
        return False
    # Backend-specific synthesis would go here, concatenating per-word segments.
    # Left as an integration point for whichever model the team installs
    # (e.g. multilingual-tts/F5-TTS-OpenBible-Hiligaynon for the hil path).
    raise NotImplementedError("Wire your installed TTS backend here.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="*", help="sentence to route")
    ap.add_argument("--infile", help="file with one sentence per line")
    ap.add_argument("--out-dir", default="out/tts")
    args = ap.parse_args()

    if args.infile:
        with open(args.infile, encoding="utf-8") as f:
            sentences = [ln.strip() for ln in f
                         if ln.strip() and not ln.startswith("#")]
    elif args.text:
        sentences = [" ".join(args.text)]
    else:
        sys.exit("Provide a sentence or --infile.")

    os.makedirs(args.out_dir, exist_ok=True)
    for n, sent in enumerate(sentences, 1):
        print(f"\n[{n}] {sent}")
        for word, lang, path, phon in route_sentence(sent):
            ph = f"  ->  /{phon}/" if phon else ""
            print(f"    {word:<16} [{lang}] {path}{ph}")
        synthesize(route_sentence(sent), os.path.join(args.out_dir, f"tts_{n:03d}.wav"))


if __name__ == "__main__":
    main()
