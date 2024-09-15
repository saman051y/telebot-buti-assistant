from database.db_functions import convert_time_to_slot
from database.db_users import *
from database.db_service import *
from functions.time_date import convert_time_slot_to_time
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *

#db_Users_Update_Name_User(423977498 , 'empty')
#db_Users_Update_Last_Name_User(423977498 , 'empty')
#db_Users_Update_Phone_Number_User(423977498 , 'empty') 
#print(' OK ')
#print(db_Service_Get_Service_With_Name('name'))
#print(db_Users_Get_All_Users())
# print(change_Username_To_URL('Ho3einNa3iri','09033883130'))
result = convert_time_slot_to_time(700)
print (result)