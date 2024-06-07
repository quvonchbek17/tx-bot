from aiogram import types
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.default.admin import admin_menu

from loader import dp, db, bot
from keyboards.inline.callbackdata import lang_callback
from keyboards.default.mainMenu import main_menu
from keyboards.default.register import register_button, register_markup
from keyboards.inline.settings import change_callback
from states.register import Register, AdminRegister, SignUp

from googletrans import Translator
trans = Translator()

text = "Iltimos ismingizni va familiyangizni kiriting!\n"
text += "Masalan: Aliyev Vali\n(Agar ism familiyangizda "
text += "<code>'</code> mana shu tiniq belgisi bor bo'lsa "
text += "uning o'rniga bu belgidan foydalaning <code>`</code>)"

lang_dict = {'en':"🇬🇧 English is selected",'ru':'🇷🇺 Выбран русский язык','uz':"🇺🇿 O'zbek tili tanlandi"}

@dp.callback_query_handler(lang_callback.filter())
async def update_language(call: CallbackQuery,state: FSMContext):
    lang = call.data.split(':')[1]
    admin_ids = [id[8] for id in await db.select_all_botadmins()]
    if call.from_user.id in admin_ids:
        await db.update_botadmin_language(chat_id=call.from_user.id, language=lang)
        full_name = (await db.select_botadmin(chat_id=call.from_user.id))[0][3]
        if full_name is None:
            await call.message.answer(trans.translate(f"Assalomu alaykum {call.from_user.full_name}, Botga xush kelibsiz!\n"
                                                      "Bu bot talabalarga juda yaxshi yordamchi bo'la oladi. (Ko'proq ma'lumot uchun - /help).\n"
                                                      "Ro'yxatdan o'tganingizdan so'ng botdan admin sifatida foydalana olasiz!", dest=lang).text, reply_markup=await register_button(lang))
            await SignUp.register.set()
        else:
            await call.message.answer(text=lang_dict[lang], reply_markup=await admin_menu(lang))
    else:
        await db.update_language(chat_id=call.from_user.id, language=lang)
        full_name = (await db.select_user(chat_id=call.from_user.id))[0][3]
        if full_name is None:
            await call.message.answer(trans.translate(f"Assalomu alaykum {call.from_user.full_name}, Botga xush kelibsiz!\n"
                                                      "Bu bot talabalarga juda yaxshi yordamchi bo'la oladi. (Ko'proq ma'lumot uchun - /help).\n"
                                                      "Botdan foydalanish uchun iltimos ro'yxatdan o'ting! Iltimos ro'yxatdan o'tish jarayonida ma'lumotlaringizni to'g'ri kiriting!\n"
                                                      "Sizning ma'lumotlaringizni biz albatta muhofaza qilamiz!", dest=lang).text, reply_markup=await register_button(lang))
            await SignUp.register.set()
        else:
            await call.message.answer(text=lang_dict[lang], reply_markup=await main_menu(lang))
    await call.message.delete()
    
@dp.callback_query_handler(change_callback.filter(), )
async def update_data(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        msg_id = data.get('msg_id')
        await bot.delete_message(chat_id=call.from_user.id,message_id=msg_id)
    except:
        pass
    item = call.data.split(':')[1]
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if call.from_user.id in admin_ids:
        lang = (await db.select_botadmin(chat_id=call.from_user.id))[0][5]
        if item == 'full_name':
            await call.message.answer(trans.translate("Iltimos ismingizni va familiyangizni kiriting!",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
            await AdminRegister.full_name.set()
        elif item == 'phone_number':
            await call.message.answer(trans.translate("Telefon raqamingizni jo'nating!\nNamuna: +998901234567",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
            await AdminRegister.phone_number.set()
    else:
        lang = (await db.select_user(chat_id=call.from_user.id))[0][5]
        if item == 'full_name':
            await call.message.answer(trans.translate("Iltimos ismingizni va familiyangizni kiriting!",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
            await Register.full_name.set()
        elif item == 'phone_number':
            await call.message.answer(trans.translate("Telefon raqamingizni jo'nating!\nNamuna: +998901234567",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
            await Register.phone_number.set()
        elif item == 'group':
            universities = await db.select_all_universities()
            await call.message.answer(trans.translate("Universitetingizni tanlang!",dest=lang).text, reply_markup=await register_markup(universities, row=1))
            await Register.university.set()