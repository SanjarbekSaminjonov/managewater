from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


basins_list_callback = CallbackData("basins_list", "id")


def list_of_basins(basins_list):
    buttons = InlineKeyboardMarkup(row_width=1)
    for basin in basins_list:
        button = InlineKeyboardButton(
            text=basin.get('name'),
            callback_data=basins_list_callback.new(
                id=basin.get('id')
            )
        )
        buttons.insert(button)
    return buttons
