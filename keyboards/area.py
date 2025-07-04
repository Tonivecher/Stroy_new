from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_area_keyboard() -> ReplyKeyboardMarkup:
    """Get the area calculation keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏠 Помещение"),
                KeyboardButton(text="📐 Проемы")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    ) 