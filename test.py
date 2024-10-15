from database.db_bot_setting import db_bot_setting_get_value_by_name
from database.db_reserve import *
from database.db_users import *
from database.db_service import *
from database.db_setwork import *
from database.db_weeklysetting import *
from functions.custom_functions import get_free_time_for_next_7day
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
from functions.time_date import *
##############################################################################
# list =[]
# for i in range(len(result)) : 
#      list.append(result[i][2])
# print(list)

# result =get_free_time_for_next_7day(part=1,duration="01:00:00")
# print( result)
result =get_free_time_for_next_7day(duration="01:00:00")
print(result)




# def get_free_time_for_next_7day(duration:str):
#     """ input is part like 1 or 2 also duration like 01:00:00 and output is [(day , hour)] that user
#          could reserve for next 7 day in one array"""
#     days_list=[]
#     days_list_can_reserve=[]
#     for i in range(1,3):
#         part=i
#         #convert duration to 15Min time slots (like 01:00:00 is 4)
#         duration_as_time_slot = 
# convert_duration_to_slot_number(duration)
#         #generate all day bu default value from weekly setting
#         GenerateNext7Day()
#         #get all day that user could reserve 
#         for i in range(7): 
#             array_all_time_slot_for_each_day=[]
#             list_time_that_could_be_reserve =[]
#             today = datetime.now().date()
#             date = today + timedelta(days=i)
#             parts_of_Day = db_SetWork_Get_Part1_or_Part2_of_Day(date=date , part=part)
#             if parts_of_Day : 
#                 days_list.append((date, parts_of_Day[0], parts_of_Day[1]))
#         #search empty time by duration in each day that user could reserve 
#         for i in range(len(days_list)):
#             date=str(days_list[i][0])
#             start_time = datetime.strptime(str(days_list[i][1]),'%H:%M:%S').strftime('%H:%M:%S')
#             end_time = datetime.strptime(str(days_list[i][2]),'%H:%M:%S').strftime('%H:%M:%S')
#             # get all empty time by tim_slot=15 Min
#             list_time_that_could_be_reserve  = db_Reserve_Get_Date_And_parts_Not_Reserved(date=date ,start_time=start_time, end_time=end_time)
#             for i in range(len(list_time_that_could_be_reserve)) :
#                 array_all_time_slot_for_each_day.append(list_time_that_could_be_reserve[i][2])
#             #get first time that able to be reserved as time slot
#             reserved_time_as_time_slot=find_consecutive_sequence(array_all_time_slot_for_each_day ,duration_as_time_slot)
#             print(f'reserved_time_as_time_slot{reserved_time_as_time_slot}')
#             print(type(reserved_time_as_time_slot))
#             #convert time slot to time like time slot 2 of 8:00:00 is 08:30:00 (2th 15 Min of 08:00)
#             time_could_be_reserve = convert_slot_number_to_duration(start_time , reserved_time_as_time_slot )
#             days_list_can_reserve.append((date ,part, time_could_be_reserve))
#     if days_list_can_reserve == [] :
#         return False 
#     return(days_list_can_reserve)