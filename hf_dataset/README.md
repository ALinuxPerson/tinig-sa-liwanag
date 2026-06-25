---
license: cc-by-4.0
language:
  - hil
  - tl
  - en
pretty_name: Sugidanon Hiligaynon Code-Switched Speech Test Set
task_categories:
  - automatic-speech-recognition
  - audio-classification
task_ids:
  - speech-recognition
tags:
  - hiligaynon
  - ilonggo
  - tagalog
  - filipino
  - code-switching
  - speech-recognition
  - word-error-rate
size_categories:
  - n<1K
---

# Sugidanon 🎙️ — Code-Switch Hiligaynon Speech Benchmark

**The first openly-licensed, code-switch-labeled speech benchmark for Hiligaynon
(Ilonggo) — a language spoken by 9M+ Filipinos yet nearly invisible to modern
speech technology.**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb)
&nbsp;·&nbsp; **Code:** https://github.com/Jazztinn/tinig-sa-liwanag
&nbsp;·&nbsp; **License:** CC BY 4.0

Real Hiligaynon-English-Tagalog speech, labeled per word, with a scorer that
measures what generic models miss: accuracy **at the moment the language
switches**. Run the one-click Colab to reproduce the headline result on a fresh
machine in minutes.

## Why it matters

The Philippines has 130+ languages. Tagalog ASR has advanced; regional tongues
like Hiligaynon have **no open speech datasets, benchmarks, or models**. Real
Ilonggo speech constantly mixes Hiligaynon, Tagalog, and English — exactly where
off-the-shelf systems break. Sugidanon makes that failure **measurable**, so the
next developer has a building block instead of a blank page.

## Headline result

Whisper small (`--language tl`) over the 40 clips:

| Metric | WER |
|--------|-----|
| Overall | 59.8% |
| Monolingual (Hiligaynon) | 66.3% |
| Switch-region | 36.4% |
| **Switch penalty** | **−30.0%** |

By pair: `hil↔en` 40.8%, `hil↔tl` 24.4%, `tl↔en` 6.2%.

**The negative penalty is the finding:** a Tagalog model nails the borrowed
English/Tagalog words but fails on the Hiligaynon matrix it was never trained on.
`tl↔en` is near-solved (6%); `hil↔en` is worst (41%). The gap scales with
Hiligaynon — precisely what this dataset exists to expose.

## What's inside

40 code-switch utterances (~3.1 min) recorded by **Aziel Faith Agustin**, a Hiligaynon
(Ilonggo) speaker who also reviewed the sentences, across
**8 everyday domains** (market, transport, school/work, family, health, culture,
everyday, oral tradition / heritage) and **4 switch types** (`HIL`, `HIL+EN`,
`HIL+TL`, `HIL+TL+EN`). Every word carries a `hil`/`tl`/`en` tag, so the scorer
can isolate switch-region errors.

Transcripts were reviewed by the speaker; per-word language tags are auto-seeded
(`lang_tags_status: seed_unverified`) pending a confirmation pass. Single
speaker — a seed benchmark to extend, not a final model-ranking corpus.

## Quick start

```python
from datasets import load_dataset
ds = load_dataset("LauelKills/sugidanon-hil-codeswitch", data_dir="data/audio", split="train")
ds[0]["audio"], ds[0]["transcript"], ds[0]["switch_type"], ds[0]["tokens"]
```

Or reproduce the benchmark end-to-end with the one-click Colab badge above.

## Languages

- `hil`: Hiligaynon / Ilonggo
- `tl`: Filipino / Tagalog
- `en`: English
- `other`: proper nouns, unclear tokens, or other languages

## Dataset Structure

Expected repository layout:

```text
data/
  audio/
    <clip_id>.wav
  annotations/
    <clip_id>.json
  predictions/
    asr/
      whisper-large-v3-tl/
        <clip_id>.json
      mms-1b-all/
        <clip_id>.json
```

Each annotation contains:

- clip ID
- audio path
- duration
- coarse speaker metadata
- matrix language
- tokenized transcript
- per-token language labels

Example:

```json
{
  "clip_id": "hil_cs_001",
  "audio_file": "audio/hil_cs_001.wav",
  "duration_sec": 3.39,
  "domain": "market",
  "switch_type": "HIL+EN",
  "transcript": "Pila ang grocery budget naton para sa weekend?",
  "matrix_language": "hil",
  "review_status": "reviewed",
  "lang_tags_status": "seed_unverified",
  "tokens": [
    { "idx": 0, "text": "Pila", "lang": "hil" },
    { "idx": 1, "text": "ang", "lang": "hil" },
    { "idx": 2, "text": "grocery", "lang": "en" },
    { "idx": 3, "text": "budget", "lang": "en" },
    { "idx": 4, "text": "naton", "lang": "hil" }
  ]
}
```

## Evaluation

One-command reproduction:

```bash
python3 scripts/eval_asr_baselines.py
```

The script evaluates every model directory under:

```text
data/predictions/asr/
```

It reports:

- overall WER
- switch-region WER
- monolingual WER
- switch penalty

Lower-level scoring:

```bash
python3 score.py --ref data/annotations --hyp data/predictions/asr/whisper-large-v3-tl
```

## Baselines

Included worked-example prediction directories:

- `whisper-large-v3-tl`
- `mms-1b-all`

These files demonstrate the evaluation format. They are not final published
benchmark numbers until real model outputs over the full test set are added.

## Annotation Guidelines

See:

```text
docs/transcription_guidelines.md
```

## Licensing

Dataset files created by Team Hague are released under **CC BY 4.0**.

Code is released under **MIT**.

Third-party resources are not relicensed. See:

```text
docs/licensing.md
LICENSE
```

## Acknowledgments

This dataset exists thanks to **Aziel Faith Agustin**, the Hiligaynon (Ilonggo) speaker who
reviewed the elicitation sentences and recorded all 40 clips. The reference
transcripts and audio are their voice and review.

## Citation

```bibtex
@dataset{team_hague_sugidanon_2026,
  title = {Sugidanon: Code-switched Hiligaynon speech and translation benchmark scaffold},
  author = {{Team Hague}},
  note = {Speech recorded and reviewed by Aziel Faith Agustin (Hiligaynon speaker)},
  year = {2026},
  license = {CC BY 4.0}
}
```

## Baseline result

Whisper small (`--language tl`) over the 40 clips:

| Metric | WER |
|--------|-----|
| Overall | 61.4% |
| Monolingual (Hiligaynon) | 69.2% |
| Switch-region | 38.8% |
| Switch penalty | −30.4% |

The negative penalty is the finding: an off-the-shelf Tagalog model handles the
borrowed English/Tagalog switch words but fails on the Hiligaynon matrix. See
`docs/evaluation_report.md`. Preliminary (Whisper small, single speaker).

## Limitations

- Single speaker — expand speakers before drawing model-level conclusions.
- Per-word language tags are auto-seeded (`seed_unverified`); confirm with the
  speaker before treating the switch/monolingual split as final.
- Baseline uses Whisper small; rerun with large-v3 / MMS for stronger numbers.
