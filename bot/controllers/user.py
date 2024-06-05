from typing import Optional
from loguru import logger
from bot.models import BlockedUser, Promo, User, Code
from tortoise.exceptions import DoesNotExist


async def create_user(user_id: int, name: str, phone_number: str, address: str) -> Optional[User]:
    """
    Create a new user in the database.

    Args:
        user_id (int): The user's ID.
        name (str): The user's name.
        phone_number (str): The user's phone number.
        address (str): The user's address.

    Returns:
        Optional[User]: The newly created user object if successful, else None.
    """
    try:
        new_user = await User.create(
            id=user_id,
            name=name,
            phone_number=phone_number,
            address=address
        )
        logger.success(f'#{user_id} user created successfully.')
        return new_user
    except Exception as e:
        logger.error(f'Failed to create user #{user_id}: {e}')
        return None


async def user_exists(user_id: int) -> bool:
    """
    Check if a user exists in the database.

    Args:
        user_id (int): The user's ID.

    Returns:
        bool: True if the user exists, else False.
    """
    try:
        return await User.exists(id=user_id)
    except Exception as e:
        logger.error(f'Failed to check user existence for #{user_id}: {e}')
        return False


async def get_user(user_id: int) -> Optional[User]:
    """
    Get a user from the database by user ID.

    Args:
        user_id (int): The user's ID.

    Returns:
        Optional[User]: The user object if found, else None.
    """
    try:
        return await User.get(id=user_id)
    except DoesNotExist:
        logger.warning(f'User #{user_id} does not exist.')
        return None
    except Exception as e:
        logger.error(f'Failed to get user #{user_id}: {e}')
        return None


async def get_all_users():
    """
    Get all users from the database.

    Returns:
        List[User]: List of all user objects.
    """
    try:
        return await User.all()
    except Exception as e:
        logger.error(f'Failed to get all users: {e}')
        return []


async def delete_all_data():
    """
    Delete all data (users, blocked users, promos) from the database.
    """
    try:
        await BlockedUser.all().delete()
        await Promo.all().delete()
        await User.all().delete()
        logger.success('All data deleted successfully.')
    except Exception as e:
        logger.error(f'Failed to delete all data: {e}')
