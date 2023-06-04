from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards import inline, reply
from keyboards.inline.habits import habits_data


class OrderAdd(StatesGroup):
    await_text = State()
    confirm = State()


class OrderDel(StatesGroup):
    confirm = State()


class OrderDelAll(StatesGroup):
    confirm = State()


async def habits_planing_start(message: Message):
    list_habits = db.habits_get()
    await message.answer(f"Вот весь список привычек. Всего {len(list_habits)} записей",
                         reply_markup=reply.habits.get_planing_menu())
    for habit in list_habits:
        await message.answer(str(habit[0]), reply_markup=inline.habits.get_plan_kb())


@dp.callback_query_handler(habits_data.filter(action="delete_from_habits"))
async def habits_inline_remove(query: CallbackQuery, state: FSMContext):
    text = query.message.text
    await state.update_data(text=text)
    msg = f"Вы уверены, что хотите удалить эту запись?\n\n{text}"
    await query.message.answer(msg, reply_markup=inline.choose.confirm())
    await OrderDel.confirm.set()
    await query.answer()


@dp.callback_query_handler(state=OrderDel.confirm, text="yes")
async def habits_inline_remove_finish(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.habits_remove(data['text'])
    await state.finish()
    await query.message.answer("Запись успешно удалена")
    await query.answer()


@dp.callback_query_handler(state=OrderAdd.confirm, text="no")
async def habits_inline_remove_cancel(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.answer("Удаление отменено")
    await query.answer()


@dp.message_handler(text="Удалить все записи из плана")
async def habits_remove_all_notes(message: Message):
    await message.answer("Вы уверены, что хотите удалить все записи?", reply_markup=inline.choose.confirm())
    await OrderDelAll.confirm.set()


@dp.callback_query_handler(state=OrderDelAll.confirm, text="yes")
async def habits_remove_all_notes_confirm(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer()
    db.habits_remove()
    await query.message.answer("Все записи были удалены")


@dp.callback_query_handler(state=OrderDelAll.confirm, text="no")
async def habits_remove_all_notes_cancel(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.answer()
    await query.message.answer("Удаление отменено")


@dp.message_handler(text="Добавить новую запись в план")
async def habits_insert(message: Message):
    await message.answer("Введите новую запись")
    await OrderAdd.await_text.set()


@dp.message_handler(state=OrderAdd.await_text)
async def habits_insert_confirm(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderAdd.next()
    await message.answer(f"Подтвердите ввод\n\n{text}", reply_markup=inline.choose.confirm())


@dp.callback_query_handler(state=OrderAdd.confirm, text="no")
async def habits_insert_finish(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.answer("Добавление отменено")
    await query.message.delete()
    await query.answer()


@dp.callback_query_handler(state=OrderAdd.confirm, text="yes")
async def habits_insert_cancel(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.habits_insert(data['text'])
    await state.finish()
    await query.message.answer("Запись успешно добавлена")
    await query.answer()
