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
RAILWAY_PUBLIC_DOMAIN = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')

# Get the base URL from available environment variables
if RAILWAY_STATIC_URL:
    base_url = RAILWAY_STATIC_URL
elif RAILWAY_PUBLIC_DOMAIN:
    base_url = f"https://{RAILWAY_PUBLIC_DOMAIN}"
else:
    # If no URL is available, use polling mode
    base_url = None

# Configure webhook URL if base URL is available
if base_url:
    # Ensure URL ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'
    WEBHOOK_URL = urljoin(base_url, WEBHOOK_PATH.lstrip('/'))
else:
    WEBHOOK_URL = None

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