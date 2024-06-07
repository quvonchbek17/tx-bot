import re

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.callbackdata import lang_callback, position_callback
from keyboards.inline.positions import positions_markup
from keyboards.default.mainMenu import main_menu
from keyboards.default.register import register_markup, phone_number_markup
from keyboards.default.admin import admin_menu
from states.register import Register, AdminRegister

from googletrans import Translator
trans = Translator()

pattern = "^[+][998]{3}[00-99]{2}[0-9]{7}$"


@dp.message_handler(state=AdminRegister.full_name)
async def full_name_handler(msg: Message, state: FSMContext):
    lang = (await db.select_botadmin(chat_id=msg.from_user.id))[0][5]
    full_name = msg.text.replace("'","''")
    try:
        await db.update_botadmin_full_name(chat_id=msg.from_user.id, full_name=full_name)
        phone_number = (await db.select_botadmin(chat_id=msg.from_user.id))[0][4]
        if not phone_number:
            await msg.answer(trans.translate("Telefon raqamingizni jo'nating!\nNamuna: +998901234567",dest=lang).text)
            await AdminRegister.phone_number.set()
        else:
            await msg.answer(trans.translate("Ism familiyangiz ma'lumotlar bazasiga muvaffaqiyatli saqlandi ✅",dest=lang).text)
            await msg.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await admin_menu(lang))
            await state.finish()
    except:
        await msg.answer(trans.translate("Xatolik yuzaga keldi.\nIltimos ism familiyangizni qayta kiriting!",dest=lang).text)
        
@dp.message_handler(state=AdminRegister.phone_number)
async def phone_number_handler(msg: Message, state: FSMContext):
    lang = (await db.select_botadmin(chat_id=msg.from_user.id))[0][5]
    if re.match(pattern, msg.text):
        try:
            await db.update_botadmin_phone(chat_id=msg.from_user.id, phone=msg.text)
            # await msg.answer(trans.translate("Botdan admin sifatida foydalanmoqchimisiz yoki oddiy foydalanuvchimi?",dest=lang).text,
            #                 				reply_markup=await positions_markup(lang))
            await msg.answer(trans.translate(f"Ma'lumotlaringiz muvaffaqiyatli saqlandi!\nBot haqida ko'proq bilmoqchi bo'lsangiz, /help buyrug'ini bosing.",dest=lang).text,
                                            reply_markup=await admin_menu(lang))
            await state.finish()
            # adminga xabar yuborish
            user = await db.select_botadmin(chat_id=msg.from_user.id)
            # faculty = await db.select_faculties(id=user[0][6])
            # university = (await db.select_university(id=faculty[0][2]))[0][1]
            admin_lang = (await db.select_botadmin(chat_id=ADMINS[0]))[0][5]
            text = trans.translate(f"😎 {msg.from_user.get_mention(as_html=True)} has been added to the database of admins",dest=admin_lang).text + '\n'
            text += trans.translate("ID:",dest=admin_lang).text + '  ' + str(user[0][8]) + '\n'
            if msg.from_user.username:
                text += trans.translate(f"To'liq ismi:",dest=admin_lang).text + '  '  + f"<a href='https://t.me/{msg.from_user.username}'>{user[0][3]}</a>:" + '\n'
            else:
                text += trans.translate(f"To'liq ismi:",dest=admin_lang).text + ' ' + user[0][3] + '\n'
            text += trans.translate("Telefon raqam:",dest=admin_lang).text + '  '  + user[0][4] + '\n'
            # text += trans.translate("University:",dest=admin_lang).text + '  ' + university + '\n'
            # text += trans.translate("Faculty:",dest=admin_lang).text + '  ' + faculty[0][1]
            text += '\n#add_admin'
            await bot.send_message(chat_id=ADMINS[0], text=text)
        except:
            await msg.answer(trans.translate("Telefon raqamingizni bazaga saqlashda muammo yuzaga keldi😔\n"
                                        "Iltimos qayta urinib ko'ring!",dest=lang).text)
    else:
        await msg.answer(trans.translate("Noto'g'ri telefon raqam jo'natdingiz, iltimos to'g'rilab qayta jo'nating",dest=lang).text)