from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from database.db import DataBase


bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBase("database/base.db")
db.create_tables()
