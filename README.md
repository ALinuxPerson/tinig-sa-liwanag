# Team Hague — Sugidanon

[![Benchmark integrity](https://github.com/Jazztinn/tinig-sa-liwanag/actions/workflows/benchmark.yml/badge.svg)](https://github.com/Jazztinn/tinig-sa-liwanag/actions/workflows/benchmark.yml)

**ACM TechSprint Asteria Submission**  
**Event dates:** June 25-27, 2026

> *Measuring what gets erased. Sugidanon is an open code-switch ASR benchmark for Hiligaynon, the language of 9M+ Filipinos that speech AI has never learned to hear.*

**Live demo:**

```text
https://tinig-sa-liwanag.vercel.app
```

**Open dataset — built by Team Hague (Hugging Face):**

[![Dataset on HuggingFace](https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-blue)](https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch)

```text
https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch
```

A dataset we built from scratch, 40 native-recorded code-switch Hiligaynon/Tagalog/English clips with per-word language tags, switch-region WER scoring, and a second 40-clip speaker extension. Recorded and reviewed by native Ilonggo speakers. CC BY 4.0.

**Reproduce the benchmark (one-click Google Colab):**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb)

Downloads the dataset, runs the ASR baseline, and prints the switch penalty on a fresh machine. No local setup.

**ASR baselines:**

```text
OpenAI Whisper:  https://github.com/openai/whisper
Meta MMS:        https://huggingface.co/facebook/mms-1b-all
```

## Team members

| Member | Primary role |
|--------|--------------|
| Legaspi, Jazztinn Kyle | Lead / pipeline, evaluation scripts, demo app |
| Michael C. Baterna | Benchmark data, schema, domain examples |
| Arwin Jeremy Bumpus | Frontend / demo UI, documentation |
| De Guzman, Nimeesha | Lexicon, Tagalog/Hiligaynon bridge, review coordination |

## Acknowledgments

**Aziel Faith Agustin** — Hiligaynon (Ilonggo) speaker who reviewed the elicitation sentences and recorded all 80+ clips. The dataset's reference transcripts and audio exist thanks to their voice and review.

---

## ✦ Why this matters

> **The Philippines has 130+ languages. Most are invisible to modern speech technology.**

Hiligaynon (Ilonggo) — spoken by **9M+ people** across Iloilo, Negros, Guimaras, and Panay, and carrier of a deep oral tradition (the *sugidanon* epic chants this project is named for), is one of them. Off-the-shelf speech models are rarely even *measured* on Ilonggo, so no one had quantified where they fail.

**Sugidanon makes that failure measurable.** Its core contribution is **switch-region WORD ERROR RATE**: instead of one blunt error rate, it separates errors on borrowed English/Tagalog words from errors on the Hiligaynon matrix language. The finding is sharp and reproducible — current models transcribe the borrowed words well but miss the Hiligaynon itself, a **negative switch penalty (−30.1%)** that puts a number on exactly what gets erased.

Measurement is the first act of inclusion:

- **Overall WER hides which language failed; switch-region WER exposes it.**
- An open, per-word-tagged corpus recorded and reviewed by native Ilonggo speakers turns heritage speech — including an `oral_tradition` domain — into reusable data, **owned by the community (CC BY 4.0), not extracted from it.**
- A reproducible benchmark makes the gap fundable and fixable, and the same clips and tags can later seed STT/TTS and speech-to-speech evaluation.

> Rather than a finished consumer product, Sugidanon is a **building block** — a measuring stick and an open corpus that future developers and researchers can extend into inclusive speech systems, so every Filipino voice gets a seat at the table before it disappears.

## UN Sustainable Development Goals

Sugidanon directly supports:

<a href="https://sdgs.un.org/goals/goal4"><img src="https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-04.jpg" alt="SDG 4 — Quality Education" width="160"/></a>
<a href="https://sdgs.un.org/goals/goal9"><img src="https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-09.jpg" alt="SDG 9 — Industry, Innovation & Infrastructure" width="160"/></a>
<a href="https://sdgs.un.org/goals/goal10"><img src="https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-10.jpg" alt="SDG 10 — Reduced Inequalities" width="160"/></a>
<a href="https://sdgs.un.org/goals/goal17"><img src="https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-17.jpg" alt="SDG 17 — Partnerships for the Goals" width="160"/></a>

## Headline results

Whisper small, `--language tl`, **1 speaker / 40 clips**:

| Metric | Value |
|--------|------:|
| Overall WER | 57.4% |
| Switch-region WER | 35.8% |
| Monolingual WER | 65.9% |
| Switch penalty | −30.1% |

```text
Current multilingual models recognize borrowed English and Tagalog words,
but fail on the Hiligaynon matrix language.
```

*N is intentionally small (40 clips, 1 headline speaker, 165 switch tokens / 208 mono tokens). Results are reproducible and directionally consistent with the spk02 extension (switch penalty −10.2% over 40 clips), but should be interpreted as early-benchmark estimates, not large-sample statistics.*

## Technologies used

- **Python 3** — stdlib only for core benchmark tooling (no install needed)
- **Next.js / React** + **Vercel** — hosted benchmark explorer and demo
- **OpenAI Whisper** and **Meta MMS** — ASR baselines
- **Hugging Face `transformers` + `torch`** — optional neural extension work
- **ffmpeg** — optional audio conversion

## Repository structure

```text
sugidanon/
├── score.py                         # switch-region ASR WER scorer (--ci for bootstrap CIs)
├── BENCHMARK.md                     # benchmark card: protocol, cohorts, reproducibility
├── SCHEMA.md                        # annotation + subset schema
├── data/benchmark/MANIFEST.json     # frozen, content-addressed benchmark version
├── scripts/
│   ├── freeze_benchmark.py          # write/verify the frozen MANIFEST (drift gate)
│   ├── build_release.py             # validation + scoring + web data + release package
│   ├── build_benchmark_web.py       # emits public/benchmark.json for the explorer
│   ├── validate.py                  # validates ASR benchmark or translation files
│   ├── review_annotations.py        # terminal language-tag review CLI
│   ├── run_whisper.py               # Whisper ASR baseline runner
│   ├── analyze_asr_breakdowns.py    # speaker/domain/switch-type/pair breakdowns
│   └── package_dataset.py           # release package builder
├── data/
│   ├── annotations/                 # primary ASR annotations (hil_cs_001..040)
│   ├── audio/                       # native-recorded Hiligaynon clips
│   ├── predictions/                 # ASR JSON predictions (forced-tl baseline)
│   └── extensions/                  # spk02 extension + non_native_eval scaffold
├── pages/
│   ├── index.js                     # live benchmark explorer
│   └── api/translate.js             # optional translation extension API
├── hf_dataset/README.md             # Hugging Face dataset card
├── docs/                            # evaluation report, licensing, transcription guidelines
└── results/
    ├── asr_score.txt                # canonical headline numbers
    └── asr_baselines.md             # multi-model baseline comparison
```

## Core pipeline

```text
 elicit / record     →   annotate          →   native review    →   FREEZE
 (record.py)             tokens + hil/tl/en    (review_annotations)  MANIFEST.json
                          (build_codeswitch_set)                      (sha256 + scorer pin)
                                                                            │
                                                                            ▼
 ASR baseline        →   predictions/      →   score.py         →   breakdowns + CIs
 (run_whisper.py)        {clip_id, text}       switch-region WER    (analyze_asr_breakdowns)
                                               + bootstrap CI              │
                                                                            ▼
                                                  web explorer  ·  release package
                                               (build_benchmark_web)  (build_release)
```

| Stage | Script | Output |
|-------|--------|--------|
| Annotate | `build_codeswitch_set.py`, `record.py` | `data/annotations`, `data/audio` |
| Review | `review_annotations.py` | reviewed per-word `lang` tags |
| Freeze | `freeze_benchmark.py` | `data/benchmark/MANIFEST.json` (drift gate) |
| Baseline | `run_whisper.py` | `data/predictions` |
| Score | `score.py --ci` | switch-region WER + 95% CIs |
| Slice | `analyze_asr_breakdowns.py` | speaker/domain/switch/pair breakdowns |
| Ship | `build_benchmark_web.py`, `build_release.py` | web JSON, release package |

## Quick start

No installs required for the core benchmark tooling.

```bash
# full release pipeline — validate, score, refresh web data, package
python3 scripts/build_release.py --overwrite

# minimal proof
python3 scripts/validate.py --kind asr --dir data/annotations
python3 score.py --ref data/annotations --hyp data/predictions
python3 scripts/freeze_benchmark.py --verify   # drift gate

# run tests
python3 -m unittest discover -s tests

# run the web app
npm install && npm run dev   # http://localhost:3000
```

## Benchmark format

One JSON annotation per clip:

```json
{
  "clip_id": "hil_cs_001",
  "audio_file": "audio/hil_cs_001.wav",
  "transcript": "Nag-grocery ko kahapon kay super traffic.",
  "matrix_language": "hil",
  "switch_type": "HIL+TL+EN",
  "tokens": [
    { "idx": 0, "text": "Nag-grocery", "lang": "hil" },
    { "idx": 1, "text": "ko",          "lang": "hil" },
    { "idx": 2, "text": "kahapon",     "lang": "hil" },
    { "idx": 3, "text": "kay",         "lang": "hil" },
    { "idx": 4, "text": "super",       "lang": "tl"  },
    { "idx": 5, "text": "traffic",     "lang": "en"  }
  ]
}
```

`score.py` aligns each ASR prediction to the reference and attributes errors to either monolingual Hiligaynon regions or switch regions within one word of a language change.

## Evaluation

- overall WER
- monolingual-region WER
- switch-region WER
- switch penalty (`switch WER − monolingual WER`)
- switch-region WER by language pair (`hil↔tl`, `hil↔en`, `tl↔en`)
- 95% clip-level bootstrap confidence intervals (`score.py --ci`)

The benchmark is **frozen and content-addressed**: `data/benchmark/MANIFEST.json` (v1.0.1) hashes every annotation and audio file and pins the scorer, so results reproduce exactly or fail loudly. See `BENCHMARK.md` for the full protocol and `docs/evaluation_report.md` for caveats.

## Extension layers

Translation and lexicon tooling (`scripts/evaluate_translation.py`, `scripts/translate_hil.py`, `pages/api/translate.js`) support a later STT → translation → TTS direction but are not the primary judged artifact. Translation examples are `seed_unverified` until reviewed by native Hiligaynon speakers.

## Roadmap

### Milestone 1 — harden the benchmark

1. Add more native Hiligaynon speakers.
2. Confirm or correct per-word language tags via multi-reviewer adjudication.
3. Compare Whisper large-v3, MMS, and future Hiligaynon-tuned ASR models.

### Milestone 2 — grow the resource

1. Add natural conversation, oral tradition, and everyday speaker subsets.
2. Keep scripted, natural, and non-native subsets separate in reporting.
3. Publish expanded dataset cards, model cards, and benchmark reports.

### Milestone 3 — connect downstream tools

1. Use ASR outputs as input to the Hiligaynon translation extension.
2. Add TTS only after transcription and translation quality are measurable.

### Scalability

Sugidanon is architected to scale without breaking its reproducibility guarantees.

| Scale target | Mechanism |
|---|---|
| More speakers | New `spk_id` entries; speaker-disjoint cohorts enforced by schema |
| More languages | New `lang` values (`ceb`, `war`, `ilo`, …); scorer already parameterized |
| More clips | Add JSON + WAV; `freeze_benchmark.py` re-hashes; CI gate verifies |
| Any ASR model | `score.py` accepts any `{clip_id, text}` output — swap and re-run |
| Community contributions | `CONTRIBUTING.md` protocol + freeze gate prevent drift |
| Larger datasets | Same pipeline publishes to HF Datasets for streaming; no database needed |

A university lab, NGO, or government digitization project can fork the repo, record their own speakers, and produce a directly comparable score using the same scorer and schema.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to add clips, run the review CLI, and pass the freeze gate before merging.

## AI disclosure

Team Hague used AI tools (ChatGPT, Codex, Claude) during ACM TechSprint Asteria for project scoping, documentation drafting, code generation, and debugging. All project claims, dataset entries, and language content remain the responsibility of Team Hague. AI output was never treated as authoritative language ground truth; Hiligaynon labels are marked `seed_unverified` until reviewed by a qualified human speaker.

## Data protection, privacy & ethics

- **Informed consent** — audio collected only from speakers who agreed to CC BY 4.0 publication.
- **Minimal data** — speakers identified only by anonymized id (`spk01`); no contact details or exact location published.
- **Right to withdraw** — any speaker may request removal of their clips at any time.
- **Honest labeling** — non-native clips are flagged; AI-assisted labels marked `seed_unverified` until human-reviewed.
- **Intended use** — research and evaluation only. Must not be used to identify, profile, surveil, or impersonate speakers, or to build voice-cloning systems without separate explicit consent.
- **Provenance** — source and license recorded per item in `docs/source_ledger.md`; external corpora stay under their own terms.

## License

Data under **CC BY 4.0**, code under **MIT**. See `LICENSE`.
