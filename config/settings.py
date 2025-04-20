import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Webhook settings
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = os.getenv('RAILWAY_STATIC_URL', '') + WEBHOOK_PATH

# Material categories
MATERIAL_CATEGORIES = {
    'wall': 'Стены',
    'ceiling': 'Потолок',
    'floor': 'Пол',
    'door': 'Двери',
    'window': 'Окна'
}

# Work types
WORK_TYPES = {
    "dismantling": "Демонтаж",
    "preparation": "Подготовка",
    "installation": "Монтаж",
    "finishing": "Отделка"
} 