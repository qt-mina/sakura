from typing import Optional, Dict

from Sakura.Chat.chat import get_response as _get_chat_response
from Sakura.Core.helpers import get_error, log_action
from Sakura.Database.conversation import add_history


async def get_response(
    user_message: str,
    user_name: str,
    user_info: Dict[str, any],
    user_id: int,
    image_bytes: Optional[bytes] = None
) -> str:
    """Gets a response from the AI."""
    try:
        response = await _get_chat_response(user_message, user_id, user_info, image_bytes)

        if response is None:
            log_action("ERROR", "❌ Failed to get AI response", user_info)
            return get_error()

        # Prepare message for history
        history_user_message = user_message
        if image_bytes:
            history_user_message = f"[Image: {user_message}]" if user_message else "[Image sent]"

        # Add to history
        await add_history(user_id, history_user_message, is_user=True)
        await add_history(user_id, response, is_user=False)
        
        return response

    except Exception as e:
        log_action("ERROR", f"❌ Error getting AI response: {e}", user_info)
        return get_error()