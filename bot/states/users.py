from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    region = State()
    city = State()
    org_name = State()
    save_user = State()


class UserLoginState(StatesGroup):
    secret_key = State()
