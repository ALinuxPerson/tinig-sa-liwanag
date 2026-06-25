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
    # scripts 2 & 3
    "total", "deliver", "order", "stop", "office", "book", "ride", "exact", "driver",
    "email", "sir", "presentation", "quiz", "interview", "laptop", "battery", "message",
    "schedule", "dentist", "friday", "record", "highlights", "october", "vlog",
    "fireworks", "send", "week", "document", "future", "stock", "gcash", "shed",
    "tricycle", "mall", "pass", "requirements", "enrollment", "overtime", "internet",
    "promoted", "tv", "arrange", "baby", "follow-up", "checkup", "blood", "pressure",
    "maintenance", "booster", "costume", "competition", "crowd", "energy", "stage",
    "awards", "ready", "hang", "out", "fade", "memory", "good", "luck", "deal",
}

# Tagalog-specific tokens (distinct from the Hiligaynon equivalent). Words shared
# between Tagalog and Hiligaynon are left as hil; the speaker confirms edge cases.
TL_WORDS = {
    "tayo", "ng", "bumili", "marami", "mura-mura", "kanina", "tapos", "kailangan",
    "namin", "nahirapan", "muna", "magpahinga", "sayaw", "ganda", "ituro", "natin",
    # scripts 2 & 3
    "tumawad", "medyo", "mahal", "tingnan", "sariwa", "gulay", "bilis", "baka",
    "maiwan", "byahe", "hirap", "sumakit", "tiyan", "uminom", "manood", "ewan", "ba",
    "tinatamad", "ipasa", "kabataan", "pinulongan", "kain", "bago", "maglakad",
    "punasan", "masama", "pakiramdam", "saglit", "habang", "tumutugtog", "saya",
    "hindi", "alam", "eh", "pagod", "buong", "araw", "nagtrabaho", "nating",
    "kahalagahan", "madali", "umalis", "papuntang", "mag-aral", "mabagal", "bahay",
    "bibili", "daw",
}

# Hiligaynon verbal/aspect affixes. A hyphenated token whose prefix is one of
# these is the matrix language (hil), even with an English/Tagalog root.
HIL_AFFIXES = ("nag", "mag", "ma", "naka", "gina", "i", "ka", "pa", "na")

# Script 2 — docs/recording_script_2.md (clip IDs hil_cs_041..080).
SENTENCES_2 = [
    ("market", "HIL+EN", "Tag-pila ang kilo sang manok subong sa market?"),
    ("market", "HIL+TL", "Tumawad ka anay kay medyo mahal ang prutas."),
    ("market", "HIL+TL+EN", "Out of stock na ang suka, kaya bumili na lang tayo ng iba."),
    ("market", "HIL", "Indi malimti dad-on ang sako para sa bugas."),
    ("market", "HIL+EN", "Pwede mo i-deliver ang order namon buas?"),
    ("transport", "HIL+EN", "Para lang sa next nga stop, malapit lang ang office."),
    ("transport", "HIL+TL", "Bilis na tayo kay baka maiwan pa tayo sa byahe."),
    ("transport", "HIL+TL+EN", "Wala na sang jeep, kaya mag-book na lang tayo ng ride."),
    ("transport", "HIL", "Pila ka oras ang biyahe halin diri pa-Iloilo?"),
    ("transport", "HIL+EN", "Magbayad ka anay sang exact para indi mabudlayan ang driver."),
    ("school_work", "HIL+EN", "Na-submit mo na ang report sa email ni sir?"),
    ("school_work", "HIL+TL+EN", "May presentation kami bukas, tapos may quiz pa pagkatapos."),
    ("school_work", "HIL+TL", "Ang hirap sang module, indi ko ma-gets ang topic."),
    ("school_work", "HIL+EN", "Pasado ka na sa interview? Good luck sa imo, te!"),
    ("school_work", "HIL", "Ginabasa ko pa ang libro para sa report ko."),
    ("family", "HIL+TL", "Hugasi anay ang pinggan kay handa na ang pamahaw."),
    ("family", "HIL+EN", "I-charge mo ang laptop ko, mubo na ang battery."),
    ("family", "HIL+TL+EN", "Sarado mo ang gripo, baka tumaas pa ang water bill namin."),
    ("family", "HIL", "Diin mo ginbutang ang remote sang TV?"),
    ("family", "HIL+EN", "Mag-message ka kay Nanay nga late ta mag-uli."),
    ("health", "HIL+EN", "May schedule ako sa dentist sa Friday sang hapon."),
    ("health", "HIL+TL", "Sumakit ang tiyan ko kaya uminom ako ng gamot."),
    ("health", "HIL+TL+EN", "May fever ang bata, kaya kailangan na ng check-up."),
    ("health", "HIL", "Kinahanglan magpabakuna ang tanan nga bata sa barangay."),
    ("health", "HIL+EN", "Na-update mo na ang health record mo sa center?"),
    ("culture", "HIL+EN", "Excited ako sa MassKara highlights sa Bacolod sa October."),
    ("culture", "HIL+TL", "Tara na, manood tayo sang street dance sa plaza."),
    ("culture", "HIL+TL+EN", "Ang ganda ng lights, perfect para sa vlog namon!"),
    ("culture", "HIL", "Madamo gid nga bisita sa pista sang aton banwa."),
    ("culture", "HIL+EN", "Mag-meet ta sa entrance pagkatapos sang fireworks."),
    ("everyday", "HIL+EN", "Sige, chat mo lang ako kung tapos ka na."),
    ("everyday", "HIL+TL+EN", "Ewan ko ba, basta i-send mo na lang sa group natin."),
    ("everyday", "HIL+TL", "Wala lang, tinatamad ako maglabas subong nga adlaw."),
    ("everyday", "HIL", "Salamat gid sa imo pag-intindi sa akon kahapon."),
    ("everyday", "HIL+EN", "Okay lang, sa next week na lang ta mag-lakwatsa."),
    ("oral_tradition", "HIL", "Ang mga sugilanon sang aton kaapuhan dapat indi malipatan."),
    ("oral_tradition", "HIL", "Paagi sa komposo ginasaysay ang kasaysayan sang aton lugar."),
    ("oral_tradition", "HIL+EN", "Importante i-document ang aton mga tradisyon para sa future."),
    ("oral_tradition", "HIL", "Madamo nga binalaybay kag huni ang nagakawala subong."),
    ("oral_tradition", "HIL+TL", "Dapat ipasa natin sa mga kabataan ang aton pinulongan."),
]

# Script 3 — docs/recording_script_3.md (clip IDs hil_cs_081..120).
SENTENCES_3 = [
    ("market", "HIL+EN", "Pila ang total sang grocery namon nga tatlo ka bag?"),
    ("market", "HIL+TL", "Tingnan mo anay kung sariwa pa ang gulay."),
    ("market", "HIL+TL+EN", "Sale daw subong, kaya bibili ako ng marami para sa stock."),
    ("market", "HIL", "Indi pagbaklon ang hilaw nga prutas kay maaslom pa."),
    ("market", "HIL+EN", "Wala ka sang sukli? Pwede GCash na lang."),
    ("transport", "HIL+EN", "Mag-stop ka lang sa may waiting shed sa unahan."),
    ("transport", "HIL+TL", "Madali na tayo kay malapit nang umalis ang bus."),
    ("transport", "HIL+TL+EN", "Puno na ang tricycle, kaya mag-grab na lang tayo papuntang mall."),
    ("transport", "HIL", "San-o ka manaog, sa banwa ukon sa balay?"),
    ("transport", "HIL+EN", "Kuwarta lang anay, ihatag ko ang change mo dayon."),
    ("school_work", "HIL+EN", "Na-pass mo na ang requirements para sa enrollment?"),
    ("school_work", "HIL+TL+EN", "May overtime ako mamaya, tapos may meeting pa bukas ng umaga."),
    ("school_work", "HIL+TL", "Ang hirap mag-aral kung mabagal ang internet sa bahay."),
    ("school_work", "HIL+EN", "Promoted ka na? Congrats gid, deserve mo gid ina!"),
    ("school_work", "HIL", "Ginahuman ko pa ang akon assignment para sa klase buas."),
    ("family", "HIL+TL", "Kain na muna tayo bago maglakad pa-simbahan."),
    ("family", "HIL+EN", "I-off mo ang TV, time na para magtulog."),
    ("family", "HIL+TL+EN", "Punasan mo ang lamesa, tapos i-arrange mo ang gamit."),
    ("family", "HIL", "Diin nagkadto si Tatay kaina nga aga?"),
    ("family", "HIL+EN", "Mag-video call ta kay Lola para makita niya ang baby."),
    ("health", "HIL+EN", "May follow-up checkup ako sa ospital sunod nga semana."),
    ("health", "HIL+TL", "Masama ang pakiramdam ko, magpahinga muna ako saglit."),
    ("health", "HIL+TL+EN", "Mataas ang blood pressure ni Lolo, kaya kailangan ng maintenance."),
    ("health", "HIL", "Inom sang madamo nga tubig kon mainit ang panahon."),
    ("health", "HIL+EN", "Naka-pa-vaccine ka na sang booster sa health center?"),
    ("culture", "HIL+EN", "Ready na ang costume ko para sa Dinagyang competition."),
    ("culture", "HIL+TL", "Sayaw tayo sa kalye habang tumutugtog ang banda."),
    ("culture", "HIL+TL+EN", "Ang saya ng crowd, grabe ang energy sa festival!"),
    ("culture", "HIL", "Matahum gid ang mga karosa sa parada sang pista."),
    ("culture", "HIL+EN", "Mag-tipon ta sa stage pagkatapos sang awards."),
    ("everyday", "HIL+EN", "Sige, tawag ka lang kung ready ka na maglakat."),
    ("everyday", "HIL+TL+EN", "Hindi ko alam eh, basta i-text mo na lang ako mamaya."),
    ("everyday", "HIL+TL", "Wala lang, pagod ako kay buong araw nagtrabaho."),
    ("everyday", "HIL", "Salamat gid sa imo nga pagdamay sa amon pamilya."),
    ("everyday", "HIL+EN", "Okay lang na, mag-hang out na lang ta sa weekend."),
    ("oral_tradition", "HIL", "Ang sugidanon nagasaysay sang kabuhi sang una nga panahon."),
    ("oral_tradition", "HIL", "Ginatudlo sang mga gurang ang mga hulubaton kag paktakon."),
    ("oral_tradition", "HIL+EN", "Dapat i-record naton ang mga estorya antes mag-fade ang memory."),
    ("oral_tradition", "HIL", "Nagakawala na ang mga tradisyonal nga ambahanon sa aton."),
    ("oral_tradition", "HIL+TL", "Kailangan nating ituro sa mga bata ang kahalagahan sang kultura."),
]

SCRIPTS = {1: SENTENCES, 2: SENTENCES_2, 3: SENTENCES_3}

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


def build(sentences, start_index, out_dir):
    """Write one annotation per sentence; clip IDs start at start_index."""
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for offset, (domain, switch_type, text) in enumerate(sentences):
        clip_id = f"hil_cs_{start_index + offset:03d}"
        ann = make_annotation(clip_id, domain, switch_type, text)
        with open(os.path.join(out_dir, f"{clip_id}.json"), "w", encoding="utf-8") as f:
            json.dump(ann, f, ensure_ascii=False, indent=2)
        written.append((clip_id, switch_type))
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="data/annotations")
    ap.add_argument("--script", default="1",
                    help="which elicitation script: 1, 2, 3, or all")
    args = ap.parse_args()

    which = list(SCRIPTS) if args.script == "all" else [int(args.script)]
    written = []
    for s in which:
        if s not in SCRIPTS:
            raise SystemExit(f"Unknown script {s}; choose from {list(SCRIPTS)} or all")
        start = (s - 1) * 40 + 1
        written += build(SCRIPTS[s], start, args.out_dir)
        print(f"Script {s}: hil_cs_{start:03d}..{start + len(SCRIPTS[s]) - 1:03d}")

    print(f"\nWrote {len(written)} annotations to {args.out_dir}.")
    counts = {}
    for _, st in written:
        counts[st] = counts.get(st, 0) + 1
    print("By switch type:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print()
    print("Only generate a script's stubs once its audio exists, or validate with")
    print("--no-audio-check. Reference text is reviewed; per-word lang tags are")
    print("auto-seeded — the recording speaker confirms them (SCHEMA.md, AI_DISCLOSURE.md).")


if __name__ == "__main__":
    main()
