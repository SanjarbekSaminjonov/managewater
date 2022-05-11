from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import dp, db
from keyboards import default
from states.users import UserLoginRegisterState


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    user_state = db.select_user(chat_id=message.from_user.id)
    if user_state is None:
        await message.answer(
            f"🙋‍♂️ Xurmatli {message.from_user.full_name}. \n\n"
            f"<i>Siz botda ro'yxatdan o'tmagansiz.\n"
            f"Shuning uchun ro'yxatdan o'tishingiz yoki o'zingizning "
            f"akkauntingizga kirishingiz kerak bo'ladi</i>",
            reply_markup=default.login_register_confirm
        )
        await UserLoginRegisterState.login_register.set()
    else:
        await message.answer("Quyidagi bo'limlardan birini tanlang", reply_markup=default.home_sections)
    await message.delete()
    await state.reset_data()
