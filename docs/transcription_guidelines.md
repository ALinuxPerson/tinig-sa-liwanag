# Transcription Guidelines

These guidelines define how to transcribe and label the code-switched
Hiligaynon, Filipino/Tagalog, and English speech test set.

## Goal

Create a labeled test set that can measure ASR performance on:

- overall word error rate
- words near language switch points
- Hiligaynon, Filipino/Tagalog, and English code-switching
- future model comparisons such as Whisper and MMS

## Audio requirements

- Preferred format: 16 kHz mono WAV.
- Keep clips short: 4-10 seconds when possible.
- Avoid background music and heavy overlapping speech.
- Store audio as `data/audio/<clip_id>.wav`.
- Do not publish audio without speaker consent.

## File format

Each clip has one JSON annotation in `data/annotations/`.

```json
{
  "clip_id": "hil_en_001",
  "audio_file": "audio/hil_en_001.wav",
  "duration_sec": 6.4,
  "speaker": {
    "id": "spk01",
    "primary_language": "hil",
    "region": "Iloilo City",
    "age_band": "18-25",
    "gender": "F"
  },
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

## Transcription rules

- Transcribe what was said, not what the speaker meant to say.
- Preserve ordinary spelling used by speakers when it is clear.
- Keep punctuation out of tokens.
- Do not lowercase manually only for scoring; keep natural casing in annotation.
- Use one token per spoken word.
- Keep common code-switched compounds as spoken when they function as one unit,
  e.g. `Nag-grocery`.
- Mark unintelligible speech as `[unk]` with `lang: "other"`.
- Mark non-speech events only if they affect comprehension, e.g. `[laugh]`.

## Language tags

Use:

| Tag | Meaning |
|-----|---------|
| `hil` | Hiligaynon / Ilonggo |
| `tl` | Filipino / Tagalog |
| `en` | English |
| `other` | proper nouns, unclear tokens, another language, or non-speech marker |

## Tagging rules

- Tag by lexical source, not accent. English `traffic` with an Ilonggo accent is
  still `en`.
- Tag established Hiligaynon borrowed words as `hil` when they are naturalized
  in Hiligaynon use.
- Tag proper names, brands, and place names as `other`.
- Tag numbers by the language actually spoken.
- If a word is identical in Hiligaynon and Tagalog, use the sentence's
  `matrix_language`.
- Use `matrix_language` for fillers when the filler is not clearly from another
  language.

## Quality control

- Every clip should be reviewed by at least one native or fluent speaker.
- At least 20% of clips should be double-annotated.
- Resolve disagreements in a separate adjudication pass.
- Track known uncertainty in a notes file or issue, not by silently changing the
  schema.

## Validation

```bash
python3 scripts/validate.py --kind asr --dir data/annotations
```

Use `--no-audio-check` only while drafting annotation stubs before audio exists.

## Evaluation

Run the judge-facing release pipeline:

```bash
python3 scripts/build_release.py --overwrite
```

Run a single prediction directory with the lower-level scorer:

```bash
python3 score.py --ref data/annotations --hyp data/predictions
```
