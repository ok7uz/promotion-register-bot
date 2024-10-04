from asyncio import sleep

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.controllers.user import get_all_users
from bot.misc import bot
from bot.states import MessageStates

message_router = Router()


@message_router.message(MessageStates.get_message)
async def register_promo_photo(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)

    users = await get_all_users()
    count = 0


    for user in users:
        try:
            await message.send_copy(user.id)
            count += 1
        except:
            pass

    await message.answer(f'Xabar <b>{count}</b> ta foydalanuvchilarga yuborildi')
    await state.clear()
