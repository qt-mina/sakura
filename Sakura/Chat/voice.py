# Sakura/Chat/voice.py
import asyncio
from io import BytesIO
from elevenlabs.client import AsyncElevenLabs
from elevenlabs.core import ApiError
from Sakura.Core.config import ELEVENLABS_API_KEY, VOICE_ID
from Sakura.Core.logging import logger

client = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)

async def generate_voice(text: str) -> BytesIO | None:
    """
    Generates voice from text using the ElevenLabs API.
    Args:
        text: The text to convert to speech.
    Returns:
        The audio data as a BytesIO object, or None if an error occurred.
    """
    if not ELEVENLABS_API_KEY:
        logger.warning("ElevenLabs API key is not configured.")
        return None
    
    try:
        logger.info(f"Generating voice for text: '{text}'")
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id="eleven_v3"
        )
        
        audio_bytes = b""
        async for chunk in audio_stream:
            audio_bytes += chunk
        
        # Convert bytes to BytesIO object with a name attribute
        audio_file = BytesIO(audio_bytes)
        audio_file.name = "voice.mp3"  # Give it a filename
        
        logger.info("Voice generation successful.")
        return audio_file
        
    except ApiError as e:
        logger.error(f"ElevenLabs API error: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during voice generation: {e}")
        return None
