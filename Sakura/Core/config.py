# Sakura/Core/config.py
import os

# CONFIGURATION
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
VALKEY_URL = os.getenv("VALKEY_URL", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
DATABASE_URL = os.getenv("DATABASE_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gemini-2.5-flash")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
PING_LINK = os.getenv("PING_LINK", "https://t.me/DoDotPy")
UPDATE_LINK = os.getenv("UPDATE_LINK", "https://t.me/DoDotPy")
SUPPORT_LINK = os.getenv("SUPPORT_LINK", "https://t.me/SoulMeetsHQ")
SAKURA_STICKERS_PACK = os.getenv("SAKURA_STICKERS_PACK", "https://t.me/addstickers/AsadKang")
START_STICKERS_PACK = os.getenv("START_STICKERS_PACK", "https://t.me/addstickers/WorkGlows")
PAYMENT_STICKERS_PACK = os.getenv("PAYMENT_STICKERS_PACK", "https://t.me/addstickers/WorkGlows")
COMMAND_PREFIXES = ["/", "!", "#", "?", "*"]
VOICE_ID = "1m7y7zSS52lXKQ5ByEUt"
SESSION_TTL = 3600
CACHE_TTL = 300
RATE_LIMIT_TTL = 60
RATE_LIMIT_COUNT = 5
MESSAGE_LIMIT = 1.0
BROADCAST_DELAY = 0.03
CHAT_LENGTH = 20
CHAT_CLEANUP = 1800
OLD_CHAT = 3600
