from aiogram import executor

from app.settings import DP
from app import create

if __name__ == '__main__':
    executor.start_polling(DP, skip_updates=True)
