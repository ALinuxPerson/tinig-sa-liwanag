#!/usr/bin/env python3
"""
translate_context_refine.py — Context-aware translate + self-critique baseline.

For each benchmark row this runs an AI-augmented, context-based pipeline using a
local Ollama LLM (no fine-tuning):

  1. TRANSLATE  the model translates source_text into Hiligaynon, conditioned on
                the row's human-written `context` and `phenomena` labels.
  2. CRITIQUE   the model checks the draft against that same context (meaning,
                register, sense of ambiguous words, intentional code-switches)
                and returns either OK or a corrected FINAL line.

Output is a predictions JSONL ({id, model, prediction}) that
scripts/evaluate_translation.py scores. Run once with --no-refine and once
without to measure whether the critique step actually helps.

This is a DEMO baseline, not validated translation. The LLM critic can be
confidently wrong in a low-resource language; predictions still need
native-speaker review (AI_DISCLOSURE.md).

Two backends (no fine-tuning, no GPU needed):

  --backend ollama   local Ollama daemon (default). Free but needs a capable
                     local model; small models do Hiligaynon poorly.
  --backend openai   any OpenAI-compatible /chat/completions endpoint. Use a
                     FREE hosted provider for far better low-resource quality:
                       Google Gemini (free tier, strong multilingual):
                         LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
                         LLM_MODEL=gemini-2.0-flash
                       Groq (free tier, fast, hosts llama-3.3-70b / gemma2-9b):
                         LLM_BASE_URL=https://api.groq.com/openai/v1
                         LLM_MODEL=llama-3.3-70b-versatile
                     Set LLM_API_KEY to the provider key.

Pure standard library (urllib).

Usage:
    # local Ollama
    ollama serve && ollama pull aya:8b
    python3 scripts/translate_context_refine.py --backend ollama --model aya:8b

    # free hosted (Gemini)
    export LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
    export LLM_API_KEY=...      # AI Studio key
    python3 scripts/translate_context_refine.py --backend openai --model gemini-2.0-flash \
        --out data/predictions/translation_context_refine.jsonl

    # single-shot (no critique) for A/B comparison
    python3 scripts/translate_context_refine.py --no-refine \
        --out data/predictions/translation_context_single.jsonl

    # preview the prompts without calling the model
    python3 scripts/translate_context_refine.py --dry-run --limit 2
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "aya:8b")
DEFAULT_OPENAI_BASE = os.environ.get("LLM_BASE_URL", "")
DEFAULT_OPENAI_KEY = os.environ.get("LLM_API_KEY", "")
DEFAULT_OPENAI_MODEL = os.environ.get("LLM_MODEL", "gemini-2.0-flash")


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def translate_prompt(row):
    phenomena = ", ".join(row.get("phenomena", [])) or "none"
    return "\n".join([
        "You are a careful Hiligaynon (Ilonggo) translator.",
        "Translate the SOURCE into natural Hiligaynon.",
        "Use the CONTEXT to pick the right meaning, tone, and register.",
        "Do not translate word by word. Preserve named entities.",
        "Keep intentional English/Tagalog code-switch words if they are normal in Ilonggo speech.",
        "Return ONLY the Hiligaynon translation, no explanation.",
        "",
        f"CONTEXT: {row.get('context', '').strip() or 'none'}",
        f"PHENOMENA: {phenomena}",
        f"SOURCE: {row['source_text']}",
        "Hiligaynon:",
    ])


def critique_prompt(row, draft):
    return "\n".join([
        "You are reviewing a Hiligaynon translation against its intended context.",
        "Check: is the meaning preserved? Is the register/tone right?",
        "Are ambiguous words translated in the sense the context implies?",
        "Are intentional code-switch words kept?",
        "If the draft is already good, keep it. Otherwise correct it.",
        "Respond in EXACTLY this format, nothing else:",
        "VERDICT: OK or FIX",
        "FINAL: <the best Hiligaynon translation>",
        "",
        f"CONTEXT: {row.get('context', '').strip() or 'none'}",
        f"SOURCE: {row['source_text']}",
        f"DRAFT: {draft}",
    ])


def ollama_generate(host, model, prompt, timeout):
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.9},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{host}/api/generate", data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data.get("response") or "").strip()


def openai_generate(base_url, api_key, model, prompt, timeout):
    """Call any OpenAI-compatible /chat/completions endpoint (Gemini, Groq, ...)."""
    body = json.dumps({
        "model": model,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data["choices"][0]["message"]["content"] or "").strip()


def make_generate(args):
    """Return a generate(prompt) closure bound to the chosen backend."""
    if args.backend == "ollama":
        return lambda prompt: ollama_generate(args.host, args.model, prompt, args.timeout)
    if not args.base_url:
        sys.exit("--backend openai needs LLM_BASE_URL (or --base-url). See module docstring.")
    if not args.api_key:
        sys.exit("--backend openai needs LLM_API_KEY (or --api-key).")
    return lambda prompt: openai_generate(args.base_url, args.api_key, args.model,
                                          prompt, args.timeout)


def clean(text):
    text = text.strip().strip('"').strip("'").strip()
    for prefix in ("Hiligaynon:", "Translation:", "FINAL:"):
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    return text


def parse_critique(out, draft):
    """Pull the FINAL line; fall back to draft if the format is off."""
    verdict, final = "OK", draft
    for line in out.splitlines():
        s = line.strip()
        if s.upper().startswith("VERDICT:"):
            verdict = s.split(":", 1)[1].strip().upper()
        elif s.upper().startswith("FINAL:"):
            final = s.split(":", 1)[1].strip()
    return verdict, clean(final) or draft


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", default="data/benchmark/hil_translation_v1.jsonl")
    ap.add_argument("--out", default="data/predictions/translation_context_refine.jsonl")
    ap.add_argument("--backend", choices=["ollama", "openai"], default="ollama",
                    help="ollama (local) or openai (any OpenAI-compatible host)")
    ap.add_argument("--host", default=DEFAULT_OLLAMA_HOST, help="Ollama host")
    ap.add_argument("--base-url", default=DEFAULT_OPENAI_BASE,
                    help="OpenAI-compatible base URL (or LLM_BASE_URL)")
    ap.add_argument("--api-key", default=DEFAULT_OPENAI_KEY, help="API key (or LLM_API_KEY)")
    ap.add_argument("--model", default=None, help="model id (backend-specific default)")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--limit", type=int, default=0, help="max rows (0 = all)")
    ap.add_argument("--no-refine", action="store_true",
                    help="skip the critique step (single-shot, for A/B)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print prompts, do not call the model")
    args = ap.parse_args()

    if args.model is None:
        args.model = DEFAULT_OLLAMA_MODEL if args.backend == "ollama" else DEFAULT_OPENAI_MODEL

    rows = read_jsonl(args.refs)
    if args.limit:
        rows = rows[:args.limit]

    mode = "single" if args.no_refine else "refine"
    model_label = f"{args.backend}-context-{mode}:{args.model}"

    if args.dry_run:
        for row in rows:
            print("=" * 60)
            print(translate_prompt(row))
            if not args.no_refine:
                print("-" * 20, "critique", "-" * 20)
                print(critique_prompt(row, "<draft goes here>"))
        return

    generate = make_generate(args)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    n_fixed = 0
    with open(args.out, "w", encoding="utf-8") as fout:
        for i, row in enumerate(rows, 1):
            try:
                draft = clean(generate(translate_prompt(row)))
                prediction = draft
                if not args.no_refine:
                    out = generate(critique_prompt(row, draft))
                    verdict, prediction = parse_critique(out, draft)
                    if verdict == "FIX" and prediction != draft:
                        n_fixed += 1
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                where = args.host if args.backend == "ollama" else args.base_url
                sys.exit(f"Backend request failed ({args.backend}, {where}): {e}\n"
                         "Check the daemon/endpoint, model id, and API key.")
            fout.write(json.dumps(
                {"id": row["id"], "model": model_label, "prediction": prediction},
                ensure_ascii=False) + "\n")
            print(f"[{i}/{len(rows)}] {row['id']}: {prediction[:60]}")

    print(f"\nWrote {len(rows)} predictions to {args.out}")
    if not args.no_refine:
        print(f"Critique changed {n_fixed}/{len(rows)} drafts.")
    print("Score with: python3 scripts/evaluate_translation.py "
          f"--refs {args.refs} --preds {args.out}")
    print("These are AI demo outputs — native-speaker review still required.")


if __name__ == "__main__":
    main()
