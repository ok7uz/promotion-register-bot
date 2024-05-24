from config import ADMIN_USERNAME

START_COMMAND_DESCRIPTION = "Botni ishga tushurish"
MYPROMOS_COMMAND_DESCRIPTION = "Promo kodlaringiz roʻyxati"
HELP_COMMAND_DESCRIPTION = "Admin bilan bogʻlanish"
EXPORT_COMMAND_DESCRIPTION = "Ma'lumotlarni olish"
BLOCK_COMMAND_DESCRIPTION = "Foydalanuvchilarni blok qilish"
SIGN_UP_TEXT = "👤 Roʻyxatdan oʻtish"
ENTER_PROMO_TEXT = "🎟 Promo kodni kiritish"
SEND_PHONE_NUMBER_TEXT = '📞 Telefon raqamni yuborish'
START_TEXT = "🤖 Assalomu alaykum. Botdan foydalanish uchun roʻyxatdan oʻtishingiz kerak."
WELCOME_TEXT = "🤖 Assalomu alaykum <b><a href='tg://user?id={}'>{}</a>!</b>"
SIGNED_UP_TEXT = "🤖 Hurmatli {}, siz roʻyxatdan oʻtgansiz"
ENTER_NAME_TEXT = "✍️ Iltimos ismingizni kiriting"
ENTER_PHONE_NUMBER_TEXT = "📞 Iltimos telefon raqamingizni yuboring"
ENTER_ADDRESS_TEXT = "🏠 Yashash manzilingiz:"
ENTER_PROMO_PHOTO_TEXT = "🖼 Kupon rasmini yuboring:"
ENTER_PHOTO_TEXT = "🖼 Rasm koʻrinishida yuboring"
PHOTO_SAVED_TEXT = "🖼 Rasm saqlandi"
ENTER_PROMO_CODE_TEXT = "🎟 Promo kodni kiriting"
DATA_SAVED_TEXT = "✅ Ma'lumotlar saqlandi"
SPECIAL_CODE_TEXT = '<b>❇️ Aksiyada qatnashish uchun maxsus kodingiz:</b> <code>{}</code>'
USERS_COUNT_TEXT = '👤 <b>Foydalanuvchilar soni:</b> {} ta'
FOR_ENTER_PROMO_TEXT: str = f"Promo kodni kiritish uchun quyidagi <b>{ENTER_PROMO_TEXT}</b> tugmasini bosing"
PROMO_SAVED_TEXT = "✅ Promo vaucher ma'lumotlar saqlandi"
PROMO_HAS_BEEN_USED = ('❗️ <b>Bu promo kod avval ishlatilgan. Haqiqatdan mahsulot sizda boʻlsa kuponni videoga olib '
                       'bizga yuboring <a href="{}">ADMIN</a></b>'.format(ADMIN_USERNAME))
USER_PROMOS_COUNT_TEXT = "<b>Siz kiritgan promolar soni {} ta</b>\n\n"
NO_PROMOS_TEXT = "<b>❌ Siz hali promo kiritmagansiz</b>"
PROMO_TEXT = '🔸 <code>{}</code> - promo kod: <b>{}</b>\n'
GETTING_READY_TEXT = "<b>Ma'lumotlar yuklanyapti...</b>"
CHANNELS_TEXT = ("Hurmatli mijoz. Biz bilan birga ekanligingizdan xursandmiz. Aksiya ishtirokchisiga aylanganingiz bilan"
                 " tabriklaymiz.\n\n<b>⚠️ Eslatma:</b> <i>Aksiya gʻolibi sovgʻani olishi uchun taglik qadogʻiga yopishtirilgan "
                 "stikerga shikastlamagan holda saqlashi zarur. Stiker qadoqdan olingan  va muhr oʻrnidan siljigan "
                 "holda boʻlsa hisobga olinmaydi.</i>\n\n<b>Aksiya jarayonlarini, gʻoliblar va oʻyinni kuzatish uchun ushbu "
                 "kanallarimizga obuna boʻling.1</b>")
HELP_COMMAND_TEXT = 'Admin bilan bogʻlanish: <a href="{}">ADMIN</a>'.format(ADMIN_USERNAME)
ASK_BLOCK_USER_PHONE_NUMBER_TEXT = 'Blok qilinadigan foydalanuvchining <b>telefon raqami</b>ni kiriting'
NO_DATA_TEXT = "<b>❌ Ma'lumotlar yoʻq</b>"
INFO_TEXT = ("<b>✅ Ma'lumotlar saqlandi</b>\n\n"
             "<b>👤 Ism:</b>  {}\n"
             "<b>📞 Telefon raqam:</b>  {}\n"
             "<b>🏠 Yashash manzil:</b>  {}")
