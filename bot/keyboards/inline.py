from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


basins_list_callback = CallbackData("list_of_basins", "sep", "id")
basin_manage_callback = CallbackData("basin_manage", "action", "id")


def list_of_basins(basins_list: list):
    buttons = InlineKeyboardMarkup(row_width=1)
    for basin in basins_list:
        button = InlineKeyboardButton(
            text=basin.get('name'),
            callback_data=basins_list_callback.new(
                sep="basin",
                id=basin.get('id')
            )
        )
        buttons.insert(button)
    return buttons


def manage_basin(basin_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Balandlikni o'zgartirish",
                    callback_data=basin_manage_callback.new(
                        action="update_height",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Statistika ko'rish",
                    callback_data=basin_manage_callback.new(
                        action="messages",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Joylashuvni ko'rish",
                    callback_data=basin_manage_callback.new(
                        action="location",
                        id=basin_id
                    )
                )
            ]
        ]
    )
