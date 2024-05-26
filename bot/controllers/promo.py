from loguru import logger
from bot.models import Promo, User

async def create_promo(user_id: int, file_id: str, code: str):
    """
    Create a new promo in the database.

    Args:
        user_id (int): The ID of the user associated with the promo.
        file_id (str): The ID of the file associated with the promo.
        code (str): The promo code.

    Returns:
        Promo: The newly created promo object.
    """
    try:
        promos = await Promo.all().order_by('special_code')
        last_promo_special_code = promos[-1].special_code if await Promo.exists() else 0
        new_special_code = str(int(last_promo_special_code) + 1).zfill(6)
        new_promo = await Promo.create(
            user_id=user_id,
            file_id=file_id,
            code=code,
            special_code=new_special_code
        )
        logger.success(f'Promo #{new_promo.special_code} created successfully.')
        return new_promo
    except Exception as e:
        logger.error(f'Failed to create promo: {e}')
        raise

async def promo_exists(code: str) -> bool:
    """
    Check if a promo with the given code exists in the database.

    Args:
        code (str): The promo code to check.

    Returns:
        bool: True if the promo exists, else False.
    """
    try:
        return await Promo.exists(code=code)
    except Exception as e:
        logger.error(f'Failed to check promo existence for code {code}: {e}')
        return False

async def get_user_promos(user_id: int):
    """
    Get all promos associated with a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Promo]: List of promo objects associated with the user.
    """
    try:
        return await Promo.filter(user_id=user_id)
    except Exception as e:
        logger.error(f'Failed to get promos for user #{user_id}: {e}')
        return []

async def get_all_promos():
    """
    Get all promos from the database.

    Returns:
        List[Dict]: List of dictionaries containing promo data.
    """
    try:
        promos = await Promo.all().prefetch_related('user')
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
    except Exception as e:
        logger.error(f'Failed to get all promos: {e}')
        return []

async def delete_user_promos(phone_number):
    """
    Delete all promos associated with a user.

    Args:
        phone_number (str): The phone number of the user.

    Returns:
        None
    """
    try:
        user = await User.get_or_none(phone_number=phone_number)
        await user.promos.all().delete() if user else None
    except Exception as e:
        logger.error(f'Failed to delete promos for user with phone number {phone_number}: {e}')
