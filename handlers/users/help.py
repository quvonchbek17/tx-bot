from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.state import any_state

from loader import dp, db
from states.register import SignUp

from googletrans import Translator
trans = Translator()


@dp.message_handler(CommandHelp(), state=any_state)
async def bot_help(message: types.Message):
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if message.from_user.id in admin_ids:
        lang = (await db.select_botadmin(chat_id=message.from_user.id))[0][5]
        text = ("   Botdan to'liq foydalanishingiz uchun botda ro'yxatdan o'tgan bo'lishingiz kerak, ",
                "agar ro'yxatdan o'tish jarayonida muammo yuzaga kelgan bo'lsa, botga /stop buyrug'ini jo'nating ",
                "keyin esa /start buyrug'ini jo'natish orqali qayta ro'yxatan o'ting!\n",
                "   Iltimos adminlik huquqingizni suv istemol qilmang❗️ Aniqrog'i foydalanuvchilarga xabar jo'natish ",
                "buyrug'idan reklama tarqatishda foydalanmang.\nBiz haqimizda - /about")
    else:
        lang = (await db.select_user(chat_id=message.from_user.id))[0][5]
        text = ("   Botdan to'liq foydalanishingiz uchun botda ro'yxatdan o'tgan bo'lishingiz kerak, ",
                "agar ro'yxatdan o'tish jarayonida muammo yuzaga kelgan bo'lsa, botga /stop buyrug'ini jo'nating ",
                "keyin esa /start buyrug'ini jo'natish orqali qayta ro'yxatan o'ting! ",
                "So'ngra bot sizga har bir darsingiz boshlanishdan 15 daqiqa oldin dars jadvalingizni jo'natib turadi.\n",
                "Agarda sizning universitetingiz bizning ro'yxat(/universities - universitetlar ro'yxati)da mavjud bo'lmasa u holda ",
                "siz fakultetingizning dekanati bilan bo'g'lanib bizning botni taklif qilishingizni tavsiya qilamiz!\nBiz haqimizda - /about",)
    await message.answer(trans.translate(text=''.join(text),dest=lang).text)