def makeup_basin_info(data: dict) -> str:
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data.get('name')}</b>\n"
    text += f"🟢 Qurilma id si: <b>{data.get('id')}</b>\n"
    text += f"🟡 Telefon raqami: <b>{data.get('phone')}</b>\n"
    text += f"🔴 Balandlik (sm): <b>{data.get('height')}</b>\n"
    return text
