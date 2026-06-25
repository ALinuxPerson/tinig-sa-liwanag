# Source Ledger

Provenance and rights for every audio source used in the Sugidanon code-switch
ASR benchmark. One row per source. No external audio enters the benchmark
without a documented row here.

See `docs/licensing.md` for the repository license structure and
`SCHEMA.md` for the subset definitions.

## Current release sources

| Source ID | Title | URL | Rights | Subset | Clips | Notes |
|-----------|-------|-----|--------|--------|-------|-------|
| `src_scripted_01` | Team Hague elicitation set | local (`data/audio/`) | CC BY 4.0 (text); audio recorded by the reviewing speaker | `scripted_native` | 40 | Speaker consented; reference text reviewed; per-word tags `seed_unverified` |

## Candidate future sources

External podcast or vlog audio is not part of the current public benchmark
release. Candidate sources must stay out of `data/audio/` and out of headline
WER until redistribution rights, speaker status, transcript quality, and subset
labels are documented.

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
