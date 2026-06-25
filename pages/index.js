import Link from "next/link";

const HF = "https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch";
const COLAB = "https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb";
const GITHUB = "https://github.com/Jazztinn/tinig-sa-liwanag";

const results = [
  ["Overall WER", "59.8%"],
  ["Monolingual (Hiligaynon)", "66.3%"],
  ["Switch-region", "36.4%"],
  ["Switch penalty", "−30.0%"],
];

const pairs = [
  ["hil ↔ en", "40.8%"],
  ["hil ↔ tl", "24.4%"],
  ["tl ↔ en", "6.2%"],
];

function Code({ children }) {
  return <pre className="code"><code>{children}</code></pre>;
}

export default function Home() {
  return (
    <main className="doc">
      <header className="top">
        <p className="eyebrow">Open speech benchmark · Hiligaynon (Ilonggo)</p>
        <h1>Sugidanon 🎙️</h1>
        <p className="tagline">
          The first openly-licensed, <strong>code-switch-labeled speech benchmark</strong> for
          Hiligaynon — a language spoken by 9M+ Filipinos yet nearly invisible to modern
          speech technology.
        </p>
        <nav className="links">
          <a className="btn primary" href={COLAB} target="_blank" rel="noreferrer">▶ Run the benchmark (Colab)</a>
          <a className="btn" href={HF} target="_blank" rel="noreferrer">📦 Dataset (Hugging Face)</a>
          <a className="btn" href={GITHUB} target="_blank" rel="noreferrer">💻 Code (GitHub)</a>
          <Link className="btn" href="/demo">🗣 Translation demo</Link>
        </nav>
      </header>

      <section className="card finding">
        <h2>The finding</h2>
        <p>
          Run an off-the-shelf Tagalog ASR model (Whisper) on real Ilonggo speech and it
          <strong> catches the borrowed English/Tagalog words but misses the Hiligaynon.</strong>
          Sugidanon makes that gap measurable with a <em>switch penalty</em>: WER at the moment
          the language switches, minus WER on monolingual words.
        </p>
        <div className="grid">
          <table>
            <tbody>
              {results.map(([k, v]) => (
                <tr key={k}><td>{k}</td><td><strong>{v}</strong></td></tr>
              ))}
            </tbody>
          </table>
          <table>
            <thead><tr><td>switch by pair</td><td>WER</td></tr></thead>
            <tbody>
              {pairs.map(([k, v]) => (
                <tr key={k}><td>{k}</td><td><strong>{v}</strong></td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="muted">
          Negative penalty = switch words scored <em>better</em> than monolingual ones: the
          model knows the loanwords, not the Ilonggo matrix. <code>tl↔en</code> is near-solved
          (6%); <code>hil↔en</code> is worst (41%). The gap scales with Hiligaynon.
          Baseline: Whisper small, single speaker — preliminary.
        </p>
      </section>

      <section className="card">
        <h2>What&apos;s inside</h2>
        <ul>
          <li><strong>40 code-switch clips</strong> (~3.1 min), one Hiligaynon speaker.</li>
          <li><strong>8 domains:</strong> market, transport, school/work, family, health,
            culture, everyday, oral tradition / heritage.</li>
          <li><strong>4 switch types:</strong> <code>HIL</code>, <code>HIL+EN</code>,
            <code>HIL+TL</code>, <code>HIL+TL+EN</code>.</li>
          <li><strong>Per-word language tags</strong> (<code>hil</code>/<code>tl</code>/<code>en</code>)
            so the scorer isolates switch-region errors.</li>
          <li>Transcripts reviewed by the speaker; per-word tags auto-seeded, pending a
            confirmation pass. CC BY 4.0.</li>
        </ul>
      </section>

      <section className="card">
        <h2>Use it</h2>
        <p><strong>Load the dataset</strong> (one line, audiofolder layout):</p>
        <Code>{`from datasets import load_dataset

ds = load_dataset("LauelKills/sugidanon-hil-codeswitch",
                  data_dir="data/audio", split="train")
print(ds[0]["transcript"], ds[0]["switch_type"])
print(ds[0]["tokens"])   # per-word hil/tl/en tags`}</Code>

        <p><strong>Reproduce the benchmark</strong> — one click, no setup:&nbsp;
          <a href={COLAB} target="_blank" rel="noreferrer">open the Colab</a> → Runtime → Run all.</p>

        <p><strong>Or locally</strong> (clone the repo first):</p>
        <Code>{`python3 scripts/validate.py --kind asr --dir data/annotations
python3 scripts/run_whisper.py --model small --language tl
python3 score.py --ref data/annotations --hyp data/predictions`}</Code>
      </section>

      <section className="card">
        <h2>Build on it</h2>
        <p>Sugidanon is a building block, not a finished product. Ways to extend:</p>
        <ul>
          <li><strong>Benchmark another model.</strong> Run Whisper <code>large-v3</code> or
            Meta MMS, drop predictions in <code>data/predictions/asr/&lt;model&gt;/</code>, then
            <code> python3 scripts/eval_asr_baselines.py</code> for a side-by-side table.</li>
          <li><strong>Grow the corpus.</strong> Add speakers/clips with the capture pipeline:
            edit the elicitation set, record with <code>scripts/record.py</code> (or batch-split
            a session via <code>scripts/split_claps.py</code>).</li>
          <li><strong>Confirm the labels.</strong> Have a Hiligaynon speaker verify the per-word
            tags, flip <code>lang_tags_status</code> to <code>reviewed</code> — then the
            switch/monolingual split is gold.</li>
          <li><strong>Fine-tune.</strong> Use the reviewed split as eval while adapting an open
            multilingual model toward Hiligaynon; keep this test set frozen.</li>
          <li><strong>Extend to a pipeline.</strong> Reuse the corpus as the speech component of
            STT → translation → TTS for Ilonggo.</li>
        </ul>
      </section>

      <section className="card">
        <h2>Why it matters</h2>
        <p>
          The Philippines has 130+ languages. Tagalog speech recognition has advanced;
          regional tongues like Hiligaynon, Cebuano, and Waray still lack open datasets,
          benchmarks, and models. Real Ilonggo speech constantly mixes Hiligaynon, Tagalog,
          and English — exactly where generic systems break. Sugidanon turns that invisible
          failure into a number the next developer can build against.
        </p>
      </section>

      <footer className="foot">
        <p>
          <strong>Acknowledgments.</strong> Recorded and reviewed by <strong>Aziel Faith
          Agustin</strong> (Hiligaynon speaker). Built by Team Hague for ACM TechSprint
          Asteria 2026.
        </p>
        <p className="muted">
          Data: CC BY 4.0 · Code: MIT ·&nbsp;
          <a href={HF} target="_blank" rel="noreferrer">Hugging Face</a> ·&nbsp;
          <a href={GITHUB} target="_blank" rel="noreferrer">GitHub</a> ·&nbsp;
          <a href={COLAB} target="_blank" rel="noreferrer">Colab</a>
        </p>
      </footer>

      <style jsx>{`
        .doc { max-width: 900px; margin: 0 auto; padding: 48px 24px 80px; }
        .top { margin-bottom: 32px; }
        .eyebrow { text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; opacity: .7; margin: 0 0 8px; }
        h1 { font-size: 2.6rem; margin: 0 0 12px; }
        .tagline { font-size: 1.15rem; line-height: 1.55; opacity: .92; margin: 0 0 24px; }
        .links { display: flex; flex-wrap: wrap; gap: 10px; }
        .btn { display: inline-block; padding: 10px 16px; border-radius: 10px; border: 1px solid rgba(127,127,127,.35);
               text-decoration: none; font-weight: 600; font-size: .95rem; }
        .btn.primary { background: #ff6b4a; color: #fff; border-color: #ff6b4a; }
        .card { border: 1px solid rgba(127,127,127,.25); border-radius: 16px; padding: 24px 28px; margin: 18px 0; }
        .card h2 { margin: 0 0 12px; font-size: 1.4rem; }
        .card p { line-height: 1.6; margin: 0 0 12px; }
        .card ul { line-height: 1.65; padding-left: 20px; margin: 0; }
        .card li { margin: 6px 0; }
        .finding .grid { display: flex; flex-wrap: wrap; gap: 24px; margin: 8px 0 12px; }
        table { border-collapse: collapse; }
        td { padding: 6px 18px 6px 0; vertical-align: top; }
        thead td { opacity: .6; font-size: .8rem; text-transform: uppercase; letter-spacing: .05em; }
        .muted { opacity: .7; font-size: .92rem; }
        code { background: rgba(127,127,127,.18); padding: 1px 6px; border-radius: 5px; font-size: .88em; }
        .code { background: rgba(127,127,127,.12); border: 1px solid rgba(127,127,127,.2);
                border-radius: 10px; padding: 16px; overflow-x: auto; font-size: .85rem; line-height: 1.5; }
        .code code { background: none; padding: 0; }
        .foot { margin-top: 28px; border-top: 1px solid rgba(127,127,127,.25); padding-top: 20px; }
        .foot a { color: inherit; }
        @media (max-width: 600px) { h1 { font-size: 2rem; } .doc { padding: 28px 16px 60px; } }
      `}</style>
    </main>
  );
}
