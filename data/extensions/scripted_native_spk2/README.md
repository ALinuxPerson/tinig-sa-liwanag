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

## Cut quality

Clap loudness was inconsistent in market/transport/culture, so amplitude
clap-splitting merged lines and left junk tails. Those three files were re-cut
with Whisper word-timestamp alignment to the known script lines, which recovered
clean boundaries for all but one.

| Clip | Dur | Status |
|------|-----|--------|
| `spk2_003` | 9.3s | `needs_manual_cut` — Whisper mistranscribed line 4 ("Indi pagbaklon …"), so its words bucketed into line 3; 003 holds lines 3+4, 004 is truncated |
| `spk2_004` | 1.5s | `needs_manual_cut` — truncated tail of line 4 |

The other **38** clips are `clip_quality: ok`. Flags are recorded per annotation.
