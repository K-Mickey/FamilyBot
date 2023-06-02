from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp
from keyboards.inline import main_menu


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    text = "Тебя приветствует семейный бот 😊\nВыбери, что ты хочешь сделать!"
    await message.answer(text, reply_markup=main_menu.get_menu())
