from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from loader import dp
from keyboards.inline import main
from .habits.actual_habits import habits_actual_view_all
from .habits.habits import habits_planing_start


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    text = "Тебя приветствует семейный бот 😊\nВыбери, что ты хочешь сделать!"
    await message.answer(text, reply_markup=main.get_menu())


@dp.callback_query_handler(main.main_data.filter(action="planing"))
async def inline_main_menu_planing(query: CallbackQuery):
    await habits_planing_start(query.message)
    await query.answer()


@dp.callback_query_handler(main.main_data.filter(action="actual"))
async def inline_main_menu_actual(query: CallbackQuery):
    await habits_actual_view_all(query.message)
    await query.answer()
