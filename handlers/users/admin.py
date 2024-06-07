import asyncio

from aiogram.types import Message, ContentType, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin import admin_menu
from keyboards.inline.manage_post import confirmation_keyboard, post_callback
from keyboards.default.mainMenu import main_menu
from loader import dp, db, bot
from states.newpost import NewPost
from utils.misc.echo import bot_echo

from googletrans import Translator
trans = Translator()


@dp.message_handler(text = ["/ac",'🔑 Admin buyruqlari','🔑 Admin commands','🔑 Команды администратора'])
async def get_admin_commands(message: Message):
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        text = ("/newpost - " + trans.translate("<i>Foydalanuvchilarga xabar jo'natish</i>",dest=lang).text + '\n')
        text += ("/allusers - " + trans.translate("<i>Barcha foydalanuvchilar haqida ma'lumot</i>",dest=lang).text + '\n')
        text += ("/cleandb - " + trans.translate("<i>Ma'lumotlar bazasini tozalash</i>",dest=lang).text + '\n')
        text += ("/countusers - " + trans.translate("<i>Foydalanuvchilar soni</i>",dest=lang).text + '\n')
        # text += ("/countadmins - " + trans.translate("Adminlar soni",dest=lang).text + '\n')
        await message.answer(text)
        await message.delete()
    else:
        await bot_echo(message)
        
@dp.message_handler(text="/allusers")
async def get_all_users(message: Message):
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        users = await db.select_all_users()
        text, k, n = '', 0, 1
        for user in users:
            text += f"<b>{str(n)}.</b> " + str([str(item) for item in user]) + '\n\n'
            k += 1
            n += 1
            if k == 20 or user == users[-1]:
                print(text)
                await message.answer(text)
                text, k = '', 0
        await message.delete()
    else:
        await bot_echo(message)
        
@dp.message_handler(text="/cleandb")
async def get_all_users(message: Message):
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        await message.answer(trans.translate("Baza tozalandi!",dest=lang).text)
        await message.delete()
    else:
        await bot_echo(message)

@dp.message_handler(text="/countusers")
async def get_users_count(message: Message):
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        count = await db.count_users()
        await message.answer(trans.translate(f'Bazada {count} ta foydalanuvchi mavjud!',dest=lang).text)
        await message.delete()
    else:
        await bot_echo(message)

@dp.message_handler(text=["📨 Отправляйте сообщения пользователям","📨 Foydalanuvchilarga xabar jo'natish","/newpost","📨 Send messages to users"])
async def create_post(message: Message):
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if message.from_user.id in admin_ids:
        lang = await db.select_admin_lang(message.from_user.id)
        await message.answer(trans.translate("Chop etish uchun post yuboring.",dest=lang).text,reply_markup=ReplyKeyboardRemove(True))
        await NewPost.NewMessage.set()
    else:
        await bot_echo(message)
        
@dp.message_handler(state=NewPost.NewMessage, content_types=ContentType.all())
async def enter_message(message: Message, state: FSMContext):
    lang = await db.select_admin_lang(message.from_user.id)
    await message.reply(text=trans.translate("Postni chop etilishini xohlaysizmi?",dest=lang).text,
                        reply_markup=await confirmation_keyboard('create_post',lang))
    await state.finish()

@dp.callback_query_handler(post_callback.filter(action="post"))
async def approve_post(call: CallbackQuery):
    lang = await db.select_admin_lang(call.from_user.id)
    await call.answer(trans.translate("Chop etishga ruhsat berdingiz.",dest=lang).text)
    await call.message.edit_reply_markup()
    message = call.message.reply_to_message
    # direction_ids = [direction[0] for direction in (await db.select_directions(faculty_id=faculty_id))]
    # for direction_id in direction_ids:
    #     group_ids = [mix[4] for mix in (await db.select_mix(direction_id=direction_id))]
    #     for group_id in group_ids:
    #         users = await db.select_user(group_id=group_id)
    #         for user in users:
    #             try:
    #                 await message.send_copy(chat_id=user[1])
    #             except:
    #                 pass
    #             asyncio.sleep(00.1)
    for user_id in [record['chat_id'] for record in await db.select_user_ids()]:
        try:
            await message.send_copy(chat_id=user_id)
        except:
            pass
        asyncio.sleep(00.1)
    await call.message.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await admin_menu(lang))
    # adminga xabar berish
    admin_lang = await db.select_admin_lang(chat_id=ADMINS[0])
    # faculty = (await db.select_faculties(id=faculty_id))[0]
    # university = (await db.select_university(id=faculty[2]))[0][1]
    # text = trans.translate(f"{university} universitetining {faculty[1]} fakultetining admini {call.from_user.get_mention(as_html=True)} foydalanuvchilarga xabar jo'natdi.",dest=admin_lang).text
    await bot.send_message(chat_id=ADMINS[0],text=f"Admin {call.from_user.get_mention(as_html=True)} foydalanuvchilarga xabar jo'natdi.")
    await message.send_copy(chat_id=ADMINS[0])

@dp.callback_query_handler(post_callback.filter(action="cancel"))
async def decline_post(call: CallbackQuery):
    lang = await db.select_admin_lang(call.from_user.id)
    await call.answer(trans.translate("Post rad etildi.",dest=lang).text)
    await call.message.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await admin_menu(lang))
    await call.message.edit_reply_markup()
