from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import keyboards.default.habits
from loader import dp, db
from keyboards import default
from keyboards import inline
from keyboards.inline.habits import habits_data


class OrderAdd(StatesGroup):
    await_text = State()
    confirm = State()


class OrderDel(StatesGroup):
    confirm = State()


async def habits_inline_view_all(message: Message):
    list_actual_habits = db.actual_habits_get()
    kb = inline.habits.get_actual_habits(list_actual_habits)
    await message.answer("Вот список актуальных привычек", reply_markup=kb)


async def habits_planing_start(message: Message):
    list_habits = db.habits_get()
    await message.answer(f"Вот весь список привычек. Всего {len(list_habits)} записей",
                         reply_markup=keyboards.default.habits.get_planing_menu())
    for habit in list_habits:
        await message.answer(str(habit[0]), reply_markup=inline.habits.get_plan_kb())


@dp.callback_query_handler(habits_data.filter(action="delete_from_habits"))
async def inline_habits_del(query: CallbackQuery, state: FSMContext):
    text = query.message.text
    await state.update_data(text=text)
    msg = f"Вы уверены, что хотите удалить эту запись?\n\n{text}"
    await query.message.answer(msg, reply_markup=inline.choose.confirm())
    await OrderDel.confirm.set()
    await query.answer()


@dp.callback_query_handler(state=OrderDel.confirm, text="yes")
async def inline_habits_del_yes(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.habits_remove(data['text'])
    await state.finish()
    await query.message.answer("Запись успешно удалена")
    await query.answer()


@dp.callback_query_handler(state=OrderAdd.confirm, text="no")
async def inline_habits_del_no(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.answer("Удаление отменено")
    await query.answer()


@dp.callback_query_handler(habits_data.filter(action="add_to_plan"))
async def inline_add_to_actual_habits(query: CallbackQuery):
    db.actual_habits_insert(query.message.text)
    await query.message.answer("Запись добавлена в актуальный план")
    await query.answer()


@dp.message_handler(text="Добавить новую запись")
async def habits_add(message: Message):
    await message.answer("Введите новую запись")
    await OrderAdd.await_text.set()


@dp.message_handler(state=OrderAdd.await_text)
async def await_text(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderAdd.next()
    await message.answer(f"Подтвердите ввод\n\n{text}", reply_markup=inline.choose.confirm())


@dp.callback_query_handler(state=OrderAdd.confirm, text="no")
async def habits_cancel(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.answer("Добавление отменено")
    await query.message.delete()
    await query.answer()


@dp.callback_query_handler(state=OrderAdd.confirm, text="yes")
async def habits_insert(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.habits_insert(data['text'])
    await state.finish()
    await query.message.answer("Запись успешно добавлена")
    await query.answer()


@dp.callback_query_handler(habits_data.filter(action="info"))
async def inline_info_habits(query: CallbackQuery):
    await query.answer()


