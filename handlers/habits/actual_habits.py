from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards import inline
from keyboards.inline.actual_habits import actual_habits_data


@dp.callback_query_handler(actual_habits_data.filter(action="info"))
async def inline_info_habits(query: CallbackQuery):
    await query.answer()


@dp.callback_query_handler(actual_habits_data.filter(action="actual_habits_delete_menu"))
async def actual_habits_show_delete_menu(query: CallbackQuery):
    list_actual_habits = db.actual_habits_get(text=False)
    kb = inline.actual_habits.get_delete_actual_habits(list_actual_habits)
    await query.message.edit_text("Нажмите дважды на запись, которую хотите удалить", reply_markup=kb)
    await query.answer()
