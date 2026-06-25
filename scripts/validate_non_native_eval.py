#!/usr/bin/env python3
"""
Validate non_native_eval scaffold/readiness.

This subset can be planned without checked-in audio. Once annotations/audio are
added, this script enforces quarantine rules so non-native clips cannot be
mistaken for native-gold headline data.
"""

import argparse
import csv
import json
import os
import sys
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIR = ROOT / "data" / "extensions" / "non_native_eval"
VALID_REVIEW = {"seed_unverified", "reviewed", "adjudicated"}


def read_manifest(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    errors = []
    seen = set()
    for row in rows:
        clip_id = row.get("clip_id", "")
        if not clip_id:
            errors.append("manifest row missing clip_id")
            continue
        if clip_id in seen:
            errors.append(f"duplicate manifest clip_id: {clip_id}")
        seen.add(clip_id)
        if not clip_id.startswith("nonnat_"):
            errors.append(f"{clip_id}: clip_id must start with nonnat_")
        if row.get("speaker_fluency") != "non_native":
            errors.append(f"{clip_id}: speaker_fluency must be non_native")
        if row.get("review_status") not in VALID_REVIEW:
            errors.append(f"{clip_id}: bad review_status {row.get('review_status')!r}")
    return rows, errors


def check_wav(path):
    with wave.open(str(path)) as w:
        return {
            "sample_rate": w.getframerate(),
            "channels": w.getnchannels(),
            "sample_width": w.getsampwidth(),
            "duration": w.getnframes() / w.getframerate(),
        }


def validate_annotation(path, subset_dir, manifest_ids):
    errors = []
    with open(path, encoding="utf-8") as f:
        row = json.load(f)
    clip_id = row.get("clip_id")
    if clip_id not in manifest_ids:
        errors.append(f"{path.name}: clip_id not in manifest: {clip_id}")
    if row.get("subset") != "non_native_eval":
        errors.append(f"{clip_id}: subset must be non_native_eval")
    if row.get("source_type") != "non_native_recording":
        errors.append(f"{clip_id}: source_type must be non_native_recording")
    if row.get("gold_status") != "not_native_gold":
        errors.append(f"{clip_id}: gold_status must be not_native_gold")
    if row.get("review_status") not in VALID_REVIEW:
        errors.append(f"{clip_id}: bad review_status {row.get('review_status')!r}")
    if row.get("lang_tags_status") not in VALID_REVIEW:
        errors.append(f"{clip_id}: bad lang_tags_status {row.get('lang_tags_status')!r}")
    speaker = row.get("speaker", {})
    if speaker.get("fluency") != "non_native":
        errors.append(f"{clip_id}: speaker.fluency must be non_native")

    audio_file = row.get("audio_file", "")
    audio_path = subset_dir / audio_file
    if not audio_file or not audio_path.exists():
        errors.append(f"{clip_id}: missing audio file {audio_file!r}")
    else:
        info = check_wav(audio_path)
        if info["sample_rate"] != 16000:
            errors.append(f"{clip_id}: sample_rate must be 16000")
        if info["channels"] != 1:
            errors.append(f"{clip_id}: channels must be 1")
        if info["sample_width"] != 2:
            errors.append(f"{clip_id}: sample_width must be 2 bytes")
        if not 3.0 <= info["duration"] <= 20.0:
            errors.append(f"{clip_id}: duration outside 3-20s")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(DEFAULT_DIR))
    ap.add_argument("--expected", type=int, default=20)
    args = ap.parse_args()

    subset_dir = Path(args.dir)
    manifest = subset_dir / "manifest.csv"
    if not manifest.exists():
        sys.exit(f"missing manifest: {manifest}")

    rows, errors = read_manifest(manifest)
    if len(rows) != args.expected:
        errors.append(f"manifest has {len(rows)} rows, expected {args.expected}")
    manifest_ids = {row["clip_id"] for row in rows}

    ann_dir = subset_dir / "annotations"
    audio_dir = subset_dir / "audio"
    annotations = sorted(path for path in ann_dir.glob("*.json"))
    audio = sorted(path for path in audio_dir.glob("*.wav"))

    for path in annotations:
        errors.extend(validate_annotation(path, subset_dir, manifest_ids))

    extra_audio = {
        path.stem for path in audio
    } - manifest_ids
    for clip_id in sorted(extra_audio):
        errors.append(f"audio not in manifest: {clip_id}")

    print(f"manifest_rows={len(rows)}")
    print(f"annotations={len(annotations)}")
    print(f"audio={len(audio)}")
    if not annotations and not audio:
        print("status=planned_only")
    elif len(annotations) == args.expected and len(audio) == args.expected:
        print("status=ready_for_review_or_scoring")
    else:
        print("status=incomplete")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
