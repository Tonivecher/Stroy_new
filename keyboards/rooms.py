from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_rooms_keyboard():
    """Get keyboard for room management."""
    keyboard = [
        [KeyboardButton(text="🏠 Добавить помещение")],
        [KeyboardButton(text="📋 Список помещений")],
        [KeyboardButton(text="✏️ Редактировать")],
        [KeyboardButton(text="❌ Удалить")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 