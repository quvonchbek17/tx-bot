from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from googletrans import Translator
trans = Translator()


async def main_menu(lang):
    menuKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=trans.translate("🗒 Bugungi jadval", dest=lang).text),
                KeyboardButton(text=trans.translate("🗓 Ertangi jadval", dest=lang).text),
            ],
            [
                KeyboardButton(text=trans.translate("📑 To'liq jadval", dest=lang).text)
            ],
            [
                KeyboardButton(text=trans.translate("📤 Murojaat uchun", dest=lang).text),
                KeyboardButton(text=trans.translate("📜 Biz haqimizda", dest=lang).text),
            ],
            [
                KeyboardButton(text=trans.translate("⚙️ Sozlamalar", dest=lang).text),
            ],
        ],
        resize_keyboard=True
    )
    return menuKeyboard