import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./english_reading.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

FREE_DAILY_LIMIT = 3
TEXT_MAX_WORDS = 5000
TEXT_SPLIT_WORDS = 3000
POLL_INTERVAL = 2

TIMEOUT_SHORT = 20
TIMEOUT_MEDIUM = 40
TIMEOUT_LONG = 60

CACHE_PREFIX = "hf_cache:"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
