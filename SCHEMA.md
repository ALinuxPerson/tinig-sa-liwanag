# Schema

Sugidanon ships two schemas. The speech MVP artifact is a code-switch-labeled
ASR benchmark (per-word `hil` / `tl` / `en` tags) scored with switch-region WER.
A JSONL translation benchmark supports the later STT -> translation pipeline.

## Primary benchmark path

```text
data/
  benchmark/
    hil_translation_v1.jsonl
  predictions/
    translation_baseline_dict.jsonl
```

## Translation benchmark row

Each line in `data/benchmark/*.jsonl` is one JSON object:

```json
{
  "id": "hil-tr-v1-001",
  "source_lang": "en",
  "target_lang": "hil",
  "domain": "health",
  "source_text": "Please call the doctor if the child has a fever tonight.",
  "reference_translation": "Palihog tawga ang doktor kon may hilanat ang bata karon nga gab-i.",
  "context": "The speaker is giving practical health advice to a family member.",
  "phenomena": ["polite_request", "medical", "conditional"],
  "difficulty": "medium",
  "review_status": "seed_unverified"
}
```

### Required fields

| Field | Type | Rule |
|-------|------|------|
| `id` | string | Unique stable ID, e.g. `hil-tr-v1-001` |
| `source_lang` | string | `en`, `fil`, `tl`, `hil`, or `mixed` |
| `target_lang` | string | Must be `hil` for v1 |
| `domain` | string | Domain bucket such as `health`, `education`, `daily_life` |
| `source_text` | string | Text to translate |
| `reference_translation` | string | Human reference translation into Hiligaynon |
| `context` | string | Extra context needed to preserve meaning |
| `phenomena` | list[string] | What the example tests |
| `difficulty` | string | `easy`, `medium`, or `hard` |
| `review_status` | string | `seed_unverified`, `reviewed`, or `adjudicated` |

### Language codes

| Code | Meaning |
|------|---------|
| `hil` | Hiligaynon / Ilonggo |
| `en` | English |
| `fil` | Filipino |
| `tl` | Tagalog |
| `mixed` | Code-switched input |

Use `fil` for Filipino as a national language label. Use `tl` only when the
example is specifically Tagalog.

### Recommended domains

- `daily_life`
- `health`
- `education`
- `public_service`
- `emergency`
- `agriculture`
- `workplace`
- `code_switching`

### Recommended phenomena labels

- `context_required`
- `paragraph_context`
- `polite_request`
- `conditional`
- `pronoun_reference`
- `tense_aspect`
- `idiom`
- `local_expression`
- `domain_term`
- `code_switching`
- `negation`
- `ambiguity`

## Prediction row

Each line in `data/predictions/translation_*.jsonl` should be:

```json
{
  "id": "hil-tr-v1-001",
  "model": "dict-baseline",
  "prediction": "Palihog tawga ang doktor kon may hilanat ang bata karon nga gab-i."
}
```

`scripts/evaluate_translation.py` joins predictions to references by `id`.

## Human evaluation rubric

Automatic metrics are not enough for Hiligaynon. Use this rubric for reviewed
examples:

| Dimension | 5 | 3 | 1 |
|-----------|---|---|---|
| Adequacy | Meaning fully preserved | Main idea present but details lost | Meaning changed |
| Fluency | Natural Hiligaynon | Understandable but awkward | Unnatural or broken |
| Context | Ambiguity resolved correctly | Partly resolved | Context ignored |
| Terminology | Domain words appropriate | Some questionable choices | Wrong terms |

For each reviewed example, record issue severity:

- `none`
- `minor`
- `major`
- `meaning_changed`

## Code-switch ASR annotation schema

The speech benchmark uses one JSON file per clip. Each clip is a code-switched
Hiligaynon / Tagalog / English utterance with per-word language tags, which is
what makes switch-region WER (`score.py`) possible.

```json
{
  "clip_id": "hil_cs_001",
  "audio_file": "audio/hil_cs_001.wav",
  "duration_sec": 6.4,
  "domain": "daily_life",
  "speaker": {
    "id": "spk01",
    "primary_language": "hil",
    "region": "Iloilo City",
    "age_band": "18-25",
    "gender": "F"
  },
  "matrix_language": "hil",
  "subset": "scripted_native",
  "source_type": "prompted_code_switch",
  "speech_style": "scripted",
  "gold_status": "native_gold",
  "review_status": "seed_unverified",
  "provenance": {
    "source": "Team Hague elicitation set (original)",
    "license": "CC BY 4.0 (text); audio under its own capture license",
    "note": "SEED per-word language tags — native Hiligaynon speaker must review"
  },
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

### ASR fields

| Field | Type | Rule |
|-------|------|------|
| `clip_id` | string | Unique stable ID, e.g. `hil_cs_001` (required) |
| `audio_file` | string | Path relative to `data/`, e.g. `audio/hil_cs_001.wav` (required) |
| `tokens` | list | Per-word `{idx, text, lang}`, `idx` contiguous from 0 (required) |
| `domain` | string | Domain bucket (optional) |
| `speaker` | object | `id`, `name`, `primary_language`, `fluency`, `region`, `age_band`, `gender` (optional) |
| `speaker.fluency` | string | `native`, `fluent`, or `non_native` — Hiligaynon fluency. Do not present `non_native` clips as native gold data. |
| `matrix_language` | string | Base language of the utterance (optional) |
| `subset` | string | Benchmark subset — see below (optional) |
| `source_type` | string | `prompted_code_switch`, `podcast`, `vlog`, `non_native_recording` (optional) |
| `speech_style` | string | `scripted`, `conversational`, `interview`, `monologue`, `mixed` (optional) |
| `gold_status` | string | `native_gold`, `reviewed_extension`, `seed_unverified`, `not_native_gold` (optional) |
| `review_status` | string | `seed_unverified`, `reviewed`, or `adjudicated` (optional) |
| `provenance` | object | `source`, `license`, `note` for redistribution (optional) |

Token `lang` is one of `hil`, `tl`, `en`, `other`.

### Benchmark subsets

Keep each speech source separate. Do **not** blend subsets into one headline WER —
report each separately, and never count non-native speech as native gold.

| Subset | Speaker | Speech type | Use in reporting |
|--------|---------|-------------|------------------|
| `scripted_native` | Native | Prompted code-switch clips | Main headline benchmark |
| `native_podcast` | Native | Natural long-form segments | Natural-speech extension |
| `native_vlog` | Native | Everyday conversational speech | Everyday-speech extension |
| `non_native_eval` | Non-native | Learner / non-native speech | Robustness / stress test only |

For non-native clips set `subset: "non_native_eval"`, `gold_status:
"not_native_gold"`, and `speaker.fluency: "non_native"`.

### Pipeline

```bash
# generate / refresh the code-switch annotation stubs from the elicitation set
python3 scripts/build_codeswitch_set.py

# capture audio for one prompt + emit its annotation
python3 scripts/record.py --prompt 1 --seconds 8

# validate (drop --no-audio-check once wavs exist)
python3 scripts/validate.py --kind asr --dir data/annotations --no-audio-check

# score switch-region WER against ASR predictions
python3 score.py --ref data/annotations --hyp data/predictions
```

See `docs/recording_kit.md` for the full capture workflow. Seed language tags
must be confirmed by a Hiligaynon speaker before the clip is treated as gold.
