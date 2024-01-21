from aiogram.dispatcher.filters.state import StatesGroup, State


class CalculateState(StatesGroup):
    calculation = State()
    first_pay = State()
