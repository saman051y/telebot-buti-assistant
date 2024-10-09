from datetime import datetime, timedelta
from convertdate import persian
import math
from database.db_setwork import *
from database.db_weeklysetting import *
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
def gregorian_to_jalali(gregorian_date_str):
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
    
    return jalali_date_str
#########################################################
def add_time(initial_time: str, duration: str) -> str:
    """
    Add a duration to a given time.

    Parameters:
    - initial_time (str): The initial time in "HH:MM" format.
    - duration (str): The duration to add in "HH:MM" format.

    Returns:
    - str: The new time in "HH:MM" format after adding the duration.
    """
    # Define the time format
    time_format = "%H:%M"
    
    # Convert the initial time string to a datetime object
    time_obj = datetime.strptime(initial_time, time_format)
    
    # Parse the duration string to extract hours and minutes
    hours, minutes = map(int, duration.split(":"))
    
    # Create a timedelta object for the duration
    time_delta = timedelta(hours=hours, minutes=minutes)
    
    # Add the timedelta to the initial time
    new_time = time_obj + time_delta
    
    # Format the new time as a string
    new_time_str = new_time.strftime(time_format)
    
    return new_time_str

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
def compare_time(lower,than):
    """return true if time1 < time2"""
    time_format = "%H:%M"
    time_A = datetime.strptime(lower, time_format).time()
    time_B = datetime.strptime(than, time_format).time()
    if time_A<time_B :
        return True
    else:
        return False
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
def cal_day(days):
    """get a number and return it day like
    1 => دوشنبه
    0 => یکشنبه"""
    tomorrow_date = datetime.now() + timedelta(days=days)
    tomorrow_weekday = tomorrow_date.weekday()
    tomorrow_persian = days_of_week_name[tomorrow_weekday]
    return tomorrow_persian

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
    text = f'{jalali_day_name} {jalali_day_number} {jalali_month} {jalali_Year}'
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
    print(default_parts)
    for i in range(0,6):
        date = today + timedelta(days=i)
        day_of_week=convertDateToDayAsGregorianCalendar(date=str(date))
        day_status=db_WeeklySetting_Get_Value(day_of_week)
        result=False
        if day_status[2] == '1':
            # exist_day = db_SetWork_exist_date(str(date))
            # if not exist_day:
            result = test_insert(date ,default_parts[0], default_parts[1], default_parts[2] , default_parts[3])
        print(f'{i} : {result} ' )
########################################################## calculate slot_number from start_time
def Get_Nth_Time_Slot(start_time_str,slot_number):
    """input is time like 08:30:00 and slot_number like 3 
        and export is 3th 15Min then export si 09:00:00"""
     # Parse the start time into a datetime object including seconds
    time_format = "%H:%M:%S"
    start_time = datetime.strptime(start_time_str, time_format)
    
    # Calculate the total minutes to add for the given slot number
    total_minutes_to_add = 15 * (slot_number - 1)  # Subtract 1 because the first slot is at the start time
    
    # Add the minutes to the start time
    new_time = start_time + timedelta(minutes=total_minutes_to_add)
    
    # Return the time in 'HH:MM:SS' format
    return new_time.strftime(time_format)
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
##########################################################