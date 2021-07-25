import datetime as dt
import asyncio
from aiogram import types, Bot, executor, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from keyboard import main_keyboard, form_keyboard

FORMAT = '%H:%M %d.%m.%Y'
FORMAT_TIME = '%H:%M'
FORMAT_DATE = '%d.%m.%Y'


class OrderCreate(state.StatesGroup):
    waiting_for_form = state.State()
    waiting_for_message = state.State()


# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        'Привет!\nтеперь я твой дневник!'
        'Чтобы зависать что-то нажми "Новая задача!"',
        reply_markup=main_keyboard
    )


# @dp.message_handler(text='Новая задача!')
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


# @dp.callback_query_handler()
async def change_message(data: types.CallbackQuery, state: FSMContext):
    now = dt.datetime.now()
    state_date = await state.get_data()
    date = state_date.get('date', now)
    if data.data == 'done':
        await state.update_data(date=date)
        await OrderCreate.next()
        await data.message.answer(
            text='Напишите послание', reply_markup=ReplyKeyboardRemove())
        return
    date += in_buttons(data.data)
    date = now if date < now else date
    text = (f'Дата: {date.strftime(FORMAT_DATE)}\n'
            f'Время: {date.strftime(FORMAT_TIME)}\n')
    if data.message.text != text:
        await data.message.edit_text(
            text=text.format(
                date.strftime(FORMAT_DATE), date.strftime(FORMAT_TIME)),
            reply_markup=form_keyboard)
        return await state.update_data(date=date)
    return


async def finish(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer('Готово!', reply_markup=main_keyboard)
    data = await state.get_data()
    await state.finish()
    now = dt.datetime.now()
    timedelta = data['date'] - now
    print(timedelta.total_seconds())
    await asyncio.sleep(timedelta.total_seconds())
    await message.answer(data['message'])


def register(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=('start', 'help'))
    dp.register_message_handler(
        new_dials, Text(equals='Новая задача!', ignore_case=True)
    )
    dp.register_callback_query_handler(
        change_message, state=OrderCreate.waiting_for_form
    )
    dp.register_message_handler(finish, state=OrderCreate.waiting_for_message)


