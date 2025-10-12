# Sakura/Chat/response.py
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
    """Gets a response from the AI.
    
    This function always returns a string, never None.
    If the AI fails to respond, it returns an error message.
    
    Args:
        user_message: The message from the user
        user_name: The user's name
        user_info: Dictionary containing user information
        user_id: The user's ID
        image_bytes: Optional image bytes if user sent an image
        
    Returns:
        str: The AI response or an error message (never None)
    """
    try:
        response = await _get_chat_response(user_message, user_id, user_info, image_bytes)

        # If response is None or empty, return error message
        if not response:
            log_action("ERROR", "❌ Failed to get AI response (None or empty returned)", user_info)
            error_msg = get_error()
            # Don't save failed responses to history
            return error_msg if error_msg else "Sorry, I'm having trouble responding right now."

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
        error_msg = get_error()
        return error_msg if error_msg else "Sorry, something went wrong."
