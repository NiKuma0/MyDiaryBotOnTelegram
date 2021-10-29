import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

if not load_dotenv():
    assert 'Not found .env file'

# env variables
ADMINS = list(map(int, os.getenv('ADMINS').split(',')))
API_TOKEN = os.getenv('TOKEN')
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# settings of aiogram
BOT = Bot(token=API_TOKEN)
DP = Dispatcher(BOT, storage=MemoryStorage())

# date and time format for output
FORMAT = '%H:%M %d.%m.%Y'
FORMAT_TIME = '%H:%M'
FORMAT_DATE = '%d.%m.%Y'

# settings of datebase
PATH_DB = os.path.join(DIR, 'db.sqlite')
