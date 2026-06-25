# External Resources

This project is translation-first for v1. Speech resources are still listed
because they matter for the future STT/TTS phase, but the immediate target is a
reviewed Hiligaynon text translation benchmark.

Check each resource's license before redistributing derived data.

## Translation and text resources

| Resource | Use | Link | Notes |
|----------|-----|------|-------|
| Kaufmann's Visayan-English Dictionary (KVED) | Hiligaynon lexicon and terminology checks | https://bohol.ph/kved.php | Use for manual lookup; do not bulk redistribute without checking terms. |
| Motus Hiligaynon Dictionary | Lexicon and usage checks | Internet Archive / UH ScholarSpace | Useful for reviewer reference. |
| pinoydictionary Hiligaynon | Queryable Hiligaynon dictionary | https://hiligaynon.pinoydictionary.com | Manual lookup only unless terms allow more. |
| kaikki.org Hiligaynon | Machine-readable Wiktionary-derived entries | https://kaikki.org/dictionary/Hiligaynon/ | Can seed `data/lexicon_hil_auto.tsv`; check CC BY-SA obligations. |
| ASJP Hiligaynon wordlist | Small machine-readable wordlist | https://asjp.clld.org | Useful for starter lexical coverage. |
| hilisenti-v1 | Hiligaynon text examples | https://huggingface.co/datasets/jjjardev/hilisenti-v1 | Check license before reuse. |

## Translation and language models

| Model | Use | Link |
|-------|-----|------|
| lfm25-sft-hiligaynon | Optional neural baseline for Hiligaynon text generation/translation | https://huggingface.co/welyjesch/lfm25-sft-hiligaynon |
| hiligaynon_llama_3.1 finetuned LoRA | Optional Hiligaynon text baseline | https://huggingface.co/PLTAT/hiligaynon_llama_3.1_finetuned_lora |
| hiligaynon_llama_3.1 tokenizer | Companion tokenizer | https://huggingface.co/PLTAT/hiligaynon_llama_3.1_finetuned_lora_tokenizer |
| hiligaynon_llama_3.1 FT 8B GGUF | Quantized local inference candidate | https://huggingface.co/PLTAT/hiligaynon_llama_3.1_FT_8B_GGUF |

Use these as baselines or fine-tuning starting points. Do not claim they are
accurate for Hiligaynon translation until they are evaluated on the benchmark
and reviewed by speakers.

## Building the dictionary baseline

The offline demo uses `data/lexicon_hil.tsv`, optionally merged with an
auto-built Wiktionary lexicon:

```bash
python3 scripts/build_dictionary.py
python3 scripts/translate_hil.py "Good morning, I went to the market yesterday"
```

The dictionary baseline is intentionally limited. It helps show why contextual
translation is needed.

## Benchmark sources to create yourselves

For the judged artifact, prioritize human-authored and human-reviewed examples:

- daily life instructions
- health and emergency messages
- classroom and education text
- public service announcements
- code-switched Filipino-English-Hiligaynon prompts
- ambiguous examples where context changes the correct translation

Avoid copying copyrighted paragraphs into the benchmark unless the license
explicitly allows redistribution.

## Future audio / speech data

These resources are deferred until after the text benchmark is credible.

| Resource | Use | Link | Access |
|----------|-----|------|--------|
| G2P-ASR (AngelAquino) | Hiligaynon audio, transcripts, and pronunciation data | https://github.com/AngelAquino/g2p-asr | Public GitHub; check license and cite authors. |
| Philippine Languages Database (PLD) | Large Philippine speech corpus | https://aclanthology.org/2024.sigul-1.32.pdf | Request access; check terms. |
| Bloom Library Talking Books | Read-aloud Hiligaynon audio and text | https://bloomlibrary.org | Check license per title. |
| Hiligaynon Speech Audio Sets | Monolingual speech baseline material | https://speech-data.ai/datasets/hiligaynon/ | Check terms. |

## Future TTS models

| Model | Use | Link |
|-------|-----|------|
| F5-TTS OpenBible Hiligaynon | Hiligaynon synthesis candidate | https://huggingface.co/multilingual-tts/F5-TTS-OpenBible-Hiligaynon |
| VITS OpenBible Hiligaynon | Alternative Hiligaynon TTS backend | https://huggingface.co/multilingual-tts/VITS-OpenBible-Hiligaynon |
| EveryVoice OpenBible Hiligaynon | Alternative Hiligaynon TTS backend | https://huggingface.co/multilingual-tts/EveryVoice-OpenBible-Hiligaynon |

## Future pronunciation / G2P resources

| Resource | Use | Link | License |
|----------|-----|------|---------|
| CMU Pronouncing Dictionary | English word-to-phoneme lookup | https://github.com/cmusphinx/cmudict | MIT-style |
| WikiPron Tagalog | Tagalog IPA and word list | https://github.com/CUNY-CL/wikipron | CC0/CC-BY, varies by dump |
| G2P-ASR Hiligaynon portion | Hiligaynon phonetic transcriptions | https://github.com/AngelAquino/g2p-asr | Check source terms |

```bash
python3 scripts/build_lexicon.py --which all
```

## Licensing rule

The repo can release original benchmark rows under CC BY 4.0 only if the source
text and Hiligaynon reference are original or license-compatible. Keep
provenance notes for anything adapted from a third-party source.
