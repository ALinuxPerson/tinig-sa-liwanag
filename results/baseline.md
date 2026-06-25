# Baseline Results

The v1 project baseline is context-aware text translation into Hiligaynon.

Current benchmark:

```text
data/benchmark/hil_translation_v1.jsonl
```

Current baseline predictions:

```text
data/predictions/translation_baseline_dict.jsonl
```

## How to reproduce

```bash
python3 scripts/validate.py --kind translation --dir data/benchmark

python3 scripts/evaluate_translation.py \
  --refs data/benchmark/hil_translation_v1.jsonl \
  --preds data/predictions/translation_baseline_dict.jsonl
```

## Text translation baselines

| Model | Coverage | Exact match | Token F1 | chrF | Notes |
|-------|----------|-------------|----------|------|-------|
| dict-baseline | TBD | TBD | TBD | TBD | Offline word lookup; exposes why context-aware MT is needed |
| neural-baseline | TBD | TBD | TBD | TBD | Optional HF model backend |
| fine-tuned-v1 | TBD | TBD | TBD | TBD | Future reviewed-data model |

## Required human evaluation

Automatic metrics do not prove translation quality. For the judged submission,
add a human evaluation table over a reviewed subset:

| Model | Adequacy | Fluency | Context | Terminology | Major error rate |
|-------|----------|---------|---------|-------------|------------------|
| dict-baseline | TBD | TBD | TBD | TBD | TBD |
| neural-baseline | TBD | TBD | TBD | TBD | TBD |
| fine-tuned-v1 | TBD | TBD | TBD | TBD | TBD |

## Expected dictionary baseline behavior

The dictionary baseline should score poorly on context-heavy examples. That is a
useful result: it demonstrates that a simple word-substitution demo is not
enough for Hiligaynon translation.

Known likely failures:

- missing Hiligaynon grammar and word order
- untranslated unknown words
- no paragraph-level context
- no pronoun or tense/aspect resolution
- weak handling of domain terminology

## Future speech results

Earlier ASR/TTS metrics have been moved out of the v1 headline scope. When the
project returns to speech, use:

```bash
python3 score.py --ref data/annotations --hyp data/predictions
```

for code-switched ASR switch-region WER.
