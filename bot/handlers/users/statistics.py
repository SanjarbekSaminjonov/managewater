import logging
from aiogram.types import CallbackQuery

from loader import dp, db
from utils.local_services.basins import makeup_basin_info, makeup_basin_message_info
from keyboards import inline


@dp.callback_query_handler(inline.basin_statistics_callback.filter(action="back_to_manage_basin"))
async def back_to_manage_basin(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    basin = await db.get_basin_by_id(basin_id)
    text = makeup_basin_info(basin)
    await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id))


@dp.callback_query_handler(inline.basin_statistics_callback.filter(action="last_message"))
async def basin_statistics_last_message(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    basin = await db.get_basin_by_id(basin_id)
    basin_message = await db.get_basin_last_message(basin_id)
    if bool(basin_message):
        text = makeup_basin_message_info(basin, basin_message)
        await call.message.edit_text(text, reply_markup=inline.back_to_statistics_types(basin_id))
    else:
        await call.answer("Ma'lumotlar yo'q", show_alert=True)


@dp.callback_query_handler(inline.back_to_statistics_callback.filter(action="back_to_statistics"))
async def back_to_statistics(call: CallbackQuery):
    basin_id = call.data.split(':')[-1]
    basin = await db.get_basin_by_id(basin_id)
    text = makeup_basin_info(basin)
    await call.message.edit_text(text, reply_markup=inline.statistics_types(basin_id))
