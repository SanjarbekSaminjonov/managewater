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

login_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Eski akkauntimga kirish")],
        [KeyboardButton("Bekor qilish")]
    ],
    resize_keyboard=True
)

register_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Ro'yxatdan o'tish")],
        [KeyboardButton("Bekor qilish")]
    ],
    resize_keyboard=True
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
