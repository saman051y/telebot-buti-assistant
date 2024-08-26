from database.db_users import *
from database.db_timing import *
from database.db_create_table import *


#print(existUser(8585))
#print(getJoinDate(8585))
#updateLast_Name(8585 , 'Yaghoubi')
#print(insertNewUser(8585 , '09033883130' , 'Ho3ien' , '2024-03-04' , 'ho3ein' , 'nasiri'))print
#createTables()
#print(insertTiming('2024-08-26','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'))
#updateTime('2024-08-26', '00' , '1')
print(getTime('2024-08-27' , '04'))

log_filename = f"./logs/output_{('%Y-%m-%d_%H-%M-%S')}.log"
logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("logging is running")