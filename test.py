from database.db_admin_list import *
from database.db_bot_setting import *
from database.db_reserve import *
from database.db_users import *
from database.db_service import *
from database.db_setwork import *
from database.db_weeklysetting import *
from functions.custom_functions import *
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
from functions.time_date import *
##############################################################################
@bot.callback_query_handler(func= lambda m:m.data.startswith("deleteReservedTime_"))
def deleteReservedTime(call:CallbackQuery):
    id_reserve=call.data.split('_')[1] 
    date=call.data.split('_')[2]
    start_time=call.data.split('_')[3]   
    text = f'{text_delete_reserve}'
    text_info= text_cleaner_info_reserve(date=date , start_time=start_time)
    #todo try catch
    markup = InlineKeyboardMarkup()
    markup = makrup_generate_empty_time_of_day(delete_day='0')
    #send message to user(not admin) that your message deleted by admin
    if db_Reserve_Delete_Reserve(id_reserve) : 
        user_id_is_admin = False
        text_user = f'{text_delete_reserve_for_user}\n\n{text_info}'
        user_id= int(db_Reserve_Get_Reserve_With_Id(id_reserve))
        admin_list=db_admin_get_all()
        for admin in admin_list : 
            if user_id==int(admin[0]) :
                user_id_is_admin = True
        if user_id_is_admin == False :
            bot.get_chat(user_id)
            bot.send_message(chat_id=user_id,text=text_user)
        text =f'{text_delete_reserve}\n\n{text_info}'
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text, reply_markup=markup)
    else:
        text =f'{text_not_delete_reserve}\n\n{text_info}'
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text_not_delete_reserve, reply_markup=markup)
