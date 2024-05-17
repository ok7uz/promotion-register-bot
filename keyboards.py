from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import SIGN_UP_TEXT, SEND_PHONE_NUMBER_TEXT

reg_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=SIGN_UP_TEXT)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=SEND_PHONE_NUMBER_TEXT,
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Iltimos <<📞Telefon raqamni yuborish📞>> tugmasini bosing",
    one_time_keyboard=True
)
