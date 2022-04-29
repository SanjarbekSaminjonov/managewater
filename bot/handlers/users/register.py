from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils.local_services.users import makeup_user_info
from utils import backend_services
from keyboards import default
from states.users import UserLoginRegisterState, UserRegisterState


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
    await message.answer('Viloyat/Shaharingizni kiriting')
    await state.update_data({'last_name': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.region)
async def register(message: Message, state: FSMContext):
    await message.answer('Tuman/Shaharingizni kiriting')
    await state.update_data({'region': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.city)
async def register(message: Message, state: FSMContext):
    await message.answer('Tashkilot nomini kiriting')
    await state.update_data({'city': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.org_name)
async def register(message: Message, state: FSMContext):
    await message.answer(
        "Barcha ma'lumotlaringiz xavfsizligi uchun parol kiriting.\n"
        "<i>Parol uzunligi 4 - 6 xonali bo'lishi lozim</i>")
    await state.update_data(
        {'org_name': message.text})
    await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.password1)
async def register(message: Message, state: FSMContext):
    password = message.text
    if len(password) > 6 or len(password) < 4:
        await message.answer(
            "<b>Parol to'g'ri emas.</b>\n"
            "Qayta kiriting")
    else:
        await message.answer("Parolni tastiqlang")
        await state.update_data({'password': password})
        await UserRegisterState.next()


@dp.message_handler(state=UserRegisterState.password2)
async def register(message: Message, state: FSMContext):
    password2 = message.text
    data = await state.get_data()
    if password2 == data.get('password'):
        await message.answer(
            f"{makeup_user_info(data)}\n\n"
            f"Barcha ma'lumotlar to'g'rimi?",
            reply_markup=default.yes_no_buttons
        )
        await UserRegisterState.next()
    else:
        await message.answer('Parollar mos kelmadi, qayta kiriting')
        await UserRegisterState.password1.set()


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
