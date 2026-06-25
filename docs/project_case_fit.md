# Project Case Fit

## Artifact

Sugidanon is an open Hiligaynon code-switch ASR benchmark.

It is not only a transcription app. It ships the reusable pieces another
developer or researcher needs to test speech recognition on Hiligaynon /
Tagalog / English code-switch speech:

- native-recorded clips
- per-word language tags
- annotation schema
- transcription guidelines
- validation checks
- ASR baseline predictions
- switch-region WER scorer
- deterministic split files
- dataset and benchmark release packaging
- web benchmark explorer

## Why It Matters

Off-the-shelf multilingual ASR can look better than it is because it recognizes
borrowed English and Tagalog words while missing the Hiligaynon matrix language.
Sugidanon measures that hidden failure directly.

Current baseline:

| Metric | Result |
|--------|--------|
| Overall WER | 59.5% |
| Monolingual Hiligaynon WER | 66.3% |
| Switch-region WER | 35.8% |
| Switch penalty | -30.6% |

The negative switch penalty means the model performs better near switch words
than on ordinary Hiligaynon. That is the benchmark finding.

## Reproduce

```bash
python3 scripts/build_release.py --overwrite
```

This validates the ASR annotations, scores the bundled baseline, refreshes
`public/benchmark.json`, and writes a release package under `release/`.

Minimal proof:

```bash
python3 scripts/validate.py --kind asr --dir data/annotations
python3 score.py --ref data/annotations --hyp data/predictions
```

## Reusable Outputs

The release package includes:

- `dataset/metadata.csv`
- `dataset/metadata.jsonl`
- `dataset/statistics.json`
- `dataset/train.csv`
- `dataset/validation.csv`
- `dataset/test.csv`
- `dataset/dataset_card.md`
- `benchmark/results.json`
- `benchmark/score.txt`
- `benchmark/report.md`
- bundled prediction JSON files

## Honest Limits

- 40 clips
- one current speaker
- token language tags are seed-labeled pending another native-speaker pass
- split is clip-level until more speakers exist

Those limits are documented so the benchmark is reusable and extensible without
overclaiming.
