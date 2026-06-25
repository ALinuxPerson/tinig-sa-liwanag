#!/usr/bin/env python3
"""
Evaluate Hiligaynon text translation predictions against a JSONL benchmark.

The metrics are intentionally lightweight and dependency-free:
  - coverage
  - exact match after normalization
  - token F1
  - chrF-style character n-gram F-score

These metrics do not replace human review. They make baseline comparisons
reproducible while the team builds a reviewed benchmark.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {e}") from e
    return rows


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s'-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def token_f1(reference, prediction):
    ref_tokens = normalize(reference).split()
    pred_tokens = normalize(prediction).split()
    if not ref_tokens and not pred_tokens:
        return 1.0
    if not ref_tokens or not pred_tokens:
        return 0.0
    ref_counts = Counter(ref_tokens)
    pred_counts = Counter(pred_tokens)
    overlap = sum((ref_counts & pred_counts).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_tokens)
    recall = overlap / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)


def char_ngrams(text, n):
    text = " " + normalize(text) + " "
    if len(text) < n:
        return Counter()
    return Counter(text[i:i + n] for i in range(len(text) - n + 1))


def chrf(reference, prediction, max_n=6, beta=2.0):
    scores = []
    beta2 = beta * beta
    for n in range(1, max_n + 1):
        ref = char_ngrams(reference, n)
        pred = char_ngrams(prediction, n)
        if not ref and not pred:
            scores.append(1.0)
            continue
        if not ref or not pred:
            scores.append(0.0)
            continue
        overlap = sum((ref & pred).values())
        precision = overlap / sum(pred.values()) if pred else 0.0
        recall = overlap / sum(ref.values()) if ref else 0.0
        if precision == 0.0 and recall == 0.0:
            scores.append(0.0)
        else:
            scores.append((1 + beta2) * precision * recall / (beta2 * precision + recall))
    return sum(scores) / len(scores)


def pct(value):
    return f"{value * 100:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", required=True, help="benchmark JSONL file")
    ap.add_argument("--preds", required=True, help="prediction JSONL file")
    args = ap.parse_args()

    refs = read_jsonl(args.refs)
    preds = read_jsonl(args.preds)

    ref_by_id = {row["id"]: row for row in refs}
    pred_by_id = {}
    for row in preds:
        rid = row.get("id")
        if rid in pred_by_id:
            sys.exit(f"duplicate prediction id: {rid}")
        pred_by_id[rid] = row

    if not refs:
        sys.exit("No reference rows found.")

    rows = []
    missing = []
    domain_scores = defaultdict(list)

    for ref in refs:
        rid = ref["id"]
        pred = pred_by_id.get(rid)
        if not pred:
            missing.append(rid)
            continue
        reference = ref["reference_translation"]
        prediction = pred.get("prediction", "")
        exact = normalize(reference) == normalize(prediction)
        tf1 = token_f1(reference, prediction)
        cf = chrf(reference, prediction)
        rows.append((rid, ref.get("domain", "unknown"), exact, tf1, cf))
        domain_scores[ref.get("domain", "unknown")].append((exact, tf1, cf))

    covered = len(rows)
    coverage = covered / len(refs)
    exact_avg = sum(1 for _, _, exact, _, _ in rows if exact) / covered if covered else 0.0
    tf1_avg = sum(row[3] for row in rows) / covered if covered else 0.0
    chrf_avg = sum(row[4] for row in rows) / covered if covered else 0.0

    print(f"References : {len(refs)}")
    print(f"Predictions: {len(preds)}")
    print(f"Coverage   : {pct(coverage)} ({covered}/{len(refs)})")
    print(f"Exact match: {pct(exact_avg)}")
    print(f"Token F1   : {pct(tf1_avg)}")
    print(f"chrF       : {pct(chrf_avg)}")

    if missing:
        print()
        print("Missing predictions:")
        for rid in missing:
            print(f"  {rid}")

    print()
    print(f"{'id':<16}{'domain':<16}{'exact':>8}{'token_f1':>12}{'chrf':>10}")
    print("-" * 62)
    for rid, domain, exact, tf1, cf in rows:
        print(f"{rid:<16}{domain:<16}{str(exact):>8}{pct(tf1):>12}{pct(cf):>10}")

    if domain_scores:
        print()
        print("By domain:")
        for domain in sorted(domain_scores):
            vals = domain_scores[domain]
            d_exact = sum(1 for exact, _, _ in vals if exact) / len(vals)
            d_tf1 = sum(tf1 for _, tf1, _ in vals) / len(vals)
            d_chrf = sum(cf for _, _, cf in vals) / len(vals)
            print(f"  {domain:<16} exact={pct(d_exact)} token_f1={pct(d_tf1)} chrf={pct(d_chrf)}")


if __name__ == "__main__":
    main()
