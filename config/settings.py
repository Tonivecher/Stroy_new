import os
from dotenv import load_dotenv
from urllib.parse import urljoin

# Load environment variables
load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Webhook settings
WEBHOOK_PATH = '/webhook'
RAILWAY_STATIC_URL = os.getenv('RAILWAY_STATIC_URL', '')
if not RAILWAY_STATIC_URL:
    raise ValueError("RAILWAY_STATIC_URL environment variable is not set")

# Ensure URL ends with a slash
if not RAILWAY_STATIC_URL.endswith('/'):
    RAILWAY_STATIC_URL += '/'

WEBHOOK_URL = urljoin(RAILWAY_STATIC_URL, WEBHOOK_PATH.lstrip('/'))

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