from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

habits_data = CallbackData("habit_id", "action", "btn_id")


def get_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for btn_id, text in buttons:
        kb.add(InlineKeyboardButton(str(text), callback_data=habits_data.new(action="activate", btn_id=str(btn_id))))

    kb.add(
        InlineKeyboardButton("Добавить запись", callback_data=habits_data.new(action="add_note", btn_id="")),
        InlineKeyboardButton("Удаление", callback_data=habits_data.new(action="habits_delete_menu", btn_id="")),
    )
    kb.add(InlineKeyboardButton("<-", callback_data=habits_data.new(action="back_main_menu", btn_id="")))
    return kb


def get_delete_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for btn_id, text in buttons:
        kb.add(InlineKeyboardButton(str(text), callback_data=habits_data.new(action="delete_note", btn_id=str(btn_id))))

    if buttons:
        kb.add(InlineKeyboardButton("Удалить все записи",
                                    callback_data=habits_data.new(action="del_all_notes", btn_id="")))
    kb.add(InlineKeyboardButton("<-", callback_data=habits_data.new(action="back_habits_menu", btn_id="")))
    return kb
