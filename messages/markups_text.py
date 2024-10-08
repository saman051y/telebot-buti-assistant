#messages for all users
from database.db_setwork import *
from database.db_weeklysetting import *
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from messages.messages_function import *
from messages.commands_msg import *
###############################################################! for client
mark_text_reserve_time='رزرو وقت'
mark_text_reserved_time='مشاهده رزرو ها '
mark_text_support='پشتیبانی'
mark_text_account_info='حساب کاربری'
mark_text_update_name = 'ویرایش نام'
mark_text_update_last_name = 'ویرایش نام خانوادگی'
mark_text_update_phone_number ='ویرایش شماره تماس'
mark_text_admin_empty_time = 'ساعت های خالی'
###############################################################! for admin
mark_text_admin_reserved_time = 'ساعت های رزرو شده'
mark_text_admin_set_work_time = 'تنظیمات ساعت کاری'
mark_text_admin_weekly_time = 'تنظیمات روز های هفته'
mark_text_admin_set_service = 'تنظیمات خدمات'
mark_text_admin_send_message_to_all='ارسال پیام همگانی'
mark_text_admin_users_list='لیست مخاطبین'
mark_text_admin_find_user='جستجو در مخاطبین'
mark_text_admin_bot_info='اطلاعات ربات'
mark_text_admin_service_insert = 'افزودن خدمات'
mark_text_admin_service_update='ویرایش خدمات'
mark_text_admin_service_delete='حذف خدمات'
mark_text_admin_service_list='لیست خدمات'
mark_text_admin_update_name='ویرایش نام'
mark_text_admin_update_time_slots='ویرایش تایم'
mark_text_admin_update_price='ویرایش قیمت'
mark_text_admin_update_is_active='تغییر فعال بودن'
mark_text_admin_delete_service='حذف سرویس'
#########################################
text_set_work_enable='تنظیم تایم کاری'
text_set_work_disable='تنظیم تایم استراحت'
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
########################################## generate markup for weekly tiem
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
    for i in range(0,6):
        date = today + timedelta(days=i)
        text=convertDateToPersianCalendar(date=str(date))
        button = InlineKeyboardButton(text=f'{text}' ,callback_data=f'SetWorkTime:{date}')
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
        result_update = db_SetWork_Create_Date_Without_part(date=date , part1_start_time=all_part[0] , part1_end_time=all_part[1] , part2_start_time=all_part[2] , part2_end_time=all_part[3])
        part=db_SetWork_Get_Part1_or_Part2_of_Day(date=date ,part=i+1)
    if part not in ['False',False]:
        for i in range(1,3):
            part=db_SetWork_Get_Part1_or_Part2_of_Day(date=date ,part=i)  
            buttons_part=[]  
            part_text2=''
            
            if part[0] in ['Null',None]:
                part_text2 = 'افزودن پارت'
                button_part = InlineKeyboardButton(text=part_text2, callback_data=f'SetWorkUpdatePart:{i}:{date}')
                markup.add(button_part)
            if part[0] not in ['Null',None]:
                part_start_time = str(part[0])
                part_end_time = str(part[1])
                text_part_start_time=part_start_time.split(':')[0]+ f':'+ part_start_time.split(':')[1]
                text_part_end_time = part_end_time.split(':')[0]+ f':'+ part_end_time.split(':')[1]
                part_text2=text_part_start_time + f' الی '+ text_part_end_time
                button_part_delete = InlineKeyboardButton(text=f'حذف', callback_data=f'SetWorkDeletePart:{i}:{date}')
                buttons_part += [button_part_delete] 
                button_part = InlineKeyboardButton(text=part_text2, callback_data=f'SetWorkUpdatePart:{i}:{date}')
                buttons_part += [button_part] 
            markup.add(*buttons_part)
        return markup
##########################################
def markup_generate_services_for_reserve(services):
    """call back data is select_service_{id}
    AND for reservation selection end call back is make_reservation """
    markup=InlineKeyboardMarkup()
    if services is None or len(services)==0 :
        return markup.add(InlineKeyboardButton(text="هیچ سرویسی جهت رزرو موجود نیست",callback_data="!!!!!!!!!"))
    for service in services:
        # print(service)
        if not service[4]:
            continue 
        id=service[0]
        name = service[1]
        price = service[3]
        isEnable="انتخاب شده" if service[5] ==1 else "انتخاب نشده"
        markup.add(InlineKeyboardButton(text=f"{name}:{price}:{isEnable}",callback_data=f"select_service_{id}"))
    markup.add(InlineKeyboardButton(text="اتمام انتخاب",callback_data="make_reservation"))
    return markup