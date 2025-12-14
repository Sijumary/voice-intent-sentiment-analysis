from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.audio import ensure_wav
from app.services.transcribe import transcribe_file
from app.services.analyze import analyze_text_and_audio
from app.models import AnalysisResponse
import os


router = APIRouter()


@router.post('/analyze', response_model=AnalysisResponse)
async def analyze(audio: UploadFile = File(...)):
    tmp_dir = '/tmp' if os.name != 'nt' else os.getenv('TEMP', '.')
    saved_path = os.path.join(tmp_dir, audio.filename)
    with open(saved_path, 'wb') as f:
        f.write(await audio.read())

    try:
        wav_path = ensure_wav(saved_path)
        transcript = transcribe_file(wav_path)
        result = analyze_text_and_audio(transcript, wav_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optionally cleanup files
        pass