from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

main_data = CallbackData("id", "action")


def get_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Актуальный план", callback_data=main_data.new(action="actual")))
    kb.add(InlineKeyboardButton("Планирование", callback_data=main_data.new(action="planing")))
    return kb
