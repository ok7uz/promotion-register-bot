from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.controllers.user import user_exists
from bot.states import RegistrationStates
from bot.texts import ENTER_NAME_TEXT, SIGN_UP_TEXT, SIGNED_UP_TEXT

message_router = Router()


@message_router.message(F.text == SIGN_UP_TEXT)
async def register_start(message: Message, state: FSMContext):
    if await user_exists(message.from_user.id):
        await message.reply(SIGNED_UP_TEXT.format(), reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(ENTER_NAME_TEXT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.name)
