# Sakura/Chat/voice.py
import asyncio
from io import BytesIO
from elevenlabs.client import AsyncElevenLabs
from elevenlabs.core import ApiError
from Sakura.Core.config import ELEVENLABS_API_KEY, VOICE_ID
from Sakura.Core.logging import logger

# Check if pydub and ffmpeg are available
try:
    from pydub import AudioSegment
    from pydub.utils import which
except ImportError:
    AudioSegment = None
    which = None

client = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)

# Determine FFmpeg availability
if AudioSegment and which:
    FFMPEG_AVAILABLE = which("ffmpeg") is not None or which("avconv") is not None
    if FFMPEG_AVAILABLE:
        logger.info("✅ FFmpeg detected - OGG conversion enabled")
    else:
        logger.warning("⚠️ FFmpeg not found - voice messages will be sent as MP3")
else:
    FFMPEG_AVAILABLE = False
    logger.warning("⚠️ pydub not installed - voice messages will be sent as MP3")

async def generate_voice(text: str) -> BytesIO | None:
    """
    Generates voice from text using the ElevenLabs API.
    Converts to OGG format if FFmpeg is available, otherwise uses MP3.
    
    Args:
        text: The text to convert to speech.
    Returns:
        The audio data as a BytesIO object, or None if an error occurred.
    """
    if not ELEVENLABS_API_KEY:
        logger.warning("⚠️ ElevenLabs API key is not configured.")
        return None
    
    try:
        logger.info(f"🎤 Generating voice for text: '{text}'")
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id="eleven_v3"
        )
        
        audio_bytes = b""
        async for chunk in audio_stream:
            audio_bytes += chunk
        
        # Try to convert to OGG if FFmpeg is available
        if FFMPEG_AVAILABLE:
            try:
                mp3_audio = AudioSegment.from_mp3(BytesIO(audio_bytes))
                ogg_buffer = BytesIO()
                mp3_audio.export(ogg_buffer, format="ogg", codec="libopus")
                ogg_buffer.seek(0)
                ogg_buffer.name = "voice.ogg"
                logger.info("✅ Voice generated and converted to OGG successfully.")
                return ogg_buffer
            except Exception as conv_error:
                logger.warning(f"⚠️ OGG conversion failed: {conv_error}. Falling back to MP3.")
        
        # Fallback: Return MP3 if FFmpeg unavailable or conversion failed
        audio_file = BytesIO(audio_bytes)
        audio_file.name = "voice.mp3"
        logger.info("✅ Voice generated as MP3 (FFmpeg not available).")
        return audio_file
        
    except ApiError as e:
        logger.error(f"❌ ElevenLabs API error: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred during voice generation: {e}")
        return None
