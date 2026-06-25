# Team Hague

**ACM TechSprint Asteria Submission**  
**Event dates:** June 25-27, 2026

**Live demo:**

```text
https://tinig-sa-liwanag.vercel.app   # Sugidanon — project site, benchmark & docs
```

**Source code & deployment (GitHub):**

```text
https://github.com/Jazztinn/tinig-sa-liwanag
```

The Vercel site auto-deploys from this repo's `main` branch to
`https://tinig-sa-liwanag.vercel.app`.

**Open dataset (Hugging Face):**

```text
https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch
```

40 native-recorded code-switch Hiligaynon/Tagalog/English clips with per-word
language tags and switch-region WER scoring. A second 40-clip native-speaker
extension is included locally for robustness reporting. CC BY 4.0.

**Reproduce the benchmark (one-click Google Colab):**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb)

```text
https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb
```

Downloads the dataset, runs the ASR baseline, and prints the switch penalty on a
fresh machine — no local setup.

**ASR model tested (baseline):**

```text
OpenAI Whisper:  https://github.com/openai/whisper
Meta MMS:        https://huggingface.co/facebook/mms-1b-all
```

## Team members, roles and rules

| Member | Primary role |
|--------|--------------|
| Legaspi, Jazztinn Kyle | Lead / pipeline, evaluation scripts, demo app |
| Michael C. Baterna | Benchmark data, schema, domain examples |
| Arwin Jeremy Bumpus | Frontend / demo UI, documentation |
| De Guzman, Nimeesha | Lexicon, Tagalog/Hiligaynon bridge, review coordination |

## Acknowledgments

- **Aziel Faith Agustin** — Hiligaynon (Ilonggo) speaker who reviewed the elicitation
  sentences and recorded all 40 clips in the speech corpus. The dataset's
  reference transcripts and audio exist thanks to their voice and review.

Working rules:

- Per-word language tags must be reviewed by a qualified speaker before they are
  treated as headline benchmark labels.
- AI output is never treated as authoritative language ground truth.
- Every commit keeps the core benchmark tooling dependency-free (stdlib).
- Source provenance and license are recorded for any third-party data.
- Decisions and scope changes are agreed by the team before merging to `main`.

# Sugidanon

**An open Hiligaynon / Tagalog / English code-switch ASR benchmark.** It measures
where multilingual speech models fail by separating ordinary WER from
switch-region WER across Hiligaynon, Tagalog, and English tokens.

This repository is scoped around one question:

> Where does multilingual speech recognition break on Hiligaynon code-switch
> speech — on the borrowed words, or on the Hiligaynon matrix language?

Overall WER hides which language failed. Sugidanon separates errors on
Hiligaynon matrix-language words from errors near Tagalog and English switch
points, making code-switch ASR failure measurable.

## Current deliverable

The repository targets the **Inclusive Speech Technology for Philippine
Languages** challenge by shipping a focused benchmark:

- 40 native-recorded Hiligaynon/Tagalog/English code-switch clips with per-word
  language tags
- a separate 40-clip second-speaker extension for robustness analysis
- a 20-line non-native evaluation scaffold for future robustness testing
- a switch-region WER scorer (overall WER, monolingual WER, switch penalty)
- speaker, domain, switch-type, token-language, and language-pair ASR
  breakdown reports
- a reproducible Whisper baseline (one-click Colab)
- an annotation schema for reviewed code-switch references
- documentation, dataset card, and provenance records

The headline finding:

```text
Current multilingual models recognize borrowed English and Tagalog words,
but fail on the Hiligaynon matrix language.
```

Live demos are linked at the top of this README.

## Features

- **Code-switch ASR benchmark** — 40 frozen headline native clips with per-word
  language tags and switch-region WER scoring (`score.py`).
- **Switch-region WER scorer** — overall WER, monolingual Hiligaynon WER,
  switch-region WER, switch penalty, and per-language-pair breakdown.
- **Robustness breakdowns** — `scripts/analyze_asr_breakdowns.py` reports ASR
  performance by speaker, domain, switch type, token language, and switch pair,
  including the second-speaker extension.
- **Non-native evaluation scaffold** — `data/extensions/non_native_eval/` has a
  20-line recording manifest plus readiness validator; no fake or unlicensed
  audio is counted.
- **Reproducible baseline** — Whisper runner + one-click Colab over the public
  Hugging Face dataset, zero local setup.
- **Annotation schema** (`SCHEMA.md`) for reviewed code-switch references and
  token language tags.
- **Token-tag review CLI** — `scripts/review_annotations.py` for native-speaker
  confirmation of seed tags.

### Extension layers (not the primary judged artifact)

The repository also carries text-translation and assistant layers that build on
the benchmark and are kept for the later STT → translation → TTS phase:

- **Context-aware translation benchmark** — JSONL examples labeled with domain,
  context notes, phenomena, difficulty, and review status, plus an offline
  dictionary baseline and automatic evaluator.
- **Lexicon tooling** — curated `data/lexicon_hil.tsv` plus Kaikki/Wiktionary
  en→hil and Tagalog→Hiligaynon bridge builders.
- **Future speech utilities** — Hiligaynon G2P and TTS routing for the later
  STT/TTS phase.

## Why this matters

The Philippines has 130+ languages, yet most regional tongues stay invisible to
modern speech technology. Hiligaynon (Ilonggo) — spoken by 9M+ people across
Iloilo, Negros, Guimaras, and Panay, and carrier of a deep oral tradition (the
*sugidanon* epic chants this project is named for) — is one of them.
Off-the-shelf speech models are rarely even *measured* on Ilonggo, so no one had
quantified where they fail.

Sugidanon makes that failure measurable. Its core contribution is
**switch-region WER**: instead of one blunt error rate, it separates errors on
borrowed English/Tagalog words from errors on the Hiligaynon matrix language.
The finding is sharp and reproducible — current models transcribe the borrowed
words well but miss the Hiligaynon itself, a **negative switch penalty** that
puts a number on exactly what gets erased.

Measurement is the first act of inclusion:

- Overall WER hides which language failed; switch-region WER exposes it.
- An open, per-word-tagged corpus recorded and reviewed by native Ilonggo
  speakers turns heritage speech — including an `oral_tradition` domain — into
  reusable data, owned by the community (CC BY 4.0), not extracted from it.
- A reproducible benchmark makes the gap fundable and fixable, and the same
  clips and tags can later seed STT/TTS and speech-to-speech evaluation.

Rather than a finished consumer product, Sugidanon is a building block — a
measuring stick and an open corpus that future developers and researchers can
extend into inclusive speech systems, so every Filipino voice gets a seat at the
table before it disappears.

## Project case

The challenge is to contribute a reusable, open-source artifact that advances
speech technology for Philippine languages or code-switched speech. Teams are
expected to build foundational infrastructure such as speech datasets,
evaluation benchmarks, fine-tuned models, or reproducible data pipelines that
future developers and researchers can extend.

The focus is not simply to build an application. The focus is to create open
resources that help bring every Filipino voice into the light.

Our interpretation of the project case:

- Start with Hiligaynon because it is underrepresented compared with Tagalog.
- Build a benchmark and reproducible pipeline before claiming a production model.
- Lead with the code-switch ASR benchmark; keep translation as an extension layer.
- Make limitations explicit: the headline benchmark is one speaker and 40 clips;
  the second speaker is reported as an extension until a multi-speaker release
  decision is made.

## What we developed

During the hackathon, we narrowed the original STT/TTS idea into a realistic
MVP: a focused Hiligaynon code-switch ASR benchmark that future speech systems
can evaluate against.

We developed:

- 40 native-recorded Hiligaynon / Tagalog / English code-switch clips
- 40 additional reviewed second-speaker extension clips kept outside the frozen
  headline score
- 20 planned non-native evaluation prompts kept outside scoring until consented
  audio and reviewed annotations exist
- per-word `hil` / `tl` / `en` language tags
- a Hugging Face-style dataset card for the labeled ASR test set
- a JSON annotation schema for clips, speaker metadata, transcripts, and token
  language tags
- a switch-region WER scorer with monolingual, switch-region, switch penalty,
  and language-pair breakdowns
- an ASR breakdown reporter for speaker, domain, switch type, and token-language
  error analysis
- a non-native evaluation scaffold with manifest, recording script, and readiness
  validator
- bundled Whisper baseline predictions and reproducible benchmark reports
- a judge-facing release pipeline (`scripts/build_release.py`)
- deterministic dataset split CSVs and release packaging
- dataset integrity tests for audio shape, duplicates, prediction coverage, and
  packaging
- transcription guidelines and clear dataset/code licensing notes
- a Next.js/Vercel benchmark explorer with audio playback and token-level error
  visualization
- an optional Tagalog-to-Hiligaynon phrase and lexicon layer for later
  translation demos
- a script for building a larger noisy Tagalog -> Hiligaynon bridge lexicon from
  Kaikki/Wiktionary dictionaries
- documentation for future native-speaker review, stronger ASR baselines, and
  downstream STT/translation/TTS extension

This is not yet a production ASR model. It is the benchmark and release scaffold
that makes future Hiligaynon speech work measurable.

## MVP

The MVP is:

> A reproducible Hiligaynon code-switch ASR benchmark with native-recorded
> clips, per-word language tags, switch-region WER scoring, and a benchmark
> explorer.

The MVP demonstrates:

- how code-switch speech clips are represented
- how baseline ASR predictions are scored
- where multilingual ASR fails on Hiligaynon compared with borrowed Tagalog and
  English words
- how future Hiligaynon reviewers can validate or correct token language tags
- how another researcher can package and extend the dataset

For demo quality, the deployed app includes:

1. a landing page summarizing the benchmark finding
2. an interactive benchmark explorer with audio playback
3. a smaller translation demo kept as an extension layer

The research artifact is the speech benchmark and evaluation pipeline.

## Technologies Used

- **Python 3** (stdlib only for the core benchmark tooling — no install needed)
- **Next.js / React** + **Vercel** for the hosted benchmark explorer and demo
- **Node.js / npm** for the web app build
- **OpenAI Whisper** and **Meta MMS** for ASR baselines
- **ffmpeg** for optional audio conversion workflows
- **Hugging Face `transformers` + `torch`** for optional neural extension work
- **Ollama** and **Kaikki.org / Wiktextract** for optional translation and
  lexicon extension layers
- Evaluation: custom switch-region WER, monolingual WER, switch penalty, token
  F1, and chrF-style metrics where appropriate

## Repository structure

```text
sugidanon/
├── README.md
├── SCHEMA.md
├── RESOURCES.md
├── AI_DISCLOSURE.md
├── hf_dataset/
│   └── README.md                    # Hugging Face dataset card
├── package.json                     # Next.js/Vercel app
├── pages/
│   ├── index.js                     # live benchmark explorer (metrics + clip token-diff)
│   └── api/translate.js             # optional translation extension API
├── styles/
│   └── globals.css
├── BENCHMARK.md                     # benchmark card: protocol, cohorts, reproducibility
├── score.py                         # switch-region ASR WER scorer (--ci for bootstrap CIs)
├── data/benchmark/MANIFEST.json     # frozen, content-addressed benchmark version
├── scripts/
│   ├── freeze_benchmark.py           # write/verify the frozen MANIFEST (drift gate)
│   ├── build_release.py              # judge-facing validation + package pipeline
│   ├── build_benchmark_web.py        # static data for the explorer (public/benchmark.json)
│   ├── validate.py                   # validates ASR benchmark or translation files
│   ├── benchmark_asr.py              # optional Whisper refresh + scoring
│   ├── package_dataset.py            # release package builder
│   ├── split_dataset.py              # deterministic split CSV builder
│   ├── review_annotations.py         # terminal language-tag review
│   ├── evaluate_translation.py       # optional translation extension evaluator
│   ├── generate_baseline_predictions.py
│   └── ...                           # future speech/G2P utilities
├── data/
│   ├── annotations/                  # primary ASR annotations
│   ├── audio/                        # native-recorded Hiligaynon clips
│   ├── predictions/                  # ASR JSON predictions + translation JSONL baseline
│   ├── benchmark/
│   │   └── hil_translation_v1.jsonl  # optional translation extension
│   └── lexicon_hil.tsv               # curated dictionary entries
├── app/
│   ├── server.py
│   └── index.html                    # legacy local Python demo
├── docs/
│   ├── evaluation_report.md
│   ├── licensing.md
│   ├── project_case_fit.md
│   ├── submission_narrative.md
│   └── transcription_guidelines.md
└── results/
    ├── asr_baselines.md
    ├── asr_score.txt
    └── baseline.md
```

## Quick start

No installs are required for the core ASR benchmark tooling.

```bash
# validate, score, refresh web benchmark data, and package the release
python3 scripts/build_release.py --overwrite

# minimal proof
python3 scripts/validate.py --kind asr --dir data/annotations
python3 score.py --ref data/annotations --hyp data/predictions

# run the web app
npm install
npm run dev
```

Then open `http://localhost:3000`.

## Code-switch ASR benchmark (speech MVP)

The speech deliverable is a code-switch-labeled corpus plus a switch-region WER
benchmark. The distinctive measurement is the **switch penalty**: how much worse
an ASR model does on words next to a Hiligaynon/Tagalog/English language switch
versus monolingual words.

What ships:

- **40 code-switch-labeled clips** in `data/annotations/` (`hil_cs_001`..`040`),
  authored as a draft and **reviewed by a Hiligaynon speaker**, who also records
  the audio. Eight domains (market, transport, school/work, family, health,
  culture, everyday, oral tradition) and four switch types (`HIL`, `HIL+EN`,
  `HIL+TL`, `HIL+TL+EN`). Reference text and per-word `hil`/`tl`/`en` tags are
  speaker-reviewed.
- **`score.py`** — switch-region WER, monolingual WER, switch penalty, and a
  per-language-pair breakdown (`hil<->tl`, `hil<->en`, `tl<->en`).
- **One-command release pipeline** — `scripts/build_release.py` validates the
  annotations, checks prediction coverage, scores switch-region WER, refreshes
  web benchmark data, and builds a release package.
- **Release packager** — `scripts/package_dataset.py` exports metadata,
  statistics, dataset card, predictions, and benchmark report to `release/`.
- **Dataset split tool** — `scripts/split_dataset.py` writes deterministic
  `train.csv`, `validation.csv`, and `test.csv` splits, using speaker-aware
  grouping when enough speakers exist.
- **Token-tag review CLI** — `scripts/review_annotations.py` lets a reviewer
  approve or edit per-token `hil` / `tl` / `en` labels in terminal.
- **Reproducible capture pipeline** — `scripts/build_codeswitch_set.py` emits the
  annotation stubs from an elicitation set; `scripts/record.py` captures audio
  and writes the matching annotation. See `docs/recording_kit.md`.
- **Labeled test-set schema** (`SCHEMA.md`), transcription rules
  (`docs/transcription_guidelines.md`), Hugging Face dataset card
  (`hf_dataset/README.md`), and licensing (`docs/licensing.md`, `LICENSE`).

```bash
# judge-facing release pipeline
python3 scripts/build_release.py --overwrite

# build / refresh the code-switch annotation stubs
python3 scripts/build_codeswitch_set.py

# validate the labeled clips
python3 scripts/validate.py --kind asr --dir data/annotations

# capture audio for one prompt
python3 scripts/record.py --list
python3 scripts/record.py --prompt 1 --seconds 8

# run a Whisper baseline and score switch-region WER
python3 scripts/run_whisper.py --model large-v3 --language tl
python3 score.py --ref data/annotations --hyp data/predictions

# optional: refresh Whisper predictions locally (requires openai-whisper)
python3 scripts/benchmark_asr.py --model small --language tl

# build a redistributable metadata + benchmark package only
python3 scripts/package_dataset.py --output release --overwrite

# build deterministic train/validation/test split CSVs
python3 scripts/split_dataset.py --output-dir release/dataset

# review token language tags
python3 scripts/review_annotations.py --summary
python3 scripts/review_annotations.py --only hil_cs_001

# run dataset integrity tests
python3 -m unittest discover -s tests
```

Per-word language tags for the headline `hil_cs_001..040` benchmark are
reviewed. New extension clips must go through the same review step before they
are treated as gold. Audio is recorded by contributors (see the recording kit)
— the repo does not redistribute third-party speech under CC BY 4.0. The bundled
ASR predictions are baseline outputs for reproducibility, not final
model-quality claims.

Sugidanon's strongest distinction is not generic data cleanup. It measures
failure at Hiligaynon/Tagalog/English switch points and connects that speech
benchmark to Hiligaynon translation and live demos.

## Next.js / Vercel app

The hosted demo is a Next.js app with a serverless dictionary-baseline API route.

```bash
npm install
npm run dev
```

Then open `http://localhost:3000`.

Production build:

```bash
npm run build
```

Deploy on Vercel:

1. Import this GitHub repository in Vercel.
2. Keep the framework preset as `Next.js`.
3. Use the default commands from `vercel.json`.
4. Deploy.

The Python app in `app/` remains as a local legacy demo; Vercel serves the
Next.js app from `pages/`.

### Tagalog coverage

The local and hosted demos use layered fallback:

1. exact seed benchmark prompt matches
2. curated phrase matches for common English and Tagalog demo cases
3. local Ollama context-aware translation, when available
4. expanded Tagalog/Hiligaynon dictionary fallback

### Local Ollama context backend

The Next.js API route tries Ollama first when running locally. This is the
context-aware path intended to avoid plain word-by-word translation.

Install or start Ollama, then pull a model:

```bash
ollama serve
ollama pull aya:8b
```

In another terminal:

```bash
OLLAMA_MODEL=aya:8b npm run dev
```

Then open:

```text
http://localhost:3000
```

The API uses this backend order:

```text
seed reference -> curated phrase -> Ollama context LLM -> dictionary fallback
```

Vercel cannot access a local Ollama daemon on your laptop, so the deployed site
uses the fallback layers unless it is connected to a hosted LLM endpoint later.

For future larger coverage, use:

```bash
python3 scripts/build_tl_hil_lexicon.py
```

That script builds a noisy Tagalog -> Hiligaynon bridge lexicon from
Kaikki/Wiktionary machine-readable dictionaries by matching shared English
glosses. Glosbe is documented in `RESOURCES.md` as a direct Tagalog-Hiligaynon
manual reference source.

## Benchmark format

The primary benchmark uses one JSON annotation per clip:

```text
data/annotations/hil_cs_001.json
data/audio/hil_cs_001.wav
data/predictions/hil_cs_001.json
```

Each annotation contains clip metadata, speaker metadata, the reference
transcript, and per-word language tags:

```json
{
  "clip_id": "hil_cs_001",
  "audio_file": "audio/hil_cs_001.wav",
  "transcript": "Nag-grocery ko kahapon kay super traffic.",
  "matrix_language": "hil",
  "switch_type": "HIL+TL+EN",
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

`score.py` aligns each ASR prediction to the reference transcript and attributes
errors to either monolingual Hiligaynon regions or switch regions within one word
of a language change.

## Evaluation

The ASR evaluator reports:

- overall WER
- monolingual-region WER
- switch-region WER
- switch penalty (`switch WER - monolingual WER`)
- switch-region WER by language pair (`hil<->tl`, `hil<->en`, `tl<->en`)
- 95% clip-level bootstrap confidence intervals (`score.py --ci`)

The benchmark is **frozen and content-addressed**: `data/benchmark/MANIFEST.json`
(version 1.0.0) hashes every annotation and audio file and pins the scorer, so
results reproduce exactly or fail loudly:

```bash
python3 scripts/freeze_benchmark.py --verify   # drift gate
python3 score.py --ref data/annotations --hyp data/predictions --ci
```

See **`BENCHMARK.md`** for the full protocol (task, metric, frozen split, cohort
ladder, reproducibility) and `docs/evaluation_report.md` for caveats.

## Extension layers

The repository also contains translation and lexicon tooling in
`data/benchmark/`, `scripts/evaluate_translation.py`, `scripts/translate_hil.py`,
and `pages/api/translate.js`. These support a later speech-to-text ->
translation -> text-to-speech direction, but they are not the main judged
artifact.

The included translation examples are `seed_unverified` starter cases. They
should not be presented as a gold translation dataset until reviewed by native
Hiligaynon speakers.

## Roadmap

### Milestone 1: harden the current benchmark

1. Add more native Hiligaynon speakers.
2. Confirm or correct the per-word language tags.
3. Keep the test set frozen once tags are adjudicated.
4. Compare Whisper small, Whisper large-v3, MMS-style models, and future
   Hiligaynon-tuned ASR models on the same clips.

### Milestone 2: grow the reusable speech resource

1. Add natural conversation, oral tradition, and everyday speaker subsets.
2. Keep scripted, natural, and non-native subsets separate in reporting.
3. Publish expanded dataset cards, model cards, and benchmark reports.
4. Preserve consent, provenance, and withdrawal records for every speaker.

### Milestone 3: connect downstream language tools

1. Use ASR outputs as input to the Hiligaynon translation extension.
2. Evaluate translation quality with human adequacy, fluency, context, and
   terminology ratings.
3. Add TTS only after transcription and translation quality are measurable.

## Speech tooling

Active speech components (see the code-switch ASR benchmark section above):

- `scripts/build_release.py` - judge-facing validation, scoring, web-data, and
  release-package pipeline
- `score.py` — code-switch switch-region WER
- `scripts/build_codeswitch_set.py` — emit code-switch annotation stubs
- `scripts/record.py` — capture audio + matching annotation
- `scripts/run_whisper.py` — Whisper ASR baseline
- `scripts/eval_asr_baselines.py` — one-command WER over baseline predictions
- `scripts/analyze_asr_breakdowns.py` — speaker/domain/switch-type/token-language
  benchmark breakdowns
- `scripts/validate_non_native_eval.py` — readiness check for the 20-line
  non-native robustness scaffold
- `data/annotations/` — the code-switch-labeled corpus

Reserved for the later TTS / speech-to-speech phase:

- `scripts/tts_route.py`
- `g2p_hil/`

## Hackathon pitch

See `docs/project_case_fit.md` for the judge-facing fit summary and
`docs/submission_narrative.md` for the concise project narrative.

## AI disclosure

Members of **Team Hague** used AI tools during ACM TechSprint Asteria,
including **ChatGPT**, **Codex**, and **Claude**.

These tools assisted with:

- project scoping and narrowing the MVP to a focused Hiligaynon code-switch ASR
  benchmark
- drafting and revising documentation
- generating and editing code for the demo app, evaluation scripts, and helper
  scripts
- improving README structure and submission narrative
- debugging local and Vercel deployment issues
- suggesting benchmark categories, schema fields, and evaluation workflow

All project claims, code, dataset entries, and Hiligaynon/Tagalog language
content remain the responsibility of Team Hague. Hiligaynon translations and ASR
labels must be reviewed by qualified human speakers before being treated as
gold data.

AI-generated content was not treated as authoritative linguistic ground truth.
The current seed translations, phrase examples, and per-word ASR language tags
are marked as requiring future human review where appropriate.

## Data protection, privacy & ethics

This project handles human voice recordings, which are personal data. We treat
them accordingly.

- **Informed consent.** Audio is collected only from speakers who agreed to have
  their voice recorded, published as an open dataset under CC BY 4.0, and reused
  for speech-technology research. Consent is obtained before recording.
- **Minimal personal data.** Clips contain elicited, scripted sentences — not
  private conversations. Speakers are identified only by a coarse, anonymized id
  (e.g. `spk01`) plus optional non-identifying metadata (region, age band,
  gender, Hiligaynon fluency). We do **not** publish contact details, exact
  location, or other directly identifying information in the dataset files.
  A speaker's name appears only as voluntary credit in `Acknowledgments`.
- **No sensitive content.** The elicitation scripts avoid real health records,
  financial details, or other sensitive personal information about real people.
  Speakers are asked to remove a recording if they accidentally include anything
  private.
- **Right to withdraw.** A contributing speaker may request removal of their
  clips at any time; we will delete the affected audio and annotations from the
  repository and the published dataset and note the change.
- **Provenance & licensing.** Third-party audio or text is never relicensed.
  Source and license are recorded per item (see `docs/licensing.md`,
  `RESOURCES.md`); external corpora stay under their own terms and are
  git-ignored, not redistributed.
- **Honest labeling.** Speaker fluency is recorded (`native` / `fluent` /
  `non_native`); non-native clips are flagged and must not be presented as
  native gold data. New AI-assisted labels are marked `seed_unverified` until a
  human reviews them; the current headline ASR token tags are reviewed.
- **Intended use.** A research and evaluation building block for inclusive
  Philippine speech technology. It must not be used to identify, profile,
  surveil, or impersonate the speakers, or to build voice-cloning systems
  without the speakers' separate, explicit consent.
- **Security.** Access tokens and credentials are never committed; secrets are
  kept out of the repository (`.gitignore`), and any exposed token is rotated.

If you reuse this dataset, keep these protections: preserve attribution, honor
withdrawal requests forwarded to us, and do not attempt to re-identify speakers.

## License

Data under **CC BY 4.0**, code under **MIT**. See `LICENSE`.
