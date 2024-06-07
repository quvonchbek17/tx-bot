from aiogram.dispatcher.filters.state import StatesGroup, State


class SignUp(StatesGroup):
    register = State()

class Register(StatesGroup):
    full_name = State()
    phone_number = State()
    university = State()
    faculty = State()
    direction = State()
    course = State()
    education = State()
    group = State()
    
class AdminRegister(StatesGroup):
    full_name = State()
    phone_number = State()