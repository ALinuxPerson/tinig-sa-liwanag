# CLAUDE.md

Guidance for working in this repository.

## What this is

**Sugidanon** — an open **code-switch ASR benchmark for Hiligaynon (Ilonggo)**.
The judged artifact is the speech benchmark, **not** the translation scaffold.
Lead all framing with the benchmark; translation / Tinig / G2P / TTS are
extension layers for a later STT → translation → TTS phase.

Core contribution: **switch-region WER** — separating ASR errors on the
Hiligaynon matrix language from errors on borrowed English/Tagalog words near a
language switch. The finding: models transcribe the borrowed words well but miss
the Hiligaynon, a **negative switch penalty**.

## Canonical baseline numbers (do not drift)

Source of truth is `results/asr_score.txt` (Whisper small, `--language tl`).
Use these everywhere; never invent or copy stale variants:

| Metric | Value |
|--------|-------|
| Overall WER | 59.5% |
| Monolingual (Hiligaynon) WER | 66.3% |
| Switch-region WER | 35.8% |
| Switch penalty | −30.6% |
| `hil↔en` | 40.0% |
| `hil↔tl` | 24.4% |
| `tl↔en` | 6.2% |

A second comparison baseline (`whisper-small-auto`) lives in
`results/asr_baselines.md`. Forcing `tl` beats auto on every metric.

## Layout

- `score.py` — switch-region WER scorer (stdlib; `align`, `normalize`,
  `switch_region_flags` are reused elsewhere).
- `data/annotations/hil_cs_001..040.json` — headline `scripted_native` set,
  Speaker 1 (Aziel Faith Agustin, `spk01`).
- `data/audio/`, `data/predictions/` (forced-tl), `data/predictions_auto/`.
- `data/extensions/` — kept **out** of the headline; never blended into the
  headline WER:
  - `scripted_native_spk2/` — Speaker 2 (Nimeesha De Guzman, `spk02`), 40 clips.
  - `non_native_eval/` — 20 podcast/vlog clips, `not_native_gold`, robustness only.
- `pages/` — Next.js site: `index.js` (landing), `benchmark.js` (`/benchmark`
  explorer), `demo.js` (translation extension). Build data: `public/benchmark.json`.
- `notebooks/sugidanon_colab.ipynb` — one-click judge-facing reproduction.
- `docs/` — `evaluation_report.md`, `source_ledger.md`, `improvement_plan.md`.
- `SCHEMA.md` — annotation + subset schema.

## Key scripts

- `scripts/build_release.py` — canonical release builder (used by the Colab).
- `scripts/package_dataset.py` — dataset/benchmark packaging + statistics.
- `scripts/build_benchmark_web.py` — emits `public/benchmark.json` + copies clip
  audio to `public/clips/` for the `/benchmark` page (reuses `score.py`).
- `scripts/run_whisper.py` — baseline ASR. `scripts/split_claps.py` — clap-split
  per-category recordings into per-phrase clips.
- `scripts/validate.py` — annotation validation.

## Subsets (see SCHEMA.md)

`scripted_native` (headline) · `native_podcast` · `native_vlog` ·
`non_native_eval` (robustness only). Each clip carries `subset`, `source_type`,
`speech_style`, `gold_status`. **Never** count `non_native_eval` toward the
native headline; **never** blend subsets into one WER.

## Conventions & ethics

- Hiligaynon references stay `seed_unverified` / per-word `lang` tags stay unset
  until a native speaker confirms. AI output is never treated as language gold.
- Core benchmark tooling is stdlib-only (no install needed).
- Record provenance + license for any third-party data in `docs/source_ledger.md`.
- Native speakers are credited as authors, not data sources.
- Keep the canonical numbers consistent across README, `hf_dataset/README.md`,
  `docs/evaluation_report.md`, the Colab, and the landing page.
