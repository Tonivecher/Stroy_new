import asyncio
import logging
import signal
import os
import json
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.token import validate_token
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiohttp.web import AppRunner, TCPSite, middleware

from config.settings import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from handlers.base import router as base_router
from handlers.estimate import router as estimate_router
from handlers.knowledge import router as knowledge_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

# Check if running on Railway
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT') is not None

async def health_check(request):
    """Health check endpoint for Railway."""
    return web.Response(text='OK', status=200)

# Middleware для обработки ошибок JSON в запросах
@middleware
async def error_middleware(request, handler):
    """Middleware для обработки ошибок в запросах."""
    try:
        return await handler(request)
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {str(e)}")
        return web.Response(text='Invalid JSON', status=400)
    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return web.Response(text='Internal Server Error', status=500)

async def on_startup(bot: Bot):
    """Actions to perform on bot startup."""
    logging.info("Bot is starting up...")
    if IS_RAILWAY and WEBHOOK_URL:
        logging.info("Running on Railway environment with webhook")
        logging.info(f"Setting webhook to: {WEBHOOK_URL}")
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
        logging.info("Running in polling mode")
        await bot.delete_webhook(drop_pending_updates=True)

async def on_shutdown(bot: Bot):
    """Actions to perform on bot shutdown."""
    logging.info("Bot is shutting down...")
    if IS_RAILWAY and WEBHOOK_URL:
        try:
            await bot.delete_webhook()
            logging.info("Webhook deleted")
        except Exception as e:
            logging.error(f"Error deleting webhook: {e}")

# Кастомный обработчик запросов вебхука с обработкой ошибок
class SafeRequestHandler(SimpleRequestHandler):
    async def handle(self, request: web.Request) -> web.Response:
        """
        Handler for webhook requests with error handling.
        """
        try:
            if request.content_length:
                try:
                    webhook_data = await request.json()
                    return await self.process_webhook_update(webhook_data)
                except json.JSONDecodeError as e:
                    logging.error(f"JSON Decode Error in webhook request: {str(e)}")
                    return web.Response(text="Invalid JSON data", status=400)
            return web.Response(text="No data provided", status=400)
        except Exception as e:
            logging.error(f"Error processing webhook: {str(e)}")
            return web.Response(text="Internal server error", status=500)

async def main():
    """Main function to start the bot."""
    # Validate token
    if not validate_token(BOT_TOKEN):
        logging.error("Invalid bot token!")
        return

    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(base_router)
    dp.include_router(estimate_router)
    dp.include_router(knowledge_router)

    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if IS_RAILWAY and WEBHOOK_URL:
        # Create aiohttp application for webhook
        app = web.Application(middlewares=[error_middleware])

        # Add health check endpoint
        app.router.add_get('/health', health_check)

        # Используем кастомный обработчик webhook с обработкой ошибок
        webhook_requests_handler = SafeRequestHandler(
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
            port=int(os.environ.get('PORT', 8080))
        )
        await site.start()
        logging.info(f"Web server started on port {os.environ.get('PORT', 8080)}")

        # Run forever
        await asyncio.Event().wait()
    else:
        # Start polling
        await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True) 