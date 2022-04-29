from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import backend_services
from utils.local_services.basins import makeup_basin_info
from keyboards import default
from states.basin import BasinCreateState


@dp.message_handler(text_contains="Bekor qilish", state=BasinCreateState.all_states)
async def cancel_adding_basin(message: Message, state: FSMContext):
    await message.answer("Qurilma qo'shish bekor qilindi", reply_markup=default.home_sections)
    await state.finish()


@dp.message_handler(text_contains="Qurilma qo'shish")
async def add_basin(message: Message):
    await message.answer("Qurilma 'id' sini kiriting (11 xonali)", reply_markup=default.cancel)
    await BasinCreateState.id.set()


@dp.message_handler(state=BasinCreateState.id)
async def add_basin(message: Message, state: FSMContext):
    if len(message.text) == 11:
        await message.answer("Qurilmadagi telefon raqamni kiriting")
        await BasinCreateState.next()
        await state.update_data({'id': message.text})
    else:
        await message.answer("Kiritilgan id 11 xonali emas. Qayta urining")


@dp.message_handler(state=BasinCreateState.phone)
async def add_basin(message: Message, state: FSMContext):
    await message.answer("Qurilmaga ism o'ylab toping")
    await BasinCreateState.next()
    await state.update_data({'phone': message.text})


@dp.message_handler(state=BasinCreateState.name)
async def add_basin(message: Message, state: FSMContext):
    await message.answer("Qurilmaning balandligini kiriting (santimetr)")
    await BasinCreateState.next()
    await state.update_data({'name': message.text})


@dp.message_handler(state=BasinCreateState.height)
async def add_basin(message: Message, state: FSMContext):
    try:
        _ = float(message.text)
        await message.answer("Qurilmaning joylashuvini kiriting", reply_markup=default.location)
        await BasinCreateState.next()
        await state.update_data({'height': message.text})
    except Exception as err:
        await message.reply("Balandlik noto'g'ri kiritildi")


@dp.message_handler(state=BasinCreateState.location, text_contains="O'tkazib yuborish")
async def add_basin(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"{makeup_basin_info(data)}\n\n"
        "Qurilma ma'lumotlar to'g'rimi?",
        reply_markup=default.yes_no_buttons
    )
    await BasinCreateState.next()


@dp.message_handler(state=BasinCreateState.location, content_types='location')
async def add_basin(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"{makeup_basin_info(data)}\n\n"
        "Qurilma ma'lumotlar to'g'rimi?",
        reply_markup=default.yes_no_buttons
    )
    await state.update_data({
        'latitude': message.location.latitude,
        'longitude': message.location.longitude
    })
    await BasinCreateState.next()


@dp.message_handler(text_contains="Ha", state=BasinCreateState.save_basin)
async def add_basin(message: Message, state: FSMContext):
    await message.answer(
        "Qurilma qurilma ma'lumotlari saqlanmoqda . . .",
        reply_markup=default.home_sections
    )
    data = await state.get_data()
    await state.finish()
    user = db.select_user(chat_id=message.from_user.id)
    resp = await backend_services.basins.add_basin(user=user, data=data)
    if resp:
        await message.answer("Jarayon yakunlandi.")
    else:
        await message.answer("Ma'lumotlarni saqlashda xatolik yuz berdi")


@dp.message_handler(text_contains="Ha", state=BasinCreateState.save_basin)
async def add_basin(message: Message, state: FSMContext):
    await message.answer(
        "Qurilma qo'shish bekor qilindi",
        reply_markup=default.home_sections
    )
    await state.finish()