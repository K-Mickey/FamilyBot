from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards import inline
from keyboards.inline.habits import habits_data
from keyboards.inline.actual_habits import actual_habits_data


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    text = "Тебя приветствует семейный бот 😊\nВыбери, что ты хочешь сделать!"
    await message.answer(text, reply_markup=inline.main.get_menu())


@dp.message_handler(CommandHelp())
async def cmd_help(message: Message):
    text = "Тут будет располагаться справка"
    await message.answer(text)


@dp.callback_query_handler(habits_data.filter(action="back_habits_menu"))
@dp.callback_query_handler(inline.main.main_data.filter(action="planing"))
async def inline_main_menu_planing(query: CallbackQuery):
    list_habits = db.habits_get(text=False)
    kb = inline.habits.get_habits(list_habits)
    await query.message.edit_text(f"Вот весь список привычек. Всего {len(list_habits)} записей", reply_markup=kb)
    await query.answer()


@dp.callback_query_handler(actual_habits_data.filter(action="back_actual_habits_menu"))
@dp.callback_query_handler(inline.main.main_data.filter(action="actual"))
async def inline_main_menu_actual(query: CallbackQuery):
    list_actual_habits = db.actual_habits_get()
    kb = inline.actual_habits.get_actual_habits(list_actual_habits)
    await query.message.edit_text("Вот список актуальных привычек", reply_markup=kb)
    await query.answer()
