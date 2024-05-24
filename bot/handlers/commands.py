from asyncio import sleep

import pandas as pd
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, chat_permissions
from aiogram.filters import CommandStart, Command

from bot.controllers.promo import get_user_promos, get_all_promos
from bot.controllers.user import get_user, user_exists
from bot.markups.reply_markups import register_kb, promo_kb
from bot.misc import bot
from bot.states import BlockStates
from bot.texts import *
from bot.utils import save_to_excel

command_router = Router()


@command_router.message(CommandStart())
async def start_command(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    if not await user_exists(message.from_user.id):
        await message.reply(text=START_TEXT, reply_markup=register_kb())
    else:
        user = await get_user(message.from_user.id)
        await message.answer(WELCOME_TEXT.format(message.from_user.id, user.name))
        await message.answer(FOR_ENTER_PROMO_TEXT, reply_markup=promo_kb())


@command_router.message(Command('mypromos'))
async def list_command(message: Message):
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
    await sleep(0.5)
    await message.answer(HELP_COMMAND_TEXT)


@command_router.message(Command('export'))
async def help_command(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.5)
    promos = await get_all_promos()
    if promos:
        msg1 = await message.answer('⏳')
        msg2 = await message.answer(GETTING_READY_TEXT)
        df = pd.DataFrame(promos)
        excel_file_name = 'data.xlsx'
        await save_to_excel(df, excel_file_name)
        await bot.send_chat_action(message.chat.id, 'upload_document')
        await message.answer_document(FSInputFile(excel_file_name))
        await msg1.delete()
        await msg2.delete()
    else:
        await message.answer(NO_DATA_TEXT)


@command_router.message(Command('block'))
async def block_command(message: Message, state: FSMContext):
    await message.answer(ASK_BLOCK_USER_PHONE_NUMBER_TEXT)
    await state.set_state(BlockStates.phone)
