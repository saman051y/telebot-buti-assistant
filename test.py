from database.db_reserve import *
from database.db_users import *
from database.db_service import *
from database.db_setwork import *
from database.db_weeklysetting import *
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
date = '2024-05-06'
date_str = '2024-5-06'
text = 'ok'
if date != date_str :
    text='not'

print( text)