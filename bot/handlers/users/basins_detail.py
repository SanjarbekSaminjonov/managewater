import logging
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import backend_services, local_services
from keyboards import inline


@dp.message_handler(text_contains="Mening qurilmalarim")
async def list_basins(message: Message, state: FSMContext):
    msg = await message.answer("Ma'lumotlar olinmoqda . . .")
    user = db.select_user(chat_id=message.from_user.id)
    try:
        basins = await local_services.basins.get_list_of_basins(user=user, state=state)
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
    user = db.select_user(chat_id=call.from_user.id)
    basin = await local_services.basins.get_basin_by_id(
        user=user, basin_id=basin_id, state=state)
    if bool(basin):
        text = local_services.basins.makeup_basin_info(basin)
        await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id=basin_id))
    else:
        await call.message.edit_text("Ushbu qurilma topilmadi")
    await call.answer(cache_time=1)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="update_height"))
async def update_basin_height(call: CallbackQuery, state: FSMContext):
    basin_id = call.data.split(':')[-1]
    user = db.select_user(chat_id=call.from_user.id)
    basin = await local_services.basins.get_basin_by_id(
        user=user, basin_id=basin_id, state=state)
    basin_height = basin.get('height')
    await state.update_data({basin_id: basin_height})
    await call.message.edit_reply_markup(inline.update_height_plus_minus(basin_id))
    await call.answer(cache_time=1)


@dp.callback_query_handler(inline.basin_update_height_callback.filter(sep="update_height"))
async def update_basin_height(call: CallbackQuery, state: FSMContext):
    data = call.data.split(':')
    basin_id = data[-2]
    value = data[-1]
    if value == "save":
        pass
    elif value == "cancel":
        user = db.select_user(chat_id=call.from_user.id)
        basin = await local_services.basins.get_basin_by_id(
            user=user, basin_id=basin_id, state=state)
        if bool(basin):
            text = local_services.basins.makeup_basin_info(basin)
            await call.message.edit_text(text, reply_markup=inline.manage_basin(basin_id=basin_id))
    else:
        try:
            user = db.select_user(chat_id=call.from_user.id)
            basin = await local_services.basins.get_basin_by_id(
                user=user, basin_id=basin_id, state=state)
            if bool(basin):
                data = await state.get_data()
                if data.get(basin_id) is not None:
                    basin_height = data.get(basin_id)
                else:
                    basin_height = basin.get('height')
                    await state.update_data({basin_id: basin_height})
                basin_height = float(basin_height) + int(value)
                basin['height'] = basin_height
                await state.update_data({basin_id: basin_height})
                await call.message.edit_text(
                    local_services.basins.makeup_basin_info(basin),
                    reply_markup=inline.update_height_plus_minus(basin_id))
        except Exception as err:
            print(err)


# @dp.message_handler(state=BasinUpdate.set_height)
# async def update_basin_height(message: Message, state: FSMContext):
#     user = db.select_user(chat_id=message.from_user.id)
#     msg = await message.answer("Balandlik sozlanmoqda . . .")
#     try:
#         _ = float(message.text)
#         data = await state.get_data()
#         basin_id = data.get('current_basin_id')
#         resp = await backend_services.basins.set_basin_height(
#             user=user, basin_id=basin_id, data={'height': message.text})
#         if bool(resp):
#             text = local_services.basins.makeup_basin_info(resp)
#             await msg.edit_text(text)
#             await msg.edit_reply_markup(inline.manage_basin(basin_id=basin_id))
#     except Exception as err:
#         await msg.edit_text("Ma'lumotlarni saqlashda xatolik yuz berdi.")
#         logging.error(err)
#     await state.finish()


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="location"))
async def basin_location(call: CallbackQuery, state: FSMContext):
    basin_id = call.data.split(':')[-1]
    user = db.select_user(chat_id=call.from_user.id)
    basin = await local_services.basins.get_basin_by_id(
        user=user, basin_id=basin_id, state=state)
    if bool(basin) and bool(basin.get('latitude')) and bool(basin.get('longitude')):
        await call.message.answer_location(
            latitude=float(basin.get('latitude')),
            longitude=float(basin.get('longitude')))
    else:
        await call.message.answer("Joylashuv ma'lumotlari topilmadi.")
    await call.answer(cache_time=2)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="back_to_basins"))
async def back_to_basins_list(call: CallbackQuery, state: FSMContext):
    user = db.select_user(chat_id=call.from_user.id)
    try:
        basins = await local_services.basins.get_list_of_basins(user=user, state=state)
        if len(basins):
            await call.message.edit_text(
                "Sizdagi qurilmalar ro'yxati", reply_markup=inline.list_of_basins(basins))
        else:
            await call.message.edit_text("Sizda ro'yxatdan qurilmalar yo'q")
    except Exception as err:
        logging.error(err)
        await call.message.edit_text("Ma'lumotlani olishning imkoni bo'lmadi")
