import re

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.callbackdata import lang_callback, position_callback
from keyboards.inline.positions import positions_markup
from keyboards.default.mainMenu import main_menu
from keyboards.default.register import register_markup, phone_number_markup, back_markup
from keyboards.default.admin import admin_menu
from states.register import AdminRegister, Register, SignUp

from googletrans import Translator
trans = Translator()


@dp.message_handler(text = ['🔐 Register',"🔐 Ro'yxatdan o'tish",'🔐 Зарегистрироваться'],state=SignUp.register)
async def show_settings(msg: Message):
    text = "Iltimos ismingizni va familiyangizni kiriting!\n"
    # text += "Masalan: Aliyev Vali\n(Agar ism familiyangizda "
    # text += "<code>'</code> mana shu tiniq belgisi bor bo'lsa "
    # text += "uning o'rniga bu belgidan foydalaning <code>`</code>)"
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if msg.from_user.id not in admin_ids:
        lang = await db.select_language(msg.from_user.id)
        await msg.answer(trans.translate(text=text, dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
        await Register.full_name.set()
    else:
        lang = await db.select_admin_lang(msg.from_user.id)
        await msg.answer(trans.translate(text=text, dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
        await AdminRegister.full_name.set()
    # await msg.edit_reply_markup(reply_markup=ReplyKeyboardRemove(True))

@dp.message_handler(state=Register.full_name)
async def full_name_handler(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    full_name = msg.text.replace("'","''")
    try:
        await state.update_data(full_name=full_name)
        phone_number = (await db.select_user(chat_id=msg.from_user.id))[0][4]
        if not phone_number:
            await msg.answer(trans.translate("Telefon raqamingizni jo'nating!\nNamuna: +998901234567",dest=lang).text, reply_markup=await back_markup(lang))
            await Register.phone_number.set()
        else:
            await msg.answer(trans.translate("Ism familiyangiz ma'lumotlar bazasiga muvaffaqiyatli saqlandi ✅",dest=lang).text)
            await msg.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await main_menu(lang))
            await state.finish()
    except:
        await msg.answer(trans.translate("Xatolik yuzaga keldi.\nIltimos ism familiyangizni qayta kiriting!",dest=lang).text)

@dp.message_handler(state=Register.phone_number)
async def phone_number_handler(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    pattern = "^\+998[0-99]{2}[0-9]{7}$"
    if msg.text == trans.translate(trans.translate('⬅️ Ortga',dest=lang).text,dest=lang).text:
        text = "Iltimos ismingizni va familiyangizni kiriting!\n"
        await msg.answer(trans.translate(text=text, dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
        await Register.full_name.set()
    elif re.match(pattern, msg.text):
        # try:
            await state.update_data(phone=msg.text)
            user_faculty_id = (await db.select_user(chat_id=msg.from_user.id))[0][4]
            if not user_faculty_id:
                universities = (await db.select_all_universities())
                await msg.answer(trans.translate("Universitetingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, universities, row=1))
                await Register.university.set()
            else:
                await msg.answer(trans.translate("Telefon raqamingiz ma'lumotlar bazasiga muvaffaqiyatli saqlandi ✅",dest=lang).text)
                await msg.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await main_menu(lang))
                await state.finish()
        # except:
        #     await msg.answer(trans.translate("Telefon raqamingizni bazaga saqlashda muammo yuzaga keldi😔\n"
        #                                     "Iltimos qayta urinib ko'ring!",dest=lang).text)
    else:
        await msg.answer(trans.translate("Noto'g'ri telefon raqam jo'natdingiz, iltimos to'g'rilab qayta jo'nating",dest=lang).text)
   

# @dp.callback_query_handler(position_callback.filter(), user_id=ADMINS)
# async def choose_position_handler(call: CallbackQuery, state: FSMContext):
#     lang = (await db.select_user(chat_id=call.from_user.id))[0][3]
#     position = call.data.split(':')[1]
#     if position == 'admin':
#         await call.message.answer(trans.translate("Asosiy manyu",dest=lang).text, reply_markup=await admins_menu(lang))
#         await db.update_user_group_id(chat_id=call.from_user.id, group_id=None)
#     else:
#         universities = (await db.select_all_universities())
#         await call.message.answer(trans.translate("Universitetingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, universities, row=1))
#         await Register.university.set()
#     await call.message.delete()


@dp.message_handler(state=Register.university)
async def university_handler(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    university = msg.text.replace("'","''")
    if msg.text == trans.translate('⬅️ Ortga',dest=lang).text:
        await msg.answer(trans.translate("Telefon raqamingizni jo'nating!\nNamuna: +998901234567",dest=lang).text, reply_markup=await back_markup(lang))
        await Register.phone_number.set()
    else:
        try:
            university_id = (await db.select_university(name=university))[0][0]
            await state.update_data(university_id=university_id)
            faculties = (await db.select_faculties(university_id=university_id))
            await msg.answer(trans.translate("Fakultetingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, faculties, row=1))
            faculties = (await db.select_faculties(university_id=university_id))
            await Register.next()
        except:
            universities = (await db.select_all_universities())
            await msg.answer(trans.translate("Ma'lumot mos kelmadi, iltimos universitetingizni qayta tanlang",dest=lang).text, reply_markup=await register_markup(lang, universities, row=1))
    
@dp.message_handler(state=Register.faculty)
async def set_faculty(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    faculty = msg.text.replace("'","''")
    data = await state.get_data()
    university_id = data.get('university_id')
    if msg.text == trans.translate('⬅️ Ortga',dest=lang).text:
        universities = (await db.select_all_universities())
        await msg.answer(trans.translate("Universitetingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, universities, row=1))
        await Register.university.set()
    else:
        try:
            faculty_id = (await db.select_faculties(name=faculty, university_id=university_id))[0][0]
            await state.update_data(faculty_id=faculty_id)
            directions = await db.select_directions(faculty_id=faculty_id)
            await msg.answer(trans.translate("Yo'nalishingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, directions, row=1))
            await Register.next()
        except:
            faculties = (await db.select_faculties(university_id=university_id))
            await msg.answer(trans.translate("Ma'lumot mos kelmadi, iltimos fakultetingizni qayta tanlang",dest=lang).text,  reply_markup=await register_markup(lang, faculties, row=1))

@dp.message_handler(state=Register.direction)
async def set_direction(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    direction = msg.text.replace("'","''")
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    if msg.text == trans.translate('⬅️ Ortga',dest=lang).text:
        university_id = data.get('university_id')
        faculties = (await db.select_faculties(university_id=university_id))
        await msg.answer(trans.translate("Fakultetingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, faculties, row=1))
        await Register.faculty.set()
    else:
        try:
            direction_id = (await db.select_directions(name=direction, faculty_id=faculty_id))[0][0]
            await state.update_data(direction_id=direction_id)
            courses =  await db.select_course(faculty_id=faculty_id)
            await msg.answer(trans.translate("Kursingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, courses, row=2))
            await Register.next()
        except:
            directions = await db.select_directions(faculty_id=faculty_id)
            await msg.answer(trans.translate("Ma'lumot mos kelmadi, iltimos yo'nalishingizni qayta tanlang",dest=lang).text, reply_markup=await register_markup(lang, directions, row=1))

@dp.message_handler(state=Register.course)
async def set_course(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    if msg.text == trans.translate('⬅️ Ortga',dest=lang).text:
        directions = await db.select_directions(faculty_id=faculty_id)
        await msg.answer(trans.translate("Yo'nalishingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, directions, row=2))
        await Register.direction.set()
    else:
        try:
            course_id = (await db.select_course(name=msg.text,faculty_id=faculty_id))[0][0]
            await state.update_data(course_id=course_id)
            education = await db.select_education(faculty_id=faculty_id)
            await msg.answer(trans.translate("Ta'lim shaklingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, education, row=1))
            await Register.next()
        except:
            courses = await db.select_course(faculty_id=faculty_id)
            await msg.answer(trans.translate("Ma'lumot mos kelmadi, iltimos kursingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, courses, row=2))

@dp.message_handler(state=Register.education)
async def set_education(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    course_id = data.get('course_id')
    direction_id = data.get('direction_id')
    if msg.text == trans.translate('⬅️ Ortga',dest=lang).text:
        courses =  await db.select_course(faculty_id=faculty_id)
        await msg.answer(trans.translate("Kursingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, courses, row=2))
        await Register.course.set()
    else:
        # try:
            education_id = (await db.select_education(name=msg.text, faculty_id=faculty_id))[0][0]
            await state.update_data(education_id=education_id)
            groups = await db.select_groups_signup(faculty_id=faculty_id, course_id=course_id, direction_id=direction_id, education_id=education_id)
            await msg.answer(trans.translate("Guruhingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, groups, row=2))
            await Register.next()
        # except:
        #     education = await db.select_education(faculty_id=faculty_id)
            # await msg.answer(trans.translate("Ma'lumot mos kelmadi, iltimos ta'lim shaklingizni qayta tanlang",dest=lang).text, reply_markup=await register_markup(lang, education, row=1))

@dp.message_handler(state=Register.group)
async def set_group(msg: Message, state: FSMContext):
    lang = await db.select_language(msg.from_user.id)
    group = msg.text.replace("'","''")
    data = await state.get_data()
    full_name = data.get('full_name')
    phone = data.get('phone')
    university_id = data.get('university_id')
    faculty_id = data.get('faculty_id')
    direction_id = data.get('direction_id')
    course_id = data.get('course_id')
    education_id = data.get('education_id')
    if msg.text == trans.translate('⬅️ Ortga',dest=lang).text:
        education = await db.select_education(faculty_id=faculty_id)
        await msg.answer(trans.translate("Ta'lim shaklingizni tanlang",dest=lang).text, reply_markup=await register_markup(lang, education, row=1))
        await Register.education.set()
    else:
        # try:
            phone_number = (await db.select_user(chat_id=msg.from_user.id))[0][4]
            if not phone_number:
                await db.update_user_full_name(chat_id=msg.from_user.id, fullname=full_name)
                await db.update_user_phone(chat_id=msg.from_user.id, phone=phone)
            group_id = await db.select_group_id(group, faculty_id, direction_id, course_id, education_id)
            group_id = str(group_id).replace("[<Record id=UUID('",'').replace("')>]",'')
            await db.update_user_group_id(msg.from_user.id, group_id)
            await msg.answer(trans.translate("Ma'lumotlaringiz muvaffaqiyatli saqlandi.\nBot haqida ko'proq bilmoqchi bo'lsangiz, /help buyrug'ini bosing.",dest=lang).text)
            await msg.answer(trans.translate("Asosiy menu", dest=lang).text, reply_markup=await main_menu(lang))
            # adminga xabar berish
            user = (await db.select_user(chat_id=msg.from_user.id))[0]
            admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
            for admin_id in admin_ids:
                admin_language = (await db.select_botadmin(chat_id=admin_id))[0][5]
                text = trans.translate(f"➕ {msg.from_user.get_mention(as_html=True)} has been added to the database",dest=admin_language).text + '\n'
                text += trans.translate("ID:",dest=admin_language).text + '  ' + str(user[9]) + '\n'
                text += trans.translate("To'liq ismi:",dest=admin_language).text + '  '  + str(user[3]) + '\n'
                text += trans.translate("Telefon raqam:",dest=admin_language).text + '  '  + str(user[4]) + '\n'
                text += trans.translate("University:",dest=admin_language).text + '  ' + str((await db.select_university(id=university_id))[0][3]) + '\n'
                text += trans.translate("Faculty:",dest=admin_language).text + '  ' + str((await db.select_faculties(id=faculty_id))[0][3]) + '\n'
                text += trans.translate("Course:",dest=admin_language).text + '  ' + str((await db.select_course(id=course_id))[0][3]) + '\n'
                text += trans.translate("Direction:",dest=admin_language).text + '  ' + str((await db.select_directions(id=direction_id))[0][3]) + '\n'
                text += trans.translate("Education:",dest=admin_language).text + '  ' + str((await db.select_education(id=education_id))[0][3]) + '\n'
                text += trans.translate("Group:",dest=admin_language).text + '  '  + msg.text
                text += "\n#add_user"
                await bot.send_message(chat_id=admin_id,text=text)
            await state.finish()
        # except:
        #     groups = await db.select_groups_signup(faculty_id=faculty_id, course_id=course_id, direction_id=direction_id, education_id=education_id)
        #     await msg.answer(trans.translate("Ma'lumot mos kelmadi, iltimos guruhingizni qayta tanlang",dest=lang).text, reply_markup=await register_markup(lang, groups, row=2))    