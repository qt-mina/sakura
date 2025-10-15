# Sakura/Modules/handlers.py
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from Sakura.Core.helpers import fetch_user, log_action, should_reply, get_error, log_response
from Sakura.Services.limiter import check_limit
from Sakura.Modules.reactions import handle_reaction
from Sakura.Chat.images import reply_image
from Sakura.Chat.polls import reply_poll
from Sakura.Modules.typing import send_typing
from Sakura.Chat.chat import get_response
from Sakura.Chat.voice import generate_voice
from Sakura.Database.cache import set_last_message, get_last_message
from Sakura.Services.broadcast import execute_broadcast
from Sakura import state
from Sakura.Core.config import OWNER_ID
from Sakura.Modules.stickers import handle_sticker
from Sakura.Modules.image import handle_image
from Sakura.Modules.poll import handle_poll
from Sakura.Services.tracking import track_user

@Client.on_message(
    (filters.text | filters.sticker | filters.voice | filters.video_note |
     filters.photo | filters.document | filters.poll) & ~filters.regex(r"^/")
)
async def handle_messages(client: Client, message: Message) -> None:
    """Handle all types of messages"""
    try:
        # Skip self messages (but allow channel messages)
        if message.from_user and message.from_user.is_self:
            return

        # Skip if no from_user AND no sender_chat (anonymous/deleted accounts)
        if not message.from_user and not message.sender_chat:
            return

        user_info = fetch_user(message)
        user_id = user_info["user_id"]
        chat_type = message.chat.type.name.lower()
        
        # Start typing indicator immediately
        asyncio.create_task(send_typing(client, message.chat.id, user_info))

        # Handle broadcast mode (only for owner)
        if message.from_user and message.from_user.id == OWNER_ID and message.from_user.id in state.broadcast_mode:
            log_action("INFO", f"📢 Executing broadcast to {state.broadcast_mode[message.from_user.id]}", user_info)
            await execute_broadcast(message, client, state.broadcast_mode[message.from_user.id], user_info)
            del state.broadcast_mode[message.from_user.id]
            return

        if chat_type in ['group', 'supergroup'] and not should_reply(message, client.me.id, client):
            return

        if await check_limit(user_id, user_info["chat_id"]):
            log_action("WARNING", "⏱️ Rate limited - ignoring message", user_info)
            return

        asyncio.create_task(handle_reaction(client, message, user_info))

        if message.sticker:
            await handle_sticker(client, message)
            return
        elif message.photo:
            await handle_image(client, message)
            return
        elif message.poll:
            await handle_poll(client, message)
            return

        # Default to text-based handling
        user_message = message.text or message.caption or "Media message"
        log_action("INFO", f"💬 Message: '{user_message}'", user_info)

        if "in your voice" in user_message.lower():
            last_bot_message = await get_last_message(user_id)
            if last_bot_message:
                log_action("INFO", "🎤 Sending voice message", user_info)
                await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_AUDIO)
                voice_data = await generate_voice(last_bot_message)
                if voice_data:
                    await message.reply_voice(voice=voice_data)
                    log_action("INFO", "✅ Voice message sent", user_info)
                    return
            else:
                await message.reply_text("I don't have a recent message to say in my voice. Please let me respond to something first!")
                return

        if await reply_image(client, message, user_message, user_info):
            return
        if await reply_poll(client, message, user_message, user_info):
            return

        # Get AI response (skip history for channel messages)
        is_channel_message = message.sender_chat and not message.from_user
        ai_response = await get_response(user_message, user_id, user_info, save_history=not is_channel_message)

        # Validate response before proceeding
        if not ai_response or not isinstance(ai_response, str):
            log_action("ERROR", f"❌ Invalid AI response", user_info)
            await message.reply_text(get_error())
            return

        # Cache the valid response (skip for channel messages)
        if not is_channel_message:
            try:
                await set_last_message(user_id, ai_response)
            except Exception as cache_error:
                log_action("WARNING", f"⚠️ Failed to cache message", user_info)

        # Try to send as voice (10% chance)
        voice_data = None
        if random.random() < 0.1:
            await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_AUDIO)
            voice_data = await generate_voice(ai_response)

        # Send response (voice or text)
        if voice_data:
            await message.reply_voice(voice=voice_data)
            log_action("INFO", "✅ Voice response sent", user_info)
        else:
            await message.reply_text(ai_response)
            log_action("INFO", "✅ Response sent", user_info)

        await log_response(user_id)

    except Exception as e:
        # Safely fetch user info for error logging
        try:
            user_info = fetch_user(message)
        except:
            user_info = {
                "user_id": "Unknown",
                "username": "Unknown",
                "full_name": "Unknown",
                "first_name": "Unknown",
                "last_name": None,
                "chat_id": message.chat.id if message.chat else "Unknown",
                "chat_type": "Unknown",
                "chat_title": "Unknown",
                "chat_username": "Unknown",
                "chat_link": "Unknown"
            }
        
        log_action("ERROR", f"❌ Error: {e}", user_info)
        try:
            await message.reply_text(get_error())
        except Exception as reply_error:
            log_action("ERROR", f"❌ Failed to send error message: {reply_error}", user_info)