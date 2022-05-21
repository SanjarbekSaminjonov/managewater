from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import backend_services, local_services
from keyboards import default, inline
from states.users import UserLoginRegisterState, UserRegisterState
from data.config import REGIONS


@dp.message_handler(text_contains="Bekor qilish", state=UserRegisterState.all_states)
async def cancel_login_register(message: Message, state: FSMContext):
    await message.answer("Ro'yxatdan o'tish bekor qilindi", reply_markup=default.login_register_confirm)
    await state.reset_data()
    await UserLoginRegisterState.login_register.set()


@dp.message_handler(text_contains="Ro'yxatdan o'tish", state=UserLoginRegisterState.login_register)
async def register(message: Message):
    await UserRegisterState.username.set()
    await message.answer(
        "📝 Ro'yxatga olish boshlandi \n\nQuyidagi tugma orqali telefon raqamingizni yuboring",
        reply_markup=default.contact
    )


@dp.message_handler(state=UserRegisterState.username, content_types='contact')
async def register(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer("Ismingizni kiriting", reply_markup=default.cancel)
    phone = message.contact.phone_number
    await state.update_data({'username': phone if phone.startswith('+') else '+' + phone})


@dp.message_handler(state=UserRegisterState.first_name)
async def register(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer('Familiyangizni kiriting')
    await state.update_data({'first_name': message.text})


@dp.message_handler(state=UserRegisterState.last_name)
async def register(message: Message, state: FSMContext):
    regions = default.buttons_of_list(REGIONS.keys())
    await UserRegisterState.next()
    await message.answer(
        'Viloyat/Shaharingizni tanlang',
        reply_markup=regions
    )
    await state.update_data({'last_name': message.text})


@dp.message_handler(state=UserRegisterState.region)
async def register(message: Message, state: FSMContext):
    await UserRegisterState.next()
    region = message.text
    districts = REGIONS.get(region)
    if districts is not None:
        districts_keyboards = default.buttons_of_list(districts)
        await message.answer(
            'Tuman/Shaharingizni tanlang',
            reply_markup=districts_keyboards
        )
    else:
        await message.answer(
            'Tuman/Shaharingizni kiriting',
            reply_markup=default.cancel
        )
    await state.update_data({'region': region})


@dp.message_handler(state=UserRegisterState.city)
async def register(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer(
        'Tashkilot nomini kiriting',
        reply_markup=default.cancel
    )
    await state.update_data({'city': message.text})


@dp.message_handler(state=UserRegisterState.org_name)
async def register(message: Message, state: FSMContext):
    password_text = "Barcha ma'lumotlaringiz xavfsizligi uchun parol kiriting.\n"
    password_text += "<i>Parol uzunligi 4 - 6 xonali bo'lishi lozim</i>\n\n"
    password_text += "Parol:"
    await message.answer(
        text=password_text,
        reply_markup=inline.numbers_buttons
    )
    await state.update_data({'org_name': message.text})
    await UserRegisterState.next()


@dp.callback_query_handler(state=UserRegisterState.password)
async def register(call: CallbackQuery, state: FSMContext):
    call_data = call.data
    data = await state.get_data()
    show_password = data.get('show_password', False)
    password = data.get('password', '')
    password_text = "Barcha ma'lumotlaringiz xavfsizligi uchun parol kiriting.\n"
    password_text += "<i>Parol uzunligi 4 - 6 xonali bo'lishi lozim</i>\n\n"

    if call_data.isdigit():
        password += call_data
        password_text += f"Parol: <b>{password if show_password else '*' * len(password)}</b>"
        await call.message.edit_text(text=password_text, reply_markup=inline.numbers_buttons)
        await state.update_data({"password": password})

    elif call_data == "show":
        show_password = not show_password
        if password:
            password_text += f"Parol: <b>{password if show_password else '*' * len(password)}</b>"
            await call.message.edit_text(text=password_text, reply_markup=inline.numbers_buttons)
        await state.update_data({"show_password": show_password})

    elif call_data == "clear":
        if len(password) > 0:
            password = password[:-1]
            password_text += f"Parol: <b>{password if show_password else '*' * len(password)}</b>"
            await call.message.edit_text(text=password_text, reply_markup=inline.numbers_buttons)
            await state.update_data({"password": password})

    elif call_data == "submit":
        if len(password) < 4 or len(password) > 6:
            await call.answer("Parol uzunligi noto'g'ri!", show_alert=True)
        else:
            await UserRegisterState.next()
            await call.message.delete()
            await call.message.answer(
                text=local_services.users.makeup_user_info(data=data) +
                     "\n\nBarcha ma'lumotlar to'g'rimi?",
                reply_markup=default.yes_no_buttons
            )

    await call.answer(cache_time=0)


@dp.message_handler(state=UserRegisterState.save_user, text_contains="Ha")
async def register(message: Message, state: FSMContext):
    await message.answer("Ma'lumotlar tizimga saqlanmoqda ...")
    data = await state.get_data()
    chat_id = message.from_user.id
    data['chat_id'] = str(chat_id)
    resp = await backend_services.users.register(data)
    if resp:
        await message.answer(
            "Jarayon yakunlandi, Sabr bilan ma'lumotlarni kiritganingiz uchun tashakkur. 😊",
            reply_markup=default.home_sections
        )
        await state.finish()
    else:
        await UserLoginRegisterState.login_register.set()
        await message.answer(
            "Ro'yxatdan o'tishda xatolik bor. Qayta harakat qiling.",
            reply_markup=default.login_register_confirm
        )
    await state.reset_data()


@dp.message_handler(state=UserRegisterState.save_user, text_contains="Yo'q")
async def register(message: Message, state: FSMContext):
    await UserLoginRegisterState.login_register.set()
    await message.answer(
        "Ro'yxatdan o'tish yakunlanmadi. Qayta harakat qiling.",
        reply_markup=default.login_register_confirm
    )
    await state.reset_data()
