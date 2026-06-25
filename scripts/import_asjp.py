#!/usr/bin/env python3
"""
import_asjp.py — Convert an ASJP / CLDF Hiligaynon wordlist into lexicon TSV.

ASJP (https://asjp.clld.org) publishes Swadesh-style wordlists as concept→form
pairs. Each concept is an English gloss (e.g. "water", "two"), each form is the
Hiligaynon word. That maps directly onto our translation lexicon
(source_word=en gloss, hiligaynon=form), so it's the one openly machine-readable
translation source we can auto-import (the bilingual dictionaries are not).

Accepts the common JSON shapes:
  * a list of objects with concept/gloss + form/word/value keys
  * a dict with a "forms" or "wordlist" list of such objects
  * CLDF-ish records using "Parameter_ID"/"Gloss" + "Form"/"Value"

ASJP transcription uses a compressed alphabet; this strips the most common ASJP
symbols so forms read closer to normal orthography. Output STILL needs a native
speaker to verify spelling before trusting it — it is appended with a comment.

Pure standard library.

Usage:
    python scripts/import_asjp.py hiligaynon_asjp.json
    python scripts/import_asjp.py wl.json --append data/lexicon_hil.tsv --dry-run
"""

import argparse
import json
import re
import sys

CONCEPT_KEYS = ("concept", "gloss", "Gloss", "Parameter_ID", "parameter", "meaning")
FORM_KEYS = ("form", "word", "value", "Form", "Value", "transcription")

# ASJP-specific symbols to drop/simplify for readability.
ASJP_STRIP = str.maketrans("", "", "~$*\"")


def clean_form(form):
    f = form.strip().translate(ASJP_STRIP)
    f = re.sub(r"\s+", " ", f)
    # ASJP often lists variants separated by ',' or '/': take the first.
    f = re.split(r"[,/]", f)[0].strip()
    return f


def clean_concept(concept):
    # Concepts may look like "water" or "WATER" or "the water"; normalize.
    c = str(concept).strip().lower()
    c = re.sub(r"^(the|to|a)\s+", "", c)
    c = re.sub(r"[^a-z\- ]", "", c).strip()
    return c.replace(" ", "_") if " " in c else c


def first_key(d, keys):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None


def extract_records(data):
    """Yield dict records from the various accepted shapes."""
    if isinstance(data, list):
        yield from (r for r in data if isinstance(r, dict))
    elif isinstance(data, dict):
        for container in ("forms", "wordlist", "data", "rows"):
            if isinstance(data.get(container), list):
                yield from (r for r in data[container] if isinstance(r, dict))
                return
        # dict of concept -> form
        for k, v in data.items():
            if isinstance(v, str):
                yield {"concept": k, "form": v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file", help="ASJP/CLDF wordlist JSON")
    ap.add_argument("--append", default="data/lexicon_hil.tsv",
                    help="lexicon TSV to append to")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be added, don't write")
    args = ap.parse_args()

    try:
        with open(args.json_file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"cannot read {args.json_file}: {e}")

    pairs = []
    seen = set()
    for rec in extract_records(data):
        concept = first_key(rec, CONCEPT_KEYS)
        form = first_key(rec, FORM_KEYS)
        if concept is None or form is None:
            continue
        en = clean_concept(concept)
        hil = clean_form(str(form))
        if not en or not hil or en in seen:
            continue
        seen.add(en)
        pairs.append((en, hil))

    if not pairs:
        sys.exit("No concept/form pairs found — check the JSON shape "
                 "(expected concept+form keys).")

    lines = [f"{en}\t{hil}\ten" for en, hil in sorted(pairs)]
    print(f"Extracted {len(pairs)} concept->form pairs.")
    for ln in lines[:15]:
        print("  " + ln)
    if len(lines) > 15:
        print(f"  ... (+{len(lines) - 15} more)")

    if args.dry_run:
        print("\n(dry run — nothing written)")
        return

    with open(args.append, "a", encoding="utf-8") as f:
        f.write(f"\n# --- imported from ASJP ({args.json_file}); "
                f"VERIFY spellings with a native speaker ---\n")
        f.write("\n".join(lines) + "\n")
    print(f"\nAppended {len(lines)} entries to {args.append}. "
          "Have a native speaker verify before trusting them.")


if __name__ == "__main__":
    main()
