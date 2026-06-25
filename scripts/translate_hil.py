#!/usr/bin/env python3
"""
translate_hil.py — Translate English / Tagalog text INTO Hiligaynon.

Two backends:

  --backend dict   Offline starter lexicon. Zero dependencies, runs anywhere.
                   Word-by-word lookup — a DEMO stub, NOT fluent translation.
                   Unknown words pass through unchanged (marked with *).

  --backend hf     Real neural translation using a Hiligaynon LLM from
                   RESOURCES.md (e.g. welyjesch/lfm25-sft-hiligaynon or
                   PLTAT/hiligaynon_llama_3.1_finetuned_lora). Needs:
                       pip install transformers torch
                   and downloads the model on first run (GPU recommended).

The dict backend exists so the feature is demonstrable immediately; swap to hf
for quality once a model is installed.

Usage:
    python scripts/translate_hil.py "Good morning, how are you?"
    python scripts/translate_hil.py --backend hf --model welyjesch/lfm25-sft-hiligaynon \
        "I went to the market yesterday"
"""

import argparse
import re
import sys

# ---------------------------------------------------------------------------
# Offline starter lexicon (en/tl -> hil). Small, illustrative, EXTEND freely.
# Keys are lowercase. This is a demo aid, not a real MT system.
# ---------------------------------------------------------------------------
LEXICON = {
    # greetings / courtesy
    "good": "maayo", "morning": "aga", "afternoon": "hapon", "evening": "gab-i",
    "hello": "kamusta", "thank": "salamat", "thanks": "salamat", "you": "ikaw",
    "please": "palihog", "sorry": "pasaylo", "yes": "huo", "no": "indi",
    # pronouns
    "i": "ako", "me": "ako", "we": "kami", "they": "sila", "he": "siya",
    "she": "siya", "my": "akon", "your": "imo",
    # common verbs
    "go": "kadto", "went": "nagkadto", "eat": "kaon", "ate": "nagkaon",
    "drink": "inom", "sleep": "tulog", "come": "kari", "see": "kita",
    "want": "gusto", "love": "palangga", "know": "kabalo", "buy": "bakal",
    "have": "may", "are": "", "is": "", "am": "", "was": "", "do": "",
    # places / nouns
    "market": "merkado", "house": "balay", "home": "balay", "school": "eskwelahan",
    "water": "tubig", "food": "pagkaon", "road": "dalan", "street": "dalan",
    "money": "kwarta", "friend": "abyan", "child": "bata", "person": "tawo",
    "day": "adlaw", "night": "gab-i", "today": "subong", "tomorrow": "buas",
    "yesterday": "kahapon",
    # adjectives / misc
    "big": "daku", "small": "gamay", "many": "damo", "beautiful": "matahum",
    "happy": "malipayon", "hungry": "gutom", "tired": "kapoy", "hot": "init",
    "cold": "lamig", "fast": "madasig", "slow": "mahinay", "how": "paano",
    "what": "ano", "where": "diin", "who": "sin-o", "when": "san-o",
    "and": "kag", "the": "", "a": "", "to": "sa", "in": "sa", "at": "sa",
    "of": "sang", "very": "tama",
    # Tagalog -> Hiligaynon (a few high-frequency)
    "salamat": "salamat", "kumusta": "kamusta", "ako": "ako",
    "gusto": "gusto", "bahay": "balay", "tubig": "tubig", "pera": "kwarta",
    "kanin": "kan-on", "umaga": "aga", "gabi": "gab-i", "ngayon": "subong",
    "bukas": "buas", "kahapon": "kahapon", "saan": "diin", "ano": "ano",
}


def translate_dict(text):
    """Word-by-word lookup. Unknown words kept as *word*. Demo only."""
    out = []
    for raw in text.split():
        m = re.match(r"^(\W*)(.*?)(\W*)$", raw)
        lead, core, trail = m.group(1), m.group(2), m.group(3)
        key = core.lower()
        if key in LEXICON:
            hil = LEXICON[key]
            if not hil:  # mapped to empty (function word dropped)
                continue
            # preserve capitalization of first letter
            if core[:1].isupper():
                hil = hil[:1].upper() + hil[1:]
            out.append(f"{lead}{hil}{trail}")
        else:
            out.append(f"{lead}*{core}*{trail}")  # untranslated marker
    return " ".join(out)


def translate_hf(text, model_name):
    """Neural translation via a Hiligaynon instruct LLM (transformers)."""
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch  # noqa: F401
    except ImportError:
        sys.exit("transformers/torch not installed. Run:\n"
                 "  pip install transformers torch\n"
                 "Then re-run with --backend hf, or use --backend dict (no deps).")

    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    prompt = (
        "Translate the following text into Hiligaynon (Ilonggo). "
        "Reply with only the Hiligaynon translation.\n\n"
        f"Text: {text}\nHiligaynon:"
    )
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=128, do_sample=False)
    text_out = tok.decode(out[0], skip_special_tokens=True)
    # Return only the part after the last "Hiligaynon:" marker.
    return text_out.split("Hiligaynon:")[-1].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="+", help="English/Tagalog text to translate")
    ap.add_argument("--backend", choices=["dict", "hf"], default="dict")
    ap.add_argument("--model", default="welyjesch/lfm25-sft-hiligaynon",
                    help="HF model id for --backend hf (see RESOURCES.md)")
    args = ap.parse_args()

    text = " ".join(args.text)
    if args.backend == "hf":
        result = translate_hf(text, args.model)
    else:
        result = translate_dict(text)

    print(result)
    if args.backend == "dict":
        print("\n(dict backend: word-by-word demo. *word* = no entry yet. "
              "Use --backend hf for real translation.)", file=sys.stderr)


if __name__ == "__main__":
    main()
