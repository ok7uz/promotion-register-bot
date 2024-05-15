from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, Contact
import re

from aiogram.utils.formatting import Text

from config import DB_NAME
from db import Database
from keyboards import contact_kb
from states import RegistrationStates

registration_router = Router()
db = Database(DB_NAME)


@registration_router.message(F.text == "👤 Ro'yxatdan o'tish")
async def register_start(message: types.Message, state: RegistrationStates):
    user = db.get_user(message.from_user.id)
    if user and None not in user:
        await message.reply(
            f"Hurmatli {user[1]}, siz ro'yxatdan o'tgansiz",
            reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(
            "Ismingizni kiriting:",
            reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.regName)


@registration_router.message(RegistrationStates.regName)
async def register_name(message: types.Message, state: RegistrationStates):
    await state.update_data(name=message.text)
    await message.answer(
        "Iltimos telefon raqamingizni yuboring",
        reply_markup=contact_kb
    )
    await state.set_state(RegistrationStates.regPhone)


@registration_router.message(RegistrationStates.regPhone)
async def register_phone(message: types.Message, state: RegistrationStates):
    reg_phone = message.contact.phone_number
    await state.update_data(reg_phone=reg_phone)
    await message.answer("Manzilingiz:")
    await state.set_state(RegistrationStates.regAddress)


@registration_router.message(RegistrationStates.regAddress)
async def register_address(message: types.Message, state: RegistrationStates):
    reg_address = message.text
    await state.update_data(reg_address=reg_address)
    user_data = await state.get_data()
    user_id = message.from_user.id
    db.update_user(user_id, user_data['name'], user_data['reg_phone'], user_data['reg_address'])
    await message.answer(f"Ma'lumotlar saqlandi!\n\n<b>Ism:</b> {user_data['name']}\n<b>Telefon raqam:</b> {user_data['reg_phone']}\n<b>Manzil:</b> {user_data['reg_address']}", reply_markup=ReplyKeyboardRemove())
    await state.finish()