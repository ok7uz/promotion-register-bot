from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from asyncio import sleep

from bot.controllers.user import create_user, user_exists
from bot.misc import bot
from bot.states import RegistrationStates
from bot.texts import *
from bot.markups.inline_markups import promo_kb, register_callback_data
from bot.markups.reply_markups import contact_kb

registration_router = Router()



@registration_router.callback_query(lambda query: query.data == register_callback_data)
async def register_user(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    await message.delete()
    if await user_exists(callback_query.from_user.id):
        await message.answer(SIGNED_UP_TEXT.format(callback_query.from_user.full_name), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(ENTER_NAME_TEXT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.name)


@registration_router.message(RegistrationStates.name)
async def register_name(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(ENTER_PHONE_NUMBER_TEXT, reply_markup=contact_kb())
    await state.set_state(RegistrationStates.phone)


@registration_router.message(RegistrationStates.phone)
async def register_phone_number(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    user_phone_number = message.contact.phone_number
    user_phone_number = '+' + user_phone_number if not user_phone_number.startswith('+') else user_phone_number
    await state.update_data(phone_number=user_phone_number)
    await message.answer(ENTER_ADDRESS_TEXT, reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.address)


@registration_router.message(RegistrationStates.address)
async def register_address(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    user_address = message.text
    await state.update_data(address=user_address)
    user_data = await state.get_data()
    await create_user(**user_data, user_id=message.from_user.id)
    await message.answer(INFO_TEXT.format(
        user_data.get('name'),
        user_data.get('phone_number'),
        user_data.get('address'),
    ))
    await message.answer(FOR_ENTER_PROMO_TEXT, reply_markup=promo_kb())
    await state.clear()
