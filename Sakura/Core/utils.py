# Sakura/Core/utils.py
from Sakura.Core.logging import logger
from Sakura.Core.config import (
    BOT_TOKEN,
    OWNER_ID,
    DATABASE_URL,
    API_ID,
    API_HASH,
)

def validate_config() -> bool:
    """Validate bot configuration"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found in environment variables")
        return False
    if not OWNER_ID:
        logger.error("❌ OWNER_ID not found in environment variables")
        return False
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL not found in environment variables")
        return False
    if not API_ID:
        logger.error("❌ API_ID not found in environment variables")
        return False
    if not API_HASH:
        logger.error("❌ API_HASH not found in environment variables")
        return False
    return True
