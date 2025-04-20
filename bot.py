import asyncio
import logging
import signal
import os
import ssl
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.token import validate_token
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web, ClientSession, TCPConnector
from aiohttp.web import AppRunner, TCPSite

from config.settings import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from handlers.base import router as base_router
from handlers.estimate import router as estimate_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Check if running on Railway
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT') is not None

async def on_startup(bot: Bot):
    """Actions to perform on bot startup."""
    logging.info("Bot is starting up...")
    if IS_RAILWAY:
        logging.info("Running on Railway environment")
        try:
            # Set webhook with retry
            for attempt in range(3):
                try:
                    await bot.set_webhook(
                        url=WEBHOOK_URL,
                        drop_pending_updates=True
                    )
                    logging.info("Webhook set successfully")
                    break
                except Exception as e:
                    if attempt == 2:
                        logging.error(f"Failed to set webhook after 3 attempts: {e}")
                        raise
                    logging.warning(f"Attempt {attempt + 1} failed to set webhook: {e}")
                    await asyncio.sleep(2)
        except Exception as e:
            logging.error(f"Error setting webhook: {e}")
            raise
    else:
        logging.info("Not running on Railway, exiting...")
        os._exit(0)

async def on_shutdown(bot: Bot):
    """Actions to perform on bot shutdown."""
    logging.info("Bot is shutting down...")
    if IS_RAILWAY:
        try:
            await bot.delete_webhook()
            logging.info("Webhook deleted")
        except Exception as e:
            logging.error(f"Error deleting webhook: {e}")

async def main():
    """Main function to start the bot."""
    if not IS_RAILWAY:
        logging.info("Not running on Railway, exiting...")
        return

    # Validate token
    if not validate_token(BOT_TOKEN):
        logging.error("Invalid bot token!")
        return

    # Create aiohttp session with custom connector
    connector = TCPConnector(ssl=False)
    session = ClientSession(connector=connector)

    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(base_router)
    dp.include_router(estimate_router)

    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Create aiohttp application
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # Start web server
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(
        runner,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080)),
        ssl_context=None  # Отключаем SSL для Railway
    )
    await site.start()

    # Run forever
    try:
        await asyncio.Event().wait()
    finally:
        await session.close()
        await connector.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True) 