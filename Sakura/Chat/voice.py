# Sakura/Chat/voice.py
import asyncio
import random
from io import BytesIO
from typing import Dict
from elevenlabs.client import AsyncElevenLabs
from elevenlabs.core import ApiError
from Sakura.Core.config import ELEVENLABS_API_KEY, VOICE_ID
from Sakura.Core.logging import logger
from Sakura.Core.helpers import log_action

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

# CONTEXTUAL VOICE TRIGGERS
# Contexts where voice responses are more likely
VOICE_CONTEXTS = {
    "emotional": {
        "probability": 0.25,  # 25% chance for emotional messages
        "keywords": [
            "love you", "miss you", "i love", "pyaar", "mohabbat", "dil se",
            "feeling", "emotional", "heart", "soul", "deeply", "truly",
            "care about", "mean to me", "special", "important to me"
        ]
    },
    "excited": {
        "probability": 0.20,  # 20% chance for excited messages
        "keywords": [
            "omg", "wow", "amazing", "incredible", "can't believe",
            "so excited", "yay", "woohoo", "awesome", "fantastic",
            "this is great", "best day", "so happy"
        ]
    },
    "intimate": {
        "probability": 0.30,  # 30% chance for intimate messages
        "keywords": [
            "whisper", "softly", "gently", "close", "intimate", "personal",
            "between us", "just us", "private", "secret", "confession",
            "tell you something", "share with you"
        ]
    },
    "storytelling": {
        "probability": 0.15,  # 15% chance for story requests
        "keywords": [
            "tell me a story", "story time", "once upon", "narrate",
            "bedtime story", "kahani", "fairy tale", "tale", "legend"
        ]
    },
    "comfort": {
        "probability": 0.25,  # 25% chance for comfort messages
        "keywords": [
            "sad", "upset", "crying", "hurt", "pain", "depressed",
            "lonely", "need you", "comfort me", "hold me", "support",
            "difficult time", "going through", "struggling"
        ]
    },
    "playful": {
        "probability": 0.15,  # 15% chance for playful messages
        "keywords": [
            "sing", "poem", "rhyme", "playful", "tease", "flirt",
            "sweet talk", "charm me", "woo me", "romantic"
        ]
    },
    "greeting": {
        "probability": 0.10,  # 10% chance for greetings
        "keywords": [
            "good morning", "good night", "hello sakura", "hi sakura",
            "hey sakura", "sup sakura", "yo sakura", "greetings"
        ]
    }
}

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
        async for audio_stream in audio_stream:
            audio_bytes += audio_stream
        
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


def should_send_voice(user_message: str, user_info: Dict[str, any]) -> bool:
    """
    Determines if a voice message should be sent based on message context.
    
    Args:
        user_message: The user's message text.
        user_info: User information dictionary for logging.
    
    Returns:
        True if voice message should be sent, False otherwise.
    """
    if not user_message:
        return False
    
    message_lower = user_message.lower()
    
    # Check each context
    for context_name, context_data in VOICE_CONTEXTS.items():
        keywords = context_data["keywords"]
        probability = context_data["probability"]
        
        # Check if any keyword matches
        if any(keyword in message_lower for keyword in keywords):
            log_action("DEBUG", f"🎯 Voice context detected: '{context_name}'", user_info)
            
            # Roll the dice based on context probability
            if random.random() < probability:
                log_action("INFO", f"🎤 Voice message triggered by context: '{context_name}' (probability: {probability*100}%)", user_info)
                return True
            else:
                log_action("DEBUG", f"🎲 Voice message NOT triggered (rolled against {probability*100}% chance)", user_info)
                return False
    
    # Default fallback: 5% chance for any other message
    if random.random() < 0.05:
        log_action("INFO", "🎤 Voice message triggered by random chance (5%)", user_info)
        return True
    
    return False


def get_voice_intro(user_message: str) -> str:
    """
    Adds a contextual intro phrase to the AI response before converting to voice.
    This makes voice messages feel more natural and intentional.
    
    Args:
        user_message: The user's original message.
    
    Returns:
        An intro phrase, or empty string if no intro needed.
    """
    message_lower = user_message.lower()
    
    # Emotional context intros
    if any(word in message_lower for word in ["love you", "miss you", "pyaar"]):
        intros = [
            "*softly* ",
            "*with feeling* ",
            "*warmly* "
        ]
        return random.choice(intros)
    
    # Excited context intros
    if any(word in message_lower for word in ["omg", "wow", "excited", "yay"]):
        intros = [
            "*excitedly* ",
            "*with enthusiasm* ",
            "*energetically* "
        ]
        return random.choice(intros)
    
    # Comfort context intros
    if any(word in message_lower for word in ["sad", "upset", "hurt", "crying"]):
        intros = [
            "*gently* ",
            "*soothingly* ",
            "*in a comforting tone* "
        ]
        return random.choice(intros)
    
    # Intimate/whisper context
    if any(word in message_lower for word in ["whisper", "secret", "private"]):
        intros = [
            "*whispering* ",
            "*softly* ",
            "*in a hushed voice* "
        ]
        return random.choice(intros)
    
    # Story/narration context
    if any(word in message_lower for word in ["story", "tell me", "narrate"]):
        intros = [
            "*in storytelling voice* ",
            "*narratively* ",
            ""
        ]
        return random.choice(intros)
    
    # Default: no intro needed
    return ""
