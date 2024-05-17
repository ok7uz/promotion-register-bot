import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand
from aiogram.fsm.context import FSMContext

from config import *
from db import Database
from keyboards import contact_kb, reg_kb
from states import RegistrationStates

db = Database(DB_NAME)

command_router = Router()
registration_router = Router()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
        # BotCommand(command="/help", description="Get help information"),
    ]
    await bot.set_my_commands(commands)


@command_router.message(CommandStart())
async def start(message: Message):
    user = db.get_user(message.from_user.id)
    if not user:
        db.add_user(message.from_user.id)
    if not user or None in user:
        await message.reply(text=START_TEXT, reply_markup=reg_kb)
    else:
        formatted_message = WELCOME_TEXT.format(user[1])
        await message.reply(text=formatted_message, parse_mode=ParseMode.HTML)


@registration_router.message(F.text == SIGN_UP_TEXT)
async def register_start(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if user and None not in user:
        await message.reply(SIGNED_UP_TEXT.format(user[1]), reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(ENTER_NAME_TEXT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.regName)


@registration_router.message(RegistrationStates.regName)
async def register_name(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(ENTER_PHONE_NUMBER_TEXT, reply_markup=contact_kb)
    await state.set_state(RegistrationStates.regPhone)


@registration_router.message(RegistrationStates.regPhone)
async def register_phone_number(message: types.Message, state: FSMContext):
    user_phone_number = message.contact.phone_number
    await state.update_data(phone_number=user_phone_number)
    await message.answer(ENTER_ADDRESS_TEXT)
    await state.set_state(RegistrationStates.regAddress)


@registration_router.message(RegistrationStates.regAddress)
async def register_address(message: types.Message, state: FSMContext):
    user_address = message.text
    await state.update_data(address=user_address)
    await message.answer(ENTER_PROMO_PHOTO_TEXT)
    await state.set_state(RegistrationStates.regPhoto)


@registration_router.message(RegistrationStates.regPhoto)
async def register_promo_photo(message: types.Message, state: FSMContext):
    photo = message.photo
    user_id = message.from_user.id
    if not photo:
        await message.answer(ENTER_PHOTO_TEXT)
        return await state.set_state(RegistrationStates.regPhoto)
    file_id = message.photo[-1].file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await message.bot.download_file(file_path)
    with open(f"{user_id}.jpg", "wb") as new_file:
        new_file.write(downloaded_file.read())
    await message.reply(PHOTO_SAVED_TEXT)
    await message.answer(ENTER_PROMO_CODE_TEXT)
    await state.set_state(RegistrationStates.regPromoCode)


@registration_router.message(RegistrationStates.regPromoCode)
async def register_promo_code(message: types.Message, state: FSMContext):
    promo_code = message.text
    await state.update_data(promo_code=promo_code)
    await message.answer(DATA_SAVED_TEXT)
    user_data = await state.get_data()
    db.update_user(**user_data, id=message.from_user.id)
    await message.answer(INFO_TEXT.format(
        user_data.get('name'),
        user_data.get('phone_number'),
        user_data.get('address'),
        user_data.get('promo_code')
    ))


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    await set_commands(bot)
    dp.include_routers(command_router, registration_router)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("An error occurred while polling for updates:", e)
        await asyncio.sleep(5)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
