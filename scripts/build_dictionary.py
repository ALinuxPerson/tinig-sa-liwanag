#!/usr/bin/env python3
"""
build_dictionary.py — Build a LARGE en->hil lexicon from kaikki.org (Wiktionary).

kaikki.org publishes a machine-readable Hiligaynon dictionary extracted from
English Wiktionary (wiktextract), as JSONL — one word entry per line. Each entry
has a Hiligaynon headword plus English glosses, which is exactly the en->hil
mapping the translator needs. This dramatically reduces "*word*" gaps.

License: Wiktionary content is CC BY-SA — keep attribution if redistributing.

Writes data/lexicon_hil_auto.tsv, which scripts/translate_hil.py and app/server.py
load IN ADDITION to the hand-curated data/lexicon_hil.tsv (manual entries win).

Pure standard library. Network needed only to fetch; or pass a local --infile.

Usage:
    python scripts/build_dictionary.py                 # fetch + build
    python scripts/build_dictionary.py --infile hil.jsonl
    python scripts/build_dictionary.py --max-words 2   # only short glosses
"""

import argparse
import json
import os
import re
import sys
import urllib.request

KAIKKI_URL = ("https://kaikki.org/dictionary/Hiligaynon/"
              "kaikki.org-dictionary-Hiligaynon.jsonl")

STOP_GLOSS = re.compile(r"^(a|an|the|to|of)\s+", re.I)
# Glosses that are definitions/notes, not translations — skip.
SKIP_IF = ("(", "alternative", "obsolete", "archaic", "see ", "synonym")


def clean_gloss(gloss):
    """Turn an English gloss into a lookup key, or None if unusable."""
    g = gloss.strip().lower()
    for bad in SKIP_IF:
        if bad in g:
            return None
    g = STOP_GLOSS.sub("", g)
    g = re.sub(r"[^a-z\- ]", "", g).strip()
    return g or None


def iter_entries(stream):
    for line in stream:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def build(entries, max_words):
    """Return dict english_key -> hiligaynon word (first/shortest wins)."""
    lex = {}
    for e in entries:
        hil = (e.get("word") or "").strip()
        if not hil or e.get("lang", "Hiligaynon") != "Hiligaynon":
            continue
        for sense in e.get("senses", []):
            for gloss in sense.get("glosses", []):
                key = clean_gloss(gloss)
                if not key:
                    continue
                if max_words and len(key.split()) > max_words:
                    continue
                key_tsv = key.replace(" ", "_") if " " in key else key
                # Prefer the shorter Hiligaynon form when several map to one key.
                if key_tsv not in lex or len(hil) < len(lex[key_tsv]):
                    lex[key_tsv] = hil
    return lex


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", help="local kaikki JSONL (skip download)")
    ap.add_argument("--url", default=KAIKKI_URL)
    ap.add_argument("--out", default=os.path.join("data", "lexicon_hil_auto.tsv"))
    ap.add_argument("--max-words", type=int, default=2,
                    help="skip glosses longer than N words (0 = keep all)")
    args = ap.parse_args()

    if args.infile:
        if not os.path.exists(args.infile):
            sys.exit(f"no such file: {args.infile}")
        with open(args.infile, encoding="utf-8") as f:
            lex = build(iter_entries(f), args.max_words)
    else:
        print(f"Fetching {args.url}")
        try:
            req = urllib.request.Request(
                args.url, headers={"User-Agent": "Sugidanon/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                text = r.read().decode("utf-8", errors="replace")
        except Exception as e:
            sys.exit(f"download failed ({e}).\n"
                     "Download the JSONL manually from "
                     "https://kaikki.org/dictionary/Hiligaynon/ and pass --infile.")
        lex = build(iter_entries(text.splitlines()), args.max_words)

    if not lex:
        sys.exit("No entries extracted — check the JSONL source.")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# AUTO-GENERATED from kaikki.org (Wiktionary, CC BY-SA).\n"
                "# en -> hil. Regenerate: python scripts/build_dictionary.py\n"
                "# Hand-curated data/lexicon_hil.tsv overrides these at runtime.\n")
        for key in sorted(lex):
            f.write(f"{key}\t{lex[key]}\ten\n")

    print(f"Wrote {len(lex)} entries to {args.out}")
    print("Now run the translator/app — it loads this automatically.")


if __name__ == "__main__":
    main()
