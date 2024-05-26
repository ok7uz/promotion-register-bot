import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

ROOT_DIR: Path = Path(__file__).resolve().parent.parent

try:
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
except Exception as e:
    raise   
