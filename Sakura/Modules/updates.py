# Sakura/Modules/updates.py
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus, ChatType
from Sakura.Core.logging import logger
from Sakura.Database.database import remove_user, remove_group

@Client.on_chat_member_updated(filters.me)
async def my_chat_member_handler(client: Client, update: ChatMemberUpdated):
    """Handle when the bot's chat member status changes."""
    
    # Get the new status
    new_status = update.new_chat_member.status if update.new_chat_member else None
    old_status = update.old_chat_member.status if update.old_chat_member else None
    chat = update.chat

    # Log for debugging
    logger.info(f"🔄 Bot status changed in chat {chat.id} ({chat.type}): {old_status} -> {new_status}")

    # Handle when bot is blocked or removed
    if new_status in [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]:
        if chat.type == ChatType.PRIVATE:
            logger.info(f"🚫 User {chat.id} blocked the bot. Removing from database.")
            await remove_user(chat.id)
        elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            logger.info(f"👋 Bot was removed from group {chat.id} ({chat.title}). Removing from database.")
            await remove_group(chat.id)
    elif new_status == ChatMemberStatus.MEMBER:
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            logger.info(f"✅ Bot added to group {chat.id} ({chat.title})")
        elif chat.type == ChatType.PRIVATE:
            logger.info(f"✅ User {chat.id} unblocked the bot")