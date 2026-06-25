#!/usr/bin/env python3
"""
validate.py — Check every annotation file conforms to SCHEMA.md.

Pure standard library. Verifies for each data/annotations/*.json:
  - required top-level keys present
  - valid `lang` values (hil | tl | en | other)
  - `idx` contiguous from 0
  - referenced audio_file exists on disk

Usage:
    python scripts/validate.py
    python scripts/validate.py --dir data/annotations --audio-root data
"""

import argparse
import json
import os
import sys

VALID_LANGS = {"hil", "tl", "en", "other"}
REQUIRED_KEYS = {"clip_id", "audio_file", "tokens"}
REQUIRED_TOKEN_KEYS = {"idx", "text", "lang"}


def validate_file(path, audio_root):
    """Return a list of error strings (empty = file is valid)."""
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"cannot read/parse: {e}"]

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")

    tokens = data.get("tokens", [])
    if not isinstance(tokens, list) or not tokens:
        errors.append("tokens must be a non-empty list")
        return errors

    for i, tok in enumerate(tokens):
        tmiss = REQUIRED_TOKEN_KEYS - tok.keys()
        if tmiss:
            errors.append(f"token {i}: missing {sorted(tmiss)}")
            continue
        if tok["lang"] not in VALID_LANGS:
            errors.append(f"token {i}: bad lang {tok['lang']!r}")
        if tok["idx"] != i:
            errors.append(f"token {i}: idx {tok['idx']} not contiguous (expected {i})")

    audio_file = data.get("audio_file")
    if audio_file:
        audio_path = os.path.join(audio_root, audio_file)
        if not os.path.exists(audio_path):
            errors.append(f"audio_file not found: {audio_path}")

    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/annotations",
                    help="directory of annotation JSON files")
    ap.add_argument("--audio-root", default="data",
                    help="root that audio_file paths are relative to")
    ap.add_argument("--no-audio-check", action="store_true",
                    help="skip the audio_file existence check")
    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        sys.exit(f"Not a directory: {args.dir}")

    files = sorted(f for f in os.listdir(args.dir) if f.endswith(".json"))
    if not files:
        sys.exit(f"No .json annotation files in {args.dir}")

    audio_root = os.devnull if args.no_audio_check else args.audio_root
    total_fail = 0
    for fn in files:
        path = os.path.join(args.dir, fn)
        if args.no_audio_check:
            # validate without touching disk for audio
            errs = [e for e in validate_file(path, args.audio_root)
                    if "audio_file not found" not in e]
        else:
            errs = validate_file(path, audio_root)
        if errs:
            total_fail += 1
            print(f"FAIL {fn}")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"OK   {fn}")

    print("-" * 40)
    print(f"{len(files) - total_fail}/{len(files)} files passed.")
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
