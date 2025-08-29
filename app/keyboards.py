from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Профиль')],
        [KeyboardButton(text='Крутилки')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Жми на кнопку')


twisters = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Крутилка 1')],
        [KeyboardButton(text='Крутилка 2')],
        [KeyboardButton(text='Сменить ставку')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Жми на кнопку')

profile = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Назад')],
        [KeyboardButton(text='Пополнить баланс')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Жми на кнопку')