from datetime import datetime,timedelta
import logging
from telebot import TeleBot , custom_filters , types,apihelper
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from auth.auth import *
from database.db_functions import delete_reservation, make_reserve_transaction
from database.db_weeklysetting import *
from database.db_create_table import *
from database.db_setwork import *
from database.db_users import *
from functions.custom_funxtions import  extract_reserveId_and_userId, get_free_time_for_next_7day
from functions.log_functions import *
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
from states import *
from database.db_service import *
from functions.time_date import *
import re
bot =TeleBot(token = BOT_TOKEN, parse_mode="HTML")
##########################################################################################!  Admin Panel  
@bot.message_handler(commands=['admin'])
def start(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id) 
    if not validation_admin (msg.from_user.id):
         bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
         return False
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark_text_admin_reserved_time , mark_text_admin_empty_time)
    markup.add(mark_text_admin_set_work_time , mark_text_admin_weekly_time)
    markup.add(mark_text_admin_set_service)
    markup.add(mark_text_admin_users_list , mark_text_admin_find_user)
    markup.add(mark_text_admin_bot_info , mark_text_admin_send_message_to_all)
    bot.send_message(chat_id=msg.from_user.id,text=text_user_is_admin, reply_markup=markup)
############################################################################################ markup reserve time
@bot.message_handler(func= lambda m:m.text == mark_text_admin_reserved_time)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    bot.send_message(chat_id=msg.from_user.id,text=text_coming_soon)
    #TODO insert reserve time section for admin
############################################################################################ markup empty time
@bot.message_handler(func= lambda m:m.text == mark_text_admin_empty_time)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    #every date when sent to markup will be delete ,so at first time i send a confusing value 
    markup = makrup_generate_empty_time_of_day(delete_day='0')
    text=text_get_empty_time
    bot.send_message(chat_id=msg.from_user.id,text=text , reply_markup=markup)

##### handle show empty time
@bot.callback_query_handler(func= lambda m:m.data.startswith("getEmptyTime:"))
def convertUserID(call:CallbackQuery):
    date=call.data.split(':')[1]
    date_persian = convertDateToPersianCalendar(date=date)
    list_empty_time=[]
    text=f'{date_persian}\n{text_et_empty_time_is_false}'
    list_empty_time=calculate_empty_time(date=date)
    if list_empty_time not in [False,'False','[]'] : 
        text=f'{date_persian}\n'
        for i in range(len(list_empty_time)):
            first_time =str(list_empty_time[i][0])
            end_time =str(list_empty_time[i][1])
            activation = str(list_empty_time[i][2])
            first_time_without_seconds = first_time[:5]
            end_time_without_seconds = end_time[:5]
            text_activation = 'رزرو شده است'
            if activation == '0':
                text_activation = 'آزاد'
            text += f'\n از {first_time_without_seconds} الی {end_time_without_seconds} {text_activation}'
    markup = makrup_generate_empty_time_of_day(delete_day=str(date))
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
############################################################################################ markup set work time
@bot.message_handler(func= lambda m:m.text == mark_text_admin_set_work_time)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.chat.id,text=text_user_is_not_admin)
        return False
    markup = InlineKeyboardMarkup()
    markup=makrup_generate_set_work_list_of_days()
    bot.send_message(chat_id=msg.chat.id,text=text_set_work_time_get_date, reply_markup=markup)
##########################################  call date from admin to set work 
@bot.callback_query_handler(func= lambda m:m.data.startswith("SetWorkTime:"))
def convertUserID(call:CallbackQuery):
    date=call.data.split(':')[1]
    markup = InlineKeyboardMarkup()
    markup = makrup_generate_parts_list_of_set_work(date=date)
    text=convertDateToPersianCalendar(date=str(date))
    #check activation of day if day be disable , admin can change day status
    date_as_day=convertDateToDayAsGregorianCalendar(date=date)
    check_is_active_day=db_WeeklySetting_Get_Value(name=date_as_day)
    if check_is_active_day[2] =='0':
        text =f'{text} \n {text_error_disable_day}'
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text, reply_markup=markup)
#########################################   call get part and time to insert new date
@bot.callback_query_handler(func= lambda m:m.data.startswith("SetWorkInsertPart:"))
def forwardToStateGetPart(call:CallbackQuery):
    part=call.data.split(':')[1]
    date=call.data.split(':')[2]
    persian_date=convertDateToPersianCalendar(date)
    if part=='1':
        text = f'{persian_date}\nپارت اول\n\n'+ text_set_work_time_get_part
    if part=='2':
        text = f'{persian_date}\nپارت دوم\n\n'+ text_set_work_time_get_part
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_setWork_get_part,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['date1']=date
        data['part']=part


# state get setWork part
@bot.message_handler(state=admin_State.state_setWork_get_part)
def setWork_section_state_get_part1(msg : Message):
    try:
        duration=str(msg.text)
        ##Regular expression pattern to match the format 'HH:MM:01/HH:MM:00' and min=[00,15,45]
        pattern =r'^([01]\d|2[0-3]):(00|15|30|45)/([01]\d|2[0-3]):(00|15|30|45)$'
        match = re.match(pattern, duration)
        if not match:
            bot.send_message(chat_id=msg.chat.id, text=text_set_work_time_get_part)
            return
        start_time_without_seconds=str(duration.split('/')[0])
        start_time=start_time_without_seconds+f':01'
        end_time_without_seconds=str(duration.split('/')[1])
        end_time=end_time_without_seconds + f':00'
        time_format = "%H:%M:%S"
        check_start_time = datetime.strptime(start_time, time_format).time()
        check_end_time = datetime.strptime(end_time, time_format).time()
        if not check_start_time < check_end_time:
            bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_parts)
            return
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            date1=str(data['date1'])
            part=str(data['part'])
            if part =='1':
                db_SetWork_Create_date(date=date1,part1_start_time=start_time, part1_end_time=end_time , part2_start_time=None , part2_end_time=None)
                text_part = 'پارت اول'
            if part =='2':
                db_SetWork_Create_date(date=date1,part1_start_time=None, part1_end_time=None , part2_start_time=start_time , part2_end_time=end_time)
                text_part = 'پارت دوم'
            persian_date=convertDateToPersianCalendar(date1)
            text = f'{persian_date}\n{text_part} برای {start_time_without_seconds} الی {end_time_without_seconds} با موفیقت درج شد \n'
            markup = InlineKeyboardMarkup()
            markup= makrup_generate_set_work_list_of_days()
            bot.send_message(chat_id=msg.chat.id, text=text , reply_markup=markup)
        bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    except ValueError:
        bot.send_message(chat_id=msg.chat.id, text=text_set_work_time_get_part)
#########################################  call update setWork part1
@bot.callback_query_handler(func= lambda m:m.data.startswith("SetWorkUpdatePart:"))
def forwardToStateUpdatePart(call:CallbackQuery):
    part=call.data.split(':')[1]
    date=call.data.split(':')[2]
    persian_date=convertDateToPersianCalendar(date)
    if part=='1':
        text = f'{persian_date}\nپارت اول\n\n'+ text_set_work_time_get_part
    if part=='2':
        text = f'{persian_date}\nپارت دوم\n\n'+ text_set_work_time_get_part

    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_setWork_update_part,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['date1']=date
        data['part']=part



# state update setwork part
@bot.message_handler(state=admin_State.state_setWork_update_part)
def setWork_section_state_update_part1(msg : Message):
    try:
        duration=str(msg.text)
        ##Regular expression pattern to match the format 'HH:MM:01/HH:MM:00' and min=[00,15,45]
        pattern =r'^([01]\d|2[0-3]):(00|15|30|45)/([01]\d|2[0-3]):(00|15|30|45)$'
        match = re.match(pattern, duration)
        # check input should be like HH:MM/HH:MM
        if not match:
            bot.send_message(chat_id=msg.chat.id, text=text_set_work_time_get_part)
            return
        start_time_without_seconds=str(duration.split('/')[0])
        end_time_without_seconds=str(duration.split('/')[1])
        start_time=start_time_without_seconds+f':01'
        end_time=end_time_without_seconds+f':00'
        time_format = "%H:%M:%S"
        check_start_time = datetime.strptime(start_time, time_format).time()
        check_end_time = datetime.strptime(end_time, time_format).time()
        # end time should be after start time
        if not check_start_time < check_end_time:
            bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_parts)
            return
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            date1=str(data['date1'])
            part=int(data['part'])
            #when you update part1 and part 2 have time ->par1 should be before part2
            if part == 1:
                part2=db_SetWork_Get_Part1_or_Part2_of_Day(date=date1 , part=2)
                part2_start_time = str(part2[0])
                part2_start_time_without_second = part2_start_time[:5]
                if part2 not in [None , 'None'] :
                    time_format = "%H:%M:%S"
                    check_start_time = datetime.strptime(part2_start_time, time_format).time()
                    check_end_time = datetime.strptime(end_time, time_format).time()
                    if not check_end_time<check_start_time :
                        bot.send_message(chat_id=msg.chat.id, text=f' پارت وارد شده باید تا قبل از ساعت {part2_start_time_without_second} باشد\n لطفا مجدد بازه را ارسال کنید ')
                        return
                    
             #when you update part2 and part1 have time ->par2 should nbe after part1
            if part == 2:
                part1=db_SetWork_Get_Part1_or_Part2_of_Day(date=date1 , part=1)
                part1_end_time = str(part1[1])
                part1_end_time_without_second = part1_end_time[:5]
                if part1 not in [None , 'None'] :
                    time_format = "%H:%M:%S"
                    check_start_time = datetime.strptime(start_time, time_format).time()
                    check_end_time = datetime.strptime(part1_end_time, time_format).time()
                    if not check_start_time>check_end_time :
                        bot.send_message(chat_id=msg.chat.id, text=f' پارت وارد شده باید تا بعد از ساعت {part1_end_time_without_second} باشد\n لطفا مجدد بازه را ارسال کنید ')
                        return
                    
            db_SetWork_Update_One_Part_Of_Day(date=date1 , part=part , start_time=start_time ,end_time=end_time)
            persian_date=convertDateToPersianCalendar(date1)
            text_part= f'پارت اول'
            if part== 2 :
                text_part= f'پارت دوم'
            text = f'{persian_date}\n{text_part}\n{start_time_without_seconds} الی {end_time_without_seconds}\n با موفیقت درج شد \n'
            markup = InlineKeyboardMarkup()
            markup= makrup_generate_set_work_list_of_days()
            bot.send_message(chat_id=msg.chat.id, text=text , reply_markup=markup)
        bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    #except ValueError:
    #    bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_parts)
    except Error as e:
        logging.error(f"reserveValidId : {e}")
        return False
############################################################################################
@bot.callback_query_handler(func= lambda m:m.data.startswith("SetWorkDeletePart:"))
def forwardToStateUpdatePart(call:CallbackQuery):
    part=call.data.split(':')[1]
    date=call.data.split(':')[2]
    db_SetWork_Delete_One_Part(part=part , date=date)
    markup=makrup_generate_set_work_list_of_days()
    persian_date=convertDateToPersianCalendar(date=date)
    text_delete = text_set_work_delete_part1
    if part == '2':
            text_delete=text_set_work_delete_part2
    text= persian_date+f'\n'+ text_delete
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
############################################################################################ markup weekly time
@bot.message_handler(func= lambda m:m.text == mark_text_admin_weekly_time)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.chat.id,text=text_user_is_not_admin)
        return False
    markup = makrup_generate_weekly_time_list()
    bot.send_message(chat_id=msg.chat.id,text=text_weekly_time, reply_markup=markup)
#########################################  get name to change value                   
@bot.callback_query_handler(func= lambda m:m.data.startswith("weeklysetting:"))
def forwardToStateUpdatePart(call:CallbackQuery):
    bot.delete_state(user_id=call.message.id,chat_id=call.message.chat.id) 
    name = str(call.data.split(':')[1])
    data= db_WeeklySetting_Get_Value(name=name)
    value=data[2]
    name_persian=ConvertVariableInWeeklySettingToPersian(name)
    if value == '1':
        db_WeeklySetting_Update(name=name , value='0' )
        text=f'{name_persian} غیر فعال شد '
        markup = makrup_generate_weekly_time_list()
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
    if value =='0':   
        db_WeeklySetting_Update(name=name , value='1' )
        text=f'{name_persian} فعال شد '
        markup = makrup_generate_weekly_time_list()
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
    if value =='None':
        text=f'زمان خود را برای تعیین پیش فرض {name_persian}  وارد کنید\n' + text_set_work_time_get_part
        value_text=ConvertVariableInWeeklySettingToPersian(value)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text)
        bot.set_state(user_id=call.message.chat.id,state=admin_State.state_weekly_update_time,chat_id=call.message.chat.id)
        with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
            data['name']= name
    if value not in ['0' , '1' , 'None'] :
        text=f'زمان خود را برای تعیین پیش فرض {name_persian}  وارد کنید در صورت نیاز برای حذف از دکمه زیر استفاده کنید\n' + text_set_work_time_get_part
        markup = InlineKeyboardMarkup()
        value_text=ConvertVariableInWeeklySettingToPersian(value)
        if value != 'None' :
            button_delete = InlineKeyboardButton(text=f'حذف {value_text}' ,callback_data=f'WeeklyDeletePart:{name}')
            markup.add(button_delete)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
        bot.set_state(user_id=call.message.chat.id,state=admin_State.state_weekly_update_time,chat_id=call.message.chat.id)
        with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
            data['name']= name

#########################################  get name to delete value                   
@bot.callback_query_handler(func= lambda m:m.data.startswith("WeeklyDeletePart:"))
def weeklySettingDeletePartFrom(call:CallbackQuery):
    name = str(call.data.split(':')[1])
    name_persian=ConvertVariableInWeeklySettingToPersian(name)
    text = f'حذف  {name_persian} انجام شد'
    db_WeeklySetting_Update(name=name , value='None')
    markup = makrup_generate_weekly_time_list()
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
######################################### state to get part for change value in default week setting  
@bot.message_handler(state=admin_State.state_weekly_update_time)
def weekly_time_section_state_update_value(msg : Message):
    try:
        part=msg.text
        pattern =r'^([01]\d|2[0-3]):(00|15|30|45)/([01]\d|2[0-3]):(00|15|30|45)$'
        match = re.match(pattern, part)
        if not match:
            bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_parts)
            return
        start_time=str(part.split('/')[0])+f':01'
        end_time=str(part.split('/')[1])+f':00'
        time_format = "%H:%M:%S"
        check_start_time = datetime.strptime(start_time, time_format).time()
        check_end_time = datetime.strptime(end_time, time_format).time()
        if not check_start_time < check_end_time:
            bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_part1_period)
            return
        with bot.retrieve_data(user_id=msg.chat.id , chat_id=msg.chat.id) as data:
            name=str(data['name'])
            part = f'{start_time}/{check_end_time}'
            if name == 'part1':
               parts=db_WeeklySetting_Get_Parts()
               part2 = str(parts[1][1])
               part2_start_time = str(part2.split('/')[0])
               part2_start_time_without_second = part2_start_time[:5]
               if part2 not in [None , 'None'] :
                   time_format = "%H:%M:%S"
                   check_start_time = datetime.strptime(part2_start_time, time_format).time()
                   check_end_time = datetime.strptime(end_time, time_format).time()
                   if not check_end_time<check_start_time :
                       bot.send_message(chat_id=msg.chat.id, text=f' پارت وارد شده باید تا قبل از ساعت {part2_start_time_without_second} باشد\n لطفا مجدد بازه را ارسال کنید ')
                       return
    
            #when you update part2 and part1 have time ->par2 should nbe after part1
            if name == 'part2':
               parts=db_WeeklySetting_Get_Parts()
               part1 = str(parts[0][1])
               part1_end_time = str(part1.split('/')[1])
               part1_start_time_without_second = part1_end_time[:5]
               if part1 not in [None , 'None'] :
                   time_format = "%H:%M:%S"
                   check_start_time = datetime.strptime(start_time, time_format).time()
                   check_end_time = datetime.strptime(part1_end_time, time_format).time()
                   if not check_end_time<check_start_time :
                       bot.send_message(chat_id=msg.chat.id, text=f' پارت وارد شده باید تا بعد از ساعت {part1_start_time_without_second} باشد\n لطفا مجدد بازه را ارسال کنید ')
                       return

            db_WeeklySetting_Update(name , part)
            name_persian=ConvertVariableInWeeklySettingToPersian(name)
            part=ConvertVariableInWeeklySettingToPersian(part)
            text=f'{name_persian} به {part} تغییر کرد'
            markup = makrup_generate_weekly_time_list()
            bot.send_message(chat_id=msg.chat.id,text=text, reply_markup=markup)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_set_work_time_get_part)
############################################################################################ markup set service
@bot.message_handler(func= lambda m:m.text == mark_text_admin_set_service)
def reserve_time(msg : Message): 
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    markupText = text_admin_update_service
    serviceData=list(db_Service_Get_All_Services())
    sorted_serviceData = sorted(serviceData, key=lambda item: item[4], reverse=True)
    markup=makrup_generate_service_list(sorted_serviceData)
    bot.send_message(chat_id=msg.chat.id,text=markupText, reply_markup=markup)
###########################################   insert service
@bot.callback_query_handler(func=lambda call: call.data == mark_text_admin_service_insert)
def callback_query(call : CallbackQuery):
    if not validation_admin(call.message.chat.id) : 
        bot.send_message(chat_id=call.message.chat.id,text=text_user_is_not_admin)
        return False
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
    bot.send_message(chat_id=call.message.chat.id,text=text_update_service_name)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_enter_name,chat_id=call.message.chat.id)

#get name for new service
@bot.message_handler(state=admin_State.state_service_enter_name)
def service_section_state_enter_name(msg : Message):
    service_name=msg.text
    if db_Service_Get_Service_With_Name(service_name=service_name) is not None :
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_name_duplicated)
        return False
    with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
        data['service_name']=service_name
    bot.set_state(user_id=msg.chat.id,state=admin_State.state_service_enter_time_slots,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.chat.id,text=text_update_service_time_slots)

#get Time for new service
@bot.message_handler(state=admin_State.state_service_enter_time_slots)
def service_section_state_enter_time_slots(msg : Message):
    user_time_input=f"{msg.text}:00"
    try:
        format_str = "%H:%M:%S"  
        timeOfService = datetime.strptime(user_time_input, format_str)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            data['service_time']=timeOfService
        bot.set_state(user_id=msg.chat.id,state=admin_State.state_service_enter_price,chat_id=msg.chat.id)
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_price)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)
        return False
   

#get price for new service
@bot.message_handler(state=admin_State.state_service_enter_price)
def service_section_state_enter_price(msg : Message):
    try:
        service_price=int(msg.text)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            data['service_price']=service_price   
        bot.set_state(user_id=msg.chat.id,state=admin_State.state_service_enter_is_active,chat_id=msg.chat.id)
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_is_active)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)

#get is_active for new service insert in db 
@bot.message_handler(state=admin_State.state_service_enter_is_active)
def service_section_state_enter_price(msg : Message):
    try:
        service_is_active_int = int(msg.text)
        if service_is_active_int ==0 or service_is_active_int ==1:
            service_is_active=bool(service_is_active_int)
        else:
            bot.send_message(msg.chat.id,text=text_update_service_error_is_active)
            return False 
        
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            data['service_is_active']=service_is_active_int
            service_name =str(data['service_name'])
            service_time =(data['service_time'])
            service_price =int(data['service_price'])
            service_is_active_int =bool(data['service_is_active'])
        service_id =db_Service_Insert_Service(name=service_name ,time_slots=service_time , price=service_price , is_active=service_is_active_int )
        service_info= createLabelServicesToShowOnButton(int(service_id))

        serviceData=list(db_Service_Get_All_Services())
        sorted_serviceData = sorted(serviceData, key=lambda item: item[4], reverse=True)
        markup=makrup_generate_service_list(sorted_serviceData)
        
        text=f"{text_update_service_enter_all_info}\n{service_info} "
        bot.send_message(chat_id=msg.chat.id,text=text,reply_markup=markup)
        bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id) 
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_is_active)

###########################################  get list services
@bot.callback_query_handler(func= lambda m:m.data.startswith("showServiceList_"))
def convertServiceID(call:CallbackQuery):

    ServiceID=int(call.data.split('_')[1])
    markup =markup_generate_service(ServiceID)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=createLabelServicesToShowOnButton(ServiceID), reply_markup=markup)


#### markup Update name Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceName_"))
def service_update_name(call:CallbackQuery):
    serviceid=int(call.data.split('_')[1])
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text_update_service_name)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_update_name,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id,chat_id=call.message.chat.id) as data:
        data['service_id']= serviceid 
#### state Update Name Service Panel
@bot.message_handler(state=admin_State.state_service_update_name)
def service_section_update_name(msg : Message):
    with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id,) as data:
        serviceId = int(data['service_id'])
        db_Service_Update_Service_Name(service_id=serviceId , name=msg.text)
        showText=createLabelServicesToShowOnButton(serviceId)
        markup=markup_generate_service(serviceId)
        bot.send_message(chat_id=msg.chat.id,text=f'{showText}\n\n نام آیتم بالا با موفقیت تغییر کرد',reply_markup=markup)
    bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id)


#### markup Update time_slot Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceTimeSlot_"))
def service_update_timeSlot(call:CallbackQuery):
    serviceId=int(call.data.split('_')[1])
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text_update_service_time_slots)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_update_time_slots,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id,chat_id=call.message.chat.id) as data:
        data['service_id']= serviceId
#### state Update time_slot Service Panel
@bot.message_handler(state=admin_State.state_service_update_time_slots)
def service_section_update_timeSlot(msg : Message):
    try:
        user_time_input=str(msg.text)# like "01:30"
        if not is_valid_time_format(user_time_input):
            bot.send_message(chat_id=msg.chat.id,text=text_time_is_not_valid)
            return False
        time_slot=convert_time_to_slot(user_time_input)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id,) as data:
            serviceId = int(data['service_id'])
            db_Service_Update_Service_Time_Slot(service_id=serviceId , time_slots=time_slot)
            showText=createLabelServicesToShowOnButton(serviceId)
            markup=markup_generate_service(serviceId)
            bot.send_message(chat_id=msg.chat.id,text=f'{showText}\n\n زمان آیتم بالا با موفقیت تغییر کرد',reply_markup=markup)
        bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)




#### markup Update price Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServicePrice_"))
def service_section_update_price(call:CallbackQuery):
    serviceId=int(call.data.split('_')[1])
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text_update_service_price)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_update_price,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id,chat_id=call.message.chat.id) as data:
        data['service_id']= serviceId
#### state Update price Service Panel
@bot.message_handler(state=admin_State.state_service_update_price)
def service_section_update_price(msg : Message):
    try:
        updated_price=int(msg.text)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id,) as data:
            serviceId = int(data['service_id'])
            db_Service_Update_Service_Price(service_id=serviceId , price=updated_price)
            showText=createLabelServicesToShowOnButton(serviceId)
            markup=markup_generate_service(serviceId)
            bot.send_message(chat_id=msg.chat.id,text=f'{showText}\n\n  قیمت آیتم بالا با موفقیت تغییر کرد',reply_markup=markup)
        bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)




#### markup Update is_active Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceIsAcive_"))
def service_section_update_is_active(call:CallbackQuery):
    serviceId=int(call.data.split('_')[1])
    data=db_Service_Get_Is_Active_Services(serviceId)
    data_str="فعال"
    if data == 1 :
        data_str="غیرفعال"
        db_Service_Disable_Service(service_id=serviceId)
    else:
        db_Service_Enable_Service(serviceId)
    showText=createLabelServicesToShowOnButton(serviceId)
    markup=markup_generate_service(serviceId)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=f'{showText}\n\n  آیتم بالا با موفقیت {data_str} شد',reply_markup=markup)
    



#### markup delete Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceDelete_"))
def service_update_name(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    serviceId=int(call.data.split('_')[1])
    showText=createLabelServicesToShowOnButton(serviceId)
    db_Service_Delete_Service(service_id=serviceId)
    serviceData=list(db_Service_Get_All_Services())
    sorted_serviceData = sorted(serviceData, key=lambda item: item[4], reverse=True)
    markup=makrup_generate_service_list(sorted_serviceData)
    bot.send_message(chat_id=call.message.chat.id,text=f'{showText}\n\n  آیتم بالا با موفقیت حذف شد',reply_markup=markup)

######################################################################## access to all users

###########################################  fins user by ID
### markup user find
#TODO when insert text instead int , bot will be crashed                                               -> need attention
#TODO when select find_user button then select list_0f_users  , it continue to find in user           -> need attention
@bot.message_handler(func= lambda m:m.text == mark_text_admin_find_user)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    bot.set_state(user_id=msg.from_user.id,state=admin_State.state_user_find,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.chat.id,text=text_user_find)
### state user find
@bot.message_handler(state=admin_State.state_user_find)
def user_section_user_find(msg : Message):
    if db_Users_Find_User_By_Id(user_id=msg.text) is False :
        bot.send_message(chat_id=msg.chat.id,text=text_user_not_find)
        return False
    data=db_Users_Find_User_By_Id(user_id=msg.text)
    phone_number=data[1]
    username=data[2]
    join_date=data[3]
    name=[4]
    last_name=[5]
    url=change_Username_To_URL(username , phone_number)
    bot.send_message(msg.chat.id, url, parse_mode='Markdown')


###########################################  get list Users
@bot.message_handler(func= lambda m:m.text == mark_text_admin_users_list)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    users_list=list(db_Users_Get_All_Users())
    markup = InlineKeyboardMarkup()
    for item in users_list :
        showText=createLabelUsersToShowOnButton(item[0])
        button = InlineKeyboardButton(text=showText ,callback_data=f'showUsersList_{item[0]}')
        markup.add(button)
    bot.send_message(chat_id=msg.chat.id,text=text_users_list, reply_markup=markup)

@bot.callback_query_handler(func= lambda m:m.data.startswith("showUsersList_"))
def convertUserID(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    user_id=int(call.data.split('_')[1])
    username=db_Users_Get_Username_user(user_id=user_id)
    phone_number=db_Users_Get_Phone_Number_User(user_id=user_id)
    url=change_Username_To_URL(username , phone_number)
    name_lastname=createLabelUsersToShowOnButton(user_id=user_id)
    showText=f"{name_lastname} \n {url}"
    bot.send_message(chat_id=call.message.chat.id,text=showText)
###########################################  send message to all
@bot.message_handler(func=lambda m:m.text == mark_text_admin_send_message_to_all)
def msg_to_all(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)  
    if not validation_admin (msg.from_user.id):
         bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
         return False
    bot.send_message(msg.chat.id,text=text_message_to_all_users)
    bot.set_state(user_id=msg.from_user.id,state=admin_State.message_to_all,chat_id=msg.chat.id)


@bot.message_handler(state =admin_State.message_to_all)
def get_message_to_send(msg : Message):
    with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['msg']=msg.text
    text=f"یک پیام از سمت ادمین :\n <strong> {data['msg']} </strong> "
    users=db_Users_Get_All_Users()
    for user in users:
        try:
            bot.get_chat(user[0])
            bot.send_message(chat_id=user[0],text=text)
        except apihelper.ApiTelegramException as e:
            logging.error(f"user with ID {user[0]} not found to send message")
    bot.send_message(chat_id=msg.chat.id,text=text_sent_message_to_all_users)
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
###########################################
#######################################################################!   User Panel
#* /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
    #bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id) 
    user_id=msg.from_user.id
    user_is_valid=db_Users_Validation_User_By_Id(user_id=user_id)
    if user_is_valid is False :
        user_is_created =db_Users_Insert_New_User(user_id=msg.from_user.id,username=msg.from_user.username,join_date=datetime.now().date(),name='empty',last_name='empty',phone_number='0')
        if user_is_created is False:
            text=text_user_not_created
            bot.send_message(chat_id=user_id,text=text,reply_markup=ReplyKeyboardRemove())
            return False
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark_text_reserve_time)
    markup.add(mark_text_reserved_time)
    markup.add(mark_text_account_info ,mark_text_support)
    text=text_start_msg
    bot.send_message(chat_id=user_id,text=text,reply_markup=markup)
####################################################################### Insert Reserve Time Section
#* mark_text_reserve_time handler
@bot.message_handler(func= lambda m:m.text == mark_text_reserve_time)
def reserve_time(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id) 
    counter=0
    db_Users_Update_Username_User(user_id=msg.from_user.id , username=msg.from_user.username)#update Username while every reservation
    name = db_Users_Get_Name_User(msg.from_user.id)
    if name == 'empty' : 
        activation_user(msg=msg)
        return
    
    services=db_Service_Get_All_Services()
    if services is None or len(services) ==0:
        bot.send_message(chat_id=msg.from_user.id,text=text_no_service_available)
        return False
    services = [service + (0,) for service in services]
    markup=markup_generate_services_for_reserve(services,total_selected=counter)

    text=text_reservation_init
    bot.send_message(chat_id=msg.chat.id,reply_markup=markup,text=text)

    bot.set_state(user_id=msg.chat.id,state=user_State.state_selecting_service,chat_id=msg.chat.id)


    with bot.retrieve_data(user_id=msg.chat.id , chat_id=msg.chat.id) as data:
        data['services_choosing']=services
        data['services_name']=''
        data['counter']=counter
            

### select a service 
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_service_"))
def callback_query(call:CallbackQuery):
    service_id=(call.data.split("_"))[2]
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        services=data['services_choosing']
        services_name=str(data["services_name"])
        counter=data['counter']
    # change enable <=> disable
    for index, service in enumerate(services):

        if int(service[0]) == int(service_id):
            if service[5]==0: # if service need to active
                if counter== 0:# if basic info not set
                    services_name="خدمات انتخاب شده \n به ترتیب : نام - قیمت - مدت زمان مورد نیاز"


                services[index]=service[:5] + (1,) 
                current_service_info=f"{services[index][1]}-{services[index][3]}-{services[index][2]}"
                services_name=f"{services_name}\n {current_service_info}"
                counter=counter+1
            else:# if service wanna be disable
                services[index]=service[:5] + (0,) 
                current_service_info=f"{services[index][1]}-{services[index][3]}-{services[index][2]}"
                services_name = services_name.replace(current_service_info, "").strip()
                counter=counter-1
            break
    markup=markup_generate_services_for_reserve(services,total_selected=counter)


    if counter<1 :
        services_name=''
    text=f"{text_reservation_init}\n {services_name}"

    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text, reply_markup=markup)
    
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['services_choosing']=services
        data['services_name']=services_name
        data['counter']=counter
    
####end of selection :select part 1 or 2
@bot.callback_query_handler(func=lambda call: call.data == ("make_reservation"))
def callback_query(call:CallbackQuery):
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        services=data['services_choosing']
    total_time = timedelta()
    total_price = 0  
    for service in services:
        if service[5]==1:
            total_time += service[2]  
            total_price += service[3] 

    total_time=convert_to_standard_time(time_string=f"{total_time}") 
    text=text_make_reservation_info(price=total_price,time=total_time,services=services)
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=text_markup_part1,callback_data=f"finish_reserve_1"),InlineKeyboardButton(text=text_markup_part2,callback_data=f"finish_reserve_2"))
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text,reply_markup=markup)
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['services_choosing']=services 
        data['total_time']=total_time
        data['total_price']=total_price

####end of reservation : show day if evadable
@bot.callback_query_handler(func=lambda call: call.data.startswith("finish_reserve"))
def callback_query(call:CallbackQuery):
    part=int(call.data.split("_")[2])
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        services =data['services_choosing']
        total_time=data['total_time']
        total_price=data['total_price']

    available_list=get_free_time_for_next_7day(part=part,duration=total_time)
    bot.delete_state(user_id=call.message.from_user.id,chat_id=call.message.chat.id)
    markup=InlineKeyboardMarkup()
    if len(available_list) <1 :
        markup.add(InlineKeyboardButton(text=text_no_time_for_reservations,callback_data="!!!!!!!!!!!"))
    else:
        for day in available_list:
            date=day[0]
            date_per=gregorian_to_jalali(date)
            time=day[1]
            btn=InlineKeyboardButton(text=f"{date_per} : {time[:5]}",callback_data=f"reserve_date_{date}_{time}")
            markup.add(btn)
    text=call.message.text
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['services_choosing']=services 
        data['total_time']=total_time
        data['total_price']=total_price

    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text,reply_markup=markup)


##make reservation in db and send info to user : btn is send pic 
@bot.callback_query_handler(func=lambda call: call.data.startswith("reserve_date_"))
def callback_query(call:CallbackQuery):
    date=(call.data.split("_")[2])
    time=(call.data.split("_")[3])
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        services =data['services_choosing']
        total_time=data['total_time']
        total_price=data['total_price']

    text=make_reservation_info_text(date=date,time=time,price=total_price,duration=total_time,services=services, )
    
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="ارسال رسید", callback_data="pic_receipt"))
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['services']=services 
        data['total_time']=total_time
        data['total_price']=total_price
        data['date']=date
        data['time']=time
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text,reply_markup=markup)

### get pic_receipt msg
@bot.callback_query_handler(func=lambda call: call.data == ("pic_receipt"))
def callback_query(call:CallbackQuery):
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        services =data['services']
        total_time=data['total_time']
        total_price=data['total_price']
        date=data['date']
        time=data['time']
    bot.delete_state(user_id=call.message.from_user.id,chat_id=call.message.chat.id)

    text=call.message.text
    cart_info=text_cart_info()
    text=f"{text}\n \n {cart_info}"
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text)
    
    text=text_send_receipt
    bot.send_message(chat_id=call.message.chat.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=user_State.get_rec,chat_id=call.message.chat.id)
    
    with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
        data['services']=services 
        data['total_time']=total_time
        data['total_price']=total_price
        data['date']=date
        data['time']=time

## pic_receipt is sended not as pic
@bot.message_handler(state=user_State.get_rec, content_types=['text', 'video', 'document', 'audio', 'sticker', 'voice', 'location', 'contact'])
def handle_non_photo(msg: Message):
    # پیام خطا برای ارسال محتوای غیر از عکس
    bot.send_message(msg.chat.id, "لطفاً فقط یک عکس از رسید خود ارسال کنید.")


## pic_receipt is sended as pic
@bot.message_handler(state=user_State.get_rec,content_types=['photo'])
def reserve_section_enter_name_first_time(msg : Message):
    with bot.retrieve_data(user_id=msg.chat.id , chat_id=msg.chat.id) as data:
        services =data['services']
        total_time=data['total_time']
        total_price=data['total_price']
        date=data['date']
        time=data['time']
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    
    markup=InlineKeyboardMarkup()
    approve_btn=InlineKeyboardButton(text="تایید رزرو و تراکنش",callback_data="approve_btn")
    deny_btn=InlineKeyboardButton(text="رد کردن رزرو و تراکنش",callback_data="deny_btn")
    markup.add(approve_btn)
    markup.add(deny_btn)

    #todo: make reserve in db
    user_id=msg.from_user.id
    print("test")
    result,reserve_id=make_reserve_transaction(user_id=user_id,services=services,duration=total_time,price=total_price,date=date,start_time=time)

    if not result:
        text=text_transaction_problem
        bot.send_message(msg.chat.id,text=text)
        return 
    
    
    #msg to user
    text=text_wait_for_approve
    bot.send_message(msg.chat.id,text=text)

    #msg to admin (the main one )
    forwarded_msg=bot.forward_message(chat_id=MAIN_ADMIN_USER_ID[0],from_chat_id=msg.chat.id,message_id=msg.message_id)
    text=make_reservation_info_text(date=date,time=time,price=total_price,duration=total_time,services=services, )
    user_id =msg.from_user.id
    text=f"{text} \n reserve_id={reserve_id} \n user_id={user_id}" #! do not change it
    bot.send_message(chat_id=MAIN_ADMIN_USER_ID[0],text=text,reply_to_message_id=forwarded_msg.message_id,disable_notification=True,reply_markup=markup)
    
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)


### accept btn
@bot.callback_query_handler(func=lambda call: call.data ==("approve_btn"))
def callback_query(call:CallbackQuery):
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش تایید شد",callback_data="!?!?!?!")
    markup.add(btn)
    info_text=call.message.text
    # approve transaction
    reserve_id,user_id=extract_reserveId_and_userId(info_text)
    result=db_Reserve_Update_Approved_Of_Reserve(reserve_id=reserve_id,approved=True)

    if not result:# to admin
        text=text_problem_with_approve_or_deny
        bot.send_message(call.message.chat.id,text=text)
        return 

    #send approve msg to user
    bot.send_message(chat_id=user_id,text=reserve_is_approved)

    #admin edit message
    text=info_text
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)


## deny btn 
@bot.callback_query_handler(func=lambda call: call.data ==("deny_btn"))
def callback_query(call:CallbackQuery):
    info_text=call.message.text
    reserve_id,user_id=extract_reserveId_and_userId(info_text)
    
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش رد شد",callback_data="!?!?!?!")
    btn2=InlineKeyboardButton(text="علت رد کردن تراکنش را بنویسید",callback_data=f"deny_message_to_{user_id}")
    markup.add(btn)
    markup.add(btn2)

    # remove reserve from db 
    result=delete_reservation(reserve_id)

    if not result:
        text=text_problem_with_approve_or_deny
        bot.send_message(call.message.chat.id,text=text)
        return 
  
    #send deny  msg to user
    bot.send_message(chat_id=user_id,text=reserve_is_denied)

    #admin edit message
    text=info_text
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)

#deny msg reason
@bot.callback_query_handler(func=lambda call: call.data.startswith("deny_message_to_"))
def deny_msg(call : CallbackQuery):
    user_id=int(call.data.split('_')[3])
    msg=f"{call.message.text}"

    text=text_deny_reason
    bot.send_message(chat_id=call.message.chat.id,text=text)
    print("test")
    bot.set_state(user_id=call.message.chat.id,state=admin_State.send_deny_reason,chat_id=call.message.chat.id)

    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['user_id'] = user_id
 

 #send deny reason to user
@bot.message_handler(state=admin_State.send_deny_reason)
def deny_reason(msg : Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        # user_id = int(data.get('user_id'))
        user_id = int( data['user_id'])

    deny_reason_msg=msg.text
    bot.send_message(chat_id=user_id,text=f"علت رد شدن تراکنش شما : \n {deny_reason_msg}")
    bot.send_message(chat_id=msg.from_user.id,text="پیام شما برای کاربر ارسال شد")
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

#?######################################################################
#### activation_user
def activation_user(msg : Message) :
        # name = db_Users_Get_Name_User(msg.from_user.id)
        # last_name = db_Users_Get_Last_Name_User(msg.from_user.id)
        # phone_number = db_Users_Get_Phone_Number_User(msg.from_user.id)
        bot.send_message(chat_id=msg.from_user.id,text=text_enter_name)
        bot.set_state(user_id=msg.chat.id,state=user_State.state_info_enter_name,chat_id=msg.chat.id)


### Enter name for first time after press 'reserve time'
@bot.message_handler(state=user_State.state_info_enter_name)
def reserve_section_enter_name_first_time(msg : Message):
    db_Users_Update_Name_User(user_id=msg.from_user.id ,name=msg.text)
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_last_name)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_info_enter_last_name,chat_id=msg.chat.id)

### Enter last_name for first time after press 'reserve time'
@bot.message_handler(state=user_State.state_info_enter_last_name)
def reserve_section_state_enter_lastname(msg : Message):
    db_Users_Update_Last_Name_User(user_id=msg.from_user.id,last_name=msg.text)
    bot.send_message(chat_id=msg.from_user.id,text=text_enter_phone_number)
    bot.set_state(user_id=msg.chat.id,state=user_State.state_info_enter_phone_number,chat_id=msg.chat.id)


###Enter phone_number for first time after press 'reserve time'
@bot.message_handler(state=user_State.state_info_enter_phone_number)
def reserve_section_state_enter_phone_number(msg : Message):
    db_Users_Update_Phone_Number_User(user_id=msg.from_user.id ,phone_number=msg.text)
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_complete_enter_info)


####################################################################### Account Info Section
@bot.message_handler(func= lambda m:m.text == mark_text_account_info)
def account_info(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id) 
    name = db_Users_Get_Name_User(msg.from_user.id)
    if name == 'empty' : 
            activation_user(msg=msg)
    else :
        data=db_Users_Find_User_By_Id(msg.from_user.id)
        text = text_cleaner_info(data)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=mark_text_update_name, callback_data=mark_text_update_name))
        markup.add(InlineKeyboardButton(text=mark_text_update_last_name, callback_data=mark_text_update_last_name))
        markup.add(InlineKeyboardButton(text=mark_text_update_phone_number, callback_data=mark_text_update_phone_number))
        bot.send_message(chat_id=msg.chat.id,text=text, reply_markup=markup)


### markup update name
@bot.callback_query_handler(func=lambda call: call.data == mark_text_update_name)
def callback_query(call):
        bot.answer_callback_query(callback_query_id=call.id,text=text_enter_name)
        bot.send_message(chat_id=call.message.chat.id, text=text_enter_name)
        bot.set_state(user_id=call.from_user.id,state=user_State.state_info_update_name)


### state update last_name
@bot.message_handler(state=user_State.state_info_update_name)
def account_info_state_update_name(msg : Message):
    db_Users_Update_Name_User(user_id=msg.from_user.id , name=msg.text )
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_updated_name)


### markup update last_name
@bot.callback_query_handler(func=lambda call: call.data == mark_text_update_last_name)
def callback_query(call):
        bot.answer_callback_query(callback_query_id=call.id,text=text_enter_last_name)
        bot.send_message(chat_id=call.message.chat.id, text=text_enter_last_name)
        bot.set_state(user_id=call.from_user.id,state=user_State.state_info_update_last_name)


### state update last_name
@bot.message_handler(state=user_State.state_info_update_last_name)
def account_info_state_update_last_name(msg : Message):
    db_Users_Update_Last_Name_User(user_id=msg.from_user.id , last_name=msg.text )
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_updated_last_name)


### markup update phone_number
@bot.callback_query_handler(func=lambda call: call.data == mark_text_update_phone_number)
def callback_query(call):
        bot.answer_callback_query(callback_query_id=call.id,text=text_enter_phone_number)
        bot.send_message(chat_id=call.message.chat.id, text=text_enter_phone_number)
        bot.set_state(user_id=call.from_user.id,state=user_State.state_info_update_phone_number)


### state update last_name
@bot.message_handler(state=user_State.state_info_update_phone_number)
def account_info_state_update_name(msg : Message):
    db_Users_Update_Phone_Number_User(user_id=msg.from_user.id , phone_number=msg.text )
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.from_user.id,text=text_updated_phone_number)


####################################################################### Support Section
@bot.message_handler(func= lambda m:m.text == mark_text_support)
def text_to_support(msg : Message):
    bot.delete_state(user_id=msg.from_user.id,chat_id=msg.chat.id) 
    bot.send_message(msg.chat.id, f"{text_support}\n{SUPPORT_USERNAME}", parse_mode='Markdown')
#######################################################################
def startMessageToAdmin(enable=True,disable_notification=True):
    if not enable:
        return False

    text=f'{msg_restart} \n 🚫{get_current_datetime()}🚫'

    #get last log    
    latest_log_file = get_latest_log_file()

    for admin in MAIN_ADMIN_USER_ID:#send for all admins
        if latest_log_file:
            last_3_errors=get_last_errors(latest_log_file)
            error_message = "\n".join(last_3_errors)
            with open(latest_log_file, 'rb') as log_file:
                bot.send_document(admin, log_file,caption=f"{text}\n{error_message}",disable_notification=disable_notification)
            logging.info(f"send last log to admin [{admin}] : {latest_log_file}")
        else:
            logging.info("ther is no log file to show")
            bot.send_message(chat_id=admin,text=f"{text}\n ⛔️فایل log وجود ندارد⛔️",disable_notification=disable_notification)

########################################################################! END :)
if __name__ == "__main__":
    #log init
    log_filename = f"./logs/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("logging is running")
    remove_old_logs()
    
    #db setting
    createTables()

    #basic functions 
    startMessageToAdmin()
    #bot setting
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.polling()