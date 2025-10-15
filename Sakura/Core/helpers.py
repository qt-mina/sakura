# Sakura/Core/helpers.py
import random
import time
from typing import Dict
from pyrogram import Client
from pyrogram.types import Message, User
from Sakura.Core.logging import logger
from Sakura.Modules.messages import RESPONSES, ERROR
from Sakura import state
from Sakura.Core.config import SESSION_TTL

def fetch_user(msg: Message) -> Dict[str, any]:
    """Extract user and chat information from message"""
    logger.debug("🔍 Extracting user information from message")
    
    # Handle channel messages (no from_user, only sender_chat)
    if msg.sender_chat and not msg.from_user:
        c = msg.chat
        info = {
            "user_id": msg.sender_chat.id,
            "username": msg.sender_chat.username,
            "full_name": msg.sender_chat.title or "Channel",
            "first_name": msg.sender_chat.title or "Channel",
            "last_name": None,
            "chat_id": c.id,
            "chat_type": str(c.type).split('.')[-1].lower(),
            "chat_title": c.title or c.first_name or "",
            "chat_username": f"@{c.username}" if c.username else "No Username",
            "chat_link": f"https://t.me/{c.username}" if c.username else "No Link",
        }
        logger.info(
            f"📑 Channel message extracted: {info['full_name']} (@{info['username']}) "
            f"[ID: {info['user_id']}] in {info['chat_title']} [{info['chat_id']}] {info['chat_link']}"
        )
        return info
    
    # Handle regular user messages
    u = msg.from_user
    c = msg.chat
    info = {
        "user_id": u.id,
        "username": u.username,
        "full_name": u.full_name,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "chat_id": c.id,
        "chat_type": str(c.type).split('.')[-1].lower(),
        "chat_title": c.title or c.first_name or "",
        "chat_username": f"@{c.username}" if c.username else "No Username",
        "chat_link": f"https://t.me/{c.username}" if c.username else "No Link",
    }
    logger.info(
        f"📑 User info extracted: {info['full_name']} (@{info['username']}) "
        f"[ID: {info['user_id']}] in {info['chat_title']} [{info['chat_id']}] {info['chat_link']}"
    )
    return info

def log_action(level: str, message: str, user_info: Dict[str, any]) -> None:
    """Log message with user information"""
    user_detail = (
        f"👤 {user_info.get('full_name', 'N/A')} (@{user_info.get('username', 'N/A')}) "
        f"[ID: {user_info.get('user_id', 'N/A')}] | "
        f"💬 {user_info.get('chat_title', 'N/A')} [{user_info.get('chat_id', 'N/A')}] "
        f"({user_info.get('chat_type', 'N/A')}) {user_info.get('chat_link', 'N/A')}"
    )
    full_message = f"{message} | {user_detail}"

    if level.upper() == "INFO":
        logger.info(full_message)
    elif level.upper() == "DEBUG":
        logger.debug(full_message)
    elif level.upper() == "WARNING":
        logger.warning(full_message)
    elif level.upper() == "ERROR":
        logger.error(full_message)
    else:
        logger.info(full_message)

def should_reply(message: Message, bot_id: int, client: Client = None) -> bool:
    """Check if bot should reply to a group message (Pyrogram way)"""
    
    logger.debug(f"🔍 Checking should_reply - Message from: {message.from_user.id if message.from_user else 'None'}")
    logger.debug(f"🔍 Sender chat: {message.sender_chat}")
    logger.debug(f"🔍 Text: {message.text or message.caption}")
    logger.debug(f"🔍 Entities: {message.entities}")
    logger.debug(f"🔍 Caption entities: {message.caption_entities}")
    
    # Check if replying to bot's message
    if message.reply_to_message and message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id == bot_id:
            logger.debug("✅ Should reply: Reply to bot's message")
            return True
    
    # Check for mentions in entities
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention" or entity.type == "text_mention":
                logger.debug(f"✅ Should reply: Found mention entity - {entity.type}")
                return True
    
    # Check for mentions in caption entities (for media)
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.type == "mention" or entity.type == "text_mention":
                logger.debug(f"✅ Should reply: Found caption mention entity - {entity.type}")
                return True
    
    # Pyrogram fallback: Check text/caption directly for @username mention
    # This catches cases where entities aren't parsed (like channel forwards)
    if client and client.me and client.me.username:
        text = message.text or message.caption or ""
        bot_mention = f"@{client.me.username}".lower()
        logger.debug(f"🔍 Checking for bot mention '{bot_mention}' in text: '{text}'")
        if bot_mention in text.lower():
            logger.debug(f"✅ Should reply: Found bot mention in text")
            return True
    
    # Also check for "sakura" keyword (original behavior)
    user_message = message.text or message.caption or ""
    if "sakura" in user_message.lower():
        logger.debug("✅ Should reply: Found 'sakura' keyword")
        return True
    
    logger.debug("❌ Should NOT reply: No mention/reply/keyword found")
    return False

def get_mention(user: User) -> str:
    """Create user mention for HTML parsing using first name"""
    first_name = user.first_name or "Friend"
    return f'<a href="tg://user?id={user.id}">{first_name}</a>'

def get_fallback() -> str:
    """Get a random fallback response when API fails"""
    return random.choice(RESPONSES)

def get_error() -> str:
    """Get a random error response when something goes wrong"""
    return random.choice(ERROR)

async def log_response(user_id: int) -> None:
    """Update the last response time for user in Valkey"""
    if state.valkey_client:
        try:
            key = f"last_response:{user_id}"
            await state.valkey_client.setex(key, SESSION_TTL, int(time.time()))
            logger.debug(f"⏰ Updated response time in Valkey for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Failed to update response time in Valkey for user {user_id}: {e}")
    state.user_last_response_time[user_id] = time.time()