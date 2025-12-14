import os
from dotenv import load_dotenv

load_dotenv()

# ===== API KEYS =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# ===== PROVIDER SWITCHES =====
TRANSCRIBE_PROVIDER = os.getenv("TRANSCRIBE_PROVIDER", "mock")
ANALYZE_PROVIDER = os.getenv("ANALYZE_PROVIDER", "mock")
