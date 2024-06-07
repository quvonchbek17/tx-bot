from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

from googletrans import Translator
trans = Translator()



async def register_button(language):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=trans.translate("🔐 Ro'yxatdan o'tish",dest=language).text),
            ],
        ],
        resize_keyboard=True,
    )
    return markup

async def register_markup(language, items, row=1):
    menuKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=trans.translate("⬅️ Ortga",dest=language).text)
            ],
        ],
        resize_keyboard=True,
        row_width=row,
    )
    for item in items:
        menuKeyboard.insert(KeyboardButton(item[3]))
    return menuKeyboard

async def phone_number_markup(language):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=trans.translate("📲 Telefon raqamni yuborish",dest=language).text, request_contact=True),
            ],
        ],
        resize_keyboard=True,
    )
    return markup

async def back_markup(language):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=trans.translate("⬅️ Ortga",dest=language).text),
            ],
        ],
        resize_keyboard=True,
    )
    return markup