#!/usr/bin/env python3
"""
ingest.py — Turn an external corpus of audio + transcripts into Sugidanon format.

Scans a source directory for audio files, finds each one's matching transcript
(a .txt / .lab / .trans file with the same stem, or a metadata.csv mapping), then:
  - copies/normalizes audio -> data/audio/<clip_id>.wav (16 kHz mono via ffmpeg)
  - writes a STUB gold annotation -> data/annotations/<clip_id>.json

The stub tags every token with a single default language (--lang, default hil) so
the file already validates and scores. **Humans must then correct the per-word
hil / tl / en / other tags** per SCHEMA.md — AI/ingest does NOT assign real
code-switch labels (see AI_DISCLOSURE.md).

Source provenance + license are recorded in each annotation so redistribution
keeps attribution. Ingested audio stays under its source license, NOT CC BY 4.0.

Pure standard library (ffmpeg optional — only needed to convert non-wav audio).

Usage:
    python scripts/ingest.py external/g2p-asr/data --prefix hil --limit 40
    python scripts/ingest.py /path/to/corpus --prefix hil_en --lang hil \
        --source "G2P-ASR (AngelAquino)" --license "research use"
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import wave

AUDIO_EXTS = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus")
TRANSCRIPT_EXTS = (".txt", ".lab", ".trans", ".transcription")


def find_transcript(audio_path):
    """Return transcript text for an audio file, or None if not found."""
    stem, _ = os.path.splitext(audio_path)
    for ext in TRANSCRIPT_EXTS:
        cand = stem + ext
        if os.path.exists(cand):
            with open(cand, encoding="utf-8", errors="replace") as f:
                return f.read().strip()
    return None


def wav_duration(path):
    """Return duration in seconds for a wav, else None."""
    try:
        with wave.open(path) as w:
            return round(w.getnframes() / float(w.getframerate()), 2)
    except (wave.Error, OSError):
        return None


def to_wav_16k_mono(src, dst):
    """Convert src audio to 16 kHz mono wav at dst using ffmpeg."""
    subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-ac", "1", "-ar", "16000",
         "-sample_fmt", "s16", dst],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def tokenize(text):
    """Whitespace tokenize, strip surrounding punctuation, drop empties."""
    return [t for t in (w.strip(".,!?;:\"'()") for w in text.split()) if t]


def make_annotation(clip_id, tokens, lang, source, license_):
    return {
        "clip_id": clip_id,
        "audio_file": f"audio/{clip_id}.wav",
        "duration_sec": None,
        "speaker": {"id": "unknown", "primary_language": lang,
                    "region": "", "age_band": "", "gender": ""},
        "matrix_language": lang,
        "provenance": {"source": source, "license": license_,
                       "note": "STUB tags — human must correct per SCHEMA.md"},
        "tokens": [{"idx": i, "text": t, "lang": lang}
                   for i, t in enumerate(tokens)],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="source corpus directory (scanned recursively)")
    ap.add_argument("--prefix", default="hil", help="clip_id prefix")
    ap.add_argument("--lang", default="hil", choices=["hil", "tl", "en", "other"],
                    help="default language for STUB tags (humans correct later)")
    ap.add_argument("--limit", type=int, default=0, help="max clips (0 = all)")
    ap.add_argument("--source", default="G2P-ASR (AngelAquino)")
    ap.add_argument("--license", default="research use; credit source authors")
    ap.add_argument("--audio-out", default="data/audio")
    ap.add_argument("--ann-out", default="data/annotations")
    args = ap.parse_args()

    if not os.path.isdir(args.src):
        sys.exit(f"Not a directory: {args.src}")

    have_ffmpeg = shutil.which("ffmpeg") is not None
    os.makedirs(args.audio_out, exist_ok=True)
    os.makedirs(args.ann_out, exist_ok=True)

    audio_files = []
    for root, _, files in os.walk(args.src):
        for fn in sorted(files):
            if fn.lower().endswith(AUDIO_EXTS):
                audio_files.append(os.path.join(root, fn))
    audio_files.sort()

    n = 0
    skipped = 0
    for ap_path in audio_files:
        if args.limit and n >= args.limit:
            break
        text = find_transcript(ap_path)
        if not text:
            skipped += 1
            continue
        tokens = tokenize(text)
        if not tokens:
            skipped += 1
            continue

        clip_id = f"{args.prefix}_{n + 1:03d}"
        dst_wav = os.path.join(args.audio_out, f"{clip_id}.wav")

        if ap_path.lower().endswith(".wav"):
            shutil.copyfile(ap_path, dst_wav)
        elif have_ffmpeg:
            to_wav_16k_mono(ap_path, dst_wav)
        else:
            print(f"  skip {os.path.basename(ap_path)}: non-wav and no ffmpeg")
            skipped += 1
            continue

        ann = make_annotation(clip_id, tokens, args.lang, args.source, args.license)
        ann["duration_sec"] = wav_duration(dst_wav)
        with open(os.path.join(args.ann_out, f"{clip_id}.json"), "w",
                  encoding="utf-8") as f:
            json.dump(ann, f, ensure_ascii=False, indent=2)
        print(f"{clip_id}: {len(tokens)} tokens  <- {os.path.relpath(ap_path, args.src)}")
        n += 1

    print("-" * 50)
    print(f"Ingested {n} clips (skipped {skipped} without usable transcript).")
    print("STUB language tags are all "
          f"'{args.lang}'. Now CORRECT per-word tags by hand (SCHEMA.md),")
    print("then: python scripts/validate.py")


if __name__ == "__main__":
    main()
