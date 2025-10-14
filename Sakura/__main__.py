# Sakura/__main__.py
import asyncio
import signal
import uvloop
from pyrogram import Client
from pyrogram.errors import FloodWait
from Sakura.Core.config import (
    API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, OWNER_ID,
    SAKURA_STICKERS_PACK, START_STICKERS_PACK, PAYMENT_STICKERS_PACK
)
from Sakura.Core.logging import logger
from Sakura.Modules.stickers import load_stickers
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

    if valkey_success:
        logger.info("📦 Loading all sticker packs into cache...")
        await load_all_stickers(app)

    state.cleanup_task = asyncio.create_task(cleanup_conversations())
    logger.info("🌸 Sakura Bot initialization completed!")


async def load_all_stickers(app: Client):
    """Load all sticker packs into the cache."""
    await asyncio.gather(
        load_stickers(app, SAKURA_STICKERS_PACK, "stickers:sakura"),
        load_stickers(app, START_STICKERS_PACK, "stickers:start"),
        load_stickers(app, PAYMENT_STICKERS_PACK, "stickers:payment")
    )


async def post_shutdown(app: Client):
    """Post shutdown tasks"""
    logger.info("🧹 Starting cleanup process...")
    
    if state.cleanup_task and not state.cleanup_task.done():
        logger.info("🛑 Cancelling cleanup task...")
        state.cleanup_task.cancel()
        try:
            await state.cleanup_task
        except asyncio.CancelledError:
            logger.info("✅ Cleanup task cancelled successfully")
    
    logger.info("📊 Closing database connections...")
    await close_database()
    
    logger.info("💾 Closing cache connections...")
    await close_cache()
    
    logger.info("🌸 Sakura Bot shutdown completed!")


async def sakura() -> None:
    """Main function to initialize and run the bot"""
    logger.info("🌸 Sakura Bot is starting up...")

    if not validate_config():
        logger.error("❌ Configuration validation failed!")
        return

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

    # Create an event for graceful shutdown
    shutdown_event = asyncio.Event()
    
    def signal_handler(signum):
        """Handle shutdown signals"""
        signame = signal.Signals(signum).name
        logger.info(f"🛑 Received {signame} signal, initiating graceful shutdown...")
        shutdown_event.set()
    
    # Register signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda s=sig: signal_handler(s))

    try:
        while True:
            try:
                logger.info("🔌 Starting Pyrogram client...")
                await app.start()
                await post_init(app)
                logger.info("🌸 Sakura Bot is now online!")
                
                # Wait for shutdown signal
                await shutdown_event.wait()
                logger.info("🛑 Shutdown signal received, stopping bot...")
                break
                
            except FloodWait as e:
                logger.warning(f"⏳ FloodWait triggered: Sleeping for {e.value} seconds...")
                await asyncio.sleep(e.value)
                logger.info("🔄 Retrying after FloodWait...")
                continue
                
            except KeyboardInterrupt:
                logger.info("🛑 Bot stopped by user (KeyboardInterrupt).")
                break
                
            except Exception as e:
                logger.error(f"💥 An unexpected error occurred: {e}", exc_info=True)
                break
                
    finally:
        logger.info("🔌 Shutting down Sakura...")
        await post_shutdown(app)
        
        if app.is_connected:
            logger.info("📡 Stopping Pyrogram client...")
            try:
                await app.stop()
                logger.info("✅ Pyrogram client stopped successfully")
            except Exception as e:
                logger.error(f"❌ Error stopping Pyrogram client: {e}")
        
        logger.info("🌸 Sakura Bot has been shut down gracefully.")


if __name__ == "__main__":
    logger.info("🌸 Sakura is getting ready...")

    try:
        uvloop.install()
        logger.info("⚡ Sakura using uvloop jutsu")
    except ImportError:
        logger.warning("💫 Sakura using default loop jutsu")
    except Exception as e:
        logger.warning(f"😭 Sakura uvloop jutsu failed: {e}")

    try:
        asyncio.run(sakura())
    except KeyboardInterrupt:
        logger.info("👋 Sakura says bye bye")
    except Exception as e:
        logger.error(f"👊 Sakura faced an enemy: {e}", exc_info=True)
    finally:
        logger.info("💤 Sakura gone for sleeping")