import Link from "next/link";

const HF = "https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch";
const COLAB = "https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb";
const GITHUB = "https://github.com/Jazztinn/tinig-sa-liwanag";

// WER bars (higher = worse). Scaled against a 70% visual ceiling.
const CEIL = 70;
const breakdown = [
  { label: "Monolingual Hiligaynon", wer: 66.3, note: "pure Ilonggo words" },
  { label: "Overall", wer: 59.8, note: "whole utterance" },
  { label: "Switch-region", wer: 36.4, note: "words next to a language switch" },
];
const pairs = [
  { label: "tl ↔ en", wer: 6.2, note: "Tagalog–English: nearly solved" },
  { label: "hil ↔ tl", wer: 24.4, note: "Hiligaynon–Tagalog" },
  { label: "hil ↔ en", wer: 40.8, note: "Hiligaynon–English: worst" },
];

function werColor(wer) {
  // green (low/good) -> amber -> red (high/bad)
  if (wer < 20) return "#34d399";
  if (wer < 40) return "#fbbf24";
  return "#fb7185";
}

function Bar({ label, wer, note }) {
  return (
    <div className="bar">
      <div className="barhead">
        <span className="barlabel">{label}</span>
        <span className="barval" style={{ color: werColor(wer) }}>{wer}%</span>
      </div>
      <div className="bartrack">
        <div className="barfill" style={{
          width: `${Math.min(100, (wer / CEIL) * 100)}%`,
          background: `linear-gradient(90deg, ${werColor(wer)}aa, ${werColor(wer)})`,
        }} />
      </div>
      <span className="barnote">{note}</span>
    </div>
  );
}

function Code({ children }) {
  return <pre className="code"><code>{children}</code></pre>;
}

export default function Home() {
  return (
    <div className="page">
      <main className="wrap">
        <header className="hero glass">
          <p className="kicker">Open speech benchmark &middot; Hiligaynon (Ilonggo)</p>
          <h1>Sugidanon</h1>
          <p className="lede">
            The first openly-licensed, code-switch-labeled speech benchmark for
            Hiligaynon &mdash; a language spoken by over 9 million Filipinos, yet
            nearly invisible to modern speech technology.
          </p>
          <nav className="links">
            <a className="pill primary" href={COLAB} target="_blank" rel="noreferrer">Run the benchmark</a>
            <a className="pill" href={HF} target="_blank" rel="noreferrer">Dataset</a>
            <a className="pill" href={GITHUB} target="_blank" rel="noreferrer">Source code</a>
            <Link className="pill" href="/demo">Translation demo</Link>
          </nav>
        </header>

        <section className="glass finding">
          <span className="eyebrow">The finding</span>
          <h2 className="punch">
            Today&apos;s speech AI hears the English and Tagalog in Ilonggo speech
            &mdash; but misses the Hiligaynon itself.
          </h2>
          <p className="plain">
            When a Hiligaynon speaker mixes in an English or Tagalog word, an
            off-the-shelf model transcribes it almost perfectly. The moment they
            speak actual Hiligaynon, it fails roughly <strong>two of every three
            words</strong>. We turned that blind spot into a measurable number.
          </p>

          <div className="bars">
            <div className="barcol">
              <h3>Word error rate by region</h3>
              <p className="colsub">Higher is worse. The model does best exactly where it leans on borrowed words.</p>
              {breakdown.map((b) => <Bar key={b.label} {...b} />)}
            </div>
            <div className="barcol">
              <h3>Error rate by switch pair</h3>
              <p className="colsub">The more Hiligaynon is involved, the harder it gets.</p>
              {pairs.map((b) => <Bar key={b.label} {...b} />)}
            </div>
          </div>

          <div className="takeaway">
            <strong>Why it matters:</strong> the failure scales with how much
            Hiligaynon a sentence contains. Tagalog&ndash;English code-switching is
            nearly solved (6% error); Hiligaynon&ndash;English is the worst (41%).
            That gap is what Sugidanon measures &mdash; and it&apos;s the first open
            dataset that lets anyone measure it.
            <span className="fine">Baseline: OpenAI Whisper (small), single speaker. Preliminary.</span>
          </div>
        </section>

        <section className="glass">
          <h2>What&apos;s inside</h2>
          <div className="chips">
            <div className="chip"><strong>40</strong><span>code-switch clips (~3.1 min)</span></div>
            <div className="chip"><strong>8</strong><span>everyday domains</span></div>
            <div className="chip"><strong>4</strong><span>switch types</span></div>
            <div className="chip"><strong>per-word</strong><span>hil / tl / en tags</span></div>
          </div>
          <p className="body">
            Domains span market, transport, school/work, family, health, culture,
            everyday talk, and oral tradition. Every word is tagged by language, so
            the scorer can isolate exactly where errors happen. Transcripts were
            reviewed by a native speaker; per-word tags are seed-labeled pending a
            confirmation pass. Released under CC BY 4.0.
          </p>
        </section>

        <section className="glass">
          <h2>Use it</h2>
          <p className="body">Load the dataset in one line:</p>
          <Code>{`from datasets import load_dataset

ds = load_dataset("LauelKills/sugidanon-hil-codeswitch",
                  data_dir="data/audio", split="train")
print(ds[0]["transcript"], ds[0]["switch_type"])
print(ds[0]["tokens"])   # per-word hil/tl/en tags`}</Code>
          <p className="body">
            Reproduce the whole benchmark with no local setup:&nbsp;
            <a className="ilink" href={COLAB} target="_blank" rel="noreferrer">open the Colab</a> and
            choose Runtime &rarr; Run all. Or run it locally:
          </p>
          <Code>{`python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions`}</Code>
        </section>

        <section className="glass">
          <h2>Build on it</h2>
          <p className="body">Sugidanon is a building block, not a finished product. You can:</p>
          <ul className="list">
            <li>Benchmark another model (Whisper large-v3, Meta MMS) on the same clips and compare switch penalties.</li>
            <li>Grow the corpus &mdash; add speakers and clips with the included capture and clap-splitting pipeline.</li>
            <li>Confirm the per-word tags with a native speaker to harden the switch/monolingual split.</li>
            <li>Fine-tune an open multilingual model toward Hiligaynon, keeping this set as a frozen test.</li>
            <li>Extend it into a full speech-to-text, translation, and text-to-speech pipeline for Ilonggo.</li>
          </ul>
        </section>

        <section className="glass">
          <h2>Why this matters</h2>
          <p className="body">
            The Philippines has more than 130 languages. Tagalog speech
            recognition has advanced; regional tongues like Hiligaynon, Cebuano,
            and Waray still lack open datasets, benchmarks, and models. Real
            Ilonggo speech constantly mixes Hiligaynon, Tagalog, and English &mdash;
            exactly where generic systems break. Sugidanon turns that invisible
            failure into a number the next developer can build against.
          </p>
        </section>

        <footer className="foot">
          <p>
            Recorded and reviewed by <strong>Aziel Faith Agustin</strong>
            (Hiligaynon speaker). Built by Team Hague for ACM TechSprint Asteria 2026.
          </p>
          <p className="fine">
            Data: CC BY 4.0 &middot; Code: MIT &middot;{" "}
            <a className="ilink" href={HF} target="_blank" rel="noreferrer">Hugging Face</a> &middot;{" "}
            <a className="ilink" href={GITHUB} target="_blank" rel="noreferrer">GitHub</a> &middot;{" "}
            <a className="ilink" href={COLAB} target="_blank" rel="noreferrer">Colab</a>
          </p>
        </footer>
      </main>

      <style jsx>{`
        .page {
          min-height: 100vh; color: #f3f6fc;
          background:
            radial-gradient(80% 70% at 12% 0%, rgba(56,140,255,.30), transparent 55%),
            radial-gradient(70% 60% at 100% 8%, rgba(150,110,255,.28), transparent 55%),
            radial-gradient(80% 70% at 80% 100%, rgba(35,200,190,.22), transparent 55%),
            #0a0e1c;
          background-attachment: fixed;
        }
        .wrap { max-width: 940px; margin: 0 auto; padding: 56px 20px 72px; display: flex; flex-direction: column; gap: 18px; }

        .glass {
          background: rgba(20,28,48,.55);
          backdrop-filter: blur(18px) saturate(140%);
          -webkit-backdrop-filter: blur(18px) saturate(140%);
          border: 1px solid rgba(255,255,255,.12);
          border-radius: 20px;
          padding: 30px 34px;
        }

        .hero { text-align: left; }
        .kicker { text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; color: #9fc0ff; margin: 0 0 12px; font-weight: 600; }
        h1 { font-size: 2.9rem; margin: 0 0 14px; letter-spacing: -.02em; color: #ffffff; font-weight: 700; }
        .lede { font-size: 1.16rem; line-height: 1.6; color: #dbe3f4; margin: 0 0 22px; max-width: 62ch; }
        .links { display: flex; flex-wrap: wrap; gap: 12px; }
        .pill {
          display: inline-block; padding: 11px 18px; border-radius: 999px;
          border: 1px solid rgba(255,255,255,.20); color: #f3f6fc; text-decoration: none;
          font-weight: 600; font-size: .95rem; background: rgba(255,255,255,.08);
          transition: background .15s ease;
        }
        .pill:hover { background: rgba(255,255,255,.16); }
        .pill.primary { border-color: transparent; color: #06121f;
          background: linear-gradient(90deg,#73c8ff,#54e0c6); }

        h2 { font-size: 1.5rem; margin: 0 0 14px; letter-spacing: -.01em; color: #ffffff; }
        .eyebrow { display: inline-block; text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; color: #7cc4ff; margin-bottom: 12px; font-weight: 600; }
        .punch { font-size: 1.65rem; line-height: 1.35; margin: 0 0 16px; letter-spacing: -.01em; color: #ffffff; font-weight: 700; }
        .plain { font-size: 1.05rem; line-height: 1.65; color: #dbe3f4; margin: 0 0 26px; max-width: 70ch; }
        .plain strong, .punch strong { color: #ffffff; }
        .body { font-size: 1rem; line-height: 1.65; color: #d4dcee; margin: 0 0 14px; max-width: 72ch; }

        .bars { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 6px 0 24px; }
        .barcol h3 { font-size: 1.02rem; margin: 0 0 4px; color: #ffffff; }
        .colsub { font-size: .86rem; color: #aab8d4; margin: 0 0 18px; line-height: 1.45; }
        .bar { margin: 0 0 16px; }
        .barhead { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; gap: 10px; }
        .barlabel { font-size: .94rem; color: #eaf0fb; }
        .barval { font-size: 1.02rem; font-weight: 700; white-space: nowrap; }
        .bartrack { height: 12px; border-radius: 999px; background: rgba(255,255,255,.10); overflow: hidden; }
        .barfill { height: 100%; border-radius: 999px; transition: width .6s ease; }
        .barnote { display: block; font-size: .8rem; color: #9aa9c6; margin-top: 5px; }

        .takeaway { font-size: 1rem; line-height: 1.62; color: #eef2fb; padding: 18px 20px;
          border-radius: 14px; background: rgba(90,150,255,.14); border: 1px solid rgba(120,170,255,.28); }
        .takeaway strong { color: #ffffff; }
        .fine { display: block; margin-top: 8px; font-size: .82rem; color: #a6b3cf; }

        .chips { display: flex; flex-wrap: wrap; gap: 12px; margin: 0 0 18px; }
        .chip { flex: 1 1 140px; border-radius: 14px; padding: 16px 18px;
          background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.12); }
        .chip strong { display: block; font-size: 1.5rem; color: #ffffff; }
        .chip span { font-size: .82rem; color: #b6c2da; }

        .list { margin: 0; padding-left: 20px; line-height: 1.7; color: #d4dcee; }
        .list li { margin: 6px 0; }

        .ilink { color: #7cc4ff; text-decoration: none; border-bottom: 1px solid rgba(124,196,255,.45); }
        .ilink:hover { border-color: #7cc4ff; }

        .code {
          background: rgba(4,8,18,.72); border: 1px solid rgba(255,255,255,.10);
          border-radius: 12px; padding: 16px 18px; overflow-x: auto;
          font-size: .85rem; line-height: 1.55; color: #d7e6ff; margin: 0 0 14px;
        }
        .code code { background: none; }

        .foot { padding: 6px 6px 0; color: #b6c2da; font-size: .95rem; line-height: 1.6; }
        .foot a { color: #7cc4ff; }
        .foot strong { color: #f3f6fc; }

        @media (max-width: 720px) {
          h1 { font-size: 2.1rem; }
          .punch { font-size: 1.32rem; }
          .bars { grid-template-columns: 1fr; gap: 20px; }
          .glass { padding: 24px 20px; }
        }
      `}</style>
    </div>
  );
}
