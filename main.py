from aiogram.utils.executor import start_polling
import logging

import handlers
from config import LOG_FMT
from loader import dp

logging.basicConfig(level=logging.DEBUG, format=LOG_FMT, filename="log_file.log")

if __name__ == '__main__':
    start_polling(dp)
