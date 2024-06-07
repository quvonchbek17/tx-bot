from aiogram import types

from keyboards.default.mainMenu import main_menu

from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.admin import admin_menu

from googletrans import Translator
trans = Translator()


# Echo bot
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if user_id in admin_ids:
        language = (await db.select_botadmin(chat_id=user_id))[0][5]
        await message.answer(trans.translate("Asosiy menyu",dest=language).text, reply_markup=await admin_menu(language))
    else:
        language = (await db.select_user(chat_id=message.from_user.id))[0][3]
        await message.answer(trans.translate("Asosiy menyu",dest=language).text, reply_markup=await main_menu(language))