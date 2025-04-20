from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_help_keyboard() -> ReplyKeyboardMarkup:
    """Create keyboard with help options."""
    keyboard = [
        [
            KeyboardButton(text="❓ Как пользоваться"),
            KeyboardButton(text="📞 Контакты")
        ],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    ) 