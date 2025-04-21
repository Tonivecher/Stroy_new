"""
Модуль для поиска в базе знаний.
"""
import logging
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import json
import re

# Настройка логирования
logger = logging.getLogger(__name__)

class KnowledgeSearch:
    """Класс для поиска в базе знаний."""
    
    def __init__(self, base_path: str = None):
        """
        Инициализация поиска по базе знаний.
        
        Args:
            base_path: Путь к директории с данными. По умолчанию используется
                      директория data внутри пакета knowledge_base.
        """
        if base_path is None:
            self.base_path = Path(__file__).parent / 'data'
        else:
            self.base_path = Path(base_path)
        
        logger.info(f"Инициализирован поиск знаний с базовым путём: {self.base_path}")
    
    def _preprocess_query(self, query: str) -> str:
        """
        Предобработка запроса.
        
        Args:
            query: Исходный запрос.
            
        Returns:
            Обработанный запрос.
        """
        # Приведение к нижнему регистру
        query = query.lower()
        
        # Удаление лишних пробелов
        query = ' '.join(query.split())
        
        return query
    
    def simple_search(self, query: str, categories: List[str] = None) -> List[Dict[str, Any]]:
        """
        Простой поиск по ключевым словам.
        
        Args:
            query: Поисковый запрос.
            categories: Список категорий для поиска. Если None, поиск по всем категориям.
            
        Returns:
            Список найденных элементов.
        """
        query = self._preprocess_query(query)
        results = []
        
        if not categories:
            # Поиск по всем категориям
            categories = [d.name for d in self.base_path.iterdir() 
                         if d.is_dir() and not d.name.startswith('__')]
        
        for category in categories:
            category_path = self.base_path / category
            
            if not category_path.exists():
                logger.warning(f"Категория '{category}' не найдена.")
                continue
            
            # Поиск во всех JSON файлах категории
            for file_path in category_path.glob('*.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Преобразуем JSON в строку для поиска
                        data_str = json.dumps(data, ensure_ascii=False).lower()
                        
                        if query in data_str:
                            # Добавляем метаданные для результата
                            data['_category'] = category
                            data['_id'] = file_path.stem
                            results.append(data)
                except Exception as e:
                    logger.error(f"Ошибка при поиске в файле {file_path}: {e}")
        
        return results
    
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
        value = str(value).lower()
        results = []
        
        if not categories:
            # Поиск по всем категориям
            categories = [d.name for d in self.base_path.iterdir() 
                         if d.is_dir() and not d.name.startswith('__')]
        
        for category in categories:
            category_path = self.base_path / category
            
            if not category_path.exists():
                logger.warning(f"Категория '{category}' не найдена.")
                continue
            
            # Поиск во всех JSON файлах категории
            for file_path in category_path.glob('*.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Проверяем наличие поля и совпадение значения
                        if field in data and str(data[field]).lower() == value:
                            # Добавляем метаданные для результата
                            data['_category'] = category
                            data['_id'] = file_path.stem
                            results.append(data)
                except Exception as e:
                    logger.error(f"Ошибка при поиске в файле {file_path}: {e}")
        
        return results
    
    def regex_search(self, pattern: str, categories: List[str] = None) -> List[Dict[str, Any]]:
        """
        Поиск по регулярному выражению.
        
        Args:
            pattern: Регулярное выражение для поиска.
            categories: Список категорий для поиска. Если None, поиск по всем категориям.
            
        Returns:
            Список найденных элементов.
        """
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            results = []
            
            if not categories:
                # Поиск по всем категориям
                categories = [d.name for d in self.base_path.iterdir() 
                             if d.is_dir() and not d.name.startswith('__')]
            
            for category in categories:
                category_path = self.base_path / category
                
                if not category_path.exists():
                    logger.warning(f"Категория '{category}' не найдена.")
                    continue
                
                # Поиск во всех JSON файлах категории
                for file_path in category_path.glob('*.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                            # Преобразуем JSON в строку для поиска
                            data_str = json.dumps(data, ensure_ascii=False)
                            
                            if regex.search(data_str):
                                # Добавляем метаданные для результата
                                data['_category'] = category
                                data['_id'] = file_path.stem
                                results.append(data)
                    except Exception as e:
                        logger.error(f"Ошибка при поиске в файле {file_path}: {e}")
            
            return results
        except re.error as e:
            logger.error(f"Ошибка в регулярном выражении: {e}")
            return [] 