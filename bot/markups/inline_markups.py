from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.texts import ENTER_ONE_MORE_PROMO_TEXT, ENTER_PROMO_TEXT, SEND_PHONE_NUMBER_TEXT, SIGN_UP_TEXT
from config import CHANNELS

promo_callback_data = 'add-promo'
register_callback_data = 'register'
contact_cd = 'contact'


def channels_kb():
    markup = InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True,
        inline_keyboard=[
            [InlineKeyboardButton(text=channel['name'], url=channel['link'])] for channel in CHANNELS
        ] + [[InlineKeyboardButton(text=ENTER_ONE_MORE_PROMO_TEXT, callback_data=promo_callback_data)]])
    return markup

def promo_kb():
    markup = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                 inline_keyboard=[[InlineKeyboardButton(text=ENTER_PROMO_TEXT, callback_data=promo_callback_data)]])
    return markup


def register_kb():
    markup = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                 inline_keyboard=[[InlineKeyboardButton(text=SIGN_UP_TEXT, callback_data=register_callback_data)]])
    return markup

