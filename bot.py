import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот-помощник для строительных расчетов.\n"
        "Пока я только учусь, но скоро смогу помочь вам с:\n"
        "- Расчетом площади помещений\n"
        "- Подбором материалов\n"
        "- Расчетом стоимости ремонта\n"
        "- Созданием отчетов\n\n"
        "Используйте /help для получения справки."
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🔍 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n\n"
        "❗️ Остальные функции находятся в разработке."
    )

async def main():
    # Delete webhook before polling
    await bot.delete_webhook(drop_pending_updates=True)
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 