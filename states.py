from telebot.handler_backends import State , StatesGroup
from telebot import TeleBot, types
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
from telebot.types import Message

class user_State(StatesGroup): 
    state_info_enter_name = State()
    state_info_enter_phone_number = State()
    state_info_update_name = State()
    state_info_update_phone_number = State()
    state_selecting_service=State()
    get_rec=State
#######################################################################
class admin_State(StatesGroup):

    ########## service states
    state_service_enter_name = State()
    state_service_enter_time_slots = State()
    state_service_enter_price = State()
    state_service_enter_is_active = State()
    state_service_enter_all_info = State()
    state_service_update_name= State()
    state_service_update_time_slots= State()
    state_service_update_price= State()
    state_service_update_is_active= State()
    state_add_admin=State()
    state_user_find =State()
    message_to_all=State()
    send_deny_reason=State()

    ########## setwork state
    state_setWork_get_part=State()
    state_setWork_update_part=State()
    
    ########## weekly time
    state_weekly_update_time=State()
#######################################################################
