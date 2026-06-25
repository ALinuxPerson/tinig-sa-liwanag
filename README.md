# Tinig sa Liwanag

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

## Why this matters

Hiligaynon is spoken by millions of Filipinos, but open translation and speech
resources remain limited. A speech model is only useful if the language layer
understands meaning, context, and local usage. This project therefore starts
with text translation before audio:

- Word-by-word lookup is not enough for useful translation.
- A benchmark makes failures visible and reproducible.
- Human-reviewed Hiligaynon references become reusable data.
- The same examples can later seed STT/TTS and speech-to-speech evaluation.

## Repository structure

```text
tinig-sa-liwanag/
├── README.md
├── SCHEMA.md
├── RESOURCES.md
├── AI_DISCLOSURE.md
├── score.py                         # legacy ASR switch-point scorer
├── scripts/
│   ├── evaluate_translation.py       # primary v1 evaluator
│   ├── translate_hil.py              # dictionary or HF translation backend
│   ├── validate.py                   # validates translation benchmark or ASR files
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
│   └── index.html
└── results/
    └── baseline.md
```

## Quick start

No installs are required for the core benchmark tooling.

```bash
# validate the translation benchmark
python3 scripts/validate.py --kind translation --dir data/benchmark

# evaluate the included dictionary baseline
python3 scripts/evaluate_translation.py \
  --refs data/benchmark/hil_translation_v1.jsonl \
  --preds data/predictions/translation_baseline_dict.jsonl

# run the local demo app
python3 app/server.py
```

Then open `http://localhost:8000`.

## Benchmark format

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

## Legacy and future speech work

This repository still contains earlier speech-oriented utilities:

- `score.py` for code-switched ASR switch-region WER
- `scripts/run_whisper.py`
- `scripts/tts_route.py`
- `g2p_hil/`
- `data/annotations/`

These are not the v1 focus anymore. They remain useful for the later STT/TTS
phase after the translation benchmark is credible.

## License

Data under **CC BY 4.0**, code under **MIT**. See `LICENSE`.

## AI usage

AI assistants helped scaffold and revise this project. Hiligaynon reference
translations and gold labels must be reviewed by humans before release. See
`AI_DISCLOSURE.md`.
