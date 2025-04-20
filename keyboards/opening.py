from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_opening_keyboard() -> ReplyKeyboardMarkup:
    """Get the opening management keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Добавить проем"),
                KeyboardButton(text="❌ Удалить проем")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    ) 