# 🇵🇭 Tinig sa Liwanag — CodeSwitch-HIL

**A code-switched Hiligaynon–English–Tagalog speech evaluation benchmark.**

An open benchmark for measuring how well speech-recognition (ASR) systems handle
**code-switched Ilonggo speech** — the natural mix of Hiligaynon, English, and
Tagalog the way people in Western Visayas actually talk
(*"Nag-grocery ko kahapon kay wala sang ulutanon, tapos super traffic."*).

Most ASR systems are tested only on "clean" monolingual speech, so nobody knows
how badly they break at **language switch points**. This benchmark measures
exactly that.

> **Track:** Inclusive Speech Technology for Philippine Languages (FTIC / GitHub).
> Deliverable is a *reusable open resource* — a labeled test set + a scoring
> harness — **not an application.**

## Why this matters

- The Philippines has 130+ languages; everyday speech is heavily code-switched —
  yet there is **almost no open benchmark** that measures ASR performance *at the
  switch points*, which is where systems fail most.
- Hiligaynon (Ilonggo) is spoken by ~9M people and is **underserved** by speech
  tech. Real Ilonggo speech also pulls in Tagalog and English, making it a true
  three-way code-switching case.
- Our contribution is **foundational infrastructure**: a labeled gold test set, a
  documented annotation schema, and a scoring script. Future teams plug in any
  model (Whisper, MMS, Google STT, …) and instantly see its switch-point WER.

## Languages & tags

Word-level language tags used in annotations:

| Tag     | Language               |
|---------|------------------------|
| `hil`   | Hiligaynon (Ilonggo)   |
| `tl`    | Tagalog / Filipino     |
| `en`    | English                |
| `other` | proper nouns, ambiguous, or another PH language |

Clip IDs are prefixed by the dominant pair, e.g. `hil_en_001`, `hil_tl_001`.

## Repository structure

```
tinig-sa-liwanag/
├── README.md              # this file
├── SCHEMA.md              # annotation format + tagging rules  (TODO)
├── LICENSE                # CC BY 4.0 (data) + MIT (code)       (TODO)
├── requirements.txt       # optional tooling deps (scorer needs none)
├── score.py               # scoring harness, pure stdlib        (TODO)
├── scripts/
│   ├── convert_audio.sh   # normalize recordings -> 16 kHz mono wav  (TODO)
│   ├── run_whisper.py     # baseline: audio -> predictions            (TODO)
│   └── validate.py        # check annotations conform to SCHEMA.md    (TODO)
├── data/
│   ├── audio/             # <clip_id>.wav  (16 kHz mono)
│   ├── annotations/       # <clip_id>.json gold transcripts w/ per-word tags
│   └── predictions/       # <clip_id>.json model hypotheses to score
└── results/
    └── baseline.md        # baseline model score table                (TODO)
```

## The metric

Headline number is the **switch penalty**: how much worse a model does on words
near a language switch vs. monolingual words.

- **Overall WER** — word error rate across all words.
- **Switch-region WER** — WER on words within ±1 token of a language switch.
- **Monolingual WER** — WER on all other words.
- **Switch penalty** = Switch-region WER − Monolingual WER.

Large positive switch penalty = model struggles with code-switching. This single
number is the contribution: it makes an invisible weakness measurable.

## Setup

The core scorer is **dependency-free** (Python 3.8+ stdlib). To score:

```bash
python score.py --ref data/annotations --hyp data/predictions
```

Optional tooling (baseline ASR, WER cross-check):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # openai-whisper, jiwer
# also needs system ffmpeg for scripts/convert_audio.sh
```

## How we build it (the 1-day plan)

1. **Schema first** (linguists) — agree on tag set + rules in `SCHEMA.md`.
2. **Record** 30–60 short Hiligaynon-English-Tagalog clips, 4–10 s each, from 3+
   speakers. Reading natural code-switched sentences aloud is fine.
3. **Transcribe + tag** each clip at the word level into `data/annotations/`.
4. **Double-annotate** ≥10 clips and report inter-annotator agreement.
5. **Baseline** — run one off-the-shelf model (e.g. Whisper) to fill
   `data/predictions/` and produce the first numbers with `score.py`.

## Roadmap

- Grow to 1,000+ clips; per-speaker / per-region breakdowns.
- Add more pairs (Waray-English, Ilocano-English).
- Leaderboard of public ASR systems.

## License

Data under **CC BY 4.0**, code under **MIT** — so anyone can reuse and extend.
Add a `LICENSE` file before submitting.

## AI usage

AI assistants helped scaffold and document this repo. All recordings and
linguistic labels are human-made. See `AI_DISCLOSURE.md`.
