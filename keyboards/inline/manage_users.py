from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from googletrans import Translator
trans = Translator()


async def confirmation(language):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(trans.translate("🆗 Yes",dest=language).text, callback_data=f"delete_user:yes"),
            InlineKeyboardButton(trans.translate("🚫 No",dest=language).text, callback_data=f"delete_user:no"),
        ]]
    )
    return markup

