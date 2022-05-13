from aiogram.dispatcher.filters.state import StatesGroup, State


class BasinCreateState(StatesGroup):
    id = State()
    phone = State()
    name = State()
    height = State()
    location = State()
    save_basin = State()
