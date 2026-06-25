# scripted_native — Speaker 2 (Nimeesha De Guzman)

Second-speaker recording of the Script 3 elicitation set: 40 prompted
code-switch phrases across 8 domains (5 each), clap-separated, split with
`scripts/split_claps.py` detection. Kept **separate** from Speaker 1's
`data/audio/` (`hil_cs_001..040`) so the single-speaker headline benchmark is
unchanged; merge into the headline only after a multi-speaker decision.

- Speaker: Nimeesha De Guzman (`spk02`), native Hiligaynon, female.
- `subset: scripted_native`, `gold_status: native_gold`.
- Transcripts come from the script; **per-word language tags are not set**
  (`tokens[].lang = null`, `lang_tags_status: seed_unverified`) — a native
  reviewer must confirm wording and tag tokens before scoring.
- Clip IDs `spk2_001..040` map 1:1 to Script 3 lines 1–40.

## Clips needing a manual cut

Clap loudness was inconsistent in three category files, so the detector merged
two adjacent lines and emitted a short junk tail. Re-cut these by hand:

| Domain | Clips | Issue |
|--------|-------|-------|
| market | `spk2_002` (11.5s), `spk2_005` (0.6s) | lines 2–3 merged; line 5 lost |
| transport | `spk2_006` (10.3s), `spk2_010` (0.5s) | lines 6–7 merged; line 10 lost |
| culture | `spk2_027` (11.3s), `spk2_028` (1.3s) | lines 27–28 merged; tail junk |

Flagged in each annotation as `clip_quality: needs_manual_cut`. The other 34
clips are `clip_quality: ok`.
