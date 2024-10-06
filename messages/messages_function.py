from auth.auth import *
from database.db_service import *
from database.db_users import *
from functions.time_date import *
import re
#######################################################################
def text_cleaner_info(data):
    user_id = data[0]
    phone_number = data[1]
    username = data[2]
    join_date = convertDateToPersiancalendar(str(data[3]))
    name = data[4]
    last_name = data[5]
    export_text = (f"شناسه عددی       {user_id} \nشناسه کاربری      {username} \nنام                     {name}\n"
     f"نام خانوادگی       {last_name}\nشماره تماس       {phone_number} \nتاریخ عضویت     {join_date}\n  ")
    return export_text
#######################################################################
def validation_admin(user_id):
    if user_id in MAIN_ADMIN_USER_ID:
        return True    
    return False
#######################################################################
def createLableServicesToShowOnButton(user_id):
    data = db_Service_Get_Service_With_Id(user_id)
    name=data[1]
    time_slot=convert_time_slot_to_time(data[2])
    price=data[3]
    is_active=data[4]
    if is_active == 1:
        is_active_text = 'فعال'
    else : 
        is_active_text = 'غیر فعال'

    export_text = (f" {name} : {time_slot} : {price} : {is_active_text}")
    return export_text
#######################################################################
def change_Username_To_URL(username,phone_number) :
    if username=='None' :
        export_text=f"شماره تماس : {phone_number} \n  فاقد آیدی میباشد    " 
        return export_text
    else :
        export_text=f"شماره تماس : {phone_number} \n https://t.me/{username} "
        return export_text
    
#######################################################################
def createLabelUsersToShowOnButton(user_id:int):
    data = list(db_Users_Find_User_By_Id(user_id))
    phone_number=data[1]
    username=data[2]
    name=data[4]
    last_name=data[5]
    export_text=f"{name}  {last_name}"
    return export_text
#######################################################################
def ConvertVariableInWeeklySettingToPersian(data:str):
    """input is Gorgian day like 'friday' and output is like 'جمعه' """
    result = data
    if data == 'saturday':
        result = 'شنبه'
    if data =='sunday':
        result = 'یکشنبه'
    if data =='monday':
        result = 'دوشنبه'
    if data =='tuesday':
        result = 'سه شنبه'
    if data =='wednesday':
        result = 'چهارشنبه'
    if data =='thursday':
        result = 'پنج شنبه'
    if data =='friday':
        result = 'جمعه'
    if data =='part1':
        result = 'پارت اول'
    if data =='part2':
        result = 'پارت دوم'
    if data =='1':
        result ='  فعال  '
    if data =='0':
        result ='  غیر فعال  '
    if data =='None':
        result ='خالی'

    pattern =  r"^(?:[01]\d|2[0-3]):(00|15|30|45):01/(?:[01]\d|2[0-3]):(00|15|30|45):00$"
    match = re.match(pattern, data)
    if match :
        start_time, end_time = data.split('/')
        formatted_start_time = start_time[:5]  # Get 'HH:MM' from 'HH:MM:SS'
        formatted_end_time = end_time[:5]
        result = f'{formatted_start_time} الی {formatted_end_time}'
    return result
#######################################################################