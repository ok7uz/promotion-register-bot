from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message, user
from aiogram.filters import CommandStart, Command

from db import Database
from keyboards import reg_kb
from config import DB_NAME

db = Database(DB_NAME)


command_router = Router()


@command_router.message(CommandStart())
async def start(message: Message):
    user = db.get_user(message.from_user.id)
    print(db.all_users())
    if not user or None in user:
        db.add_user(message.from_user.id)
        await message.reply(text="Assalomu alaykum. Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak.",
                            reply_markup=reg_kb)
    else:
        formatted_message = f"Assalomu alaykum  {user[1]}!"
        await message.reply(text=formatted_message, parse_mode=ParseMode.HTML)


@command_router.message(Command('help'))
async def cmd_code(message: Message):
    user = db.get_users(message.from_user.id)
    if user:
        s = f"Salom @{user[4]} men sizga yordam beraman"
        await message.reply(s)


@command_router.message(Command('code'))
async def cmd_code(message: Message):
    code_snippet = "```python\nprint('hello world')\n```"
    await message.answer(code_snippet, parse_mode=ParseMode.MARKDOWN_V2)
