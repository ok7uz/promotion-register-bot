from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.controllers.user import create_user
from bot.markups.reply_markups import contact_kb
from bot.states import RegistrationStates
from bot.texts import *

registration_router = Router()


@registration_router.message(RegistrationStates.name)
async def register_name(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(ENTER_PHONE_NUMBER_TEXT, reply_markup=contact_kb())
    await state.set_state(RegistrationStates.phone)


@registration_router.message(RegistrationStates.phone)
async def register_phone_number(message: Message, state: FSMContext):
    user_phone_number = message.contact.phone_number
    await state.update_data(phone_number=user_phone_number)
    await message.answer(ENTER_ADDRESS_TEXT, reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.address)


@registration_router.message(RegistrationStates.address)
async def register_address(message: Message, state: FSMContext):
    user_address = message.text
    await state.update_data(address=user_address)
    await message.answer(ENTER_PROMO_PHOTO_TEXT)
    await state.set_state(RegistrationStates.photo)


@registration_router.message(RegistrationStates.photo)
async def register_promo_photo(message: Message, state: FSMContext):
    photo = message.photo
    if not photo:
        await message.answer(ENTER_PHOTO_TEXT)
        return await state.set_state(RegistrationStates.photo)
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await message.reply(PHOTO_SAVED_TEXT)
    await message.answer(ENTER_PROMO_CODE_TEXT)
    await state.set_state(RegistrationStates.promoCode)


@registration_router.message(RegistrationStates.promoCode)
async def register_promo_code(message: Message, state: FSMContext):
    promo_code = message.text
    await state.update_data(promo_code=promo_code)
    await message.answer(DATA_SAVED_TEXT)
    user_data = await state.get_data()
    new_user = await create_user(**user_data, user_id=message.from_user.id)
    await message.answer(INFO_TEXT.format(
        user_data.get('name'),
        user_data.get('phone_number'),
        user_data.get('address'),
        user_data.get('promo_code')
    ))
    await message.answer(SPECIAL_CODE_TEXT.format(new_user.special_code))
    await state.clear()
