import Head from "next/head";
import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import SegmentedFilter from "../components/SegmentedFilter";

const SWITCH_TYPES = ["HIL", "HIL+EN", "HIL+TL", "HIL+TL+EN"];

// The finding in one clip: the model keeps the borrowed English ("preserve",
// "culture") but erases the Hiligaynon matrix around it.
const FEATURED_CLIP = "hil_cs_038";

function MetricCard({ label, value, suffix = "%", hint, strong }) {
  return (
    <div className={`glass metric ${strong ? "metricStrong" : ""}`}>
      <span className="metricLabel">{label}</span>
      <span className="metricValue">
        {value}
        <em>{suffix}</em>
      </span>
      {hint && <span className="metricHint">{hint}</span>}
    </div>
  );
}

function Token({ t }) {
  const cls = [
    "tok",
    t.switch ? "tokSwitch" : "",
    t.error ? "tokErr" : "tokOk",
  ].join(" ");
  return (
    <span
      className={cls}
      title={`${t.lang}${t.switch ? " · switch" : ""}${
        t.error ? " · error" : " · correct"
      }`}
    >
      {t.text}
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
          <span className="werSub">sw {clip.wer.switch}%</span>
          <span className="werSub">mono {clip.wer.mono}%</span>
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

              <div className="rowLabel">Reference — token diff</div>
              <div className="tokens">
                {clip.tokens.map((t, i) => (
                  <Token key={i} t={t} />
                ))}
              </div>

              <div className="rowLabel">
                Whisper prediction (forced <code>tl</code>)
              </div>
              <div className="pred">{clip.prediction}</div>
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
            An open <strong>code-switch ASR benchmark</strong> for Hiligaynon
            (Ilonggo). We measure <strong>switch-region WER</strong> — separating
            errors on the Hiligaynon matrix language from borrowed English/Tagalog
            words near a language switch.
          </p>
          <p className="finding">
            The finding: models transcribe the borrowed words well but miss the
            Hiligaynon — a <strong>negative switch penalty</strong>.
          </p>
          <span className="modelTag">model · {data.model}</span>
        </header>

        {featured && (
          <section className="glass featured">
            <span className="featuredTag">▶ The finding, in one clip</span>
            <p className="featuredCaption">
              The model keeps the borrowed English — <strong>preserve</strong>,{" "}
              <strong>culture</strong> — but erases the Hiligaynon around it. The
              language the speaker owns is the language the machine drops.
            </p>
            <audio controls preload="none" src={`/${featured.audio}`} className="player" />
            <div className="rowLabel">Reference — token diff</div>
            <div className="tokens">
              {featured.tokens.map((t, i) => (
                <Token key={i} t={t} />
              ))}
            </div>
            <div className="rowLabel">Whisper prediction (forced <code>tl</code>)</div>
            <div className="pred">{featured.prediction}</div>
          </section>
        )}

        <section className="metrics">
          <MetricCard label="Overall WER" value={h.overall} hint="all clips" />
          <MetricCard
            label="Monolingual (Hiligaynon)"
            value={h.mono}
            hint="matrix language"
          />
          <MetricCard
            label="Switch-region WER"
            value={h.switch}
            hint="borrowed words"
          />
          <MetricCard
            label="Switch penalty"
            value={h.penalty}
            hint="switch − mono"
            strong
          />
        </section>

        <section className="glass pairs">
          <h2>Switch-pair WER</h2>
          <PairBar label="hil ↔ en" value={h.pairs.hil_en} />
          <PairBar label="hil ↔ tl" value={h.pairs.hil_tl} />
          <PairBar label="tl ↔ en" value={h.pairs.tl_en} />
        </section>

        {data.cohorts && data.cohorts.length > 1 && (
          <section className="glass cohorts">
            <h2>Cohort ladder</h2>
            <p className="cohortNote">
              Speaker-disjoint. spk02 is a development cohort, reported separately —
              never blended into the headline. The negative switch penalty replicates
              across both speakers.
            </p>
            <div className="cohortTable">
              <div className="cohortRow cohortHead">
                <span>Cohort</span>
                <span>Role</span>
                <span>Overall</span>
                <span>Switch</span>
                <span>Mono</span>
                <span>Penalty</span>
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
              <i className="sw tokSwitch" /> switch region
            </span>
            <span>
              <i className="sw tokErr" /> ASR error
            </span>
            <span>
              <i className="sw tokOk" /> correct
            </span>
            <span className="count">{clips.length} clips</span>
          </div>
        </div>

        <section className="clips glass">
          <div className="clipsHeader">
            <span>Clip</span>
            <span>Tags</span>
            <span style={{textAlign:"right",gridColumn:"3/5"}}>WER · sw · mono</span>
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
          Headline set: <code>scripted_native</code>, Speaker 1. Extension subsets
          (Speaker 2, non-native) excluded from this WER. UI transplanted from
          TreeParse.
        </footer>
      </main>

      <style jsx>{`
        .loading {
          padding: 80px;
          text-align: center;
          color: var(--muted);
        }
        .shell {
          width: min(1080px, calc(100% - 32px));
          margin: 0 auto;
          padding: 32px 0 64px;
          display: flex;
          flex-direction: column;
          gap: 20px;
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
          max-width: 70ch;
          color: #2a2320;
        }
        .finding {
          margin: 0;
          max-width: 70ch;
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
        .featured {
          padding: 22px 26px;
          border-color: rgba(249, 115, 22, 0.45);
          background: rgba(249, 115, 22, 0.1);
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .featuredTag {
          font-size: 0.74rem;
          font-weight: 700;
          letter-spacing: 0.04em;
          text-transform: uppercase;
          color: var(--accent-strong);
        }
        .featuredCaption {
          margin: 0 0 4px;
          max-width: 72ch;
          color: #2a2320;
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
        .segTrack {
          display: inline-flex;
          padding: 4px;
          border-radius: 999px;
          background: rgba(0,0,0,0.07);
          box-shadow: inset 0 2px 5px rgba(0,0,0,0.12), inset 0 -1px 0 rgba(255,255,255,0.55);
          gap: 2px;
          flex-wrap: wrap;
        }
        .segBtn {
          padding: 5px 14px;
          border-radius: 999px;
          border: none;
          background: transparent;
          font-size: 0.78rem;
          font-weight: 500;
          color: rgba(0,0,0,0.45);
          cursor: pointer;
          transition: color 0.15s;
          white-space: nowrap;
        }
        .segBtn:hover {
          color: rgba(0,0,0,0.7);
        }
        .segActive {
          background: linear-gradient(to bottom, rgba(255,255,255,0.92), rgba(235,238,244,0.95));
          box-shadow: inset 0 2px 2px rgba(255,255,255,1), inset 0 -2px 3px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.12);
          color: rgba(0,0,0,0.85) !important;
          font-weight: 700;
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
          background: rgba(255,255,255,0.7) !important;
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
          min-width: 68px;
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
          .clipWer em {
            display: none;
          }
        }
      `}</style>
    </>
  );
}
