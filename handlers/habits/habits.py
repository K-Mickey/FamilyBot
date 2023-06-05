from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType

from handlers.main import cmd_start, inline_main_menu_planing
from loader import dp, db
from keyboards import inline
from keyboards.inline.habits import habits_data, habits_data_with_id


class OrderAdd(StatesGroup):
    await_text = State()
    confirm = State()


class OrderDel(StatesGroup):
    confirm = State()


class OrderDelAll(StatesGroup):
    confirm = State()


class OrderInsertActual(StatesGroup):
    confirm = State()


@dp.callback_query_handler(habits_data.filter(action="back_main_menu"))
async def back_to_main_menu(query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    await cmd_start(query.message)


@dp.callback_query_handler(habits_data.filter(action="del_all_notes"))
async def habits_remove_all_notes(query: CallbackQuery):
    await query.message.edit_text("Вы уверены, что хотите удалить все записи?", reply_markup=inline.choose.confirm())
    await query.answer()
    await OrderDelAll.confirm.set()


@dp.callback_query_handler(state=OrderDelAll.confirm, text="yes")
async def habits_remove_all_notes_confirm(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer()
    db.habits_remove()
    await query.message.edit_text("Все записи были удалены")


@dp.callback_query_handler(state=OrderDelAll.confirm, text="no")
async def habits_remove_all_notes_cancel(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer()
    await query.message.edit_text("Удаление отменено")


@dp.callback_query_handler(habits_data.filter(action="add_note"))
async def habits_insert_note(query: CallbackQuery):
    await query.message.edit_text("Введите новую запись")
    await query.answer()
    await OrderAdd.await_text.set()


@dp.message_handler(state=OrderAdd.await_text, content_types=ContentType.TEXT)
async def habits_insert_confirm(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderAdd.next()
    await message.answer(f"Подтвердите ввод\n\n{text}", reply_markup=inline.choose.confirm())


@dp.callback_query_handler(state=OrderAdd.confirm, text="no")
async def habits_insert_finish(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text("Добавление отменено")
    await query.answer()


@dp.callback_query_handler(state=OrderAdd.confirm, text="yes")
async def habits_insert_cancel(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.habits_insert(data['text'])
    await state.finish()
    await query.message.answer("Запись успешно добавлена")
    await query.answer()
    await inline_main_menu_planing(query)


@dp.callback_query_handler(habits_data_with_id.filter(action="activate"))
async def habits_info_about_note(query: CallbackQuery, callback_data: dict, state: FSMContext):
    but_id = int(callback_data["but_id"])
    actual_note = db.actual_habits_find_note(but_id)
    if actual_note:
        await query.answer("Данная запись уже есть в актуальном плане", show_alert=True)
    else:
        note = db.habits_find_note(but_id)
        await OrderInsertActual.confirm.set()
        await state.update_data(text=note[0])
        await state.update_data(but_id=str(but_id))
        await query.answer("Для добавления нажмите ещё раз")


@dp.callback_query_handler(habits_data_with_id.filter(action="activate"), state=OrderInsertActual.confirm)
async def habits_insert_into_actual_list(query: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    text = str(data["text"])
    but_id = int(data["but_id"])
    if but_id == int(callback_data["but_id"]):
        await state.finish()
        db.actual_habits_insert(text, but_id)
        await query.answer("Запись добавлена")
    else:
        await query.answer()
        await state.finish()


@dp.callback_query_handler(habits_data.filter(action="habits_delete_menu"))
async def habits_show_delete_menu(query: CallbackQuery):
    buttons = db.habits_get(text=False)
    kb = inline.habits.get_delete_habits(buttons)
    await query.message.edit_text("Выберите записи для удаления", reply_markup=kb)
    await query.answer()


@dp.callback_query_handler(habits_data_with_id.filter(action="delete_note"))
async def habits_delete_note_activate(query: CallbackQuery, callback_data: dict, state: FSMContext):
    but_id = int(callback_data["but_id"])
    await OrderDel.confirm.set()
    await state.update_data(but_id=str(but_id))
    await query.answer("Для удаления нажмите ещё раз")


@dp.callback_query_handler(habits_data_with_id.filter(action="delete_note"), state=OrderDel.confirm)
async def habits_delete_from_db(query: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    but_id = int(data["but_id"])
    if but_id == int(callback_data["but_id"]):
        await state.finish()
        db.habits_remove(note_id=but_id)
        await query.answer("Запись удалена")
        await habits_show_delete_menu(query)
    else:
        await query.answer()
        await state.finish()
