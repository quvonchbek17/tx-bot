from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from googletrans import Translator
trans = Translator()


post_callback = CallbackData("create_post", "action")
sma_callback = CallbackData("sma", "action")
ad_callback = CallbackData("ad", "action")

async def confirmation_keyboard(prefix, language):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(trans.translate("🆗 Chop etish",dest=language).text, callback_data=f"{prefix}:post"),
            InlineKeyboardButton(trans.translate("❌ Bekor qilish",dest=language).text, callback_data=f"{prefix}:cancel"),
        ]]
    )
    return markup
