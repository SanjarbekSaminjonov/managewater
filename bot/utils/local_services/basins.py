def makeup_basin_info(data: dict) -> str:
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data[2]}</b>\n\n"
    text += f"🟢 Qurilma id si: <b>{data[0]}</b>\n\n"
    text += f"🟡 Telefon raqami: <b>{data[1]}</b>\n\n"
    text += f"🔴 Balandlik: <b>{data[3]} sm</b>\n\n"
    text += f"⚪ Balandlik sozlamasi: <b>{data[7]} sm</b>\n"
    return text
