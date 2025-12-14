from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_file(wav_path: str) -> dict:
    with open(wav_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json"
        )

    return {
        "text": transcript["text"],
        "segments": transcript.get("segments", []),
        "language": transcript.get("language")
    }

