import Head from "next/head";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { useEffect, useMemo, useRef, useState } from "react";
import SegmentedFilter from "../components/SegmentedFilter";

const SWITCH_TYPES = ["HIL", "HIL+EN", "HIL+TL", "HIL+TL+EN"];
const FEATURED_CLIP = "hil_cs_038";
const WAVEFORM_BARS = 36;

function formatPenalty(value) {
  return `${value < 0 ? "\u2212" : ""}${Math.abs(value).toFixed(1)}%`;
}

function pct(value) {
  return `${Number(value).toFixed(1)}%`;
}

function Token({ t, reveal = false, revealIndex = 0, reduceMotion = false, showSwitch = true }) {
  const [tip, setTip] = useState(null);
  const ref = useRef(null);
  const resultClass = t.error === true ? "tokErr" : t.error === false ? "tokOk" : "tokPending";
  const cls = ["tok", showSwitch && t.switch ? "tokSwitch" : "", resultClass].join(" ");
  const label = [
    t.error === true ? "ASR error" : t.error === false ? "correct" : "not scored",
    t.switch ? "switch region" : "monolingual",
    `lang: ${t.lang}`,
  ].join(" / ");

  function handleEnter(e) {
    const rect = ref.current.getBoundingClientRect();
    const mid = rect.top + rect.height / 2;
    setTip(e.clientY < mid ? "above" : "below");
  }

  const content = (
    <>
      {t.text}
      {tip && (
        <span className={`tip tip${tip === "above" ? "Above" : "Below"}`}>
          {label}
        </span>
      )}
    </>
  );

  if (reveal) {
    return (
      <motion.span
        ref={ref}
        className={cls}
        onMouseEnter={handleEnter}
        onMouseLeave={() => setTip(null)}
        initial={{ opacity: reduceMotion ? 1 : 0, y: reduceMotion ? 0 : 10, filter: reduceMotion ? "none" : "blur(4px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        transition={{
          delay: reduceMotion ? 0 : revealIndex * 0.04,
          duration: reduceMotion ? 0 : 0.24,
          ease: [0.22, 1, 0.36, 1],
        }}
      >
        {content}
      </motion.span>
    );
  }

  return (
    <span
      ref={ref}
      className={cls}
      onMouseEnter={handleEnter}
      onMouseLeave={() => setTip(null)}
    >
      {content}
    </span>
  );
}

function TopNav({ version }) {
  const links = [
    {
      label: "GitHub",
      href: "https://github.com/Jazztinn/tinig-sa-liwanag",
      icon: (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M12 2.4c-5.4 0-9.8 4.4-9.8 9.8 0 4.3 2.8 8 6.7 9.3.5.1.7-.2.7-.5v-1.9c-2.7.6-3.3-1.2-3.3-1.2-.4-1.1-1.1-1.4-1.1-1.4-.9-.6.1-.6.1-.6 1 0 1.6 1.1 1.6 1.1.9 1.5 2.4 1.1 3 .8.1-.7.4-1.1.7-1.4-2.2-.2-4.5-1.1-4.5-4.8 0-1.1.4-1.9 1-2.6-.1-.2-.4-1.2.1-2.5 0 0 .8-.3 2.7 1 .8-.2 1.6-.3 2.5-.3s1.7.1 2.5.3c1.9-1.3 2.7-1 2.7-1 .5 1.3.2 2.3.1 2.5.6.7 1 1.5 1 2.6 0 3.8-2.3 4.6-4.5 4.8.4.3.7.9.7 1.8V21c0 .3.2.6.7.5 3.9-1.3 6.7-5 6.7-9.3 0-5.4-4.4-9.8-9.8-9.8Z" />
        </svg>
      ),
    },
    {
      label: "Hugging Face",
      href: "https://huggingface.co/datasets/LauelKills/sugidanon-hil-codeswitch",
      icon: <span aria-hidden="true">HF</span>,
    },
    {
      label: "Google Colab",
      href: "https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb",
      icon: (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M8.1 15.7c-2.1 0-3.8-1.7-3.8-3.8s1.7-3.8 3.8-3.8c1.1 0 2 .4 2.7 1.2l1.7-1.7a6.2 6.2 0 1 0 0 8.6l-1.7-1.7a3.6 3.6 0 0 1-2.7 1.2Zm7.8-7.6c-1.1 0-2 .4-2.7 1.2l1.7 1.7a3.6 3.6 0 0 1 2.7-1.2c2.1 0 3.8 1.7 3.8 3.8s-1.7 3.8-3.8 3.8c-1.1 0-2-.4-2.7-1.2l-1.7 1.7a6.2 6.2 0 1 0 2.7-9.8Z" />
        </svg>
      ),
    },
  ];

  return (
    <header className="topNav" aria-label="Site navigation">
      <a className="navBrand" href="#top" aria-label="Sugidanon home">
        <img src="/logo.png" alt="" />
        <span>Sugidanon</span>
      </a>
      <div className="resourceLinks" aria-label={`External resources for v${version}`}>
        {links.map((link) => (
          <a
            key={link.label}
            className="resourceButton"
            href={link.href}
            target="_blank"
            rel="noreferrer"
            aria-label={link.label}
            title={link.label}
          >
            {link.icon}
          </a>
        ))}
      </div>
    </header>
  );
}

function DossierNote() {
  return (
    <aside className="pinnedNote" aria-label="Sugidanon name note">
      <span className="tape tapeOne" />
      <span className="tape tapeTwo" />
      <h2>Sugidanon</h2>
      <p>
        Named for <em>sugid</em> (story) + <em>-anon</em> (people). Stories
        carry language; we measure when systems miss it.
      </p>
      <div className="etching" aria-hidden="true">
        <span />
      </div>
    </aside>
  );
}

function MetricGauge({ label, value, tone = "ink" }) {
  return (
    <div className={`metricGauge gauge-${tone}`}>
      <div className="gaugeTitle">
        <span>{label}</span>
      </div>
      <div className="gaugeRing" aria-hidden="true">
        <strong>{pct(value)}</strong>
      </div>
    </div>
  );
}

function BaselinePanel({ h, model }) {
  return (
    <section className="baselinePanel" aria-label="Baseline reference">
      <div className="baselineModel">
        <span className="railLabel">Baseline reference</span>
        <h2>Whisper small, forced tl</h2>
        <p>OpenAI Whisper small</p>
        <p>Forced decoder: Tagalog (tl)</p>
        <p>Decoding: greedy</p>
        <p>Model id: {model}</p>
      </div>
      <MetricGauge label="Overall" value={h.overall} />
      <MetricGauge label="Hiligaynon" value={h.mono} tone="rust" />
      <MetricGauge label="Switch-region" value={h.switch} tone="ochre" />
      <div className="penaltyCard">
        <span>Matrix-Language Erasure Gap</span>
        <strong>{formatPenalty(h.penalty)}</strong>
        <p>Switch-region WER minus Hiligaynon WER. Negative means borrowed words survive better.</p>
      </div>
    </section>
  );
}

function blobToDataUrl(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

function preferredRecorderMimeType() {
  if (typeof MediaRecorder === "undefined") return undefined;
  return ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/wav"].find((type) =>
    MediaRecorder.isTypeSupported(type)
  );
}

function parseRecordingDataUrl(dataUrl, fallbackMimeType, blobSize) {
  const value = String(dataUrl || "");
  const commaIndex = value.indexOf(",");
  const meta = commaIndex >= 0 ? value.slice(5, commaIndex) : "";
  const audioBase64 = commaIndex >= 0 ? value.slice(commaIndex + 1).replace(/\s+/g, "") : "";
  const metaParts = meta.split(";").filter(Boolean);
  const dataUrlMimeType = metaParts.find((part) => part.includes("/")) || "";
  const hasBase64Flag = metaParts.some((part) => part.toLowerCase() === "base64");

  if (!value.startsWith("data:") || commaIndex < 0 || !hasBase64Flag || !audioBase64) {
    const prefix = value ? value.slice(0, 32) : "empty";
    throw new Error(
      `Recorder produced invalid audio payload (${fallbackMimeType || "no type"}, ${blobSize || 0} bytes, ${prefix}).`
    );
  }

  return {
    mimeType: fallbackMimeType || dataUrlMimeType || "audio/webm",
    audioBase64,
  };
}

function normalizeTokenForWer(text) {
  return String(text || "")
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{N}_'-]/gu, "");
}

function transcriptWordList(text) {
  return String(text || "")
    .split(/\s+/)
    .map(normalizeTokenForWer)
    .filter(Boolean);
}

function alignWords(refWords, hypWords) {
  const rows = refWords.length + 1;
  const cols = hypWords.length + 1;
  const dp = Array.from({ length: rows }, () => Array(cols).fill(0));

  for (let i = 0; i < rows; i += 1) dp[i][0] = i;
  for (let j = 0; j < cols; j += 1) dp[0][j] = j;

  for (let i = 1; i < rows; i += 1) {
    for (let j = 1; j < cols; j += 1) {
      const subCost = refWords[i - 1] === hypWords[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1,
        dp[i][j - 1] + 1,
        dp[i - 1][j - 1] + subCost
      );
    }
  }

  const ops = [];
  let i = refWords.length;
  let j = hypWords.length;

  while (i > 0 || j > 0) {
    if (i > 0 && j > 0) {
      const subCost = refWords[i - 1] === hypWords[j - 1] ? 0 : 1;
      if (dp[i][j] === dp[i - 1][j - 1] + subCost) {
        ops.push({ type: subCost ? "sub" : "match", refIndex: i - 1 });
        i -= 1;
        j -= 1;
        continue;
      }
    }
    if (i > 0 && dp[i][j] === dp[i - 1][j] + 1) {
      ops.push({ type: "del", refIndex: i - 1 });
      i -= 1;
      continue;
    }
    ops.push({ type: "ins", refIndex: i > 0 ? i - 1 : 0 });
    j -= 1;
  }

  return ops.reverse();
}

function scoreTranscript(clip, transcript) {
  const refItems = clip.tokens
    .map((token, index) => ({
      index,
      word: normalizeTokenForWer(token.text),
      switch: Boolean(token.switch),
    }))
    .filter((item) => item.word);
  const refWords = refItems.map((item) => item.word);
  const hypWords = transcriptWordList(transcript);
  const switchFlags = refItems.map((item) => item.switch);

  const buckets = {
    overall: { errors: 0, total: refWords.length },
    switch: { errors: 0, total: switchFlags.filter(Boolean).length },
    mono: { errors: 0, total: switchFlags.filter((flag) => !flag).length },
  };

  for (const op of alignWords(refWords, hypWords)) {
    if (op.type === "match") continue;
    buckets.overall.errors += 1;
    if (op.type === "ins") continue;
    const bucket = switchFlags[op.refIndex] ? buckets.switch : buckets.mono;
    bucket.errors += 1;
  }

  function wer(bucket) {
    if (!bucket.total) return null;
    return (bucket.errors / bucket.total) * 100;
  }

  return {
    overall: wer(buckets.overall),
    switch: wer(buckets.switch),
    mono: wer(buckets.mono),
  };
}

function assessTranscriptTokens(clip, transcript, shouldScore) {
  const tokens = clip.tokens.map((token) => ({
    ...token,
    error: shouldScore ? false : null,
  }));

  if (!shouldScore) return tokens;

  const refItems = clip.tokens
    .map((token, index) => ({
      index,
      word: normalizeTokenForWer(token.text),
    }))
    .filter((item) => item.word);
  const refWords = refItems.map((item) => item.word);
  const hypWords = transcriptWordList(transcript);

  for (const op of alignWords(refWords, hypWords)) {
    if (op.type === "match" || op.type === "ins") continue;
    const tokenIndex = refItems[op.refIndex]?.index;
    if (typeof tokenIndex === "number") tokens[tokenIndex].error = true;
  }

  return tokens;
}

function pctOrDash(value) {
  return Number.isFinite(value) ? pct(value) : "--";
}

function emptyWaveform() {
  return Array.from({ length: WAVEFORM_BARS }, () => 0.08);
}

function SpeechDemo({ clip, model }) {
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [recordedUrl, setRecordedUrl] = useState("");
  const [transcript, setTranscript] = useState("");
  const [transcriptionMeta, setTranscriptionMeta] = useState(null);
  const [durationMs, setDurationMs] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [voiceLevel, setVoiceLevel] = useState(0);
  const [waveLevels, setWaveLevels] = useState(emptyWaveform);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameRef = useRef(0);
  const recordingStartedAtRef = useRef(0);
  const playbackAudioRef = useRef(null);
  const stopTimerRef = useRef(null);
  const urlRef = useRef("");
  const reduceMotion = useReducedMotion();

  useEffect(() => {
    return () => {
      window.clearTimeout(stopTimerRef.current);
      window.cancelAnimationFrame(animationFrameRef.current);
      streamRef.current?.getTracks().forEach((track) => track.stop());
      audioContextRef.current?.close().catch(() => {});
      playbackAudioRef.current?.pause();
      if (urlRef.current) URL.revokeObjectURL(urlRef.current);
    };
  }, []);

  if (!clip) return null;

  function resetPlayback() {
    if (playbackAudioRef.current) {
      playbackAudioRef.current.pause();
      playbackAudioRef.current = null;
    }
    setIsPlaying(false);
  }

  function stopLiveInput() {
    window.cancelAnimationFrame(animationFrameRef.current);
    animationFrameRef.current = 0;
    analyserRef.current = null;
    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  }

  function drawVoiceLevel() {
    const analyser = analyserRef.current;
    if (!analyser) return;

    const samples = new Uint8Array(analyser.fftSize);
    analyser.getByteTimeDomainData(samples);
    let sum = 0;
    for (const sample of samples) {
      const centered = (sample - 128) / 128;
      sum += centered * centered;
    }
    const rms = Math.sqrt(sum / samples.length);
    const level = Math.min(1, rms * 5.5);

    setVoiceLevel(level);
    setWaveLevels((levels) => [...levels.slice(1), Math.max(0.06, level)]);
    setDurationMs(Date.now() - recordingStartedAtRef.current);
    animationFrameRef.current = window.requestAnimationFrame(drawVoiceLevel);
  }

  async function startRecording() {
    setError("");
    setRecordedUrl("");
    setTranscript("");
    setTranscriptionMeta(null);
    setDurationMs(0);
    setVoiceLevel(0);
    setWaveLevels(emptyWaveform());
    setIsPlaying(false);
    resetPlayback();
    if (urlRef.current) {
      URL.revokeObjectURL(urlRef.current);
      urlRef.current = "";
    }

    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      setStatus("error");
      setError("Mic recording is not available in this browser.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: true, noiseSuppression: true },
      });
      streamRef.current = stream;
      const mimeType = preferredRecorderMimeType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextCtor) {
        throw new Error("Voice meter is not available in this browser.");
      }
      const audioContext = new AudioContextCtor();
      await audioContext.resume();
      const source = audioContext.createMediaStreamSource(stream);
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);

      mediaRecorderRef.current = recorder;
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data?.size) chunksRef.current.push(event.data);
      };
      recorder.onstop = () => {
        window.clearTimeout(stopTimerRef.current);
        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || mimeType || "audio/webm" });
        chunksRef.current = [];
        mediaRecorderRef.current = null;
        stopLiveInput();
        setVoiceLevel(0);
        const nextUrl = URL.createObjectURL(blob);
        if (urlRef.current) URL.revokeObjectURL(urlRef.current);
        urlRef.current = nextUrl;
        setRecordedUrl(nextUrl);
        transcribeRecording(blob);
      };

      setStatus("recording");
      recordingStartedAtRef.current = Date.now();
      recorder.start(120);
      drawVoiceLevel();
      stopTimerRef.current = window.setTimeout(() => {
        if (recorder.state === "recording") recorder.stop();
      }, 9000);
    } catch {
      stopLiveInput();
      setStatus("error");
      setError("Mic permission was blocked or no input device was found.");
    }
  }

  async function transcribeRecording(blob) {
    setError("");
    setStatus("analyzing");

    try {
      if (!(blob instanceof Blob)) {
        throw new Error("Recorder did not return an audio blob.");
      }
      if (!blob.size) {
        throw new Error(`Recorder returned empty audio (${blob.type || "no type"}).`);
      }
      const audio = await blobToDataUrl(blob);
      const payload = parseRecordingDataUrl(audio, blob.type, blob.size);
      const response = await fetch("/api/transcribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          audioBase64: payload.audioBase64,
          mimeType: payload.mimeType,
          reference: clip.reference,
        }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || "Transcription failed.");
      }

      setTranscript(String(data.text || "").trim());
      setTranscriptionMeta({
        backend: data.backend || "hf-space-whisper",
        model: data.model || model,
      });
      setStatus("complete");
    } catch (err) {
      setStatus("error");
      setError(err.message || "Model transcription failed.");
    }
  }

  function stopRecording() {
    const recorder = mediaRecorderRef.current;
    if (recorder?.state === "recording") recorder.stop();
  }

  function togglePlayback() {
    if (!recordedUrl) return;
    if (!playbackAudioRef.current) {
      const audio = new Audio(recordedUrl);
      audio.onended = () => setIsPlaying(false);
      audio.onpause = () => setIsPlaying(false);
      audio.onplay = () => setIsPlaying(true);
      playbackAudioRef.current = audio;
    }
    if (isPlaying) {
      playbackAudioRef.current.pause();
    } else {
      playbackAudioRef.current.play().catch(() => setError("Playback could not start."));
    }
  }

  const isRecording = status === "recording";
  const isAnalyzing = status === "analyzing";
  const isComplete = status === "complete";
  const canRecord = !isRecording && !isAnalyzing;
  const demoMetrics = isComplete ? scoreTranscript(clip, transcript) : null;
  const assessedTokens = assessTranscriptTokens(clip, transcript, isComplete);
  const transcriptAccuracy = demoMetrics ? Math.max(0, 100 - Number(demoMetrics.overall || 0)) : null;
  const outputText = isComplete
    ? transcript || "No speech detected."
    : error
      ? "Transcript unavailable."
      : "Live transcript appears after recording.";

  return (
    <section className="speechDemo" aria-labelledby="speech-demo-title">
      <div className="speechDemoIntro">
        <span className="railLabel">Try the hosted model</span>
        <h2 id="speech-demo-title">Say anything in Hiligaynon</h2>
        <p>Press the mic and speak in Hiligaynon or code-switched Hiligaynon; the hosted Space transcribes it with Whisper.</p>
        <div className="demoPreset" aria-label={`Reference prompt benchmark: ${clip.reference}`}>
          <span>Reference prompt / benchmark</span>
          <div>
            {clip.reference
              .replace(/[.!?]+$/u, "")
              .split(/\s+/)
              .map((word) => (
                <b key={word}>{word}</b>
              ))}
          </div>
        </div>
      </div>

      <div className="demoRecorder" aria-live="polite">
        <button
          className={`micButton ${isRecording ? "micRecording" : ""}`}
          type="button"
          onClick={isRecording ? stopRecording : startRecording}
          disabled={!canRecord && !isRecording}
          aria-label={isRecording ? "Stop recording" : "Start recording"}
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 14.4c1.9 0 3.4-1.5 3.4-3.4V6.8a3.4 3.4 0 0 0-6.8 0V11c0 1.9 1.5 3.4 3.4 3.4Zm5.8-3.5a.9.9 0 0 0-1.8 0 4 4 0 0 1-8 0 .9.9 0 0 0-1.8 0 5.8 5.8 0 0 0 4.9 5.7v2.1H8.7a.9.9 0 1 0 0 1.8h6.6a.9.9 0 1 0 0-1.8h-2.4v-2.1a5.8 5.8 0 0 0 4.9-5.7Z" />
          </svg>
        </button>
        <div>
          <strong>
            {isRecording ? "Recording" : isAnalyzing ? "Analyzing" : isComplete ? "Analysis ready" : "Mic ready"}
          </strong>
          <span>
            {isRecording
              ? "Speak in Hiligaynon."
              : isAnalyzing
                ? "Model pass running."
                : isComplete
                  ? `${(durationMs / 1000).toFixed(1)}s captured and processed.`
                  : "Press mic to begin."}
          </span>
        </div>
        <div className={`recorderWaveform ${isRecording ? "waveRecording" : ""}`} aria-label="Recording voice level">
          <div className="waveBars" aria-hidden="true">
            {waveLevels.map((level, i) => (
              <span
                key={i}
                style={{
                  transform: `scaleY(${Math.max(0.08, level)})`,
                  opacity: isRecording ? 0.42 + Math.min(0.58, level) : 0.34,
                }}
              />
            ))}
          </div>
        </div>
        <div className="playbackRow">
          <button
            type="button"
            className="playbackButton"
            onClick={togglePlayback}
            disabled={!recordedUrl}
            aria-label={isPlaying ? "Stop playback" : "Play recording"}
            title={isPlaying ? "Stop playback" : "Play recording"}
          >
            {isPlaying ? (
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M7.5 6.5h9v11h-9z" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M8 5.6v12.8L18.2 12 8 5.6Z" />
              </svg>
            )}
          </button>
          <span>{recordedUrl ? "Captured audio ready" : "Playback appears after recording"}</span>
        </div>
      </div>

      <AnimatePresence initial={false}>
        {isComplete && (
          <motion.div
            className="demoPrompt"
            initial={{ opacity: reduceMotion ? 1 : 0, y: reduceMotion ? 0 : 14 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: reduceMotion ? 1 : 0, y: reduceMotion ? 0 : -6 }}
            transition={{ duration: reduceMotion ? 0 : 0.26, ease: [0.22, 1, 0.36, 1] }}
          >
            <span className="rowLabel">Reference prompt</span>
            <div className="tokens">
              {assessedTokens.map((t, i) => (
                <Token
                  key={i}
                  t={t}
                  reveal
                  revealIndex={i}
                  reduceMotion={reduceMotion}
                  showSwitch={false}
                />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="demoResult">
        <div>
          <span className="rowLabel">Model output</span>
          <p className="pred">{outputText}</p>
          {transcriptionMeta && (
            <p className="demoMeta">
              {transcriptionMeta.backend} / {transcriptionMeta.model}
            </p>
          )}
          {isComplete && (
            <div className="accuracyStamp">
              <span>Transcript accuracy</span>
              <strong>{pctOrDash(transcriptAccuracy)}</strong>
              <small>scored against reference prompt</small>
            </div>
          )}
          {error && <p className="demoError">{error}</p>}
        </div>
        <div className="clipWer">
          <div>
            <span>Switch-region WER</span>
            <strong>{pctOrDash(demoMetrics?.switch)}</strong>
          </div>
          <div>
            <span>Hiligaynon WER</span>
            <strong>{pctOrDash(demoMetrics?.mono)}</strong>
          </div>
          <div>
            <span>Overall WER</span>
            <strong>{pctOrDash(demoMetrics?.overall)}</strong>
          </div>
        </div>
      </div>
    </section>
  );
}

function ArchiveStrip({ clips, version }) {
  return (
    <section className="archiveStrip" aria-label="Benchmark inventory">
      <a className="inspectButton" href="#clips">
        <span className="waveIcon" aria-hidden="true" />
        Inspect clips
        <b aria-hidden="true">-&gt;</b>
      </a>
      <p>Explore code-switch regions, token diffs, and per-clip metrics.</p>
      <div className="archiveFacts">
        <div>
          <span className="factIcon">01</span>
          <strong>{clips.length} clips</strong>
          <small>headline explorer</small>
        </div>
        <div>
          <span className="factIcon">02</span>
          <strong>Hiligaynon-Tagalog</strong>
          <small>natural code-switch speech</small>
        </div>
        <div>
          <span className="factIcon">03</span>
          <strong>Manual transcripts</strong>
          <small>benchmark v{version}</small>
        </div>
      </div>
    </section>
  );
}

function MiniTranscript({ clip }) {
  if (!clip) return null;

  return (
    <div className="transcriptSheet">
      <div className="clipAudio">
        <div className="clipAudioMeta">
          <span className="clipId">{clip.clip_id}</span>
          <span className="clipTime">{clip.domain}</span>
        </div>
        <audio
          controls
          preload="metadata"
          src={`/${clip.audio}`}
          className="player"
          aria-label={`Play benchmark audio for ${clip.clip_id}`}
        />
      </div>
      <div className="transcriptLines">
        <div>
          <span className="rowLabel">Reference (Hiligaynon-Tagalog)</span>
          <div className="tokens">
            {clip.tokens.map((t, i) => (
              <Token key={i} t={t} />
            ))}
          </div>
        </div>
        <div>
          <span className="rowLabel">Whisper small, forced tl</span>
          <p className="pred">{clip.prediction}</p>
        </div>
      </div>
      <aside className="clipEvidence" aria-label={`${clip.clip_id} scoring evidence`}>
        <div className="diffLegend" aria-label="Diff legend">
          <span><i className="sw swOk" />Correct</span>
          <span><i className="sw swErr" />Substitution</span>
          <span><i className="sw swSwitch" />Switch token</span>
        </div>
        <div className="clipEvidenceWer">
          <div>
            <span>Switch-region WER</span>
            <strong>{pct(clip.wer.switch)}</strong>
          </div>
          <div>
            <span>Hiligaynon WER</span>
            <strong>{pct(clip.wer.mono)}</strong>
          </div>
          <div>
            <span>Overall WER</span>
            <strong>{pct(clip.wer.overall)}</strong>
          </div>
        </div>
      </aside>
    </div>
  );
}

function PairBar({ label, value }) {
  return (
    <div className="pairRow">
      <span className="pairLabel">{label}</span>
      <div className="track" aria-hidden="true">
        <div className="fill" style={{ width: `${value}%` }} />
      </div>
      <span className="pairVal">{pct(value)}</span>
    </div>
  );
}

function EvidenceRail({ h, cohorts, version }) {
  return (
    <aside className="evidenceRail" aria-label="Evidence rail">
      <section id="leaderboard">
        <h2>Evidence rail</h2>
        <div className="railRule" />
        <span className="railLabel">Cohort ladder (WER down)</span>
        <p className="railHint">Lower is better.</p>
        <ol className="leaderList">
          {cohorts.map((c) => (
            <li key={c.name}>
              <span>{c.speaker} / {c.role}</span>
              <b>{pct(c.switch)}</b>
            </li>
          ))}
        </ol>
      </section>

      <section id="reproducibility" className="railBlock">
        <span className="railLabel">Reproducibility path</span>
        <ol className="reproSteps">
          <li><b>1</b><span>Get the data<small>sugidanon/corpus v{version}</small></span></li>
          <li><b>2</b><span>Run baseline<small>scripts/run_whisper.py</small></span></li>
          <li><b>3</b><span>Score switch WER<small>score.py --ci</small></span></li>
          <li><b>4</b><span>Submit results<small>results/asr_score.txt</small></span></li>
        </ol>
      </section>

      <section className="railBlock">
        <span className="railLabel">Language pairs</span>
        <PairBar label="hil<->en" value={h.pairs.hil_en} />
        <PairBar label="hil<->tl" value={h.pairs.hil_tl} />
        <PairBar label="tl<->en" value={h.pairs.tl_en} />
      </section>

      <a
        className="reproduceButton"
        href="https://colab.research.google.com/github/Jazztinn/tinig-sa-liwanag/blob/main/notebooks/sugidanon_colab.ipynb"
        target="_blank"
        rel="noreferrer"
      >
        Reproduce v{version}
      </a>
    </aside>
  );
}

function werColor(v) {
  if (v < 40) return "werLow";
  if (v < 70) return "werMid";
  return "werHigh";
}

function ClipRow({ clip, open, onToggle }) {
  const reduceMotion = useReducedMotion();

  return (
    <div className={`clip ${open ? "clipOpen" : ""}`}>
      <button
        className="clipHead"
        type="button"
        aria-expanded={open}
        onClick={onToggle}
      >
        <span className="clipId">{clip.clip_id}</span>
        <span className="chipCol">
          <span className="chip chipDomain">{clip.domain}</span>
          <span className="chip chipSwitch">{clip.switch_type}</span>
        </span>
        <span className="clipStats">
          <span className={`werVal ${werColor(clip.wer.overall)}`}>
            {pct(clip.wer.overall)}
          </span>
          <span className="werSub">switch {pct(clip.wer.switch)}</span>
          <span className="werSub">Hil {pct(clip.wer.mono)}</span>
        </span>
        <span className="caret">{open ? "Close" : "Open"}</span>
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            className="clipBody"
            initial={{ height: 0, opacity: reduceMotion ? 1 : 0, y: reduceMotion ? 0 : -6 }}
            animate={{ height: "auto", opacity: 1, y: 0 }}
            exit={{ height: 0, opacity: reduceMotion ? 1 : 0, y: reduceMotion ? 0 : -4 }}
            transition={{ duration: reduceMotion ? 0 : 0.26, ease: [0.22, 1, 0.36, 1] }}
          >
            <motion.div
              className="clipBodyInner"
              initial={{ scale: reduceMotion ? 1 : 0.992 }}
              animate={{ scale: 1 }}
              exit={{ scale: reduceMotion ? 1 : 0.996 }}
              transition={{ duration: reduceMotion ? 0 : 0.2, ease: [0.22, 1, 0.36, 1] }}
            >
              <MiniTranscript clip={clip} />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function Home() {
  const [data, setData] = useState(null);
  const [openId, setOpenId] = useState(FEATURED_CLIP);
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
    return data.clips.find((c) => c.clip_id === FEATURED_CLIP) || data.clips[0] || null;
  }, [data]);

  const clips = useMemo(() => {
    if (!data?.clips) return [];
    return data.clips.filter(
      (c) =>
        (fSwitch === "ALL" || c.switch_type === fSwitch) &&
        (fDomain === "ALL" || c.domain === fDomain)
    );
  }, [data, fSwitch, fDomain]);

  if (!data) return <div className="loading">Loading benchmark</div>;
  if (data.error) return <div className="loading">Could not load benchmark.json</div>;

  const h = data.headline;
  const cohorts = data.cohorts || [];

  return (
    <>
      <Head>
        <title>Sugidanon | Code-Switch Hiligaynon ASR Benchmark</title>
        <meta
          name="description"
          content="Open switch-region WER benchmark for Hiligaynon code-switched speech."
        />
      </Head>

      <main className="archiveWorld" id="top">
        <span className="edgeMap" aria-hidden="true" />
        <span className="edgeCabinet" aria-hidden="true">
          <b>BINABAGAN<br />APR 2019</b>
          <b>SILAY CITY<br />JUN 2019</b>
          <b>HINIGARAN<br />MAY 2019</b>
        </span>

        <div className="paperStage">
          <TopNav version={data.version} />

          <section className="heroSheet">
            <p className="kicker">An open code-switch ASR benchmark for Hiligaynon</p>
            <h1>Switch-region WER exposes what overall WER hides</h1>
            <p className="thesis">borrowed words survive, Hiligaynon drops out</p>
          </section>
          <DossierNote />

          <div className="mainGrid">
            <div className="reportColumn">
              <SpeechDemo clip={featured} model={data.model} />
              <BaselinePanel h={h} model={data.model} />
              <ArchiveStrip clips={data.clips} version={data.version} />

              <section className="inspector" id="clips" aria-labelledby="clips-title">
                <div className="inspectorHeader">
                  <div className="filterDeck">
                    <div className="filterGroup">
                      <span className="filterLabel">Filter</span>
                      <SegmentedFilter
                        options={["ALL", ...SWITCH_TYPES].map((s) => ({
                          id: s,
                          label: s === "ALL" ? "All" : s,
                        }))}
                        value={fSwitch}
                        onChange={setFSwitch}
                      />
                    </div>
                    <div className="filterGroup">
                      <span className="filterLabel">Domain</span>
                      <SegmentedFilter
                        options={["ALL", ...domains].map((d) => ({
                          id: d,
                          label: d === "ALL" ? "All" : d,
                        }))}
                        value={fDomain}
                        onChange={setFDomain}
                      />
                    </div>
                    <strong>{clips.length} clips</strong>
                  </div>
                </div>
                <div className="clipsTable">
                  <div className="clipsHeader">
                    <span>Clip</span>
                    <span>Tags</span>
                    <span>WER bands</span>
                    <span>Action</span>
                  </div>
                  {clips.map((c) => (
                    <ClipRow
                      key={c.clip_id}
                      clip={c}
                      open={openId === c.clip_id}
                      onToggle={() => setOpenId(openId === c.clip_id ? null : c.clip_id)}
                    />
                  ))}
                </div>
              </section>

              <section className="paperSection" id="methodology">
                <h2>The negative switch penalty</h2>
                <div className="methodGrid">
                  <article>
                    <span>01</span>
                    <h3>Score the frozen split</h3>
                    <p>Headline WER comes from 40 scripted native clips by spk01 only.</p>
                  </article>
                  <article>
                    <span>02</span>
                    <h3>Mark switch regions</h3>
                    <p>Errors near borrowed English or Tagalog words are separated from Hiligaynon matrix errors.</p>
                  </article>
                  <article id="corpus">
                    <span>03</span>
                    <h3>Keep cohorts apart</h3>
                    <p>Development and robustness clips remain outside the headline benchmark.</p>
                  </article>
                </div>
              </section>

              {cohorts.length > 1 && (
                <section className="cohorts paperSection" aria-labelledby="cohort-title">
                  <h2 id="cohort-title">Cohort ledger</h2>
                  <div className="cohortTable">
                    <div className="cohortRow cohortHead">
                      <span>Speaker</span>
                      <span>Role</span>
                      <span>Overall</span>
                      <span>Switch</span>
                      <span>Hil</span>
                      <span>Penalty</span>
                    </div>
                    {cohorts.map((c) => (
                      <div className="cohortRow" key={c.name}>
                        <span className="cohortName">
                          {c.speaker} <em>{c.n} clips</em>
                        </span>
                        <span>{c.role}</span>
                        <span>{pct(c.overall)}</span>
                        <span>{pct(c.switch)}</span>
                        <span>{pct(c.mono)}</span>
                        <strong>{formatPenalty(c.penalty)}</strong>
                      </div>
                    ))}
                  </div>
                </section>
              )}
            </div>

            <EvidenceRail h={h} cohorts={cohorts} version={data.version} />
          </div>

          <footer className="foot" id="about">
            Native speakers are credited as authors. Hiligaynon references stay seed-unverified until native review confirms them.
          </footer>
        </div>
      </main>
    </>
  );
}
