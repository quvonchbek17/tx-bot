from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .callbackdata import university_callback, faculty_callback, direction_callback, group_callback

from googletrans import Translator
trans = Translator()


async def objects_markup(objects, prefix, language):
    row = 2 if prefix in ['group','course'] else 1
    markup = InlineKeyboardMarkup(row_width=row)
    if objects:
        for object in objects:
            markup.insert(InlineKeyboardButton(object[1],callback_data=str(prefix+':'+str(object[0]))))
    if prefix == 'course':
        markup.row_width = 1
        markup.insert(InlineKeyboardButton(text=trans.translate(text="😎 Admins",dest=language).text, callback_data='admins'))
    elif prefix == 'admin':
        markup.insert(InlineKeyboardButton(trans.translate("➕ Yangi admin qo'shish",dest=language).text, callback_data='admin:add'))
    if prefix != 'university':
        markup.row_width = 1
        markup.insert(InlineKeyboardButton("🔙", callback_data=f'{prefix}:back'))
        markup.row_width = 2
    markup.insert(InlineKeyboardButton('❌', callback_data='delete'))
    return markup