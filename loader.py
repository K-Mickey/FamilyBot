from aiogram import Bot, Dispatcher

import config
from database.db import DataBase


bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
db = DataBase()
db.create_tables()