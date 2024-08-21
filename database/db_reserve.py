 #       """reserve(id,user_id,date,start_time,end_time,approved,payment)"""

import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from auth.auth import DB_CONFIG
##################################################
def insertReserve(user_id:int ,date:str,start_time:str,end_time:str,payment:int):
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
def getReserveWithId(reserve_id :int):
    valid_id=reserveValidId(reserve_id=reserve_id)
    if not valid_id:
        logging.error("DeleteReserve: id is not valid")
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
def updateDateOfReserve(reserve_id:int,new_date:str):
    valid_id=reserveValidId(reserve_id=reserve_id)
    if not valid_id:
        logging.error("DeleteReserve: id is not valid")
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
def updateTimeOfReserve(reserve_id:int,new_start_time:str,new_end_time:str):
    valid_id=reserveValidId(reserve_id=reserve_id)
    if not valid_id:
        logging.error("DeleteReserve: id is not valid")
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
def updatePaymentOfReserve(reserve_id:int,new_payment:int):
    valid_id=reserveValidId(reserve_id=reserve_id)
    if not valid_id:
        logging.error("DeleteReserve: id is not valid")
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
def updateApprovedOfReserve(reserve_id:int,approved:bool):
    valid_id=reserveValidId(reserve_id=reserve_id)
    if not valid_id:
        logging.error("DeleteReserve: id is not valid")
        return False
    try:
        sql = f"""UPDATE reserve 
                  SET approved = '{approved}' 
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
def getReserveOfDate(date:str):

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
def DeleteReserve(reserve_id:int):
    valid_id=reserveValidId(reserve_id=reserve_id)
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
def reserveValidId(reserve_id:int):
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