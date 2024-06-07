from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from googletrans import Translator
trans = Translator()

change_callback = CallbackData("change", "item")


async def change_data_markup(language):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(trans.translate("Full name",dest=language).text, callback_data=f"change:full_name"),
            ],
            [
            InlineKeyboardButton(trans.translate("Telefon raqam",dest=language).text, callback_data=f"change:phone_number"),
            InlineKeyboardButton(trans.translate("Group",dest=language).text, callback_data=f"change:group"),
            ],
        ]
    )
    return markup

async def change_data_for_admin_markup(language):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(trans.translate("Full name",dest=language).text, callback_data=f"change:full_name"),
            InlineKeyboardButton(trans.translate("Telefon raqam",dest=language).text, callback_data=f"change:phone_number"),
        ]]
    )
    return markup