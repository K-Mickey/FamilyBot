from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards.inline import choose
from keyboards.inline import custom
from keyboards.inline.main_menu import habits


class OrderAdd(StatesGroup):
    await_text = State()
    confirm = State()


@dp.callback_query_handler(habits.filter(action="add"))
async def inline_habits_add(query: CallbackQuery):
    await query.message.answer("Введите новую запись")
    await OrderAdd.await_text.set()
    await query.answer()


@dp.message_handler(state=OrderAdd.await_text)
async def await_text(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderAdd.next()
    await message.answer(f"Подтвердите ввод\n\n{text}", reply_markup=choose.confirm())


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


@dp.callback_query_handler(habits.filter(action="view_all"))
async def inline_habits_view_all(query: CallbackQuery):
    list_habits = db.habits_get()
    kb = custom.get_kb(list_habits)
    await query.message.answer("Вот список", reply_markup=kb)
    await query.answer()
