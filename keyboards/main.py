from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.settings import MATERIAL_CATEGORIES

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Create the main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔲 Рассчитать площадь")],
            [KeyboardButton(text="🏠 Мои помещения")],
            [KeyboardButton(text="📦 Материалы")],
            [KeyboardButton(text="📊 Мои сметы")],
            [KeyboardButton(text="🧮 Расчет материалов")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    return keyboard

def get_estimate_keyboard() -> ReplyKeyboardMarkup:
    """Create keyboard for estimate management."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Добавить материал")],
            [KeyboardButton(text="📊 Показать смету")],
            [KeyboardButton(text="🧮 Расчет материалов")],
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    return keyboard 