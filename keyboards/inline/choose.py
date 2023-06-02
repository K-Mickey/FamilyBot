from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Да", callback_data="yes"),
        InlineKeyboardButton("Нет", callback_data="no"),
    )
    return kb
