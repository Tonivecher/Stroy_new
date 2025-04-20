from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_area_keyboard():
    """Get keyboard for area calculation."""
    keyboard = [
        [KeyboardButton(text="🏠 Помещение")],
        [KeyboardButton(text="🚪 Проем")],
        [KeyboardButton(text="📏 Стены")],
        [KeyboardButton(text="⬜ Пол")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 