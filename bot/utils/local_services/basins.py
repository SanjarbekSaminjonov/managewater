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
    text = str()

    bat = basin_message[6]
    bat = round((bat - 3.70) / 0.42 * 100)
    dt = basin_message[10] + datetime.timedelta(hours=5)
    dt = dt.strftime("%H:%M | %d.%m.%Y")

    text += f"🔵 Qurilma nomi: <b>{basin[2]}</b>\n\n"
    text += f"📏  Suvdan qurilma balandligi: <b>{basin_message[1]} sm</b>\n"
    text += f"📏  Suv sathidan balandligi: <b>{basin_message[2]} sm</b>\n"
    text += f"🌊  O'tayotgan suv miqdori: <b>{basin_message[3]} litr/sekund</b>\n"
    text += f"🌊  O'tayotgan suv miqdori: <b>{basin_message[4]} m³/soat</b>\n"
    text += f"📈  Jami o'tayotgan suv miqdori: <b>{int(basin_message[5])} m³</b>\n"
    text += f"🔋  Batareya quvvati: <b>{bat} %</b>\n"
    text += f"📡  GPRS Antena kuchi: <b>{basin_message[7]} net</b>\n"
    text += f"📆  So'ngi o'lchangan vaqti <b>{dt}</b>\n"

    return text
