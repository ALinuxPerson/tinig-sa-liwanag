#!/usr/bin/env python3
"""
benchmark_asr.py - One-command Sugidanon ASR benchmark pipeline.

Runs validation, clip edge screening, optional Whisper transcription, scoring,
and optional release packaging.
"""

import argparse
import os
import subprocess
import sys


def run(cmd, capture=False):
    print("+ " + " ".join(cmd), flush=True)
    return subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=capture,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="small")
    ap.add_argument("--language", default="tl")
    ap.add_argument("--skip-whisper", action="store_true")
    ap.add_argument("--package", action="store_true", dest="make_package")
    ap.add_argument("--release-dir", default="release")
    ap.add_argument("--include-audio", action="store_true")
    args = ap.parse_args()

    run(["python3", "scripts/validate.py", "--kind", "asr", "--dir", "data/annotations"])
    run(["python3", "scripts/screen_clips.py"])

    if not args.skip_whisper:
        run([
            "python3",
            "scripts/run_whisper.py",
            "--model",
            args.model,
            "--language",
            args.language,
        ])

    score = run(["python3", "score.py", "--ref", "data/annotations", "--hyp", "data/predictions"], capture=True)
    print(score.stdout)

    os.makedirs("results", exist_ok=True)
    with open("results/asr_score.txt", "w", encoding="utf-8") as f:
        f.write(score.stdout)

    if args.make_package:
        package_cmd = [
            "python3",
            "scripts/package_dataset.py",
            "--output",
            args.release_dir,
            "--overwrite",
        ]
        if args.include_audio:
            package_cmd.append("--include-audio")
        run(package_cmd)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
