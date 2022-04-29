from aiogram import types

from loader import dp
from keyboards import default


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Dastur yangilandi", reply_markup=default.home_sections)
    await message.delete()
