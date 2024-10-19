from datetime import datetime, timedelta
from convertdate import persian
import math
from database.db_setwork import *
from database.db_weeklysetting import *
from database.db_reserve import *
from messages.commands_msg import *
#########################################################
def convert_time_to_slot(time:str):
    """get a time like '01:30' return  6 (1 slot = 15 min)"""
    hour, min = map(int, time.split(":"))
    total_minutes=(hour*60) + min
    if total_minutes ==0 :return 0
    blocks = math.ceil(total_minutes / 15)
    return blocks
#########################################################
def convert_time_slot_to_time(time_slot:int):
    # تبدیل تعداد بلوک‌ها به دقیقه
    total_minutes = time_slot * 15
    
    # تبدیل دقیقه‌ها به ساعت و دقیقه
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    # فرمت کردن خروجی به صورت HH:MM
    return f"{hours:02}:{minutes:02}"
#########################################################
def gregorian_to_jalali(gregorian_date_str,reverse:bool=False):
    """
    Convert Gregorian date from string format 'YYYY-MM-DD' to Jalali (Shamsi) date.
    :param gregorian_date_str: Date in Gregorian calendar in 'YYYY-MM-DD' format
    :return: Date in Jalali calendar in 'YYYY-MM-DD' format
    """
    # Parse the input date string into a datetime object
    gregorian_date = datetime.strptime(gregorian_date_str, '%Y-%m-%d')
    
    # Extract year, month, and day from the datetime object
    year = gregorian_date.year
    month = gregorian_date.month
    day = gregorian_date.day
    
    # Convert Gregorian date to Jalali date
    jalali_date = persian.from_gregorian(year, month, day)
    
    # Format Jalali date into 'YYYY-MM-DD' string
    jalali_date_str = f"{jalali_date[0]}-{jalali_date[1]:02d}-{jalali_date[2]:02d}"
    if reverse :
        # Format Jalali date into 'DD-MM_YYYY' string
        jalali_date_str = f"{jalali_date[2]:02d}-{jalali_date[1]:02d}-{jalali_date[0]}"

    
    return jalali_date_str
#########################################################
def add_times(time1, time2):
    # تبدیل رشته‌های زمانی به timedelta
    t1 = datetime.strptime(time1, "%H:%M:%S")
    t2 = datetime.strptime(time2, "%H:%M:%S")
    
    # محاسبه مجموع زمان‌ها
    delta1 = timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
    delta2 = timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
    
    total_delta = delta1 + delta2
    
    # تبدیل نتیجه به فرمت "HH:MM:SS"
    total_seconds = int(total_delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours:02}:{minutes:02}:{seconds:02}"

#########################################################
def add_date(date_str:str, days:int):
    # تبدیل رشته تاریخ به شیء datetime
    date = datetime.strptime(date_str, '%Y-%m-%d')
    # اضافه کردن تعداد روزهای مورد نظر
    new_date = date + timedelta(days=days)
    # تبدیل نتیجه به فرمت رشته ای
    return new_date.strftime('%Y-%m-%d')



#########################################################
def date_isEq(time,eqTime):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(time, time_format).date()
    time_B = datetime.strptime(eqTime, time_format).date()
    if time_A==time_B :
        return True
    else:
        return False
#########################################################

def compare_time(lower: str, than: str) -> bool:
    """Return True if time1 < time2."""
    # بررسی فرمت و انتخاب الگوی مناسب
    if len(lower) == 5:  # فرمت بدون ثانیه
        time_format = "%H:%M"
    else:  # فرمت با ثانیه
        time_format = "%H:%M:%S"
        
    time_A = datetime.strptime(lower, time_format).time()

    # انجام همین کار برای ورودی دوم
    if len(than) == 5:  # فرمت بدون ثانیه
        time_format_than = "%H:%M"
    else:  # فرمت با ثانیه
        time_format_than = "%H:%M:%S"
    
    time_B = datetime.strptime(than, time_format_than).time()
    
    return time_A <= time_B
#########################################################
def compare_date(lower_eq,than):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(lower_eq, time_format).date()
    time_B = datetime.strptime(than, time_format).date()
    if time_A<=time_B :
        return True
    else:
        return False
#########################################################
def compare_date_is_eq(date1,date2):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(date1, time_format).date()
    time_B = datetime.strptime(date2, time_format).date()
    if time_A==time_B :
        return True
    else:
        return False
#########################################################
def date_is_past(past,than):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(past, time_format).date()
    time_B = datetime.strptime(than, time_format).date()
    if time_A<time_B :
        return True
    else:
        return False
#########################################################
def get_current_date():
    """ return : %Y-%m-%d """
    # دریافت تاریخ و ساعت لحظه‌ای
    now = datetime.now()
    # تبدیل به رشته با فرمت YYYY-MM-DD HH:MM:SS
    date_time_str = now.strftime("%Y-%m-%d")
    return date_time_str

#########################################################
def get_current_datetime():
    """ return : %Y-%m-%d %H:%M:%S """
    # دریافت تاریخ و ساعت لحظه‌ای
    now = datetime.now()
    # تبدیل به رشته با فرمت YYYY-MM-DD HH:MM:SS
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_str
#########################################################
def cal_date(days):
    """make date of day
    get (-1 to 6 ) return like 2024-08-05 
    [-1 means yesterday ]
    [0 mean today ]
    [1 mean tomorrow]
    """
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

#########################################################
# def cal_day(days):
#     """get a number and return it day like
#     1 => دوشنبه
#     0 => یکشنبه"""
#     tomorrow_date = datetime.now() + timedelta(days=days)
#     tomorrow_weekday = tomorrow_date.weekday()
#     # tomorrow_persian = days_of_week_name[tomorrow_weekday]
#     return tomorrow_persian

#########################################################
def get_current_time():
    """ return : %H:%M """

    # بدست آوردن زمان کنونی
    now = datetime.now()
    
    # قالب‌بندی زمان به صورت رشته‌ای با فرمت 'HH:MM:SS'
    current_time = now.strftime("%H:%M")
    
    return current_time
#########################################################
#check is valid time
def is_valid_time_format(time_str):
    try:
        # بررسی فرمت ساعت
        hours, minutes ,sec= map(int, time_str.split(":"))
        
        # بررسی محدوده ساعت و دقیقه
        if 0 <= hours <= 23 and 0 <= minutes <= 59 and  0<=sec <=59: 
            return True
        else:
            return False
    except ValueError:
        # اگر نتواند رشته را به اعداد تبدیل کند، یعنی فرمت اشتباه است
        return False
#########################################################
def time_deference(time_a,time_b):
    time_format = "%H"
    time_a = int(time_a.split(":")[0])
    time_b= int(time_b.split(":")[0])
    return time_b-time_a


######################################################### change timeDelta to Normal format
def convertTimeDeltaToTime(timedelta):
    """input like (1500) as total seconds and it return in format HH:MM:SS as string"""
    total_seconds = int(timedelta)
    if total_seconds>3600 :
        hours, remainder = divmod(total_seconds, 3600)
    else:
        hours=00
        remainder  = total_seconds
    minutes, seconds = divmod(remainder, 60)

    # Format the result as HH:MM:SS
    time_string = f'{hours:02}:{minutes:02}:{seconds:02}'
    return time_string
########################################################## get name of days as persian calendar

def convertDateToDayAsPersianCalendar(date:str):
    """input date string in Gorgian 'YYYY-MM-DD' format and return the day in Persian."""

    days_of_week_name = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه','یکشنبه']
    # Convert the string to a Gregorian date (assuming 'YYYY-MM-DD' format)
    gregorian_date = datetime.strptime(date, '%Y-%m-%d')
    # Get the weekday number (Monday is 0 and Sunday is 6)
    weekday_num = gregorian_date.weekday()
    # Map the weekday number to Persian day name
    persian_day_name = days_of_week_name[weekday_num]
    return persian_day_name
########################################################## get name of Month as persian calendar
# Persian month names mapping
def convertDateToMonthAsPersianCalendar(date:str):
    """Get a date string in Gorgian 'YYYY-MM-DD' format and return the day in Persian."""
    months_of_year_name = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
]
    persian_date=gregorian_to_jalali(date)
    persian_month_int=int(persian_date.split('-')[1])
    persian_month_str=months_of_year_name[persian_month_int - 1]
    return persian_month_str
########################################################## generate persian format date like 1403 مهر 08 شنبه
def convertDateToPersianCalendar(date:str):
    """input is Gregorian date like'224-09-29' and output is like '1403 مهر 08 شنبه' """
    jalali_date = gregorian_to_jalali(date)
    jalali_Year = jalali_date.split('-')[0]
    jalali_month = convertDateToMonthAsPersianCalendar(date)
    jalali_day_name = convertDateToDayAsPersianCalendar(date)
    jalali_day_number= jalali_date.split('-')[2]
    text = f'{jalali_day_name} {jalali_day_number} {jalali_month}'
    return text 
########################################################## input is date and output is name day of week
def convertDateToDayAsGregorianCalendar(date:str):
    """input is date like '2024-05-04' and output is like 'saturday'"""
    days_of_week_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    gregorian_date = datetime.strptime(date, '%Y-%m-%d')
    weekday_num = gregorian_date.weekday()
    Gregorian_day_name = days_of_week_name[weekday_num]
    return Gregorian_day_name
########################################################## generate 7 day from now by default as weekly setting 
def GenerateNext7Day() :
    today = datetime.now().date()
    get_default_parts= db_WeeklySetting_Get_Parts()
    default_parts =[]
    for i in range(2) :
        default_part= get_default_parts[i][1]
        start_time = 'Null'
        end_time = 'Null'
        if default_part not in [None , 'None' , 'Null']:
            start_time=str(default_part.split('/')[0])
            end_time=str(default_part.split('/')[1])
        default_parts += [start_time , end_time]
    for i in range(0,6):
        date = today + timedelta(days=i)
        day_of_week=convertDateToDayAsGregorianCalendar(date=str(date))
        day_status=db_WeeklySetting_Get_Value(day_of_week)
        result=False
        if day_status[2] == '1':
            # exist_day = db_SetWork_exist_date(str(date))
            # if not exist_day:
            result = db_SetWork_Create_date(date ,default_parts[0], default_parts[1], default_parts[2] , default_parts[3])
########################################################## calculate slot_number from start_time
def convert_slot_number_to_duration(start_time:str,slot_number:str):
    """input is time like 08:30:00 and slot_number like 2 
        and export is 2th 15Min then export is 09:00:00"""
    
    time_obj = datetime.strptime(start_time , "%H:%M:%S")
    
    # Calculate the total time to add based on the number of slots and slot duration
    total_minutes = int(slot_number) * 15
    
    # Add the total minutes to the time object
    new_time_obj = time_obj + timedelta(minutes=total_minutes)
    
    # Convert the updated time back to a string
    return new_time_obj.strftime("%H:%M:%S")
########################################################## input is duration and export is time_slot bu 15 Min
def convert_duration_to_slot_number(time_str):
    """input is duration and export is time_slot bu 15 Min like input 01:30:00 export 6"""
    # Parse the time string into a datetime object
    time_format = "%H:%M:%S"
    time_obj = datetime.strptime(time_str, time_format)
    
    # Calculate total minutes since midnight
    total_minutes = time_obj.hour * 60 + time_obj.minute
    
    # Calculate the slot number (each slot is 15 minutes)
    slot_number = total_minutes // 15
    
    return slot_number
##########################################################search for first time that empty as array
def find_consecutive_sequence(array, sequence_length):
    """input is array from empty time and get duration as time_slot number"""
    # Iterate through the list to find the first group of `sequence_length` consecutive numbers
    for i in range(len(array) - sequence_length + 1):
        # Check if the next numbers in the sequence are consecutive
        is_consecutive = all(array[i + j] == array[i] + j for j in range(sequence_length))
        
        if is_consecutive:
            return array[i]  # Return the first number of the consecutive sequence
########################################################## # user for calculate empty time
def calculate_numbers_in_a_row(array):
    """ find numbers in row like [1, 2, 3, 4, 14, 15, 16, 17, 18, 19, 20, 21, 22, 30] 
        and export like [(1, 4), (14, 22), (30, 30)]
        """
    if not array:
        return []
    array.sort()  # Make sure the list is sorted
    grouped = []
    start = array[0]  # Start the first group
    for i in range(1, len(array)):
        # Check if the current number is not consecutive to the previous one
        if array[i] != array[i - 1] + 1:
            # Append the start and the previous element as a tuple
            grouped.append((start, array[i - 1]))
            start = array[i]  # Start a new group

    # Append the last group
    grouped.append((start, array[-1]))
    return grouped

##########################################################
def convert_to_standard_time(time_string:str, input_format:str="%H:%M:%S"):
    try:
        # تبدیل رشته زمانی به شیء datetime بر اساس فرمت ورودی
        time_obj = datetime.strptime(time_string, input_format)
        # تبدیل زمان به فرمت استاندارد "HH:MM:SS"
        return time_obj.strftime("%H:%M:%S")
    except ValueError:
        return "Invalid format"
##########################################################
def get_weekday(date_str):
    # تاریخ را به فرمت "%Y-%m-%d" دریافت می‌کنیم و به نوع datetime تبدیل می‌کنیم
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    # گرفتن شماره روز هفته (0 = دوشنبه, 6 = یکشنبه)
    weekday_number = date.weekday()
    
    # لیستی از نام روزهای هفته به فارسی
    weekdays_farsi = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه', 'یکشنبه']
    
    return weekdays_farsi[weekday_number]

##########################################################
def calculate_empty_time_and_reserved_time(date:str):
    #3th item is flag by 0 or 1 that show this time is (0=NOT RESERVED or 1=RESERVED)
    #this section is getting times that Not reserved
    export_empty_list=[]
    export_reserved_list=[]
    merged_list =[]
    for i in range(1,3):
        duration_empty_time_as_slot_time=[]
        duration_empty_time_as_time=[]
        sorted_list_empty_time_as_array =[]
        parts = db_SetWork_Get_Part1_or_Part2_of_Day(date=date ,part=i)
        if parts in [False, None, 'False', 'None']:
            continue
        if parts[0] in [False, None, 'False', 'None']:
            continue
        start_time = datetime.strptime(str(parts[0]),'%H:%M:%S').strftime('%H:%M:%S')
        end_time = datetime.strptime(str(parts[1]),'%H:%M:%S').strftime('%H:%M:%S')
        time_obj = datetime.strptime(start_time, "%H:%M:%S")
        new_time_obj = time_obj + timedelta(minutes=15)
        start_time_with_add_15Min = new_time_obj.strftime("%H:%M:%S")
        start_time_with_add_15Min_and_seconds_00 = start_time_with_add_15Min[:7]+'0'
        list_empty_time_as_array=db_Reserve_Get_Date_And_parts_Not_Reserved(date=date , start_time=start_time , end_time=end_time)
        for i in range(len(list_empty_time_as_array)) : 
            sorted_list_empty_time_as_array.append(list_empty_time_as_array[i][2])
        duration_empty_time_as_slot_time=calculate_numbers_in_a_row(sorted_list_empty_time_as_array)
        for y in range(len(duration_empty_time_as_slot_time)):
            first_time=convert_slot_number_to_duration(start_time=start_time , slot_number=duration_empty_time_as_slot_time[y][0])
            second_time=convert_slot_number_to_duration(start_time=start_time_with_add_15Min_and_seconds_00 , slot_number=duration_empty_time_as_slot_time[y][1])
            duration_empty_time_as_time.append((first_time,second_time,'0'))
        export_empty_list.extend(duration_empty_time_as_time)
    #this section is getting times that reserved
    reserved_list = db_Reserve_Get_Reserve_Of_Date(date=date)
    for i in range(len(reserved_list)):
        start_time = datetime.strptime(str(reserved_list[i][3]),'%H:%M:%S').strftime('%H:%M:%S')
        end_time = datetime.strptime(str(reserved_list[i][4]),'%H:%M:%S').strftime('%H:%M:%S')
        export_reserved_list.append((start_time , end_time , '1'))
    merged_list.extend(export_empty_list)
    merged_list.extend(export_reserved_list)
    sorted_merged_list = sorted(merged_list, key=lambda x: x[0])
    return sorted_merged_list

######################3
def time_difference(time1: str, time2: str):
    # بررسی فرمت ورودی‌ها و انتخاب الگوی مناسب
    if len(time1) == 5:  # فرمت بدون ثانیه
        time_format = "%H:%M"
    else:  # فرمت با ثانیه
        time_format = "%H:%M:%S"
        
    # تبدیل رشته‌ها به آبجکت‌های datetime
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)
    
    # محاسبه اختلاف زمانی
    time_diff = abs(t2 - t1)
    return time_diff
