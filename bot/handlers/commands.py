from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.controllers.user import get_all_users, get_user, user_exists
from bot.markups.reply_markups import register_kb
from bot.texts import INFO_TEXT, START_TEXT, USERS_COUNT_TEXT, WELCOME_TEXT

command_router = Router()


@command_router.message(CommandStart())
async def start(message: Message):
    if not await user_exists(message.from_user.id):
        await message.reply(text=START_TEXT, reply_markup=register_kb())
    else:
        user = await get_user(message.from_user.id)
        formatted_message = WELCOME_TEXT.format(message.from_user.id, user.name)
        await message.reply(text=formatted_message)


@command_router.message(Command('list'))
async def start(message: Message):
    users = await get_all_users()
    await message.answer(USERS_COUNT_TEXT.format(len(users)))
    for user in users:
        await message.answer_photo(user.file_id, caption=INFO_TEXT.format(user.name, user.phone_number, user.address, user.promo_code))
