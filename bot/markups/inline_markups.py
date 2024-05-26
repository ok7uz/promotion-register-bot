from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.texts import ENTER_ONE_MORE_PROMO_TEXT, ENTER_PROMO_TEXT, SIGN_UP_TEXT
from config import CHANNELS

promo_callback_data = 'add-promo'
register_callback_data = 'register'
contact_cd = 'contact'


def create_channels_keyboard():
    """
    Create an inline keyboard with buttons for subscribing to channels.

    Returns:
        InlineKeyboardMarkup: The created inline keyboard markup.
    """
    buttons = [
        [InlineKeyboardButton(text=channel['name'], url=channel['link'])] for channel in CHANNELS
    ]
    buttons.append([InlineKeyboardButton(text=ENTER_ONE_MORE_PROMO_TEXT, callback_data=promo_callback_data)])
    return InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, inline_keyboard=buttons)

def create_promo_keyboard():
    """
    Create an inline keyboard with a button for entering a promo code.

    Returns:
        InlineKeyboardMarkup: The created inline keyboard markup.
    """
    return InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                inline_keyboard=[[InlineKeyboardButton(text=ENTER_PROMO_TEXT, callback_data=promo_callback_data)]])

def create_registration_keyboard():
    """
    Create an inline keyboard with a button for user registration.

    Returns:
        InlineKeyboardMarkup: The created inline keyboard markup.
    """
    return InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                inline_keyboard=[[InlineKeyboardButton(text=SIGN_UP_TEXT, callback_data=register_callback_data)]])
