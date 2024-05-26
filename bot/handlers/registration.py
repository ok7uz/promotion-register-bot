from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from asyncio import sleep

from bot.controllers.blocked_user import is_user_blocked
from bot.controllers.user import create_user, get_user, user_exists
from bot.misc import bot
from bot.states import RegistrationStates
from bot.texts import *
from bot.markups.inline_markups import register_callback_data, create_promo_keyboard
from bot.markups.reply_markups import create_contact_keyboard

registration_router = Router()


@registration_router.callback_query(lambda query: query.data == register_callback_data)
async def register_user(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle callback query to register user.

    Args:
        callback_query (CallbackQuery): The callback query.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    message = callback_query.message
    user = await get_user(message.from_user.id)
    if user and await is_user_blocked(user.phone_number):
        return
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.delete()
    if await user_exists(callback_query.from_user.id):
        await message.answer(SIGNED_UP_TEXT.format(callback_query.from_user.full_name), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(ENTER_NAME_TEXT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.name)


@registration_router.message(RegistrationStates.name)
async def register_name(message: Message, state: FSMContext):
    """
    Register user's name.

    Args:
        message (Message): The message object.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(ENTER_PHONE_NUMBER_TEXT, reply_markup=create_contact_keyboard())
    await state.set_state(RegistrationStates.phone)


@registration_router.message(RegistrationStates.phone)
async def register_phone_number(message: Message, state: FSMContext):
    """
    Register user's phone number.

    Args:
        message (Message): The message object.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    user_phone_number = message.contact.phone_number
    user_phone_number = '+' + user_phone_number if not user_phone_number.startswith('+') else user_phone_number
    await state.update_data(phone_number=user_phone_number)
    await message.answer(ENTER_ADDRESS_TEXT, reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.address)


@registration_router.message(RegistrationStates.address)
async def register_address(message: Message, state: FSMContext):
    """
    Register user's address.

    Args:
        message (Message): The message object.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    user_address = message.text
    await state.update_data(address=user_address)
    user_data = await state.get_data()
    await create_user(**user_data, user_id=message.from_user.id)
    await message.answer(INFO_TEXT.format(
        user_data.get('name'),
        user_data.get('phone_number'),
        user_data.get('address'),
    ))
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer(FOR_ENTER_PROMO_TEXT, reply_markup=create_promo_keyboard())
    await state.clear()
