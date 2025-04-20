from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_openings_keyboard():
    """Get keyboard for openings management."""
    keyboard = [
        [KeyboardButton(text="🚪 Добавить проем")],
        [KeyboardButton(text="📋 Список проемов")],
        [KeyboardButton(text="✏️ Редактировать")],
        [KeyboardButton(text="❌ Удалить")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 