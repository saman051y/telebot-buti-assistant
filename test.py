from database.db_weeklysetting import db_WeeklySetting_Get_Value, db_WeeklySetting_Get_Value_one_day


result=db_WeeklySetting_Get_Value_one_day('saturday')
print(result)