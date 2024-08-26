import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
######################################################################################################
"""each hour save as  4 part like 0200 => {0 = not working, 1 = working ,2 = full} for each bit
      0000 : {0 to 15 min ,15 to 30 min,30 min to 45,45 to 60}
"""
######################################################################################################
def insertTiming(record_date: str , hour_00 :str  , hour_01 :str  , hour_02 :str  , hour_03 :str  ,
                  hour_04 :str  , hour_05 :str  , hour_06 :str  , hour_07 :str  , hour_08 :str  , hour_09 :str  ,
                    hour_10 :str  , hour_11 :str  , hour_12 :str  , hour_13 :str  , hour_14 :str  ,
                      hour_15 :str  , hour_16 :str  , hour_17 :str  , hour_18 :str  , hour_19 :str  ,
                        hour_20 :str  , hour_21 :str  , hour_22 :str, hour_23 :str):
    """each hour save as  4 part like 0200 => {0 = not working, 1 = working ,2 = full} for each bit
      0000 : {0 to 15 min ,15 to 30 min,30 min to 45,45 to 60}
    """ 
    try:
        
        sql=f"""INSERT INTO timing (record_date,hour_00,hour_01,hour_02,hour_03,hour_04,hour_05,hour_06,hour_07,
        hour_08,hour_09,hour_10,hour_11,hour_12,hour_13,hour_14,hour_15,hour_16,
        hour_17,hour_18,hour_19,hour_20,hour_21,hour_22,hour_23)
VALUES ('{record_date}', '{hour_00}', '{hour_01}' , '{hour_02}' , '{hour_03}' , '{hour_04}', '{hour_05}', '{hour_06}', '{hour_07}',
 '{hour_08}', '{hour_09}', '{hour_10}', '{hour_11}', '{hour_12}', '{hour_13}', '{hour_14}', '{hour_15}', '{hour_16}', 
 '{hour_17}', '{hour_18}', '{hour_19}','{hour_20}','{hour_21}','{hour_22}','{hour_23}');"""
        
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()# when something is created or updated or inserted;
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("can't insert new Timing")
    except Error as e :
        logging.error(f"in insertTiming : {e}") 
        return False
    ######################################################################################################
def updateTime(record_date:str, hour:str , value:str):
    """ hour should be like {01}  & value should be like 0100"""
    try:
            sql=f"""UPDATE timing
                    SET hour_{hour} = '{value}'
                    WHERE record_date = '{record_date}';"""
            
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("can't update hour")
    except Error as e :
        logging.error(f"in updateTime : {e}") 
        return False
 ######################################################################################################               
def getDate(record_date:str):
    """value should be like 2023-02-07"""
    try:
        sql=f"""SELECT *
                FROM timing
                WHERE record_date = '{record_date}';"""
        
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     date=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     if date is None:
                        return False
                     else: 
                         return date
            else:
                logging.error("can't get a date")
    except Error as e :
        logging.error(f"in getDate : {e}") 
        return False       
######################################################################################################
def getTime(record_date:str , hour:str):
    """hour should be like {04}"""
    try:
        sql=f"""SELECT hour_{hour}
                FROM timing
                WHERE record_date = '{record_date}';"""
        
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     date=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     if date is None:
                        return False
                     else: 
                         return date[0]
            else:
                logging.error("can't get time of a day")
    except Error as e :
        logging.error(f"in getTime : {e}") 
        return False     
######################################################################################################