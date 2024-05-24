from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    name = State()
    phone = State()
    address = State()


class PromoStates(StatesGroup):
    photo = State()
    promoCode = State()


class BlockStates(StatesGroup):
    phone = State()
