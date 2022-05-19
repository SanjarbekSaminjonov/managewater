import datetime


def makeup_basin_info_pre_save(data) -> str:
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data.get('name')}</b>\n\n"
    text += f"🟢 Qurilma id si: <b>{data.get('id')}</b>\n\n"
    text += f"🟡 Telefon raqami: <b>{data.get('phone')}</b>\n\n"
    text += f"🔴 Balandlik: <b>{data.get('height')} sm</b>\n\n"
    return text


def makeup_basin_info(data) -> str:
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data[2]}</b>\n\n"
    text += f"🟢 Qurilma id si: <b>{data[0]}</b>\n\n"
    text += f"🟡 Telefon raqami: <b>{data[1]}</b>\n\n"
    text += f"🔴 Balandlik: <b>{data[3]} sm</b>\n\n"
    text += f"⚪ Balandlik sozlamasi: <b>{data[7]} sm</b>\n"
    return text


def makeup_basin_message_info(basin, basin_message) -> str:
    dt = basin_message[10] + datetime.timedelta(hours=5)
    dt = dt.strftime("%H:%M | %d.%m.%Y")
    text = str()
    text += f"🔵 Qurilma nomi: <b>{basin[2]}</b>\n\n"
    text += f"-- Suvdan balandligi: <b>{basin_message[1]}</b>\n"
    text += f"-- Suv sathidan balandligi: <b>{basin_message[2]}</b>\n"
    text += f"-- O'tayotgan suv miqdori: <b>{basin_message[3]} litr/sekund</b>\n"
    text += f"-- O'tayotgan suv miqdori: <b>{basin_message[4]} metr kub/soat</b>\n"
    text += f"-- Jami o'tgan suv miqdori: <b>{int(basin_message[5])} metr kub</b>\n"
    text += f"-- Batareya quvvati: <b>{basin_message[6]} volt</b>\n"
    text += f"-- Tarmoq ko'rsatkichi: <b>{basin_message[7]} volt</b>\n"
    text += f"-- Xabar vaqti: <b>{dt}</b>\n"

    return text
