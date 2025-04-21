from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.settings import MATERIAL_CATEGORIES
from data.materials import get_materials_by_category

def get_material_keyboard() -> ReplyKeyboardMarkup:
    """Get the material management keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Добавить материал"),
                KeyboardButton(text="📊 Показать материалы")
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_material_categories() -> ReplyKeyboardMarkup:
    """Get the material categories keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Стены"),
                KeyboardButton(text="Потолок")
            ],
            [
                KeyboardButton(text="Пол"),
                KeyboardButton(text="Двери")
            ],
            [
                KeyboardButton(text="Окна"),
                KeyboardButton(text="⬅️ Назад")
            ],
            [
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_material_units() -> ReplyKeyboardMarkup:
    """Get the material units keyboard layout."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="м²"),
                KeyboardButton(text="м³")
            ],
            [
                KeyboardButton(text="шт"),
                KeyboardButton(text="кг")
            ],
            [
                KeyboardButton(text="л"),
                KeyboardButton(text="⬅️ Назад")
            ],
            [
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_material_categories_keyboard() -> ReplyKeyboardMarkup:
    """Create keyboard with material categories."""
    keyboard = []
    row = []
    
    # Добавляем по 2 категории в строку
    for i, value in enumerate(MATERIAL_CATEGORIES.values()):
        row.append(KeyboardButton(text=value))
        
        # После каждых 2 кнопок или если это последняя кнопка, добавляем строку
        if len(row) == 2 or i == len(MATERIAL_CATEGORIES) - 1:
            keyboard.append(row)
            row = []
    
    keyboard.append([KeyboardButton(text="🏠 Главное меню")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def get_materials_keyboard(category: str) -> ReplyKeyboardMarkup:
    """Create keyboard with materials for specific category."""
    materials = get_materials_by_category(category)
    keyboard = []
    row = []
    
    # Добавляем по 2 материала в строку
    for i, material in enumerate(materials.values()):
        row.append(KeyboardButton(text=material.name))
        
        # После каждых 2 кнопок или если это последняя кнопка, добавляем строку
        if len(row) == 2 or i == len(materials) - 1:
            keyboard.append(row)
            row = []
    
    keyboard.append([KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="🏠 Главное меню")])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    ) 