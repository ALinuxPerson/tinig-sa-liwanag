# Source Ledger

Provenance and rights for every audio source used in the Sugidanon code-switch
ASR benchmark. One row per source. No external audio enters the benchmark
without a documented row here.

See `docs/licensing.md` for the repository license structure and
`SCHEMA.md` for the subset definitions.

## Sources

| Source ID | Title | URL | Rights | Subset | Clips | Notes |
|-----------|-------|-----|--------|--------|-------|-------|
| `src_scripted_01` | Team Hague elicitation set | local (`data/audio/`) | CC BY 4.0 (text); audio recorded by the reviewing speaker | `scripted_native` | 40 | Speaker consented; reference text reviewed; per-word tags `seed_unverified` |
| `src_nonnative_01` | Ilongga Talks Podcast Episode 1 (saify TeeVee) | https://www.youtube.com/watch?v=EQuaPh4axGg | YouTube; rights confirmed by Team Hague | `non_native_eval` | 10 | Non-native speech (`podcast_*`); `not_native_gold`; Whisper-seeded; tags not set; robustness only |
| `src_nonnative_02` | ilonggo (hiligaynon) only for a day (Nisa Nuggets) | https://www.youtube.com/watch?v=iMu7p4NvOlg | YouTube; rights confirmed by Team Hague | `non_native_eval` | 10 | Non-native speech (`vlog_*`); `not_native_gold`; exclude music clips (`vlog_001/003/010`) on review; robustness only |

## Required record per external source

For each new external source (podcast, vlog, non-native), record before ingest:

- source title
- source URL
- creator or rights holder
- license or permission status
- date accessed
- whether audio redistribution is allowed
- attribution text required by the license
- excluded sections (music, intro, outro, overlapping speech)

## Clip policy for external audio

- segment into 5-15 second clips
- avoid background music
- avoid overlapping speakers unless explicitly labeled
- avoid private or personally identifying content
- convert to mono 16 kHz WAV
- manually review transcripts before using as benchmark references

## Rules

- Do not publish external audio without documented redistribution rights.
- Keep non-native clips out of the native headline score (`non_native_eval` only).
- Do not claim token language tags are gold while they remain `seed_unverified`.
