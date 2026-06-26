export const config = {
  api: {
    bodyParser: {
      sizeLimit: "12mb",
    },
  },
};

const MAX_AUDIO_BYTES = Number(process.env.TRANSCRIBE_MAX_AUDIO_BYTES || 8 * 1024 * 1024);
const DEFAULT_HF_SPACE_URL = "https://alinuxperson-tinig-sa-liwanag-space.hf.space";
const HF_SPACE_API_NAME = process.env.HF_SPACE_TRANSCRIBE_API_NAME || "transcribe_base64";
const HF_SPACE_TIMEOUT_MS = Number(process.env.HF_SPACE_TRANSCRIBE_TIMEOUT_MS || 120000);

function normalizeSpaceUrl(rawUrl) {
  const value = String(rawUrl || DEFAULT_HF_SPACE_URL).trim().replace(/\/+$/u, "");
  const repoUrl = value.match(/^https:\/\/huggingface\.co\/spaces\/([^/]+)\/([^/?#]+)/iu);

  if (repoUrl) {
    return `https://${repoUrl[1].toLowerCase()}-${repoUrl[2].toLowerCase()}.hf.space`;
  }

  return value;
}

function normalizeApiName(rawName) {
  return String(rawName || "transcribe_base64").trim().replace(/^\/+/u, "");
}

function bufferFromBase64(audioBase64) {
  const value = String(audioBase64 || "").replace(/\s+/gu, "");
  if (!value || !/^[A-Za-z0-9+/]+={0,2}$/u.test(value) || value.length % 4 === 1) {
    throw new Error("Recorded audio is not valid base64.");
  }

  return {
    audioBase64: value,
    buffer: Buffer.from(value, "base64"),
  };
}

function parseBase64DataUrl(audio) {
  const value = String(audio || "");
  const commaIndex = value.indexOf(",");
  const meta = commaIndex >= 0 ? value.slice(5, commaIndex) : "";
  const audioBase64 = commaIndex >= 0 ? value.slice(commaIndex + 1) : "";
  const metaParts = meta.split(";").filter(Boolean);
  const mimeType = metaParts.find((part) => part.includes("/")) || "audio/webm";
  const hasBase64Flag = metaParts.some((part) => part.toLowerCase() === "base64");

  if (!value.startsWith("data:") || commaIndex < 0 || !hasBase64Flag) {
    const preview = value ? value.slice(0, 48) : "missing";
    throw new Error(
      `Expected audioBase64 or a base64 media data URL. Received audio=${preview}.`
    );
  }

  return {
    mimeType,
    audioBase64,
  };
}

function parseAudioPayload(payload) {
  const mimeType =
    typeof payload?.mimeType === "string" && payload.mimeType.trim()
      ? payload.mimeType.trim()
      : "audio/webm";

  if (typeof payload?.audioBase64 === "string" && payload.audioBase64.trim()) {
    return {
      mimeType,
      ...bufferFromBase64(payload.audioBase64),
    };
  }

  const audio = parseBase64DataUrl(payload?.audio);

  return {
    mimeType: payload?.mimeType ? mimeType : audio.mimeType,
    ...bufferFromBase64(audio.audioBase64),
  };
}

function hfSpaceEndpoint() {
  const baseUrl = normalizeSpaceUrl(process.env.HF_SPACE_TRANSCRIBE_URL || DEFAULT_HF_SPACE_URL);
  const apiName = encodeURIComponent(normalizeApiName(HF_SPACE_API_NAME));
  return `${baseUrl}/gradio_api/call/${apiName}`;
}

async function fetchWithTimeout(url, options, label) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), HF_SPACE_TIMEOUT_MS);

  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } catch (err) {
    if (err?.name === "AbortError") {
      throw new Error(`${label} timed out after ${Math.round(HF_SPACE_TIMEOUT_MS / 1000)}s.`);
    }
    throw new Error(`${label} request failed: ${err?.message || "unknown network error"}`);
  } finally {
    clearTimeout(timeout);
  }
}

async function readJsonResponse(response, label) {
  const text = await response.text();

  if (!response.ok) {
    throw new Error(`${label} failed (${response.status}): ${text.slice(0, 500)}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${label} returned invalid JSON.`);
  }
}

function gradioErrorMessage(value) {
  if (!value) return "unknown error";
  if (typeof value === "string") return value;
  if (typeof value.error === "string") return value.error;
  if (typeof value.message === "string") return value.message;
  return JSON.stringify(value).slice(0, 500);
}

function unpackGradioData(value) {
  let result = value;

  while (Array.isArray(result) && result.length === 1) {
    result = result[0];
  }

  if (typeof result === "string") {
    return { text: result };
  }

  if (result && typeof result === "object") {
    return result;
  }

  throw new Error("HF Space returned an empty transcription result.");
}

function parseGradioEventStream(streamText) {
  let completeData;
  let lastData;
  let errorData;

  for (const block of String(streamText || "").split(/\r?\n\r?\n/u)) {
    const lines = block.split(/\r?\n/u);
    let eventName = "";
    const dataLines = [];

    for (const line of lines) {
      if (line.startsWith("event:")) eventName = line.slice(6).trim();
      if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
    }

    if (!dataLines.length) continue;

    const rawData = dataLines.join("\n");
    let parsedData;
    try {
      parsedData = JSON.parse(rawData);
    } catch {
      parsedData = rawData;
    }

    if (eventName === "error") {
      errorData = parsedData;
    } else if (eventName === "complete") {
      completeData = parsedData;
    } else {
      lastData = parsedData;
    }
  }

  if (errorData) {
    throw new Error(`HF Space failed: ${gradioErrorMessage(errorData)}`);
  }

  if (completeData === undefined && lastData === undefined) {
    throw new Error("HF Space did not return a transcription event.");
  }

  return unpackGradioData(completeData ?? lastData);
}

async function transcribeWithHfSpace(parsed, reference) {
  const endpoint = hfSpaceEndpoint();
  const startResponse = await fetchWithTimeout(
    endpoint,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        data: [parsed.audioBase64, parsed.mimeType, reference || ""],
      }),
    },
    "HF Space transcription"
  );
  const job = await readJsonResponse(startResponse, "HF Space transcription");
  const eventId = job?.event_id;

  if (!eventId) {
    throw new Error("HF Space did not return a Gradio event id.");
  }

  const resultResponse = await fetchWithTimeout(
    `${endpoint}/${encodeURIComponent(eventId)}`,
    { headers: { Accept: "text/event-stream" } },
    "HF Space transcription result"
  );
  const streamText = await resultResponse.text();

  if (!resultResponse.ok) {
    throw new Error(
      `HF Space transcription result failed (${resultResponse.status}): ${streamText.slice(0, 500)}`
    );
  }

  const result = parseGradioEventStream(streamText);
  return {
    text: String(result.text || result.transcript || "").trim(),
    backend: result.backend || "hf-space-whisper",
    model: result.model || "whisper-small",
    language: result.language || "tl",
  };
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  let parsed;
  try {
    parsed = parseAudioPayload(req.body);
  } catch (err) {
    return res.status(400).json({ error: err.message });
  }

  if (!parsed.buffer.length) {
    return res.status(400).json({ error: "Recorded audio is empty." });
  }

  if (parsed.buffer.length > MAX_AUDIO_BYTES) {
    return res.status(413).json({ error: "Recorded audio is too large." });
  }

  try {
    const result = await transcribeWithHfSpace(parsed, req.body?.reference);
    return res.status(200).json(result);
  } catch (err) {
    return res.status(503).json({
      error: err.message || "Hosted transcription failed.",
    });
  }
}
