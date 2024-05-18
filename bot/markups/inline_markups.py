from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNELS


def channels_kb():
    markup = InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True,
        inline_keyboard=[
            [InlineKeyboardButton(text=channel['name'], url=channel['link'])] for channel in CHANNELS
        ])
    return markup
