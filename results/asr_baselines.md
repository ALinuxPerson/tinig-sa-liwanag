# ASR Baseline Results

This file records the reproducible ASR baseline output for the current
worked-example test set.

Run:

```bash
# headline baseline — Whisper small, forced Tagalog
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions

# comparison baseline — Whisper small, auto language detect
python3 scripts/run_whisper.py --model small --out-dir data/predictions_auto
python3 score.py --ref data/annotations --hyp data/predictions_auto
```

Current output. Scores are reported **per subset** — subsets are never blended
into one headline WER (see `SCHEMA.md`).

### `scripted_native` — main headline benchmark

| Model | Clips | Overall WER | Switch-region WER | Monolingual WER | Switch penalty |
|-------|-------|-------------|-------------------|-----------------|----------------|
| `whisper-small-tl` (forced Tagalog) | 40 | 59.5% | 35.8% | 66.3% | -30.6% |
| `whisper-small-auto` (auto-detect) | 40 | 61.7% | 38.8% | 68.3% | -29.5% |

Per language pair (`whisper-small-tl`): `hil↔en` 40.0%, `hil↔tl` 24.4%, `tl↔en` 6.2%.

Both configs show the same finding: the model handles switch-region (borrowed)
words far better than the Hiligaynon matrix. Forcing Tagalog (`--language tl`)
beats auto-detect across every metric, so it is the headline baseline.

### Extension subsets

Report separately; never count `non_native_eval` as native gold.

| Subset | Model | Clips | Overall WER | Switch-region WER | Monolingual WER | Switch penalty |
|--------|-------|-------|-------------|-------------------|-----------------|----------------|
| `scripted_native_spk2` | `whisper-small-tl` | 40 | 34.4% | 28.6% | 38.8% | -10.2% |
| `non_native_eval` | not scored | 20 planned | TBD | TBD | TBD | TBD |

## Important limitation

These are baseline numbers over reviewed headline tags and bundled prediction
files. `scripted_native_spk2` is a second-speaker extension, not part of the
frozen headline score. `non_native_eval` is planned-only until consented audio,
reviewed transcripts, and reviewed token-language tags exist. Re-run after every
audio, transcript, or language-tag change:

```bash
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions
```
