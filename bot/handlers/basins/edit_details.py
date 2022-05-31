from aiogram.types import CallbackQuery

from loader import dp, db
from keyboards import inline
from utils.local_services.basins import makeup_basin_info


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="edit_name"))
async def edit_details(call: CallbackQuery):
    # data = call.data.split(':')
    # basin_id = data[-1]
    await call.answer("Tez orada ushbu imkoniyat qo'shiladi", show_alert=True)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="edit_phone"))
async def edit_details(call: CallbackQuery):
    # data = call.data.split(':')
    # basin_id = data[-1]
    await call.answer("Tez orada ushbu imkoniyat qo'shiladi", show_alert=True)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="delete"))
async def edit_details(call: CallbackQuery):
    # data = call.data.split(':')
    # basin_id = data[-1]
    await call.answer("Tez orada ushbu imkoniyat qo'shiladi", show_alert=True)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="back"))
async def edit_details(call: CallbackQuery):
    data = call.data.split(':')
    basin_id = data[-1]
    basin = await db.get_basin_by_id(basin_id)
    await call.message.edit_text(
        makeup_basin_info(basin),
        reply_markup=inline.manage_basin(basin_id)
    )
