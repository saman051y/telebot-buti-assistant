import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
######################################################################################################
"""input: name:varchar(20), value:varchar(20) """
######################################################################################################
def db_WeeklySetting_Insert(name: str, value: str):
    """Insert a new weekly setting with name and value."""
    try:
        sql = f"""INSERT INTO weekly_setting (name, value) VALUES ('{name}', '{value}');"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()  # Commit the transaction
                    cursor.close()
                    connection.close()
                    logging.info(f"Inserted {name}: {value} into weekly_setting.")
                    return True
            else:
                logging.error("Connection to database is not working")
                return False
    except Error as e:
        logging.error(f"db_WeeklySetting_Insert_Value: {e}")
        return False

######################################################################################################
def db_WeeklySetting_Update(name:str, value:str):
    """weekly setting(name:varchar(20), value:varchar(20)  and it will be updated"""
    try:
        sql=f"""UPDATE weekly_setting
                SET value = '{value}'
                WHERE name = '{name}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    connection.commit()# when something is created or updated or inserted;
                    cursor.close()
                    connection.close()
                    return True
            else:
                logging.error("connection to database is not working")
    except Error as e :
        logging.error(f"Error in db_WeeklySetting_Update : {e}") 
        return False
######################################################################################################
def db_WeeklySetting_Get_Value(name:str):
    """input name:str , output is value """
    try:
        sql = f"""SELECT * FROM weekly_setting WHERE name='{name}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     result=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return result
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" db_WeeklySetting_Get_Value: {e}") 
######################################################################################################
def db_WeeklySetting_Get_All():
    """get all data"""
    try:
        sql=f"""SELECT * FROM weekly_setting"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    result=cursor.fetchall()
                    cursor.close()
                    connection.close()
                    if result:
                        return result
                    else:
                        return None
            else:
                logging.error("connection to database is not working")
    except Error as e :
        logging.error(f"Error in db_WeeklySetting_Get_All : {e}") 
        return False
######################################################################################################
def db_WeeklySetting_Get_Parts():
    """get all parts"""
    try:
        sql=f"""SELECT name, value 
                FROM weekly_setting 
                WHERE name IN ('part1', 'part2');"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    result=cursor.fetchall()
                    cursor.close()
                    connection.close()
                    return result
            else:
                logging.error("connection to database is not working")
    except Error as e :
        logging.error(f"Error in db_WeeklySetting_Get_Parts : {e}") 
        return False