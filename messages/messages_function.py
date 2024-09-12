from auth.auth import *
from database.db_service import *
from database.db_users import *
#######################################################################
def text_cleaner_info(data):
    user_id = data[0]
    phone_number = data[1]
    username = data[2]
    join_date = data[3]
    name = data[4]
    last_name = data[5]
    export_text = (f"شناسه عددی       {user_id} \nشناسه کاربری      {username} \nنام                     {name}\n"
     f"نام خانوادگی      {last_name}\nشماره تماس        {phone_number} \nتاریخ عضویت     {join_date}\n  ")
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
    time_slot=data[2]
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