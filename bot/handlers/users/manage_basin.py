import logging
from aiogram.types import CallbackQuery

from loader import dp, db
from keyboards import inline
from data.config import ADMINS


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="update_height"))
async def update_basin_height(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    await call.message.edit_reply_markup(inline.update_height_plus_minus(basin_id))
    await call.answer(cache_time=1)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="statistics"))
async def basin_statistics(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    await call.message.edit_reply_markup(inline.statistics_types(basin_id))
    await call.answer(cache_time=1)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="location"))
async def basin_location(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    basin = await db.get_basin_by_id(basin_id)
    if bool(basin) and bool(basin[4]) and bool(basin[5]):
        try:
            await call.message.answer_location(
                latitude=float(basin[4]), longitude=float(basin[5]))
        except Exception as err:
            logging.error(err)
            await call.answer("Qurilma joylashuvi noto'g'ri kiritilgan", show_alert=True)
    else:
        await call.answer("Qurilma joylashuvi kiritilmagan", show_alert=True)
    await call.answer(cache_time=2)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="back_to_basins"))
async def back_to_basins_list(call: CallbackQuery):
    if str(call.from_user.id) in ADMINS:
        try:
            basins = await db.get_basins()
            buttons = await inline.list_of_basins_for_admin(basins)
            if len(basins):
                await call.message.edit_text(
                    "Barcha qurilmalar ro'yxati", reply_markup=buttons)
            else:
                await call.message.edit_text("Ro'yxatdan qurilmalar yo'q")
        except Exception as err:
            logging.error(err)
            await call.message.edit_text("Ma'lumotlani olishning imkoni bo'lmadi")
    else:
        try:
            user = await db.get_user(chat_id=str(call.from_user.id))
            basins = await db.get_user_basins(user[0])
            watched_basins = await db.get_watched_basins_by_user(user[0])
            for watched_basin in watched_basins:
                basin = await db.get_basin_by_id(watched_basin[1])
                basins.append(basin)
            if len(basins):
                await call.message.edit_text(
                    "Sizdagi qurilmalar ro'yxati", reply_markup=inline.list_of_basins(basins))
            else:
                await call.message.edit_text("Sizda ro'yxatdan qurilmalar yo'q")
        except Exception as err:
            logging.error(err)
            await call.message.edit_text("Ma'lumotlani olishning imkoni bo'lmadi")
    await call.answer(cache_time=2)
