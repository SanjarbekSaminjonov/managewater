from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.local_services.users import makeup_user_info
from keyboards import default
from states.users import UserLoginState


@dp.message_handler(text_contains="Bekor qilish", state=UserLoginState.all_states)
async def cancel_login_register(message: Message, state: FSMContext):
    await message.answer("Hisobga kirish bekor qilindi", reply_markup=default.login_register_confirm)
    await state.finish()


@dp.message_handler(text_contains="Eski akkauntimga kirish", state='*')
async def login(message: Message):
    await message.answer(
        "📝 Eski hisobni tiklash uchun maxfiy kodni kiriting",
        reply_markup=default.register_confirm
    )
    await UserLoginState.secret_key.set()


@dp.message_handler(state=UserLoginState.secret_key)
async def login(message: Message, state: FSMContext):
    secret_key = message.text
    f_msg = await message.answer('Jarayon bajarilmoqda ...')
    res = change_username(secret_key=secret_key, chat_id=message.from_user.id)
    await f_msg.delete()
    if res.get('is_done'):
        data = res.get('data')
        await message.answer(makeup_user_info(data))
        secret_key = f"{data.get('id')}#{message.from_user.id}"
        l_msg = await message.answer(
            f"Jarayon yakunlandi.\n"
            f"<b><code>{secret_key}</code></b> - maxfiy kod o'rgartirildi. Uni hech kimga bermang\n."
            f"U orqali boshqa qurilmadan hisobingizga kirishizgiz mumkin.",
            reply_markup=default.home_sections
        )
        await bot.pin_chat_message(message.from_user.id, l_msg.message_id, disable_notification=True)
    else:
        await message.answer(
            f"Jarayon yakunlanmadi, iltimos qayta urinib ko'ring.",
            reply_markup=default.login_register_confirm
        )
    await state.finish()
