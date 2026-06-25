#!/usr/bin/env python3
"""
build_release.py - Judge-facing Sugidanon release pipeline.

Runs the implemented ASR benchmark checks, refreshes the static benchmark data
for the web explorer, and writes a redistributable release package.
"""

import argparse
import subprocess


def run(cmd):
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotations", default="data/annotations")
    ap.add_argument("--audio", default="data/audio")
    ap.add_argument("--predictions", default="data/predictions")
    ap.add_argument("--output", default="release")
    ap.add_argument("--model", default="whisper-small-tl")
    ap.add_argument("--include-audio", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument(
        "--skip-web",
        action="store_true",
        help="do not regenerate public/benchmark.json or public/clips",
    )
    args = ap.parse_args()

    run([
        "python3",
        "scripts/validate.py",
        "--kind",
        "asr",
        "--dir",
        args.annotations,
    ])

    run([
        "python3",
        "score.py",
        "--ref",
        args.annotations,
        "--hyp",
        args.predictions,
    ])

    if not args.skip_web:
        run([
            "python3",
            "scripts/build_benchmark_web.py",
            "--annotations",
            args.annotations,
            "--audio",
            args.audio,
            "--hyp",
            args.predictions,
            "--model",
            args.model,
        ])

    package_cmd = [
        "python3",
        "scripts/package_dataset.py",
        "--annotations",
        args.annotations,
        "--audio",
        args.audio,
        "--predictions",
        args.predictions,
        "--output",
        args.output,
    ]
    if args.include_audio:
        package_cmd.append("--include-audio")
    if args.overwrite:
        package_cmd.append("--overwrite")
    run(package_cmd)

    print()
    print(f"Release package ready: {args.output}")
    print(f"Web benchmark data ready: {'skipped' if args.skip_web else 'public/benchmark.json'}")


if __name__ == "__main__":
    main()
