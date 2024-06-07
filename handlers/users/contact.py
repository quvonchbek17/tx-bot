from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from states.manage import Contact
from keyboards.default.mainMenu import main_menu
from keyboards.default.settings import cancel_button

from googletrans import Translator
trans = Translator()


@dp.message_handler(text=["📤 Murojaat uchun","📤 For reference","📤 Для ознакомления"])
async def contact_handler(msg: Message):
    lang = (await db.select_user(chat_id=msg.from_user.id))[0][5]
    text = trans.translate("Muammo yoki murojaatingiz bo'lsa yozib jo'nating, tez orada javob beramiz!",dest=lang).text
    await msg.answer(text=text, reply_markup=await cancel_button(lang))
    await Contact.contact_admin.set()

@dp.message_handler(text=["🚫 Bekor qilish","🚫 Cancel", "🚫 Отмена"], state=Contact.contact_admin)
async def cancel(msg: Message, state: FSMContext):
    lang = (await db.select_user(chat_id=msg.from_user.id))[0][5]
    await msg.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await main_menu(lang))
    await state.finish()

@dp.message_handler(state=Contact.contact_admin, content_types=ContentType.all())
async def send_text(msg: Message, state: FSMContext):
    lang = (await db.select_user(chat_id=msg.from_user.id))[0][5]
    await msg.forward(chat_id=ADMINS[0])
    await msg.answer(trans.translate("Xabar jo'natildi 📤",dest=lang).text)
    await msg.answer(trans.translate("Asosiy menyu",dest=lang).text, reply_markup=await main_menu(lang))
    await state.finish()