from database.db_reserve import *
from database.db_users import *
from database.db_service import *
from database.db_setwork import *
from database.db_weeklysetting import *
from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
##############################################################################

markup_generate_parts_of_days_for_reservation_by_needed_time(1 , '01:15:00')

'compelet auto generate days and calculate day with time to reseve for user by duration of needed services and part ' 