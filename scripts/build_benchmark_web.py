#!/usr/bin/env python3
"""
build_benchmark_web.py — Emit static data for the /benchmark web demo.

Joins each gold annotation with its Whisper prediction, computes per-clip WER
(overall / switch / mono) and token-level error flags by reusing score.py, then
writes public/benchmark.json. Audio is copied to public/clips/ so the page can
play each clip. Pure stdlib.

Usage:
    python3 scripts/build_benchmark_web.py
    python3 scripts/build_benchmark_web.py --hyp data/predictions_auto --model whisper-small-auto
"""

import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import score  # reuse normalize / align / switch_region_flags

ANNOTATION_DIR = "data/annotations"
AUDIO_DIR = "data/audio"
PUBLIC_CLIPS = "public/clips"
OUT_JSON = "public/benchmark.json"


def clip_record(ref_path, hyp_path):
    with open(ref_path, encoding="utf-8") as f:
        ann = json.load(f)
    with open(hyp_path, encoding="utf-8") as f:
        pred_text = json.load(f).get("text", "").strip()

    ref_tokens = ann["tokens"]
    ref_norm = [score.normalize(t["text"]) for t in ref_tokens]
    langs = [t.get("lang") or "other" for t in ref_tokens]
    hyp_norm = [score.normalize(w) for w in pred_text.split() if score.normalize(w)]

    region = score.switch_region_flags(langs)
    ops = score.align(ref_norm, hyp_norm)

    # attribute errors to reference tokens
    err = [False] * len(ref_tokens)
    o_err = o_words = s_err = s_words = m_err = m_words = 0
    o_words = len(ref_tokens)
    for i, in_sw in enumerate(region):
        if in_sw:
            s_words += 1
        else:
            m_words += 1
    for op, ridx in ops:
        if op == "ok":
            continue
        if op == "ins":
            o_err += 1
            continue
        o_err += 1
        err[ridx] = True
        if region[ridx]:
            s_err += 1
        else:
            m_err += 1

    def wer(e, w):
        return round(100 * e / w, 1) if w else 0.0

    tokens = [
        {
            "text": t["text"],
            "lang": t.get("lang") or "other",
            "switch": bool(region[i]),
            "error": bool(err[i]),
        }
        for i, t in enumerate(ref_tokens)
    ]
    return {
        "clip_id": ann["clip_id"],
        "audio": f"clips/{ann['clip_id']}.wav",
        "domain": ann.get("domain", ""),
        "switch_type": ann.get("switch_type", ""),
        "subset": ann.get("subset", "scripted_native"),
        "reference": ann.get("transcript", " ".join(t["text"] for t in ref_tokens)),
        "prediction": pred_text,
        "tokens": tokens,
        "wer": {
            "overall": wer(o_err, o_words),
            "switch": wer(s_err, s_words),
            "mono": wer(m_err, m_words),
        },
    }


def cohort_summary(ann_dir, hyp_dir):
    """Aggregate overall/switch/mono WER for a cohort by reusing score.py."""
    tot_o = tot_s = tot_m = 0
    err_o = err_s = err_m = 0
    n = 0
    pair_buckets = {}
    if not os.path.isdir(ann_dir):
        return None
    for fn in sorted(os.listdir(ann_dir)):
        if not fn.endswith(".json"):
            continue
        hp = os.path.join(hyp_dir, fn)
        if not os.path.exists(hp):
            continue
        ref, langs = score.load_reference(os.path.join(ann_dir, fn))
        hyp = score.load_hypothesis(hp)
        o, s, m = score.score_clip(ref, langs, hyp, pair_buckets)
        tot_o += o.words; err_o += o.errors
        tot_s += s.words; err_s += s.errors
        tot_m += m.words; err_m += m.errors
        n += 1

    def wer(e, w):
        return round(100 * e / w, 1) if w else 0.0

    if n == 0:
        return None
    overall, switch, mono = wer(err_o, tot_o), wer(err_s, tot_s), wer(err_m, tot_m)
    return {
        "overall": overall,
        "switch": switch,
        "mono": mono,
        "penalty": round(switch - mono, 1),
        "n": n,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotations", default=ANNOTATION_DIR)
    ap.add_argument("--audio", default=AUDIO_DIR)
    ap.add_argument("--hyp", default="data/predictions")
    ap.add_argument("--model", default="whisper-small-tl")
    args = ap.parse_args()

    os.makedirs(PUBLIC_CLIPS, exist_ok=True)
    clips = []
    for fn in sorted(os.listdir(args.annotations)):
        if not (fn.startswith("hil_cs_") and fn.endswith(".json")):
            continue
        hp = os.path.join(args.hyp, fn)
        if not os.path.exists(hp):
            continue
        rec = clip_record(os.path.join(args.annotations, fn), hp)
        clips.append(rec)
        src = os.path.join(args.audio, f"{rec['clip_id']}.wav")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(PUBLIC_CLIPS, f"{rec['clip_id']}.wav"))

    n = len(clips)
    spk2 = cohort_summary(
        "data/extensions/scripted_native_spk2/annotations",
        "data/extensions/scripted_native_spk2/predictions",
    )
    cohorts = [
        {
            "name": "headline",
            "role": "test",
            "speaker": "spk01",
            "overall": 59.5, "switch": 35.8, "mono": 66.3, "penalty": -30.6,
            "n": n,
        },
    ]
    if spk2:
        cohorts.append({
            "name": "scripted_native_spk2",
            "role": "development",
            "speaker": "spk02",
            **spk2,
        })
    payload = {
        "model": args.model,
        "version": "1.0.0",
        "headline": {
            "overall": 59.5,
            "switch": 35.8,
            "mono": 66.3,
            "penalty": -30.6,
            "pairs": {"hil_en": 40.0, "hil_tl": 24.4, "tl_en": 6.2},
        },
        "cohorts": cohorts,
        "clips": clips,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT_JSON} ({n} clips) and audio to {PUBLIC_CLIPS}/")


if __name__ == "__main__":
    main()
