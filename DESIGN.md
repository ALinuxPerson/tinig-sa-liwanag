---
name: "Sugidanon"
description: "An archival field-report website for a Hiligaynon code-switch ASR benchmark."
colors:
  paper: "#eee3d0"
  paper-light: "#f6ecd8"
  paper-dark: "#d7c8ae"
  ink: "#2f221d"
  ink-strong: "#1d1512"
  muted-ink: "#6e5a48"
  rust: "#a7471d"
  ochre: "#d89021"
  green: "#6f8f3a"
  red: "#b84b3b"
  blue: "#4f6fa3"
  button-dark: "#4a3034"
typography:
  display:
    fontFamily: "Cormorant Garamond, EB Garamond, Libre Baskerville, Georgia, serif"
    fontSize: "clamp(3.4rem, 6.7vw, 6.15rem)"
    fontWeight: 700
    lineHeight: 0.94
    letterSpacing: "-0.035em"
  body:
    fontFamily: "Literata, Georgia, Times New Roman, serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.52
  label:
    fontFamily: "Courier Prime, JetBrains Mono, IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.75rem"
    fontWeight: 700
    letterSpacing: "0.14em"
components:
  paper-stage:
    backgroundImage: "linear-gradient(rgba(238,227,208,.76), rgba(238,227,208,.88)), url('/paper.png')"
    textColor: "{colors.ink}"
  pinned-note:
    backgroundColor: "#eadcc2"
    borderColor: "rgba(70,45,25,.25)"
    transform: "rotate(4deg)"
  metric-gauge:
    border: "4px dotted currentColor"
    shape: "circle"
  token-correct:
    backgroundColor: "#c6d0aa"
    textColor: "{colors.ink}"
  token-error:
    backgroundColor: "#e2a199"
    textColor: "{colors.ink}"
  token-switch:
    underlineColor: "{colors.ochre}"
---

# Design System: Sugidanon

## 1. Overview

**Creative North Star: "Archival Field Report"**

Sugidanon should feel like a linguistic field notebook that became a benchmark
dashboard: paper, ink, transcript marks, dotted gauges, cohort ledgers, and a
right-hand evidence rail. It is data-heavy, but never sterile.

The judged artifact is the ASR benchmark. Translation, G2P, TTS, and Tinig are
future extension layers and must not lead the page.

## 2. Visual World

- Use `public/paper.png` as the page material. Body, panels, notes, and section
  dividers should feel printed or typed on paper.
- The outer scene may use desk/map/archive-cabinet edge treatments, but core
  content stays readable and data-first.
- Pinned notes, tape, archive labels, and torn edges are allowed when they frame
  evidence. They must not hide real numbers or subset boundaries.
- Avoid glassmorphism, neon, pure white cards, gradient blobs, glossy charts,
  and generic SaaS dashboard styling.

## 3. Color

Palette is warm, muted, and dusty:

- **Paper** `#eee3d0`: main sheet and panel material.
- **Ink** `#2f221d`: primary text.
- **Muted Ink** `#6e5a48`: secondary notes and hints.
- **Rust** `#a7471d`: thesis, penalty, CTAs, active filters.
- **Ochre** `#d89021`: switch-region emphasis.
- **Green / Red / Blue**: diff states only. Do not use semantic colors as loose
  decoration.
- **Button Dark** `#4a3034`: reproduction CTA.

## 4. Typography

Use a literary serif for the brand and headline, a readable serif for body, and
a restrained mono for labels, filters, metrics, ledgers, and file paths.

- **Display:** `Cormorant Garamond`, `EB Garamond`, `Libre Baskerville`,
  `Georgia`, serif.
- **Body:** `Literata`, `Georgia`, serif.
- **Technical labels:** `Courier Prime`, `JetBrains Mono`, `IBM Plex Mono`,
  ui-monospace.

Display text can be large and newspaper-like, but keep letter-spacing no tighter
than `-0.04em`. Use italic serif only for the core thesis line, not for every
section.

## 5. Components

### Top Navigation

Navigation is restrained archival UI: plain text links, small GitHub/star
control, no glass, no large pill buttons.

### Pinned Note

The note card explains the name "Sugidanon". It uses aged paper, subtle tape,
mono label text, and a small etched illustration treatment. It is decorative
supporting context, not the main proof.

### Baseline Panel

The baseline reference panel is the first proof object:

- Left cell: model and decoding settings.
- Middle cells: dotted circular gauges for Overall, Hiligaynon, and
  Switch-region WER.
- Right cell: switch penalty with short explanation.

Use canonical numbers only:

| Metric | Value |
|--------|-------|
| Overall WER | 57.4% |
| Monolingual (Hiligaynon) WER | 65.9% |
| Switch-region WER | 35.8% |
| Switch penalty | -30.1% |
| `hil<->en` | 40.0% |
| `hil<->tl` | 24.4% |
| `tl<->en` | 6.2% |

### Evidence Rail

The right rail carries cohort ladder, language-pair bars, reproducibility steps,
and the Colab CTA. It should feel like a research dossier margin. It may be
sticky on desktop and stacked on mobile.

### Transcript Inspector

Transcript rows are styled like annotated transcripts:

- Correct token: muted green highlighter.
- ASR error: muted red highlighter plus strikethrough.
- Switch token: ochre underline/inset mark.
- Prediction block: recessed paper well.
- Color is paired with labels and tooltips; never rely on color alone.

### Clip Rows

Clip rows are compact, scannable evidence. Open rows reveal audio, reference
tokens, prediction, and WER bands. Do not bury clips behind marketing copy.

## 6. Layout Rules

- First viewport must show: brand name, benchmark framing, switch-region WER
  finding, headline metrics, and evidence rail.
- Keep `/clips`, methodology, cohort ledger, and reproducibility anchors
  reachable from top nav.
- On mobile, stack note, baseline panel, rail, and transcript table in that
  order. Horizontal scroll is acceptable for dense clip/cohort tables.
- Cards should have square or lightly rounded paper edges, never large rounded
  SaaS cards.

## 7. Content Rules

- Lead with benchmark, not translation.
- Never blend `non_native_eval` or development cohorts into headline WER.
- Do not invent leaderboard rows or stale baselines. When showing comparison
  slots, label them as submission slots or cohort rows.
- Native speakers are credited as authors, not data sources.
- Hiligaynon references stay `seed_unverified` until native review confirms
  them.

## 8. Do / Do Not

Do:

- Use paper texture, serif hierarchy, mono labels, dotted gauges, transcript
  chips, and archival side props.
- Preserve canonical baseline values from `results/asr_score.txt`.
- Keep every large metric near its protocol context.

Do not:

- Use glass containers, neon, gradient blobs, glossy data-viz, or modern
  dashboard tropes.
- Present Sugidanon as a finished consumer translation app.
- Hide evidence under decorative imagery.
