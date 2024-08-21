from datetime import datetime,timedelta
from database.db_reserve import *
from database.db_create_table import createTables

log_filename = f"./logs/output.log"
logging.basicConfig(filename=log_filename,
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("logging is running")
# createTables()
# id=insertReserve(1,'1403-03-03','13:00','14:00',100)
# result =updateDateOfReserve(1,'1403-03-11')
# result =updatePaymentOfReserve(1,2000)
result=DeleteReserve(2)
# result=reserveValidId(2)
# number=000
# print ( datetime.now().strftime('%Y-%m-%d '))

print  (result)