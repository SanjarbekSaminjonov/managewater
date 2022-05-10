from email import message
from tkinter import E
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils.local_services.users import makeup_user_info
from utils import backend_services, local_services
from keyboards import default, inline
from states.users import UserLoginRegisterState, UserRegisterState
from data.config import REGIONS


@dp.message_handler(text_contains="Bekor qilish", state=UserRegisterState.all_states)
async def cancel_login_register(message: Message, state: FSMContext):
    await message.answer("Ro'yxatdan o'tish bekor qilindi", reply_markup=default.login_register_confirm)
    await UserLoginRegisterState.login_register.set()


@dp.message_handler(text_contains="Ro'yxatdan o'tish", state=UserLoginRegisterState.login_register)
async def register(message: Message):
    await message.answer(
        "📝 Ro'yxatga olish boshlandi \n\nTelefon raqamingizni yuboring",
        reply_markup=default.contact
    )
    await UserRegisterState.username.set()


@dp.message_handler(state=UserRegisterState.username, content_types='contact')
async def register(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiriting", reply_markup=default.cancel)
    await UserRegisterState.next()
    await state.update_data({'username': message.contact.phone_number})


@dp.message_handler(state=UserRegisterState.first_name)
async def register(message: Message, state: FSMContext):
    await message.answer('Familiyangizni kiriting')
    await state.update_data({'first_name': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.last_name)
async def register(message: Message, state: FSMContext):
    regions = default.buttons_of_list(REGIONS.keys())
    await message.answer(
        'Viloyat/Shaharingizni kiriting',
        reply_markup=regions
    )
    await state.update_data({'last_name': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.region)
async def register(message: Message, state: FSMContext):
    region = message.text
    districts = REGIONS.get(region)
    if districts is not None:
        districts_keyboards = default.buttons_of_list(districts)
        await message.answer(
            'Tuman/Shaharingizni kiriting',
            reply_markup=districts_keyboards
        )
    else:
        await message.answer(
            'Tuman/Shaharingizni kiriting',
            reply_markup=default.cancel
        )
    await state.update_data({'region': region})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.city)
async def register(message: Message, state: FSMContext):
    await message.answer('Tashkilot nomini kiriting', reply_markup=default.cancel)
    await state.update_data({'city': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.org_name)
async def register(message: Message, state: FSMContext):
    password_text = "Barcha ma'lumotlaringiz xavfsizligi uchun parol kiriting.\n"
    password_text += "<i>Parol uzunligi 4 - 6 xonali bo'lishi lozim</i>\n\n"
    password_text += "Parol:"
    await message.answer(
        text=password_text, reply_markup=inline.numbers_buttons)
    await state.update_data({'org_name': message.text})
    await UserRegisterState.next()


@dp.callback_query_handler(state=UserRegisterState.password)
async def register(call: CallbackQuery, state: FSMContext):
    call_data = call.data
    data = await state.get_data()
    password = data.get('password')
    password_text = "Barcha ma'lumotlaringiz xavfsizligi uchun parol kiriting.\n"
    password_text += "<i>Parol uzunligi 4 - 6 xonali bo'lishi lozim</i>\n\n"
    if call_data.isdigit():
        if password is None:
            password = call_data
        else:
            password += call_data
        password_text += f"Parol: <b>{'*' * len(password)}</b>"
        await call.message.edit_text(text=password_text, reply_markup=inline.numbers_buttons)
        await state.update_data({"password": password})

    elif call_data == "show":
        if password is None:
            password_text += "Parol:"
        else:
            password_text += f"Parol: <b>{password}</b>"
        await call.message.edit_text(text=password_text, reply_markup=inline.numbers_buttons)

    elif call_data == "clear":
        if len(password) > 0:
            password = password[:-1]
            password_text += f"Parol: <b>{'*' * len(password)}</b>"
            await call.message.edit_text(text=password_text, reply_markup=inline.numbers_buttons)
            await state.update_data({"password": password})

    elif call_data == "submit":
        if len(password) < 4 or len(password) > 6:
            await call.answer("Parol uzunligi noto'g'ri!", show_alert=True)
        else:
            await call.message.edit_reply_markup()
            await call.message.answer(
                text=local_services.users.makeup_user_info(data=data) +
                "\n\nBarcha ma'lumotlar to'g'rimi?",
                reply_markup=default.yes_no_buttons
            )
            await UserRegisterState.next()

    await call.answer(cache_time=0)


@dp.message_handler(state=UserRegisterState.save_user, text_contains="Ha")
async def register(message: Message, state: FSMContext):
    await message.answer("Ma'lumotlar tizimga saqlanmoqda ...", reply_markup=None)
    data = await state.get_data()
    chat_id = message.from_user.id
    data['chat_id'] = str(chat_id)
    resp = await backend_services.users.register(data)
    if resp:
        username = data.get('username')
        password = data.get('password')
        db.add_user(chat_id, username, password)
        await message.answer(
            "Jarayon yakunlandi, Sabr bilan ma'lumotlarni kiritganingiz uchun tashakkur. 😊",
            reply_markup=default.home_sections
        )
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(
            "Ro'yxatdan o'tishda xatolik bor. Qayta harakat qiling.",
            reply_markup=default.login_register_confirm
        )
        await UserLoginRegisterState.login_register.set()


@dp.message_handler(state=UserRegisterState.save_user, text_contains="Yo'q")
async def register(message: Message):
    await message.answer(
        "Ro'yxatdan o'tish yakunlanmadi. Qayta harakat qiling.",
        reply_markup=default.login_register_confirm
    )
    await UserLoginRegisterState.login_register.set()
