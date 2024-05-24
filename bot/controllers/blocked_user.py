from loguru import logger

from bot.models import BlockedUser


async def create_blocked_user(phone_number: str):
    blocked_user = await BlockedUser.get_or_create(phone_number=phone_number)
    logger.warning(f'{phone_number} blocked.')
    return blocked_user


async def is_user_blocked(phone_number: str) -> bool:
    return await BlockedUser.exists(phone_number=phone_number)
