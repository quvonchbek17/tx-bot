import asyncio
import re

from aiogram.types import Message, ContentType, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from data.config import ADMINS
from keyboards.default.settings import cancel_button
from loader import dp, db, bot
from utils.misc.echo import bot_echo
from states.manage import AddAdmin
from states.newpost import NewPost
from keyboards.inline.manage_post import confirmation_keyboard, post_callback, ad_callback, sma_callback
from keyboards.inline.show_objects import objects_markup
from keyboards.inline.manage_users import confirmation
from keyboards.inline.callbackdata import (university_callback, faculty_callback, admin_callback,
direction_callback, group_callback, student_callback, course_callback, education_callback)

from googletrans import Translator
trans = Translator()

@dp.message_handler(text="/sc",user_id=ADMINS[0])
async def spicial_commands(message: Message):
    lang = await db.select_admin_lang(message.from_user.id)
    text = "/ad - " + trans.translate("<i>Barcha foydalanuvchilarga reklama jo'natish</i>",dest=lang).text + '\n'
    text += "/control - " + trans.translate("<i>Talabalarni va adminlarni nazorat qilish</i>",dest=lang).text + '\n'
    text += "/delete_posts - " + trans.translate("<i>Oxirgi xabarlarni o'chirish</i>",dest=lang).text + '\n'
    text += "/send_message_admins - " + trans.translate("<i>Adminlarga xabar jo'natish</i>",dest=lang).text + '\n'
    await message.answer(text)
    await message.delete()

# foydalanuvchiga javob berish
@dp.message_handler(is_reply=True, content_types=ContentType.all(), user_id=ADMINS[0])
async def reply_message(msg: Message):
    lang = await db.select_admin_lang(msg.from_user.id)
    try:
        await msg.send_copy(chat_id=msg.reply_to_message.forward_from.id)
    except:
        await msg.reply(trans.translate("Bu foydalanuvchi 'forward'ni yopib qo'ygan.",dest=lang).text)

# barcha foydalanuvchilarga xabar jo'natish adminlardan tashqari
@dp.message_handler(Command("ad"), user_id=ADMINS[0])
async def ad(message: Message):
    admin_ids = [id[8] for id in await db.select_all_botadmins()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        await message.answer(trans.translate("Chop etish uchun post yuboring.",dest=lang).text)
        await NewPost.Ad.set()
    else:
        await bot_echo(message)
    
@dp.message_handler(state=NewPost.Ad, content_types=ContentType.all(), user_id=ADMINS[0])
async def enter_message(message: Message, state: FSMContext):
    lang = await db.select_admin_lang(message.from_user.id)
    await message.reply(text=trans.translate("Postni chop etilishini xohlaysizmi?",dest=lang).text,
                        reply_markup=await confirmation_keyboard('ad',lang))
    await state.finish()

@dp.callback_query_handler(ad_callback.filter(action="post"), user_id=ADMINS[0])
async def approve_post(call: CallbackQuery):
    admin = (await db.select_botadmin(chat_id=call.from_user.id))[0]
    lang, faculty_id = admin[5], admin[6]
    await call.answer(trans.translate("Chop etishga ruhsat berdingiz.",dest=lang).text)
    await call.message.edit_reply_markup()
    message = call.message.reply_to_message
    users = await db.select_all_users()
    for user in users:
        try:
            await message.send_copy(chat_id=user[1])
        except:
            pass
        asyncio.sleep(00.1)
    
@dp.callback_query_handler(ad_callback.filter(action="cancel"), user_id=ADMINS[0])
async def decline_post(call: CallbackQuery):
    lang = await db.select_admin_lang(call.from_user.id)
    await call.answer(trans.translate("Post rad etildi.",dest=lang).text)
    await call.message.edit_reply_markup()

# adminlarga xabar jo'natish
@dp.message_handler(Command("send_message_admins"), user_id=ADMINS[0])
async def send_message_to_admins(message: Message):
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        await message.answer(trans.translate("Chop etish uchun post yuboring.",dest=lang).text)
        await message.delete()
        await NewPost.SMA.set()
    else:
        await bot_echo(message)

@dp.message_handler(state=NewPost.SMA, content_types=ContentType.all(), user_id=ADMINS[0])
async def enter_message(message: Message, state: FSMContext):
    lang = await db.select_admin_lang(message.from_user.id)
    await message.reply(text=trans.translate("Postni chop etilishini xohlaysizmi?",dest=lang).text,
                        reply_markup=await confirmation_keyboard('sma',lang))
    await state.finish()
    
@dp.callback_query_handler(sma_callback.filter(action="post"), user_id=ADMINS[0])
async def approve_post(call: CallbackQuery):
    lang = await db.select_admin_lang(call.from_user.id)
    await call.answer(trans.translate("Chop etishga ruhsat berdingiz.",dest=lang).text)
    await call.message.edit_reply_markup()
    message = call.message.reply_to_message
    users = await db.select_all_botadmins()
    for user in users:
        try:
            await message.send_copy(chat_id=user[1])
        except:
            pass
        asyncio.sleep(00.1)

@dp.callback_query_handler(sma_callback.filter(action="cancel"), user_id=ADMINS[0])
async def decline_post(call: CallbackQuery):
    lang = await db.select_admin_lang(call.from_user.id)
    await call.answer(trans.translate("Post rad etildi.",dest=lang).text)
    await call.message.edit_reply_markup()

# foydalanuvchilarni va adminlarni nazorat qilish
@dp.message_handler(Command("control"), user_id=ADMINS[0])
async def show_universities(message: Message):
    lang = await db.select_admin_lang(message.from_user.id)
    universities = await db.select_all_universities()
    await message.answer(trans.translate("Universities 👇",dest=lang).text, reply_markup=(await objects_markup(universities,'university',lang)))
    await message.delete()
    
@dp.callback_query_handler(text='delete')
async def delete_message(call: CallbackQuery):
    await call.message.delete()

@dp.callback_query_handler(faculty_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_universities(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    universities = await db.select_all_universities()
    await call.message.edit_text(trans.translate("Universities 👇",dest=lang).text, reply_markup=await objects_markup(universities,'university',lang))

@dp.callback_query_handler(course_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_faculties(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    data = await state.get_data()
    university_id = data.get('university_id')
    faculties = await db.select_faculties(university_id=university_id)
    await call.message.edit_text(trans.translate("Faculties 👇",dest=lang).text, reply_markup=await objects_markup(faculties,'faculty',lang))

@dp.callback_query_handler(direction_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_courses(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    courses = await db.select_courses()
    await call.message.edit_text(trans.translate("Courses 👇",dest=lang).text, reply_markup=await objects_markup(courses,'course',lang))

@dp.callback_query_handler(education_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_directions(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    course_id = data.get('course_id')
    directions = await db.select_directions_signup(course_id,faculty_id)
    await call.message.edit_text(trans.translate("Directions 👇",dest=lang).text, reply_markup=await objects_markup(directions,'direction',lang))

@dp.callback_query_handler(group_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_education(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    data = await state.get_data()
    direction_id = data.get('direction_id')
    education = await db.select_all_education()
    await call.message.edit_text(trans.translate("Education 👇",dest=lang).text, reply_markup=await objects_markup(education,'education',lang))
    
@dp.callback_query_handler(student_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_groups(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    data = await state.get_data()
    direction_id = data.get('direction_id')
    course_id = data.get('course_id')
    education_id = data.get('education_id')
    groups = await db.select_groups_signup(course_id,direction_id,education_id)
    await call.message.edit_text(trans.translate("Groups 👇",dest=lang).text, reply_markup=await objects_markup(groups,'group',lang))

@dp.callback_query_handler(admin_callback.filter(item_name="back"), user_id=ADMINS[0])
async def back_courses(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    courses = await db.select_courses()
    await call.message.edit_text(trans.translate("Courses 👇",dest=lang).text, reply_markup=await objects_markup(courses,'course',lang))

@dp.callback_query_handler(university_callback.filter(), user_id=ADMINS[0])
async def show_faculties(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    university_id = call.data.split(':')[1]
    await state.update_data(university_id=university_id)
    faculties = await db.select_faculties(university_id=university_id)
    await call.message.edit_text(trans.translate("Faculties 👇",dest=lang).text, reply_markup=await objects_markup(faculties,'faculty',lang))
    
@dp.callback_query_handler(faculty_callback.filter(), user_id=ADMINS[0])
async def show_courses(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    faculty_id = call.data.split(':')[1]
    await state.update_data(faculty_id=faculty_id)
    courses = await db.select_courses()
    await call.message.edit_text(trans.translate("Courses 👇",dest=lang).text, reply_markup=await objects_markup(courses,'course',lang))

@dp.callback_query_handler(course_callback.filter(), user_id=ADMINS[0])
async def show_directions(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    course_id = call.data.split(':')[1]
    await state.update_data(course_id=course_id)
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    directions = await db.select_direcrions_signup(course_id,faculty_id)
    await call.message.edit_text(trans.translate("Directions 👇",dest=lang).text, reply_markup=await objects_markup(directions,'direction',lang))
    
@dp.callback_query_handler(direction_callback.filter(), user_id=ADMINS[0])
async def show_education(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    direction_id = call.data.split(':')[1]
    await state.update_data(direction_id=direction_id)
    education = await db.select_all_education()
    await call.message.edit_text(trans.translate("Education 👇",dest=lang).text, reply_markup=await objects_markup(education,'education',lang))

@dp.callback_query_handler(education_callback.filter(), user_id=ADMINS[0])
async def show_groups(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    education_id = call.data.split(':')[1]
    await state.update_data(education_id=education_id)
    data = await state.get_data()
    direction_id = data.get('direction_id')
    course_id = data.get('course_id')
    groups = await db.select_groups_signup(course_id,direction_id,education_id)
    await call.message.edit_text(trans.translate("Groups 👇",dest=lang).text, reply_markup=await objects_markup(groups,'group',lang))
    
@dp.callback_query_handler(group_callback.filter(), user_id=ADMINS[0])
async def show_students(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    users = await db.select_user(user_group_id=call.data.split(':')[1])
    users = [list(user) for user in users]
    users.sort(key=lambda user: user[2])
    group = await db.select_groups(group_id=call.data.split(':')[1])
    text = trans.translate(f'<b>{group[0][1]}</b> guruhining talabalari.',dest=lang).text + '\n\n'
    k = 1
    for user in users:
        if user[6]:
            text += f"{k}. <a href='t.me/{user[5]}'>{user[2]}</a>\n{trans.translate('Phone number',dest=lang).text}: {user[4]}\n\n"
        else:
            text += f"{k}. {user[2]}\n{trans.translate('Phone number',dest=lang).text}: {user[4]}\n\n"
        k += 1
    await call.message.edit_text(text, disable_web_page_preview=True, reply_markup=await objects_markup(None, 'student', lang))
    
@dp.callback_query_handler(text='admins', user_id=ADMINS[0])
async def show_admins(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    faculty = await db.select_faculties(faculty_id=faculty_id)
    admins = await db.select_botadmin(admin_faculty_id=faculty_id)
    text = trans.translate(f'<b>{faculty[0][1]}</b> fakultetining adminlari',dest=lang).text + '\n\n'
    k = 1
    for admin in admins:
        if admin[3]:
            text += f"{k}. <a href='t.me/{admin[3]}'>{admin[2]}</a>     <a href='{await confirmation_delete_admin(call, admin[1], state)}'>❌</a>\n{trans.translate('Phone number',dest=lang).text}: {admin[4]}\n\n"
        else:
            text += f"{k}. {admin[2]}     <a href='{await confirmation_delete_admin(call,admin[1],state)}'>❌</a>\n{trans.translate('Phone number',dest=lang).text}: {admin[4]}\n\n"
        k += 1
    await call.message.edit_text(text, disable_web_page_preview=True, reply_markup=await objects_markup(None, 'admin', lang))
    
async def confirmation_delete_admin(call: CallbackQuery, user_id, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    await state.update_data(user_id=user_id)
    user = (await db.select_botadmin(chat_id=user_id))[0]
    if user[3]:
        text = trans.translate(f"Adminlar bazasidan <a href='t.me/{user[3]}'>{user[2]}</a> o'chirilsinmi?",dest=lang).text,
    else:
        text = trans.translate(f"Adminlar bazasidan {user[2]} o'chirilsinmi?",dest=lang).text,
    await call.message.answer(text, disable_web_page_preview=True, reply_markup=await confirmation(lang))
    
async def confirmation_delete_user(call: CallbackQuery, user_id, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    await state.update_data(user_id=user_id)
    user = (await db.select_user(user_chat_id=user_id))[0]
    if user[5]:
        text = trans.translate(f"Adminlar bazasidan <a href='t.me/{user[5]}'>{user[2]}</a> o'chirilsinmi?",dest=lang).text,
    else:
        trans.translate(f"Foydalanuvchi {user[2]} bazasidan o'chirilsinmi?",dest=lang).text,
    await call.message.answer(text, disable_web_page_preview=True, reply_markup=await confirmation(lang))
    
@dp.callback_query_handler(text="delete_user:yes", user_id=ADMINS[0])
async def delete_user(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    data = await state.get_data()
    user_id = data.get('user_id')
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if int(user_id) in admin_ids:
        user_full_name = (await db.select_botadmin(chat_id=user_id))[0][2]
        await db.delete_botadmin(user_id)
    else:
        user_full_name = (await db.select_user(user_chat_id=user_id))[0][2]
        await db.delete_user(user_id)
    text = trans.translate(f"{user_full_name} bazadan o'chirildi!",dest=lang).text
    await call.answer(text)
    await call.message.delete()
    
@dp.callback_query_handler(text="delete_user:no", user_id=ADMINS[0])
async def cancel_deleting_user(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    text = trans.translate(f"O'chirish bekor qilindi!",dest=lang).text
    await call.answer(text)
    await call.message.delete()
    
@dp.message_handler(Command("delete_posts"), user_id=ADMINS[0])
async def delete_post(message: Message):
    lang = await db.select_admin_lang(message.from_user.id)
    command_parse = re.compile(r"(/delete_posts) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    n = int(parsed.group(2)) if parsed.group(2) else 4
    comment = parsed.group(3)
    users = await db.select_all_users()
    for user in users:
        try:
            msg = await bot.send_message(chat_id=user[1], text="🚫 Error")
            message_id = msg.message_id
            for i in range(n):
                try:
                    await bot.delete_message(chat_id=user[1], message_id=int(message_id-i))
                except:
                    pass
                asyncio.sleep(00.1)
        except:
            pass
    if comment:
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=comment)
    await message.delete()

# bazadagi admimlar soni
@dp.message_handler(text="/countadmins", user_id=ADMINS[0])
async def get_admins_count(message: Message):
    admin_ids = [id[1] for id in await db.select_all_botadmins()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        count = await db.count_botadmins()
        await message.answer(trans.translate(f'Bazada {count} ta admin mavjud!',dest=lang).text)
        await message.delete()
    else:
        await bot_echo(message)
    
# yangi admin qo'shish
@dp.callback_query_handler(text="admin:add", user_id=ADMINS[0])
async def notification(call: CallbackQuery, state: FSMContext):
    lang = await db.select_admin_lang(call.from_user.id)
    await call.message.answer(trans.translate("Biror Telegram foydalanuvchisining xabarini jo'nating.",dest=lang).text,reply_markup=await cancel_button(lang))
    await AddAdmin.Message.set()
    
# yangi admin qo'shishni berkor qlish
@dp.message_handler(text=["🚫 Bekor qilish","🚫 Cancel", "🚫 Отмена"], state=AddAdmin.Message)
async def cancel(message: Message, state: FSMContext):
    lang = await db.select_admin_lang(message.from_user.id)
    await message.answer(trans.translate("Bekor qilindi!",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
    # ma'lumotlarni saqlash
    data = await state.get_data()
    university_id = data.get('university_id')
    faculty_id = data.get('faculty_id')
    direction_id = data.get('direction_id')
    await state.finish()
    await state.update_data(university_id=university_id)
    await state.update_data(faculty_id=faculty_id)
    await state.update_data(direction_id=direction_id)
    
# bazaga yangi admin qo'shish
@dp.message_handler(state=AddAdmin.Message)
async def add_new_amdin(message: Message, state: FSMContext):
    lang = await db.select_admin_lang(message.from_user.id)
    data = await state.get_data()
    faculty_id = data.get('faculty_id')
    try:
        user_id = message.forward_from.id
        try:
            await db.add_botadmin(chat_id=user_id,faculty_id=faculty_id)
            await message.answer(trans.translate(f"{message.forward_from.full_name} has been joined the database!",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
            # ma'lumotlarni saqlash
            data = await state.get_data()
            university_id = data.get('university_id')
            faculty_id = data.get('faculty_id')
            direction_id = data.get('direction_id')
            await state.finish()
            await state.update_data(university_id=university_id)
            await state.update_data(faculty_id=faculty_id)
            await state.update_data(direction_id=direction_id)
        except:
            await message.answer(trans.translate(f"This user had already been joined the database!",dest=lang).text,reply_markup=await cancel_button(lang))
    except:
        await message.answer(trans.translate(f"Iltimos biror bir foydalanuvchining xabarini jo'nating!",dest=lang).text,reply_markup=await cancel_button(lang))
        
