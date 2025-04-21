from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.settings import MATERIAL_CATEGORIES

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get the main keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔲 Рассчитать площадь"),
                KeyboardButton(text="🏠 Мои помещения"),
                KeyboardButton(text="✏️ Редактировать помещение")
            ],
            [
                KeyboardButton(text="📦 Материалы"),
                KeyboardButton(text="🧮 Расчет материалов"),
                KeyboardButton(text="🏠 Главное меню")
            ],
            [
                KeyboardButton(text="❓ Помощь")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_estimate_keyboard() -> ReplyKeyboardMarkup:
    """Get the estimate calculation keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Показать материалы"),
                KeyboardButton(text="📝 Добавить материал")
            ],
            [
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )