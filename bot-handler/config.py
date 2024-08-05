from dotenv import load_dotenv
import os

load_dotenv("../.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
DB_PORT = int(os.getenv("DB_PORT", '5432'))
DB_NAME = os.getenv("DB_NAME", "notifications_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD", "PaSSword")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
