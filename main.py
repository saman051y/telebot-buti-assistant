from datetime import datetime,timedelta
import logging
from telebot import TeleBot , custom_filters
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from auth.auth import *
from database.db_create_table import createTables
from messages.commands_msg import *
##################
bot =TeleBot(token = BOT_TOKEN, parse_mode="HTML")
##################
#* /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
    user_id=msg.from_user.id
    text=start_msg
    bot.send_message(chat_id=user_id,text=text)


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