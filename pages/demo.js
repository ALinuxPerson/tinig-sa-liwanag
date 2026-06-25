import { useMemo, useState } from "react";
import Link from "next/link";

const samples = [
  { label: "Health", text: "Please call the doctor if the child has a fever tonight." },
  { label: "Education", text: "The class was cancelled because the rain was strong, but students should read the module at home." },
  { label: "Emergency", text: "Do not cross the bridge because the water is rising quickly." },
  { label: "Code-switching", text: "Kung nahihilo ka, sit down anay and drink water." },
  { label: "Tagalog", text: "Kailangan ko ng tulong." },
  { label: "Tagalog health", text: "Nasaan ang ospital?" },
  { label: "Public service", text: "If you cannot read the form, ask the staff for help." },
  { label: "Daily life", text: "I left the key on the table, not inside the bag." },
];

export default function Demo() {
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
          <p className="eyebrow"><Link href="/">← Back to Sugidanon</Link></p>
          <h1>Translation demo</h1>
          <p className="lede">
            Context-aware English / Filipino / code-switched text into Hiligaynon. An
            extension layer on top of the speech benchmark — not the research artifact.
          </p>
        </div>
      </section>

      <section className="notice">
        <strong>Hackathon scope:</strong> local runs can use Ollama for context-aware
        translation after seed and curated phrase checks. Vercel uses seed, phrase, and
        dictionary baselines because it cannot access your machine's Ollama daemon.
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
        <span>Backend order: seed references, curated phrases, Ollama context LLM, dictionary fallback.</span>
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
