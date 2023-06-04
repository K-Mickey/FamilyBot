from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards import default
from keyboards import inline
from keyboards.inline.habits import habits_data


async def habits_planing_start(message: Message):
    list_habits = db.habits_get()
    await message.answer(f"Вот весь список привычек. Всего {len(list_habits)} записей",
                         reply_markup=default.habits.get_planing_menu())
    for habit in list_habits:
        await message.answer(str(habit[0]), reply_markup=inline.habits.get_plan_kb())


@dp.callback_query_handler(habits_data.filter(action="add_to_plan"))
async def inline_add_to_actual_habits(query: CallbackQuery):
    db.actual_habits_insert(query.message.text)
    await query.message.answer("Запись добавлена в актуальный план")
    await query.answer()


@dp.callback_query_handler(habits_data.filter(action="info"))
async def inline_info_habits(query: CallbackQuery):
    await query.answer()

