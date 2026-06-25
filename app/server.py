#!/usr/bin/env python3
"""
server.py - Local Hiligaynon translation baseline demo.

Two-pane UI for English / Filipino / code-switched input into Hiligaynon output.
Runs on the Python standard library only with the offline dictionary backend.
If transformers + a Hiligaynon LLM are installed, start with --backend hf for a
neural baseline.

Usage:
    python3 app/server.py                 # dict backend, http://127.0.0.1:8000
    python3 app/server.py --port 5000
    python3 app/server.py --backend hf --model welyjesch/lfm25-sft-hiligaynon

Then open the printed URL in your browser.
"""

import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Import the translation logic from scripts/translate_hil.py.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import translate_hil  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# Filled in main() based on --backend.
_BACKEND = "dict"
_MODEL = None
_HF_READY = False


def do_translate(text):
    text = text.strip()
    if not text:
        return ""
    if _BACKEND == "hf" and _HF_READY:
        return translate_hil.translate_hf(text, _MODEL)
    return translate_hil.translate_dict(text)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
                self._send(200, f.read())
        elif self.path == "/api/status":
            self._send(200, json.dumps({
                "backend": _BACKEND,
                "model": _MODEL if (_BACKEND == "hf" and _HF_READY) else None,
            }), "application/json")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/translate":
            self._send(404, "not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = do_translate(payload.get("text", ""))
            self._send(200, json.dumps({"translation": result}),
                       "application/json")
        except Exception as e:
            self._send(500, json.dumps({"error": str(e)}), "application/json")

    def log_message(self, *args):
        pass  # quiet


def main():
    global _BACKEND, _MODEL, _HF_READY
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--backend", choices=["dict", "hf"], default="dict")
    ap.add_argument("--model", default="welyjesch/lfm25-sft-hiligaynon")
    ap.add_argument("--lexicon", default=os.path.join(ROOT, "data", "lexicon_hil.tsv"))
    args = ap.parse_args()

    # Auto-generated dictionary first, hand-curated file on top (manual wins).
    auto = os.path.join(os.path.dirname(args.lexicon), "lexicon_hil_auto.tsv")
    na = translate_hil.load_lexicon_file(auto)
    n = translate_hil.load_lexicon_file(args.lexicon)
    print(f"Loaded {na} auto + {n} curated lexicon entries.")

    _BACKEND = args.backend
    _MODEL = args.model
    if args.backend == "hf":
        print(f"Warming up neural model {args.model} (first run downloads it)...")
        try:
            translate_hil.translate_hf("test", args.model)
            _HF_READY = True
            print("Neural backend ready.")
        except SystemExit as e:
            print(e)
            print("Falling back to dictionary backend.")
            _BACKEND = "dict"

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"\nHiligaynon translation demo running:  http://{args.host}:{args.port}")
    print(f"Backend: {_BACKEND}.  Press Ctrl+C to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")


if __name__ == "__main__":
    main()
