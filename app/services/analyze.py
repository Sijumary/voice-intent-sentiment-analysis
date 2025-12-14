import json
from typing import Dict
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


def analyze_text_and_audio(transcript: Dict, wav_path: str) -> Dict:
    # Build instruction with transcript + short context
    text = transcript.get('text', '')
    # Very naive heuristics for demo purposes
    text_lower = text.lower()
    intent = 'other'
    if 'cancel' in text_lower or 'cancel my' in text_lower:
        intent = 'cancel_subscription'
    elif 'bill' in text_lower or 'charge' in text_lower:
        intent = 'billing_issue'


    sentiment = 'neutral'
    if 'not happy' in text_lower or 'angry' in text_lower or 'frustrat' in text_lower:
        sentiment = 'negative'
    elif 'thank' in text_lower or 'great' in text_lower or 'love' in text_lower:
        sentiment = 'positive'


    tone = 'neutral'
    if sentiment == 'negative':
        tone = 'frustrated'
    elif sentiment == 'positive':
        tone = 'cheerful'


    urgency = 'low'
    if 'now' in text_lower or 'immediately' in text_lower or 'asap' in text_lower:
        urgency = 'high'


    summary = text[:400]


    result = {
        'sentiment': sentiment,
        'tone': tone,
        'intent': intent,
        'urgency': urgency,
        'summary': summary,
        'important_phrases': [],
        'agent_score': None,
        'raw_response': None,
    }


# Try to format as AnalysisResponse compatible dict
    return result