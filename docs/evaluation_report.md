# Evaluation Report

## Code-switch ASR benchmark (speech MVP)

The speech deliverable: **40 native-recorded code-switch clips** (3.1 min total),
one Hiligaynon speaker, 8 domains (market, transport, school/work, family,
health, culture, everyday, oral tradition), 4 switch types (`HIL`=10, `HIL+EN`=15,
`HIL+TL`=8, `HIL+TL+EN`=7). Reference text reviewed by the speaker; per-word
language tags auto-seeded, pending speaker confirmation.

### Baseline result — Whisper small, `--language tl`

| Metric | WER |
|--------|-----|
| Overall | 59.5% |
| Monolingual (pure Hiligaynon) | 66.3% |
| Switch-region (next to a language switch) | 35.8% |
| **Switch penalty** (switch − mono) | **−30.6%** |

Switch-region WER by language pair: `hil↔en` 40.0%, `hil↔tl` 24.4%, `tl↔en` 6.2%.

### Interpretation — the negative penalty is the finding

An off-the-shelf Tagalog ASR model transcribes the **switch words better than the
monolingual ones**. Switch regions carry the English/Tagalog loanwords
(`traffic`, `meeting`, `grab`) the model already knows; the **Hiligaynon matrix**
is what it fails on (66% WER, no Hiligaynon training). The failure scales with
Hiligaynon involvement: `tl↔en` is near-solved (6%), `hil↔en` is worst (40%).

This quantifies the exact gap Sugidanon exists to expose: **current speech tech
catches the borrowed words and misses the Ilonggo.**

### Caveats

- Whisper **small** (not large-v3) — preliminary; a larger model lowers WER.
- Per-word tags are `seed_unverified`; speaker confirmation firms up the
  switch/monolingual split.
- Single speaker — expand speakers before drawing model-level conclusions.

### Reproduce

```bash
python3 scripts/validate.py --kind asr --dir data/annotations
python3 scripts/run_whisper.py --model small --language tl   # or large-v3
python3 score.py --ref data/annotations --hyp data/predictions
```

---

## Translation benchmark

## Current status

This hackathon version evaluates a **dictionary baseline** on a 30-row seed
benchmark for English, Filipino, and code-switched text into Hiligaynon.

The benchmark rows are marked `seed_unverified`. They are useful for showing the
workflow and failure modes, but they are not gold data until reviewed by native
Hiligaynon speakers.

## Reproduce

```bash
python3 scripts/validate.py --kind translation --dir data/benchmark
python3 scripts/generate_baseline_predictions.py
python3 scripts/evaluate_translation.py \
  --refs data/benchmark/hil_translation_v1.jsonl \
  --preds data/predictions/translation_baseline_dict.jsonl
```

## What is evaluated

The current evaluator reports:

- coverage
- exact match after normalization
- token F1
- chrF-style character n-gram F-score
- per-domain averages

These metrics are only a scaffold. Hiligaynon translation quality still needs
human review for adequacy, fluency, context preservation, and terminology.

## Baseline being tested

`dict-baseline` uses `scripts/translate_hil.py` with the local Hiligaynon
lexicon. It translates known words and marks unknown terms with `*word*`.

This is intentionally weak. Its purpose is to prove that word-level translation
is insufficient for context-aware Hiligaynon translation.

## Current generated result

Latest local run:

| Model | References | Predictions | Coverage | Exact match | Token F1 | chrF |
|-------|------------|-------------|----------|-------------|----------|------|
| dict-baseline | 30 | 30 | 100.0% | 0.0% | 30.9% | 34.7% |

The result is useful because it makes the failure visible: even with complete
prediction coverage, the baseline does not produce exact contextual translations.

## Expected failure modes

- unknown words are copied as `*word*`
- grammar and word order are not repaired
- context is ignored
- pronoun references are not resolved
- tense/aspect is not handled reliably
- idioms and local expressions are not translated naturally
- code-switched sentences remain fragmented
- public-service, education, and health terminology need reviewer decisions

## Human review needed

Before this can become a real benchmark:

1. A native Hiligaynon reviewer should edit or reject each `reference_translation`.
2. A second reviewer should check a subset for agreement.
3. Rows should move from `seed_unverified` to `reviewed`.
4. Disagreements should be adjudicated and marked `adjudicated`.
5. The final test split should be frozen before model tuning.

## Why this is still a valid MVP

In a two-hour hackathon, the team cannot honestly claim a production model or a
gold Hiligaynon dataset without speaker validation. The MVP instead delivers the
reproducible infrastructure:

- benchmark schema
- seed benchmark rows
- baseline generation
- automatic scoring
- demo app
- clear path to human validation and later STT/TTS work
