from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

basins_list_callback = CallbackData("basin_manage", "sep", "id")
basin_manage_callback = CallbackData("basin_manage", "action", "id")
basin_update_height_callback = CallbackData(
    "basin_manage", "sep", "id", "value")
basin_statistics_callback = CallbackData("basin_manage", "action", "id")
back_to_statistics_callback = CallbackData("basin_manage", "action", "id")

numbers_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="1️⃣", callback_data="1"),
            InlineKeyboardButton(
                text="2️⃣", callback_data="2"),
            InlineKeyboardButton(
                text="3️⃣", callback_data="3"),
        ],
        [
            InlineKeyboardButton(
                text="4️⃣", callback_data="4"),
            InlineKeyboardButton(
                text="5️⃣", callback_data="5"),
            InlineKeyboardButton(
                text="6️⃣", callback_data="6"),
        ],
        [
            InlineKeyboardButton(
                text="7️⃣", callback_data="7"),
            InlineKeyboardButton(
                text="8️⃣", callback_data="8"),
            InlineKeyboardButton(
                text="9️⃣", callback_data="9"),
        ],
        [
            InlineKeyboardButton(
                text="❌", callback_data="clear"),
            InlineKeyboardButton(
                text="0️⃣", callback_data="0"),
            InlineKeyboardButton(
                text="👁", callback_data="show"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash", callback_data="submit"),
        ]
    ]
)


def list_of_basins(basins_list: list):
    buttons = InlineKeyboardMarkup(row_width=1)
    for basin in basins_list:
        button = InlineKeyboardButton(
            text=basin[2],
            callback_data=basins_list_callback.new(
                sep="basin",
                id=basin[0]
            )
        )
        buttons.insert(button)
    return buttons


async def list_of_basins_for_admin(basins_list: list):
    from loader import db
    buttons = InlineKeyboardMarkup(row_width=1)
    for basin in basins_list:
        user = await db.get_user(id=basin[6])
        button = InlineKeyboardButton(
            text=f"{basin[2]} | {user[4]} | {user[13]}",
            callback_data=basins_list_callback.new(
                sep="basin",
                id=basin[0]
            )
        )
        buttons.insert(button)
    return buttons


def manage_basin(basin_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚙️Balandlikni o'zgartirish",
                    callback_data=basin_manage_callback.new(
                        action="update_height",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Statistikani ko'rish",
                    callback_data=basin_manage_callback.new(
                        action="statistics",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="📍 Joylashuvni ko'rish",
                    callback_data=basin_manage_callback.new(
                        action="location",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Qurilmalar ro'yxati",
                    callback_data=basin_manage_callback.new(
                        action="back_to_basins",
                        id=basin_id
                    )
                )
            ]
        ]
    )


def update_height_plus_minus(basin_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="-1 sm",
                    callback_data=basin_update_height_callback.new(
                        sep="update_height",
                        id=basin_id,
                        value="-1"
                    )
                ),
                InlineKeyboardButton(
                    text="+1 sm",
                    callback_data=basin_update_height_callback.new(
                        sep="update_height",
                        id=basin_id,
                        value="1"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="✔️ Ok",
                    callback_data=basin_update_height_callback.new(
                        sep="update_height",
                        id=basin_id,
                        value="ok"
                    )
                )
            ]
        ]
    )


def statistics_types(basin_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ℹ️ Oxirgi xabar",
                    callback_data=basin_statistics_callback.new(
                        action="last_message",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 To'liq statistika",
                    callback_data=basin_statistics_callback.new(
                        action="excel_file",
                        id=basin_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data=basin_statistics_callback.new(
                        action="back_to_manage_basin",
                        id=basin_id
                    )
                )
            ]
        ]
    )


def back_to_statistics_types(basin_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data=back_to_statistics_callback.new(
                        action="back_to_statistics",
                        id=basin_id
                    )
                )
            ]
        ]
    )
