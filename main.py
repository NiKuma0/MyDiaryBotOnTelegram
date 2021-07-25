from aiogram import Bot, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.create import register

API_TOKEN = '1731291683:AAFuZGeMvIf_R3oLkoLRtcyCxRqsgVG4oUA'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    register(dp)
    executor.start_polling(dp, skip_updates=True)
