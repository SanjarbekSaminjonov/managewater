import logging
from aiogram.types import CallbackQuery

from loader import dp, db
from utils import local_services
from keyboards import inline


@dp.callback_query_handler(inline.basin_update_height_callback.filter(sep="update_height"))
async def update_basin_height(call: CallbackQuery):
    data = call.data.split(':')
    basin_id = data[-2]
    value = data[-1]
    basin = await db.get_basin_by_id(basin_id)
    if bool(basin):
        if value == "ok":
            try:
                text = local_services.basins.makeup_basin_info(basin)
                await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id))
            except Exception as err:
                logging.error(err)
                await call.message.edit_reply_markup(inline.manage_basin(basin_id))
        elif value == "1" or value == "-1":
            conf_height = basin[7] + int(value)
            await db.update_basin_conf_height(basin_id, conf_height)
            new_basin = await db.get_basin_by_id(basin_id)
            try:
                await call.message.edit_text(
                    local_services.basins.makeup_basin_info(new_basin),
                    reply_markup=inline.update_height_plus_minus(basin_id))
            except Exception as err:
                logging.error(err)
                await call.message.delete()
                await call.message.answer(
                    local_services.basins.makeup_basin_info(new_basin),
                    reply_markup=inline.update_height_plus_minus(basin_id)
                )
