#messages for all users
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup

from messages.messages_function import createLableServicesToShowOnButton

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

def markup_service(ServiceID:int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_name ,callback_data=f'editServiceName_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_time_slots ,callback_data=f'editServiceTimeSlot_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_price ,callback_data=f'editServicePrice_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_update_is_active ,callback_data=f'editServiceIsAcive_{ServiceID}'))
    markup.add(InlineKeyboardButton(text=mark_text_admin_delete_service ,callback_data=f'editServiceDelete_{ServiceID}'))
    return markup

def makrup_service_list(sorted_serviceData):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=mark_text_admin_service_insert ,callback_data=mark_text_admin_service_insert))
    for item in sorted_serviceData :
        text=createLableServicesToShowOnButton(item[0])
        button = InlineKeyboardButton(text=text ,callback_data=f'showServiceList_{item[0]}')
        markup.add(button)
    return markup