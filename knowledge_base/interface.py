"""
Интерфейс для взаимодействия с базой знаний.
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from .loader import KnowledgeLoader
from .search import KnowledgeSearch

# Настройка логирования
logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Основной класс интерфейса базы знаний."""
    
    def __init__(self, base_path: str = None):
        """
        Инициализация базы знаний.
        
        Args:
            base_path: Путь к директории с данными. По умолчанию используется
                      директория data внутри пакета knowledge_base.
        """
        self.loader = KnowledgeLoader(base_path)
        self.search = KnowledgeSearch(base_path)
        logger.info("Инициализирована база знаний")
    
    def get_categories(self) -> List[str]:
        """
        Получение списка категорий.
        
        Returns:
            Список названий категорий.
        """
        return self.loader.get_categories()
    
    def get_item(self, category: str, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Получение конкретного элемента.
        
        Args:
            category: Название категории.
            item_id: Идентификатор элемента.
            
        Returns:
            Данные элемента или None, если элемент не найден.
        """
        return self.loader.load_item(category, item_id)
    
    def add_item(self, category: str, item_id: str, data: Dict[str, Any]) -> bool:
        """
        Добавление элемента в базу знаний.
        
        Args:
            category: Название категории.
            item_id: Идентификатор элемента.
            data: Данные для сохранения.
            
        Returns:
            True в случае успешного сохранения, иначе False.
        """
        return self.loader.save_item(category, item_id, data)
    
    def search_knowledge(self, query: str, categories: List[str] = None) -> List[Dict[str, Any]]:
        """
        Поиск в базе знаний.
        
        Args:
            query: Поисковый запрос.
            categories: Список категорий для поиска. Если None, поиск по всем категориям.
            
        Returns:
            Список найденных элементов.
        """
        return self.search.simple_search(query, categories)
    
    def search_by_field(self, field: str, value: str, categories: List[str] = None) -> List[Dict[str, Any]]:
        """
        Поиск по конкретному полю.
        
        Args:
            field: Имя поля для поиска.
            value: Значение для поиска.
            categories: Список категорий для поиска. Если None, поиск по всем категориям.
            
        Returns:
            Список найденных элементов.
        """
        return self.search.search_by_field(field, value, categories)
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """
        Форматирование результата для вывода пользователю.
        
        Args:
            result: Данные элемента.
            
        Returns:
            Отформатированный текст для вывода.
        """
        # Базовое форматирование, можно настроить по своему усмотрению
        output = []
        
        # Добавляем заголовок, если он есть
        if 'title' in result:
            output.append(f"<b>{result['title']}</b>")
        
        # Добавляем описание, если оно есть
        if 'description' in result:
            output.append(f"{result['description']}")
        
        # Добавляем другие поля, исключая служебные
        for key, value in result.items():
            if key not in ['title', 'description'] and not key.startswith('_'):
                # Форматируем в зависимости от типа данных
                if isinstance(value, list):
                    # Для списков
                    list_items = "\n".join([f"  • {item}" for item in value])
                    output.append(f"<b>{key}:</b>\n{list_items}")
                elif isinstance(value, dict):
                    # Для словарей
                    dict_items = "\n".join([f"  • {k}: {v}" for k, v in value.items()])
                    output.append(f"<b>{key}:</b>\n{dict_items}")
                else:
                    # Для простых значений
                    output.append(f"<b>{key}:</b> {value}")
        
        # Добавляем метаинформацию
        if '_category' in result:
            output.append(f"\n<i>Категория: {result['_category']}</i>")
        
        return "\n\n".join(output)
    
    def get_help_text(self) -> str:
        """
        Получение справочного текста о базе знаний.
        
        Returns:
            Справочный текст.
        """
        categories = self.get_categories()
        
        help_text = [
            "<b>База знаний StroyHelper</b>",
            "",
            "База знаний содержит информацию о строительных материалах, технологиях и расчетах.",
            "",
            "<b>Доступные категории:</b>"
        ]
        
        for category in categories:
            help_text.append(f"  • {category}")
        
        help_text.extend([
            "",
            "<b>Как использовать:</b>",
            "  • Используйте команду /search <запрос> для поиска",
            "  • Используйте команду /category <категория> для просмотра категории",
            "  • Используйте команду /help_kb для вывода этой справки"
        ])
        
        return "\n".join(help_text) 