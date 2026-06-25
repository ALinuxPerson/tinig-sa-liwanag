# Extension subsets (natural speech)

Natural-speech subsets kept **separate** from the headline `scripted_native`
benchmark. They are stored here — not in `data/annotations/` — so they never
enter the headline WER or the standard `score.py` / `run_whisper.py` runs.

| Subset | Dir | Clips | Status |
|--------|-----|-------|--------|
| `native_podcast` | `native_podcast/` | 10 | Whisper-seeded, `seed_unverified` |
| `native_vlog` | `native_vlog/` | 10 | Whisper-seeded, `seed_unverified` |

## Status and rules

- Transcripts are **Whisper-seeded drafts**, not gold. `gold_status:
  seed_unverified`.
- Per-word language tags are **not set** (`tokens[].lang = null`) — a native
  Hiligaynon speaker must transcribe-correct and tag before these are scored.
- Source rights: YouTube, confirmed by Team Hague. Fill exact title/URL in
  `docs/source_ledger.md`.
- Some vlog clips (`vlog_001`, `vlog_003`, `vlog_010`) fall on music/intro and
  should be dropped on review (no-music policy, `SCHEMA.md`).
- Audio is mono 16 kHz WAV, segmented to 5-15s on silence boundaries.

Report these subsets separately when scored. Never blend into the headline
`scripted_native` number.
