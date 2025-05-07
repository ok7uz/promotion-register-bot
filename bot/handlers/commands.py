import os
from asyncio import sleep
from datetime import timedelta, timezone

from loguru import logger
import pandas as pd
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command
from bot.controllers.blocked_user import is_user_blocked
from bot.controllers.code import create_code, code_exists
from bot.controllers.promo import get_user_promos, get_all_promos
from bot.controllers.user import delete_all_data, get_user, user_exists
from bot.markups.inline_markups import create_promo_keyboard, create_registration_keyboard, create_order_keyboard
from bot.misc import bot, local_bot
from bot.states import BlockStates, MessageStates, GetCodesFileStates, ExportStates
from bot.texts import *
from bot.utils import save_to_excel, create_month_keyboard
from bot.models import Promo
from config import ADMIN_USERNAME, ADMINS

command_router = Router()


@command_router.message(Command('start'))
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


@command_router.message(Command('order'))
async def start_command(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer(ORDER_TEXT, reply_markup=create_order_keyboard())


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
            text += PROMO_TEXT.format(promo.special_code, promo.code_id)
        return await message.answer(text)
    await message.answer(NO_PROMOS_TEXT)


@command_router.message(Command('help'))
async def help_command(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer(HELP_COMMAND_TEXT.format(ADMIN_USERNAME))


@command_router.message(Command('export'))
async def export_command(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
        
    await message.answer(
        "📅 Ma'lumot olish uchun oyni belgilang:",
        reply_markup=create_month_keyboard()
    )
    await state.set_state(ExportStates.select_month)


@command_router.callback_query(lambda c: c.data.startswith('month:'))
async def handle_month_selection(callback: CallbackQuery, state: FSMContext):
    """Handle month selection and generate Excel file"""
    try:
        # Parse month and year from callback
        _, month, year = callback.data.split(':')
        month, year = int(month), int(year)
        
        # Show progress
        status_msg = await callback.message.edit_text("<b>⏳ Ma'lumotlar tayyotlanyapti ...</b>")
        
        # Get promos for selected period
        promos = await get_all_promos(year=year, month=month)
        if not promos:
            await status_msg.edit_text("<b>📭 Bu oy uchun ma'lumot mavjud emas</b>")
            await state.clear()
            return
            
        # Update status and prepare file
        await status_msg.edit_text(f"<b>📊 {len(promos)} ta promo ma'lumot tayyorlanyapti ...</b>")
        
        # Generate Excel file
        file_name = f'promos_{month:02d}_{year}.xlsx'
        try:
            df = pd.DataFrame(promos)
            await save_to_excel(df, file_name)
            
            # Send file
            await local_bot.send_document(
                chat_id=callback.message.chat.id, 
                document=FSInputFile(file_name),
                caption=f"<b>📊 {month:02d}/{year} uchun promo kodlar ro'yxati</b>"
            )
            
        finally:
            # Cleanup
            try:
                os.remove(file_name)
            except OSError:
                pass
            
        await status_msg.delete()
        await state.clear()
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        await callback.message.edit_text(
            "❌ Export failed. Please try again later."
        )
        await state.clear()


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


@command_router.message(Command('send'))
async def delete_data_command(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return

    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer(SEND_MESSAGE_TEXT_TEXT)
    await state.set_state(MessageStates.get_message)


@command_router.message(Command('set0'))
async def set0(message: Message):
    try:
        if message.from_user.id not in ADMINS:
            return

        # start_of_year = datetime(2025, 1, 1)
        # end_of_year = datetime(2025, 12, 31)
        #
        #
        # await bot.send_chat_action(message.chat.id, 'typing')
        # await sleep(0.2)
        # await message.answer('Calculating ...')
        #
        # new_promos = await Promo.filter(date__gte=start_of_year, date__lte=end_of_year).order_by('date')
        # await message.answer('Yangi promo kodlar olindi')
        # await message.answer(str(len(new_promos)))
        # old_promos = await Promo.filter(date__lt=start_of_year).all()
        # await message.answer('Eski promo kodlar olindi')
        # await message.answer(str(len(old_promos)))
        # i = 1
        #
        # for promo in old_promos:
        #     promo.special_code = ''.join(choices(ascii_lowercase, k=6))
        #     await promo.save()
        #
        # await bot.send_chat_action(message.chat.id, 'typing')
        # await sleep(0.2)
        # await message.answer('The old promos have been successfully updated')
        #
        # for promo in new_promos:
        #     promo.special_code = str(i).zfill(6)
        #     await promo.save()
        #     i += 1
        #
        # await bot.send_chat_action(message.chat.id, 'typing')
        # await sleep(0.2)
        # await message.answer("The new promos have been successfully updated.")
        # await message.answer('✅ DONE!')
        latest = await Promo.all().order_by('-date').first()
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await message.answer(f'<b>Latest</b>')
        await message.answer(f'PromoDate: {latest.date}')
    except Exception as e:
        await bot.send_chat_action(message.chat.id, 'typing')
        await sleep(0.2)
        await message.answer(f"⁉️ Error: {str(e)}")


@command_router.message(Command('latest'))
async def get_latest(message: Message):
    if message.from_user.id not in ADMINS:
        return

    latest = await Promo.all().order_by('-date').first()
    time_delta = timedelta(hours=5)
    tz_obj = timezone(time_delta, name='UZ')
    await bot.send_chat_action(message.chat.id, 'typing')
    await sleep(0.2)
    await message.answer((f'<b>Special Code:</b> {latest.special_code}\n'
                          f'<b>Date</b>: {latest.date.astimezone(tz_obj).strftime('%H:%M:%S  %d.%m.%Y')}'))


@command_router.message(Command('upload'))
async def upload_codes(message: Message, state: FSMContext):
    print(ADMINS)
    if message.from_user.id not in ADMINS:
        return

    await message.answer('Send file')
    await state.set_state(GetCodesFileStates.get_file)


@command_router.message(GetCodesFileStates.get_file)
async def get_file(message: Message, state: FSMContext):
    document = message.document

    if document:
        file = await message.bot.get_file(document.file_id)
        file_path = file.file_path
        file_data = await message.bot.download_file(file_path)

        codes = file_data.readlines()

        success = 0
        fail = 0
        last = None

        for code in codes:
            code = code.decode('ascii').strip()
            code = code[:-1] if code[-1] == ';' else code
            if not await code_exists(code):
                await create_code(code)
                success += 1
            else:
                fail += 1
            last = code

        await message.answer(
            'DONE!\n\n'
            f'<b>ALL:</b>: {success + fail}'
            f'<b>Success:</b> {success}'
            f'<b>Fail:</b> {fail}'
            f'<b>Last:</b> {last}'
        )
        await state.clear()
