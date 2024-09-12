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
from database.db_service import *
bot =TeleBot(token = BOT_TOKEN, parse_mode="HTML")

#######################################################################!  Admin Panel
@bot.message_handler(commands=['admin'])
def start(msg : Message):
    if validation_admin :
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(mark_text_admin_reserved_time , mark_text_admin_empty_time)
            markup.add(mark_text_admin_set_work_time)
            markup.add(mark_text_admin_set_service)
            markup.add(mark_text_admin_users_list , mark_text_admin_find_user)
            markup.add(mark_text_admin_bot_info , mark_text_admin_send_message_to_all)
            text=text_user_is_admin
            bot.send_message(chat_id=msg.from_user.id,text=text_user_is_admin, reply_markup=markup)
    else : 
         bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
####################################################################### markup reserve time
@bot.message_handler(func= lambda m:m.text == mark_text_admin_reserved_time)
def reserve_time(msg : Message):
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    bot.send_message(chat_id=msg.from_user.id,text=text_cooming_soon)
    #TODO insert reserve time section for admin
####################################################################### markup empty time
@bot.message_handler(func= lambda m:m.text == mark_text_admin_empty_time)
def reserve_time(msg : Message):
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    bot.send_message(chat_id=msg.from_user.id,text=text_cooming_soon)
    #TODO insert empty_time section for admin  
####################################################################### markup set work time

@bot.message_handler(func= lambda m:m.text == mark_text_admin_set_work_time)
def reserve_time(msg : Message):
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    bot.send_message(chat_id=msg.from_user.id,text=text_cooming_soon)
    #TODO insert set_work section for admin  
######################################################################## markup set service

@bot.message_handler(func= lambda m:m.text == mark_text_admin_set_service)
def reserve_time(msg : Message):
    if not validation_admin(msg.from_user.id) : 
        bot.send_message(chat_id=msg.from_user.id,text=text_user_is_not_admin)
        return False    
    markuptext = text_admin_update_service
    serviceData=list(db_Service_Get_All_Services())
    sorted_serviceData = sorted(serviceData, key=lambda item: item[4], reverse=True)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_admin_service_insert ,callback_data=mark_text_admin_service_insert))
    for item in sorted_serviceData :
        text=createLableServicesToShowOnButton(item[0])
        button = InlineKeyboardButton(text=text ,callback_data=f'showServiceList_{item[0]}')
        markup.add(button)
    bot.send_message(chat_id=msg.chat.id,text=markuptext, reply_markup=markup)
###########################################   insert service
@bot.callback_query_handler(func=lambda call: call.data == mark_text_admin_service_insert)
def callback_query(call : CallbackQuery):
    if not validation_admin(call.message.chat.id) : 
        bot.send_message(chat_id=call.message.chat.id,text=text_user_is_not_admin)
        return False
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

#get time_slots for new service
@bot.message_handler(state=admin_State.state_service_enter_time_slots)
def service_section_state_enter_time_slots(msg : Message):
    service_time_slots=msg.text
    try:
        time_slots = int(msg.text)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            data['service_time_slots']=service_time_slots
        bot.set_state(user_id=msg.chat.id,state=admin_State.state_service_enter_price,chat_id=msg.chat.id)
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_price)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)
    

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
             return False 
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id) as data:
            data['service_is_active']=service_is_active_int
            service_name =str(data['service_name'])
            service_time_slots =int(data['service_time_slots'])
            service_price =int(data['service_price'])
            service_is_active_int =bool(data['service_is_active'])
        db_Service_Insert_Service(name=service_name ,time_slots=service_time_slots , price=service_price , is_active=service_is_active_int )
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_enter_all_info)
        bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id) 
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_is_active)

###########################################  get list services
@bot.callback_query_handler(func= lambda m:m.data.startswith("showServiceList_"))
def convertServiceID(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    ServiceID=int(call.data.split('_')[1])
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_name ,callback_data=f'editServiceName_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_time_slots ,callback_data=f'editServiceTimeSlot_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_price ,callback_data=f'editServicePrice_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_is_active ,callback_data=f'editServiceIsAcive_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_delete_service ,callback_data=f'editServiceDelete_{ServiceID}'))
    bot.send_message(chat_id=call.message.chat.id,text=createLableServicesToShowOnButton(ServiceID), reply_markup=markup)


#### markup Update name Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceName_"))
def service_update_name(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    serviceid=int(call.data.split('_')[1])
    bot.send_message(chat_id=call.message.chat.id,text=text_update_service_name)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_update_name,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id,chat_id=call.message.chat.id,) as data:
        data['service_id']= serviceid 
#### state Update Name Service Panel
@bot.message_handler(state=admin_State.state_service_update_name)
def service_section_update_name(msg : Message):
    with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id,) as data:
        serviceid = int(data['service_id'])
        db_Service_Update_Service_Name(service_id=serviceid , name=msg.text)
        showtext=createLableServicesToShowOnButton(serviceid)
        bot.send_message(chat_id=msg.chat.id,text=f'{showtext}\n\n نام آیتم بالا با موفقیت تغییر کرد')
    bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id)




#### markup Update time_slot Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceTimeSlot_"))
def service_update_timeslot(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    serviceid=int(call.data.split('_')[1])
    bot.send_message(chat_id=call.message.chat.id,text=text_update_service_time_slots)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_update_time_slots,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id,chat_id=call.message.chat.id,) as data:
        data['service_id']= serviceid
#### state Update time_slot Service Panel
@bot.message_handler(state=admin_State.state_service_update_time_slots)
def service_section_update_timeslot(msg : Message):
    try:
        updated_time_slots=int(msg.text)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id,) as data:
            serviceid = int(data['service_id'])
            db_Service_Update_Service_Time_Slot(service_id=serviceid , time_slots=updated_time_slots)
            showtext=createLableServicesToShowOnButton(serviceid)
            bot.send_message(chat_id=msg.chat.id,text=f'{showtext}\n\n زمان آیتم بالا با موفقیت تغییر کرد')
        bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)




#### markup Update price Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServicePrice_"))
def service_section_update_price(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    serviceid=int(call.data.split('_')[1])
    bot.send_message(chat_id=call.message.chat.id,text=text_update_service_price)
    bot.set_state(user_id=call.message.chat.id,state=admin_State.state_service_update_price,chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id,chat_id=call.message.chat.id,) as data:
        data['service_id']= serviceid
#### state Update price Service Panel
@bot.message_handler(state=admin_State.state_service_update_price)
def service_section_update_price(msg : Message):
    try:
        updated_price=int(msg.text)
        with bot.retrieve_data(user_id=msg.chat.id,chat_id=msg.chat.id,) as data:
            serviceid = int(data['service_id'])
            db_Service_Update_Service_Price(service_id=serviceid , price=updated_price)
            showtext=createLableServicesToShowOnButton(serviceid)
            bot.send_message(chat_id=msg.chat.id,text=f'{showtext}\n\n  قیمت آیتم بالا با موفقیت تغییر کرد')
        bot.delete_state(user_id=msg.chat.id,chat_id=msg.chat.id)
    except ValueError:
        bot.send_message(chat_id=msg.chat.id,text=text_update_service_error_int)




#### markup Update is_active Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceIsAcive_"))
def service_section_update_is_active(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    serviceid=int(call.data.split('_')[1])
    data=db_Service_Get_Is_Active_Services(serviceid)
    if data==0 :
        db_Service_Enable_Service(serviceid)
        showtext=createLableServicesToShowOnButton(serviceid)
        bot.send_message(chat_id=call.message.chat.id,text=f'{showtext}\n\n  آیتم بالا با موفقیت فعال شد')
    else :
        db_Service_Disable_Service(serviceid)
        showtext=createLableServicesToShowOnButton(serviceid)
        bot.send_message(chat_id=call.message.chat.id,text=f'{showtext}\n\n  آیتم بالا با موفقیت غیرفعال شد')
    



#### markup delete Service Panel
@bot.callback_query_handler(func= lambda m:m.data.startswith("editServiceDelete_"))
def service_update_name(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    serviceid=int(call.data.split('_')[1])
    showtext=createLableServicesToShowOnButton(serviceid)
    db_Service_Delete_Service(service_id=serviceid)
    bot.send_message(chat_id=call.message.chat.id,text=f'{showtext}\n\n  آیتم بالا با موفقیت حذف شد')

######################################################################## access to all users

###########################################  fins user by ID
### markup user find
@bot.message_handler(func= lambda m:m.text == mark_text_admin_find_user)
def reserve_time(msg : Message):
    bot.send_message(chat_id=msg.chat.id,text=text_user_find)
    bot.set_state(user_id=msg.from_user.id,state=admin_State.state_user_find,chat_id=msg.chat.id)

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
    users_list=list(db_Users_Get_All_Users())
    markup = InlineKeyboardMarkup()
    for item in users_list :
        showtext=createLabelUsersToShowOnButton(item[0])
        button = InlineKeyboardButton(text=showtext ,callback_data=f'showUsersList_{item[0]}')
        markup.add(button)
    bot.send_message(chat_id=msg.chat.id,text=text_users_list, reply_markup=markup)

@bot.callback_query_handler(func= lambda m:m.data.startswith("showUsersList_"))
def convertUserID(call:CallbackQuery):
    bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
    user_id=int(call.data.split('_')[1])
    username=db_Users_Get_Username_user(user_id=user_id)
    phone_number=db_Users_Get_Phone_Number_User(user_id=user_id)
    url=change_Username_To_URL(username , phone_number)
    name_lasname=createLabelUsersToShowOnButton(user_id=user_id)
    showtext=f"{name_lasname} \n {url}"
    bot.send_message(chat_id=call.message.chat.id,text=showtext)
                     
#######################################################################!   User Panel
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
        db_Users_Update_Username_User(user_id=msg.from_user.id , username=msg.from_user.username)#update Username while every reservation
        name = db_Users_Get_Name_User(msg.from_user.id)
        if name == 'empty' : 
            activation_user(msg=msg)
        else :
            #TODO insert calendar to reserve
            return True
#### activation_user
def activation_user(msg : Message) :
        name = db_Users_Get_Name_User(msg.from_user.id)
        last_name = db_Users_Get_Last_Name_User(msg.from_user.id)
        phone_number = db_Users_Get_Phone_Number_User(msg.from_user.id)
        bot.send_message(chat_id=msg.from_user.id,text=text_enter_name)
        bot.set_state(user_id=msg.chat.id,state=user_State.state_info_enter_name,chat_id=msg.chat.id)


### Enter name for first time after press 'reserve time'
@bot.message_handler(state=user_State.state_info_enter_name)
def reserve_section_enter_name_frist_time(msg : Message):
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
    bot.send_message(chat_id=msg.from_user.id,text=text_compelet_enter_info)


####################################################################### Account Info Section
@bot.message_handler(func= lambda m:m.text == mark_text_account_info)
def account_info(msg : Message):
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
    bot.send_message(msg.chat.id, f"{text_support}\n{SUPPORT_USERNAME}", parse_mode='Markdown')
########################################################################! END :)
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