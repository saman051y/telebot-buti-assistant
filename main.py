from datetime import datetime,timedelta
import logging
from telebot import TeleBot , custom_filters
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from auth.auth import *
from database.db_create_table import createTables
from database.db_users import *
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
##################
bot =TeleBot(token = BOT_TOKEN, parse_mode="HTML")
##################
#* /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
    user_id=msg.from_user.id
    user_is_valid=userValidId(user_id=user_id)
    if not user_is_valid:
        user_is_created =insertNewUser(user_id=user_id,username=msg.from_user.username,join_date=current_date(),name='empty',last_name='empty',phone_number='0')
        if not user_is_created:
            text=user_not_created
            bot.send_message(chat_id=user_id,text=text,reply_markup=ReplyKeyboardRemove())
            return False
    # user_info=getUser(user_id=user_id)
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark_text_reserve_time)
    text=start_msg
    bot.send_message(chat_id=user_id,text=text,reply_markup=markup)
#######################################################################
#* mark_text_reserve_time handler
@bot.message_handler(func= lambda m:m.text == mark_text_reserve_time)
def reserve_time(msg : Message):
    bot.send_message(chat_id=msg.from_user.id,text="hi")

#!########################
if __name__ == "__main__":
    log_filename = f"./logs/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("logging is running")
    createTables()
    print()
    bot.polling()