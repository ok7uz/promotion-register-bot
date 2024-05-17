from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    name = State()
    phone = State()
    address = State()
    photo = State()
    promoCode = State()
