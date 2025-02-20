import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
from database.db_weeklysetting import *
######################################################################################################
"""(date,part1_start_time,part1_end_time,part2_start_time,part2_end_time)"""
######################################################################################################
########################################################################################! Insert Section
def db_SetWork_Create_date(date: str, part1_start_time: str, part1_end_time: str, part2_start_time: str, part2_end_time: str):
    """(date, part1_start_time, part1_end_time, part2_start_time, part2_end_time)"""
    try:
        date_exist=db_SetWork_exist_date(date=date)
        if not date_exist:
            
            sql=f"""INSERT INTO setwork (date, part1_start_time, part1_end_time, part2_start_time, part2_end_time)
                    VALUES ('{date}','{part1_start_time}','{part1_end_time}','{part2_start_time}','{part2_end_time}');"""
            
            if part2_start_time  == 'Null' :
                sql=f"""INSERT INTO setwork (date, part1_start_time, part1_end_time)
                    VALUES ('{date}','{part1_start_time}','{part1_end_time}');"""

            if part1_start_time == 'Null' :
                sql=f"""INSERT INTO setwork (date, part2_start_time, part2_end_time)
                    VALUES ('{date}','{part2_start_time}','{part2_end_time}');"""
                
            if part2_start_time == 'Null' and part1_start_time == 'Null' :
                sql=f"""INSERT INTO setwork (date)
                    VALUES ('{date}');"""
                
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                         cursor.execute(sql)
                         connection.commit()# when something is created or updated or inserted;
                         cursor.close()
                         connection.close()
                         return True
                else:
                    logging.error("Error in db_Setwork_Insert_New_date")
        else:
            return False
    except Error as e :
        logging.error(f"Error in db_Setwork_Insert_New_date : {e}") 
        return False
######################################################################################################

#######################################################################################! Get Section
###################################### get all set work date al time
def db_SetWork_Get_ALL_Days():
    try:
        sql = f"""SELECT * FROM setwork;"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     setTime=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     if setTime is None:
                        return None
                     return setTime
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" db_Setwork_Get_ALL_Days: {e}") 
###################################### get parts of a day
def db_SetWork_Get_One_Day(date:str):
    """request a day and get all parts of a day"""
    try:
        date_exist=db_SetWork_exist_date(date=date)
        if not date_exist:  
            return False 
        sql=f"""SELECT *
                FROM setwork
                WHERE date = '{date}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    setwork=cursor.fetchone()
                    cursor.close()
                    connection.close()
                    return setwork
            else:
                logging.error("Error in db_Setwrk_Get_Day")
    except Error as e :
        logging.error(f"Error in db_Setwrk_Get_Day : {e}") 
        return False
######################################  get one part of a day
def db_SetWork_Get_Part1_or_Part2_of_Day(date:str, part:int):
    """if (2024-04-05 , 2): you'll get part 2 as array"""
    try:
        date_exist=db_SetWork_exist_date(date=date)
        if date_exist:   
            sql=f"""SELECT part{part}_start_time , part{part}_end_time 
                    FROM setwork
                    WHERE date = '{date}';"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        setwork=cursor.fetchone()
                        cursor.close()
                        connection.close()
                        return setwork
                else:
                    logging.error("Error in db_Setwork_Get_Day")
        else: 
            return False
    except Error as e :
        logging.error(f"Error in db_Setwork_Get_Day : {e}") 
        return False
    ######################################  get one part of a month
def db_SetWork_Get_Part1_or_Part2_of_Day_for_1Month(data , date_range):
    """ """
    try:
        sql = f"""
        SELECT date, part1_start_time, part1_end_time, part2_start_time, part2_end_time
        FROM setwork
        WHERE date IN ({data});
        """

        with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor(dictionary=True) as cursor:
                        cursor.execute(sql, date_range)
                        results = cursor.fetchall()
                        return results
                else:
                    logging.error("Error in db_SetWork_Get_Part1_or_Part2_of_Day_for_1Month")
    except Error as e :
        logging.error(f"Error in db_SetWork_Get_Part1_or_Part2_of_Day_for_1Month : {e}") 
        return False
######################################  is day exist or not ?
def db_SetWork_exist_date(date:str):
    """request a day to know if exist"""
    try:
            sql=f"""SELECT date
                    FROM setwork
                    WHERE date = '{date}';"""
            
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        setwork=cursor.fetchone()
                        cursor.close()
                        connection.close()
                        if setwork is None:
                            return False
                        else: 
                            return setwork
                else:
                    logging.error("Error in db_Setwork_Get_Day")
    except Error as e :
        logging.error(f"Error in db_Setwork_Get_Day : {e}") 
        return False
    
#######################################################################################!update section
###################################### update all part ofday with date
def db_Setwork_Update_All_Part_Of_Day(date: str, part1_start_time: str, part1_end_time: str, part2_start_time: str, part2_end_time: str):
    """update a day with all part"""
    try:
        date_exist=db_SetWork_exist_date(date)
        if date_exist:  
            sql=f"""UPDATE setwork
                    SET part1_start_time = '{part1_start_time}', 
                        part1_end_time = '{part1_end_time}', 
                        part2_start_time = '{part2_start_time}', 
                        part2_end_time = '{part2_end_time}'
                    WHERE date = '{date}';"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("Error in db_Setwork_Update_All_Part_Of_Day")
        else:
            return False
    except Error as e :
        logging.error(f"Error in db_Setwork_Update_All_Part_Of_Day : {e}") 
        return False
###################################### update just one part of a day    
def db_SetWork_Update_One_Part_Of_Day(date: str, part: int, start_time: str, end_time: str):
    """get date and number of part to update also get start_time  end_time to update one part of date """
    try:
        date_exist=db_SetWork_exist_date(date)
        if date_exist:  
            sql=f"""UPDATE setwork
                    SET part{part}_start_time = '{start_time}', 
                        part{part}_end_time = '{end_time}'
                    WHERE date = '{date}';"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("Error in db_Setwork_Update_One_Part_Of_Day")
        else:
            return False
    except Error as e :
        logging.error(f"Error in db_Setwork_Update_One_Part_Of_Day : {e}") 
        return False
#######################################################################################! Delete Section
###################################### delete compeletly a dey
def db_Setwork_Delete_date(date: str):
    """delete a day with parts"""
    try:
        date_exist=db_SetWork_exist_date(date=date)
        if date_exist:
            sql=f"""DELETE FROM setwork 
                    WHERE date = '{date}';"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                         cursor.execute(sql)
                         connection.commit()# when something is created or updated or inserted;
                         cursor.close()
                         connection.close()
                         return True
                else:
                    logging.error("Error in db_Setwork_Delete_date")
        else:
            return False
    except Error as e :
        logging.error(f"Error in db_Setwork_Delete_date : {e}") 
        return False
###################################### set free one part a day  
def db_SetWork_Delete_One_Part(date:str, part:int):
    """delete a day with parts"""
    try:
        date_exist=db_SetWork_exist_date(date=date)
        if date_exist:
            sql=f"""UPDATE setwork
                        SET part{part}_start_time = NULL, 
                            part{part}_end_time = NULL
                        WHERE date = '{date}';"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                         cursor.execute(sql)
                         connection.commit()# when something is created or updated or inserted;
                         cursor.close()
                         connection.close()
                         return True
                else:
                    logging.error("Error in db_Setwork_Delete_date")
        else:
            return False
    except Error as e :
        logging.error(f"Error in db_Setwork_Delete_date : {e}") 
        return False
#######################################################################################! finish
