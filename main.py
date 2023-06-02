from aiogram.utils.executor import start_polling
import logging

import handlers
from loader import dp

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    start_polling(dp)
