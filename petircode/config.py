"""
Configuration management for PetriCode bot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Bot configuration"""

    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

    # Webhook settings
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))

    # Admin users
    ADMIN_USER_IDS = [
        int(uid.strip())
        for uid in os.getenv('ADMIN_USER_IDS', '').split(',')
        if uid.strip()
    ]

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        return True


config = Config()
