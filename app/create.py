import asyncio, datetime as dt
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from keyboard import main_keyboard, form_keyboard
from app.settings import DP, FORMAT_DATE, FORMAT_TIME, ADMINS
from .db import Diary

dp = DP

class OrderCreate(state.StatesGroup):
    waiting_for_form = state.State()
    waiting_for_message = state.State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    print(message.chat.id)
    await message.answer(
        'Привет!\nтеперь я твой дневник!'
        'Чтобы зависать что-то нажми "Новая задача!"',
        reply_markup=main_keyboard
    )

@dp.message_handler(text='Новая задача!')
async def new_dials(message: types.Message):
    date = dt.datetime.now()
    text = (f'Дата: {date.strftime(FORMAT_DATE)}\n'
            f'Время: {date.strftime(FORMAT_TIME)}\n')
    await OrderCreate.waiting_for_form.set()
    await message.answer(text, reply_markup=form_keyboard)


def in_buttons(data: str):
    if data == 'done':
        return dt.timedelta()
    reform_data = {
        data.split()[0]: int(data.split()[1])
    }
    delta = dt.timedelta(**reform_data)
    return delta


@dp.callback_query_handler(state=OrderCreate)
async def change_message(data: types.CallbackQuery, state: FSMContext):
    now = dt.datetime.now()
    state_data = await state.get_data()
    obj = state_data.get('obj', None) or Diary(date=now, chat_id=data.message.chat.id)
    error_text = ''
    match data.data:
        case 'done' if obj.date < now:
            error_text = 'К сожалению, этот бот не может отправить сообщение в прошлое\n'
            obj.date = now
            await state.update_data(obj=obj)
        case 'done':
            await OrderCreate.next()
            await state.update_data(obj=obj)
            await data.message.edit_text(
                text='Напишите послание',  # reply_markup=types.reply_keyboard.ReplyKeyboardRemove
            )
            return
        case 'cancel':
            await state.reset_data()
            await state.finish()
            await data.message.edit_text(text='Отменено')
            return
        case _:
            obj.date += in_buttons(data.data)
    text = (
        error_text + 
        f'Дата: {obj.date.strftime(FORMAT_DATE)}\n'
        f'Время: {obj.date.strftime(FORMAT_TIME)}\n'
    )
    await state.update_data(obj=obj)
    await data.message.edit_text(
        text=text, reply_markup=form_keyboard
    )

@dp.message_handler(state=OrderCreate)
async def finish(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    obj = state_data.get('obj', None)
    obj.message = message.text
    obj.save()
    await state.reset_data()
    await state.finish()
    await message.answer('Готово!', reply_markup=main_keyboard)

@dp.message_handler(commands=['start_polling'])
async def check_db(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer(text='Вы не админ!')
    while True:
        ls = Diary.all(limit=1)
        if len(ls) == 0:
            await asyncio.sleep(1)
            continue
        obj = ls[0]
        if obj.date <= dt.datetime.now():
            await dp.bot.send_message(chat_id=obj.chat_id, text=obj.message)
            obj.delete()
        await asyncio.sleep(1)
