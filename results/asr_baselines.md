# ASR Baseline Results

This file records the reproducible ASR baseline output for the current
worked-example test set.

Run:

```bash
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions
```

Current output. Scores are reported **per subset** — subsets are never blended
into one headline WER (see `SCHEMA.md`).

### `scripted_native` — main headline benchmark

| Model | Clips | Overall WER | Switch-region WER | Monolingual WER | Switch penalty |
|-------|-------|-------------|-------------------|-----------------|----------------|
| `whisper-small-tl` | 40 | 59.5% | 35.8% | 66.3% | -30.6% |

Per language pair: `hil↔en` 40.0%, `hil↔tl` 24.4%, `tl↔en` 6.2%.

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
