import Head from "next/head";
import { useEffect, useMemo, useState } from "react";

const SWITCH_TYPES = ["HIL", "HIL+EN", "HIL+TL", "HIL+TL+EN"];

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

function ClipRow({ clip, open, onToggle }) {
  return (
    <div className={`glass clip ${open ? "clipOpen" : ""}`}>
      <button className="clipHead" onClick={onToggle}>
        <span className="clipId">{clip.clip_id}</span>
        <span className="chip chipDomain">{clip.domain}</span>
        <span className="chip chipSwitch">{clip.switch_type}</span>
        <span className="clipWer">
          WER {clip.wer.overall}%
          <em> · sw {clip.wer.switch}% · mono {clip.wer.mono}%</em>
        </span>
        <span className="caret">{open ? "▾" : "▸"}</span>
      </button>

      {open && (
        <div className="clipBody">
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
      )}
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

        <section className="filters">
          <div className="filterGroup">
            <span className="filterLabel">Switch</span>
            <button
              className={`glassBtn ${fSwitch === "ALL" ? "active" : ""}`}
              onClick={() => setFSwitch("ALL")}
            >
              All
            </button>
            {SWITCH_TYPES.map((s) => (
              <button
                key={s}
                className={`glassBtn ${fSwitch === s ? "active" : ""}`}
                onClick={() => setFSwitch(s)}
              >
                {s}
              </button>
            ))}
          </div>
          <div className="filterGroup">
            <span className="filterLabel">Domain</span>
            <button
              className={`glassBtn ${fDomain === "ALL" ? "active" : ""}`}
              onClick={() => setFDomain("ALL")}
            >
              All
            </button>
            {domains.map((d) => (
              <button
                key={d}
                className={`glassBtn ${fDomain === d ? "active" : ""}`}
                onClick={() => setFDomain(d)}
              >
                {d}
              </button>
            ))}
          </div>
        </section>

        <div className="legend glass">
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

        <section className="clips">
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
        .filters {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .filterGroup {
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          gap: 8px;
        }
        .filterLabel {
          font-size: 0.74rem;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          color: var(--muted);
          width: 64px;
        }
        .legend {
          display: flex;
          gap: 18px;
          align-items: center;
          padding: 10px 18px;
          font-size: 0.8rem;
          color: var(--muted);
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
        .clips {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        :global(.clip) {
          overflow: hidden;
        }
        :global(.clipHead) {
          width: 100%;
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 13px 18px;
          background: transparent;
          border: none;
          cursor: pointer;
          text-align: left;
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
        :global(.clipWer) {
          margin-left: auto;
          font-size: 0.82rem;
          font-weight: 600;
          color: var(--accent-strong);
          white-space: nowrap;
        }
        :global(.clipWer em) {
          font-style: normal;
          font-weight: 400;
          color: var(--muted);
        }
        :global(.caret) {
          color: var(--muted);
        }
        :global(.clipBody) {
          padding: 4px 18px 18px;
          display: flex;
          flex-direction: column;
          gap: 8px;
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
          background: rgba(255, 255, 255, 0.5);
          border: 1px dashed var(--line);
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
