# 🇵🇭 Sugidanon — A Code-Switched Hiligaynon Speech Benchmark

**An open benchmark + tooling for code-switched Hiligaynon–Tagalog–English
speech recognition, with a scoped Hiligaynon text-to-speech proof-of-concept.**

*Sugidanon* is the Ilonggo word for the epic oral traditions of Panay — fitting
for a project about preserving and recognizing how Ilonggos actually speak: a
natural mix of Hiligaynon, Tagalog, and English
(*"Nag-grocery ko kahapon kay wala sang ulutanon, tapos super traffic."*).

Most ASR systems are tested only on "clean" monolingual speech, so nobody knows
how badly they break at **language switch points**. Sugidanon measures exactly
that — and adds a TTS path that pronounces each language correctly.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb)

**Run it in your browser:** the Colab notebook clones this repo and runs the full
benchmark + TTS demo with zero local setup (core cells need no installs).

> **Track:** Inclusive Speech Technology for Philippine Languages (FTIC / GitHub).
> Deliverable is a *reusable open resource* — a labeled test set, a scoring
> harness, and a pipeline — **not an application.**

## Why this matters

- The Philippines has 130+ languages; everyday speech is heavily code-switched —
  yet there is **almost no open benchmark** measuring ASR *at the switch points*,
  where systems fail most.
- Hiligaynon (~9M speakers) is underserved by speech tech. Tagalog is spreading
  into the Visayas, so **hil↔tl mixing is a live, growing phenomenon**. Because
  `hil` and `tl` share vocabulary, clean labels are hard — that difficulty is our
  contribution's value.
- We ship **foundational infrastructure**: a labeled gold test set, a documented
  annotation schema, a scoring script, and a TTS routing PoC. Future teams plug
  in any model and instantly see its switch-point WER.

## Languages & tags

| Tag     | Language               |
|---------|------------------------|
| `hil`   | Hiligaynon (Ilonggo)   |
| `tl`    | Tagalog / Filipino     |
| `en`    | English                |
| `other` | proper nouns, ambiguous, or another PH language |

Clip IDs are prefixed by the dominant pair: `hil_en_001`, `hil_tl_001`, `tl_en_001`.

## Repository structure

```
tinig-sa-liwanag/                # repo (project name: Sugidanon)
├── README.md              # this file
├── SCHEMA.md              # annotation format + hil/tl tagging rules
├── RESOURCES.md           # external datasets + models we build on
├── AI_DISCLOSURE.md       # how AI assistants were used
├── LICENSE                # CC BY 4.0 (data) + MIT (code)
├── requirements.txt       # optional tooling deps (scorer needs none)
├── score.py               # scoring harness, pure stdlib
├── g2p_hil/               # Hiligaynon grapheme→phoneme rules (TTS path)
│   └── g2p.py
├── scripts/
│   ├── convert_audio.sh   # normalize recordings → 16 kHz mono wav
│   ├── run_whisper.py     # baseline: audio → predictions (whisper optional)
│   ├── validate.py        # check annotations conform to SCHEMA.md
│   ├── tts_route.py       # per-word language router for code-switched TTS
│   └── roundtrip_wer.py   # TTS quality via TTS→STT→WER
├── data/
│   ├── audio/             # <clip_id>.wav (16 kHz mono)
│   ├── annotations/       # gold transcripts w/ per-word language tags
│   ├── predictions/       # model hypotheses to be scored
│   └── tts_samples.txt    # code-switched sentences for the TTS PoC
└── results/
    └── baseline.md        # baseline score table
```

## The metric

Headline number is the **switch penalty**: how much worse a model does on words
near a language switch vs monolingual words.

- **Overall WER** — across all words.
- **Switch-region WER** — words within ±1 token of a language switch.
- **Monolingual WER** — all other words.
- **Switch penalty** = Switch-region WER − Monolingual WER.

`score.py` also breaks the switch-region WER down **per language pair**
(hil↔tl, hil↔en, tl↔en), so you can see which kind of switch hurts most.

## Quick start (no installs needed)

```bash
# validate annotations (skip audio-file check for the worked example)
python scripts/validate.py --no-audio-check

# score the included worked example
python score.py --ref data/annotations --hyp data/predictions
```

To benchmark a real model: record clips → `scripts/convert_audio.sh` → annotate
into `data/annotations/` → `python scripts/run_whisper.py` → `score.py`.

## TTS proof-of-concept

We do **not** train a voice from scratch. Instead we route each word by language
and pronounce it correctly:

```bash
# show routing + Hiligaynon phonemes for a sentence (no model needed)
python scripts/tts_route.py "Nag-grocery ko kahapon kay super traffic"

# Hiligaynon G2P smoke test
python g2p_hil/g2p.py "Maayong aga sa imo"
```

- `g2p_hil/` — Hiligaynon grapheme→phoneme rules (the novel linguistic piece).
- `scripts/tts_route.py` — sends hil/tl words down the Hiligaynon G2P path, en
  words down an English TTS path. Backend (e.g. F5-TTS / VITS Hiligaynon from
  `RESOURCES.md`) is optional and import-guarded.
- **TTS metric:** round-trip WER (`scripts/roundtrip_wer.py`) — synthesize, run
  back through STT, measure error — plus a quick human naturalness rating.

## Setup

Core scorer is **dependency-free** (Python 3.8+ stdlib). Optional tooling:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # openai-whisper, jiwer, TTS
# also needs system ffmpeg for scripts/convert_audio.sh
```

See `RESOURCES.md` for the Hiligaynon datasets and models we build on.

## How we build it (the 1-day plan)

1. **Schema first** (linguists) — tag set + hil/tl rules in `SCHEMA.md`.
2. **Record** 40–60 short hil-tl-en clips, 4–10 s, 3+ Ilonggo speakers.
3. **Transcribe + tag** each clip at the word level into `data/annotations/`.
4. **Double-annotate** ≥10 clips; report inter-annotator agreement.
5. **Baseline** — run Whisper to fill `data/predictions/`; first numbers via
   `score.py` into `results/baseline.md`.
6. **TTS PoC** — ~10 sentences through `tts_route.py`; report round-trip WER.

## Roadmap (future work)

- Demo app: record → STT → color-tagged transcript → native-speaker correct →
  approve & archive (grows the open dataset).
- LoRA fine-tune Whisper on Hiligaynon audio; trained Hiligaynon voice.
- More pairs (Waray-English, Ilocano-English); public-model leaderboard.

## License

Data under **CC BY 4.0**, code under **MIT**. See `LICENSE`.

## AI usage

AI assistants helped scaffold and document this repo. All recordings and
linguistic labels are human-made. See `AI_DISCLOSURE.md`.
