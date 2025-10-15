# Sakura/Chat/voice.py
import asyncio
from io import BytesIO
from elevenlabs.client import AsyncElevenLabs
from elevenlabs.core import ApiError
from pydub import AudioSegment
from Sakura.Core.config import ELEVENLABS_API_KEY, VOICE_ID
from Sakura.Core.logging import logger

client = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)

async def generate_voice(text: str) -> BytesIO | None:
    """
    Generates voice from text using the ElevenLabs API and converts to OGG format.
    Args:
        text: The text to convert to speech.
    Returns:
        The audio data as a BytesIO object in OGG format, or None if an error occurred.
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
        
        # Convert MP3 bytes to OGG format
        mp3_audio = AudioSegment.from_mp3(BytesIO(audio_bytes))
        
        # Export as OGG
        ogg_buffer = BytesIO()
        mp3_audio.export(ogg_buffer, format="ogg", codec="libopus")
        ogg_buffer.seek(0)  # Reset buffer position to start
        ogg_buffer.name = "voice.ogg"
        
        logger.info("Voice generation and conversion to OGG successful.")
        return ogg_buffer
        
    except ApiError as e:
        logger.error(f"ElevenLabs API error: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during voice generation: {e}")
        return None
