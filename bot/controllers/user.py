from typing import Optional
from loguru import logger

from bot.models import User


async def create_user(user_id: int, name: str, phone_number: str, address: str, file_id:str, promo_code: str) -> Optional[User]:
    users = await User.all().order_by('special_code')
    last_user_code = users[-1].special_code if await User.exists() else 0
    new_code = str(int(last_user_code) + 1).zfill(6)
    new_user =  await User.create(
        id=user_id,
        name=name,
        phone_number=phone_number,
        address=address,
        file_id=file_id,
        promo_code=promo_code,
        special_code=new_code
    )
    logger.success(f'ID: {user_id} user created successfully.')
    return new_user


async def user_exists(user_id: int) -> bool:
    return await User.exists(id=user_id)


async def get_user(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    return user


async def get_all_users():
    users = await User.all()
    return users
