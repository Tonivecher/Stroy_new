from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_room_keyboard() -> ReplyKeyboardMarkup:
    """Get the room management keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Добавить комнату"),
                KeyboardButton(text="❌ Удалить комнату")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    ) 