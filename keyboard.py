from aiogram.types.inline_keyboard import (
    InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.types.reply_keyboard import (
    ReplyKeyboardMarkup, KeyboardButton
)

form_buttons = (
    InlineKeyboardButton(text='+1 минута', callback_data='minutes 1'),
    InlineKeyboardButton(text='-1 минута', callback_data='minutes -1'),
    InlineKeyboardButton(text='+30 минут', callback_data='minutes 30'),
    InlineKeyboardButton(text='-30 минут', callback_data='minutes -30'),
    InlineKeyboardButton(text='+1 час', callback_data='hours 1'),
    InlineKeyboardButton(text='-1 час', callback_data='hours -1'),
    InlineKeyboardButton(text='1 день', callback_data='days 1'),
    InlineKeyboardButton(text='-1 день', callback_data='days -1'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel'),
    InlineKeyboardButton(text='Готово!', callback_data='done'),

)
form_keyboard = InlineKeyboardMarkup(row_width=2)
form_keyboard.add(*form_buttons)

main_buttons = (
    # KeyboardButton(text='Что ты можешь?'),
    KeyboardButton(text='Новая задача!'),
)
main_keyboard = ReplyKeyboardMarkup(row_width=1, input_field_placeholder='\/ \/ \/')
main_keyboard.add(*main_buttons)
