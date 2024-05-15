import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from config import BOT_TOKEN, DB_NAME
from db import Database
from keyboards import contact_kb, reg_kb
from states import RegistrationStates



db = Database(DB_NAME)


command_router = Router()
registration_router = Router()


@command_router.message(CommandStart())
async def start(message: Message):
    user = db.get_user(message.from_user.id)
    print(db.all_users(), user, message.from_user.id)
    if not user:
        db.add_user(message.from_user.id)
    if not user or None in user:
        await message.reply(text="Assalomu alaykum. Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak.",
                            reply_markup=reg_kb)
    else:
        formatted_message = f"Assalomu alaykum  {user[1]}!"
        await message.reply(text=formatted_message, parse_mode=ParseMode.HTML)


@command_router.message(Command('help'))
async def cmd_code(message: Message):
    user = db.get_users(message.from_user.id)
    if user:
        s = f"Salom @{user[4]} men sizga yordam beraman"
        await message.reply(s)


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
    # await state.finish_state()


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()  
    dp.include_routers(command_router, registration_router)
    await dp.start_polling(bot)  

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
