from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters.state import any_state

from loader import dp, db
from states.register import SignUp

from googletrans import Translator
trans = Translator()


@dp.message_handler(text = ['📜 About us','📜 Biz haqimizda','📜 О нас'])
@dp.message_handler(Command("about"))
async def bot_about(message: types.Message):
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if message.from_user.id in admin_ids:
        lang = (await db.select_botadmin(chat_id=message.from_user.id))[0][5]     
    else:
        lang = (await db.select_user(chat_id=message.from_user.id))[0][5]
    text = ("Bizning jamoa",
            "<a href='t.me/QuvonchbekMuysinov'>Quvonchbek Muysinov</a> - Backend dasturchi",
            # "<a href='t.me/Jaloliddin0205'>Jaloliddin Nasrullayev</a> - Backend dasturchi",
            "<a href='t.me/nosirovbehzodjon'>Behzodjon Nosirov</a> - Frontend dasturchi",
            "<a href='t.me/akbarqoyliev'>Akbar Qo'yliyev</a> - Telegram bot dasturchi\n",
            "Botning muhokama chati - @talabagaxabar")
    await message.answer(trans.translate(text='\n'.join(text),dest=lang).text, disable_web_page_preview=True)
    
# @dp.message_handler(Command("about"), state=SignUp.register)
# async def bot_about(message: types.Message):
#     admin_ids = [id[1] for id in await db.select_all_botadmins()]
#     if message.from_user.id in admin_ids:
#         lang = (await db.select_botadmin(admin_chat_id=message.from_user.id))[0][5]     
#     else:
#         lang = (await db.select_user(user_chat_id=message.from_user.id))[0][3]
#     text = ("Bizning jamoa",
#             "<a href='t.me/QuvonchbekMuysinov'>Quvonchbek Muysinov</a> - Backend dasturchi",
#             "<a href='t.me/Jaloliddin0205'>Jaloliddin Nasrullayev</a> - Backend dasturchi",
#             "<a href='t.me/nosirovbehzodjon'>Behzodjon Nosirov</a> - Frontend dasturchi",
#             "<a href='t.me/akbarqoyliev'>Akbar Qo'yliyev</a> - Telegram bot dasturchi",)
#     await message.answer(trans.translate(text='\n'.join(text),dest=lang).text, disable_web_page_preview=True)
