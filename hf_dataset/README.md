---
license: cc-by-4.0
language:
  - hil
  - tl
  - en
pretty_name: Tinig sa Liwanag / Sugidanon Hiligaynon Code-Switched Speech Test Set
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

# Dataset Card: Tinig sa Liwanag / Sugidanon

## Dataset Summary

Tinig sa Liwanag / Sugidanon is a small, open, labeled test-set scaffold for
evaluating code-switched Hiligaynon, Filipino/Tagalog, and English speech
recognition.

The dataset is designed to measure not only overall WER, but also WER near
language switch points. This is important for Philippine speech technology
because real speech often mixes regional languages, Filipino/Tagalog, and
English.

Current repository status: worked-example scaffold. Replace or extend the sample
annotation with consented audio and reviewed transcripts before treating this as
a final benchmark release.

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
  "clip_id": "hil_en_001",
  "audio_file": "audio/hil_en_001.wav",
  "duration_sec": 6.4,
  "matrix_language": "hil",
  "tokens": [
    { "idx": 0, "text": "Nag-grocery", "lang": "hil" },
    { "idx": 1, "text": "ko", "lang": "hil" },
    { "idx": 2, "text": "kahapon", "lang": "hil" },
    { "idx": 3, "text": "kay", "lang": "hil" },
    { "idx": 4, "text": "super", "lang": "tl" },
    { "idx": 5, "text": "traffic", "lang": "en" }
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
@dataset{team_hague_tinig_sa_liwanag_2026,
  title = {Tinig sa Liwanag / Sugidanon: Code-switched Hiligaynon speech and translation benchmark scaffold},
  author = {{Team Hague}},
  year = {2026},
  license = {CC BY 4.0}
}
```

## Limitations

- Current repository data is a scaffold and worked example.
- Real audio requires consented speakers and reviewed transcripts.
- The test set should be expanded before drawing model-level conclusions.
- Per-token language labels require human review.
