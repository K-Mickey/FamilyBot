from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

habits_data = CallbackData("id", "action")
habits_data_with_id = CallbackData("id", "action", "but_id")


def get_actual_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for button in buttons:
        kb.add(InlineKeyboardButton(str(button[0]), callback_data=habits_data.new(action="info")))
    return kb


def get_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for but_id, text in buttons:
        kb.add(InlineKeyboardButton(str(text),
                                    callback_data=habits_data_with_id.new(action="activate", but_id=str(but_id))))
    kb.add(
        InlineKeyboardButton("Добавить запись", callback_data=habits_data.new(action="add_note")),
        InlineKeyboardButton("Удаление", callback_data=habits_data.new(action="habits_delete_menu")),
    )
    kb.add(InlineKeyboardButton("<-", callback_data=habits_data.new(action="back_main_menu")))
    return kb


def get_delete_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for but_id, text in buttons:
        kb.add(InlineKeyboardButton(str(text),
                                    callback_data=habits_data_with_id.new(action="delete_note", but_id=str(but_id))))
    kb.add(InlineKeyboardButton("Удалить все записи", callback_data=habits_data.new(action="del_all_notes")))
    kb.add(InlineKeyboardButton("<-", callback_data=habits_data.new(action="back_habits_menu")))
    return kb


def get_plan_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Добавить в план", callback_data=habits_data.new(action="add_to_plan")),
        InlineKeyboardButton("Удалить", callback_data=habits_data.new(action="delete_from_habits")),
    )
    return kb
