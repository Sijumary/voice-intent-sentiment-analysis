import subprocess
import tempfile
import os

# 👇 FULL PATH to ffmpeg.exe (adjust if needed)
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

def ensure_wav(input_path: str) -> str:
    """
    Converts input audio to mono 16k WAV using ffmpeg.
    Returns path to converted wav.
    """
    if not os.path.exists(FFMPEG_PATH):
        raise RuntimeError("FFmpeg not found at configured path")

    output_path = os.path.join(
        tempfile.gettempdir(),
        os.path.basename(input_path).replace(".wav", "_16k.wav")
    )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path
