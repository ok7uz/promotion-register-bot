from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from config import BOT_TOKEN

ROOT_DIR: Path = Path(__file__).resolve().parent.parent

try:
    local_server = TelegramAPIServer.from_base('http://localhost:8081')
    session = AiohttpSession(api=local_server)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'), session=session)
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
except Exception as e:
    raise   
