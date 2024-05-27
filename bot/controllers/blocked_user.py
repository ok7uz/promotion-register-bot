from loguru import logger
from bot.models import BlockedUser


async def create_blocked_user(phone_number: str):
    """
    Create a blocked user entry in the database.

    Args:
        phone_number (str): The phone number of the blocked user.

    Returns:
        BlockedUser: The blocked user object.
    """
    try:
        blocked_user, _ = await BlockedUser.get_or_create(phone_number=phone_number)
        logger.warning(f'{phone_number} blocked.')
        return blocked_user
    except Exception as e:
        logger.error(f'Failed to create blocked user: {e}')
        raise


async def is_user_blocked(phone_number: str) -> bool:
    """
    Check if a user is blocked.

    Args:
        phone_number (str): The phone number of the user.

    Returns:
        bool: True if the user is blocked, else False.
    """
    try:
        return await BlockedUser.exists(phone_number=phone_number)
    except Exception as e:
        logger.error(f'Failed to check if user {phone_number} is blocked: {e}')
        raise
