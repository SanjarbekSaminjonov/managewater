from distutils.command.build_py import build_py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yes_no_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ha"),
            KeyboardButton("Yo'q")
        ]
    ],
    resize_keyboard=True
)

login_register_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Ro'yxatdan o'tish")],
        [KeyboardButton("Eski akkauntimga kirish")]
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Bekor qilish")]
    ],
    resize_keyboard=True
)

contact = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📱 Telefon raqamni yuborish",
                request_contact=True)
        ],
        [KeyboardButton("Bekor qilish")]
    ]
)

location = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📍 Joylashuv yuborish",
                request_location=True)
        ],
        [KeyboardButton("O'tkazib yuborish")],
        [KeyboardButton("Bekor qilish")]
    ]
)

home_sections = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Qurilma qo'shish")],
        [KeyboardButton("Mening qurilmalarim")],
        [
            KeyboardButton("Button"),
            KeyboardButton("Button"),
        ]
    ],
    resize_keyboard=True
)


def buttons_of_list(items: list):
    buttons = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for item in items:
        buttons.insert(KeyboardButton(text=item))
    buttons.insert(KeyboardButton("Bekor qilish"))
    return buttons
