from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reg_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Ro'yxatdan o'tish")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=" 📞Telefon raqamni yuborish📞 ",
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Iltimos <<📞Telefon raqamni yuborish📞>> tugmasini bosing",
    one_time_keyboard=True
)
