from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.backend_services.users import create, is_already_user
from utils.local_services.users import makeup_user_info
from keyboards import default
from states.users import UserRegisterState


@dp.message_handler(text_contains="Bekor qilish", state='*')
async def cancel_login_register(message: Message, state: FSMContext):
    await message.answer("Bekor qilindi", reply_markup=default.login_register_confirm)
    await state.finish()
    res = await is_already_user(message.from_user.id)
    if res.get('is_done'):
        await message.answer("Siz allqachon ro'yhatdan o'tgansiz", reply_markup=default.home_sections)


@dp.message_handler(text_contains="Ro'yxatdan o'tish", state='*')
async def register(message: Message):
    await message.answer(
        "📝 Ro'yxatga olish boshlandi \nIsmingizni kiriting",
        reply_markup=default.login_confirm
    )
    await UserRegisterState.first_name.set()


@dp.message_handler(state=UserRegisterState.first_name)
async def register(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data({'first_name': first_name})
    await message.answer('Familiyangizni kiriting')
    await UserRegisterState.last_name.set()


@dp.message_handler(state=UserRegisterState.last_name)
async def register(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data({'last_name': last_name})
    await message.answer('Viloyat/Shaharingizni kiriting')
    await UserRegisterState.region.set()


@dp.message_handler(state=UserRegisterState.region)
async def register(message: Message, state: FSMContext):
    region = message.text
    await state.update_data({'region': region})
    await message.answer('Tuman/Shaharingizni kiriting')
    await UserRegisterState.city.set()


@dp.message_handler(state=UserRegisterState.city)
async def register(message: Message, state: FSMContext):
    city = message.text
    await state.update_data({'city': city})
    await message.answer('Tashkilot nomini kiriting')
    await UserRegisterState.org_name.set()


@dp.message_handler(state=UserRegisterState.org_name)
async def register(message: Message, state: FSMContext):
    org_name = message.text
    await state.update_data({'org_name': org_name})
    data = await state.get_data()
    await message.answer(
        f"{makeup_user_info(data)}\n\n"
        f"Barcha ma'lumotlar to'g'rimi?",
        reply_markup=default.yes_no_buttons
    )
    await UserRegisterState.save_user.set()


@dp.message_handler(state=UserRegisterState.save_user, text_contains="Ha")
async def register(message: Message, state: FSMContext):
    f_msg = await message.answer("Ma'lumotlar saqlanmoqda ...", reply_markup=None)
    data = await state.get_data()
    res = create(chat_id=message.from_user.id, data=data)
    await f_msg.delete()
    if res.get('is_done'):
        secret_key = f"{res.get('data').get('id')}#{message.from_user.id}"
        l_msg = await message.answer(
            f"Ma'lumotlar saqlandi.\n"
            f"<b><code>{secret_key}</code></b> - sizning maxfiy kodingiz. Uni hech kimga bermang\n."
            f"U orqali boshqa qurilmadan hisobingizga kirishizgiz mumkin.",
            reply_markup=default.home_sections
        )
        await bot.pin_chat_message(message.from_user.id, l_msg.message_id, disable_notification=True)
    else:
        await message.answer(
            f"Ma'lumotlarni saqlashda muammo bor, iltimos qayta urinib ko'ring.",
            reply_markup=default.login_register_confirm
        )
    await state.finish()


@dp.message_handler(state=UserRegisterState.save_user, text_contains="Yo'q")
async def register(message: Message):
    await message.answer(
        "Jarayon tugatildi, qayta harakat qiling.",
        reply_markup=default.login_register_confirm
    )
