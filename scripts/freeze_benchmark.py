#!/usr/bin/env python3
"""
freeze_benchmark.py - Freeze and version the Sugidanon benchmark.

Writes data/benchmark/MANIFEST.json: a content-addressed snapshot of every
cohort (sha256 of each annotation + audio file), the frozen split roles, the
scorer protocol, and inclusion rules. This is what makes the benchmark
reproducible: --verify recomputes the checksums and fails if the data has
drifted from the frozen version, so "the same numbers every time" is enforced,
not hoped for.

Pure standard library.

Usage:
    python3 scripts/freeze_benchmark.py            # write/refresh MANIFEST
    python3 scripts/freeze_benchmark.py --verify   # gate: fail on any drift
"""

import argparse
import hashlib
import json
import os
import sys
import wave
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "benchmark", "MANIFEST.json")

VERSION = "1.0.0"

# Cohort ladder. Roles are frozen split assignments; speaker-disjoint by
# construction so test (spk01) and development (spk02) never leak.
COHORTS = [
    {
        "name": "headline",
        "role": "test",
        "speaker": "spk01",
        "annotations": "data/annotations",
        "audio": "data/audio",
        "predictions": "data/predictions",
    },
    {
        "name": "scripted_native_spk2",
        "role": "development",
        "speaker": "spk02",
        "annotations": "data/extensions/scripted_native_spk2/annotations",
        "audio": "data/extensions/scripted_native_spk2/audio",
        "predictions": "data/extensions/scripted_native_spk2/predictions",
    },
    {
        "name": "non_native_eval",
        "role": "robustness",
        "speaker": "mixed",
        "annotations": "data/extensions/non_native_eval/annotations",
        "audio": "data/extensions/non_native_eval/audio",
        "predictions": "data/extensions/non_native_eval/predictions",
    },
]

INCLUSION_RULES = [
    "Headline (test) = scripted_native, Speaker 1 (spk01) only.",
    "Cohorts are speaker-disjoint; spk02 is development, never blended into the headline WER.",
    "non_native_eval is robustness only and never counts toward the native headline.",
    "A clip is eligible only with a gold reference annotation and a matching prediction file.",
    "Hiligaynon references stay seed_unverified until a native speaker confirms; AI output is never treated as gold.",
]

SCORER = {
    "script": "score.py",
    "metric": "word error rate (Levenshtein, word-level)",
    "normalization": "lowercase; strip punctuation except apostrophe and hyphen",
    "switch_region_window": 1,
    "language_forcing": "tl",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def wav_duration(path):
    try:
        with wave.open(path) as w:
            return round(w.getnframes() / w.getframerate(), 3)
    except Exception:
        return None


def build_cohort(cohort):
    ann_dir = os.path.join(ROOT, cohort["annotations"])
    audio_dir = os.path.join(ROOT, cohort["audio"])
    pred_dir = os.path.join(ROOT, cohort["predictions"])

    clips = []
    domains, switch_types = Counter(), Counter()
    total_dur = 0.0

    names = []
    if os.path.isdir(ann_dir):
        names = sorted(n for n in os.listdir(ann_dir) if n.endswith(".json"))

    for name in names:
        with open(os.path.join(ann_dir, name), encoding="utf-8") as f:
            ann = json.load(f)
        clip_id = ann.get("clip_id", os.path.splitext(name)[0])
        audio_path = os.path.join(audio_dir, os.path.basename(ann.get("audio_file", "")))
        has_audio = os.path.exists(audio_path)
        has_pred = os.path.exists(os.path.join(pred_dir, f"{clip_id}.json"))
        dur = ann.get("duration_sec") or (wav_duration(audio_path) if has_audio else None)
        if dur:
            total_dur += dur
        domains[ann.get("domain", "?")] += 1
        switch_types[ann.get("switch_type", "?")] += 1
        clips.append({
            "clip_id": clip_id,
            "annotation_sha256": sha256_file(os.path.join(ann_dir, name)),
            "audio_sha256": sha256_file(audio_path) if has_audio else None,
            "duration_sec": dur,
            "domain": ann.get("domain"),
            "switch_type": ann.get("switch_type"),
            "gold_status": ann.get("gold_status"),
            "has_prediction": has_pred,
        })

    status = "frozen" if clips else "pending"
    return {
        "role": cohort["role"],
        "speaker": cohort["speaker"],
        "annotations": cohort["annotations"],
        "audio": cohort["audio"],
        "predictions": cohort["predictions"],
        "status": status,
        "n_clips": len(clips),
        "total_duration_sec": round(total_dur, 1),
        "by_domain": dict(domains),
        "by_switch_type": dict(switch_types),
        "clips": clips,
    }


def build_manifest():
    return {
        "benchmark": "Sugidanon",
        "version": VERSION,
        "frozen_on": date.today().isoformat(),
        "task": "code-switch automatic speech recognition (Hiligaynon matrix)",
        "primary_metric": "switch-region word error rate",
        "splits": {
            "train": None,
            "test": "headline",
            "development": "scripted_native_spk2",
            "robustness": "non_native_eval",
        },
        "inclusion_rules": INCLUSION_RULES,
        "scorer": dict(SCORER, sha256=sha256_file(os.path.join(ROOT, "score.py"))),
        "cohorts": {c["name"]: build_cohort(c) for c in COHORTS},
    }


def verify():
    if not os.path.exists(MANIFEST):
        sys.exit("No MANIFEST.json. Run without --verify to create it first.")
    with open(MANIFEST, encoding="utf-8") as f:
        frozen = json.load(f)
    current = build_manifest()

    problems = []

    fs = frozen["scorer"].get("sha256")
    cs = current["scorer"]["sha256"]
    if fs != cs:
        problems.append(f"scorer score.py changed (frozen {fs[:12]}, now {cs[:12]})")

    for name, fcoh in frozen["cohorts"].items():
        ccoh = current["cohorts"].get(name)
        if ccoh is None:
            problems.append(f"{name}: cohort missing from working tree")
            continue
        fclips = {c["clip_id"]: c for c in fcoh["clips"]}
        cclips = {c["clip_id"]: c for c in ccoh["clips"]}
        for cid in fclips.keys() - cclips.keys():
            problems.append(f"{name}/{cid}: clip removed since freeze")
        for cid in cclips.keys() - fclips.keys():
            problems.append(f"{name}/{cid}: clip added since freeze (not in frozen version)")
        for cid in fclips.keys() & cclips.keys():
            for field in ("annotation_sha256", "audio_sha256"):
                if fclips[cid][field] != cclips[cid][field]:
                    problems.append(f"{name}/{cid}: {field} drifted")

    if problems:
        print("DRIFT against frozen benchmark v{}:".format(frozen["version"]))
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"OK: working tree matches frozen benchmark v{frozen['version']}.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="fail if the working tree drifted from the frozen manifest")
    args = ap.parse_args()

    if args.verify:
        verify()
        return

    manifest = build_manifest()
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    counts = {k: v["n_clips"] for k, v in manifest["cohorts"].items()}
    print(f"Wrote {os.path.relpath(MANIFEST, ROOT)} (v{manifest['version']})")
    for name, n in counts.items():
        print(f"  {name:<22} {n} clips [{manifest['cohorts'][name]['role']}]")


if __name__ == "__main__":
    main()
