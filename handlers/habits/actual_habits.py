from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards.inline.habits import habits_data
from keyboards import inline


async def habits_actual_view_all(message: Message):
    list_actual_habits = db.actual_habits_get()
    kb = inline.habits.get_actual_habits(list_actual_habits)
    await message.answer("Вот список актуальных привычек", reply_markup=kb)


@dp.callback_query_handler(habits_data.filter(action="add_to_plan"))
async def inline_add_to_actual_habits(query: CallbackQuery):
    db.actual_habits_insert(query.message.text)
    await query.message.answer("Запись добавлена в актуальный план")
    await query.answer()


@dp.callback_query_handler(habits_data.filter(action="info"))
async def inline_info_habits(query: CallbackQuery):
    await query.answer()
