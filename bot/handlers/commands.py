from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.controllers.promo import get_user_promos
from bot.controllers.user import get_all_users, get_user, user_exists
from bot.markups.reply_markups import register_kb, promo_kb
from bot.texts import *

command_router = Router()


@command_router.message(CommandStart())
async def start_command(message: Message):
    if not await user_exists(message.from_user.id):
        await message.reply(text=START_TEXT, reply_markup=register_kb())
    else:
        user = await get_user(message.from_user.id)
        await message.answer(WELCOME_TEXT.format(message.from_user.id, user.name))
        await message.answer(FOR_ENTER_PROMO_TEXT, reply_markup=promo_kb())


@command_router.message(Command('mypromos'))
async def list_command(message: Message):
    user_promos = await get_user_promos(message.from_user.id)
    count = len(user_promos)

    if count:
        text = USER_PROMOS_COUNT_TEXT.format(count)
        for promo in user_promos:
            text += PROMO_TEXT.format(promo.special_code, promo.code)
        return await message.answer(text)
    await message.answer(NO_PROMOS_TEXT)
