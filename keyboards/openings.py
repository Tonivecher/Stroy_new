from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_openings_keyboard() -> ReplyKeyboardMarkup:
    """Get the openings management keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🚪 Дверь"),
                KeyboardButton(text="🪟 Окно")
            ],
            [
                KeyboardButton(text="📋 Список проемов"),
                KeyboardButton(text="✏️ Редактировать")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    ) 