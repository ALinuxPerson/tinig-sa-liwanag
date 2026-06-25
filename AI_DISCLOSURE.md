# AI Usage Disclosure

**Project:** Sugidanon — A Code-Switched Hiligaynon-Tagalog-English Speech
Evaluation Benchmark
**Track:** Inclusive Speech Technology for Philippine Languages (FTIC / GitHub)
**Team:** [TEAM NAME]
**Date:** [DATE]

We used AI coding and writing assistants during this project. In the spirit of
open and honest research, this document discloses which tools were used, for
what, and what the team did itself.

## Tools used

| Tool | Provider | How we used it |
|------|----------|----------------|
| **Claude** (Claude Code / Claude.ai) | Anthropic | Project scoping, repo scaffolding, drafting `score.py` + scripts, schema design, Hiligaynon G2P rules, documentation. |
| **Codex** (OpenAI / GitHub Copilot) | OpenAI | Editor code completion and small refactors; helper scripts. |
| **Gemini** | Google | Cross-checking explanations, seed-sentence ideas, reviewing doc wording. |

> Edit the rows above to match what your team actually used. Remove any tool you
> did not use. Do not claim a tool you didn't use.

## What AI assisted with

- Scaffolding the repository structure and configuration files.
- Drafting and explaining the WER scoring logic and the switch-penalty metric
  (overall / switch-region / monolingual, plus per-pair breakdown).
- Drafting the Hiligaynon grapheme-to-phoneme rule set (reviewed by linguists).
- Writing and editing documentation (README, SCHEMA, this disclosure).
- Suggesting example/seed sentences and tagging-rule wording.

## What the team did ourselves (not AI)

- **All audio recordings** — produced by human Hiligaynon (Ilonggo) speakers on
  our team and from consenting volunteers.
- **All language annotations** — every word-level `hil` / `tl` / `en` / `other`
  tag was decided by human native speakers. AI did not assign linguistic labels.
- **hil vs tl disambiguation** — judged by native Ilonggo/Tagalog speakers.
- **Inter-annotator agreement** — verified by two human annotators.
- **Final review** — all AI-generated code and text was read, tested, and
  approved by the team. We take responsibility for the contents of this repo.

## Data, consent, and ethics

- Speakers gave informed consent for their voice recordings to be released under
  an open license.
- No personally identifying information beyond coarse speaker metadata
  (region, age band, gender) is published.
- Third-party datasets/models are used under their own licenses (see
  `RESOURCES.md`).
- The dataset is released under **CC BY 4.0** and the code under the **MIT**
  license.

## Note on accuracy

AI tools can produce errors. We manually tested the scoring script and reviewed
all generated content. Any remaining mistakes are the team's responsibility, not
the tools'.

---
*Signed: [TEAM MEMBER NAMES]*
