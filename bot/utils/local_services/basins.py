import datetime


def makeup_basin_info_pre_save(data) -> str:
    text = str()
    text += f"ðµ Qurilma nomi: <b>{data.get('name')}</b>\n\n"
    text += f"ð¢ Qurilma id si: <b>{data.get('id')}</b>\n\n"
    text += f"ð¡ Telefon raqami: <b>{data.get('phone')}</b>\n\n"
    text += f"ð´ Balandlik: <b>{data.get('height')} sm</b>\n\n"
    return text


def makeup_basin_info(data) -> str:
    text = str()
    text += f"ðµ Qurilma nomi: <b>{data[2]}</b>\n\n"
    text += f"ð¢ Qurilma id si: <b>{data[0]}</b>\n\n"
    text += f"ð¡ Telefon raqami: <b>{data[1]}</b>\n\n"
    text += f"ð´ Balandlik: <b>{data[3]} sm</b>\n\n"
    text += f"âª Balandlik sozlamasi: <b>{data[7]} sm</b>\n"
    return text


def makeup_basin_message_info(basin, basin_message) -> str:
    text = str()

    bat = float(basin_message[6])
    if bat > 4.12:
        bat = 4.12
    if bat < 3.7:
        bat = 3.7
    bat = round((bat - 3.70) / 0.42 * 100)
    dt = basin_message[10] + datetime.timedelta(hours=5)
    dt = dt.strftime("%H:%M | %d.%m.%Y")

    text += f"ðµ Qurilma nomi: <b>{basin[2]}</b>\n"
    text += f"ð  So'ngi o'lchangan vaqti <b>{dt}</b>\n\n"
    text += f"ð  Suvdan qurilma balandligi: <b>{basin_message[1]} sm</b>\n"
    text += f"ð  Suv sathidan balandligi: <b>{basin_message[2]} sm</b>\n"
    text += f"ð  O'tayotgan suv miqdori: <b>{basin_message[3]} litr/sekund</b>\n"
    text += f"ð  O'tayotgan suv miqdori: <b>{basin_message[4]} mÂ³/soat</b>\n"
    text += f"ð  Jami o'tayotgan suv miqdori: <b>{int(basin_message[5])} mÂ³</b>\n"
    text += f"ð  Batareya quvvati: <b>{bat} %</b>\n"
    text += f"ð¡  GPRS Antena kuchi: <b>{basin_message[7]} net</b>\n"

    return text
