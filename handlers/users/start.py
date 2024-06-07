import asyncpg

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import any_state

from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline.languages import languages
from keyboards.default.mainMenu import main_menu
from keyboards.default.admin import admin_menu

from googletrans import Translator
trans = Translator()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # Foydalanuvchini bazaga qo'shish
    if message.from_user.id in [record['chat_id'] for record in await db.select_admin_ids()]:
        try:
            await db.delete_user(chat_id=message.from_user.id)
            await db.add_botadmin(message.from_user.id)
            count = await db.count_botadmins()
            if not message.from_user.username:
                msg = f"😎 <a href='https://t.me/{message.from_user.username}'>{message.from_user.full_name}</a> admin sifatida bazaga qo'shildi.\nBazada {count} ta admin bor."
            else:
                msg = f"😎 {message.from_user.full_name} admin sifatida bazaga qo'shildi.\nBazada {count} ta admin bor."
        except:
            msg = None
        language = await db.select_admin_lang(message.from_user.id)
        if language is None:
            await message.answer("🇬🇧 Choose language\n🇷🇺 Выберите язык\n🇺🇿 Tilni tanlang", reply_markup=languages)
        else:
            await message.answer(text=trans.translate(text="Asosiy menyu",dest=language).text, reply_markup=await admin_menu(language))
        await db.update_botadmin_username(message.from_user.id, message.from_user.username)
    else:
        try:
            await db.add_user(chat_id=message.from_user.id)
            count = await db.count_users()
            if message.from_user.username:
                msg = f"<a href='https://t.me/{message.from_user.username}'>{message.from_user.full_name}</a> bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            else:
                msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        except:
            msg = None
        if message.from_user.username:
            await db.update_username(chat_id=message.from_user.id, username=message.from_user.username)
        else:
            await db.update_username(chat_id=message.from_user.id, username='')
        language = await db.select_language(message.from_user.id)
        if language is None:
            await message.answer("🇬🇧 Choose language\n🇷🇺 Выберите язык\n🇺🇿 Tilni tanlang", reply_markup=languages)
        else:
            await message.answer(text=trans.translate(text="Asosiy menyu",dest=language).text, reply_markup=await main_menu(language))
    # Adminga xabar berish
    if msg:
        for admin_id in ADMINS:
            await bot.send_message(chat_id=admin_id, text=msg, disable_web_page_preview=True)
            # admin_language = (await db.select_botadmin(chat_id=admin_id))[0][5]
            # await bot.send_message(chat_id=admin_id, text=trans.translate(msg,dest=admin_language).text, disable_web_page_preview=True)