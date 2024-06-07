from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from googletrans import Translator
trans = Translator()


async def positions_markup(language):
    markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(trans.translate("😎 admin",dest=language).text, callback_data='position:admin'),
				InlineKeyboardButton(trans.translate("🙂 user",dest=language).text, callback_data='position:user')
			],
		],
	)
    return markup