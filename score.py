#!/usr/bin/env python3
"""
score.py — Code-switched ASR evaluation for Sugidanon.

Computes Word Error Rate (WER) overall, and broken down into:
  - switch-region words  (within +/-1 token of a language switch point)
  - monolingual words    (everything else)

Also reports a per-pair breakdown of the switch penalty across the three
languages in the benchmark: hil<->tl, hil<->en, tl<->en.

No external dependencies. Pure standard library (Python 3.8+).

Usage:
    python score.py --ref data/annotations --hyp data/predictions
    python score.py --ref data/annotations/hil_en_001.json \
                    --hyp data/predictions/hil_en_001.json
"""

import argparse
import json
import os
import random
import re
import sys


# ---------------------------------------------------------------------------
# Text handling
# ---------------------------------------------------------------------------

def normalize(word):
    """Lowercase and strip punctuation for fair comparison."""
    word = word.lower().strip()
    word = re.sub(r"[^\w'\-]", "", word)
    return word


def load_reference(path):
    """Return (tokens, langs) from a gold annotation file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    tokens = [normalize(t["text"]) for t in data["tokens"]]
    langs = [t.get("lang", "other") for t in data["tokens"]]
    return tokens, langs


def load_hypothesis(path):
    """
    Return a list of predicted tokens.
    Accepts either the same token format, or {"text": "full transcript"}.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if "tokens" in data:
        return [normalize(t["text"]) for t in data["tokens"]]
    if "text" in data:
        return [normalize(w) for w in data["text"].split()]
    raise ValueError(f"{path}: expected 'tokens' or 'text' field")


# ---------------------------------------------------------------------------
# Switch-point detection
# ---------------------------------------------------------------------------

def switch_region_flags(langs, window=1):
    """
    Return a list of booleans, one per reference token.
    True  = token is in a switch region (within +/-window of a switch point).
    A switch point is a position where lang[i] != lang[i-1], ignoring 'other'.
    """
    n = len(langs)
    is_switch_point = [False] * n
    prev = None
    for i, lg in enumerate(langs):
        if lg == "other":
            continue
        if prev is not None and lg != prev:
            is_switch_point[i] = True
        prev = lg

    in_region = [False] * n
    for i, sp in enumerate(is_switch_point):
        if sp:
            for j in range(max(0, i - window), min(n, i + window + 1)):
                in_region[j] = True
    return in_region


def switch_pairs(langs):
    """
    Return a list of (i, pair) for each switch point, where pair is a frozenset
    like {"hil", "tl"} identifying the two languages involved in the switch.
    Used for the per-pair breakdown. Ignores 'other'.
    """
    pairs = []
    prev = None
    for i, lg in enumerate(langs):
        if lg == "other":
            continue
        if prev is not None and lg != prev:
            pairs.append((i, frozenset((prev, lg))))
        prev = lg
    return pairs


# ---------------------------------------------------------------------------
# Alignment (Levenshtein with backtrace) to attribute errors to ref tokens
# ---------------------------------------------------------------------------

def align(ref, hyp):
    """
    Standard word-level edit-distance alignment.
    Returns a list of operations: ("ok"|"sub"|"del"|"ins", ref_idx_or_None).
    ref_idx lets us attribute each error to a reference token (and its region).
    """
    n, m = len(ref), len(hyp)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # deletion
                dp[i][j - 1] + 1,        # insertion
                dp[i - 1][j - 1] + cost  # match / substitution
            )

    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref[i - 1] == hyp[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            ops.append(("ok", i - 1)); i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("sub", i - 1)); i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("del", i - 1)); i -= 1
        else:
            ops.append(("ins", None)); j -= 1
    ops.reverse()
    return ops


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

class Counts:
    def __init__(self):
        self.errors = 0   # sub + del + ins attributed here
        self.words = 0    # reference words in this bucket

    def wer(self):
        return (self.errors / self.words) if self.words else 0.0


PAIR_LABELS = {
    frozenset(("hil", "tl")): "hil<->tl",
    frozenset(("hil", "en")): "hil<->en",
    frozenset(("tl", "en")):  "tl<->en",
}


def score_clip(ref, langs, hyp, pair_buckets):
    """
    Score one clip. Mutates pair_buckets (dict pair_label -> Counts) in place so
    per-pair switch-region WER aggregates across the corpus.
    Returns (overall, switch, mono) Counts for this clip.
    """
    region = switch_region_flags(langs)
    overall, switch, mono = Counts(), Counts(), Counts()
    overall.words = len(ref)
    for in_switch in region:
        (switch if in_switch else mono).words += 1

    # Per-pair word counts: a switch-region token belongs to the pair(s) of the
    # switch point(s) it sits within +/-1 of.
    pair_of_token = [set() for _ in ref]
    for idx, pair in switch_pairs(langs):
        label = PAIR_LABELS.get(pair)
        if label is None:
            continue
        for j in range(max(0, idx - 1), min(len(ref), idx + 2)):
            pair_of_token[j].add(label)
    for j, labels in enumerate(pair_of_token):
        for label in labels:
            pair_buckets.setdefault(label, Counts()).words += 1

    for op, ridx in align(ref, hyp):
        if op == "ok":
            continue
        if op == "ins":
            # Insertion has no reference token to attribute to a region/pair,
            # so it is charged to the overall WER only.
            overall.errors += 1
            continue
        # sub or del -> attributable to a reference token
        overall.errors += 1
        if region[ridx]:
            switch.errors += 1
            for label in pair_of_token[ridx]:
                pair_buckets[label].errors += 1
        else:
            mono.errors += 1
    return overall, switch, mono


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals (clip-level resampling)
# ---------------------------------------------------------------------------

def bootstrap_ci(per_clip, key, resamples=2000, seed=1234, alpha=0.05):
    """
    Clip-level bootstrap 95% CI for a WER bucket.

    per_clip: list of dicts with (errors, words) per bucket key.
    key: bucket name, e.g. "overall" / "switch" / "mono".
    Resamples whole clips with replacement so the interval reflects
    between-clip variance, which is what matters for a small test set.
    Returns (low, high) as fractions, or None if the bucket has no words.
    """
    items = [(c[key][0], c[key][1]) for c in per_clip]
    if sum(w for _, w in items) == 0:
        return None
    rng = random.Random(seed)
    n = len(items)
    wers = []
    for _ in range(resamples):
        e = w = 0
        for _ in range(n):
            de, dw = items[rng.randrange(n)]
            e += de
            w += dw
        if w:
            wers.append(e / w)
    if not wers:
        return None
    wers.sort()
    lo = wers[int((alpha / 2) * len(wers))]
    hi = wers[min(len(wers) - 1, int((1 - alpha / 2) * len(wers)))]
    return lo, hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True, help="annotation file or directory")
    ap.add_argument("--hyp", required=True, help="prediction file or directory")
    ap.add_argument("--ci", action="store_true",
                    help="report 95%% bootstrap confidence intervals")
    ap.add_argument("--resamples", type=int, default=2000,
                    help="bootstrap resamples for --ci (default 2000)")
    args = ap.parse_args()

    pairs = []
    if os.path.isdir(args.ref):
        for fn in sorted(os.listdir(args.ref)):
            if fn.endswith(".json"):
                hp = os.path.join(args.hyp, fn)
                if os.path.exists(hp):
                    pairs.append((os.path.join(args.ref, fn), hp))
    else:
        pairs.append((args.ref, args.hyp))

    if not pairs:
        sys.exit("No matching ref/hyp pairs found.")

    tot_o, tot_s, tot_m = Counts(), Counts(), Counts()
    pair_buckets = {}
    per_clip = []
    print(f"{'clip':<16}{'overall':>10}{'switch':>10}{'mono':>10}")
    print("-" * 46)
    for ref_path, hyp_path in pairs:
        ref, langs = load_reference(ref_path)
        hyp = load_hypothesis(hyp_path)
        o, s, m = score_clip(ref, langs, hyp, pair_buckets)
        for agg, one in ((tot_o, o), (tot_s, s), (tot_m, m)):
            agg.errors += one.errors
            agg.words += one.words
        per_clip.append({
            "overall": (o.errors, o.words),
            "switch": (s.errors, s.words),
            "mono": (m.errors, m.words),
        })
        cid = os.path.splitext(os.path.basename(ref_path))[0]
        print(f"{cid:<16}{o.wer():>9.1%}{s.wer():>10.1%}{m.wer():>10.1%}")

    print("-" * 46)
    print(f"{'CORPUS':<16}{tot_o.wer():>9.1%}{tot_s.wer():>10.1%}{tot_m.wer():>10.1%}")
    print()
    print(f"Overall WER       : {tot_o.wer():.1%}  ({tot_o.errors}/{tot_o.words})")
    print(f"Switch-region WER : {tot_s.wer():.1%}  ({tot_s.errors}/{tot_s.words})")
    print(f"Monolingual WER   : {tot_m.wer():.1%}  ({tot_m.errors}/{tot_m.words})")
    if tot_m.words:
        gap = tot_s.wer() - tot_m.wer()
        print(f"Switch penalty    : {gap:+.1%} (switch WER minus monolingual WER)")

    if args.ci:
        print()
        print(f"95% bootstrap CIs ({args.resamples} clip-level resamples):")
        for label, key in (("Overall", "overall"),
                           ("Switch-region", "switch"),
                           ("Monolingual", "mono")):
            ci = bootstrap_ci(per_clip, key, resamples=args.resamples)
            if ci:
                print(f"  {label:<14}: [{ci[0]:.1%}, {ci[1]:.1%}]")

    # Per-pair switch-region WER breakdown.
    if pair_buckets:
        print()
        print("Switch-region WER by language pair:")
        for label in ("hil<->tl", "hil<->en", "tl<->en"):
            c = pair_buckets.get(label)
            if c and c.words:
                print(f"  {label:<10}: {c.wer():.1%}  ({c.errors}/{c.words})")


if __name__ == "__main__":
    main()
