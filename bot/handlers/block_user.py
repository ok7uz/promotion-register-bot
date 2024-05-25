from asyncio import sleep

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.controllers.blocked_user import create_blocked_user
from bot.controllers.promo import delete_user_promos
from bot.misc import bot
from bot.states import PromoStates, BlockStates
from bot.texts import *

router = Router()


@router.message(BlockStates.phone)
async def get_blocking_phone_number(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    phone_number = message.text
    phone_number = phone_number.replace(' ', '')
    phone_number = '+' + phone_number if not phone_number.startswith('+') else phone_number
    await create_blocked_user(phone_number)
    await delete_user_promos(phone_number)
    await message.answer("block qilindi va barcha promo kodlari o'chirildi")
    await state.clear()
