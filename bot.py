import asyncio
import logging
import signal
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.token import validate_token
from aiogram.client.default import DefaultBotProperties
from keep_alive import keep_alive

from config.settings import BOT_TOKEN
from handlers.base import router as base_router
from handlers.estimate import router as estimate_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Check if running on Railway
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT') is not None

async def on_startup():
    """Actions to perform on bot startup."""
    logging.info("Bot is starting up...")
    if IS_RAILWAY:
        logging.info("Running on Railway environment")
    else:
        logging.info("Not running on Railway, exiting...")
        os._exit(0)

async def on_shutdown():
    """Actions to perform on bot shutdown."""
    logging.info("Bot is shutting down...")

def signal_handler(signum, frame):
    """Handle system signals."""
    logging.info(f"Received signal {signum}")
    asyncio.run(on_shutdown())
    os._exit(0)

async def main():
    """Main function to start the bot."""
    if not IS_RAILWAY:
        logging.info("Not running on Railway, exiting...")
        return

    # Validate token
    if not validate_token(BOT_TOKEN):
        logging.error("Invalid bot token!")
        return

    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(base_router)
    dp.include_router(estimate_router)

    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 