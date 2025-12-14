import os
from dotenv import load_dotenv


load_dotenv()


FASTAPI_HOST = os.getenv('FASTAPI_HOST', '0.0.0.0')
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT', 8000))
GENAI_API_KEY = os.getenv('GENAI_API_KEY')
TRANSCRIBE_PROVIDER = os.getenv('TRANSCRIBE_PROVIDER', 'mock')
DIARIZATION_PROVIDER = os.getenv('DIARIZATION_PROVIDER', 'none')