from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

from googletrans import Translator
trans = Translator()


async def settings_markup(lang):
    menuKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
				KeyboardButton(trans.translate("📝 Ma'lumotlarni o'zgartirish",dest=lang).text)
			],
            [
				KeyboardButton(trans.translate("🌎 Tilni o'zgartirish",dest=lang).text)
			],
            [
				KeyboardButton(trans.translate("🔙 Asosiy menyu",dest=lang).text)
			],
        ],
        resize_keyboard=True,
    )
    return menuKeyboard

async def cancel_button(language):
    markup = ReplyKeyboardMarkup(
		keyboard=[
      		[
				KeyboardButton(trans.translate("🚫 Cancel",dest=language).text)
			],
		],
		resize_keyboard=True,
	)
    return markup