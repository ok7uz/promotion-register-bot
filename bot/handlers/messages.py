from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.controllers.user import user_exists
from bot.markups.reply_markups import register_kb
from bot.states import RegistrationStates, PromoStates
from bot.texts import *

message_router = Router()


@message_router.message(F.text == SIGN_UP_TEXT)
async def register_start(message: Message, state: FSMContext):
    if await user_exists(message.from_user.id):
        await message.reply(SIGNED_UP_TEXT.format(), reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(ENTER_NAME_TEXT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.name)


@message_router.message(F.text == ENTER_PROMO_TEXT)
async def enter_promo(message: Message, state: FSMContext):
    if await user_exists(message.from_user.id):
        await message.answer(ENTER_PROMO_PHOTO_TEXT)
        await state.set_state(PromoStates.photo)
    else:
        await message.reply(text=START_TEXT, reply_markup=register_kb())
