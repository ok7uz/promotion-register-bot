from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    regName = State()
    regPhone = State()
    regAddress = State()
