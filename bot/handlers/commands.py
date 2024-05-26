from asyncio import sleep
from loguru import logger
import pandas as pd
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from bot.controllers.blocked_user import is_user_blocked
from bot.controllers.promo import get_user_promos, get_all_promos
from bot.controllers.user import delete_all_data, get_user, user_exists
from bot.markups.inline_markups import create_promo_keyboard, create_registration_keyboard
from bot.misc import bot
from bot.states import BlockStates
from bot.texts import *
from bot.utils import save_to_excel
from config import ADMIN_USERNAME, ADMINS

command_router = Router()


@command_router.message(CommandStart())
async def start_command(message: Message):
    user = await get_user(message.from_user.id)
    if user and await is_user_blocked(user.phone_number):
        return
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    if not await user_exists(message.from_user.id):
        await message.reply(text=START_TEXT, reply_markup=create_registration_keyboard())
    else:
        user = await get_user(message.from_user.id)
        await message.answer(WELCOME_TEXT.format(message.from_user.id, user.name), reply_markup=ReplyKeyboardRemove())
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await message.answer(FOR_ENTER_PROMO_TEXT, reply_markup=create_promo_keyboard())


@command_router.message(Command('mypromos'))
async def list_command(message: Message):
    user = await get_user(message.from_user.id)
    if user and await is_user_blocked(user.phone_number):
        return
    user_promos = await get_user_promos(message.from_user.id)
    count = len(user_promos)
    if count:
        text = USER_PROMOS_COUNT_TEXT.format(count)
        for promo in user_promos:
            text += PROMO_TEXT.format(promo.special_code, promo.code)
        return await message.answer(text)
    await message.answer(NO_PROMOS_TEXT)


@command_router.message(Command('help'))
async def help_command(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer(HELP_COMMAND_TEXT.format(ADMIN_USERNAME))


@command_router.message(Command('export'))
async def export_command(message: Message):
    if message.from_user.id not in ADMINS:
        return
    try:
        promos = await get_all_promos()
        if promos:
            msg1 = await message.answer('⏳')
            await bot.send_chat_action(message.chat.id, 'typing')
            await sleep(0.2)
            msg2 = await message.answer(GETTING_READY_TEXT)
            df = pd.DataFrame(promos)
            excel_file_name = 'data.xlsx'
            await save_to_excel(df, excel_file_name)
            await bot.send_chat_action(message.chat.id, 'upload_document')
            await msg1.delete()
            await msg2.delete()
            await message.answer_document(FSInputFile(excel_file_name))
        else:
            await bot.send_chat_action(message.chat.id, 'typing')
            await sleep(0.2)
            await message.answer(NO_DATA_TEXT)
    except Exception as e:
        # Handle any exceptions here, log them, and potentially notify the user of an error.
        logger.error(f"Error occurred while exporting data: {e}")


@command_router.message(Command('block'))
async def block_command(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer(ASK_BLOCK_USER_PHONE_NUMBER_TEXT)
    await state.set_state(BlockStates.phone)


@command_router.message(Command('deldata'))
async def delete_data_command(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await delete_all_data()
        await message.answer('✅')
    except Exception as e:
        # Handle any exceptions here, log them, and potentially notify the user of an error.
        logger.error(f"Error occurred while deleting data: {e}")
