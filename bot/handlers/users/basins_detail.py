import logging
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import backend_services, local_services
from keyboards import inline
from states.basin import BasinUpdate


@dp.message_handler(text_contains="Mening qurilmalarim")
async def list_basins(message: Message, state: FSMContext):
    msg = await message.answer("Ma'lumotlar olinmoqda . . .")
    user = db.select_user(chat_id=message.from_user.id)
    try:
        basins = await local_services.basins.get_list_of_basins(user=user, state=state)
        if len(basins):
            await msg.edit_text("Sizdagi qurilmalar ro'yxati")
            await msg.edit_reply_markup(reply_markup=inline.list_of_basins(basins))
        else:
            await message.answer("Sizda ro'yxatdan qurilmalar yo'q")
    except Exception as err:
        logging.error(err)
        await message.answer("Ma'lumotlani olishning imkoni bo'lmadi")


@dp.callback_query_handler(inline.basins_list_callback.filter(sep="basin"))
async def select_basin(call: CallbackQuery, state: FSMContext):
    basin_id = call.data.split(':')[-1]
    user = db.select_user(chat_id=call.message.from_user.id)
    basin = await local_services.basins.get_basin_by_id(
        user=user, basin_id=basin_id, state=state)
    if bool(basin):
        text = local_services.basins.makeup_basin_info(basin)
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(inline.manage_basin(basin_id=basin_id))
    else:
        await call.message.edit_text("Ushbu qurilma topilmadi")
    await call.answer(cache_time=60)


@dp.callback_query_handler(inline.basin_manage_callback.filter(action="update_height"))
async def update_basin_height(call: CallbackQuery, state: FSMContext):
    basin_id = call.data.split(':')[-1]
    await state.update_data({'current_basin_id': basin_id})
    await call.message.answer("Balandlikni kiriting (sm)")
    await BasinUpdate.set_height.set()
    await call.answer(cache_time=60)


@dp.message_handler(state=BasinUpdate.set_height)
async def update_basin_height(message: Message, state: FSMContext):
    user = db.select_user(chat_id=message.from_user.id)
    msg = await message.answer("Balandlik sozlanmoqda . . .")
    try:
        _ = float(message.text)
        data = await state.get_data()
        basin_id = data.get('current_basin_id')
        resp = await backend_services.basins.set_basin_height(
            user=user, basin_id=basin_id, data={'height': message.text})
        if bool(resp):
            text = local_services.basins.makeup_basin_info(resp)
            await msg.edit_text(text)
            await msg.edit_reply_markup(inline.manage_basin(basin_id=basin_id))
            await state.finish()
    except Exception as err:
        await message.answer("Ma'lumotlarni saqlashda xatolik yuz berdi.")
        logging.error(err)
