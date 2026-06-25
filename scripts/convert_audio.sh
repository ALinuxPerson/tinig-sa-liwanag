#!/usr/bin/env bash
# convert_audio.sh — Normalize any input audio to 16 kHz mono WAV.
#
# Usage:
#   scripts/convert_audio.sh input.m4a hil_en_001
#   scripts/convert_audio.sh recording.mp3 hil_tl_007 data/audio
#
# Produces <out_dir>/<clip_id>.wav (default out_dir: data/audio).
# Requires: ffmpeg.

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <input_audio> <clip_id> [out_dir]" >&2
  exit 1
fi

INPUT="$1"
CLIP_ID="$2"
OUT_DIR="${3:-data/audio}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "error: ffmpeg not found. Install it first (brew install ffmpeg)." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
ffmpeg -y -i "$INPUT" -ac 1 -ar 16000 -sample_fmt s16 "$OUT_DIR/$CLIP_ID.wav"
echo "wrote $OUT_DIR/$CLIP_ID.wav"
