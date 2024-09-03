from telebot.handler_backends import State , StatesGroup
from telebot import TeleBot, types
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
from telebot.types import Message

class user_State(StatesGroup): 
    state_enter_name = State()
    state_enter_last_name = State()
    state_enter_phone_number = State()
    state_update_name = State()
    state_update_last_name = State()
    state_update_phone_number = State()
#######################################################################