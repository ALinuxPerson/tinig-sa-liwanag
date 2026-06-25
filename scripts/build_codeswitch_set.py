#!/usr/bin/env python3
"""
build_codeswitch_set.py — Emit code-switch-labeled gold annotation stubs.

Source of truth is the 40-sentence elicitation set below: natural Hiligaynon /
Tagalog / English code-switch utterances across 8 domains, authored as a draft
and then REVIEWED by a Hiligaynon speaker. The speaker also records audio for
each (data/audio/hil_cs_NNN.wav).

Each sentence carries a clause-level switch type ([HIL], [HIL+EN], [HIL+TL],
[HIL+TL+EN]). The benchmark scorer (score.py) needs PER-WORD language tags, so
this script auto-drafts token-level hil/tl/en tags from explicit EN/TL word
lists plus a Hiligaynon-affix rule. Those per-word tags are SEED values
(`lang_tags_status: seed_unverified`) — the recording speaker confirms/corrects
them. The reference TEXT is `reviewed` because the speaker vetted the sentences;
only the auto per-word tagging still needs a confirmation pass (AI_DISCLOSURE.md).

Pure standard library.

Usage:
    python3 scripts/build_codeswitch_set.py
    python3 scripts/build_codeswitch_set.py --out-dir data/annotations
"""

import argparse
import json
import os

# (domain, switch_type, text). switch_type is the speaker's clause-level label.
SENTENCES = [
    # 1. Market / Palengke
    ("market", "HIL+EN", "Pila ang grocery budget naton para sa weekend?"),
    ("market", "HIL+TL", "Magbakal ta sang isda kay mura-mura pa siya kanina."),
    ("market", "HIL+TL", "Nag-discount gali ang tindahan, kaya bumili na lang tayo ng marami."),
    ("market", "HIL", "Tama na ina nga bugas, indi na magdugang."),
    ("market", "HIL+EN", "Wala na sang change ang vendor, so pabayloan ta sang bente."),
    # 2. Transport / Jeepney
    ("transport", "HIL+EN", "Pwede ko mag-drop off sa may corner sang highway?"),
    ("transport", "HIL+TL", "Sakay na tayo kay ma-late pa ako sa trabaho."),
    ("transport", "HIL+EN", "Traffic gid subong, kaya mag-grab na lang ako para mas mabakas."),
    ("transport", "HIL+EN", "Diin ka manaog, sa eskina ukon sa terminal?"),
    ("transport", "HIL+EN", "Bayad lang anay, kulang pa ang fare mo sang tatlo ka pesos."),
    # 3. School / Work
    ("school_work", "HIL+EN", "Indi ko ma-submit ang assignment kay slow ang wifi namon."),
    ("school_work", "HIL+TL+EN", "May meeting kami sa Monday, tapos may deadline pa sang report."),
    ("school_work", "HIL+TL", "Nahirapan ako sa exam kahapon, grabe ka-budlay."),
    ("school_work", "HIL+EN", "Naka-pasar ka na sa subject mo? Congrats, abi!"),
    ("school_work", "HIL", "Ginahimo ko pa ang akon project para sa klase."),
    # 4. Family / Home
    ("family", "HIL", "Kaon na kita kay handa na ang sud-an ni Nanay."),
    ("family", "HIL+EN", "Charge mo anay ang phone ko, lowbat na gid."),
    ("family", "HIL+TL+EN", "Lipat ko gali i-off ang aircon, kaya ang taas ng bill namin."),
    ("family", "HIL", "Diin gintago mo ang yabi sang puwertahan?"),
    ("family", "HIL+EN", "Mag-video call ta kay Manong nga naa sa abroad."),
    # 5. Health / Barangay
    ("health", "HIL+EN", "May appointment ako sa health center buwas sang aga."),
    ("health", "HIL+TL", "Masakit ang ulo ko kaya magpahinga muna ako."),
    ("health", "HIL+TL+EN", "May check-up kami sa clinic, tapos kailangan pa ng prescription."),
    ("health", "HIL", "Indi pagkalimti inom sang bulong sa adlaw-adlaw."),
    ("health", "HIL+EN", "Nag-register ka na sa barangay para sa vaccine?"),
    # 6. Culture / Festivals
    ("culture", "HIL+EN", "Excited gid ako sa Dinagyang festival sa sunod nga semana."),
    ("culture", "HIL+TL", "Sayaw na tayo kay nagsugod na ang parada."),
    ("culture", "HIL+TL+EN", "Ang ganda ng costumes, perfect para sa photo namon!"),
    ("culture", "HIL", "Daku gid ang kasadya sang mga tawo sa plaza."),
    ("culture", "HIL+EN", "Mag-meet ta sa booth pagkatapos sang performance."),
    # 7. Everyday / Spontaneous
    ("everyday", "HIL+EN", "Sige, text mo na lang ako kung diin kita magkita."),
    ("everyday", "HIL+TL+EN", "Ambot ah, basta i-message mo na lang sa group chat namin."),
    ("everyday", "HIL", "Wala lang, ginatamad ako maglakat subong."),
    ("everyday", "HIL", "Salamat gid sa imo bulig kahapon, ginapasalamatan ko ina."),
    ("everyday", "HIL+EN", "Okay lang na, next time na lang ta mag-hangout."),
    # 8. Oral tradition / Heritage
    ("oral_tradition", "HIL", "Ang sugidanon amo ang aton mga pamatan-on nga sugilanon halin sang una."),
    ("oral_tradition", "HIL", "Ginasaysay sang aton mga katigulangan ang mga estorya paagi sa pag-amba."),
    ("oral_tradition", "HIL+EN", "Importante gid i-preserve ang aton culture para sa palaabuton."),
    ("oral_tradition", "HIL", "Madamo nga hurobaton kag paktakon ang nadula na sa karon nga henerasyon."),
    ("oral_tradition", "HIL+TL", "Dapat ituro natin sa mga bata ang aton lenguahe kag tradisyon."),
]

# Bare English tokens (lowercased). Hil-affixed English roots (mag-grab, i-off)
# are tagged hil by the affix rule below, matching the matrix language.
EN_WORDS = {
    "grocery", "budget", "weekend", "change", "vendor", "so", "corner", "highway",
    "traffic", "fare", "assignment", "slow", "wifi", "meeting", "monday", "deadline",
    "report", "congrats", "phone", "lowbat", "aircon", "bill", "video", "call",
    "appointment", "health", "center", "check-up", "clinic", "prescription", "vaccine",
    "excited", "festival", "costumes", "perfect", "photo", "text", "group", "chat",
    "okay", "next", "time", "culture", "booth", "performance", "subject", "abroad",
    "off", "terminal",
}

# Tagalog-specific tokens (distinct from the Hiligaynon equivalent). Words shared
# between Tagalog and Hiligaynon are left as hil; the speaker confirms edge cases.
TL_WORDS = {
    "tayo", "ng", "bumili", "marami", "mura-mura", "kanina", "tapos", "kailangan",
    "namin", "nahirapan", "muna", "magpahinga", "sayaw", "ganda", "ituro", "natin",
}

# Hiligaynon verbal/aspect affixes. A hyphenated token whose prefix is one of
# these is the matrix language (hil), even with an English/Tagalog root.
HIL_AFFIXES = ("nag", "mag", "ma", "naka", "gina", "i", "ka", "pa", "na")

PROVENANCE = {
    "source": "Team Hague elicitation set (draft, reviewed by a Hiligaynon speaker)",
    "license": "CC BY 4.0 (text); audio recorded by the reviewing speaker",
    "note": "Reference text reviewed. Per-word lang tags are AUTO-SEEDED — speaker confirms (SCHEMA.md).",
}


def normalize(tok):
    return tok.strip(".,!?;:\"'()").lower()


def tag_token(raw):
    """Best-effort per-word language tag. SEED — needs speaker confirmation."""
    word = normalize(raw)
    if not word:
        return "hil"
    if "-" in word:
        prefix = word.split("-", 1)[0]
        if prefix in HIL_AFFIXES:
            return "hil"
        if word in EN_WORDS:
            return "en"
        if word in TL_WORDS:
            return "tl"
        return "hil"  # reduplication / native compounds (adlaw-adlaw, sud-an)
    if word in EN_WORDS:
        return "en"
    if word in TL_WORDS:
        return "tl"
    return "hil"


def tag_tokens(text):
    """Return [(token, lang), ...] for one sentence."""
    out = []
    for i, raw in enumerate(text.split()):
        out.append((raw.strip(".,!?;:\"'()"), tag_token(raw)))
    return [(t, lg) for t, lg in out if t]


def make_annotation(clip_id, domain, switch_type, text, duration=None):
    toks = tag_tokens(text)
    return {
        "clip_id": clip_id,
        "audio_file": f"audio/{clip_id}.wav",
        "duration_sec": duration,
        "domain": domain,
        "switch_type": switch_type,
        "transcript": text,
        "speaker": {"id": "spk01", "primary_language": "hil",
                    "region": "", "age_band": "", "gender": ""},
        "matrix_language": "hil",
        "review_status": "reviewed",            # text vetted by a Hiligaynon speaker
        "lang_tags_status": "seed_unverified",  # per-word tags auto-seeded, pending confirmation
        "provenance": PROVENANCE,
        "tokens": [{"idx": i, "text": t, "lang": lg}
                   for i, (t, lg) in enumerate(toks)],
    }


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for n, (domain, switch_type, text) in enumerate(SENTENCES, 1):
        clip_id = f"hil_cs_{n:03d}"
        ann = make_annotation(clip_id, domain, switch_type, text)
        with open(os.path.join(out_dir, f"{clip_id}.json"), "w", encoding="utf-8") as f:
            json.dump(ann, f, ensure_ascii=False, indent=2)
        written.append((clip_id, switch_type))
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="data/annotations")
    args = ap.parse_args()
    written = build(args.out_dir)
    print(f"Wrote {len(written)} code-switch annotations to {args.out_dir}.")
    counts = {}
    for _, st in written:
        counts[st] = counts.get(st, 0) + 1
    print("By switch type:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print()
    print("Reference text is reviewed. Per-word lang tags are auto-seeded — the")
    print("recording speaker confirms them (SCHEMA.md, AI_DISCLOSURE.md).")
    print("Capture audio per clip with scripts/record.py (see docs/recording_kit.md).")


if __name__ == "__main__":
    main()
