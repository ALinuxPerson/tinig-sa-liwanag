# ASR Baseline Results

This file records the reproducible ASR baseline output for the current
worked-example test set.

Run:

```bash
python3 scripts/eval_asr_baselines.py
```

Current output:

| Model | Clips | Overall WER | Switch-region WER | Monolingual WER | Switch penalty |
|-------|-------|-------------|-------------------|-----------------|----------------|
| `mms-1b-all` | 1 | 25.0% | 0.0% | 33.3% | -33.3% |
| `whisper-large-v3-tl` | 1 | 37.5% | 20.0% | 33.3% | -13.3% |

## Important limitation

These are worked-example numbers over the included sample annotation and sample
prediction files. They verify that the evaluation pipeline is reproducible.
They are not final model-quality claims.

To reproduce final reported Whisper/MMS WER, replace:

```text
data/predictions/asr/whisper-large-v3-tl/*.json
data/predictions/asr/mms-1b-all/*.json
```

with real model outputs over the full labeled test set, then rerun:

```bash
python3 scripts/eval_asr_baselines.py
```
