"""
Модуль для векторизации текста и семантического поиска.
"""
import logging
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Настройка логирования
logger = logging.getLogger(__name__)

class KnowledgeVectorizer:
    """
    Класс для векторизации текста и семантического поиска.
    
    Примечание: Для работы требуется установить дополнительные зависимости:
    - sentence-transformers
    - faiss-cpu (или faiss-gpu)
    - numpy
    """
    
    def __init__(self, base_path: str = None, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Инициализация векторизатора знаний.
        
        Args:
            base_path: Путь к директории с данными. По умолчанию используется
                      директория data внутри пакета knowledge_base.
            model_name: Название модели для sentence-transformers.
        """
        if base_path is None:
            self.base_path = Path(__file__).parent / 'data'
        else:
            self.base_path = Path(base_path)
        
        self.model_name = model_name
        self.model = None
        self.index = None
        self.index_to_data = {}
        
        logger.info(f"Инициализирован векторизатор знаний с базовым путём: {self.base_path}")
    
    def _load_dependencies(self):
        """
        Загрузка зависимостей для векторизации.
        Этот метод загружает необходимые библиотеки только при необходимости,
        чтобы избежать загрузки тяжелых зависимостей при инициализации.
        
        Raises:
            ImportError: Если необходимые зависимости не установлены.
        """
        try:
            import numpy as np
            from sentence_transformers import SentenceTransformer
            import faiss
            
            self.np = np
            self.faiss = faiss
            
            # Загружаем модель, если она еще не загружена
            if self.model is None:
                logger.info(f"Загрузка модели {self.model_name}...")
                self.model = SentenceTransformer(self.model_name)
                logger.info("Модель успешно загружена")
                
        except ImportError as e:
            logger.error(f"Ошибка загрузки зависимостей: {e}")
            logger.error("Убедитесь, что установлены пакеты: sentence-transformers, faiss-cpu, numpy")
            raise ImportError("Не удалось загрузить необходимые зависимости для векторизации") from e
    
    def _extract_text_from_data(self, data: Dict[str, Any]) -> str:
        """
        Извлечение текста из данных для векторизации.
        
        Args:
            data: Данные элемента.
            
        Returns:
            Текст для векторизации.
        """
        texts = []
        
        # Добавляем заголовок с большим весом (дублируем)
        if 'title' in data:
            texts.append(str(data['title']) * 3)
        
        # Добавляем описание
        if 'description' in data:
            texts.append(str(data['description']))
        
        # Добавляем другие текстовые поля
        for key, value in data.items():
            if key not in ['title', 'description'] and not key.startswith('_'):
                if isinstance(value, str):
                    texts.append(f"{key}: {value}")
                elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                    texts.append(f"{key}: {', '.join(value)}")
        
        return " ".join(texts)
    
    def build_index(self, categories: List[str] = None):
        """
        Построение индекса для векторного поиска.
        
        Args:
            categories: Список категорий для индексации. Если None, индексируются все категории.
        """
        self._load_dependencies()
        
        logger.info("Начало построения индекса...")
        
        if not categories:
            # Индексация всех категорий
            categories = [d.name for d in self.base_path.iterdir() 
                         if d.is_dir() and not d.name.startswith('__')]
        
        all_texts = []
        self.index_to_data = {}
        index = 0
        
        for category in categories:
            category_path = self.base_path / category
            
            if not category_path.exists():
                logger.warning(f"Категория '{category}' не найдена.")
                continue
            
            # Обработка всех JSON файлов в категории
            for file_path in category_path.glob('*.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Извлекаем текст для векторизации
                        text = self._extract_text_from_data(data)
                        
                        if text:
                            all_texts.append(text)
                            
                            # Добавляем метаданные для результата
                            data['_category'] = category
                            data['_id'] = file_path.stem
                            self.index_to_data[index] = data
                            index += 1
                except Exception as e:
                    logger.error(f"Ошибка при индексации файла {file_path}: {e}")
        
        if not all_texts:
            logger.warning("Нет данных для индексации.")
            return
        
        # Векторизация текстов
        logger.info(f"Векторизация {len(all_texts)} элементов...")
        embeddings = self.model.encode(all_texts, show_progress_bar=True)
        
        # Создание FAISS индекса
        dimension = embeddings.shape[1]
        self.index = self.faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        logger.info(f"Индекс успешно построен с {self.index.ntotal} элементами")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Семантический поиск по запросу.
        
        Args:
            query: Поисковый запрос.
            top_k: Количество результатов для возврата.
            
        Returns:
            Список найденных элементов, отсортированных по релевантности.
        """
        if self.index is None or not self.index_to_data:
            logger.warning("Индекс не построен. Запуск построения индекса...")
            self.build_index()
            
            if self.index is None or not self.index_to_data:
                logger.error("Не удалось построить индекс")
                return []
        
        # Векторизация запроса
        query_vector = self.model.encode([query])
        
        # Поиск ближайших соседей
        distances, indices = self.index.search(query_vector, top_k)
        
        # Формирование результатов
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.index_to_data):
                continue
            
            data = self.index_to_data[idx].copy()
            # Добавляем оценку релевантности
            data['_score'] = float(1.0 / (1.0 + distances[0][i]))
            results.append(data)
        
        return results 