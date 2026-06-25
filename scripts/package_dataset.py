#!/usr/bin/env python3
"""
package_dataset.py - Build a reproducible Sugidanon release package.

Outputs dataset metadata, statistics, dataset card, benchmark predictions, and
benchmark report. Audio is copied only with --include-audio.
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import wave
from collections import Counter
from datetime import date


ANNOTATION_DIR = "data/annotations"
AUDIO_DIR = "data/audio"
PREDICTION_DIR = "data/predictions"


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_annotations(annotation_dir):
    rows = []
    for name in sorted(os.listdir(annotation_dir)):
        if name.startswith("hil_cs_") and name.endswith(".json"):
            rows.append(read_json(os.path.join(annotation_dir, name)))
    return rows


def audio_duration(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def edge_flags(path, edge=0.15, clip_ratio=0.6, clap_ratio=0.85):
    import audioop

    with wave.open(path) as w:
        sr = w.getframerate()
        data = w.readframes(w.getnframes())
        width = w.getsampwidth()
    edge_bytes = int(edge * sr) * width
    body = data[edge_bytes:len(data) - edge_bytes] or data
    body_rms = audioop.rms(body, width) or 1
    global_peak = audioop.max(data, width) or 1
    flags = []
    for name, segment in (("head", data[:edge_bytes]), ("tail", data[-edge_bytes:])):
        if not segment:
            continue
        segment_rms = audioop.rms(segment, width)
        segment_peak = audioop.max(segment, width)
        if segment_rms > clip_ratio * body_rms:
            flags.append(f"CLIPPED-{name}")
        elif segment_peak > clap_ratio * global_peak:
            flags.append(f"CLAP-{name}")
    return flags


def write_metadata_csv(rows, out_path):
    fields = [
        "clip_id",
        "file_name",
        "transcript",
        "domain",
        "switch_type",
        "matrix_language",
        "review_status",
        "lang_tags_status",
        "duration_sec",
        "token_count",
        "speaker_id",
        "primary_language",
        "region",
        "age_band",
        "gender",
    ]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            speaker = row.get("speaker", {})
            duration = row.get("duration_sec")
            if duration is None:
                duration = row.get("_actual_duration_sec", "")
            writer.writerow({
                "clip_id": row["clip_id"],
                "file_name": os.path.basename(row["audio_file"]),
                "transcript": row["transcript"],
                "domain": row.get("domain", ""),
                "switch_type": row.get("switch_type", ""),
                "matrix_language": row.get("matrix_language", ""),
                "review_status": row.get("review_status", ""),
                "lang_tags_status": row.get("lang_tags_status", ""),
                "duration_sec": duration,
                "token_count": len(row.get("tokens", [])),
                "speaker_id": speaker.get("id", ""),
                "primary_language": speaker.get("primary_language", ""),
                "region": speaker.get("region", ""),
                "age_band": speaker.get("age_band", ""),
                "gender": speaker.get("gender", ""),
            })


def write_metadata_jsonl(rows, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            duration = row.get("duration_sec")
            if duration is None:
                duration = row.get("_actual_duration_sec")
            f.write(json.dumps({
                "file_name": os.path.basename(row["audio_file"]),
                "clip_id": row["clip_id"],
                "transcript": row["transcript"],
                "domain": row.get("domain"),
                "switch_type": row.get("switch_type"),
                "matrix_language": row.get("matrix_language"),
                "review_status": row.get("review_status"),
                "lang_tags_status": row.get("lang_tags_status"),
                "duration_sec": duration,
                "tokens": row.get("tokens", []),
            }, ensure_ascii=False) + "\n")


def compute_statistics(rows, audio_dir):
    durations = []
    flagged = {}
    token_langs = Counter()
    for row in rows:
        audio_path = os.path.join(audio_dir, os.path.basename(row["audio_file"]))
        duration = audio_duration(audio_path)
        row["_actual_duration_sec"] = round(duration, 3)
        durations.append(duration)
        flags = edge_flags(audio_path)
        if flags:
            flagged[row["clip_id"]] = flags
        token_langs.update(token["lang"] for token in row.get("tokens", []))
    total_duration = sum(durations)
    return {
        "clip_count": len(rows),
        "total_duration_sec": round(total_duration, 3),
        "average_duration_sec": round(total_duration / len(rows), 3) if rows else 0,
        "min_duration_sec": round(min(durations), 3) if durations else 0,
        "max_duration_sec": round(max(durations), 3) if durations else 0,
        "domains": dict(Counter(row.get("domain") for row in rows)),
        "switch_types": dict(Counter(row.get("switch_type") for row in rows)),
        "review_status": dict(Counter(row.get("review_status") for row in rows)),
        "lang_tags_status": dict(Counter(row.get("lang_tags_status") for row in rows)),
        "token_languages": dict(token_langs),
        "edge_flags": flagged,
    }


def run_score(annotation_dir, prediction_dir):
    proc = subprocess.run(
        ["python3", "score.py", "--ref", annotation_dir, "--hyp", prediction_dir],
        check=True,
        text=True,
        capture_output=True,
    )
    return proc.stdout


def parse_score(score_text):
    metrics = {}
    for line in score_text.splitlines():
        if line.startswith("Overall WER"):
            metrics["overall_wer"] = line.split(":", 1)[1].strip()
        elif line.startswith("Switch-region WER :"):
            metrics["switch_region_wer"] = line.split(":", 1)[1].strip()
        elif line.startswith("Monolingual WER"):
            metrics["monolingual_wer"] = line.split(":", 1)[1].strip()
        elif line.startswith("Switch penalty"):
            metrics["switch_penalty"] = line.split(":", 1)[1].strip()
    return metrics


def write_dataset_card(rows, stats, out_path, include_audio):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Sugidanon Dataset Card\n\n")
        f.write("## Summary\n\n")
        f.write(
            "Sugidanon is a code-switch Hiligaynon speech benchmark scaffold "
            "covering Hiligaynon, Tagalog/Filipino, and English utterances.\n\n"
        )
        f.write("## Contents\n\n")
        f.write(f"- Clips: {stats['clip_count']}\n")
        f.write(f"- Total duration: {stats['total_duration_sec']} seconds\n")
        f.write(f"- Audio included in this package: {'yes' if include_audio else 'no'}\n")
        f.write(f"- Domains: {', '.join(sorted(stats['domains']))}\n")
        f.write(f"- Switch types: {', '.join(sorted(stats['switch_types']))}\n\n")
        f.write("## Review Status\n\n")
        f.write(f"- Transcript review: {stats['review_status']}\n")
        f.write(f"- Token language tags: {stats['lang_tags_status']}\n\n")
        f.write("## Known Limitations\n\n")
        f.write("- Per-word language tags are still `seed_unverified` unless updated by a speaker.\n")
        if stats["edge_flags"]:
            f.write(f"- Edge QA flags remain: {stats['edge_flags']}.\n")
        f.write("- Speaker metadata is intentionally coarse and may contain blank optional fields.\n\n")
        f.write("## License\n\n")
        f.write("Dataset files created by Team Hague are released under CC BY 4.0.\n")


def write_benchmark_report(score_text, stats, out_path):
    metrics = parse_score(score_text)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Sugidanon ASR Benchmark Report\n\n")
        f.write(f"Generated: {date.today().isoformat()}\n\n")
        f.write("## Metrics\n\n")
        for key, value in metrics.items():
            f.write(f"- {key}: {value}\n")
        f.write("\n## Quality Notes\n\n")
        if stats["edge_flags"]:
            f.write(f"- Edge QA flags: {stats['edge_flags']}\n")
        else:
            f.write("- No edge QA flags.\n")
        f.write("- Baseline uses Whisper with Tagalog language forcing when generated by `scripts/run_whisper.py --language tl`.\n")
        f.write("- Results are not final model-quality claims while token tags remain `seed_unverified`.\n\n")
        f.write("## Raw Score Output\n\n")
        f.write("```text\n")
        f.write(score_text)
        f.write("```\n")


def copy_tree_files(src_dir, dst_dir, suffix):
    os.makedirs(dst_dir, exist_ok=True)
    for name in sorted(os.listdir(src_dir)):
        if name.endswith(suffix):
            shutil.copy2(os.path.join(src_dir, name), os.path.join(dst_dir, name))


def build_package(args):
    rows = load_annotations(args.annotations)
    if not rows:
        raise SystemExit(f"No annotations in {args.annotations}")

    if os.path.exists(args.output) and args.overwrite:
        shutil.rmtree(args.output)
    os.makedirs(args.output, exist_ok=True)

    dataset_dir = os.path.join(args.output, "dataset")
    benchmark_dir = os.path.join(args.output, "benchmark")
    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(benchmark_dir, exist_ok=True)

    copy_tree_files(args.annotations, os.path.join(dataset_dir, "annotations"), ".json")
    if args.include_audio:
        copy_tree_files(args.audio, os.path.join(dataset_dir, "audio"), ".wav")
    write_metadata_csv(rows, os.path.join(dataset_dir, "metadata.csv"))
    write_metadata_jsonl(rows, os.path.join(dataset_dir, "metadata.jsonl"))

    stats = compute_statistics(rows, args.audio)
    with open(os.path.join(dataset_dir, "statistics.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    write_dataset_card(rows, stats, os.path.join(dataset_dir, "dataset_card.md"), args.include_audio)

    copy_tree_files(args.predictions, os.path.join(benchmark_dir, "predictions"), ".json")
    score_text = run_score(args.annotations, args.predictions)
    with open(os.path.join(benchmark_dir, "score.txt"), "w", encoding="utf-8") as f:
        f.write(score_text)
    with open(os.path.join(benchmark_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(parse_score(score_text), f, ensure_ascii=False, indent=2)
    write_benchmark_report(score_text, stats, os.path.join(benchmark_dir, "report.md"))
    print(f"Wrote release package to {args.output}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotations", default=ANNOTATION_DIR)
    ap.add_argument("--audio", default=AUDIO_DIR)
    ap.add_argument("--predictions", default=PREDICTION_DIR)
    ap.add_argument("--output", default="release")
    ap.add_argument("--include-audio", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    build_package(args)


if __name__ == "__main__":
    main()
