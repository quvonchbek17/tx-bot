from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from googletrans import Translator
trans = Translator()

async def admin_menu(language):
    markup = ReplyKeyboardMarkup(
		keyboard=[
      		# [
			# 	KeyboardButton(trans.translate("🔑 Admin buyruqlari",dest=language).text)
			# ],
			[
				KeyboardButton(trans.translate("📨 Foydalanuvchilarga xabar jo'natish",dest=language).text)
			],
			[
                KeyboardButton(text=trans.translate("📜 Biz haqimizda", dest=language).text),
			],
      		[
				KeyboardButton(trans.translate("⚙️ Sozlamalar ",dest=language).text)
			],
		],
		resize_keyboard=True,
	)
    return markup

async def admin_settings(lang):
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
