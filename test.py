from database.db_admin_list import *
from database.db_bot_setting import *
from database.db_reserve import *
from database.db_users import *
from database.db_service import *
from database.db_setwork import *
from database.db_weeklysetting import *
from functions.custom_functions import *
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
from functions.time_date import *
##############################################################################
result=get_free_time_for_next_7day(duration="0:45:00")
print(result) 
#skjdghkjdfg