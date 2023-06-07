from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

actual_habits_data = CallbackData("actual_id", "action", "btn_id")


def get_actual_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for _, button, _ in buttons:
        btn = str(button)
        kb.add(InlineKeyboardButton(btn, callback_data=actual_habits_data.new(action="info", btn_id="")))

    if buttons:
        kb.add(InlineKeyboardButton("Меню удаления", callback_data=actual_habits_data.new(
            action="actual_habits_delete_menu", btn_id="")))
    kb.add(InlineKeyboardButton("<-", callback_data=actual_habits_data.new(action="back_main_menu", btn_id="")))
    return kb


def get_delete_actual_habits(buttons: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for btn_id, text, _ in buttons:
        btn_id = str(btn_id)
        text = str(text)
        kb.add(InlineKeyboardButton(text, callback_data=actual_habits_data.new(
            action="delete_actual_note", btn_id=btn_id)))
    if buttons:
        kb.add(InlineKeyboardButton("Удалить все записи", callback_data=actual_habits_data.new(
            action="del_all_notes", btn_id="")))
    kb.add(InlineKeyboardButton("<-", callback_data=actual_habits_data.new(
        action="back_actual_habits_menu", btn_id="")))
    return kb
