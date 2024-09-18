from cgitb import text
from email import header
from aiogram.fsm.state import StatesGroup, State
#from aiogram.fsm.context import FSMContext


class Request_reg(StatesGroup):
    
    header = State()
    text = State()
    comfer = State()