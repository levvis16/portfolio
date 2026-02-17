from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise ValueError("SECRET_KEY не загружен. Проверь .env файл")

