import asyncio
import uvloop
from pyrogram import Client
from pyrogram.errors import FloodWait
from Sakura.Core.config import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, OWNER_ID
from Sakura.Core.logging import logger
from Sakura.Core.server import start_server_thread
from Sakura.Core.utils import validate_config
from Sakura.Database.database import connect_database, close_database
from Sakura.Database.valkey import connect_cache, close_cache
from Sakura.Services.cleanup import cleanup_conversations
from Sakura.Chat.chat import init_client
from Sakura import state
from Sakura.Modules.commands import COMMANDS


async def setup_commands(app: Client) -> None:
    """Setup bot commands menu"""
    try:
        await app.set_bot_commands(COMMANDS)
        logger.info("✅ Bot commands menu set successfully")
    except FloodWait as e:
        logger.warning(f"⏳ FloodWait: Sleeping for {e.value} seconds before retrying set_bot_commands...")
        await asyncio.sleep(e.value)
        return await setup_commands(app)  # retry after sleep
    except Exception as e:
        logger.error(f"Failed to set bot commands: {e}")


async def post_init(app: Client):
    """Post initialization tasks"""
    valkey_success = await connect_cache()
    if not valkey_success:
        logger.warning("⚠️ Valkey initialization failed. Bot will continue with memory fallback.")
    db_success = await connect_database()
    if not db_success:
        logger.error("❌ Database initialization failed. Bot will continue without persistence.")

    await setup_commands(app)
    state.cleanup_task = asyncio.create_task(cleanup_conversations())
    logger.info("🌸 Sakura Bot initialization completed!")


async def post_shutdown(app: Client):
    """Post shutdown tasks"""
    if state.cleanup_task and not state.cleanup_task.done():
        logger.info("🛑 Cancelling cleanup task...")
        state.cleanup_task.cancel()
        try:
            await state.cleanup_task
        except asyncio.CancelledError:
            logger.info("✅ Cleanup task cancelled successfully")
    await close_database()
    await close_cache()
    logger.info("🌸 Sakura Bot shutdown completed!")


async def sakura() -> None:
    """Main function to initialize and run the bot"""
    logger.info("🌸 Sakura Bot is starting up...")
    if not validate_config():
        return

    try:
        uvloop.install()
        logger.info("🚀 uvloop installed successfully")
    except ImportError:
        logger.warning("⚠️ uvloop not available")
    except Exception as e:
        logger.warning(f"⚠️ uvloop setup failed: {e}")

    logger.info("🚀 Initializing clients...")
    start_server_thread()
    init_client()

    app = Client(
        "sakura",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="Sakura.Modules")
    )

    while True:  # Loop to retry after FloodWait without recursion
        try:
            await app.start()
            await post_init(app)
            logger.info("🌸 Sakura Bot is now online!")
            await asyncio.Event().wait()
        except FloodWait as e:
            logger.warning(f"⏳ FloodWait triggered: Sleeping for {e.value} seconds...")
            await asyncio.sleep(e.value)
            logger.info("🔄 Retrying after FloodWait...")
            continue  # retry loop
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"💥 An unexpected error occurred: {e}", exc_info=True)
            break
        finally:
            logger.info("🔌 Shutting down...")
            await post_shutdown(app)
            if app.is_connected:
                await app.stop()
            logger.info("🌸 Sakura Bot has been shut down.")
            break  # exit loop after cleanup


if __name__ == "__main__":
    try:
        asyncio.run(sakura())
    except KeyboardInterrupt:
        pass