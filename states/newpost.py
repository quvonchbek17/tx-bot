from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPost(StatesGroup):
    NewMessage = State()
    SMA = State()
    Ad = State()
    Confirm = State()
