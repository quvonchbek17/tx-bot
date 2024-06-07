from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAdmin(StatesGroup):
    Message = State()

class Contact(StatesGroup):
    contact_admin = State()