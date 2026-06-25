# non_native_eval

20-slot robustness subset for non-native Hiligaynon speech.

This subset is **not** native gold and is **not** part of headline WER. It exists
to test how ASR behaves when a non-native speaker reads Hiligaynon /
Tagalog / English code-switch prompts.

## Status

- Planned clips: 20
- Current checked-in audio: 0
- Current checked-in annotations: 0
- Source: local Team Hague recording only, after speaker consent
- Public release status: not ready until audio, transcript review, token-language
  review, and consent/provenance are complete

## Required layout after recording

```text
data/extensions/non_native_eval/
  audio/nonnat_001.wav
  annotations/nonnat_001.json
  predictions/nonnat_001.json
  ...
```

Annotation rules:

- `subset: non_native_eval`
- `source_type: non_native_recording`
- `speaker.fluency: non_native`
- `gold_status: not_native_gold`
- `review_status: seed_unverified` until transcript review
- `lang_tags_status: seed_unverified` until token-language review

Run readiness check:

```bash
python3 scripts/validate_non_native_eval.py
```
