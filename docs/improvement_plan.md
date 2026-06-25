# Sugidanon Improvement Plan

## Goal

Improve Sugidanon's judging strength without turning it into a generic speech
pipeline. The project should be presented as:

> An open Hiligaynon / Tagalog / English code-switch ASR benchmark that exposes
> where multilingual speech recognition fails, using token-level language tags,
> switch-region WER, reproducible baselines, and real-world Hiligaynon speech
> subsets.

The strongest path is to make the benchmark more focused, more reproducible,
and easier to understand in a live demo.

## Judging Criteria Strategy

| Criterion | Improvement Target |
|-----------|--------------------|
| Innovation & Creativity | Make switch-region WER and code-switch failure analysis the central contribution. |
| Technical Execution | Add clean subset metadata, consistent benchmark numbers, release artifacts, validation, and multiple ASR baselines. |
| Design & User Experience | Add a benchmark demo view with playable audio, colored language tags, ASR predictions, highlighted errors, and simple charts. |
| Theme Relevance & Impact | Expand from scripted clips to real Hiligaynon speech contexts while keeping native, podcast, vlog, and non-native data separate. |

## Priority 0: Fix Credibility Issues

These should be done first because they directly affect judge trust.

### 1. Use one canonical benchmark result

Current documentation has inconsistent WER values. Pick one canonical result and
use it everywhere.

Recommended current canonical values:

| Metric | Value |
|--------|-------|
| Overall WER | 61.4% |
| Monolingual Hiligaynon WER | 69.2% |
| Switch-region WER | 38.8% |
| Switch penalty | -30.4% |
| `hil<->en` switch WER | 44.2% |
| `hil<->tl` switch WER | 24.4% |
| `tl<->en` switch WER | 6.2% |

Files to check:

- `README.md`
- `hf_dataset/README.md`
- `docs/evaluation_report.md`
- `results/asr_score.txt`
- generated release reports

### 2. Clarify the main pitch

The README should lead with the speech benchmark, not the translation scaffold.

Recommended top-level framing:

```text
Sugidanon is an open Hiligaynon code-switch ASR benchmark. It measures where
multilingual speech models fail by separating ordinary WER from switch-region
WER across Hiligaynon, Tagalog, and English tokens.
```

Translation, Tinig, G2P, and TTS should be described as extensions or future
layers, not the primary judged artifact.

## Priority 1: Strengthen the Dataset

### 3. Add explicit dataset subsets

Keep each speech source separate so the benchmark remains interpretable.

Recommended subset names:

| Subset | Speaker Type | Speech Type | Use in Reporting |
|--------|--------------|-------------|------------------|
| `scripted_native` | Native | Prompted code-switch clips | Main headline benchmark |
| `native_podcast` | Native | Natural long-form speech segments | Separate natural-speech extension |
| `native_vlog` | Native | Everyday conversational speech | Separate everyday-speech extension |
| `non_native_eval` | Non-native | Learner or non-native speech | Robustness/stress test only |

Do not blend all subsets into one headline WER. Report each subset separately.

### 4. Add subset metadata to ASR annotations

Add these optional fields to each ASR JSON annotation:

```json
{
  "subset": "scripted_native",
  "source_type": "prompted_code_switch",
  "speech_style": "scripted",
  "gold_status": "native_gold"
}
```

Recommended values:

| Field | Suggested Values |
|-------|------------------|
| `subset` | `scripted_native`, `native_podcast`, `native_vlog`, `non_native_eval` |
| `source_type` | `prompted_code_switch`, `podcast`, `vlog`, `non_native_recording` |
| `speech_style` | `scripted`, `conversational`, `interview`, `monologue`, `mixed` |
| `gold_status` | `native_gold`, `reviewed_extension`, `seed_unverified`, `not_native_gold` |

For non-native clips, use:

```json
{
  "subset": "non_native_eval",
  "gold_status": "not_native_gold",
  "speaker": {
    "fluency": "non_native"
  }
}
```

### 5. Add podcast and vlog data carefully

Use the native Hiligaynon podcast and everyday-life vlog only when rights are
documented.

For each external source, record:

- source title
- source URL
- creator or rights holder
- license or permission status
- date accessed
- whether audio redistribution is allowed
- attribution text required by the license
- notes about excluded sections, such as music, intro, outro, or overlapping speech

Recommended clip policy:

- segment into 5-15 second clips
- avoid background music
- avoid overlapping speakers unless explicitly labeled
- avoid private or personally identifying content
- convert to mono 16 kHz WAV
- manually review transcripts before using as benchmark references

## Priority 2: Improve Benchmark Reporting

### 6. Make switch-region WER the main innovation

Add a short explanation near the top of README and demo pages:

```text
Overall WER hides which language failed. Sugidanon separates errors on
Hiligaynon matrix-language words from errors near Tagalog and English switch
points, making code-switch ASR failure measurable.
```

Include a table like:

| Region | WER | Interpretation |
|--------|-----|----------------|
| Monolingual Hiligaynon | 69.2% | The model struggles most with Hiligaynon words. |
| Switch-region | 38.8% | Borrowed English/Tagalog words are easier. |
| `hil<->en` | 44.2% | Hardest switch pair. |
| `tl<->en` | 6.2% | Mostly solved by existing models. |

### 7. Report scores by subset

Update benchmark reports to show:

| Subset | Clips | Overall WER | HIL WER | Switch WER | Notes |
|--------|-------|-------------|---------|------------|-------|
| `scripted_native` | 40 | current | current | current | Main benchmark |
| `native_podcast` | TBD | TBD | TBD | TBD | Natural speech |
| `native_vlog` | TBD | TBD | TBD | TBD | Everyday speech |
| `non_native_eval` | TBD | TBD | TBD | TBD | Robustness only |

This improves technical credibility and prevents misleading aggregate numbers.

### 8. Add at least one more ASR baseline

Current baseline is useful, but one additional model or configuration would make
the benchmark more convincing.

Recommended options:

- Whisper small with Tagalog forcing
- Whisper small with automatic language detection
- Whisper large-v3
- Meta MMS

Report:

| Model | Overall WER | HIL WER | Switch WER | Switch Penalty |
|-------|-------------|---------|------------|----------------|
| Whisper small `--language tl` | 61.4% | 69.2% | 38.8% | -30.4% |
| Whisper auto | TBD | TBD | TBD | TBD |
| Whisper large-v3 | TBD | TBD | TBD | TBD |

## Priority 3: Improve Demo and UX

### 9. Add a benchmark demo section

Add a `/benchmark` page or homepage section focused on the ASR benchmark.

Minimum useful features:

- audio player for selected clips
- reference transcript
- model prediction
- colored tokens by language
- highlighted ASR errors
- per-clip WER
- filter by subset
- chart for monolingual WER vs switch-region WER

Suggested token colors:

| Language | Color Purpose |
|----------|---------------|
| `hil` | Hiligaynon matrix-language words |
| `tl` | Tagalog / Filipino words |
| `en` | English words |
| `other` | proper nouns, unclear tokens, or other languages |

Example presentation:

```text
Reference:
[hil] Pila [hil] ang [en] grocery [en] budget [hil] naton?

Whisper:
Pila ang grocery budget natin?

Observed error:
naton -> natin
```

### 10. Add a 60-second judge demo path

The live presentation should follow one clear sequence:

1. Play one Hiligaynon code-switch clip.
2. Show reference transcript with language colors.
3. Show Whisper prediction.
4. Highlight the ASR mistake.
5. Show switch-region WER and monolingual Hiligaynon WER.
6. Explain the finding: the model catches borrowed English/Tagalog terms but
   misses Hiligaynon matrix-language words.

## Priority 4: Release Packaging

### 11. Generate a clean release folder

The release package should be easy for another developer to reuse.

Target structure:

```text
release/
  dataset/
    audio/
    annotations/
    metadata.csv
    metadata.jsonl
    statistics.json
    dataset_card.md
  benchmark/
    predictions/
    results.json
    report.md
```

The package should clearly say whether audio is included and under what license.

### 12. Add statistics by subset

`statistics.json` should include:

- clip count
- total duration
- average duration
- speaker count
- subset counts
- domain counts
- switch-type counts
- token-language counts
- review-status counts
- license/provenance summary

## Priority 5: Documentation and Ethics

### 13. Update the dataset card

The dataset card should clearly describe:

- what is included
- what is not included
- speaker fluency labels
- source subsets
- review status
- redistribution rights
- intended use
- prohibited use
- limitations

Important limitation language:

```text
Non-native clips are included only as a robustness subset and should not be used
as native Hiligaynon gold data.
```

### 14. Add source attribution records

Create or update a source ledger, for example:

```text
docs/source_ledger.md
```

Recommended columns:

| Source ID | Title | URL | Rights | Subset | Clips | Notes |
|-----------|-------|-----|--------|--------|-------|-------|
| `src_scripted_01` | Team Hague elicitation set | local | CC BY 4.0 | `scripted_native` | 40 | Speaker consented |
| `src_podcast_01` | TBD | TBD | TBD | `native_podcast` | TBD | Exclude music |
| `src_vlog_01` | TBD | TBD | TBD | `native_vlog` | TBD | Everyday speech |

## Implementation Checklist

### Must Do

- [ ] Fix WER inconsistencies across README, dataset card, and evaluation report.
- [ ] Rewrite README opening around code-switch ASR benchmark.
- [ ] Add dataset subset definitions to `SCHEMA.md`.
- [ ] Add subset/source metadata to existing ASR annotations.
- [ ] Add source ledger for scripted, podcast, vlog, and non-native data.
- [ ] Keep non-native clips out of the native headline score.
- [ ] Report benchmark metrics by subset.

### Should Do

- [ ] Add podcast clips as `native_podcast`.
- [ ] Add vlog clips as `native_vlog`.
- [ ] Add non-native clips as `non_native_eval`.
- [ ] Add one more ASR baseline.
- [ ] Generate `release/dataset/statistics.json`.
- [ ] Generate `release/benchmark/report.md`.
- [ ] Update Hugging Face dataset card with subset structure.

### Nice To Have

- [ ] Add `/benchmark` web demo page.
- [ ] Add colored token display.
- [ ] Add audio playback per benchmark example.
- [ ] Add ASR error highlighting.
- [ ] Add WER charts.
- [ ] Add a small leaderboard-style model comparison table.

## What Not To Do

- Do not copy a generic dataset ingestion toolkit pattern.
- Do not mix native and non-native speech into one headline benchmark score.
- Do not publish external audio without documented redistribution rights.
- Do not claim token language tags are gold if they are still seed-unverified.
- Do not lead the project pitch with translation if the judged artifact is the
  speech benchmark.
- Do not overclaim production ASR quality from a small benchmark.

## Best Final Positioning

Sugidanon should be presented as a focused benchmark, not a broad platform:

```text
BosesPH-style projects build general dataset pipelines. Sugidanon provides a
focused Hiligaynon code-switch benchmark that makes a specific ASR failure mode
visible: current multilingual models often recognize borrowed English and
Tagalog words, but fail on the Hiligaynon matrix language.
```

This position is distinct, honest, and aligned with the challenge criteria.
