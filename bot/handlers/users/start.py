from cgitb import text
from aiogram import types
from aiogram import dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards import default
from states.users import UserLoginRegisterState


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: dispatcher.FSMContext):
    await state.finish()
    await state.reset_data()
    user = await db.get_user(chat_id=str(message.from_user.id))
    if user is None:
        msg_text = f"🙋‍♂️ Salom {message.from_user.full_name} xush kelibsiz. \n\n"
        msg_text += f"<i>Siz bizning xizmatdan birinchi marta foydalanmoqdasiz. "
        msg_text += f"Shuning uchun ro'yxatdan o'tishingiz kerak bo'ladi</i>"
        await message.answer(
            text=msg_text,
            reply_markup=default.login_register_confirm
        )
        await UserLoginRegisterState.login_register.set()
    else:
        await message.answer(
            f"🙋‍♂️ Salom {user[6]} {user[5]} yana ko'rishganimizdan xursandman!",
            reply_markup=default.home_sections
        )
