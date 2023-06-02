from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_kb(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for button in buttons:
        kb.add(InlineKeyboardButton(str(button[0]), callback_data="view"))
    return kb
