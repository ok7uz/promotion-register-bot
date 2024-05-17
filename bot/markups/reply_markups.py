from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.texts import SEND_PHONE_NUMBER_TEXT, SIGN_UP_TEXT


def register_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                 keyboard=[[KeyboardButton(text=SIGN_UP_TEXT)]])
    return markup


def contact_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                 keyboard=[[KeyboardButton(text=SEND_PHONE_NUMBER_TEXT, request_contact=True)]])
    return markup
