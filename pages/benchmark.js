import { useMemo, useRef, useState } from "react";
import Link from "next/link";
import fs from "fs";
import path from "path";

export async function getStaticProps() {
  const file = path.join(process.cwd(), "public", "benchmark.json");
  const data = JSON.parse(fs.readFileSync(file, "utf-8"));
  return { props: { data } };
}

const LANG = {
  hil: { name: "Hiligaynon", color: "#5ad6c0" },
  tl: { name: "Tagalog", color: "#fbbf24" },
  en: { name: "English", color: "#7cc4ff" },
  other: { name: "Other", color: "#aab8d4" },
};

const CEIL = 100;

function werColor(w) {
  if (w < 20) return "#34d399";
  if (w < 45) return "#fbbf24";
  return "#fb7185";
}

function Bar({ label, wer }) {
  return (
    <div className="bar">
      <div className="barhead">
        <span>{label}</span>
        <span style={{ color: werColor(wer), fontWeight: 700 }}>{wer}%</span>
      </div>
      <div className="bartrack">
        <div className="barfill" style={{ width: `${Math.min(100, (wer / CEIL) * 100)}%`, background: werColor(wer) }} />
      </div>
      <style jsx>{`
        .bar { margin: 0 0 12px; }
        .barhead { display: flex; justify-content: space-between; font-size: .9rem; color: #eaf0fb; margin-bottom: 5px; }
        .bartrack { height: 10px; border-radius: 999px; background: rgba(255,255,255,.10); overflow: hidden; }
        .barfill { height: 100%; border-radius: 999px; transition: width .5s ease; }
      `}</style>
    </div>
  );
}

export default function Benchmark({ data }) {
  const { clips, headline, model } = data;
  const subsets = useMemo(
    () => ["all", ...Array.from(new Set(clips.map((c) => c.subset)))],
    [clips]
  );
  const [subset, setSubset] = useState("all");
  const filtered = useMemo(
    () => (subset === "all" ? clips : clips.filter((c) => c.subset === subset)),
    [clips, subset]
  );
  const [sel, setSel] = useState(0);
  const clip = filtered[sel] || filtered[0];
  const audioRef = useRef(null);

  return (
    <div className="page">
      <main className="wrap">
        <header className="glass hero">
          <p className="kicker"><Link href="/">← Sugidanon</Link> &middot; Benchmark explorer</p>
          <h1>Where speech AI breaks on Ilonggo</h1>
          <p className="lede">
            Each clip is real Hiligaynon code-switch speech. Play it, read the
            gold transcript with per-word language colors, and see exactly which
            words <strong>{model}</strong> got wrong. Errors cluster on the
            Hiligaynon — not the borrowed English and Tagalog.
          </p>
          <div className="headline">
            <Bar label="Monolingual Hiligaynon WER" wer={headline.mono} />
            <Bar label="Overall WER" wer={headline.overall} />
            <Bar label="Switch-region WER" wer={headline.switch} />
            <p className="penalty">Switch penalty <strong>{headline.penalty}%</strong> — the model does better exactly where it leans on borrowed words.</p>
          </div>
        </header>

        <section className="glass">
          <div className="toolbar">
            <div className="filters">
              {subsets.map((s) => (
                <button
                  key={s}
                  className={`chip ${s === subset ? "on" : ""}`}
                  onClick={() => { setSubset(s); setSel(0); }}
                >
                  {s} {s !== "all" && <span className="count">{clips.filter((c) => c.subset === s).length}</span>}
                </button>
              ))}
            </div>
            <div className="legend">
              {Object.entries(LANG).map(([k, v]) => (
                <span key={k} className="leg"><i style={{ background: v.color }} />{v.name}</span>
              ))}
              <span className="leg"><i className="errdot" />error</span>
            </div>
          </div>

          <div className="grid">
            <ul className="cliplist">
              {filtered.map((c, i) => (
                <li key={c.clip_id}>
                  <button className={i === sel ? "on" : ""} onClick={() => setSel(i)}>
                    <span className="cid">{c.clip_id}</span>
                    <span className="meta">{c.domain} &middot; {c.switch_type}</span>
                    <span className="cwer" style={{ color: werColor(c.wer.overall) }}>{c.wer.overall}%</span>
                  </button>
                </li>
              ))}
            </ul>

            {clip && (
              <div className="detail">
                <audio ref={audioRef} controls src={`/${clip.audio}`} className="player" />

                <h3>Reference <span className="sub">gold transcript, colored by language</span></h3>
                <p className="tokens">
                  {clip.tokens.map((t, i) => (
                    <span
                      key={i}
                      className={`tok ${t.error ? "err" : ""}`}
                      style={{ color: (LANG[t.lang] || LANG.other).color }}
                      title={`${(LANG[t.lang] || LANG.other).name}${t.switch ? " · switch region" : ""}${t.error ? " · model error" : ""}`}
                    >
                      {t.text}
                    </span>
                  ))}
                </p>

                <h3>{model} prediction</h3>
                <p className="pred">{clip.prediction || <em>(empty)</em>}</p>

                <div className="clipwer">
                  <Bar label="This clip — monolingual WER" wer={clip.wer.mono} />
                  <Bar label="This clip — overall WER" wer={clip.wer.overall} />
                  <Bar label="This clip — switch-region WER" wer={clip.wer.switch} />
                </div>
                <p className="readout">
                  Red words are model errors. Notice they land on the Hiligaynon
                  matrix far more than on the {LANG.en.name}/{LANG.tl.name} switch words.
                </p>
              </div>
            )}
          </div>
        </section>

        <footer className="foot">
          Baseline: {model}, single speaker. Per-word tags seed-labeled pending
          native confirmation. Data CC BY 4.0.
        </footer>
      </main>

      <style jsx>{`
        .page { min-height: 100vh; position: relative; color: #f3f6fc; background: #0a0e1c; }
        .page::before { content: ""; position: fixed; inset: 0; z-index: 0; background: url('/bg-festival.webp') center/cover no-repeat; filter: blur(22px) brightness(.7); transform: scale(1.12); }
        .page::after { content: ""; position: fixed; inset: 0; z-index: 0; background: rgba(8,11,24,.72); }
        .wrap { position: relative; z-index: 1; max-width: 1040px; margin: 0 auto; padding: 48px 20px 64px; display: flex; flex-direction: column; gap: 16px; }
        .glass { background: rgba(20,28,48,.58); backdrop-filter: blur(18px) saturate(140%); -webkit-backdrop-filter: blur(18px) saturate(140%); border: 1px solid rgba(255,255,255,.12); border-radius: 20px; padding: 28px 32px; }
        .kicker { text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; color: #9fc0ff; margin: 0 0 12px; font-weight: 600; }
        .kicker :global(a) { color: #9fc0ff; text-decoration: none; }
        h1 { font-size: 2.2rem; margin: 0 0 12px; letter-spacing: -.02em; color: #fff; }
        .lede { font-size: 1.06rem; line-height: 1.6; color: #dbe3f4; margin: 0 0 22px; max-width: 74ch; }
        .headline { max-width: 560px; }
        .penalty { font-size: .92rem; color: #c4d0ea; margin: 8px 0 0; }
        .penalty strong { color: #fb7185; }

        .toolbar { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 14px; margin-bottom: 20px; }
        .filters { display: flex; flex-wrap: wrap; gap: 8px; }
        .chip { cursor: pointer; padding: 7px 13px; border-radius: 999px; border: 1px solid rgba(255,255,255,.18); background: rgba(255,255,255,.06); color: #e7eefc; font-size: .85rem; font-weight: 600; }
        .chip.on { background: #5ad6c0; color: #06121f; border-color: transparent; }
        .chip .count { opacity: .7; margin-left: 4px; }
        .legend { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; font-size: .8rem; color: #c4d0ea; }
        .leg { display: inline-flex; align-items: center; gap: 5px; }
        .leg i { width: 11px; height: 11px; border-radius: 3px; display: inline-block; }
        .leg i.errdot { background: transparent; border-bottom: 2px solid #fb7185; border-radius: 0; height: 7px; }

        .grid { display: grid; grid-template-columns: 280px 1fr; gap: 22px; }
        .cliplist { list-style: none; margin: 0; padding: 0; max-height: 560px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; }
        .cliplist button { width: 100%; text-align: left; display: grid; grid-template-columns: 1fr auto; gap: 2px 8px; padding: 9px 12px; border-radius: 11px; border: 1px solid rgba(255,255,255,.10); background: rgba(255,255,255,.04); color: #e7eefc; cursor: pointer; }
        .cliplist button.on { background: rgba(90,150,255,.18); border-color: rgba(120,170,255,.4); }
        .cid { font-weight: 600; font-size: .9rem; }
        .meta { font-size: .76rem; color: #9fb0d0; grid-column: 1; }
        .cwer { grid-row: 1 / span 2; align-self: center; font-weight: 700; font-size: .95rem; }

        .detail { min-width: 0; }
        .player { width: 100%; margin-bottom: 18px; }
        h3 { font-size: 1rem; color: #fff; margin: 16px 0 8px; }
        h3 .sub { font-weight: 400; font-size: .82rem; color: #9fb0d0; margin-left: 8px; }
        .tokens { line-height: 2; margin: 0; font-size: 1.18rem; }
        .tok { margin-right: .4em; font-weight: 600; }
        .tok.err { text-decoration: underline; text-decoration-color: #fb7185; text-decoration-thickness: 3px; text-underline-offset: 4px; }
        .pred { font-size: 1.05rem; color: #d4dcee; background: rgba(4,8,18,.5); border: 1px solid rgba(255,255,255,.10); border-radius: 12px; padding: 12px 15px; margin: 0; }
        .clipwer { margin: 22px 0 10px; max-width: 460px; }
        .readout { font-size: .9rem; color: #c4d0ea; line-height: 1.55; margin: 0; }

        .foot { color: #aab8d4; font-size: .85rem; padding: 4px 8px; }

        @media (max-width: 760px) {
          .grid { grid-template-columns: 1fr; }
          .cliplist { max-height: 240px; }
          h1 { font-size: 1.7rem; }
        }
      `}</style>
    </div>
  );
}
