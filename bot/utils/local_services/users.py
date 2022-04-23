def makeup_user_info(data):
    text = f"Telefon: {data.get('username')}\n"
    text += f"Ism: {data.get('first_name')}\n"
    text += f"Familiya: {data.get('last_name')}\n"
    text += f"Viloyat/Sh.: {data.get('region')}\n"
    text += f"Tuman/Sh.: {data.get('city')}\n"
    text += f"Tashkilot: {data.get('org_name')}"

    return text
