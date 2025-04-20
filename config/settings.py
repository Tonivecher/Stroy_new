import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Material categories
MATERIAL_CATEGORIES = [
    "🏠 Стены",
    "🏠 Пол",
    "🏠 Потолок",
    "🚽 Сантехника",
    "💡 Электрика",
    "🚪 Двери",
    "🪟 Окна",
    "🔨 Инструменты",
    "📦 Прочее"
]

# Work types
WORK_TYPES = {
    "dismantling": "Демонтаж",
    "preparation": "Подготовка",
    "installation": "Монтаж",
    "finishing": "Отделка"
} 