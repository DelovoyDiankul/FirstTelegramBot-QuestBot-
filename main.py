import asyncio, logging
from aiogram import Bot, Dispatcher, types, F 
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import request
import keyboards as keyb
import db
import time
import random
from db import locations

bot = Bot(token = '7519027128:AAHqGQ1H2FFBOngAai9TfKnSwg0Epj8UN7g')
disp = Dispatcher()

class Register(StatesGroup):
    GetCode = State() 

location_status = {loc: False for loc in locations}
user_quests = {}

def get_random_location(user_id):
    free_locations = [loc for loc, status in location_status.items() if not status]
    if free_locations:
        return random.choice(free_locations)
    return None

def check_quest_status(user_id):
    return user_quests.get(user_id, (False, []))[0] 

def start_quest(user_id):
    user_quests[user_id] = (True, []) 

def update_location_status(location):
    location_status[location] = True

def visit_location(user_id):
    if check_quest_status(user_id):
        visited_locations = user_quests[user_id][1]

        if len(visited_locations) >= len(locations):
            return "Всі локації вже відвідані."

        location = get_random_location(user_id)
        if location:
            update_location_status(location)
            visited_locations.append(location)  
            return (f"Ваша наступна локація: {location}")
        else:
            return ("Всі локації вже відвідані або вільних локацій немає.")
    else:
        return ("Ви не розпочали квест або квест завершено.")

@disp.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext):
    userID = msg.from_user.id
    await msg.answer('Тебе вітає Квест-бот. Тут ти можеш отримувати адреса локацій', reply_markup=keyb.main)
    if(db.accessed == False):
        await msg.reply('Спочатку введіть код доступу', reply_markup=keyb.entercode)
        await state.set_state(Register.GetCode)
    else:
        #await msg.answer(f'Tviy ID: {userID}')
        start_quest(userID)
        await msg.answer(visit_location(userID))
    

@disp.message(F.text == 'Почати')
async def start(msg: Message, state: FSMContext):
    userID = msg.from_user.id
    await msg.answer('Тебе вітає Квест-бот. Тут ти можеш отримувати адреси локацій')
    #time.sleep(1)
    if(db.accessed == False):
        await msg.reply('Спочатку введіть код доступу', reply_markup=keyb.entercode)
        await state.set_state(Register.GetCode)
    else:
        start_quest(userID)
        await msg.answer(visit_location(userID))


@disp.message(F.text == 'Відвідав')
async def start(msg: Message, state: FSMContext):
    userID = msg.from_user.id
    if(db.accessed == False):
        await msg.reply('Спочатку введіть код доступу', reply_markup=keyb.entercode)
        await state.set_state(Register.GetCode)
    else:
        await msg.answer(visit_location(userID))
        

@disp.message(Register.GetCode)
async def register(msg: Message, state: FSMContext):
    if msg.text == 'Назад':
        await msg.answer("Повернення до меню",reply_markup=keyb.main)
    elif msg.text == db.code:
        await state.update_data(GetCode=msg.text)
        await msg.answer('Код вірний',reply_markup=keyb.main)
        db.accessed=True
        await state.clear()
    else:
        await msg.answer('Код невірний')

            

async def main():
    await disp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнений')





    


