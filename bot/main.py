from handlers import my_router
import asyncio
import logging
import sys
from os import getenv

from middleware.middleware import DbMiddleware
from dotenv import load_dotenv
from pathlib import Path
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.database import Database

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = getenv("BOT_TOKEN")

db = Database("postgresql+asyncpg://ecommerce_user:htmlpagelev@localhost:5432/ecommerce_db") 
dp = Dispatcher()
dp.message.middleware(DbMiddleware(db))  
dp.include_router(my_router)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())