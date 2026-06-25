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

# Dataset Card: Sugidanon

## Dataset Summary

Sugidanon is a small, open, labeled test set for evaluating code-switched
Hiligaynon, Filipino/Tagalog, and English speech recognition.

It is designed to measure not only overall WER, but also WER near language
switch points — the switch penalty. This matters for Philippine speech
technology because real speech mixes regional languages, Filipino/Tagalog, and
English.

**Contents:** 40 code-switch utterances (~3.1 min) recorded by one Hiligaynon
speaker, across 8 domains (market, transport, school/work, family, health,
culture, everyday, oral tradition) and 4 switch types (`HIL`, `HIL+EN`,
`HIL+TL`, `HIL+TL+EN`). The reference transcripts were reviewed by the speaker;
per-word language tags are auto-seeded and marked `lang_tags_status:
seed_unverified` pending the speaker's confirmation. Single-speaker — expand
before drawing model-level conclusions.

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

## Citation

```bibtex
@dataset{team_hague_sugidanon_2026,
  title = {Sugidanon: Code-switched Hiligaynon speech and translation benchmark scaffold},
  author = {{Team Hague}},
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
