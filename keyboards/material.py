from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_material_keyboard() -> ReplyKeyboardMarkup:
    """Get the material management keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Добавить материал"),
                KeyboardButton(text="❌ Удалить материал")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    ) 