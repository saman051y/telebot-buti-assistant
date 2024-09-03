#######################################################################
def text_cleaner_info(data):
    user_id = data[0]
    phone_number = data[1]
    username = data[2]
    join_date = data[3]
    name = data[4]
    last_name = data[5]
    export_text = (f"شناسه عددی {user_id} \nشناسه کاربری: {username} \nنام: {name}\n"
     f"نام خانوادگی :{last_name} \nشماره تماس: {phone_number} \nتاریخ عضویت: {join_date}\n  ")
    return export_text
#######################################################################
