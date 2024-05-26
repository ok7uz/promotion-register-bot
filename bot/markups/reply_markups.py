from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.texts import SEND_PHONE_NUMBER_TEXT, SIGN_UP_TEXT, ENTER_PROMO_TEXT

def create_registration_keyboard():
    """
    Create a reply keyboard with a button for user registration.

    Returns:
        ReplyKeyboardMarkup: The created reply keyboard markup.
    """
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                               keyboard=[[KeyboardButton(text=SIGN_UP_TEXT)]])

def create_promo_keyboard():
    """
    Create a reply keyboard with a button for entering a promo code.

    Returns:
        ReplyKeyboardMarkup: The created reply keyboard markup.
    """
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                               keyboard=[[KeyboardButton(text=ENTER_PROMO_TEXT)]])

def create_contact_keyboard():
    """
    Create a reply keyboard with a button for sending the phone number as a contact.

    Returns:
        ReplyKeyboardMarkup: The created reply keyboard markup.
    """
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                               keyboard=[[KeyboardButton(text=SEND_PHONE_NUMBER_TEXT, request_contact=True)]])
