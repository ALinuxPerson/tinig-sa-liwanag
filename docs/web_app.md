# Web app (demo) — Next.js / Vercel

Deployment, hosted speech transcription, Tagalog-coverage fallback, and the
local Ollama backend for the translation **extension** demo.

The hosted demo is a Next.js app. Live microphone transcription calls the
Hugging Face Space in `spaces/tinig-sa-liwanag-space`, which runs Whisper behind
a Gradio API endpoint.

```bash
npm install
npm run dev
```

Then open `http://localhost:3000`.

### Hosted speech demo

Initialize the Hugging Face Space submodule:

```bash
git submodule update --init --recursive
```

The Space lives at:

```text
https://huggingface.co/spaces/ALinuxPerson/tinig-sa-liwanag-space
```

The Next.js API route posts browser-recorded base64 audio to the Space's Gradio
API:

```text
https://alinuxperson-tinig-sa-liwanag-space.hf.space/gradio_api/call/transcribe_base64
```

Local dev uses that hosted endpoint by default:

```bash
npm run dev
```

Override the endpoint if the Space slug changes:

```bash
HF_SPACE_TRANSCRIBE_URL=https://alinuxperson-tinig-sa-liwanag-space.hf.space npm run dev
```

The browser records audio, the API route validates size/base64 shape, and the
Space runs Whisper. No `OPENAI_API_KEY`, local `ffmpeg`, or local `whisper`
binary is required by the Next.js app.

Production build:

```bash
npm run build
```

Deploy on Vercel:

1. Import this GitHub repository in Vercel.
2. Keep the framework preset as `Next.js`.
3. Use the default commands from `vercel.json`.
4. Deploy.

The Python app in `app/` remains as a local legacy demo; Vercel serves the
Next.js app from `pages/`.

### Tagalog coverage

The local and hosted demos use layered fallback:

1. exact seed benchmark prompt matches
2. curated phrase matches for common English and Tagalog demo cases
3. local Ollama context-aware translation, when available
4. expanded Tagalog/Hiligaynon dictionary fallback

### Local Ollama context backend

The Next.js API route tries Ollama first when running locally. This is the
context-aware path intended to avoid plain word-by-word translation.

Install or start Ollama, then pull a model:

```bash
ollama serve
ollama pull aya:8b
```

In another terminal:

```bash
OLLAMA_MODEL=aya:8b npm run dev
```

Then open:

```text
http://localhost:3000
```

The API uses this backend order:

```text
seed reference -> curated phrase -> Ollama context LLM -> dictionary fallback
```

Vercel cannot access a local Ollama daemon on your laptop, so the deployed site
uses the fallback layers unless it is connected to a hosted LLM endpoint later.

For future larger coverage, use:

```bash
python3 scripts/build_tl_hil_lexicon.py
```

That script builds a noisy Tagalog -> Hiligaynon bridge lexicon from
Kaikki/Wiktionary machine-readable dictionaries by matching shared English
glosses. Glosbe is documented in `RESOURCES.md` as a direct Tagalog-Hiligaynon
manual reference source.
