#!/usr/bin/env python3
"""
validate.py - Check benchmark files against SCHEMA.md.

Primary v1 mode validates translation benchmark JSONL files in data/benchmark.
Legacy ASR mode still validates data/annotations/*.json for future speech work.

Usage:
    python3 scripts/validate.py --kind translation --dir data/benchmark
    python3 scripts/validate.py --kind asr --dir data/annotations --no-audio-check
"""

import argparse
import json
import os
import sys

VALID_LANGS = {"hil", "tl", "en", "other", None}
VALID_FLUENCY = {"native", "fluent", "non_native"}
VALID_SOURCE_LANGS = {"en", "fil", "tl", "hil", "mixed"}
VALID_DIFFICULTY = {"easy", "medium", "hard"}
VALID_REVIEW_STATUS = {"seed_unverified", "reviewed", "adjudicated"}
REQUIRED_TRANSLATION_KEYS = {
    "id",
    "source_lang",
    "target_lang",
    "domain",
    "source_text",
    "reference_translation",
    "context",
    "phenomena",
    "difficulty",
    "review_status",
}
REQUIRED_ASR_KEYS = {"clip_id", "audio_file", "tokens"}
REQUIRED_TOKEN_KEYS = {"idx", "text", "lang"}


def validate_translation_file(path):
    """Return a list of error strings for a translation JSONL file."""
    errors = []
    seen_ids = set()
    try:
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"line {lineno}: invalid JSON: {e}")
                    continue

                missing = REQUIRED_TRANSLATION_KEYS - row.keys()
                if missing:
                    errors.append(f"line {lineno}: missing keys: {sorted(missing)}")
                    continue

                rid = row["id"]
                if not isinstance(rid, str) or not rid:
                    errors.append(f"line {lineno}: id must be a non-empty string")
                elif rid in seen_ids:
                    errors.append(f"line {lineno}: duplicate id {rid!r}")
                else:
                    seen_ids.add(rid)

                if row["source_lang"] not in VALID_SOURCE_LANGS:
                    errors.append(f"line {lineno}: bad source_lang {row['source_lang']!r}")
                if row["target_lang"] != "hil":
                    errors.append(f"line {lineno}: target_lang must be 'hil'")
                if row["difficulty"] not in VALID_DIFFICULTY:
                    errors.append(f"line {lineno}: bad difficulty {row['difficulty']!r}")
                if row["review_status"] not in VALID_REVIEW_STATUS:
                    errors.append(f"line {lineno}: bad review_status {row['review_status']!r}")
                if not isinstance(row["phenomena"], list) or not row["phenomena"]:
                    errors.append(f"line {lineno}: phenomena must be a non-empty list")

                for key in ("domain", "source_text", "reference_translation", "context"):
                    if not isinstance(row[key], str) or not row[key].strip():
                        errors.append(f"line {lineno}: {key} must be a non-empty string")
    except OSError as e:
        return [f"cannot read: {e}"]

    if not seen_ids and not errors:
        errors.append("file has no JSONL rows")
    return errors


def validate_asr_file(path, audio_root):
    """Return a list of error strings (empty = file is valid)."""
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"cannot read/parse: {e}"]

    missing = REQUIRED_ASR_KEYS - data.keys()
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

    speaker = data.get("speaker")
    if isinstance(speaker, dict) and "fluency" in speaker:
        if speaker["fluency"] not in VALID_FLUENCY:
            errors.append(f"bad speaker.fluency {speaker['fluency']!r} "
                          f"(use {sorted(VALID_FLUENCY)})")

    audio_file = data.get("audio_file")
    if audio_file:
        audio_path = os.path.join(audio_root, audio_file)
        if not os.path.exists(audio_path):
            errors.append(f"audio_file not found: {audio_path}")

    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["translation", "asr"], default="translation",
                    help="schema to validate")
    ap.add_argument("--dir", default=None,
                    help="directory of benchmark JSONL files or ASR annotation JSON files")
    ap.add_argument("--audio-root", default="data",
                    help="root that audio_file paths are relative to")
    ap.add_argument("--no-audio-check", action="store_true",
                    help="skip the audio_file existence check")
    args = ap.parse_args()

    if args.dir is None:
        args.dir = "data/benchmark" if args.kind == "translation" else "data/annotations"

    if not os.path.isdir(args.dir):
        sys.exit(f"Not a directory: {args.dir}")

    suffix = ".jsonl" if args.kind == "translation" else ".json"
    files = sorted(f for f in os.listdir(args.dir) if f.endswith(suffix))
    if not files:
        sys.exit(f"No {suffix} files in {args.dir}")

    audio_root = os.devnull if args.no_audio_check else args.audio_root
    total_fail = 0
    for fn in files:
        path = os.path.join(args.dir, fn)
        if args.kind == "translation":
            errs = validate_translation_file(path)
        elif args.no_audio_check:
            # validate without touching disk for audio
            errs = [e for e in validate_asr_file(path, args.audio_root)
                    if "audio_file not found" not in e]
        else:
            errs = validate_asr_file(path, audio_root)
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
