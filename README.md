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

### Environment variables (example `.env`)

```
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
GENAI_API_KEY=your_gemini_or_google_api_key
TRANSCRIBE_PROVIDER=gemini  # or whisper/assemblyai
DIARIZATION_PROVIDER=pyannote  # optional
```

### Install

Using `pip` and `requirements.txt` (or `pyproject.toml`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` (suggested minimal):

```
fastapi
uvicorn[standard]
pydub
python-multipart
google-generativeai
requests
pytest
python-dotenv
numpy
soundfile
```

(If you use diarization add `pyannote.audio` and follow its install docs.)

---

## Key code snippets

### 1) app/main.py (startup)

```python
from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Voice Intent & Sentiment Analyzer")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2) app/api.py (endpoints)

```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.audio import ensure_wav
from app.services.transcribe import transcribe_file
from app.services.analyze import analyze_text_and_audio
from app.models import AnalysisResponse

router = APIRouter()

@router.post('/analyze', response_model=AnalysisResponse)
async def analyze(audio: UploadFile = File(...)):
    saved_path = f"/tmp/{audio.filename}"
    with open(saved_path, 'wb') as f:
        f.write(await audio.read())

    wav_path = ensure_wav(saved_path)
    transcript = transcribe_file(wav_path)
    result = analyze_text_and_audio(transcript, wav_path)
    return result
```

### 3) app/services/audio.py

```python
import os
from pydub import AudioSegment

def ensure_wav(path: str) -> str:
    # convert to mono 16k wav suitable for many speech models
    filename, ext = os.path.splitext(path)
    out = filename + '.wav'
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(out, format='wav')
    return out
```

### 4) app/services/transcribe.py

```python
import google.generativeai as genai
from app.config import GENAI_API_KEY

genai.configure(api_key=GENAI_API_KEY)

# Note: adjust to whichever Gemeni/voice API is current. This is an illustrative adapter.

def transcribe_file(wav_path: str) -> dict:
    # Upload file then call a speech-to-text method.
    # Depending on the official SDK, the exact call will change.
    with open(wav_path, 'rb') as f:
        uploaded = genai.upload_file(f, file_name=wav_path)

    # Example: ask the model to transcribe using a voice model
    prompt = (
        "Transcribe the following call recording. Provide speaker labels if possible, timestamps, and keep punctuation."
    )
    response = genai.chat.completions.create(
        model='gpt-voice-1',
        input=[{'role':'user','content': prompt, 'file': uploaded['name']}]
    )
    # adapt to SDK's real response structure
    return response
```

> **NOTE:** APIs change — when you implement, consult the provider docs and swap the adapter implementation as necessary.

### 5) app/services/analyze.py

```python
import google.generativeai as genai
from app.config import GENAI_API_KEY

PROMPT_INSTRUCTIONS = '''
You are an assistant specialized in call analytics. Given the transcript (with timestamps) and optional audio cues, return JSON with keys: intent, tone, sentiment, urgency, summary, important_phrases.
Possible intents: billing_issue, cancel_subscription, product_question, feedback, support_request, other.
Tone values: calm, frustrated, angry, cheerful, uncertain, neutral.
Sentiment: positive, negative, neutral.
Urgency: low, medium, high.
Return only valid JSON.
'''

def analyze_text_and_audio(transcript: dict, wav_path: str) -> dict:
    # Build instruction with transcript + short context
    payload = PROMPT_INSTRUCTIONS + "\nTranscript:\n" + transcript['text']
    response = genai.chat.completions.create(
        model='gpt-4o-mini',
        input=[{'role':'user','content': payload}]
    )
    # parse JSON from response
    text = response.choices[0].message['content']
    import json
    try:
        return json.loads(text)
    except Exception:
        # fallback: return raw text
        return {"raw_response": text}
```

---

## Response model (pydantic)

`app/models.py` should define the structure returned to clients, example:

```python
from pydantic import BaseModel
from typing import List, Optional

class AgentScore(BaseModel):
    politeness: Optional[int]
    clarity: Optional[int]
    resolution: Optional[int]

class AnalysisResponse(BaseModel):
    sentiment: str
    tone: str
    intent: str
    urgency: str
    summary: str
    important_phrases: Optional[List[str]]
    agent_score: Optional[AgentScore]
    raw_response: Optional[str]
```

---

## Tests

Add unit tests that mock the transcription and the LLM analyze call. Keep tests small and deterministic.

`tests/test_analyze.py` example (pytest + monkeypatch):

```python
from app.services.analyze import analyze_text_and_audio

def test_analyze_basic(monkeypatch):
    fake_transcript = {'text': 'I want to cancel my subscription, I am not happy.'}
    monkeypatch.setattr('app.services.analyze.genai.chat.completions.create', lambda **kwargs: type('R', (), {'choices':[type('C',(),{'message':{'content':'{"intent":"cancel_subscription","tone":"angry","sentiment":"negative","urgency":"high","summary":"User wants to cancel due to dissatisfaction."}'}}])}) )
    out = analyze_text_and_audio(fake_transcript, '/tmp/dummy.wav')
    assert out['intent'] == 'cancel_subscription'
```

---

## Dockerfile (simple)

```
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## CI (GitHub Actions) - `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q
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

