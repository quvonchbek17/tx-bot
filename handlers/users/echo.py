from aiogram import types



from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.admin import admin_menu
from keyboards.default.mainMenu import main_menu
from keyboards.default.register import register_button
from states.register import SignUp
from googletrans import Translator
trans = Translator()


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if user_id in admin_ids:
        language = (await db.select_botadmin(chat_id=user_id))[0][5]
        await message.answer(trans.translate("Asosiy menyu",dest=language).text, reply_markup=await admin_menu(language))
    else:
        language = (await db.select_user(chat_id=message.from_user.id))[0][5]
        await message.answer(trans.translate("Asosiy menyu",dest=language).text, reply_markup=await main_menu(language))
        
@dp.message_handler(state=SignUp.register)
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if user_id in admin_ids:
        language = (await db.select_botadmin(chat_id=user_id))[0][5]
    else:
        language = (await db.select_user(chat_id=message.from_user.id))[0][5]
    await message.answer(trans.translate("Botdan foydalanish uchun iltimos ro'yxatdan o'ting.",dest=language).text, reply_markup=await register_button(language))
