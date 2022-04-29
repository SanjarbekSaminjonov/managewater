def makeup_basin_info(data: dict) -> str:
    text = f"id: {data.get('id')}\n"
    text += f"phone: {data.get('phone')}\n"
    text += f"name: {data.get('name')}\n"
    text += f"height: {data.get('height')}\n"
    return text
