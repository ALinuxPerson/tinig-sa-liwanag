#!/usr/bin/env python3
"""
Generate richer ASR benchmark breakdowns for Sugidanon.

The canonical scorer remains score.py. This script reuses the same
normalization, alignment, switch-region, and pair-bucket logic, then adds
clip-level and token-level slices for dataset growth decisions.

Usage:
    python3 scripts/analyze_asr_breakdowns.py \
      --dataset headline:data/annotations:data/predictions \
      --dataset spk2:data/extensions/scripted_native_spk2/annotations:data/extensions/scripted_native_spk2/predictions \
      --out-json results/asr_breakdowns.json \
      --out-md results/asr_breakdowns.md
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Set

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import score  # noqa: E402


@dataclass
class Bucket:
    errors: int = 0
    words: int = 0
    clips: Set[str] = field(default_factory=set)

    def add(self, errors=0, words=0, clip_id=None):
        self.errors += errors
        self.words += words
        if clip_id:
            self.clips.add(clip_id)

    def metric(self):
        return {
            "wer": self.errors / self.words if self.words else 0.0,
            "errors": self.errors,
            "words": self.words,
            "clips": len(self.clips),
        }


def parse_dataset(value):
    parts = value.split(":", 2)
    if len(parts) != 3 or not all(parts):
        raise argparse.ArgumentTypeError(
            "dataset must be NAME:REF_DIR:HYP_DIR"
        )
    name, ref_dir, hyp_dir = parts
    return name, Path(ref_dir), Path(hyp_dir)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def iter_annotation_paths(ref_dir):
    return sorted(path for path in Path(ref_dir).iterdir() if path.suffix == ".json")


def load_hypothesis_for(ref_path, hyp_dir):
    hyp_path = Path(hyp_dir) / ref_path.name
    if not hyp_path.exists():
        raise FileNotFoundError(hyp_path)
    return score.load_hypothesis(hyp_path)


def empty_summary():
    return {
        "clip_count": 0,
        "overall": score.Counts(),
        "switch_region": score.Counts(),
        "monolingual": score.Counts(),
        "language_pairs": {},
        "speakers": {},
        "domains": {},
        "switch_types": {},
        "token_languages": {},
        "unattributed_token_language_insertions": 0,
    }


def add_counts(target, source):
    target.errors += source.errors
    target.words += source.words


def clip_bucket(mapping, key):
    key = key or "unspecified"
    return mapping.setdefault(key, Bucket())


def score_one_dataset(name, ref_dir, hyp_dir):
    if not ref_dir.is_dir():
        raise SystemExit(f"Reference directory not found for {name}: {ref_dir}")
    if not hyp_dir.is_dir():
        raise SystemExit(f"Prediction directory not found for {name}: {hyp_dir}")

    summary = empty_summary()
    missing = []

    for ref_path in iter_annotation_paths(ref_dir):
        data = read_json(ref_path)
        clip_id = data.get("clip_id") or ref_path.stem
        try:
            hyp = load_hypothesis_for(ref_path, hyp_dir)
        except FileNotFoundError:
            missing.append(clip_id)
            continue

        ref = [score.normalize(token["text"]) for token in data["tokens"]]
        langs = [token.get("lang", "other") for token in data["tokens"]]
        overall, switch_region, monolingual = score.score_clip(
            ref,
            langs,
            hyp,
            summary["language_pairs"],
        )
        add_counts(summary["overall"], overall)
        add_counts(summary["switch_region"], switch_region)
        add_counts(summary["monolingual"], monolingual)
        summary["clip_count"] += 1

        clip_errors = 0
        token_lang_buckets = summary["token_languages"]
        for lang in langs:
            clip_bucket(token_lang_buckets, lang).add(words=1, clip_id=clip_id)

        for op, ridx in score.align(ref, hyp):
            if op == "ok":
                continue
            clip_errors += 1
            if op == "ins":
                summary["unattributed_token_language_insertions"] += 1
                continue
            lang = langs[ridx] if ridx is not None else "other"
            clip_bucket(token_lang_buckets, lang).add(errors=1, clip_id=clip_id)

        speaker = data.get("speaker", {}).get("id") or "unspecified"
        domain = data.get("domain") or "unspecified"
        switch_type = data.get("switch_type") or "unspecified"
        for mapping, key in (
            (summary["speakers"], speaker),
            (summary["domains"], domain),
            (summary["switch_types"], switch_type),
        ):
            clip_bucket(mapping, key).add(
                errors=clip_errors,
                words=len(ref),
                clip_id=clip_id,
            )

    if missing:
        raise SystemExit(
            f"Missing predictions for {len(missing)} clips in {hyp_dir}: "
            + ", ".join(missing[:10])
            + (" ..." if len(missing) > 10 else "")
        )
    if summary["clip_count"] == 0:
        raise SystemExit(f"No scored clips for {name}.")
    return summary


def merge_summaries(summaries):
    merged = empty_summary()
    for summary in summaries:
        merged["clip_count"] += summary["clip_count"]
        for key in ("overall", "switch_region", "monolingual"):
            add_counts(merged[key], summary[key])
        for label, counts in summary["language_pairs"].items():
            target = merged["language_pairs"].setdefault(label, score.Counts())
            add_counts(target, counts)
        for key in ("speakers", "domains", "switch_types", "token_languages"):
            for label, bucket in summary[key].items():
                target = merged[key].setdefault(label, Bucket())
                target.errors += bucket.errors
                target.words += bucket.words
                target.clips.update(bucket.clips)
        merged["unattributed_token_language_insertions"] += summary[
            "unattributed_token_language_insertions"
        ]
    return merged


def counts_metric(counts):
    return {
        "wer": counts.wer(),
        "errors": counts.errors,
        "words": counts.words,
    }


def bucket_metrics(mapping):
    return {
        key: value.metric()
        for key, value in sorted(
            mapping.items(),
            key=lambda item: (-item[1].words, item[0]),
        )
    }


def summary_to_json(summary):
    switch = summary["switch_region"].wer()
    mono = summary["monolingual"].wer()
    return {
        "clip_count": summary["clip_count"],
        "overall": counts_metric(summary["overall"]),
        "switch_region": counts_metric(summary["switch_region"]),
        "monolingual": counts_metric(summary["monolingual"]),
        "switch_penalty": switch - mono,
        "language_pairs": {
            key: counts_metric(value)
            for key, value in sorted(summary["language_pairs"].items())
        },
        "by_speaker": bucket_metrics(summary["speakers"]),
        "by_domain": bucket_metrics(summary["domains"]),
        "by_switch_type": bucket_metrics(summary["switch_types"]),
        "by_token_language": bucket_metrics(summary["token_languages"]),
        "unattributed_token_language_insertions": summary[
            "unattributed_token_language_insertions"
        ],
    }


def pct(value):
    return f"{value * 100:.1f}%"


def metric_cell(metric):
    return f"{pct(metric['wer'])} ({metric['errors']}/{metric['words']})"


def write_markdown(results, out_path):
    lines = [
        "# ASR Breakdown Report",
        "",
        "All values use the same normalization and alignment rules as `score.py`.",
        "Clip-level slices count insertions against the clip bucket. Token-language slices attribute substitutions and deletions to the reference token language; insertions are reported separately because they have no reference-language owner.",
        "",
    ]
    for name, summary in results.items():
        lines.extend([
            f"## {name}",
            "",
            f"Clips: {summary['clip_count']}",
            "",
            "| Metric | WER |",
            "|---|---:|",
            f"| Overall | {metric_cell(summary['overall'])} |",
            f"| Switch-region | {metric_cell(summary['switch_region'])} |",
            f"| Monolingual | {metric_cell(summary['monolingual'])} |",
            f"| Switch penalty | {pct(summary['switch_penalty'])} |",
            "",
        ])
        for title, key in (
            ("By speaker", "by_speaker"),
            ("By domain", "by_domain"),
            ("By switch type", "by_switch_type"),
            ("By token language", "by_token_language"),
            ("Switch-region by language pair", "language_pairs"),
        ):
            rows = summary[key]
            if not rows:
                continue
            lines.extend([f"### {title}", ""])
            if key == "language_pairs":
                lines.extend(["| Bucket | WER |", "|---|---:|"])
            else:
                lines.extend(["| Bucket | Clips | WER |", "|---|---:|---:|"])
            for bucket, metric in rows.items():
                if key == "language_pairs":
                    lines.append(f"| `{bucket}` | {metric_cell(metric)} |")
                else:
                    lines.append(
                        f"| `{bucket}` | {metric.get('clips', '')} | {metric_cell(metric)} |"
                    )
            lines.append("")
        insertions = summary["unattributed_token_language_insertions"]
        if insertions:
            lines.extend([
                f"Unattributed token-language insertions: {insertions}",
                "",
            ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--dataset",
        action="append",
        type=parse_dataset,
        required=True,
        help="Dataset triple as NAME:REF_DIR:HYP_DIR",
    )
    ap.add_argument("--out-json", default="results/asr_breakdowns.json")
    ap.add_argument("--out-md", default="results/asr_breakdowns.md")
    args = ap.parse_args()

    summaries = {}
    for name, ref_dir, hyp_dir in args.dataset:
        summaries[name] = score_one_dataset(name, ref_dir, hyp_dir)

    json_results = {
        name: summary_to_json(summary)
        for name, summary in summaries.items()
    }
    if len(summaries) > 1:
        json_results["combined"] = summary_to_json(merge_summaries(summaries.values()))

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(json_results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_markdown(json_results, Path(args.out_md))
    print(f"Wrote {args.out_json}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
