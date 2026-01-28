"""
Configuration module - loads settings from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Google Sheets settings
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME', 'Absences')

# Resolve credentials path relative to project root
_credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './credentials.json')
_project_root = Path(__file__).parent.parent
if not os.path.isabs(_credentials_path):
    GOOGLE_APPLICATION_CREDENTIALS = str(_project_root / _credentials_path)
else:
    GOOGLE_APPLICATION_CREDENTIALS = _credentials_path

# Timezone
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Moscow')

# Validate required settings
def validate_config():
    """Check that all required environment variables are set."""
    required = {
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'CHAT_ID': CHAT_ID,
        'SPREADSHEET_ID': SPREADSHEET_ID,
        'GOOGLE_APPLICATION_CREDENTIALS': GOOGLE_APPLICATION_CREDENTIALS,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return True
