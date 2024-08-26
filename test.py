from datetime import datetime,timedelta
from database.db_reserve_service import *
from database.db_create_table import createTables
# result= None
log_filename = f"./logs/output.log"
logging.basicConfig(filename=log_filename,
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("logging is running")
# result =createTables()
# result=getIsActiveServices(1)
# result = DeleteService(1)
result = insertReserveService(reserve_id=2,service_id=2)
result =getResSerWithResId(2)
print  (result)