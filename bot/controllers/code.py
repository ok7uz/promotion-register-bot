from loguru import logger
from bot.models import Promo, User, Code


async def create_code(code: str):
    """
    Create a new promo in the database.

    Args:
        code (str): The promo code.

    Returns:
        Promo: The newly created promo object.
    """
    try:
        new_code = await Code.create(code=code)
        logger.success(f'Code {code} created successfully.')
        return new_code
    except Exception as e:
        logger.error(f'Failed to create promo: {e}')
        raise


async def code_exists(code: str) -> bool:
    """
    Check if a promo with the given code exists in the database.

    Args:
        code (str): The promo code to check.

    Returns:
        bool: True if the promo exists, else False.
    """
    try:
        return await Code.exists(code=code)
    except Exception as e:
        logger.error(f'Failed to check promo existence for code {code}: {e}')
        return False


async def delete_code(code: str):
    """
    Delete all promos associated with a user.

    Args:
       code (str): The promo code to check.

    Returns:
        None
    """
    try:
        code = await Code.get_or_none(code=code)
        await code.delete()
    except Exception as e:
        logger.error(f'Failed to delete code: {e}')
