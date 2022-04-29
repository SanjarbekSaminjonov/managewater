from aiogram import types
from aiogram import dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards import default
from states.users import UserLoginRegisterState


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: dispatcher.FSMContext):
    await state.finish()
    user_state = db.select_user(chat_id=message.from_user.id)
    if user_state is None:
        await message.answer(
            f"🙋‍♂️ Salom {message.from_user.full_name} xush kelibsiz. \n\n"
            f"<i>Siz bizning xizmatdan birinchi marta foydalanmoqdasiz."
            f"Shuning uchun ro'yxatdan o'tishingiz yoki o'zingizning "
            f"akkauntingizga kirishingiz kerak bo'ladi</i>",
            reply_markup=default.login_register_confirm
        )
        await UserLoginRegisterState.login_register.set()
    else:
        await message.answer(
            f"🙋‍♂️ Salom yana ko'rishganimizdan xursandman!",
            reply_markup=default.home_sections
        )
