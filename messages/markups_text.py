#messages for all users
from database.db_reserve import *
from database.db_setwork import *
from database.db_weeklysetting import *
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from messages.messages_function import *
from messages.commands_msg import *
from datetime import datetime, timedelta
###############################################################! for user
mark_text_reserve_time='رزرو وقت 💅🏼'
mark_text_reserved_time='مشاهده رزرو ها 📜'
mark_text_support='پشتیبانی 💬'
mark_text_account_info='حساب کاربری 🙋🏻‍♀️'
mark_text_update_name = 'ویرایش نام 🔤'
mark_text_update_phone_number ='ویرایش شماره تماس 📞'
###############################################################! for admin
mark_text_admin_empty_time = 'وضعیت روزها 📊'
mark_text_admin_reserved_time = 'ساعت های رزرو شده'
mark_text_admin_set_work_time = 'تنظیمات ساعت کاری ⏰'
mark_text_admin_weekly_time = 'تنظیمات هفته 📅'
mark_text_admin_set_service = 'تنظیمات خدمات 💅🏼'
mark_text_admin_bot_setting="تنظیمات ربات"
mark_text_admin_custom_reserve="رزرو ساعت دلخواه ⏬"
mark_text_admin_send_message_to_all='ارسال پیام همگانی'
mark_text_admin_users_list='لیست مخاطبین'
mark_text_admin_send_message_to_all='ارسال پیام همگانی 🗣'
mark_text_admin_users_list='لیست مخاطبین 👥'
mark_text_admin_find_user='جستجو 🔍'
mark_text_admin_bot_info='اطلاعات ربات'
mark_text_admin_service_insert = 'افزودن خدمات 📥'
mark_text_admin_update_name='ویرایش نام 🔤'
mark_text_admin_update_time_slots='ویرایش تایم ⏰'
mark_text_admin_update_price='ویرایش قیمت 💰' 
mark_text_admin_update_is_active='تغییر فعال بودن ✅❌'
mark_text_admin_delete_service='حذف 🗑'
mark_text_admin_bot_setting = 'تنظیمات ربات 🤖'
markup_text_add_admin="📥 افزودن ادمین"
markup_text_list_admin="مشاهده لیست"
markup_text_remove_admin="🗑 حذف ادمین"
markup_text_change_main_admin="💬 تغییر به ادمین پاسخگو"
markup_text_no_change_for_main_admin = 'بعد از عوض کردن ادمین پاسخگو💬 قادر به حذف ادمین هستید'
markup_text_admin_list="لیست ادمین ها 👑"
######################################### create markup for account info in user panel
def markup_generate_account_info(user_id:int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_update_name, callback_data=f'updateNameUser_{user_id}'))
    markup.add(InlineKeyboardButton(text=mark_text_update_phone_number, callback_data=f'updatePhoneNumberUser_{user_id}'))
    return markup
######################################### create markup for update service
def markup_generate_service(ServiceID:int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_name ,callback_data=f'editServiceName_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_time_slots ,callback_data=f'editServiceTimeSlot_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_price ,callback_data=f'editServicePrice_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_is_active ,callback_data=f'editServiceIsAcive_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_delete_service ,callback_data=f'editServiceDelete_{ServiceID}'))
    return markup
########################################## create markup for show service
def makrup_generate_service_list(sorted_serviceData):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_admin_service_insert ,callback_data=mark_text_admin_service_insert))
    for item in sorted_serviceData :
        text=createLabelServicesToShowOnButton(item[0])
        button = InlineKeyboardButton(text=text ,callback_data=f'showServiceList_{item[0]}')
        markup.add(button)
    return markup
########################################## generate markup for weekly time
def makrup_generate_weekly_time_list():
    bot_setting=db_WeeklySetting_Get_All()
    markup = InlineKeyboardMarkup()
    buttons = []
    for i in bot_setting :
        name=i[1]
        value=i[2]
        name_persian=ConvertVariableInWeeklySettingToPersian(name)
        value_persian=ConvertVariableInWeeklySettingToPersian(value)
        text_button = f'{name_persian} {value_persian}'
        button = InlineKeyboardButton(text=text_button, callback_data=f'weeklysetting:{name}')
        buttons.append(button)
    if len(buttons) >= 2:
        markup.row(*buttons[:2])  # First 2 buttons in the first row
    if len(buttons) >= 4:
        markup.row(*buttons[2:4])  # Next 2 buttons in the second row
    if len(buttons) >= 6:
        markup.row(*buttons[4:6])  # Next 2 buttons in the third row
    if len(buttons) >= 7:
        markup.add(buttons[6])     # Single button in the fourth row
    if len(buttons) >= 9:
        markup.row(*buttons[7:9])  # Last 2 buttons in the fifth row
    return markup
########################################## generate markup setwork list until 7 days
def makrup_generate_set_work_list_of_days() :
    markup = InlineKeyboardMarkup()
    today = datetime.now().date()
    for i in range(7):
        date = today + timedelta(days=i)
        text=convertDateToPersianCalendar(date=str(date))
        text =f'🗓 {text}'
        button = InlineKeyboardButton(text=text ,callback_data=f'SetWorkTime:{date}')
        markup.add(button)
    return markup
########################################## generate markup for parts list of set work  
def makrup_generate_parts_list_of_set_work(date):
    
    markup = InlineKeyboardMarkup()
    part_text2=''
    all_part = []
    part=db_SetWork_Get_Part1_or_Part2_of_Day(date=date ,part=1)
    if part in ['False',False]:
        for i in range(2):
            default_parts=db_WeeklySetting_Get_Parts()
            if default_parts[i][1] in ['Null' , None , 'None']:
                part_start_time = 'Null'
                part_end_time = 'Null'
            else:   
                #if default_parts[i][1] not in ['Null' , None , 'None']:
                part = str(default_parts[i][1])
                default_parts_str=str(default_parts[i][1])
                part_start_time= default_parts_str.split('/')[0]
                part_end_time= default_parts_str.split('/')[1]
            all_part += [(part_start_time)]
            all_part += [(part_end_time)]
        result_update = db_SetWork_Create_date(date=date , part1_start_time=all_part[0] , part1_end_time=all_part[1] , part2_start_time=all_part[2] , part2_end_time=all_part[3])
        part=db_SetWork_Get_Part1_or_Part2_of_Day(date=date ,part=i+1)
    if part not in ['False',False]:
        for i in range(1,3):
            part=db_SetWork_Get_Part1_or_Part2_of_Day(date=date ,part=i)  
            buttons_part=[]  
            part_text2=''
            
            if part[0] in ['Null',None]:
                part_tex_array = ['صبح ☀️','عصر 🌙']
                part_text2=f'📥 افزودن {part_tex_array[i-1]}'
                button_part = InlineKeyboardButton(text=part_text2, callback_data=f'SetWorkUpdatePart:{i}:{date}')
                markup.add(button_part)
            if part[0] not in ['Null',None]:
                part_start_time = str(part[0])
                part_end_time = str(part[1])
                text_part_start_time=part_start_time.split(':')[0]+ f':'+ part_start_time.split(':')[1]
                text_part_end_time = part_end_time.split(':')[0]+ f':'+ part_end_time.split(':')[1]
                part_text2=f'⏰ {text_part_start_time} الی {text_part_end_time}'
                button_part_delete = InlineKeyboardButton(text=f'حذف 🗑', callback_data=f'SetWorkDeletePart:{i}:{date}')
                buttons_part += [button_part_delete] 
                button_part = InlineKeyboardButton(text=part_text2, callback_data=f'SetWorkUpdatePart:{i}:{date}')
                buttons_part += [button_part] 
            markup.add(*buttons_part)
        return markup
##########################################
def markup_generate_services_for_reserve(services,total_selected:int=0,admin:bool=False):
    """call back data is select_service_{id}
    AND for reservation selection end call back is make_reservation """
    markup=InlineKeyboardMarkup()
    if services is None or len(services)==0 :
        return markup.add(InlineKeyboardButton(text="هیچ خدماتی جهت رزرو موجود نیست",callback_data="!!!!!!!!!"))
    for service in services:
        if not service[4]:
            continue 
        id=service[0]
        name = service[1]
        price = service[3]
        isEnable=" ✅ " if service[5] ==1 else ""
        if admin:
            markup.add(InlineKeyboardButton(text=f"💅🏼 {name} {price}هزار تومان {isEnable}",callback_data=f"admin_select_service_{id}"))
        else:
            markup.add(InlineKeyboardButton(text=f"💅🏼 {name} {price}هزار تومان {isEnable}",callback_data=f"select_service_{id}"))
    if total_selected>0:
        if admin:
            markup.add(InlineKeyboardButton(text="تایید نهایی 💫",callback_data="admin_make_reservation"))
        else:
            markup.add(InlineKeyboardButton(text="تایید نهایی 💫",callback_data="make_reservation"))
    return markup
########################################## show parts of days by needed time for reserve 

##########################################
def makrup_generate_empty_time_of_day(delete_day:str,admin:bool=False) :
    markup = InlineKeyboardMarkup()
    today = datetime.now().date()
    custom_reserve_text= "customReserve" if admin else ''
    for i in range(7):
        date = today + timedelta(days=i)
        if delete_day != str(date) :
            text_date=convertDateToPersianCalendar(date=str(date))
            text = f'🗓 {text_date}'
            button = InlineKeyboardButton(text=text ,callback_data=f'{custom_reserve_text}getEmptyTime:{date}')
            markup.add(button)
    return markup
##########################################
def makrup_reserve_date(date_persian,weekDay,time,date):
    """callback data : reserve_date_"""
    return InlineKeyboardButton(text=f"{date_persian}  {time[:5]}",
                                callback_data=f"reserve_date_{date}_{time}")
##########################################
def markup_admin_bot_setting(bot_is_enable:bool=True):
    """
    bot enable : change_bot_enable_disable
    """
    markup=InlineKeyboardMarkup()
    text_bot_is_enable="فعال ✅" if bot_is_enable else "غیرفعال ❌"
    btn_enable_disable=InlineKeyboardButton(text=f"🤖 ربات {text_bot_is_enable}",callback_data=f"change_bot_enable_disable")
    btn_admin_list=InlineKeyboardButton(text=f"👑 تغییر ادمین ها",callback_data=f"change_admin_list")
    btn_welcome_message=InlineKeyboardButton(text=f"💁‍♀️ تغییر پیام خوش آمدگویی",callback_data=f"welcome_message")
    btn_change_card_info=InlineKeyboardButton(text=f"💳 تغییر شماره کارت",callback_data=f"change_cart_info")
    markup.add(btn_enable_disable)
    markup.add(btn_admin_list)
    markup.add(btn_welcome_message)
    markup.add(btn_change_card_info)
    return markup
######
def markup_show_admin_list(admin_list):
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text=markup_text_add_admin,callback_data=f"admin_list_add")
    markup.add(btn1) 
    if len(admin_list) < 1  :
        btn=InlineKeyboardButton(text=text_markup_no_admin,callback_data="!!!!!!!")
        markup.add(btn) 
        return markup
    for admin in admin_list:
        name=db_Users_Get_Name_User(admin[0])
        user_is_main_admin_bool=bool(admin[1])
        user_is_main_admin="💬ادمین پاسخگو" if user_is_main_admin_bool else ""
        btn=InlineKeyboardButton(text=f"👑 {name}  {user_is_main_admin}",callback_data=f"adminList_{admin[0]}_{user_is_main_admin}")
        markup.add(btn)
    return markup
##########################################
def markup_generate_list_of_users(user_id_for_delete):
    markup = InlineKeyboardMarkup()
    users_list=list(db_Users_Get_All_Users())
    text=mark_text_admin_find_user
    button = InlineKeyboardButton(text=text ,callback_data=f'searchForUser')
    markup.add(button)
    for item in users_list :
        name=item[4]
        user_id=item[0]
        text=f'✨ {name} ✨'
        if user_id != user_id_for_delete :
            button = InlineKeyboardButton(text=text ,callback_data=f'showUsersList_{user_id}')
            markup.add(button)
    return markup
##########################################
def markup_generate_reserved_list(reserve_list , delete_reserve_id:str):
    markup=InlineKeyboardMarkup()
    user_id= str(reserve_list[0]['user_id'])
    for reserve in reserve_list:
        reserve_id=reserve['id']
        if delete_reserve_id != str(reserve_id):
            date=convertDateToPersianCalendar(f"{reserve['date']}")
            start_time=convert_to_standard_time(f"{reserve['start_time']}")[:5]
            payment=(reserve['payment'])
            text=f"🗓{date} ⏰{start_time} 💰{payment} هزار تومان"
            btn=InlineKeyboardButton(text=text,callback_data=f"userSeeReserve_{reserve_id}_{user_id}")
            markup.add(btn)
    return markup