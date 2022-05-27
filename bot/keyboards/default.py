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
        [KeyboardButton("Ro'yxatdan o'tish")]
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

be_watcher = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("Ushbu qurilmani kuzatmoqchiman")],
        [KeyboardButton("Bekor qilish")]
    ]
)

location = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📍 Qurilma joylashuvini yuborish",
                request_location=True)
        ],
        [KeyboardButton("Tashlab ketish")],
        [KeyboardButton("Bekor qilish")]
    ]
)

home_sections = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Qurilma qo'shish")],
        [KeyboardButton("Mening qurilmalarim")]
    ],
    resize_keyboard=True
)


def buttons_of_list(items: list):
    buttons = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for item in items:
        buttons.insert(KeyboardButton(text=item))
    buttons.insert(KeyboardButton("Bekor qilish"))
    return buttons
