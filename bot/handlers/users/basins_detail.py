from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import backend_services
from states.basin import BasinsData
from keyboards import inline


@dp.message_handler(text_contains="Mening qurilmalarim")
async def list_basins(message: Message, state: FSMContext):
    msg = await message.answer("Ma'lumotlar olinmoqda . . .")
    user = db.select_user(chat_id=message.from_user.id)
    basins = await backend_services.basins.get_basins_list(user=user)
    await msg.delete()
    if len(basins):
        await message.answer(
            "Sizdagi qurilmalar ro'yxati",
            reply_markup=inline.list_of_basins(basins_list=basins)
        )
        await BasinsData.list.set()
        await state.update_data({'basins': basins})
    else:
        await message.answer("Sizda ro'yxatdan qurilmalar yo'q")
