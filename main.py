from datetime import datetime,timedelta
import logging
from telebot import TeleBot , custom_filters , types
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from auth.auth import *
from database.db_create_table import createTables
from database.db_users import *
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
from states import *
#######################################################################
bot =TeleBot(token = BOT_TOKEN, parse_mode="HTML")
#######################################################################
#* /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
    user_id=msg.from_user.id
    user_is_valid=db_Users_Validation_User_By_Id(user_id=user_id)
    if not user_is_valid:
        user_is_created =db_Users_Insert_New_User(user_id=user_id,username=msg.from_user.username,join_date=current_date(),name='empty',last_name='empty',phone_number='0')
        if not user_is_created:
            text=text_user_not_created
            bot.send_message(chat_id=user_id,text=text,reply_markup=ReplyKeyboardRemove())
            return False
    # user_info=getUser(user_id=user_id)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark_text_reserve_time)
    markup.add(mark_text_reserved_time)
    markup.add(mark_text_account_info ,mark_text_text_support)
    text=text_start_msg
    bot.send_message(chat_id=user_id,text=text,reply_markup=markup)
#######################################################################
#######################################################################! Insert Reserve Time Section
#* mark_text_reserve_time handler
@bot.message_handler(func= lambda m:m.text == mark_text_reserve_time)
def reserve_time(msg : Message):
        name = db_Users_Get_Name_User(msg.from_user.id)
        last_name = db_Users_Get_Last_Name_User(msg.from_user.id)
        phone_number = db_Users_Get_Phone_Number_User(msg.from_user.id)
        db_Users_Update_Username_User(user_id=msg.from_user.id , username=msg.from_user.username)#update Username while every reservation
        if name == 'empty' :
            bot.send_message(chat_id=msg.from_user.id,text=text_enter_name)
            bot.set_state(user_id=msg.chat.id,state=user_State.state_enter_name,chat_id=msg.chat.id)
        else :
            #!ready to insert calendar
            return True
#######################################################################
@bot.message_handler(state=user_State.state_enter_name)
def reserve_section_enter_name_frist_time(msg : Message):
    db_Users_Update_Name_User(user_id=msg.from_user.id ,name=msg.text)
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_last_name)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_enter_last_name,chat_id=msg.chat.id)
#######################################################################
@bot.message_handler(state=user_State.state_enter_last_name)
def reserve_section_state_enter_lastname(msg : Message):
    db_Users_Update_Last_Name_User(user_id=msg.from_user.id,last_name=msg.text)
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_phone_number)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_enter_phone_number,chat_id=msg.chat.id)
#######################################################################
@bot.message_handler(state=user_State.state_enter_phone_number)
def reserve_section_state_enter_phone_number(msg : Message):
    db_Users_Update_Phone_Number_User(user_id=msg.from_user.id ,phone_number=msg.text)
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_compelet_enter_info)
#######################################################################
########################################################################!Account Info Section
@bot.message_handler(func= lambda m:m.text == mark_text_account_info)
def account_info(msg : Message):
    data=db_Users_Find_User_By_Id(msg.from_user.id)
    text = text_cleaner_info(data)
    bot.send_message(chat_id=msg.from_user.id,text=text)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark_text_update_name)
    markup.add(mark_text_update_last_name)
    markup.add(mark_text_update_phone_number)
    text=text_account_info
    bot.send_message(chat_id=msg.from_user.id,text=text,reply_markup=markup)
#######################################################################
@bot.message_handler(func= lambda m:m.text == mark_text_update_name)
def account_info_update_last_name(msg : Message):
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_name)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_update_name,chat_id=msg.chat.id)
#######################################################################
@bot.message_handler(state=user_State.state_update_name)
def account_info_state_update_last_name(msg : Message):
    db_Users_Update_Name_User(user_id=msg.from_user.id , name=msg.text )
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_update_name)
#######################################################################
@bot.message_handler(func= lambda m:m.text == mark_text_update_last_name)
def account_info_update_last_name(msg : Message):
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_last_name)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_update_last_name,chat_id=msg.chat.id)
######################################################################
@bot.message_handler(state=user_State.state_update_last_name)
def account_info_state_update_last_name(msg : Message):
    db_Users_Update_Last_Name_User(user_id=msg.from_user.id , last_name=msg.text )
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_update_last_name)
######################################################################
@bot.message_handler(func= lambda m:m.text == mark_text_update_phone_number)
def account_info_update_phone_number(msg : Message):
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_phone_number)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_update_phone_number,chat_id=msg.chat.id)
#######################################################################
@bot.message_handler(state=user_State.state_update_phone_number)
def account_info_state_udpate_phone_number(msg : Message):
    db_Users_Update_Phone_Number_User(user_id=msg.from_user.id , phone_number=msg.text )
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_update_phone_number)
#######################################################################
#!########################
if __name__ == "__main__":
    log_filename = f"./logs/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("logging is running")
    createTables()
    print()
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.polling()