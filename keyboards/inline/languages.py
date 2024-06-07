from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('🇬🇧 English', callback_data='language:en')
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data='language:ru')
        ],
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='language:uz')
        ],
    ])