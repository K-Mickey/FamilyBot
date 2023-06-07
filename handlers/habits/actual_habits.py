from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from handlers.main import cmd_start, inline_main_menu_actual
from loader import dp, db
from keyboards import inline
from keyboards.inline.actual_habits import actual_habits_data


class ActOrderDel(StatesGroup):
    confirm = State()


class ActOrderDelAll(StatesGroup):
    confirm = State()


@dp.callback_query_handler(actual_habits_data.filter(action="back_main_menu"))
async def back_to_main_menu(query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    await cmd_start(query.message)


@dp.callback_query_handler(actual_habits_data.filter(action="info"))
async def inline_info_habits(query: CallbackQuery):
    await query.answer()


@dp.callback_query_handler(actual_habits_data.filter(action="actual_habits_delete_menu"))
async def actual_habits_show_delete_menu(query: CallbackQuery):
    list_actual_habits = db.actual_habits_get(text=False)
    kb = inline.actual_habits.get_delete_actual_habits(list_actual_habits)
    text = "Нажмите <b>дважды на запись</b>, которую хотите удалить." \
        if list_actual_habits else "Нет записей для удаления."

    await query.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await query.answer()


@dp.callback_query_handler(actual_habits_data.filter(action="delete_actual_note"))
async def actual_habits_delete(query: CallbackQuery, callback_data: dict, state: FSMContext):
    btn_id = int(callback_data["btn_id"])
    await state.update_data(btn_id=btn_id)
    await ActOrderDel.confirm.set()
    await query.answer("Для удаления нажмите еще раз")


@dp.callback_query_handler(actual_habits_data.filter(action="delete_actual_note"), state=ActOrderDel.confirm)
async def actual_habits_delete_confirm(query: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    cur_btn_id = int(data["btn_id"])
    prev_btn_id = int(callback_data["btn_id"])
    await state.finish()
    if cur_btn_id == prev_btn_id:
        db.actual_habits_remove(note_id=cur_btn_id)
        await query.answer("Запись удалена")
        await actual_habits_show_delete_menu(query)
    else:
        await query.answer()


@dp.callback_query_handler(actual_habits_data.filter(action="del_all_notes"))
async def actual_habits_remove_all_notes(query: CallbackQuery):
    await ActOrderDelAll.confirm.set()
    text = "Вы уверены, что хотите удалить <b>все записи?</b>"
    await query.message.edit_text(text, reply_markup=inline.choose.confirm(), parse_mode="HTML")
    await query.answer()


@dp.callback_query_handler(state=ActOrderDelAll.confirm, text="yes")
async def actual_habits_remove_all_notes_accept(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer("Все сообщения были удалены", show_alert=True)
    db.actual_habits_remove()
    await inline_main_menu_actual(query)


@dp.callback_query_handler(state=ActOrderDelAll.confirm, text="no")
async def actual_habits_remove_all_notes_cancel(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer("Удаление отменено")
    await actual_habits_show_delete_menu(query)
