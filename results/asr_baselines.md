# ASR Baseline Results

This file records the reproducible ASR baseline output for the current
worked-example test set.

Run:

```bash
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions
```

Current output:

| Model | Clips | Overall WER | Switch-region WER | Monolingual WER | Switch penalty |
|-------|-------|-------------|-------------------|-----------------|----------------|
| `whisper-small-tl` | 40 | 59.5% | 35.8% | 66.3% | -30.6% |

## Important limitation

These are baseline numbers over the current 40-clip reviewed-text scaffold.
Per-word language tags remain `seed_unverified`, so these are not final
model-quality claims. Re-run after every audio, transcript, or language-tag
change:

```bash
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions
```
