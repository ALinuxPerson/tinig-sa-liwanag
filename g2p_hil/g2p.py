#!/usr/bin/env python3
"""
g2p.py — Hiligaynon grapheme-to-phoneme (G2P) rules.

The novel linguistic piece of Sugidanon's TTS path. Hiligaynon orthography is
highly phonemic, so a small ordered rule set covers most of the language. Output
is a space-separated IPA-ish phoneme string usable by a phoneme-input TTS.

Pure standard library. Owned/extended by the team's linguists.

Phoneme inventory (Hiligaynon):
  vowels:     a e i o u   (e/o mostly in loanwords; i~e and u~o often merge)
  consonants: p b t d k g ʔ m n ŋ s h l r w j

Usage:
    python g2p_hil/g2p.py "Maayong aga sa imo"
    >>> m a ʔ a j o ŋ   ʔ a g a   s a   ʔ i m o
"""

import re
import sys

# Ordered digraphs / multigraphs first, then single letters.
# Each rule maps a lowercased grapheme chunk to one or more phonemes.
RULES = [
    ("ng", "ŋ"),   # velar nasal, written as a digraph
    ("ts", "ts"),  # loan cluster
    ("ch", "tʃ"),  # loan
    ("ll", "l j"), # rare loan (Spanish-derived names)
    ("a", "a"),
    ("e", "e"),
    ("i", "i"),
    ("o", "o"),
    ("u", "u"),
    ("b", "b"),
    ("c", "k"),    # loanwords; native HIL uses k
    ("d", "d"),
    ("f", "p"),    # nativized: f -> p
    ("g", "g"),
    ("h", "h"),
    ("j", "dʒ"),   # loan; native 'y' glide handled below
    ("k", "k"),
    ("l", "l"),
    ("m", "m"),
    ("n", "n"),
    ("p", "p"),
    ("q", "k"),
    ("r", "r"),
    ("s", "s"),
    ("t", "t"),
    ("v", "b"),    # nativized: v -> b
    ("w", "w"),
    ("x", "k s"),
    ("y", "j"),
    ("z", "s"),
    ("'", "ʔ"),    # explicit glottal stop marker
    ("-", "ʔ"),    # hyphen in HIL often marks a glottal stop (nag-grocery)
]

VOWELS = set("aeiou")


def g2p(word):
    """
    Convert one Hiligaynon word to a space-separated phoneme string.
    Inserts a glottal stop /ʔ/ before a word-initial vowel and between
    adjacent vowels (Hiligaynon has no true vowel hiatus).
    """
    w = word.lower().strip()
    w = re.sub(r"[^\w'\-]", "", w)
    if not w:
        return ""

    phonemes = []
    i = 0
    prev_was_vowel = False
    at_word_start = True
    while i < len(w):
        matched = None
        for graph, phon in RULES:
            if w.startswith(graph, i):
                matched = (graph, phon)
                break
        if matched is None:
            i += 1
            continue
        graph, phon = matched
        is_vowel = graph in VOWELS

        # Glottal stop insertion: word-initial vowel, or vowel after vowel.
        if is_vowel and (at_word_start or prev_was_vowel):
            phonemes.append("ʔ")

        phonemes.extend(phon.split())
        prev_was_vowel = is_vowel
        at_word_start = False
        i += len(graph)

    return " ".join(phonemes)


def g2p_sentence(text):
    """Convert a sentence; words separated by '  |  ' for clarity."""
    return "  |  ".join(g2p(w) for w in text.split())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Smoke test with known words.
        for w in ["Maayong", "aga", "imo", "Nag-grocery", "balay"]:
            print(f"{w:<14} -> {g2p(w)}")
    else:
        print(g2p_sentence(" ".join(sys.argv[1:])))
