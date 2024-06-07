from aiogram.dispatcher.filters.state import any_state
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline.languages import languages
from keyboards.default.mainMenu import main_menu

from googletrans import Translator
trans = Translator()


@dp.message_handler(text="/stop", state=any_state)
@dp.my_chat_member_handler(state=any_state)
async def delete_user(member: types.ChatMemberUpdated, state: FSMContext):
    await state.finish()
    id = member.from_user.id
    admin_ids = [record['chat_id'] for record in await db.select_admin_ids()]
    if id in admin_ids:
        user = (await db.select_botadmin(chat_id=id))[0]
        await db.delete_botadmin(chat_id=id)
        language = (await db.select_botadmin(chat_id=ADMINS[0]))[0][5]
        faculty = await db.select_faculties(id=user[6])
        university = (await db.select_university(id=faculty[0][2]))[0][1]
        text = trans.translate(f"🗑 {member.from_user.get_mention(as_html=True)} has been deleted from the admin database",dest=language).text + '\n'
        text += trans.translate("ID:",dest=language).text + '  ' + str(user[1]) + '\n'
        text += trans.translate("To'liq ismi:",dest=language).text + f"  <a href='{user[3]}'>{user[2]}</a>\n"
        text += trans.translate("Telefon raqam:",dest=language).text + '  '  + user[4] + '\n'
        text += trans.translate("University:",dest=language).text + '  ' + university + '\n'
        text += trans.translate("Faculty:",dest=language).text + '  '  + user[6] + '\n'
        text += "#delete_admin"
        await bot.send_message(chat_id=ADMINS[0],text=text)
    else:
        user = (await db.select_user(chat_id=id))[0]
        try:
            group_name = (await db.select_groups(id=user[6]))[0][1]
        except:
            group_name = 'None'
        await db.delete_user(chat_id=id)
        # adminga xabar berish
        for admin_id in ADMINS:
            language = (await db.select_botadmin(chat_id=admin_id))[0][5]
            text = trans.translate(f"🗑 {member.from_user.get_mention(as_html=True)} has been deleted from the database",dest=language).text + '\n'
            text += trans.translate("ID:",dest=language).text + '  ' + str(user[1]) + '\n'
            text += trans.translate("To'liq ismi:",dest=language).text + '  '  + f"<a href='{user[6]}'>{user[3]}</a>\n"
            text += trans.translate("Telefon raqam:",dest=language).text + '  ' + str(user[4]) + '\n'
            text += trans.translate("Group name:",dest=language).text + '  '  + group_name + '\n'
            text += "#delete_user"
            await bot.send_message(chat_id=admin_id,text=text)
