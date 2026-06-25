# Schema

Tinig sa Liwanag now uses a translation-first schema. The primary artifact is a
JSONL benchmark for context-aware translation into Hiligaynon.

Legacy code-switched ASR annotations are still supported for future speech work,
but they are no longer the main v1 deliverable.

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

## Legacy ASR annotation schema

The earlier speech benchmark used one JSON file per clip:

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

This remains supported by:

```bash
python3 scripts/validate.py --kind asr --dir data/annotations --no-audio-check
python3 score.py --ref data/annotations --hyp data/predictions
```
