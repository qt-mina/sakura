import base64
from typing import Optional, Dict
from google import genai
from Sakura.Core.config import GEMINI_API_KEY, AI_MODEL
from Sakura.Core.logging import logger
from Sakura.Core.helpers import log_action, get_fallback, get_error
from Sakura.Database.conversation import get_history, update_history
from Sakura.Chat.prompts import SAKURA_PROMPT
from Sakura import state

def init_client():
    """Initialize Google Gemini client for chat."""
    if not GEMINI_API_KEY:
        logger.warning("⚠️ No Gemini API key found, chat functionality will be disabled.")
        return
    logger.info("🫡 Initializing Google GenAI API key.")
    try:
        state.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("✅ Chat client (Gemini) initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize chat client: {e}")

async def get_response(
    user_message: str,
    user_id: int,
    user_info: Dict[str, any],
    image_bytes: Optional[bytes] = None
) -> str:
    """Get response from Gemini API using ChatSession."""
    user_name = user_info.get("first_name", "User")

    # Convert user_message to plain string if it's not already
    message_text = str(user_message) if user_message else ""

    log_action("DEBUG", f"🤖 Getting AI response for '{message_text[:50]}...'", user_info)

    if not state.gemini_client:
        log_action("WARNING", "❌ Chat client not available, using fallback response", user_info)
        return get_fallback()

    try:
        # Get chat history
        history = await get_history(user_id)

        # Build history in the correct format for Gemini
        formatted_history = []
        if history:
            for msg in history:
                role = "user" if msg['role'] == 'user' else "model"
                formatted_history.append({
                    "role": role,
                    "parts": [{"text": str(msg['content'])}]
                })

        # Initialize chat session with system prompt and history
        chat_session = state.gemini_client.chats.create(
            model=AI_MODEL,
            config={
                "system_instruction": f"{SAKURA_PROMPT}\nUser name: {user_name}",
                "temperature": 1.0,
                "max_output_tokens": 200,        # Limit response length
            },
            history=formatted_history
        )

        # Send message and get response
        if image_bytes:
            # Create a Part object with inline data
            image_part = genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
            response = chat_session.send_message([
                message_text or 'What do you see in this image?',
                image_part
            ])
        else:
            response = chat_session.send_message(message_text)

        ai_response = response.text.strip() if response.text else get_fallback()

        # Update history with plain string
        await update_history(user_id, message_text, ai_response)
        log_action("INFO", f"✅ AI response generated: '{ai_response[:50]}...'", user_info)

        return ai_response

    except Exception as e:
        error_message = f"❌ AI API error: {e}"
        log_action("ERROR", error_message, user_info)
        return get_error()
