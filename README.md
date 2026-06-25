# Team Hague

**ACM TechSprint Asteria Submission**  
**Event dates:** June 25-27, 2026

**Live demos:**

```text
https://tinig-sa-liwanag.vercel.app   # Sugidanon — project site & docs (translation demo at /demo)
https://tinig-one.vercel.app          # Companion Demo: Tinig — AI assistant using Sugidanon's resources
Tinig (companion demo repository): https://github.com/ALinuxPerson/tinig
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
language tags and switch-region WER scoring. CC BY 4.0.

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

## Members

- **Legaspi, Jazztinn Kyle**
- **Michael C. Baterna**
- **Arwin Jeremy Bumpus**
- **De Guzman, Nimeesha**

## Acknowledgments

- **Aziel Faith Agustin** — Hiligaynon (Ilonggo) speaker who reviewed the elicitation
  sentences and recorded all 40 clips in the speech corpus. The dataset's
  reference transcripts and audio exist thanks to their voice and review.

## Team roles and rules

| Member | Primary role |
|--------|--------------|
| Legaspi, Jazztinn Kyle | Lead / pipeline, evaluation scripts, demo app |
| Michael C. Baterna | Benchmark data, schema, domain examples |
| Arwin Jeremy Bumpus | Frontend / demo UI, documentation |
| De Guzman, Nimeesha | Lexicon, Tagalog/Hiligaynon bridge, review coordination |

Working rules:

- Hiligaynon references stay `seed_unverified` until a qualified speaker reviews them.
- AI output is never treated as authoritative language ground truth.
- Every commit keeps the core benchmark tooling dependency-free (stdlib).
- Source provenance and license are recorded for any third-party data.
- Decisions and scope changes are agreed by the team before merging to `main`.

# Sugidanon

**A context-aware Hiligaynon text translation benchmark, baseline, and demo
pipeline.**

This repository is now scoped around one first question:

> Can a system translate meaning into Hiligaynon accurately in context, instead
> of only replacing the words it already knows?

The current first milestone is not a full STT/TTS system. It is an open,
reusable text translation resource that future teams can extend into speech:
STT -> translation, translation -> TTS, and speech-to-speech translation.

## Current deliverable

The repository targets the **Inclusive Speech Technology for Philippine
Languages** challenge by shipping foundational infrastructure:

- a Hiligaynon translation benchmark with domain and context labels
- an annotation schema for reviewed translation examples
- a baseline translation runner
- an evaluation script for automatic metrics
- a small local demo app
- documentation for future STT/TTS extensions

The primary task for v1 is:

```text
English / Filipino / code-switched text -> Hiligaynon text
```

Live demos are linked at the top of this README.

## Features

- **Context-aware translation benchmark** — JSONL examples labeled with domain,
  context notes, linguistic phenomena, difficulty, and review status.
- **Annotation schema** (`SCHEMA.md`) for reviewed Hiligaynon translation examples.
- **Baseline translation runner** — dictionary backend (offline, zero deps) plus
  an optional Hugging Face neural backend.
- **Automatic evaluator** — coverage, exact match, token F1, chrF, per-domain
  summaries.
- **Two demo apps** — a stdlib local Python app (`app/`) and a Next.js/Vercel app
  (`pages/`), both with layered phrase + dictionary fallback.
- **Tinig — AI assistant demo** — a multilingual (Hiligaynon / Tagalog / English)
  assistant built on the translation layer, with an on-page context section to
  ground the conversation.
- **Lexicon tooling** — curated `data/lexicon_hil.tsv`, plus builders that mine
  Kaikki/Wiktionary for en→hil and Tagalog→Hiligaynon bridge entries.
- **Sample prompts** across health, education, emergency, public service, daily
  life, and code-switching for quick demoing.
- **Future-ready speech utilities** — code-switched ASR scorer, Whisper runner,
  Hiligaynon G2P, and TTS routing kept for the later STT/TTS phase.

## Why this matters

Despite the Philippines being home to more than 130 languages, most regional
languages remain underrepresented in open speech and language technology. While
Tagalog speech recognition has seen significant progress, many languages such
as Cebuano, Ilocano, Hiligaynon, and Waray still lack the open datasets,
benchmarks, and models needed to develop inclusive AI systems. This gap limits
the accessibility of voice-driven technologies for millions of Filipinos.

Hiligaynon is spoken by millions of Filipinos, but open translation and speech
resources remain limited. A speech system is only useful if the language layer
understands meaning, context, and local usage. This project therefore starts
with text translation before audio:

- Word-by-word lookup is not enough for useful translation.
- A benchmark makes failures visible and reproducible.
- Human-reviewed Hiligaynon references become reusable data.
- The same examples can later seed STT/TTS and speech-to-speech evaluation.

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
- Use text translation as the foundation for later speech workflows.
- Make limitations explicit: current seed translations still need
  native-speaker review.

## What we developed

During the hackathon, we narrowed the original STT/TTS idea into a realistic
MVP: a context-aware Hiligaynon translation benchmark scaffold and demo.

We developed:

- a 30-row seed benchmark for English, Filipino, and code-switched input into
  Hiligaynon
- a Hugging Face-style dataset card for the labeled ASR test set
- a JSONL schema for source text, context notes, reference translation,
  phenomena labels, difficulty, and review status
- a baseline prediction generator
- an automatic evaluator with coverage, exact match, token F1, chrF, and
  per-domain summaries
- a one-command ASR baseline evaluator for Whisper/MMS-format predictions
- transcription guidelines and clear dataset/code licensing notes
- a Next.js/Vercel demo with phrase matching and dictionary fallback
- a Tagalog-to-Hiligaynon phrase layer for common demo cases
- a script for building a larger noisy Tagalog -> Hiligaynon bridge lexicon from
  Kaikki/Wiktionary dictionaries
- documentation for future native-speaker review, neural baselines, and STT/TTS
  extension

This is not yet a gold translation dataset or a production translation model.
It is the scaffold that makes that next step reproducible.

## MVP

The MVP is:

> A reproducible context-aware Hiligaynon translation benchmark scaffold with a
> baseline web demo.

The MVP demonstrates:

- how benchmark examples are represented
- how baseline predictions are generated
- how translation outputs are evaluated
- where dictionary and phrase-based translation fail
- how future Hiligaynon reviewers can validate or correct the seed data

For demo quality, the deployed app uses three layers:

1. exact seed benchmark prompt matches
2. curated phrase matches for common English and Tagalog demo cases
3. expanded dictionary fallback for remaining text

The phrase and dictionary layers improve presentation, but the research artifact
remains the benchmark/evaluation pipeline.

### Tinig — the AI assistant demo

The MVP also includes a working demo app named **Tinig**: an AI assistant built
on top of Sugidanon that can converse in **Hiligaynon, Tagalog, and
English** (including code-switched input).

How it works:

- The user opens Tinig and is shown a **context section** — plain-language
  background the user can understand — so the conversation has grounding instead
  of starting cold.
- The user types or speaks in any mix of Hiligaynon, Tagalog, and English.
- Tinig replies using the translation layer, so responses come back in
  Hiligaynon (or the user's chosen language), demonstrating the project's core
  capability in a real assistant flow.

Tinig is the user-facing proof that the benchmark and translation pipeline are
useful in practice: the same Hiligaynon language layer that the benchmark
measures is what powers the assistant's understanding and replies. The benchmark
remains the research artifact; Tinig shows what it enables.

## Technologies Used

- **Python 3** (stdlib only for the core benchmark tooling — no install needed)
- **Next.js / React** + **Vercel** for the hosted demo and serverless API route
- **Node.js / npm** for the web app build
- **Hugging Face `transformers` + `torch`** (optional neural translation backend)
- **Ollama** (optional local context-aware LLM, e.g. `aya:8b`)
- **Kaikki.org / Wiktextract** machine-readable dictionaries for lexicon building
- Evaluation: custom token F1 + chrF-style metrics (pure Python)
- Future speech phase: **OpenAI Whisper**, **Meta MMS**, F5-TTS/VITS Hiligaynon,
  `ffmpeg`

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
│   ├── index.js                     # hosted demo UI
│   └── api/translate.js             # serverless translation baseline API
├── styles/
│   └── globals.css
├── score.py                         # legacy ASR switch-point scorer
├── scripts/
│   ├── evaluate_translation.py       # primary v1 evaluator
│   ├── generate_baseline_predictions.py
│   ├── build_tl_hil_lexicon.py       # Kaikki/Wiktionary bridge lexicon builder
│   ├── translate_hil.py              # dictionary or HF translation backend
│   ├── validate.py                   # validates translation benchmark or ASR files
│   ├── benchmark_asr.py              # one-command ASR validation + scoring
│   ├── package_dataset.py            # release package builder
│   ├── split_dataset.py              # deterministic split CSV builder
│   ├── review_annotations.py         # terminal language-tag review
│   └── ...                           # future speech/G2P utilities
├── data/
│   ├── benchmark/
│   │   └── hil_translation_v1.jsonl  # primary v1 benchmark
│   ├── predictions/
│   │   └── translation_baseline_dict.jsonl
│   ├── annotations/                  # legacy/future ASR annotations
│   └── lexicon_hil.tsv               # curated dictionary entries
├── app/
│   ├── server.py
│   └── index.html                    # legacy local Python demo
├── docs/
│   ├── evaluation_report.md
│   ├── licensing.md
│   ├── submission_narrative.md
│   └── transcription_guidelines.md
└── results/
    ├── asr_baselines.md
    ├── asr_score.txt
    └── baseline.md
```

## Quick start

No installs are required for the core benchmark tooling.

```bash
# validate the translation benchmark
python3 scripts/validate.py --kind translation --dir data/benchmark

# regenerate the dictionary baseline predictions
python3 scripts/generate_baseline_predictions.py

# evaluate the included dictionary baseline
python3 scripts/evaluate_translation.py \
  --refs data/benchmark/hil_translation_v1.jsonl \
  --preds data/predictions/translation_baseline_dict.jsonl

# run the local demo app
python3 app/server.py
```

Then open `http://localhost:8000`.

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
  `HIL+TL`, `HIL+TL+EN`). Reference text is `reviewed`; per-word `hil`/`tl`/`en`
  tags are auto-seeded (`lang_tags_status: seed_unverified`) for the speaker to
  confirm.
- **`score.py`** — switch-region WER, monolingual WER, switch penalty, and a
  per-language-pair breakdown (`hil<->tl`, `hil<->en`, `tl<->en`).
- **One-command ASR benchmark** — `scripts/benchmark_asr.py` validates, screens
  edge cuts, refreshes Whisper predictions, scores switch-region WER, and can
  build a release package.
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
# build / refresh the code-switch annotation stubs
python3 scripts/build_codeswitch_set.py

# validate the labeled clips (drop --no-audio-check once wavs exist)
python3 scripts/validate.py --kind asr --dir data/annotations --no-audio-check

# capture audio for one prompt
python3 scripts/record.py --list
python3 scripts/record.py --prompt 1 --seconds 8

# run a Whisper baseline and score switch-region WER
python3 scripts/run_whisper.py --model large-v3 --language tl
python3 score.py --ref data/annotations --hyp data/predictions

# one-command local benchmark pipeline
python3 scripts/benchmark_asr.py --model small --language tl

# build a redistributable metadata + benchmark package
python3 scripts/benchmark_asr.py --skip-whisper --package

# build deterministic train/validation/test split CSVs
python3 scripts/split_dataset.py --output-dir release/dataset

# review token language tags
python3 scripts/review_annotations.py --summary
python3 scripts/review_annotations.py --only hil_cs_001

# run dataset integrity tests
python3 -m unittest discover -s tests
```

Per-word language tags are `seed_unverified`: a qualified Hiligaynon speaker must
review them before the clips are treated as gold. Audio is recorded by
contributors (see the recording kit) — the repo does not redistribute
third-party speech under CC BY 4.0. The bundled ASR predictions are baseline
outputs for reproducibility, not final model-quality claims.

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

The current hackathon scaffold contains 30 seed examples in:

```text
data/benchmark/hil_translation_v1.jsonl
```

All current examples are `seed_unverified` until a Hiligaynon speaker reviews
the reference translations.

Each row in `data/benchmark/hil_translation_v1.jsonl` is one translation case:

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

`seed_unverified` means the example is a starter case that still needs native
speaker review before it can be treated as gold data.

## Evaluation

The v1 evaluator reports:

- coverage: how many benchmark IDs have predictions
- exact match after normalization
- token F1
- chrF-style character n-gram F-score
- per-domain metric averages

See `docs/evaluation_report.md` for the current hackathon evaluation notes.

Automatic metrics are only a first pass. The final benchmark should include
human ratings for:

- adequacy: meaning is preserved
- fluency: Hiligaynon sounds natural
- context: ambiguous meaning is resolved correctly
- terminology: domain words are appropriate
- severity: minor issue, major issue, or meaning changed

## Baselines

The included baseline is intentionally simple:

- `dict`: offline dictionary lookup from `scripts/translate_hil.py`
- `hf`: optional Hugging Face model backend when `transformers` and `torch` are installed

The dictionary baseline is useful because it exposes the problem clearly: it can
translate known words, but it cannot reliably handle grammar, context, idioms,
or paragraph-level meaning.

## Proper plan

### Milestone 1: benchmark foundation

1. Freeze the translation schema in `SCHEMA.md`.
2. Write 300-500 English/Filipino/code-switched source examples.
3. Group examples by domain: health, education, public service, daily life,
   emergency, and code-switching.
4. Add context notes and the expected linguistic phenomenon for each example.
5. Have native Hiligaynon speakers produce and review reference translations.

### Milestone 2: baseline and error analysis

1. Run the dictionary baseline and at least one neural baseline.
2. Score every prediction with `scripts/evaluate_translation.py`.
3. Add human ratings for a representative subset.
4. Document common failure modes: literal translation, wrong pronoun, wrong
   tense/aspect, missing implied meaning, and unnatural Hiligaynon.

### Milestone 3: model improvement

1. Split reviewed data into train/dev/test.
2. Fine-tune or adapt an open multilingual model when enough reviewed pairs are
   available.
3. Keep the test set fixed.
4. Publish model cards and dataset cards.

### Milestone 4: demo

1. Keep the demo small: source text in, Hiligaynon text out.
2. Include benchmark examples so judges can test difficult cases quickly.
3. Show whether the backend is dictionary, neural baseline, or fine-tuned model.
4. Avoid claiming production-level translation until human scores support it.

### Milestone 5: speech extension

1. Reuse the text benchmark as the translation component of a speech pipeline.
2. Add STT input once text translation quality is measurable.
3. Add TTS output after translation quality and pronunciation resources are ready.
4. Reuse the existing G2P, ASR, and TTS scripts as future infrastructure.

## Speech tooling

Active speech components (see the code-switch ASR benchmark section above):

- `score.py` — code-switch switch-region WER
- `scripts/build_codeswitch_set.py` — emit code-switch annotation stubs
- `scripts/record.py` — capture audio + matching annotation
- `scripts/run_whisper.py` — Whisper ASR baseline
- `scripts/eval_asr_baselines.py` — one-command WER over baseline predictions
- `data/annotations/` — the code-switch-labeled corpus

Reserved for the later TTS / speech-to-speech phase:

- `scripts/tts_route.py`
- `g2p_hil/`

## Hackathon pitch

See `docs/submission_narrative.md` for a concise project narrative.

## AI disclosure

Members of **Team Hague** used AI tools during ACM TechSprint Asteria,
including **ChatGPT**, **Codex**, and **Claude**.

These tools assisted with:

- project scoping and narrowing the MVP from STT/TTS to a translation-first
  benchmark scaffold
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
The current seed translations, phrase examples, and ASR labels are marked as
requiring future human review where appropriate.

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
  native gold data. AI-assisted labels are marked `seed_unverified` until a
  human reviews them.
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
