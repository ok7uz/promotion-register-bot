import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

ROOT_DIR: Path = Path(__file__).parent.parent

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())
