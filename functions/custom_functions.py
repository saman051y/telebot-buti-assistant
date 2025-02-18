


from datetime import datetime, timedelta
from database.db_reserve import db_Reserve_Get_Date_And_parts_Not_Reserved
from database.db_setwork import db_SetWork_Get_Part1_or_Part2_of_Day, db_SetWork_Get_Part1_or_Part2_of_Day_for_1Month
from functions.time_date import GenerateNext5Weeks, GenerateNext7Day, convert_duration_to_slot_number, convert_slot_number_to_duration, find_consecutive_sequence

import re
##################################3
def extract_reserveId_and_userId(text):
    """ return reserve_id, user_id"""
    reserve_match = re.search(r"reserve_id=(\d+)", text)
    user_match = re.search(r"user_id=(\d+)", text)
    
    if reserve_match and user_match:
        reserve_id = int(reserve_match.group(1))
        user_id = int(user_match.group(1))
        return reserve_id, user_id
    else:
        return None, None
###########################
def get_free_time_for_next_7day(duration:str,offset:int=0):

    """Returns available reservation slots for the next 7 days."""
    
    # Convert duration to 15-min time slots
    duration_as_time_slot = convert_duration_to_slot_number(duration)

    # Generate all necessary workdays if needed
    GenerateNext5Weeks()

    # Get the target date range
    today = datetime.now().date() + timedelta(days=int(offset))
    date_range = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    # Fetch all relevant data in a single query
    placeholders = ', '.join(['%s'] * len(date_range))  # For SQL IN clause
    days=db_SetWork_Get_Part1_or_Part2_of_Day_for_1Month(data=placeholders,date_range=date_range)
    days_list_can_reserve = []
    days_list=[]
    for row in days:
            date = row['date']
            for part in range(1, 3):
                start_time = row[f'part{part}_start_time']
                end_time = row[f'part{part}_end_time']
                if start_time and end_time:
                    days_list.append((date, start_time, end_time))

    #search empty time by duration in each day that user could reserve
    for i in range(len(days_list)):
        array_all_time_slot_for_each_day=[]
        list_time_that_could_be_reserve =[]
        date=str(days_list[i][0])
                    # بررسی مقدار None
        if days_list[i][1] is None or days_list[i][2] is None:
            continue  # اگر یکی از مقادیر None بود، ادامه دهید و از چاپ صرف‌نظر کنید
        start_time = datetime.strptime(str(days_list[i][1]),'%H:%M:%S').strftime('%H:%M:%S')
        end_time = datetime.strptime(str(days_list[i][2]),'%H:%M:%S').strftime('%H:%M:%S')
        # get all empty time by tim_slot=15 Min
        list_time_that_could_be_reserve  = db_Reserve_Get_Date_And_parts_Not_Reserved(date=date ,start_time=start_time, end_time=end_time)
        for i in range(len(list_time_that_could_be_reserve)) :
            array_all_time_slot_for_each_day.append(list_time_that_could_be_reserve[i][2])
        #get first time that able to be reserved as time slot
        reserved_time_as_time_slot=find_consecutive_sequence(array_all_time_slot_for_each_day ,duration_as_time_slot)
        if reserved_time_as_time_slot not in[None ,'None']:
            #convert time slot to time like time slot 2 of 8:00:00 is 08:30:00 (2th 15 Min of 08:00)
            time_could_be_reserve = convert_slot_number_to_duration(start_time , reserved_time_as_time_slot )
            export_list=(date,part,time_could_be_reserve)
            days_list_can_reserve.append(export_list)
    if days_list_can_reserve == [] :
        return None 
    return(days_list_can_reserve)


##################################33
def calculate_time_difference(time_str1: str, time_str2: str) -> int:
    # تعریف فرمت‌های مختلف
    full_time_format = "%Y-%m-%d %H:%M:%S"
    time_format = "%H:%M:%S"
    
    # تابعی برای استخراج زمان از ورودی
    def extract_time(time_str):
        try:
            return datetime.strptime(time_str, full_time_format).time()
        except ValueError:
            return datetime.strptime(time_str, time_format).time()

    # استخراج زمان‌ها
    time1 = extract_time(time_str1)
    time2 = extract_time(time_str2)
    
    # محاسبه اختلاف زمانی
    time_difference = abs((datetime.combine(datetime.today(), time2) - datetime.combine(datetime.today(), time1)).total_seconds()) / 3600  # تبدیل به ساعت

    # بررسی اختلاف و برگرداندن مقدار مناسب
    if time_difference < 4:
        return 100
    else:
        return 200