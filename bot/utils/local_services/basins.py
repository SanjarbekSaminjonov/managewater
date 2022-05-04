from aiogram.dispatcher import FSMContext

from utils import backend_services


def makeup_basin_info(data: dict) -> str:
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data.get('name')}</b>\n\n"
    text += f"🟢 Qurilma id si: <b>{data.get('id')}</b>\n\n"
    text += f"🟡 Telefon raqami: <b>{data.get('phone')}</b>\n\n"
    text += f"🔴 Balandlik (sm): <b>{data.get('height')}</b>\n\n"
    return text


async def get_list_of_basins(user: tuple, state: FSMContext, new: bool = False) -> list:
    data = await state.get_data()
    basins = data.get('basins')
    if basins is None or new:
        basins = await backend_services.basins.get_basins_list(user=user)
        await state.update_data({'basins': basins})
        return basins
    else:
        return basins


async def get_basin_by_id(user: tuple, basin_id: str, state: FSMContext) -> dict:
    basins = await get_list_of_basins(user=user, state=state)
    await state.update_data({'current_basin_id': basin_id})
    for basin in basins:
        if basin.get('id') == basin_id:
            return basin
    return dict()
