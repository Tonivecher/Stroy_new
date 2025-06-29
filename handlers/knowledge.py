"""
Обработчик команд для базы знаний.
"""
import logging
import json
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from knowledge_base.interface import KnowledgeBase
from keyboards.knowledge_keyboards import (
    create_categories_keyboard,
    create_search_results_keyboard,
    create_back_to_categories_keyboard
)

# Настройка логирования
logger = logging.getLogger(__name__)

# Создание роутера
router = Router(name="knowledge_router")

# Инициализация базы знаний
kb = KnowledgeBase()

# Определение состояний FSM
class KnowledgeStates(StatesGroup):
    """Состояния для работы с базой знаний."""
    waiting_for_search_query = State()
    viewing_category = State()
    viewing_item = State()

@router.message(Command("kb", "knowledge", "knowledgebase"))
async def cmd_knowledge_base(message: Message, state: FSMContext):
    """
    Обработчик команды для входа в режим базы знаний.
    
    Args:
        message: Сообщение пользователя.
        state: Контекст состояния.
    """
    try:
        categories = kb.get_categories()
        
        if not categories:
            await message.answer(
                "База знаний пока пуста. Скоро здесь появится полезная информация."
            )
            return
        
        # Сбрасываем состояние
        await state.clear()
        
        # Отправляем приветственное сообщение и клавиатуру категорий
        await message.answer(
            "Добро пожаловать в базу знаний StroyHelper!\n\n"
            "Выберите категорию для просмотра информации или "
            "используйте команду /search для поиска.",
            reply_markup=create_categories_keyboard(categories)
        )
    except Exception as e:
        logger.error(f"Ошибка при открытии базы знаний: {e}")
        await message.answer("Произошла ошибка при открытии базы знаний. Пожалуйста, попробуйте позже.")

@router.message(Command("help_kb"))
async def cmd_knowledge_help(message: Message):
    """
    Обработчик команды для получения справки по базе знаний.
    
    Args:
        message: Сообщение пользователя.
    """
    try:
        help_text = kb.get_help_text()
        await message.answer(help_text)
    except Exception as e:
        logger.error(f"Ошибка при получении справки: {e}")
        await message.answer("Произошла ошибка при получении справочной информации.")

@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    """
    Обработчик команды для поиска в базе знаний.
    
    Args:
        message: Сообщение пользователя.
        state: Контекст состояния.
    """
    try:
        # Если команда содержит текст после /search
        command_parts = message.text.split(maxsplit=1)
        
        if len(command_parts) > 1:
            query = command_parts[1].strip()
            await perform_search(message, query)
        else:
            # Запрашиваем поисковый запрос
            await message.answer(
                "Введите поисковый запрос:"
            )
            await state.set_state(KnowledgeStates.waiting_for_search_query)
    except Exception as e:
        logger.error(f"Ошибка при обработке команды поиска: {e}")
        await message.answer("Произошла ошибка при обработке команды поиска.")

@router.message(KnowledgeStates.waiting_for_search_query)
async def handle_search_query(message: Message, state: FSMContext):
    """
    Обработчик поискового запроса.
    
    Args:
        message: Сообщение пользователя.
        state: Контекст состояния.
    """
    try:
        query = message.text.strip()
        
        if not query:
            await message.answer(
                "Пожалуйста, введите текст для поиска или используйте /cancel для отмены."
            )
            return
        
        # Очищаем состояние
        await state.clear()
        
        # Выполняем поиск
        await perform_search(message, query)
    except Exception as e:
        logger.error(f"Ошибка при обработке поискового запроса: {e}")
        await message.answer("Произошла ошибка при обработке поискового запроса.")
        await state.clear()

async def perform_search(message: Message, query: str):
    """
    Выполнение поиска по запросу.
    
    Args:
        message: Сообщение пользователя.
        query: Поисковый запрос.
    """
    try:
        logger.info(f"Поиск по запросу: {query}")
        
        # Выполняем поиск
        results = kb.search_knowledge(query)
        
        if not results:
            await message.answer(
                f"К сожалению, по запросу '{query}' ничего не найдено.\n\n"
                f"Попробуйте использовать другие ключевые слова или просмотрите категории командой /kb."
            )
            return
        
        # Отправляем результаты поиска
        await message.answer(
            f"Найдено результатов: {len(results)}.\n\n"
            f"Выберите элемент для просмотра подробной информации:",
            reply_markup=create_search_results_keyboard(results, query)
        )
    except Exception as e:
        logger.error(f"Ошибка при выполнении поиска по запросу '{query}': {e}")
        await message.answer(f"Произошла ошибка при выполнении поиска. Пожалуйста, попробуйте позже.")

@router.message(Command("category"))
async def cmd_category(message: Message):
    """
    Обработчик команды для просмотра категории.
    
    Args:
        message: Сообщение пользователя.
    """
    try:
        # Если команда содержит название категории после /category
        command_parts = message.text.split(maxsplit=1)
        
        if len(command_parts) > 1:
            category_name = command_parts[1].strip()
            await show_category(message, category_name)
        else:
            # Отправляем список категорий
            categories = kb.get_categories()
            
            if not categories:
                await message.answer(
                    "База знаний пока пуста. Скоро здесь появится полезная информация."
                )
                return
            
            await message.answer(
                "Выберите категорию для просмотра:",
                reply_markup=create_categories_keyboard(categories)
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке команды просмотра категории: {e}")
        await message.answer("Произошла ошибка при получении списка категорий.")

async def show_category(message: Message, category_name: str):
    """
    Отображение содержимого категории.
    
    Args:
        message: Сообщение пользователя.
        category_name: Название категории.
    """
    try:
        # Загружаем данные категории
        category_data = kb.loader.load_category(category_name)
        
        if not category_data:
            await message.answer(f"Категория '{category_name}' пуста.")
            return
        
        # Формируем текст с элементами категории
        items_text = f"<b>Категория: {category_name}</b>\n\n"
        items_text += "Доступные элементы:\n"
        
        for item_id, data in category_data.items():
            title = data.get('title', item_id)
            items_text += f"• {title}\n"
        
        await message.answer(
            items_text,
            reply_markup=create_back_to_categories_keyboard()
        )
        
    except FileNotFoundError:
        await message.answer(f"Категория '{category_name}' не найдена.")
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка формата JSON в категории '{category_name}': {e}")
        await message.answer(f"Ошибка в данных категории '{category_name}'. Пожалуйста, сообщите администратору.")
    except Exception as e:
        logger.error(f"Ошибка при просмотре категории '{category_name}': {e}")
        await message.answer("Произошла ошибка при загрузке категории.")

@router.callback_query(F.data.startswith("kb_category:"))
async def on_category_selected(callback: CallbackQuery):
    """
    Обработчик выбора категории.
    
    Args:
        callback: Данные колбэка.
    """
    try:
        # Извлекаем название категории из данных колбэка
        category_name = callback.data.split(":", 1)[1]
        
        # Показываем содержимое категории
        await show_category(callback.message, category_name)
        
        # Отвечаем на колбэк, чтобы убрать часики
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при обработке выбора категории: {e}")
        await callback.message.answer("Произошла ошибка при выборе категории.")
        await callback.answer()

@router.callback_query(F.data.startswith("kb_item:"))
async def on_item_selected(callback: CallbackQuery):
    """
    Обработчик выбора элемента.
    
    Args:
        callback: Данные колбэка.
    """
    try:
        # Извлекаем категорию и ID элемента из данных колбэка
        # Формат: kb_item:category:item_id
        _, category, item_id = callback.data.split(":", 2)
        
        # Загружаем элемент
        item_data = kb.get_item(category, item_id)
        
        if not item_data:
            await callback.message.answer(f"Элемент не найден.")
            await callback.answer()
            return
        
        # Форматируем результат
        formatted_result = kb.format_result(item_data)
        
        # Отправляем информацию об элементе
        await callback.message.answer(
            formatted_result,
            reply_markup=create_back_to_categories_keyboard()
        )
        
        # Отвечаем на колбэк, чтобы убрать часики
        await callback.answer()
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка формата JSON при выборе элемента '{category}/{item_id}': {e}")
        await callback.message.answer("Ошибка в данных элемента. Пожалуйста, сообщите администратору.")
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при обработке выбора элемента: {e}")
        await callback.message.answer("Произошла ошибка при загрузке элемента.")
        await callback.answer()

@router.callback_query(F.data == "kb_back_to_categories")
async def on_back_to_categories(callback: CallbackQuery):
    """
    Обработчик кнопки возврата к категориям.
    
    Args:
        callback: Данные колбэка.
    """
    try:
        categories = kb.get_categories()
        
        await callback.message.answer(
            "Выберите категорию:",
            reply_markup=create_categories_keyboard(categories)
        )
        
        # Отвечаем на колбэк, чтобы убрать часики
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при возврате к категориям: {e}")
        await callback.message.answer("Произошла ошибка при загрузке категорий.")
        await callback.answer()

@router.callback_query(F.data.startswith("kb_search:"))
async def on_search_again(callback: CallbackQuery):
    """
    Обработчик кнопки повторного поиска.
    
    Args:
        callback: Данные колбэка.
    """
    try:
        # Извлекаем запрос из данных колбэка
        query = callback.data.split(":", 1)[1]
        
        # Выполняем поиск
        await perform_search(callback.message, query)
        
        # Отвечаем на колбэк, чтобы убрать часики
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при повторном поиске: {e}")
        await callback.message.answer("Произошла ошибка при выполнении поиска.")
        await callback.answer()

@router.callback_query(F.data == "kb_search")
async def on_search_button(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки поиска.
    
    Args:
        callback: Данные колбэка.
        state: Контекст состояния.
    """
    try:
        await callback.message.answer("Введите поисковый запрос:")
        await state.set_state(KnowledgeStates.waiting_for_search_query)
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при инициации поиска: {e}")
        await callback.message.answer("Произошла ошибка при инициации поиска.")
        await callback.answer() 