from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.backend_services import users
from keyboards import default


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    f_msg = await message.answer(
        f"Salom, {message.from_user.full_name}, "
        f"biz sizni bazadan tekshirmoqdamiz ..."
    )
    user_state = await users.is_already_user(message.from_user.id)
    if user_state.get('is_done'):
        data = user_state.get('data')
        await message.answer(
            f"Salom {data.get('first_name')} {data.get('last_name')}\n"
            f"sizga yana xizmat ko'rsatishdan mamnunmiz",
            reply_markup=default.home_sections
        )
        await f_msg.delete()
    else:
        await message.answer(
            f"Siz botda yangisiz, foydalanish uchun ro'yxatdan o'tishigiz kerak, "
            f"yoki boshqa telegram akkauntdagi hisobingizga kirishingiz mumkin.",
            reply_markup=default.login_register_confirm
        )
