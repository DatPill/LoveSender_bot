from aiogram.fsm.state import State, StatesGroup


class UserCreation(StatesGroup):
    setting_daily_compliment = State()
    choosing_animal = State()


class UserEditing(StatesGroup):
    changing_animal = State()
