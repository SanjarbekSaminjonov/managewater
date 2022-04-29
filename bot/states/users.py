from aiogram.dispatcher.filters.state import State, StatesGroup


class UserLoginRegisterState(StatesGroup):
    login_register = State()


class UserRegisterState(StatesGroup):
    username = State()
    first_name = State()
    last_name = State()
    region = State()
    city = State()
    org_name = State()
    password1 = State()
    password2 = State()
    save_user = State()

