# Sakura/Chat/audio.py
import io
from pydub import AudioSegment
from google import genai
from google.genai import types
from Sakura.Core.logging import logger

async def transcribe_audio(audio_bytes: bytes, mime_type: str) -> str | None:
    """
    Transcribes audio to text using the Gemini API, with a 30-second limit.

    Args:
        audio_bytes: The audio data in bytes.
        mime_type: The MIME type of the audio data.

    Returns:
        The transcribed text, or None if an error occurred.
    """
    try:
        # Check audio duration
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        if len(audio) > 30000:
            logger.warning("Audio duration exceeds 30-second limit.")
            return None

        # Transcribe audio using Gemini API
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(
            [
                "Generate a transcript of the speech.",
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type,
                )
            ]
        )
        return response.text.strip() if response.text else None

    except Exception as e:
        logger.error(f"Error during audio transcription: {e}")
        return None
