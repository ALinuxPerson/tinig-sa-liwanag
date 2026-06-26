import Head from "next/head";
import { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import SegmentedFilter from "../components/SegmentedFilter";

const SWITCH_TYPES = ["HIL", "HIL+EN", "HIL+TL", "HIL+TL+EN"];

// The finding in one clip: the model keeps the borrowed English ("preserve",
// "culture") but erases the Hiligaynon matrix around it.
const FEATURED_CLIP = "hil_cs_038";

function Token({ t }) {
  const [tip, setTip] = useState(null); // null | "above" | "below"
  const ref = useRef(null);
  const cls = ["tok", t.switch ? "tokSwitch" : "", t.error ? "tokErr" : "tokOk"].join(" ");
  const label = [
    t.error ? "ASR error" : "correct",
    t.switch ? "switch region" : "monolingual",
    `lang: ${t.lang}`,
  ].join(" · ");

  function handleEnter(e) {
    const rect = ref.current.getBoundingClientRect();
    const mid = rect.top + rect.height / 2;
    setTip(e.clientY < mid ? "above" : "below");
  }

  return (
    <span
      ref={ref}
      className={cls}
      style={{ position: "relative" }}
      onMouseEnter={handleEnter}
      onMouseLeave={() => setTip(null)}
    >
      {t.text}
      {tip && (
        <span
          style={{
            position: "absolute",
            [tip === "above" ? "bottom" : "top"]: "calc(100% + 7px)",
            left: "50%",
            transform: "translateX(clamp(-120px, -50%, 0px))",
            background: "rgba(255,255,255,0.82)",
            backdropFilter: "blur(24px) saturate(220%) brightness(1.08)",
            WebkitBackdropFilter: "blur(24px) saturate(220%) brightness(1.08)",
            border: "1px solid rgba(255,255,255,0.9)",
            boxShadow: "0 4px 20px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,1)",
            color: "rgba(0,0,0,0.8)",
            fontSize: "0.68rem",
            fontWeight: 600,
            whiteSpace: "nowrap",
            padding: "5px 10px",
            borderRadius: 8,
            pointerEvents: "none",
            zIndex: 300,
            letterSpacing: "0.02em",
          }}
        >
          {label}
        </span>
      )}
    </span>
  );
}

function werColor(v) {
  if (v < 40) return "werLow";
  if (v < 70) return "werMid";
  return "werHigh";
}

function ClipRow({ clip, open, onToggle }) {
  return (
    <div className={`clip ${open ? "clipOpen" : ""}`}>
      <button className="clipHead" onClick={onToggle}>
        <span className="clipId">{clip.clip_id}</span>
        <span className="chipCol">
          <span className="chip chipDomain">{clip.domain}</span>
          <span className="chip chipSwitch">{clip.switch_type}</span>
        </span>
        <span className="clipStats">
          <span className={`werVal ${werColor(clip.wer.overall)}`}>{clip.wer.overall}%</span>
          <span className="werSub">borrowed {clip.wer.switch}%</span>
          <span className="werSub">Hil {clip.wer.mono}%</span>
        </span>
        <span className="caret">{open ? "▾" : "▸"}</span>
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            className="clipBody"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.22, ease: [0.4, 0, 0.2, 1] }}
            style={{ overflow: "hidden" }}
          >
            <div className="clipBodyInner">
              <audio controls preload="none" src={`/${clip.audio}`} className="player" />

              <div className="clipCols">
                <div className="clipCol">
                  <div className="rowLabel">What the speaker said</div>
                  <div className="tokens">
                    {clip.tokens.map((t, i) => (
                      <Token key={i} t={t} />
                    ))}
                  </div>
                </div>
                <div className="clipColDivider" />
                <div className="clipCol">
                  <div className="rowLabel">What the AI heard</div>
                  <div className="pred">{clip.prediction}</div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function PairBar({ label, value }) {
  return (
    <div className="pairRow">
      <span className="pairLabel">{label}</span>
      <div className="track">
        <div className="fill" style={{ width: `${value}%` }} />
      </div>
      <span className="pairVal">{value}%</span>
      <style jsx>{`
        .pairRow {
          display: grid;
          grid-template-columns: 90px 1fr 56px;
          align-items: center;
          gap: 12px;
          margin: 7px 0;
        }
        .pairLabel {
          font-size: 0.85rem;
          color: var(--muted);
        }
        .track {
          height: 10px;
          border-radius: 999px;
          background: rgba(124, 92, 60, 0.12);
          overflow: hidden;
        }
        .fill {
          height: 100%;
          border-radius: 999px;
          background: linear-gradient(90deg, #fbbf24, var(--accent-strong));
        }
        .pairVal {
          text-align: right;
          font-weight: 700;
          font-size: 0.85rem;
          color: var(--accent-strong);
        }
      `}</style>
    </div>
  );
}

export default function Home() {
  const [data, setData] = useState(null);
  const [openId, setOpenId] = useState(null);
  const [fSwitch, setFSwitch] = useState("ALL");
  const [fDomain, setFDomain] = useState("ALL");

  useEffect(() => {
    fetch("/benchmark.json")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData({ error: true }));
  }, []);

  const domains = useMemo(() => {
    if (!data?.clips) return [];
    return [...new Set(data.clips.map((c) => c.domain))];
  }, [data]);

  const featured = useMemo(() => {
    if (!data?.clips) return null;
    return data.clips.find((c) => c.clip_id === FEATURED_CLIP) || null;
  }, [data]);

  const clips = useMemo(() => {
    if (!data?.clips) return [];
    return data.clips.filter(
      (c) =>
        (fSwitch === "ALL" || c.switch_type === fSwitch) &&
        (fDomain === "ALL" || c.domain === fDomain)
    );
  }, [data, fSwitch, fDomain]);

  if (!data) return <div className="loading">Loading benchmark…</div>;
  if (data.error)
    return <div className="loading">Could not load benchmark.json</div>;

  const h = data.headline;

  return (
    <>
      <Head>
        <title>Sugidanon — Code-Switch Hiligaynon ASR Benchmark</title>
        <meta
          name="description"
          content="Switch-region WER benchmark for Hiligaynon code-switched speech."
        />
      </Head>

      <main className="shell">
        <header className="glass hero">
          <h1 className="brand">Sugidanon</h1>
          <p className="tagline">
            A test of how well speech-to-text AI understands{" "}
            <strong>Hiligaynon (Ilonggo)</strong> — a Philippine language spoken
            by about 9 million people.
          </p>
          <p className="subtitle">
            Hiligaynon speakers naturally drop in English and Tagalog words
            mid-sentence. We measured exactly where the AI breaks down — and
            found it breaks on the home language, not the borrowed words.
          </p>
          <span className="modelTag">tested model · {data.model}</span>
        </header>

        {/* plain-language finding band — the whole story in three lines */}
        <section className="glass story">
          <span className="storyTag">The finding, in plain terms</span>
          <p className="storyLead">
            When a sentence mixes languages, the AI transcribes the borrowed{" "}
            <strong>English and Tagalog words correctly</strong> — but drops the{" "}
            <strong>Hiligaynon words</strong> right next to them. It hears the
            foreign words, and loses the home language.
          </p>

          {featured && (
            <div className="storyClip">
              <span className="storyClipTag">▶ Hear it in one clip</span>
              <audio controls preload="none" src={`/${featured.audio}`} className="player" />
              <div className="storyGrid">
                <div>
                  <div className="rowLabel">What the speaker said</div>
                  <div className="tokens">
                    {featured.tokens.map((t, i) => (
                      <Token key={i} t={t} />
                    ))}
                  </div>
                </div>
                <div>
                  <div className="rowLabel">What the AI heard</div>
                  <div className="pred">{featured.prediction}</div>
                </div>
              </div>
              <p className="storyClipNote">
                The AI kept the English — <strong>preserve</strong>,{" "}
                <strong>culture</strong> — but erased the Hiligaynon around it.
              </p>
            </div>
          )}
        </section>

        {/* the contrast, as two big numbers — this IS the result */}
        <section className="glass contrast">
          <div className="contrastSide">
            <span className="contrastLabel">Hiligaynon words</span>
            <span className="contrastNum bad">{h.mono}<em>%</em></span>
            <span className="contrastSub">wrong — the home language</span>
          </div>
          <div className="contrastVs">
            <span className="contrastGap">{h.penalty}%</span>
            <span className="contrastGapLabel">gap</span>
          </div>
          <div className="contrastSide">
            <span className="contrastLabel">Borrowed En/Tl words</span>
            <span className="contrastNum good">{h.switch}<em>%</em></span>
            <span className="contrastSub">wrong — the easy words</span>
          </div>
        </section>

        <p className="werNote">
          These are <strong>word error rates</strong> — the share of words the AI
          got wrong. Lower is better. Overall across every clip:{" "}
          <strong>{h.overall}%</strong>.
        </p>

        <section className="glass pairs">
          <h2>Which language mixes are hardest?</h2>
          <p className="pairsNote">
            Error rate on the words right around each kind of switch.
          </p>
          <PairBar label="Hil + English" value={h.pairs.hil_en} />
          <PairBar label="Hil + Tagalog" value={h.pairs.hil_tl} />
          <PairBar label="Tagalog + English" value={h.pairs.tl_en} />
        </section>

        <section className="glass repro">
          <h2 className="sectionTitle">Try it or reproduce the numbers</h2>
          <p className="reproNote">
            Everything is open. Run the exact benchmark in your browser, download
            the dataset, or read the code.
          </p>
          <div className="reproGrid">
            <a
              className="reproCard"
              href="https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb"
              target="_blank"
              rel="noreferrer"
            >
              <span className="reproIcon">▶</span>
              <span className="reproName">Run in Google Colab</span>
              <span className="reproDesc">
                One click reproduces every number on this page. No setup.
              </span>
              <span className="reproLink">colab.research.google.com →</span>
            </a>
            <a
              className="reproCard"
              href="https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch"
              target="_blank"
              rel="noreferrer"
            >
              <span className="reproIcon">⬇</span>
              <span className="reproName">Download the dataset</span>
              <span className="reproDesc">
                Audio, transcripts, and labels on Hugging Face.
              </span>
              <span className="reproLink">huggingface.co/datasets →</span>
            </a>
            <a
              className="reproCard"
              href="https://github.com/Jazztinn/tinig-sa-liwanag"
              target="_blank"
              rel="noreferrer"
            >
              <span className="reproIcon">{"{ }"}</span>
              <span className="reproName">Read the code</span>
              <span className="reproDesc">
                Scorer, scripts, and benchmark card on GitHub.
              </span>
              <span className="reproLink">github.com →</span>
            </a>
          </div>
        </section>

        {data.cohorts && data.cohorts.length > 1 && (
          <section className="glass cohorts">
            <h2>Does it hold up with a second speaker?</h2>
            <p className="cohortNote">
              Yes. We ran a second speaker (kept fully separate, never mixed into
              the headline numbers). The same gap shows up — the AI drops the
              Hiligaynon for both speakers.
            </p>
            <div className="cohortTable">
              <div className="cohortRow cohortHead">
                <span>Speaker</span>
                <span>Role</span>
                <span>Overall</span>
                <span>Borrowed</span>
                <span>Hiligaynon</span>
                <span>Gap</span>
              </div>
              {data.cohorts.map((c) => (
                <div className="cohortRow" key={c.name}>
                  <span className="cohortName">
                    {c.speaker} <em>· {c.n}</em>
                  </span>
                  <span className="cohortRole">{c.role}</span>
                  <span>{c.overall}%</span>
                  <span>{c.switch}%</span>
                  <span>{c.mono}%</span>
                  <span className="cohortPen">{c.penalty}%</span>
                </div>
              ))}
            </div>
          </section>
        )}

        <div className="filterCard glass">
          <section className="filters">
            <div className="filterGroup">
              <span className="filterLabel">Switch</span>
              <SegmentedFilter
                options={["ALL", ...SWITCH_TYPES].map((s) => ({ id: s, label: s === "ALL" ? "All" : s }))}
                value={fSwitch}
                onChange={setFSwitch}
              />
            </div>
            <div className="filterGroup">
              <span className="filterLabel">Domain</span>
              <SegmentedFilter
                options={["ALL", ...domains].map((d) => ({ id: d, label: d === "ALL" ? "All" : d }))}
                value={fDomain}
                onChange={setFDomain}
              />
            </div>
          </section>

          <div className="filterDivider" />

          <div className="legend">
            <span>
              <i className="sw tokSwitch" /> near a language switch
            </span>
            <span>
              <i className="sw tokErr" /> AI got it wrong
            </span>
            <span>
              <i className="sw tokOk" /> AI got it right
            </span>
            <span className="count">{clips.length} clips</span>
          </div>
        </div>

        <section className="clips glass">
          <div className="clipsExplain">
            <h2>Browse every clip</h2>
            <p>
              Click any row to play the audio and see, word by word, what the
              speaker said versus what the AI heard.
            </p>
          </div>
          <div className="clipsHeader">
            <span>Clip</span>
            <span>Tags</span>
            <span style={{textAlign:"right",gridColumn:"3/5"}}>overall · borrowed · Hiligaynon</span>
          </div>
          {clips.map((c) => (
            <ClipRow
              key={c.clip_id}
              clip={c}
              open={openId === c.clip_id}
              onToggle={() => setOpenId(openId === c.clip_id ? null : c.clip_id)}
            />
          ))}
        </section>

        <footer className="foot">
          Headline numbers come from 40 scripted clips by one native speaker.
          The second speaker and non-native clips are kept separate and never
          mixed into these numbers.
        </footer>
      </main>

      <style jsx>{`
        .loading {
          padding: 80px;
          text-align: center;
          color: var(--muted);
        }
        .shell {
          width: min(var(--content-w), calc(100% - var(--s7)));
          margin: 0 auto;
          padding: var(--s7) 0 var(--s8);
          display: flex;
          flex-direction: column;
          gap: var(--s5);
        }
        .hero {
          padding: 30px 32px;
        }
        .brand {
          font-family: "Borel", cursive;
          font-size: clamp(2.4rem, 6vw, 3.6rem);
          margin: 0 0 6px;
          color: var(--accent-strong);
          line-height: 1.1;
        }
        .tagline {
          margin: 0 0 8px;
          max-width: 68ch;
          font-size: 1.08rem;
          color: #2a2320;
        }
        .subtitle {
          margin: 0;
          max-width: 68ch;
          color: var(--muted);
        }
        .modelTag {
          display: inline-block;
          margin-top: 14px;
          font-size: 0.72rem;
          letter-spacing: 0.04em;
          text-transform: uppercase;
          color: var(--accent-strong);
          background: rgba(249, 115, 22, 0.12);
          padding: 4px 10px;
          border-radius: 999px;
        }
        /* ---- plain-language story band ---- */
        .story {
          padding: 24px 28px;
          display: flex;
          flex-direction: column;
          gap: 14px;
        }
        .storyTag {
          font-size: 0.74rem;
          font-weight: 700;
          letter-spacing: 0.04em;
          text-transform: uppercase;
          color: var(--accent-strong);
        }
        .storyLead {
          margin: 0;
          max-width: 72ch;
          font-size: 1.12rem;
          line-height: 1.5;
          color: #2a2320;
        }
        .storyClip {
          margin-top: 4px;
          padding: 16px 18px;
          border-radius: 12px;
          background: rgba(249, 115, 22, 0.08);
          border: 1px solid rgba(249, 115, 22, 0.28);
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .storyClipTag {
          font-size: 0.74rem;
          font-weight: 700;
          letter-spacing: 0.03em;
          color: var(--accent-strong);
        }
        .storyGrid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 18px;
          align-items: start;
        }
        .storyClipNote {
          margin: 0;
          font-size: 0.9rem;
          color: var(--muted);
        }
        /* ---- the contrast (two big numbers) ---- */
        .contrast {
          padding: 22px 24px;
          display: grid;
          grid-template-columns: 1fr auto 1fr;
          align-items: center;
          gap: 12px;
        }
        .contrastSide {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          gap: 2px;
        }
        .contrastLabel {
          font-size: 0.8rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          color: var(--muted);
        }
        .contrastNum {
          font-size: clamp(2.6rem, 8vw, 3.6rem);
          font-weight: 800;
          line-height: 1;
          font-variant-numeric: tabular-nums;
        }
        .contrastNum em {
          font-size: 1.4rem;
          font-style: normal;
          font-weight: 700;
        }
        .contrastNum.bad {
          color: #dc2626;
        }
        .contrastNum.good {
          color: #16a34a;
        }
        .contrastSub {
          font-size: 0.82rem;
          color: var(--muted);
        }
        .contrastVs {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 0 8px;
        }
        .contrastGap {
          font-size: 1.6rem;
          font-weight: 800;
          color: var(--accent-strong);
          font-variant-numeric: tabular-nums;
        }
        .contrastGapLabel {
          font-size: 0.68rem;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--muted);
        }
        .werNote {
          margin: -4px 4px 0;
          font-size: 0.9rem;
          color: var(--muted);
          text-align: center;
        }
        .pairsNote {
          margin: 0 0 12px;
          font-size: 0.85rem;
          color: var(--muted);
        }
        .repro {
          padding: var(--s5) var(--s6);
        }
        .reproNote {
          margin: 0 0 var(--s4);
          font-size: var(--fs-md);
          color: var(--muted);
          max-width: var(--measure);
        }
        .reproGrid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: var(--s3);
        }
        .reproCard {
          display: flex;
          flex-direction: column;
          gap: var(--s1);
          padding: var(--s4);
          border-radius: var(--r-md);
          background: rgba(255, 255, 255, 0.45);
          border: 1px solid rgba(255, 255, 255, 0.7);
          text-decoration: none;
          color: var(--text);
          transition: transform 0.12s var(--ease), background 0.15s,
            border-color 0.15s;
        }
        .reproCard:hover {
          transform: translateY(-2px);
          background: rgba(255, 255, 255, 0.75);
          border-color: var(--accent-tint-2);
        }
        .reproIcon {
          font-size: 1.1rem;
          font-weight: var(--fw-bold);
          color: var(--accent-strong);
        }
        .reproName {
          font-weight: var(--fw-bold);
          font-size: var(--fs-base);
        }
        .reproDesc {
          font-size: var(--fs-sm);
          color: var(--muted);
          flex: 1;
        }
        .reproLink {
          margin-top: var(--s1);
          font-size: var(--fs-xs);
          font-weight: var(--fw-semibold);
          color: var(--accent-strong);
        }
        .clipsExplain {
          padding: 18px 20px 4px;
        }
        .clipsExplain h2 {
          margin: 0 0 4px;
          font-size: 0.95rem;
        }
        .clipsExplain p {
          margin: 0;
          font-size: 0.85rem;
          color: var(--muted);
          max-width: 64ch;
        }
        .metrics {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 14px;
        }
        :global(.metric) {
          padding: 16px 18px;
          display: flex;
          flex-direction: column;
          gap: 2px;
        }
        :global(.metricStrong) {
          background: rgba(249, 115, 22, 0.16);
          border-color: rgba(249, 115, 22, 0.4);
        }
        :global(.metricLabel) {
          font-size: 0.74rem;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          color: var(--muted);
        }
        :global(.metricValue) {
          font-size: 1.9rem;
          font-weight: 700;
          color: var(--accent-strong);
        }
        :global(.metricValue em) {
          font-size: 1rem;
          font-style: normal;
          color: var(--muted);
          margin-left: 2px;
        }
        :global(.metricHint) {
          font-size: 0.74rem;
          color: var(--muted);
        }
        .pairs {
          padding: 18px 24px;
        }
        .pairs h2 {
          margin: 0 0 12px;
          font-size: 0.95rem;
        }
        .cohorts {
          padding: 18px 24px;
        }
        .cohorts h2 {
          margin: 0 0 6px;
          font-size: 0.95rem;
        }
        .cohortNote {
          margin: 0 0 14px;
          font-size: 0.82rem;
          color: var(--muted);
          max-width: 72ch;
        }
        .cohortTable {
          display: flex;
          flex-direction: column;
          gap: 2px;
        }
        .cohortRow {
          display: grid;
          grid-template-columns: 1.4fr 1.1fr repeat(4, 0.8fr);
          align-items: center;
          gap: 8px;
          padding: 8px 10px;
          border-radius: 8px;
          font-variant-numeric: tabular-nums;
          font-size: 0.88rem;
        }
        .cohortRow:nth-child(odd of .cohortRow:not(.cohortHead)) {
          background: rgba(255, 255, 255, 0.4);
        }
        .cohortHead {
          font-size: 0.72rem;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          color: var(--muted);
          font-weight: 600;
        }
        .cohortName {
          font-weight: 700;
        }
        .cohortName em,
        .cohortRole {
          font-style: normal;
          font-weight: 400;
          color: var(--muted);
        }
        .cohortPen {
          font-weight: 700;
          color: var(--accent-strong);
        }
        .filterCard {
          display: flex;
          flex-direction: column;
          gap: 0;
          padding: 20px 24px 18px;
        }
        .filters {
          display: flex;
          flex-direction: column;
          gap: 14px;
        }
        .filterDivider {
          height: 1px;
          background: rgba(0, 0, 0, 0.06);
          margin: 16px 0 14px;
        }
        .filterGroup {
          display: flex;
          align-items: center;
          gap: 14px;
        }
        .filterLabel {
          font-size: 0.68rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--muted);
          width: 56px;
          flex-shrink: 0;
        }
        .legend {
          display: flex;
          gap: 18px;
          align-items: center;
          font-size: 0.82rem;
          font-weight: 500;
          color: var(--text);
          flex-wrap: wrap;
        }
        .legend .count {
          margin-left: auto;
          font-weight: 600;
          color: var(--accent-strong);
        }
        .sw {
          display: inline-block;
          width: 14px;
          height: 14px;
          border-radius: 4px;
          margin-right: 6px;
          vertical-align: -2px;
        }
        .legend .tokSwitch {
          background: var(--switch);
          box-shadow: none;
        }
        .legend .tokOk {
          background: var(--ok);
        }
        .legend .tokErr {
          background: var(--err);
          text-decoration: none;
        }
        .clips {
          display: flex;
          flex-direction: column;
          gap: 0;
          overflow: hidden;
          padding: 0;
        }
        :global(.clip) {
          border-radius: 0;
          background: transparent;
          border: none;
          box-shadow: none;
          backdrop-filter: none;
          -webkit-backdrop-filter: none;
          transition: opacity 0.18s ease;
        }
        :global(.clip + .clip) {
          border-top: 1px solid rgba(0, 0, 0, 0.07);
        }
        /* dim siblings when one clip is open */
        :global(.clips:has(.clipOpen) .clip:not(.clipOpen)) {
          opacity: 0.45;
        }
        :global(.clipOpen) {
          background: rgba(255,250,244,0.97) !important;
          backdrop-filter: blur(20px) saturate(180%);
          -webkit-backdrop-filter: blur(20px) saturate(180%);
          border-top: 1px solid rgba(255,255,255,0.9) !important;
          border-bottom: 1px solid rgba(0,0,0,0.06) !important;
          box-shadow: 0 4px 20px rgba(0,0,0,0.1), 0 1px 4px rgba(0,0,0,0.06) !important;
          z-index: 2;
          position: relative;
          border-radius: 12px !important;
          margin: 4px 0;
          opacity: 1 !important;
        }
        :global(.clipHead) {
          width: 100%;
          display: grid;
          grid-template-columns: 120px 1fr auto auto;
          align-items: center;
          gap: 12px;
          padding: 13px 20px;
          background: transparent;
          border: none;
          cursor: pointer;
          text-align: left;
        }
        :global(.clipHead:hover) {
          background: rgba(0, 0, 0, 0.025);
        }
        :global(.clipBodyInner) {
          padding: 4px 20px 18px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        :global(.chipCol) {
          display: flex;
          gap: 6px;
          flex-wrap: wrap;
        }
        :global(.clipStats) {
          display: flex;
          gap: 12px;
          align-items: center;
          font-size: 0.82rem;
          font-variant-numeric: tabular-nums;
          white-space: nowrap;
        }
        :global(.werVal) {
          font-weight: 700;
          min-width: 48px;
          text-align: right;
        }
        :global(.werLow)  { color: #16a34a; }
        :global(.werMid)  { color: #d97706; }
        :global(.werHigh) { color: #dc2626; }
        :global(.werSub) {
          color: var(--muted);
          font-weight: 400;
          min-width: 92px;
          text-align: right;
        }
        :global(.clipId) {
          font-weight: 700;
          font-variant-numeric: tabular-nums;
        }
        :global(.chip) {
          font-size: 0.7rem;
          padding: 2px 9px;
          border-radius: 999px;
          font-weight: 600;
          white-space: nowrap;
        }
        :global(.chipDomain) {
          background: rgba(124, 92, 60, 0.12);
          color: var(--muted);
        }
        :global(.chipSwitch) {
          background: rgba(245, 158, 11, 0.2);
          color: #92580a;
        }
        .clipsHeader {
          display: grid;
          grid-template-columns: 120px 1fr auto auto;
          gap: 12px;
          padding: 10px 20px;
          font-size: 0.65rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--muted);
          border-bottom: 1px solid rgba(0,0,0,0.07);
          background: rgba(0,0,0,0.018);
        }
        :global(.caret) {
          color: var(--muted);
        }
        :global(.clipBody) {
          overflow: hidden;
        }
        :global(.clipCols) {
          display: grid;
          grid-template-columns: 1fr 1px 1fr;
          gap: 16px;
          align-items: start;
        }
        :global(.clipCol) {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        :global(.clipColDivider) {
          background: rgba(0,0,0,0.07);
          align-self: stretch;
        }
        :global(.player) {
          width: 100%;
          height: 38px;
        }
        :global(.rowLabel) {
          font-size: 0.72rem;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          color: var(--muted);
          margin-top: 6px;
        }
        :global(.tokens) {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
          overflow: visible;
          padding-top: 4px;
        }
        :global(.tok) {
          padding: 3px 8px;
          border-radius: 7px;
          font-size: 0.95rem;
        }
        :global(.tokOk) {
          background: var(--ok-bg);
          color: #15803d;
        }
        :global(.tokErr) {
          background: var(--err-bg);
          color: var(--err);
          text-decoration: line-through;
          text-decoration-color: rgba(220, 38, 38, 0.5);
        }
        :global(.tokSwitch) {
          box-shadow: inset 0 0 0 2px var(--switch);
        }
        :global(.pred) {
          background: rgba(0, 0, 0, 0.04);
          border: 1px solid rgba(0, 0, 0, 0.08);
          box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.08), inset 0 1px 2px rgba(0, 0, 0, 0.06);
          border-radius: 8px;
          padding: 8px 12px;
          font-size: 0.95rem;
        }
        .foot {
          font-size: 0.78rem;
          color: var(--muted);
          text-align: center;
          padding-top: 8px;
        }
        @media (max-width: 720px) {
          .metrics {
            grid-template-columns: repeat(2, 1fr);
          }
          .storyGrid {
            grid-template-columns: 1fr;
          }
          .contrast {
            grid-template-columns: 1fr;
            gap: 16px;
          }
          .reproGrid {
            grid-template-columns: 1fr;
          }
          .contrastVs {
            flex-direction: row;
            gap: 8px;
          }
          .clipWer em {
            display: none;
          }
        }
      `}</style>
    </>
  );
}
