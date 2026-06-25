# Annotation Schema — Sugidanon

Sugidanon targets **code-switched Hiligaynon–Tagalog–English speech**. Each clip
is annotated at the **word (token) level** so evaluation can measure how well a
speech recognizer performs *specifically at language switch points*, which is
where most ASR systems fail.

## Files

```
data/
  audio/            # one .wav per clip (16 kHz mono recommended)
  annotations/      # one .json per clip (the gold reference)
  predictions/      # one .json per clip (a model's hypothesis, for scoring)
```

## Annotation JSON (one file per clip)

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
    { "idx": 1, "text": "ko",          "lang": "hil" },
    { "idx": 2, "text": "kahapon",     "lang": "hil" },
    { "idx": 3, "text": "kay",         "lang": "hil" },
    { "idx": 4, "text": "super",       "lang": "tl"  },
    { "idx": 5, "text": "traffic",     "lang": "en"  }
  ]
}
```

### Field rules

- **clip_id** — unique, prefixed by the dominant language pair:
  `hil_en_`, `hil_tl_`, `tl_en_`.
- **tokens** — the gold transcript, already tokenized (split on whitespace).
  Keep punctuation OUT of tokens; normalize to lowercase only in scoring, not here.
- **idx** — contiguous integers starting at 0 (validated).
- **lang** — one of:
  - `hil` Hiligaynon (Ilonggo)
  - `tl`  Tagalog / Filipino
  - `en`  English
  - `other` proper nouns, brands, ambiguous, or another PH language
- **matrix_language** — the dominant/base language of the utterance (the grammar
  it follows). The *embedded* language is the one being inserted.

### Switch points (derived, not hand-labeled)

A **switch point** is any token whose `lang` differs from the previous token's
`lang` (ignoring `other`). You do NOT label these by hand — `score.py` computes
them from the `lang` sequence. A **switch-region word** is any token within a
window of ±1 of a switch point; everything else is **monolingual**. This lets us
report WER on switch regions vs monolingual regions separately, and by language
pair (hil↔tl, hil↔en, tl↔en).

## Tagging guidelines (for annotators)

1. **Tag the word as the language it comes from**, not how it's pronounced.
   "traffic" said with an Ilonggo accent is still `en`.
2. **Borrowed/nativized words** standard in Ilonggo (e.g. "kompyuter",
   "tindahan") → `hil`, not `en`.
3. **Proper nouns** (names, brands, places) → `other`.
4. **Fillers** ("uh", "ah", "ano", "te") → matrix language.
5. **Numbers** → tag by the language actually spoken ("duha" = hil, "dalawa" = tl,
   "two" = en).
6. When two annotators disagree, record both and resolve by discussion; report
   **inter-annotator agreement** (% token-level lang agreement) in the README.

### hil vs tl disambiguation (the hard case)

Hiligaynon and Tagalog share much vocabulary, so labels can collide. Rules:

- **Tag by the form actually spoken**, not the meaning:
  `ginahimo` → `hil`, `ginagawa` → `tl`; `indi` → `hil`, `hindi` → `tl`.
- **Identical-in-both word** (same spelling, both languages) → tag by the
  **sentence's matrix language** (usually `hil` in this corpus).
- **Nativized loanwords** standard in Ilonggo → `hil`.
- Affixes are decisive: Hiligaynon `nag-/ga-/mag-` patterns vs Tagalog
  `nag-/um-/ma-` — tag by the affix system the word uses.

## Recommended scale for a 1-day benchmark

- Hiligaynon matrix throughout; partners Tagalog + English.
- 40–60 clips, 4–10 seconds each.
- 3+ speakers (Iloilo / Bacolod) for voice diversity.
- Every clip transcribed AND a subset (≥10) double-annotated for agreement.
