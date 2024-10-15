from auth.auth import *
from database.db_reserve_service import getResSerWithResId
from database.db_service import *
from database.db_users import *
from functions.time_date import *
import re
#######################################################################
def text_cleaner_info(data):
    user_id = data[0]
    phone_number = data[1]
    username = data[2]
    join_date = convertDateToPersianCalendar(str(data[3]))
    name = data[4]
    export_text = (f"شناسه عددی             {user_id} \n🔢 شناسه کاربری      {username} \n🔡 نام                     {name}\n"
     f"📞 شماره تماس       {phone_number} \n📅 تاریخ عضویت     {join_date}\n.")
    return export_text
#######################################################################
def validation_admin(user_id):
    if user_id in MAIN_ADMIN_USER_ID:
        return True    
    return False
#######################################################################
def createLabelServicesToShowOnButton(user_id):
    data = db_Service_Get_Service_With_Id(user_id)
    name=data[1]
    time = datetime.strptime(str(data[2]),'%H:%M:%S').strftime('%H:%M')
    time=time[:5]
    price=data[3]
    is_active=data[4]
    if is_active == 1:
        is_active_text = '✅'
    else : 
        is_active_text = '❌'
    export_text = (f" {name}  {time}  {price} هزارتومان  {is_active_text}")
    return export_text
#######################################################################
def accountInfoCreateTextToShow(user_id=str) :
    data_user=db_Users_Find_User_By_Id(user_id=user_id)
    username=data_user[2]
    if data_user in [False , 'False' , None , 'None']:
        return False
    else :
        text_info_user=text_cleaner_info(data=data_user)
        text =  f'{text_info_user}'
        if data_user[2] not in [False , 'False' , None , 'None']:
            text =  f'{text_info_user}\nhttps://t.me/{username}'
    return text
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
        result = 'صبح'
    if data =='part2':
        result = 'عصر'
    if data =='1':
        result ='✅'
    if data =='0':
        result ='❌'
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
def text_make_reservation_info(price,time,services):
    names=""
    for service in services:
        if (service[5] == 0 ):
            continue
        names=f"{names} - {service[1]} \n"
    text=f"""
هزینه کل خدمات انتخاب شده : {price}
کل تایم رزرو شده : {time}
خدمات انتخاب شده : {names}
"""
    return text
#######################################################################
def make_reservation_info_text_for_user(price:int,duration:str,date:str,time:str,services):
    names=""
    for service in services:
        if (service[5] == 0 ):
            continue
        names=f"{names} - {service[1]}"
    text=f"""
هزینه کل :  {price}
مدت زمان رزور شده : {duration}
تاریخ انتخاب شده : {date}
ساعت انتخاب شده : {time}
خدمات انتخاب شده : {names}
"""
    return text

#######################################################################
def make_reservation_info_text_for_admin(reserve_id,user_id):
    #reserve info
    reserve=db_Reserve_Get_Reserve_With_Id(reserve_id=reserve_id)
    date=reserve[2]
    start_time=reserve[3]
    end_time=reserve[4]
    price=reserve[6]
    #service names
    services_id=getResSerWithResId(reserve_id=reserve_id)
    services=[]
    for service_id in services_id:
       services.append (db_Service_Get_Service_With_Id(service_id=service_id[0]))
    names=""
    total_price=0
    for service in services:
        names=f"{names} - {service[1]}"
        total_price= total_price+ int(service[3])
    week_day=get_weekday(f"{date}")
    user=db_Users_Find_User_By_Id(user_id=user_id)
    text=f"""
اطلاعات کاربر
نام: {user[4]}
نام خانوادگی: {user[5]}
نام کاربری:  {user[2]}
شناسه کاربر: {user[0]}
هزینه پرداخت شده :  {price}
تاریخ انتخاب  :  {week_day} = {date} 
ساعت شروع  : {start_time}
ساعت اتمام : {end_time}
خدمات رزرو شده : {names}
مجموع قیمت خدمات انتخاب شده : {total_price}
"""
    return text
#######################################################################
def text_cart_info():
    text="""
شماره کارت: 
مالک کارت:
بانک :
"""
    return text
#######################################################################