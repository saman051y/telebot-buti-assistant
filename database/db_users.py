import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
#######################################################################################
 # """reserve(id,user_id,date,start_time,end_time,payment)"""
 #todo : get all users
#######################################################################################
def insertNewUser(user_id : int,phone_number :str,username :str,join_date :str,name:str,last_name:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        sql=f"""INSERT INTO users (user_id,phone_number,username,join_date,name,last_name)
VALUES ({user_id}, '{phone_number}', '{username}' , '{join_date}' , '{name}' , '{last_name}');"""
        
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()# when something is created or updated or inserted;
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("can't insert new user")
    except Error as e :
        logging.error(f"in insertNewUser : {e}") 
        return False
#######################################################################################
def findUserById(user_id):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist = userValidId(user_id)
        if user_exist : 
            sql=f"""SELECT *
                    FROM users
                    WHERE user_id = {user_id};"""
            
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        user=cursor.fetchone()
                        cursor.close()
                        connection.close()
                        return user[0]
                else:
                    logging.error("can't find user")
        else :
                return False
    except Error as e :
        logging.error(f"in findUserById : {e}") 
        return False
#######################################################################################
def userValidId(user_id):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        sql=f"""SELECT user_id
                FROM users
                WHERE user_id = {user_id};"""
        
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     user=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     if user is None:
                        return False
                     else: 
                         return True
            else:
                logging.error("can't find user that exist or not !")
    except Error as e :
        logging.error(f"in existUser : {e}") 
        return False
 #######################################################################################
def getJoinDate(user_id):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= userValidId(user_id)
        if user_exist:
            sql=f"""SELECT join_date
                    FROM users
                    WHERE user_id = {user_id};"""
            
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        user=cursor.fetchone()
                        cursor.close()
                        connection.close()
                        return user[0]
                else:
                    logging.error("can't find user for getting join date")
        else: 
            return False
    except Error as e :
        logging.error(f"in getJoinDate : {e}") 
        return False
#######################################################################################
def updatePhone_Number(user_id:int, phone_number:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= userValidId(user_id)
        if user_exist:
            sql=f"""UPDATE users
                    SET phone_number = {phone_number}
                    WHERE user_id = {user_id};"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("can't Update Phone number")
        else: 
            return False
    except Error as e :
        logging.error(f"in updatePhone_Number : {e}") 
        return False
#######################################################################################
def updateName(user_id:int, name:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= userValidId(user_id)
        if user_exist:
            sql=f"""UPDATE users
                    SET name = '{name}'
                    WHERE user_id = {user_id};"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("can't update name")
        else: 
            return False
    except Error as e :
        logging.error(f"in updateName : {e}") 
        return False
#######################################################################################
def updateLast_Name(user_id:int, last_name:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= userValidId(user_id)
        if user_exist:
            sql=f"""UPDATE users
                    SET last_name = '{last_name}'
                    WHERE user_id = {user_id};"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("can't update last_name")
        else: 
            return False
    except Error as e :
        logging.error(f"in updateLast_Name : {e}") 
        return False
#######################################################################################
def updateUsername(user_id:int, username:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= userValidId(user_id)
        if user_exist:
            sql=f"""UPDATE users
                    SET username = '{username}'
                    WHERE user_id = {user_id};"""
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()# when something is created or updated or inserted;
                        cursor.close()
                        connection.close()
                        return True
                else:
                    logging.error("can't update username")
        else: 
            return False
    except Error as e :
        logging.error(f"in updateUsername : {e}") 
        return False
#######################################################################################
def getUser(user_id:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        sql=f"""SELECT *
                FROM users
                WHERE user_id = {user_id};"""
        
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     user=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     if user is None:
                        return False
                     else: 
                         return user
            else:
                logging.error("can't find user that exist or not !")
    except Error as e :
        logging.error(f"in getAllInfo : {e}") 
        return False