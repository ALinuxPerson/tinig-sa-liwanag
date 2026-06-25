#!/usr/bin/env python3
"""
run_whisper.py — Baseline ASR: transcribe data/audio/*.wav into predictions.

Loops over every clip in data/audio/, transcribes with OpenAI Whisper, and
writes data/predictions/<clip_id>.json in the format score.py expects:
    {"clip_id": "...", "text": "the transcript"}

Whisper is OPTIONAL. The import is guarded so the repo works without it
installed; this script only needs whisper when you actually run a baseline.

Usage:
    python scripts/run_whisper.py                    # model=small, lang auto
    python scripts/run_whisper.py --model large-v3 --language tl
"""

import argparse
import json
import os
import sys

try:
    import whisper  # type: ignore
    HAVE_WHISPER = True
except ImportError:
    HAVE_WHISPER = False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir", default="data/audio")
    ap.add_argument("--out-dir", default="data/predictions")
    ap.add_argument("--model", default="small",
                    help="whisper model name (tiny/base/small/medium/large-v3)")
    ap.add_argument("--language", default=None,
                    help="force a language code (e.g. tl); default auto-detect. "
                         "Note: Whisper has no native 'hil' — tl is the closest.")
    args = ap.parse_args()

    if not HAVE_WHISPER:
        sys.exit("whisper not installed. Run: pip install -r requirements.txt\n"
                 "(this script is optional; score.py works without it)")

    wavs = sorted(f for f in os.listdir(args.audio_dir) if f.endswith(".wav"))
    if not wavs:
        sys.exit(f"No .wav files in {args.audio_dir}")

    os.makedirs(args.out_dir, exist_ok=True)
    print(f"Loading whisper model: {args.model}")
    model = whisper.load_model(args.model)

    for wav in wavs:
        clip_id = os.path.splitext(wav)[0]
        path = os.path.join(args.audio_dir, wav)
        use_fp16 = str(getattr(model, "device", "cpu")) != "cpu"
        result = model.transcribe(path, language=args.language, fp16=use_fp16)
        text = result["text"].strip()
        out = {"clip_id": clip_id, "text": text}
        out_path = os.path.join(args.out_dir, f"{clip_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"{clip_id}: {text[:60]}...")

    print(f"Wrote {len(wavs)} predictions to {args.out_dir}")


if __name__ == "__main__":
    main()
