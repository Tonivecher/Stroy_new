"""
Клавиатуры для работы с базой знаний.
"""
from typing import List, Dict, Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_categories_keyboard(categories: List[str]) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры со списком категорий.
    
    Args:
        categories: Список названий категорий.
        
    Returns:
        Инлайн-клавиатура с категориями.
    """
    keyboard = []
    
    # Добавляем кнопки для каждой категории
    for category in categories:
        keyboard.append([
            InlineKeyboardButton(
                text=category,
                callback_data=f"kb_category:{category}"
            )
        ])
    
    # Добавляем кнопку поиска
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 Поиск",
            callback_data="kb_search"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_search_results_keyboard(results: List[Dict[str, Any]], query: str) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с результатами поиска.
    
    Args:
        results: Список результатов поиска.
        query: Поисковый запрос.
        
    Returns:
        Инлайн-клавиатура с результатами.
    """
    keyboard = []
    
    # Добавляем кнопки для каждого результата
    for result in results:
        category = result.get('_category', 'unknown')
        item_id = result.get('_id', 'unknown')
        title = result.get('title', item_id)
        
        # Ограничиваем длину заголовка
        if len(title) > 30:
            title = title[:27] + "..."
        
        keyboard.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"kb_item:{category}:{item_id}"
            )
        ])
    
    # Добавляем кнопки навигации
    nav_buttons = []
    
    # Кнопка возврата к категориям
    nav_buttons.append(
        InlineKeyboardButton(
            text="📁 К категориям",
            callback_data="kb_back_to_categories"
        )
    )
    
    # Кнопка нового поиска
    nav_buttons.append(
        InlineKeyboardButton(
            text="🔍 Новый поиск",
            callback_data=f"kb_search:{query}"
        )
    )
    
    keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_back_to_categories_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с кнопкой возврата к категориям.
    
    Returns:
        Инлайн-клавиатура с кнопкой возврата.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="📁 К категориям",
                callback_data="kb_back_to_categories"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 