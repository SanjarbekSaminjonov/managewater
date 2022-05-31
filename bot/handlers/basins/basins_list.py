import logging
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.users import UserLoginRegisterState
from utils import local_services
from keyboards import inline, default
from data.config import ADMINS


@dp.message_handler(text_contains="Mening qurilmalarim")
async def list_basins(message: Message, state: FSMContext):
    user = await db.get_user(chat_id=str(message.from_user.id))
    if user is None:
        await message.answer(
            f"🙋‍♂️ Xurmatli {message.from_user.full_name}. \n\n"
            f"<i>Siz botda ro'yxatdan o'tmagansiz.\n"
            f"Shuning uchun ro'yxatdan o'tishingiz kerak bo'ladi </i>",
            reply_markup=default.login_register_confirm
        )
        await UserLoginRegisterState.login_register.set()
        await message.delete()
        await state.reset_data()
    else:
        msg = await message.answer("Ma'lumotlar olinmoqda . . .")
        if str(message.from_user.id) in ADMINS:
            try:
                basins = await db.get_basins()
                buttons = await inline.list_of_basins_for_admin(basins)
                if len(basins):
                    await msg.edit_text(
                        "Barcha qurilmalar ro'yxati", reply_markup=buttons)
                else:
                    await msg.edit_text("Ro'yxatdan qurilmalar yo'q")
            except Exception as err:
                logging.error(err)
                await msg.edit_text("Ma'lumotlani olishning imkoni bo'lmadi")
        else:
            try:
                user = await db.get_user(chat_id=str(message.from_user.id))
                basins = await db.get_user_basins(user[0])
                watched_basins = await db.get_watched_basins_by_user(user[0])
                for watched_basin in watched_basins:
                    basin = await db.get_basin_by_id(watched_basin[1])
                    basins.append(basin)
                if len(basins):
                    await msg.edit_text(
                        "Sizdagi qurilmalar ro'yxati", reply_markup=inline.list_of_basins(basins))
                else:
                    await msg.edit_text("Sizda ro'yxatdan qurilmalar yo'q")
            except Exception as err:
                logging.error(err)
                await msg.edit_text("Ma'lumotlani olishning imkoni bo'lmadi")


@dp.callback_query_handler(inline.basins_list_callback.filter(sep="basin"))
async def select_basin(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    basin = await db.get_basin_by_id(basin_id)
    if bool(basin):
        text = local_services.basins.makeup_basin_info(basin)
        await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id))
    else:
        await call.message.edit_text("Ushbu qurilma topilmadi")
    await call.answer(cache_time=1)
