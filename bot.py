import asyncio
import logging
import signal
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.token import validate_token
from aiogram.client.default import DefaultBotProperties

from config.settings import BOT_TOKEN
from handlers.base import router as base_router
from handlers.estimate import router as estimate_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Global variables
bot = None
dp = None

async def on_startup():
    """Startup actions"""
    logger.info("Performing startup actions...")
    if bot:
        # Delete webhook and drop pending updates
        logger.info("Deleting webhook and dropping updates...")
        await bot.delete_webhook(drop_pending_updates=True)
        # Wait for webhook to be fully deleted
        await asyncio.sleep(1)
        # Test connection
        me = await bot.get_me()
        logger.info(f"Bot started successfully: @{me.username}")

async def on_shutdown():
    """Shutdown actions"""
    logger.info("Performing shutdown actions...")
    if bot:
        await bot.session.close()
        logger.info("Bot session closed")

def signal_handler(signum, frame):
    """Handle termination signals"""
    logger.info(f"Received signal {signum}")
    raise SystemExit()

async def main():
    global bot, dp
    
    try:
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Initialize bot
        logger.info("Initializing bot...")
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Initialize dispatcher
        dp = Dispatcher(storage=MemoryStorage())
        
        # Register routers
        logger.info("Registering routers...")
        dp.include_router(base_router)
        dp.include_router(estimate_router)
        
        # Startup
        await on_startup()
        
        # Start polling
        logger.info("Starting polling...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            close_bot_session=True,
            polling_timeout=30,
            handle_signals=False,
            reset_webhook=True
        )
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        raise
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True) 