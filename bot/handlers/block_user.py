from asyncio import sleep
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger
from bot.controllers.blocked_user import create_blocked_user
from bot.controllers.promo import delete_user_promos
from bot.misc import bot
from bot.states import BlockStates
from bot.texts import USER_BLOCKED_TEXT

router = Router()


@router.message(BlockStates.phone)
async def get_blocking_phone_number(message: Message, state: FSMContext):
    """
    Handle the process of blocking a user based on the provided phone number.

    Args:
        message (Message): The message object containing the phone number.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        phone_number = message.text.strip().replace(' ', '')
        phone_number = '+' + phone_number if not phone_number.startswith('+') else phone_number
        await create_blocked_user(phone_number)
        await delete_user_promos(phone_number)
        await message.answer(USER_BLOCKED_TEXT.format(phone_number))
        await state.clear()
    except Exception as e:
        # Handle any exceptions here, log them, and potentially notify the user of an error.
        # For example:
        # await message.answer("An error occurred while processing your request. Please try again later.")
        logger.error(f"Error occurred while blocking user: {e}")
