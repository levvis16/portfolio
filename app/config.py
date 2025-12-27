import os
from pathlib import Path
from dotenv import load_dotenv

# Определяем путь к .env (на уровень выше app/)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # ← явно указываем путь

SECRET_KEY = "b4c09517c62a39dc2df795800dfd09d5450fb73b8bc8f35a11cd79835ab5fc00"
ALGORITHM = "HS256"

# Для отладки
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не загружен. Проверь .env файл")

