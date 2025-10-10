import asyncio
from pyrogram.types import Message
from Sakura.Core.helpers import log_action
from Sakura.Database.database import save_user, save_group
from Sakura import state

async def track_user(message: Message, user_info: dict) -> None:
    """Track new users for broadcasting (fast memory + async database)."""
    user_id = user_info["user_id"]

    # Only track new users
    if user_id not in state.user_ids:
        state.user_ids.add(user_id)
        asyncio.create_task(save_user(
            user_id,
            user_info.get("username"),
            user_info.get("first_name"),
            user_info.get("last_name")
        ))
        log_action("INFO", f"👤 New user tracked for broadcasting", user_info)