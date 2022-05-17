import logging
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import local_services
from keyboards import inline


@dp.message_handler(text_contains="Mening qurilmalarim")
async def list_basins(message: Message):
    msg = await message.answer("Ma'lumotlar olinmoqda . . .")
    user = await db.get_user(chat_id=str(message.from_user.id))
    try:
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
async def select_basin(call: CallbackQuery, state: FSMContext):
    basin_id = call.data.split(':')[-1]
    basin = await db.get_basin_by_id(basin_id)
    if bool(basin):
        text = local_services.basins.makeup_basin_info(basin)
        await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id))
    else:
        await call.message.edit_text("Ushbu qurilma topilmadi")
    await call.answer(cache_time=1)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="update_height"))
async def update_basin_height(call: CallbackQuery, state: FSMContext):
    basin_id = call.data.split(':')[-1]
    await call.message.edit_reply_markup(inline.update_height_plus_minus(basin_id))
    await call.answer(cache_time=1)


@dp.callback_query_handler(inline.basin_update_height_callback.filter(sep="update_height"))
async def update_basin_height(call: CallbackQuery, state: FSMContext):
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
                await call.message.delete()
                text = local_services.basins.makeup_basin_info(basin)
                await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id))
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
                    reply_markup=inline.update_height_plus_minus(basin_id))


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="location"))
async def basin_location(call: CallbackQuery, state: FSMContext):
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
async def back_to_basins_list(call: CallbackQuery, state: FSMContext):
    user = await db.get_user(chat_id=str(call.from_user.id))
    basins = await db.get_user_basins(user[0])
    try:
        if len(basins):
            await call.message.edit_text(
                "Sizdagi qurilmalar ro'yxati", reply_markup=inline.list_of_basins(basins))
        else:
            await call.message.edit_text("Sizda ro'yxatdan qurilmalar yo'q")
    except Exception as err:
        logging.error(err)
        await call.message.edit_text("Ma'lumotlani olishning imkoni bo'lmadi")
