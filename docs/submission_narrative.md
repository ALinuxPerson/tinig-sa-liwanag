# Submission Narrative

## One-line pitch

Sugidanon is an open Hiligaynon code-switch ASR benchmark that shows exactly
where multilingual speech recognition fails when Ilonggo speakers move between
Hiligaynon, Tagalog, and English.

## Problem

Many Philippine languages remain underrepresented in open speech technology.
Generic multilingual ASR systems can appear usable because they catch familiar
English and Tagalog words, while still failing on the regional language that
holds the sentence together.

For Hiligaynon, that failure is hard to improve until it is measurable.

## MVP delivered

This repository ships a reusable speech benchmark, not only a demo app:

- 40 native-recorded Hiligaynon / Tagalog / English code-switch clips
- per-word language tags for `hil`, `tl`, and `en`
- a documented annotation schema and transcription policy
- audio integrity checks and dataset integrity tests
- a switch-region WER scorer that separates ordinary WER from errors near
  language switches
- bundled Whisper baseline predictions
- a benchmark report with overall WER, monolingual Hiligaynon WER,
  switch-region WER, switch penalty, and language-pair breakdowns
- deterministic train / validation / test split CSVs
- a release package builder for metadata, statistics, cards, predictions, and
  benchmark outputs
- a web explorer where judges can play clips, inspect language tags, and see
  token-level ASR errors
- a one-click Colab path for reproduction on a fresh machine

## Key finding

The baseline model performs better near Tagalog and English switch words than
on monolingual Hiligaynon words:

| Region | WER |
|--------|-----|
| Overall | 59.5% |
| Monolingual Hiligaynon | 66.3% |
| Switch-region | 35.8% |
| Switch penalty | -30.6% |

The negative switch penalty is the point: the model is not mainly breaking on
borrowed English or Tagalog words. It is breaking on the Hiligaynon matrix
language.

## Why this fits the project case

The project case asks for reusable open-source infrastructure for Philippine
speech technology. Sugidanon contributes a focused benchmark that future
researchers and developers can extend:

- dataset files with provenance and licensing
- benchmark code that can score new ASR predictions
- reporting that isolates failures by language region
- release packaging for dataset and benchmark artifacts
- a clear path for adding speakers, clips, models, and reviewed language tags

The translation demo and lexicon tools are extension layers. The judged artifact
is the speech benchmark.

## Reproduce

```bash
python3 scripts/build_release.py --overwrite
```

The command validates the ASR annotations, scores the included baseline,
refreshes web benchmark data, and writes a release package under `release/`.

For the minimal benchmark proof:

```bash
python3 scripts/validate.py --kind asr --dir data/annotations
python3 score.py --ref data/annotations --hyp data/predictions
python3 scripts/package_dataset.py --output release --overwrite
```

## Honest limitations

- The current corpus has one speaker and 40 clips.
- Per-word language tags are seed-labeled and need another native-speaker
  confirmation pass before being described as fully adjudicated gold labels.
- The baseline result is preliminary and should be compared with larger ASR
  models.
- The deterministic split falls back to clip-level splitting until more
  speakers are added.

These limits are documented because the project is intended as a trustworthy
benchmark foundation, not a production speech product.

## Next step

The highest-impact next step is to add more Hiligaynon speakers, confirm the
token language tags, and freeze a larger test set for comparing Whisper,
MMS-style models, and future Hiligaynon-tuned ASR systems.
