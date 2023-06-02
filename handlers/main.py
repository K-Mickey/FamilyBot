from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db


@dp.message_handler(commands="get")
async def cmd_add(message: Message):
    ls = db.get_all()
    kb = InlineKeyboardMarkup()
    for s in ls:
        s = str(s[0])
        kb.insert(InlineKeyboardButton(s, callback_data='show'))
    await message.answer("Список", reply_markup=kb)


@dp.message_handler()
async def cmd_start(message: Message):
    await message.answer("Hello")
    db.insert(message.text)

