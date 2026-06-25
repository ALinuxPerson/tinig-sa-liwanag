import { useMemo, useState } from "react";

const samples = [
  {
    label: "Health",
    text: "Please call the doctor if the child has a fever tonight.",
  },
  {
    label: "Education",
    text: "The class was cancelled because the rain was strong, but students should read the module at home.",
  },
  {
    label: "Emergency",
    text: "Do not cross the bridge because the water is rising quickly.",
  },
  {
    label: "Code-switching",
    text: "Kung nahihilo ka, sit down anay and drink water.",
  },
  {
    label: "Tagalog",
    text: "Kailangan ko ng tulong.",
  },
  {
    label: "Tagalog health",
    text: "Nasaan ang ospital?",
  },
  {
    label: "Public service",
    text: "If you cannot read the form, ask the staff for help.",
  },
  {
    label: "Daily life",
    text: "I left the key on the table, not inside the bag.",
  },
];

const metrics = [
  ["Seed rows", "30"],
  ["Coverage", "100.0%"],
  ["Token F1", "30.9%"],
  ["chrF", "34.7%"],
];

export default function Home() {
  const [source, setSource] = useState("");
  const [translation, setTranslation] = useState("");
  const [backend, setBackend] = useState("");
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const canTranslate = useMemo(() => source.trim().length > 0 && !loading, [source, loading]);

  async function translate(nextSource = source) {
    const text = nextSource.trim();
    if (!text) {
      setTranslation("");
      return;
    }

    setLoading(true);
    setError("");
    setTranslation("");
    setBackend("");
    setNote("");

    try {
      const response = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Translation failed");
      setTranslation(data.translation || "");
      setBackend(data.backend || "");
      setNote(data.note || "");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function chooseSample(text) {
    setSource(text);
    translate(text);
  }

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Context-aware Hiligaynon translation MVP</p>
          <h1>Tinig sa Liwanag</h1>
          <p className="lede">
            A reproducible benchmark scaffold, dictionary baseline, evaluator, and demo for
            English, Filipino, and code-switched text into Hiligaynon.
          </p>
        </div>
        <div className="statusPanel" aria-label="Current benchmark status">
          {metrics.map(([label, value]) => (
            <div key={label}>
              <span>{label}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="notice">
        <strong>Hackathon scope:</strong> translations are marked seed_unverified until
        reviewed by native Hiligaynon speakers. This demo intentionally shows a weak
        dictionary baseline so the context gap is visible.
      </section>

      <section className="translator" aria-label="Translation demo">
        <div className="pane">
          <label htmlFor="source">Source text</label>
          <textarea
            id="source"
            value={source}
            onChange={(event) => setSource(event.target.value)}
            onKeyDown={(event) => {
              if ((event.metaKey || event.ctrlKey) && event.key === "Enter") translate();
            }}
            placeholder="Type English, Filipino, or code-switched text..."
          />
        </div>
        <div className="pane">
          <label>Hiligaynon output</label>
          <div className="output" aria-live="polite">
            {loading ? "Translating..." : error || translation || "Translation appears here"}
          </div>
          {(backend || note) && !loading && !error ? (
            <div className="resultMeta">
              {backend ? <span>{backend}</span> : null}
              {note ? <p>{note}</p> : null}
            </div>
          ) : null}
        </div>
      </section>

      <div className="actions">
        <button type="button" onClick={() => translate()} disabled={!canTranslate}>
          Translate
        </button>
        <span>Seed prompts return seed references; other text uses the expanded dictionary fallback.</span>
      </div>

      <section className="samples" aria-label="Benchmark seed prompts">
        {samples.map((sample) => (
          <button key={sample.label} type="button" onClick={() => chooseSample(sample.text)}>
            <span>{sample.label}</span>
            {sample.text}
          </button>
        ))}
      </section>
    </main>
  );
}
