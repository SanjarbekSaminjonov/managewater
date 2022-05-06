from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("IP")
API_URL = env.str("API_URL")


REGIONS = {
    "Andijon viloyati": None,
    "Buxoro viloyati": None,
    "Farg'ona viloyati": [
        "Bog'dod tumani",
        "Beshariq tumani",
        "Buvayda tumani",
        "Dang'ara tumani",
        "Farg'ona tumani",
        "Farg'ona shahri",
        "Furqat tumani",
        "Oltiariq tumani",
        "O'zbekiston tumani",
        "Marg'ilon shahri",
        "Qo'qon shahri",
        "Qo'shtepa tumani",
        "Quvasoy shahri",
        "Quva tumani",
        "Rishton tumani",
        "So'x tumani",
        "Toshloq tumani",
        "Uchko'prik tumani",
        "Yozyovon tumani"
    ],
    "Jizzax viloyati": None,
    "Xorazm viloyati": None,
    "Namangan viloyati": None,
    "Navoiy viloyati": None,
    "Qashqadaryo viloyati": None,
    "Qoraqalpog'iston Respublikasi": None,
    "Samarqand viloyati": None,
    "Sirdaryo viloyati": None,
    "Surxondaryo viloyati": None,
    "Toshkent viloyati": None,
    "Toshkent shahri": None
}
