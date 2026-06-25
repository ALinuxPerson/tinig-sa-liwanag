# External Resources

Open datasets and models Sugidanon builds on. **Check each one's license before
redistributing** — we only ship our own recordings under CC BY 4.0; third-party
assets stay under their original terms (see `AI_DISCLOSURE.md`).

## Audio / speech data

| Resource | Use | Link |
|----------|-----|------|
| Hiligaynon Speech Audio Sets | Source audio + monolingual baseline material | https://speech-data.ai/datasets/hiligaynon/ |
| Hiligaynon Text Samples (hilisenti-v1) | Sentence/text mining for code-switch prompts | https://huggingface.co/datasets/jjjardev/hilisenti-v1 |

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

## STT baseline

- **OpenAI Whisper** (`scripts/run_whisper.py`) — no native `hil`; use Tagalog
  (`tl`) as the closest language code. The whole point of the benchmark is to
  expose how it degrades at hil↔tl / hil↔en switch points.
- **Meta MMS** — broader Philippine-language coverage; candidate second baseline.

> Linguistic labels in `data/annotations/` are human-made. The LLMs above may
> assist text normalization but must NOT assign the gold `lang` tags.
