


from datetime import datetime, timedelta
from database.db_reserve import db_Reserve_Get_Date_And_parts_Not_Reserved
from database.db_setwork import db_SetWork_Get_Part1_or_Part2_of_Day
from functions.time_date import GenerateNext7Day, convert_duration_to_slot_number, convert_slot_number_to_duration, find_consecutive_sequence

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
def get_free_time_for_next_7day(part:int , duration:str):
    """ input is part like 1 or 2 also duration like 01:00:00 and output is [(day , hour)] that user
         could reserve for next 7 day in one array"""
    days_list=[]
    days_list_can_reserve=[]
    array_all_time_slot_for_each_day=[]
    list_time_that_could_be_reserve =[]
    #convert duration to 15Min time slots (like 01:00:00 is 4)
    duration_as_time_slot = convert_duration_to_slot_number(duration)
    #generate all day bu default value from weekly setting
    GenerateNext7Day()
    #get all day that user could reserve 
    for i in range(7):
        today = datetime.now().date()
        date = today + timedelta(days=i)
        parts_of_Day = db_SetWork_Get_Part1_or_Part2_of_Day(date=date , part=part)
        if parts_of_Day : 
            days_list.append((date, parts_of_Day[0], parts_of_Day[1]))
    #search empty time by duration in each day that user could reserve 
    for i in range(len(days_list)):
        date=str(days_list[i][0])
        start_time = datetime.strptime(str(days_list[i][1]),'%H:%M:%S').strftime('%H:%M:%S')
        end_time = datetime.strptime(str(days_list[i][2]),'%H:%M:%S').strftime('%H:%M:%S')
        # get all empty time by tim_slot=15 Min
        list_time_that_could_be_reserve  = db_Reserve_Get_Date_And_parts_Not_Reserved(date=date ,start_time=start_time, end_time=end_time)
        for i in range(len(list_time_that_could_be_reserve)) :
            array_all_time_slot_for_each_day.append(list_time_that_could_be_reserve[i][2])
        #get first time that able to be reserved as time slot
        reserved_time_as_time_slot=find_consecutive_sequence(array_all_time_slot_for_each_day ,duration_as_time_slot)
        #convert time slot to time like time slot 2 of 8:00:00 is 08:30:00 (2th 15 Min of 08:00)
        time_could_be_reserve = convert_slot_number_to_duration(start_time , reserved_time_as_time_slot )
        days_list_can_reserve.append((date , time_could_be_reserve))
    if days_list_can_reserve == [] :
        return False 
    return(days_list_can_reserve)
