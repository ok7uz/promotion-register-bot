from loguru import logger

from bot.models import Promo, User


async def create_promo(user_id: int, file_id: str, code: str):
    promos = await Promo.all().order_by('special_code')
    last_promo_special_code = promos[-1].special_code if await Promo.exists() else 0
    new_special_code = str(int(last_promo_special_code) + 1).zfill(6)
    new_promo = await Promo.create(
        user_id=user_id,
        file_id=file_id,
        code=code,
        special_code=new_special_code
    )
    logger.success(f'#{new_promo.special_code} promo created successfully.')
    return new_promo


async def promo_exists(code: str) -> bool:
    return await Promo.exists(code=code)


async def get_user_promos(user_id: int):
    return await Promo.filter(user_id=user_id)


async def get_all_promos():
    promos = await Promo.filter().prefetch_related('user')
    data = []
    for promo in promos:
        user_data = {
            'Ism': promo.user.name,
            'Telefon raqam': promo.user.phone_number,
            'Manzil': promo.user.address,
            'PROMO Kod': promo.code,
            'Maxsus kod': promo.special_code,
            'file_id': promo.file_id,
            'Rasm': None
        }
        data.append(user_data)
    return data


async def delete_user_promos(phone_number):
    user = await User.get_or_none(phone_number=phone_number)
    await user.promos.all().delete() if user else None
