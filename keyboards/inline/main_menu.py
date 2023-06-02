from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

habits = CallbackData("id", "action")


def get_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Добавить запись", callback_data=habits.new(action="add")))
    kb.add(InlineKeyboardButton("Посмотреть все записи", callback_data=habits.new(action="view_all")))
    return kb
