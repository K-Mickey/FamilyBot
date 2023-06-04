from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.utils.executor import start_polling
import logging

import handlers
from config import LOG_FMT
from loader import dp

logging.basicConfig(level=logging.INFO, format=LOG_FMT, filename="log_file.log")


async def set_commands(dispatcher: Dispatcher):
    await dispatcher.bot.set_my_commands(
        commands=[
            BotCommand("start", "Команда старт"),
            BotCommand("help", "Помощь"),
        ],
        scope=BotCommandScopeDefault(),
    )


async def del_commands(dispatcher: Dispatcher):
    await dispatcher.bot.delete_my_commands(scope=BotCommandScopeDefault())


if __name__ == '__main__':
    start_polling(dp, skip_updates=True, on_startup=set_commands, on_shutdown=del_commands)
