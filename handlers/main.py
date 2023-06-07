from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from keyboards import inline
from keyboards.inline.habits import habits_data
from keyboards.inline.actual_habits import actual_habits_data


@dp.message_handler(CommandStart(), state="*")
async def cmd_start(message: Message, state: FSMContext = None):
    if state:
        await state.finish()
    text = "Тебя приветствует семейный бот 😊\nВыбери, что ты хочешь сделать!"
    await message.answer(text, reply_markup=inline.main.get_menu())


@dp.message_handler(CommandHelp(), state="*")
async def cmd_help(message: Message, state: FSMContext = None):
    if state:
        await state.finish()
    text = "Тут будет располагаться справка"
    await message.answer(text)


@dp.callback_query_handler(habits_data.filter(action="back_habits_menu"))
@dp.callback_query_handler(inline.main.main_data.filter(action="planing"))
async def inline_main_menu_planing(query: CallbackQuery):
    list_habits = db.habits_get(text=False)
    n_habits = len(list_habits)
    kb = inline.habits.get_habits(list_habits)

    text = f"Всего записей: <i>{n_habits}.</i>\n" \
           f"Для добавления в актуальные <b>дважды</b> тапните на нужную кнопку." \
        if n_habits else "Список пуст, но Вы можете его пополнить!"

    await query.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await query.answer()


@dp.callback_query_handler(actual_habits_data.filter(action="back_actual_habits_menu"))
@dp.callback_query_handler(inline.main.main_data.filter(action="actual"))
async def inline_main_menu_actual(query: CallbackQuery):
    list_actual_habits = db.actual_habits_get()
    kb = inline.actual_habits.get_actual_habits(list_actual_habits)
    n_actual_habits = len(list_actual_habits)

    text = f"Всего актуальных записей: <i>{n_actual_habits}.</i>" \
        if n_actual_habits else "Актуальный список пуст.\nМожете его пополнить в <i>Меню планирования!</i>"

    await query.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await query.answer()
