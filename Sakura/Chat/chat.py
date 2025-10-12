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
) -> Optional[str]:
    """Get response from Gemini API using ChatSession.
    
    Returns:
        str: The AI response text
        None: If an error occurred or response is empty
    """
    user_name = user_info.get("first_name", "User")

    # Convert user_message to plain string if it's not already
    message_text = str(user_message) if user_message else ""

    log_action("DEBUG", f"🤖 Getting AI response for '{message_text}'", user_info)

    if not state.gemini_client:
        log_action("WARNING", "❌ Chat client not available", user_info)
        return None

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
                "max_output_tokens": 500,        # Increased limit for response (was 200)
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
        
        ai_response = response.text.strip() if response.text else None

        if not ai_response:
            # Check why the response is empty and log cleanly
            finish_reason = None
            usage_info = ""
            
            if hasattr(response, 'candidates') and response.candidates:
                finish_reason = str(getattr(response.candidates[0], 'finish_reason', ''))
            
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                metadata = response.usage_metadata
                prompt_tokens = getattr(metadata, 'prompt_token_count', 0)
                thought_tokens = getattr(metadata, 'thoughts_token_count', 0)
                total_tokens = getattr(metadata, 'total_token_count', 0)
                usage_info = f" [Tokens: {prompt_tokens} prompt + {thought_tokens} thoughts = {total_tokens} total]"
            
            # Clean, readable logs based on finish reason
            if 'MAX_TOKENS' in finish_reason:
                log_action("WARNING", f"⚠️ AI response truncated (hit token limit){usage_info}", user_info)
            elif 'SAFETY' in finish_reason:
                log_action("WARNING", "⚠️ AI response blocked by safety filters", user_info)
            elif 'RECITATION' in finish_reason:
                log_action("WARNING", "⚠️ AI response blocked (detected copyrighted content)", user_info)
            else:
                log_action("WARNING", f"⚠️ AI returned empty response (reason: {finish_reason or 'unknown'})", user_info)
            
            return None

        # Update history with plain string
        await update_history(user_id, message_text, ai_response)
        log_action("INFO", f"✅ AI response generated: '{ai_response}'", user_info)

        return ai_response

    except Exception as e:
        # Extract just the error type and message, not the full traceback
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Clean up common Gemini API errors for better readability
        if "429" in error_msg or "quota" in error_msg.lower():
            log_action("ERROR", f"❌ AI API rate limit exceeded (quota exhausted)", user_info)
        elif "401" in error_msg or "api key" in error_msg.lower():
            log_action("ERROR", f"❌ AI API authentication failed (invalid API key)", user_info)
        elif "404" in error_msg or "not found" in error_msg.lower():
            log_action("ERROR", f"❌ AI model not found ({AI_MODEL})", user_info)
        elif "timeout" in error_msg.lower():
            log_action("ERROR", f"❌ AI API request timed out", user_info)
        elif "connection" in error_msg.lower():
            log_action("ERROR", f"❌ AI API connection failed", user_info)
        else:
            # For unexpected errors, show type and brief message
            log_action("ERROR", f"❌ AI API error: {error_type} - {error_msg[:100]}", user_info)
        
        return None