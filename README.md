# voice-intent-sentiment-analysis
# voice-intent-sentiment-analyzer

A step-by-step GitHub-ready project scaffold to analyze call / voice recordings using a voice LLM (e.g., Gemini Voice). The project transcribes audio, performs speaker diarization (optional), and runs an intent/tone/sentiment extraction pipeline producing structured JSON and a small dashboard.

---

## What you'll get in this repo

* A clear file structure and README
* FastAPI backend with endpoints to upload audio and return analysis
* `services/` modules: audio preprocessing, transcription adapter, analysis adapter (calls LLM), postprocessing
* Example client script and minimal React UI (optional) to play recordings and view analysis
* Dockerfile and GitHub Actions CI for linting and tests
* Sample audio and test data

---

## Repo file tree (suggested)

```
voice-intent-sentiment-analyzer/
├── README.md
├── LICENSE
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml (or requirements.txt)
├── app/
│   ├── main.py            # FastAPI app
│   ├── api.py             # endpoints
│   ├── config.py          # env vars and config
│   ├── models.py          # pydantic response/request models
│   ├── services/
│   │   ├── audio.py       # audio processing helpers
│   │   ├── transcribe.py  # transcription adapter
│   │   ├── diarize.py     # speaker diarization (optional)
│   │   └── analyze.py     # call to Gemini LLM for intent/tone/sentiment
│   └── utils/
│       └── fileio.py
├── client/
│   ├── example_client.py  # CLI example to call the API
│   └── small_web_ui/      # optional React app
├── tests/
│   ├── test_transcribe.py
│   └── test_analyze.py
└── samples/
    ├── sample_calls/
    │   └── sample1.wav
    └── expected_output.json
```

---

## High-level steps (what this scaffold covers)

1. Install dependencies and set environment variables
2. Start FastAPI server
3. Upload / POST an audio file to `/analyze` endpoint
4. Server preprocesses audio (normalize, convert to wav, resample)
5. Transcription service returns text + timestamps
6. (Optional) Diarization to split speakers
7. Analysis service calls Gemini (or chosen LLM) with audio transcript + timestamps + short instructions to extract intent, tone, sentiment, urgency, and summary
8. Postprocess and return a JSON analysis and small HTML viewer

---

## Detailed setup

### Prerequisites

* Python 3.10+
* ffmpeg installed and in PATH (for pydub / ffmpeg-python)
* (Optional) Node.js 18+ for the small UI
* API key for the voice LLM (e.g., GOOGLE_GENAI_API_KEY for Gemini)

# Install

Using `pip` and `requirements.txt` (or `pyproject.toml`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Security & costs notes

* LLM and transcription calls may incur costs — use small test keys and a budget while developing.
* Never commit API keys — use `.env` and repository secrets for CI.
* If processing PII/audio from customers, follow local privacy laws and store minimal data.

---

## 🚀 Quick Start (GitHub Ready)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/voice-intent-sentiment-analyzer.git
cd voice-intent-sentiment-analyzer
```

### 2️⃣ Create virtual environment (Windows-friendly)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file:

```env
GENAI_API_KEY=your_api_key_here
TRANSCRIBE_PROVIDER=mock
```

### 5️⃣ Start the API server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 6️⃣ Analyze an audio file

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@samples/sample_calls/sample1.wav"
```

---

## 📦 Example API Response

```json
{
  "sentiment": "negative",
  "tone": "frustrated",
  "intent": "cancel_subscription",
  "urgency": "high",
  "summary": "Customer wants to cancel due to dissatisfaction."
}
```

---

## 🧱 Architecture Overview

```
Client (curl / UI)
      │
      ▼
FastAPI API
      │
      ├─► Audio Normalization (FFmpeg)
      ├─► Transcription Adapter (mock / Whisper / Gemini)
      └─► LLM Analysis (intent, sentiment, tone)
      │
      ▼
Structured JSON Response
```

---


## 🧠 Resume Value

**Skills demonstrated:**

* FastAPI & REST APIs
* Audio processing (FFmpeg)
* LLM prompt engineering
* NLP classification (intent, sentiment)
* Production-ready project structure

---

## 📜 License

MIT

---

