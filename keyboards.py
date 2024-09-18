from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='Почати'),KeyboardButton(text='Відвідав')]], input_field_placeholder='Оберіть пункт меню',resize_keyboard=True)

entercode = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='Назад')]], input_field_placeholder='Введіть код',resize_keyboard=True )

