# External Resources

Open datasets and models Sugidanon builds on. **Check each one's license before
redistributing** — we only ship our own recordings under CC BY 4.0; third-party
assets stay under their original terms (see `AI_DISCLOSURE.md`).

## Audio / speech data

| Resource | Use | Link | Access |
|----------|-----|------|--------|
| **G2P-ASR** (AngelAquino) — **start here** | Real Hiligaynon audio + transcripts + pronunciation/phone data. Clone & ingest directly. | https://github.com/AngelAquino/g2p-asr | Public GitHub. **No license file** — research use; credit the authors (Aquino et al., ISMAC 2019). |
| **Philippine Languages Database (PLD)** | Richest Hiligaynon source; 454+ hrs across PH languages. | https://aclanthology.org/2024.sigul-1.32.pdf | Request access; CC for research. |
| **Bloom Library** "Talking Books" | Clean read-aloud Hiligaynon audio + aligned text; monolingual samples. | https://bloomlibrary.org | Free, openly licensed; check per-title license. |
| Hiligaynon Speech Audio Sets | Source audio + monolingual baseline material | https://speech-data.ai/datasets/hiligaynon/ | Check terms |
| Hiligaynon Text Samples (hilisenti-v1) | Sentence/text mining for code-switch prompts | https://huggingface.co/datasets/jjjardev/hilisenti-v1 | HF, check license |

### How to pull G2P-ASR

```bash
bash scripts/fetch_g2p_asr.sh            # clones into external/g2p-asr
python scripts/ingest.py external/g2p-asr/data --prefix hil --limit 40
# -> writes data/audio/*.wav + STUB data/annotations/*.json (all hil)
# then HUMANS fix code-switch tags per SCHEMA.md
```

> **Licensing note:** these are third-party corpora. Ingested audio stays under
> its source license — do NOT relicense it CC BY 4.0. Only our own recordings
> are CC BY 4.0. Keep provenance in each clip's annotation if redistributing.

## TTS models (for the TTS PoC — `scripts/tts_route.py`)

| Model | Use | Link |
|-------|-----|------|
| F5-TTS OpenBible Hiligaynon | Hiligaynon synthesis path (phoneme/voice) | https://huggingface.co/multilingual-tts/F5-TTS-OpenBible-Hiligaynon |
| VITS OpenBible Hiligaynon | Alt. Hiligaynon TTS backend | https://huggingface.co/multilingual-tts/VITS-OpenBible-Hiligaynon |
| EveryVoice OpenBible Hiligaynon | Alt. Hiligaynon TTS backend | https://huggingface.co/multilingual-tts/EveryVoice-OpenBible-Hiligaynon |

## LLMs (optional — text normalization / annotation assist, not for labels)

| Model | Use | Link |
|-------|-----|------|
| hiligaynon_llama_3.1 finetuned (LoRA) | Hiligaynon text tasks | https://huggingface.co/PLTAT/hiligaynon_llama_3.1_finetuned_lora |
| └ tokenizer | companion tokenizer | https://huggingface.co/PLTAT/hiligaynon_llama_3.1_finetuned_lora_tokenizer |
| └ 8B GGUF | quantized inference | https://huggingface.co/PLTAT/hiligaynon_llama_3.1_FT_8B_GGUF |
| lfm25-sft-hiligaynon | Hiligaynon SFT model | https://huggingface.co/welyjesch/lfm25-sft-hiligaynon |

## Lexicons & dictionaries

**Translation pairs (en/tl → hil)** — curate by hand into `data/lexicon_hil.tsv`
(a native speaker must verify). These bilingual dicts are the source material:

| Resource | Use | Link |
|----------|-----|------|
| Kaufmann's Visayan-English Dictionary (KVED) | Largest Hiligaynon lexicon, 23,557 entries, searchable | https://bohol.ph/kved.php |
| Motus, Hiligaynon Dictionary | Full dictionary, downloadable PDF | Internet Archive / UH ScholarSpace |
| pinoydictionary (Hiligaynon) | Large queryable online Hiligaynon dictionary | https://hiligaynon.pinoydictionary.com |
| ASJP Hiligaynon wordlist | Clean machine-readable (JSON/RDF) Swadesh wordlist | https://asjp.clld.org |

**Pronunciation / G2P** — machine-readable, auto-fetchable via
`scripts/build_lexicon.py` (feeds the TTS router, not translation):

| Resource | Use | Link | License |
|----------|-----|------|---------|
| CMU Pronouncing Dictionary (cmudict) | English word→phonemes, ~134k; English G2P + wordlist | https://github.com/cmusphinx/cmudict | MIT-style |
| WikiPron (tl) | Tagalog word→IPA; Tagalog G2P | https://github.com/CUNY-CL/wikipron | CC0/CC-BY |
| G2P-ASR (Hiligaynon portion) | Hiligaynon words + gold phonetic transcriptions; best for hil G2P/TTS | https://github.com/AngelAquino/g2p-asr | research use |
| PanLex / diksiyonaryo.ph (Tagalog) | Broader Tagalog word lists | https://panlex.org · https://diksiyonaryo.ph | varies |

```bash
python scripts/build_lexicon.py --which all   # -> data/cmudict.txt, wikipron_tl.tsv
```

> Scrape responsibly: respect each site's terms. KVED / Motus / pinoydictionary
> are for building `lexicon_hil.tsv` by hand, not bulk redistribution.

## STT baseline

- **OpenAI Whisper** (`scripts/run_whisper.py`) — no native `hil`; use Tagalog
  (`tl`) as the closest language code. The whole point of the benchmark is to
  expose how it degrades at hil↔tl / hil↔en switch points.
- **Meta MMS** — broader Philippine-language coverage; candidate second baseline.

> Linguistic labels in `data/annotations/` are human-made. The LLMs above may
> assist text normalization but must NOT assign the gold `lang` tags.
