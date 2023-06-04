from aiogram.types import ReplyKeyboardMarkup


def get_planing_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add("Добавить новую запись", "Удалить все записи")
    return kb
