#!/usr/bin/env python3
"""
split_claps.py — Split per-category recordings into per-phrase clips.

The Hiligaynon speaker recorded one file per category (5 phrases each), clapping
between phrases. Claps are loud impulsive spikes; this detects them by amplitude
and cuts the audio into one 16 kHz mono wav per phrase, mapped to the hil_cs_NNN
clip IDs the annotations expect.

File order must match scripts/build_codeswitch_set.py domains:
  1 market 2 transport 3 school_work 4 family 5 health 6 culture
  7 everyday 8 oral_tradition  → 5 phrases each → hil_cs_001..040.

Pure standard library (wave + audioop) plus ffmpeg for decode/cut.

Usage:
    python3 scripts/split_claps.py --src "/path/to/m4a-folder" --dry-run
    python3 scripts/split_claps.py --src "/path/to/m4a-folder" --out data/audio
    # per-file tuning if a file miscounts:
    python3 scripts/split_claps.py --src ... --only 5 --thresh 0.7 --dry-run
"""

import argparse
import audioop
import glob
import os
import subprocess
import sys
import wave

WIN = 0.03  # analysis window (s)


def to_wav(src, dst):
    subprocess.run(["ffmpeg", "-y", "-i", src, "-ac", "1", "-ar", "16000",
                    "-sample_fmt", "s16", dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def detect_claps(wav, thresh, merge_gap):
    """Return (clap_centers, duration). Claps = loud spikes above thresh*gmax."""
    w = wave.open(wav)
    sr, n = w.getframerate(), w.getnframes()
    data = w.readframes(n)
    w.close()
    win = int(WIN * sr) * 2  # bytes per window (16-bit)
    peaks = [audioop.max(data[i:i + win], 2) for i in range(0, len(data) - win, win)]
    gmax = max(peaks) or 1
    claps, prev = [], -10.0
    for i, p in enumerate(peaks):
        if p >= thresh * gmax:
            t = i * WIN
            if t - prev > merge_gap:
                claps.append(t)
            prev = t
    return claps, n / sr


def phrases_from_claps(claps, duration, per_cat, guard):
    """5 phrases per file: each clap ends a phrase; a 5th clap is trailing."""
    phrases, cursor = [], 0.0
    for c in claps:
        end = max(cursor, c - guard)
        if end - cursor > 0.3:
            phrases.append((cursor, end))
        cursor = c + guard
    # if no trailing clap, the tail after the last clap is the final phrase
    if len(claps) < per_cat and duration - cursor > 0.3:
        phrases.append((cursor, duration - guard))
    return phrases


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder of per-category audio files")
    ap.add_argument("--out", default="data/audio")
    ap.add_argument("--thresh", type=float, default=0.6, help="clap peak threshold (x global max)")
    ap.add_argument("--merge-gap", type=float, default=1.0, help="merge spikes within this many s")
    ap.add_argument("--guard", type=float, default=0.18, help="trim around each clap (s)")
    ap.add_argument("--per-cat", type=int, default=5, help="expected phrases/file")
    ap.add_argument("--start-clip", type=int, default=1,
                    help="first clip number (Script 2 = 41, Script 3 = 81)")
    ap.add_argument("--only", type=int, default=0, help="process only file N (1-based)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(f for f in glob.glob(os.path.join(args.src, "*"))
                   if f.lower().endswith((".m4a", ".wav", ".mp3", ".m4r")))
    if not files:
        sys.exit(f"No audio files in {args.src}")

    scratch = "/tmp/split_claps_tmp.wav"
    os.makedirs(args.out, exist_ok=True)
    total_ok = True
    for cat_idx, f in enumerate(files):
        if args.only and cat_idx + 1 != args.only:
            continue
        to_wav(f, scratch)
        claps, dur = detect_claps(scratch, args.thresh, args.merge_gap)
        phrases = phrases_from_claps(claps, dur, args.per_cat, args.guard)
        flag = "" if len(phrases) == args.per_cat else "  <-- CHECK (tune --thresh/--merge-gap)"
        if len(phrases) != args.per_cat:
            total_ok = False
        print(f"[{cat_idx+1}] {os.path.basename(f)[:26]:28} {dur:5.1f}s  "
              f"{len(claps)} claps -> {len(phrases)} phrases{flag}")
        base = (args.start_clip - 1) + cat_idx * args.per_cat
        for p_i, (a, b) in enumerate(phrases):
            clip_id = f"hil_cs_{base + p_i + 1:03d}"
            print(f"      {clip_id}  {a:6.2f}-{b:6.2f}s  ({b-a:.1f}s)")
            if not args.dry_run:
                dst = os.path.join(args.out, f"{clip_id}.wav")
                subprocess.run(["ffmpeg", "-y", "-i", scratch, "-ss", f"{a}",
                                "-to", f"{b}", "-ac", "1", "-ar", "16000",
                                "-sample_fmt", "s16", dst],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\n" + ("All files split into the expected count." if total_ok
                  else "Some files miscounted — re-run those with --only N and tuned flags."))
    if args.dry_run:
        print("Dry run — no files written.")


if __name__ == "__main__":
    main()
