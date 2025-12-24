import os
from pathlib import Path
from dotenv import load_dotenv

# Определяем путь к .env (на уровень выше app/)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # ← явно указываем путь

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Для отладки
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не загружен. Проверь .env файл")