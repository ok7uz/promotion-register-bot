from typing import Optional
from loguru import logger

from bot.models import BlockedUser, Promo, User


async def create_user(user_id: int, name: str, phone_number: str, address: str) -> Optional[User]:
    new_user = await User.create(
        id=user_id,
        name=name,
        phone_number=phone_number,
        address=address
    )
    logger.success(f'#{user_id} user created successfully.')
    return new_user


async def user_exists(user_id: int) -> bool:
    return await User.exists(id=user_id)


async def get_user(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    return user


async def get_all_users():
    users = await User.all()
    return users


async def delete_all_data():
    await BlockedUser.all().delete()
    await Promo.all().delete()
    await User.all().delete()
