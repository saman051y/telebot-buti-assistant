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
result=db_bot_setting_get_value_by_name(name="main_admin")
print(result)