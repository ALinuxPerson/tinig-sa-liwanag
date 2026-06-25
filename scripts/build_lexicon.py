#!/usr/bin/env python3
"""
build_lexicon.py — Fetch open, machine-readable pronunciation lexicons.

These power the *pronunciation* side (G2P for the TTS router), NOT the
translation lexicon. Translation pairs (en/tl -> hil) are inherently bilingual
and must be curated by hand into data/lexicon_hil.tsv from sources like Kaufmann
KVED / Motus / pinoydictionary (see RESOURCES.md).

What this fetches (all openly licensed, machine-readable):
  cmudict   English word -> ARPABET phonemes (~134k). MIT-style license.
            -> data/cmudict.txt   (English G2P + valid-English-word set)
  wikipron  Tagalog word -> IPA phonemes. CC0/CC-BY.
            -> data/wikipron_tl.tsv

Network is required only when you run this. Output files are gitignored data
artifacts. Uses only the standard library (urllib).

Usage:
    python scripts/build_lexicon.py --which cmudict
    python scripts/build_lexicon.py --which all --out-dir data
"""

import argparse
import os
import sys
import urllib.request

SOURCES = {
    "cmudict": (
        "https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict",
        "cmudict.txt",
    ),
    "wikipron_tl": (
        "https://raw.githubusercontent.com/CUNY-CL/wikipron/master/data/scrape/tsv/tgl_latn_broad.tsv",
        "wikipron_tl.tsv",
    ),
}


def fetch(url, dst):
    print(f"  GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Sugidanon/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(dst, "wb") as f:
        f.write(data)
    print(f"  -> wrote {dst} ({len(data)} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", choices=["cmudict", "wikipron_tl", "all"],
                    default="cmudict")
    ap.add_argument("--out-dir", default="data")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    targets = SOURCES.keys() if args.which == "all" else [args.which]

    failed = 0
    for key in targets:
        url, fname = SOURCES[key]
        dst = os.path.join(args.out_dir, fname)
        print(f"[{key}]")
        try:
            fetch(url, dst)
        except Exception as e:  # network / URL issues are expected offline
            failed += 1
            print(f"  FAILED: {e}", file=sys.stderr)
    if failed:
        print(f"\n{failed} source(s) failed (offline? URL moved?). "
              "These are optional pronunciation aids.", file=sys.stderr)
        sys.exit(1)
    print("\nDone. These feed the G2P/TTS path; translation pairs still go in "
          "data/lexicon_hil.tsv by hand.")


if __name__ == "__main__":
    main()
