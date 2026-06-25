# Baseline Results

Switch-penalty WER for off-the-shelf ASR on the Sugidanon test set.
Generated with `score.py` (lower WER better; larger switch penalty = worse
code-switch handling). Fill the numbers after running a baseline.

## How to reproduce

```bash
# 1. transcribe audio with a baseline model
python scripts/run_whisper.py --model large-v3 --language tl
# 2. score
python score.py --ref data/annotations --hyp data/predictions
```

## STT results

| Model | Overall WER | Switch WER | Mono WER | Switch penalty |
|-------|------------|-----------|----------|----------------|
| Whisper small (tl)   | TBD | TBD | TBD | TBD |
| Whisper large-v3 (tl)| TBD | TBD | TBD | TBD |
| Meta MMS             | TBD | TBD | TBD | TBD |

### Switch penalty by language pair (best model)

| Pair    | Switch-region WER |
|---------|-------------------|
| hil↔tl  | TBD |
| hil↔en  | TBD |
| tl↔en   | TBD |

## TTS PoC — round-trip WER

TTS output transcribed back through STT, scored vs the input text
(`scripts/roundtrip_wer.py`). Plus a 1–5 human naturalness rating.

| TTS model | Round-trip WER | Naturalness (1–5) |
|-----------|----------------|-------------------|
| F5-TTS OpenBible Hiligaynon | TBD | TBD |

## Notes

- Whisper has no native Hiligaynon; `tl` is the closest code. Exposing how it
  breaks at hil↔tl / hil↔en switches is the point of the benchmark.
- Worked example (`data/.../hil_en_001.json`) is illustrative, not a real number.
