from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.settings import MATERIAL_CATEGORIES
from data.materials import get_materials_by_category

def get_material_keyboard():
    """Get keyboard for material actions."""
    keyboard = [
        [KeyboardButton(text="📝 Добавить материал")],
        [KeyboardButton(text="📊 Показать материалы")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_material_categories():
    """Get keyboard with material categories."""
    keyboard = [
        [KeyboardButton(text="🧱 Стены")],
        [KeyboardButton(text="⬜ Потолок")],
        [KeyboardButton(text="⬜ Пол")],
        [KeyboardButton(text="🚪 Двери")],
        [KeyboardButton(text="🪟 Окна")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_material_units():
    """Get keyboard with material units."""
    keyboard = [
        [KeyboardButton(text="м²")],
        [KeyboardButton(text="м³")],
        [KeyboardButton(text="шт")],
        [KeyboardButton(text="кг")],
        [KeyboardButton(text="л")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_material_categories_keyboard() -> ReplyKeyboardMarkup:
    """Create keyboard with material categories."""
    keyboard = []
    
    for value in MATERIAL_CATEGORIES.values():
        keyboard.append([KeyboardButton(text=value)])
    
    keyboard.append([KeyboardButton(text="🏠 Главное меню")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def get_materials_keyboard(category: str) -> ReplyKeyboardMarkup:
    """Create keyboard with materials for specific category."""
    materials = get_materials_by_category(category)
    keyboard = []
    
    for material in materials.values():
        keyboard.append([KeyboardButton(text=material.name)])
    
    keyboard.append([KeyboardButton(text="⬅️ Назад")])
    keyboard.append([KeyboardButton(text="🏠 Главное меню")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    ) 