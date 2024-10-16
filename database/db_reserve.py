 #       """reserve(id,user_id,date,start_time,end_time,approved,payment)"""
from datetime import datetime, timedelta
import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
##################################################
##################################################! insert section
def db_Reserve_insert_Reserve(user_id:int ,date:str,start_time:str,end_time:str,payment:int):
    """return reserve_id"""
    try:
        sql =f"""INSERT INTO reserve (user_id,date,start_time,end_time,payment) 
        VALUES ({user_id},'{date}','{start_time}','{end_time}',{payment});"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     reserve_id = cursor.lastrowid
                     connection.commit()# when something is created or updated or inserted;
                     cursor.close()
                     connection.close()
                     return int(reserve_id)
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"insertReserve : {e}")
        return False
##################################################
##################################################! get section
def db_Reserve_Get_Reserve_With_Id(reserve_id :int):
    valid_id=db_Reserve_Reserve_Valid_Id(reserve_id=reserve_id)
    if not valid_id:
        logging.error("getReserveWithId: id is not valid")
        return False
    try:
        sql =f"""SELECT * FROM reserve WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     reserve=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return reserve
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"getReserveWithId : {e}")
##################################################
def db_Reserve_Get_Reserve_Of_Date(date:str):
    try:
        sql = f"""SELECT * FROM reserve 
                  WHERE date = '{date}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     reserves=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     return reserves
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"getReserveOfDate : {e}")
##################################################     
def db_Reserve_Get_Date_And_parts_Not_Reserved(date:str , start_time:str , end_time:str):
    """input is date for search from start_time to end_time to find first duration and output is list of"""
    try:
        #Subtract 1Min from end_time for db
        

        start_time_with_00_seconds=start_time[:7] +f'0'
        sql = f""" 
                WITH RECURSIVE time_slots AS (
                    -- Generate 15-min time slots starting from 9:00 AM (300 minutes = 20 slots)
                    SELECT '{start_time}' AS slot_start_time,
                           ADDTIME('{start_time_with_00_seconds}', '00:15:00') AS slot_end_time
                    UNION ALL
                    SELECT ADDTIME(slot_start_time, '00:15:00') AS slot_start_time,
                           ADDTIME(slot_end_time, '00:15:00') AS slot_end_time
                    FROM time_slots
                    WHERE slot_end_time < '{end_time}' -- Stop before 2:00 PM (to include 1:45 PM - 2:00 PM slot)
                ),
                numeric_time_slots AS (
                  SELECT 
                    ROW_NUMBER() OVER (ORDER BY slot_start_time) AS SlotNumber,
                    slot_start_time, slot_end_time
                  FROM time_slots  
                ),
                reserved_slots AS (
                    SELECT start_time, end_time
                    FROM reserve
                    WHERE date = '{date}'
                )
                -- Fetch time slots that are not reserved
                SELECT slot_start_time, slot_end_time ,SlotNumber-1
                FROM numeric_time_slots t
                LEFT JOIN reserved_slots r
                    ON t.slot_start_time BETWEEN r.start_time AND r.end_time
                    OR t.slot_end_time BETWEEN r.start_time AND r.end_time
                    OR (r.start_time <= t.slot_start_time AND r.end_time >= t.slot_end_time)
                WHERE r.start_time IS NULL;
                """
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    reserves=cursor.fetchall()
                    cursor.close()
                    connection.close()
                    return reserves
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"getReserveOfDate : {e}")

##################################################
def db_reserve_get_info_reserve_by_date_and_start_time(date: str, start_time: str):
    """Return user_id who reserved a specific date and start time."""
    try:
        sql = f"""SELECT user_id FROM reserve 
                  WHERE date = '{date}' AND start_time = '{start_time}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchone()  # Fetch the first matching record
                    cursor.close()
                    connection.close()
                    if result:
                        return int(result[0])  # Return user_id
                    else:
                        return None  # No matching reservation found
            else:
                logging.error("Connection to the database is not working.")
                return False
    except Error as e:
        logging.error(f"db_get_user_by_reservation: {e}")
        return False
##################################################
def db_reserve_get_info_reserve_by_date_and_start_time(date: str, start_time: str):
    """Return id who reserved a specific date and start time."""
    try:
        sql = f"""SELECT * FROM reserve 
                  WHERE date = '{date}' AND start_time = '{start_time}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchone()  # Fetch the first matching record
                    cursor.close()
                    connection.close()
                    if result:
                        return result  # Return user_id
                    else:
                        return None  # No matching reservation found
            else:
                logging.error("Connection to the database is not working.")
                return False
    except Error as e:
        logging.error(f"db_get_user_by_reservation: {e}")
        return False
# ##################################################! update section   
def db_Reserve_Update_Date_Of_Reserve(reserve_id:int,new_date:str):
    valid_id=db_Reserve_Reserve_Valid_Id(reserve_id=reserve_id)
    if not valid_id:
        logging.error("updateDateOfReserve: id is not valid")
        return False
    try:
        sql = f"""UPDATE reserve 
                  SET date = '{new_date}' 
                  WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"updateDateOfReserve : {e}")
##################################################
def db_Reserve_Update_Time_Of_Reserve(reserve_id:int,new_start_time:str,new_end_time:str):
    valid_id=db_Reserve_Reserve_Valid_Id(reserve_id=reserve_id)
    if not valid_id:
        logging.error("updateTimeOfReserve: id is not valid")
        return False
    try:
        sql = f"""UPDATE reserve 
                  SET start_time = '{new_start_time}' ,  end_time='{new_end_time}'
                  WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"updateTimeOfReserve : {e}")
##################################################
def db_Reserve_Update_Payment_Of_Reserve(reserve_id:int,new_payment:int):
    valid_id=db_Reserve_Reserve_Valid_Id(reserve_id=reserve_id)
    if not valid_id:
        logging.error("updatePaymentOfReserve: id is not valid")
        return False
    try:
        sql = f"""UPDATE reserve 
                  SET payment = '{new_payment}' 
                  WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"updatePaymentOfReserve : {e}")
##################################################
def db_Reserve_Update_Approved_Of_Reserve(reserve_id:int,approved:bool):
    valid_id=db_Reserve_Reserve_Valid_Id(reserve_id=reserve_id)
    if not valid_id:
        logging.error("updateApprovedOfReserve: id is not valid")
        return False
    try:
        if approved:
            sql = f"""UPDATE reserve 
                    SET approved = 1 
                    WHERE id = {reserve_id};"""
        else:
            sql= f"""UPDATE reserve 
                    SET approved = 0
                    WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"updateApprovedOfReserve : {e}")
##################################################
##################################################! delete section
##################################################
def db_Reserve_Delete_Reserve(reserve_id:int):
    valid_id=db_Reserve_Reserve_Valid_Id(reserve_id=reserve_id)
    if not valid_id:
        logging.error("DeleteReserve: id is not valid")
        return False
    try:
        sql = f"""DELETE FROM reserve 
                WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return True
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"DeleteReserve : {e}")
##################################################
def get_reserves_for_user(user_id, days):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor(dictionary=True) as cursor:
                    today = datetime.now().date()
                    end_date = today + timedelta(days=days)
                    
                    sql_query = f"""
                    SELECT * FROM reserve 
                    WHERE user_id = {user_id} 
                    AND date >= '{today}' 
                    AND date <= '{end_date}';
                    """
                    
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    return results
    except mysql.connector.Error as e:
        logging.error(f"Error fetching reserves for user: {e}")
        return None
##################################################
def get_reserves_for_admin(days):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor(dictionary=True) as cursor:
                    today = datetime.now().date()
                    end_date = today + timedelta(days=days)
                    
                    sql_query = f"""
                    SELECT * FROM reserve 
                    WHERE date >= '{today}' 
                    AND date <= '{end_date}';
                    """
                    
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    return results
    except mysql.connector.Error as e:
        logging.error(f"Error fetching reserves for user: {e}")
        return None
##################################################
##################################################! check section
def db_Reserve_Reserve_Valid_Id(reserve_id:int):
    try:
        sql = f"""SELECT COUNT(*) 
                  FROM reserve 
                  WHERE id = {reserve_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchone()  # Fetch the count result
                    
                    cursor.close()
                    connection.close()
                    return result[0] > 0  # Return True if count > 0, else False
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"reserveValidId : {e}")
        return False
##################################################