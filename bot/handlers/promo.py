from asyncio import sleep

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.controllers.promo import create_promo, promo_exists
from bot.markups.inline_markups import channels_kb
from bot.markups.reply_markups import promo_kb
from bot.misc import bot
from bot.states import PromoStates
from bot.texts import *

promo_router = Router()


@promo_router.message(PromoStates.photo)
async def register_promo_photo(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    photo = message.photo
    if not photo:
        await message.answer(ENTER_PHOTO_TEXT)
        return await state.set_state(PromoStates.photo)
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await message.reply(PHOTO_SAVED_TEXT)
    await message.answer(ENTER_PROMO_CODE_TEXT)
    await state.set_state(PromoStates.promoCode)


@promo_router.message(PromoStates.promoCode)
async def register_promo_code(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    promo_code = message.text
    await state.update_data(code=promo_code)
    promo_data = await state.get_data()
    promo_code_exists = await promo_exists(promo_code)

    if not promo_code_exists:
        new_promo = await create_promo(user_id=message.from_user.id, **promo_data)
        await message.answer(PROMO_SAVED_TEXT)
        await message.answer(SPECIAL_CODE_TEXT.format(new_promo.special_code), reply_markup=promo_kb())
        await message.answer(CHANNELS_TEXT, reply_markup=channels_kb())
        return await state.clear()
    await message.answer(PROMO_HAS_BEEN_USED, reply_markup=promo_kb())
  