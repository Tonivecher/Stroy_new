"""
Модуль для загрузки и обработки данных базы знаний.
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Настройка логирования
logger = logging.getLogger(__name__)

class KnowledgeLoader:
    """Загрузчик данных для базы знаний."""
    
    def __init__(self, base_path: str = None):
        """
        Инициализация загрузчика базы знаний.
        
        Args:
            base_path: Путь к директории с данными. По умолчанию используется
                      директория data внутри пакета knowledge_base.
        """
        if base_path is None:
            self.base_path = Path(__file__).parent / 'data'
        else:
            self.base_path = Path(base_path)
        
        logger.info(f"Инициализирован загрузчик знаний с базовым путём: {self.base_path}")
        
    def get_categories(self) -> List[str]:
        """
        Получение списка категорий базы знаний.
        
        Returns:
            Список названий категорий.
        """
        try:
            return [d.name for d in self.base_path.iterdir() 
                   if d.is_dir() and not d.name.startswith('__')]
        except Exception as e:
            logger.error(f"Ошибка при получении списка категорий: {e}")
            return []
    
    def load_category(self, category: str) -> Dict[str, Any]:
        """
        Загрузка данных для указанной категории.
        
        Args:
            category: Название категории.
            
        Returns:
            Словарь с данными категории.
            
        Raises:
            FileNotFoundError: Если категория не найдена.
        """
        category_path = self.base_path / category
        
        if not category_path.exists():
            logger.error(f"Категория '{category}' не найдена.")
            raise FileNotFoundError(f"Категория '{category}' не найдена.")
        
        result = {}
        
        # Загрузка всех JSON файлов в категории
        for file_path in category_path.glob('*.json'):
            try:
                if file_path.stat().st_size == 0:
                    logger.error(f"Файл {file_path} пуст.")
                    continue
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip():
                        logger.error(f"Файл {file_path} содержит только пробельные символы.")
                        continue
                        
                    data = json.loads(content)
                    result[file_path.stem] = data
                    logger.debug(f"Загружен файл: {file_path}")
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка формата JSON в файле {file_path}: {e}")
            except Exception as e:
                logger.error(f"Ошибка при загрузке файла {file_path}: {e}")
        
        return result
    
    def load_item(self, category: str, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Загрузка конкретного элемента знаний.
        
        Args:
            category: Название категории.
            item_id: Идентификатор элемента (имя файла без расширения).
            
        Returns:
            Данные элемента или None, если элемент не найден.
        """
        file_path = self.base_path / category / f"{item_id}.json"
        
        if not file_path.exists():
            logger.warning(f"Элемент '{item_id}' в категории '{category}' не найден.")
            return None
        
        try:
            if file_path.stat().st_size == 0:
                logger.error(f"Файл {file_path} пуст.")
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    logger.error(f"Файл {file_path} содержит только пробельные символы.")
                    return None
                    
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка формата JSON в файле {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка при загрузке элемента {item_id}: {e}")
            return None
    
    def save_item(self, category: str, item_id: str, data: Dict[str, Any]) -> bool:
        """
        Сохранение элемента в базу знаний.
        
        Args:
            category: Название категории.
            item_id: Идентификатор элемента.
            data: Данные для сохранения.
            
        Returns:
            True в случае успешного сохранения, иначе False.
        """
        category_path = self.base_path / category
        
        # Создаем директорию категории, если она не существует
        os.makedirs(category_path, exist_ok=True)
        
        file_path = category_path / f"{item_id}.json"
        
        try:
            # Проверка данных перед сохранением
            if not data:
                logger.error(f"Попытка сохранить пустые данные для элемента {item_id}")
                return False
                
            # Проверяем, можно ли сериализовать данные в JSON
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            logger.info(f"Элемент '{item_id}' успешно сохранен в категории '{category}'")
            return True
        except TypeError as e:
            logger.error(f"Ошибка сериализации данных для элемента {item_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при сохранении элемента {item_id}: {e}")
            return False 