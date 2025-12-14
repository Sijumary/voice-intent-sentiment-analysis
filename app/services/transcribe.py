from typing import Dict
from app.config import TRANSCRIBE_PROVIDER




def transcribe_file(wav_path: str) -> dict:
    """
    Temporary mock transcription.
    Replace this later with Gemini or Whisper.
    """
    return {
        "text": "The customer is angry and wants to cancel the subscription immediately.",
        "language": "en",
        "duration_seconds": 5
    }
