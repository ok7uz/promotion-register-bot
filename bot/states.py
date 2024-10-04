from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    """
    States for user registration process.
    """
    name = State()
    phone = State()
    address = State()


class PromoStates(StatesGroup):
    """
    States for handling promotional code submissions.
    """
    photo = State()
    promo_code = State()


class BlockStates(StatesGroup):
    """
    States for blocking users.
    """
    phone = State()


class MessageStates(StatesGroup):
    get_message = State()
