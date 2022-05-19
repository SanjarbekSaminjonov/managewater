import logging
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils import local_services
from utils.local_services.basins import makeup_basin_info_pre_save
from keyboards import default
from states.basin import BasinCreateState


@dp.message_handler(text_contains="Bekor qilish", state=BasinCreateState.all_states)
async def cancel_adding_basin(message: Message, state: FSMContext):
    await message.answer(
        "Qurilma qo'shish bekor qilindi",
        reply_markup=default.home_sections
    )
    await state.reset_data()
    await state.finish()


@dp.message_handler(text_contains="Qurilma qo'shish")
async def add_basin(message: Message):
    await BasinCreateState.id.set()
    await message.answer(
        "Qurilma 'id' sini kiriting (11 xonali)",
        reply_markup=default.cancel
    )


@dp.message_handler(state=BasinCreateState.id)
async def add_basin(message: Message, state: FSMContext):
    basin_id = message.text
    if len(basin_id) == 11:
        basin_is_exist = await db.check_basin_is_exist(basin_id)
        if basin_is_exist is not None:
            basin = await db.get_basin_by_id(basin_id)
            if basin is not None:
                await message.answer(
                    "Bu qurilma allaqachon ro'yxatdan o'tgan.\nQayta kiriting",
                    reply_markup=default.cancel
                )
            else:
                await message.answer(
                    "Qurilmadagi telefon raqamni kiriting\n" +
                    "Mison uchun: <b>+998*****7777</b>")
                await state.update_data({'id': message.text})
                await BasinCreateState.next()
        else:
            await message.answer(
                "Qurilma 'id' si noto'g'ri kiritildi.\nBunday qurilma mavjud emas. Qayta kiriting",
                reply_markup=default.cancel
            )
    else:
        await message.answer("Kiritilgan id 11 xonali emas.\nQayta kiriting")


@dp.message_handler(state=BasinCreateState.phone)
async def add_basin(message: Message, state: FSMContext):
    phone_number = message.text
    if len(phone_number) == 13 and phone_number.startswith("+998") and phone_number[1:].isdigit():
        await BasinCreateState.next()
        await message.answer("Qurilmaga nom bering")
        await state.update_data({'phone': phone_number})
    else:
        await message.answer("Telefon noto'g'ri kiritildi.\nIltimos ko'rsatilgan tartibda kiriting")


@dp.message_handler(state=BasinCreateState.name)
async def add_basin(message: Message, state: FSMContext):
    await message.answer("Qurilmaning standart balandligini kiriting (santimetr)")
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


@dp.message_handler(state=BasinCreateState.location, text_contains="Tashlab ketish")
async def add_basin(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"{makeup_basin_info_pre_save(data)}\n\n"
        "Qurilma ma'lumotlar to'g'rimi?",
        reply_markup=default.yes_no_buttons
    )
    await BasinCreateState.next()


@dp.message_handler(state=BasinCreateState.location, content_types='location')
async def add_basin(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"{makeup_basin_info_pre_save(data)}\n\n"
        "Qurilma ma'lumotlar to'g'rimi?",
        reply_markup=default.yes_no_buttons
    )
    await state.update_data({
        "latitude": message.location.latitude,
        "longitude": message.location.longitude
    })
    await BasinCreateState.next()


@dp.message_handler(text_contains="Ha", state=BasinCreateState.save_basin)
async def add_basin(message: Message, state: FSMContext):
    msg = await message.answer(
        "Qurilma qurilma ma'lumotlari saqlanmoqda . . ."
    )
    data = await state.get_data()
    try:
        await msg.delete()
        user = await db.get_user(chat_id=str(message.from_user.id))
        data['belong_to_id'] = user[0]
        await db.add_basin(data)
        await message.answer("Qurilma muvaffaqiyatli qo'shildi", reply_markup=default.home_sections)
    except Exception as err:
        logging.error(err)
        await message.answer(
            "Ma'lumotlarni saqlashda xatolik yuz berdi", reply_markup=default.home_sections)
    await state.finish()


@dp.message_handler(text_contains="Ha", state=BasinCreateState.save_basin)
async def add_basin(message: Message, state: FSMContext):
    await message.answer(
        "Qurilma qo'shish bekor qilindi",
        reply_markup=default.home_sections
    )
    await state.finish()
