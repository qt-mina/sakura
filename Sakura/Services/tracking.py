# Sakura/Services/tracking.py
from pyrogram.types import Message
from Sakura.Core.helpers import log_action
from Sakura.Database.database import save_user, save_group
from Sakura import state

async def track_user(message: Message, user_info: dict) -> None:
    """Track user and chat IDs for broadcasting (fast memory + async database)"""
    user_id = user_info["user_id"]
    chat_id = user_info["chat_id"]
    chat_type = user_info["chat_type"]

    if chat_type == "private":
        if user_id not in state.user_ids:
            state.user_ids.add(user_id)
            await save_user(
                user_id,
                user_info.get("username"),
                user_info.get("first_name"),
                user_info.get("last_name")
            )
            log_action("INFO", f"👤 New user tracked for broadcasting", user_info)

    elif chat_type in ['group', 'supergroup']:
        if chat_id not in state.group_ids:
            state.group_ids.add(chat_id)
            await save_group(
                chat_id,
                user_info.get("chat_title"),
                user_info.get("chat_username"),
                chat_type
            )
            log_action("INFO", f"📢 New group tracked for broadcasting", user_info)
