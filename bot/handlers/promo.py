from asyncio import sleep
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.controllers.blocked_user import is_user_blocked
from bot.controllers.code import code_exists
from bot.controllers.promo import create_promo, promo_exists
from bot.controllers.user import get_user, user_exists
from bot.markups.inline_markups import (
    create_registration_keyboard, create_promo_keyboard, 
    create_channels_keyboard, promo_callback_data
)
from bot.misc import bot
from bot.states import PromoStates
from bot.texts import *
from config import ADMIN_USERNAME

promo_router = Router()


@promo_router.callback_query(lambda query: query.data == promo_callback_data)
async def enter_promo(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle the callback query to enter a promo.

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
        await message.answer(ENTER_PROMO_PHOTO_TEXT)
        await state.set_state(PromoStates.photo)
    else:
        await message.answer(text=START_TEXT, reply_markup=create_registration_keyboard())


@promo_router.message(PromoStates.photo)
async def register_promo_photo(message: Message, state: FSMContext):
    """
    Register promo photo.

    Args:
        message (Message): The message object.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    photo = message.photo
    if not photo:
        await message.answer(ENTER_PHOTO_TEXT)
        return await state.set_state(PromoStates.photo)
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await message.reply(PHOTO_SAVED_TEXT)
    await message.answer(ENTER_PROMO_CODE_TEXT)
    await state.set_state(PromoStates.promo_code)


@promo_router.message(PromoStates.promo_code)
async def register_promo_code(message: Message, state: FSMContext):
    """
    Register promo code.

    Args:
        message (Message): The message object.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    promo_code = message.text
    await state.update_data(code=promo_code)
    promo_data = await state.get_data()
    promo_code_exists = await promo_exists(promo_code)
    is_code_valid = await code_exists(promo_code)
    print(is_code_valid)

    if not is_code_valid:
        bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await message.answer(CODE_NOT_FOUND_TEXT, reply_markup=create_promo_keyboard())
        return await state.clear()
    elif not promo_code_exists:
        new_promo = await create_promo(user_id=message.from_user.id, **promo_data)
        await message.answer(PROMO_SAVED_TEXT)
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await message.answer(SPECIAL_CODE_TEXT.format(new_promo.special_code))
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await message.answer(CHANNELS_TEXT, reply_markup=create_channels_keyboard())
        return await state.clear()
    await message.answer(PROMO_HAS_BEEN_USED.format(ADMIN_USERNAME), reply_markup=create_promo_keyboard())
