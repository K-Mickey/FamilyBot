from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType

from handlers.main import cmd_start, inline_main_menu_planing
from loader import dp, db
from keyboards import inline
from keyboards.inline.habits import habits_data


class OrderAdd(StatesGroup):
    await_text = State()
    confirm = State()


class OrderDel(StatesGroup):
    confirm = State()


class OrderDelAll(StatesGroup):
    confirm = State()


class OrderInsertActual(StatesGroup):
    confirm = State()


@dp.callback_query_handler(habits_data.filter(action="add_to_plan"))
async def inline_add_to_actual_habits(query: CallbackQuery):
    db.actual_habits_insert(query.message.text)
    await query.message.answer("Запись добавлена в актуальный план")
    await query.answer()


@dp.callback_query_handler(habits_data.filter(action="back_main_menu"))
async def back_to_main_menu(query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    await cmd_start(query.message)


@dp.callback_query_handler(habits_data.filter(action="del_all_notes"))
async def habits_remove_all_notes(query: CallbackQuery):
    text = "Вы уверены, что хотите удалить <b>все записи?</b>"
    await query.message.edit_text(text, reply_markup=inline.choose.confirm(), parse_mode="HTML")
    await query.answer()
    await OrderDelAll.confirm.set()


@dp.callback_query_handler(state=OrderDelAll.confirm, text="yes")
async def habits_remove_all_notes_confirm(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer("Все записи были удалены", show_alert=True)
    db.habits_remove()
    await inline_main_menu_planing(query)


@dp.callback_query_handler(state=OrderDelAll.confirm, text="no")
async def habits_remove_all_notes_cancel(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer("Удаление отменено")
    await habits_show_delete_menu(query)


@dp.callback_query_handler(habits_data.filter(action="add_note"))
async def habits_insert_note(query: CallbackQuery):
    await query.message.edit_text("<i>Отправьте сообщение с новой записью!</i>", parse_mode="HTML")
    await query.answer()
    await OrderAdd.await_text.set()


@dp.message_handler(state=OrderAdd.await_text, content_types=ContentType.TEXT)
async def habits_insert_confirm(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderAdd.next()
    msg_text = f"<i>Добавить данную запись?</i>\n\n{text}"
    await message.answer(msg_text, reply_markup=inline.choose.confirm(), parse_mode="HTML")


@dp.callback_query_handler(state=OrderAdd.confirm, text="no")
async def habits_insert_finish(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer("Добавление отменено")
    await inline_main_menu_planing(query)


@dp.callback_query_handler(state=OrderAdd.confirm, text="yes")
async def habits_insert_cancel(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.habits_insert(data['text'])
    await state.finish()
    await query.answer("Запись успешно добавлена")
    await inline_main_menu_planing(query)


@dp.callback_query_handler(habits_data.filter(action="activate"))
async def habits_info_about_note(query: CallbackQuery, callback_data: dict, state: FSMContext):
    btn_id = int(callback_data["btn_id"])
    actual_note = db.actual_habits_find_note(btn_id)
    if actual_note:
        await query.answer("Данная запись уже есть в актуальном плане!", show_alert=True)
    else:
        note = db.habits_find_note(btn_id)
        await OrderInsertActual.confirm.set()
        await state.update_data(text=note[0])
        await state.update_data(btn_id=str(btn_id))
        await query.answer("Для добавления нажмите ещё раз")


@dp.callback_query_handler(habits_data.filter(action="activate"), state=OrderInsertActual.confirm)
async def habits_insert_into_actual_list(query: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    text = str(data["text"])
    btn_id = int(data["btn_id"])
    await state.finish()
    if btn_id == int(callback_data["btn_id"]):
        db.actual_habits_insert(text, btn_id)
        await query.answer("Запись добавлена")
    else:
        await query.answer()


@dp.callback_query_handler(habits_data.filter(action="habits_delete_menu"))
async def habits_show_delete_menu(query: CallbackQuery):
    buttons = db.habits_get(text=False)
    kb = inline.habits.get_delete_habits(buttons)
    text = "<b>Дважды</b> нажмите на запись, которую хотите удалить." \
        if len(buttons) else "Список пуст, нечего удалять."
    await query.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await query.answer()


@dp.callback_query_handler(habits_data.filter(action="delete_note"))
async def habits_delete_note_activate(query: CallbackQuery, callback_data: dict, state: FSMContext):
    btn_id = int(callback_data["btn_id"])
    await OrderDel.confirm.set()
    await state.update_data(btn_id=str(btn_id))
    await query.answer("Для удаления нажмите ещё раз")


@dp.callback_query_handler(habits_data.filter(action="delete_note"), state=OrderDel.confirm)
async def habits_delete_from_db(query: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    btn_id = int(data["btn_id"])
    if btn_id == int(callback_data["btn_id"]):
        await state.finish()
        db.habits_remove(note_id=btn_id)
        await query.answer("Запись удалена")
        await habits_show_delete_menu(query)
    else:
        await query.answer()
        await state.finish()
