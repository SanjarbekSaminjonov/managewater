import logging
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from utils import local_services
from keyboards import inline
from data.config import ADMINS


@dp.message_handler(text_contains="Mening qurilmalarim")
async def list_basins(message: Message):
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
