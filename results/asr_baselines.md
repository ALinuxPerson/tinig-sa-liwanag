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

Not yet populated. Report separately when added; never count `non_native_eval`
as native gold.

| Subset | Model | Clips | Overall WER | Switch-region WER | Monolingual WER | Switch penalty |
|--------|-------|-------|-------------|-------------------|-----------------|----------------|
| `native_podcast` | TBD | TBD | TBD | TBD | TBD | TBD |
| `native_vlog` | TBD | TBD | TBD | TBD | TBD | TBD |
| `non_native_eval` | TBD | TBD | TBD | TBD | TBD | TBD |

## Important limitation

These are baseline numbers over the current 40-clip reviewed-text scaffold.
Per-word language tags remain `seed_unverified`, so these are not final
model-quality claims. Re-run after every audio, transcript, or language-tag
change:

```bash
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions
```
