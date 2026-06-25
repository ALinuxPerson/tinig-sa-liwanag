#!/usr/bin/env bash
# fetch_g2p_asr.sh — Clone the G2P-ASR corpus (Tagalog/Cebuano/Hiligaynon).
#
# Source: https://github.com/AngelAquino/g2p-asr  (Aquino et al., ISMAC 2019)
# No license file in the repo — treat as research use, credit the authors.
# Audio stays under its source terms; do NOT relicense it as CC BY 4.0.
#
# Usage:  bash scripts/fetch_g2p_asr.sh
# Result: external/g2p-asr/  (gitignored)

set -euo pipefail

DEST="external/g2p-asr"
REPO="https://github.com/AngelAquino/g2p-asr.git"

mkdir -p external
if [ -d "$DEST/.git" ]; then
  echo "Already cloned -> $DEST (pulling latest)"
  git -C "$DEST" pull --ff-only || true
else
  git clone --depth 1 "$REPO" "$DEST"
fi

echo
echo "Cloned to $DEST"
echo "Next: python scripts/ingest.py $DEST/data --prefix hil --limit 40"
