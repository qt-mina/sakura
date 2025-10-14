# Sakura/Modules/stickers.py
import random
import asyncio
import orjson
import base64
from pyrogram import Client, raw
from pyrogram.types import Message
from pyrogram.enums import ChatType
from Sakura.Core.helpers import fetch_user, log_action
from Sakura.Modules.typing import sticker_action
from Sakura import state


def parse_link(link: str) -> str:
    """Extract sticker pack name from Telegram link"""
    return link.split("/")[-1]


async def load_stickers(client: Client, pack_link: str, cache_key: str):
    """Load stickers from a pack and cache them in Valkey."""
    system_user_info = {"user_id": "System", "username": "Startup", "chat_id": "Logger"}
    if not state.valkey_client:
        log_action("ERROR", "Valkey client not available for sticker loading.", system_user_info)
        return

    try:
        pack_name = parse_link(pack_link)
        sticker_set = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=pack_name),
                hash=0
            )
        )

        # Serialize sticker documents to a JSON-compatible format
        stickers_to_cache = [
            {
                "id": doc.id,
                "access_hash": doc.access_hash,
                "file_reference": base64.b64encode(doc.file_reference).decode('utf-8'),
            }
            for doc in sticker_set.documents
        ]

        await state.valkey_client.set(cache_key, orjson.dumps(stickers_to_cache))
        log_action("INFO", f"✅ Loaded and cached {len(stickers_to_cache)} stickers from {pack_name}.", system_user_info)

    except Exception as e:
        log_action("ERROR", f"❌ Failed to load/cache sticker pack {pack_link}: {e}", system_user_info)


async def get_random_sticker(cache_key: str, user_info: dict) -> dict | None:
    """Get a random sticker from the Valkey cache."""
    if not state.valkey_client:
        log_action("ERROR", "Valkey client not available for getting sticker.", user_info)
        return None

    cached_stickers = await state.valkey_client.get(cache_key)
    if not cached_stickers:
        log_action("WARNING", f"⚠️ No stickers found in cache for key: {cache_key}", user_info)
        return None

    sticker_list = orjson.loads(cached_stickers)
    return random.choice(sticker_list) if sticker_list else None


async def send_cached_sticker(client: Client, chat_id: int, sticker_data: dict, user_info: dict, reply_to_message_id: int | None = None):
    """Constructs and sends a sticker from cached data using raw API."""
    try:
        log_action("DEBUG", f"📤 Sending random sticker: {sticker_data['id']}", user_info)

        sticker_input = raw.types.InputMediaDocument(
            id=raw.types.InputDocument(
                id=sticker_data["id"],
                access_hash=sticker_data["access_hash"],
                file_reference=base64.b64decode(sticker_data["file_reference"])
            )
        )

        peer = await client.resolve_peer(chat_id)
        reply_to = None
        if reply_to_message_id:
            reply_to = raw.types.InputReplyToMessage(
                reply_to_msg_id=reply_to_message_id
            )

        await client.invoke(
            raw.functions.messages.SendMedia(
                peer=peer,
                media=sticker_input,
                message="",
                random_id=client.rnd_id(),
                reply_to=reply_to
            )
        )
        log_action("INFO", "✅ Sent sticker response", user_info)

    except Exception as e:
        log_action("ERROR", f"❌ Failed to send sticker: {e}", user_info)


async def handle_sticker(client: Client, message: Message) -> None:
    """Handle sticker messages"""
    user_info = fetch_user(message)
    log_action("INFO", "🎭 Sticker message received", user_info)

    await sticker_action(client, message.chat.id, user_info)

    random_sticker_data = await get_random_sticker("stickers:sakura", user_info)
    if not random_sticker_data:
        log_action("ERROR", "No sticker found to send.", user_info)
        return

    reply_id = None
    if (message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP] and
        message.reply_to_message and
        message.reply_to_message.from_user.id == client.me.id):
        reply_id = message.reply_to_message.id

    await send_cached_sticker(client, message.chat.id, random_sticker_data, user_info, reply_to_message_id=reply_id)
