import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
#######################################################################################
########################################################################################! Insert Sectin
def db_Users_Insert_New_User(user_id : int,phone_number :str,username :str,join_date :str,name:str,last_name:str):
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
                logging.error("Error in db_Users_Insert_New_User")
    except Error as e :
        logging.error(f"Error in db_Users_Insert_New_User : {e}") 
        return False
#######################################################################################
########################################################################################! Find Sectin
def db_Users_Find_User_By_Id(user_id):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist = db_Users_Validation_User_By_Id(user_id)
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
                        return user
                else:
                    logging.error("Error in db_Users_Find_User_By_Id")
        else :
                return False
    except Error as e :
        logging.error(f"Error in db_Users_Find_User_By_Id : {e}") 
        return False
#######################################################################################
def db_Users_Validation_User_By_Id(user_id):
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
                logging.error("Error in db_Users_Validation_User_By_Id")
    except Error as e :
        logging.error(f"Error in db_Users_Validation_User_By_Id : {e}") 
        return False
#######################################################################################
########################################################################################!Get Section
def db_Users_Get_Join_Date(user_id):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= db_Users_Validation_User_By_Id(user_id)
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
                    logging.error("Error in db_Users_Get_Join_Date")
        else: 
            return False
    except Error as e :
        logging.error(f"Error in db_Users_Get_Join_Date : {e}") 
        return False
#######################################################################################
def db_Users_Get_Name_User(user_id:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        sql=f"""SELECT name
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
                         return user[0]
            else:
                logging.error("Error in db_Users_Get_Name_User")
    except Error as e :
        logging.error(f"Error in db_Users_Get_Name_User : {e}") 
        return False
#######################################################################################
def db_Users_Get_Last_Name_User(user_id:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
            sql=f"""SELECT last_name
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
                            return user[0]
                else:
                    logging.error("Error in db_Users_Get_Last_Name_User")
    except Error as e :
        logging.error(f"Error in db_Users_Get_Last_Name_User : {e}") 
        return False
#######################################################################################
def db_Users_Get_Phone_Number_User(user_id:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
            sql=f"""SELECT phone_number
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
                            return user[0]
                else:
                    logging.error("Error in db_Users_Get_Username_User")
    except Error as e :
        logging.error(f"Error in db_Users_Get_Username_User : {e}") 
        return False
#######################################################################################   
def db_Users_Get_Phone_Number_User(user_id:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
            sql=f"""SELECT phone_number
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
                            return user[0]
                else:
                    logging.error("Error in db_Users_Get_Phone_Number_User")
    except Error as e :
        logging.error(f"Error in db_Users_Get_Phone_Number_User : {e}") 
        return False
#######################################################################################
def db_Users_Get_All_Users():
    try:
        sql = f"""SELECT * FROM users ;"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     users=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     if users is None:
                        logging.error("service name not fund")
                        return None
                     return users
                       
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" db_Users_Get_All_Users: {e}") 
#######################################################################################   
def db_Users_Get_Username_user(user_id:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
            sql=f"""SELECT username
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
                            return user[0]
                else:
                    logging.error("Error in db_Users_Get_Username_user")
    except Error as e :
        logging.error(f"Error in db_Users_Get_Username_user : {e}") 
        return False
########################################################################################!Update Section
def db_Users_Update_Name_User(user_id:int, name:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= db_Users_Validation_User_By_Id(user_id)
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
                    logging.error("Error in db_Users_Update_Name_User")
        else: 
            return False
    except Error as e :
        logging.error(f"Error in db_Users_Update_Name_User : {e}") 
        return False
#######################################################################################
def db_Users_Update_Last_Name_User(user_id:int, last_name:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= db_Users_Validation_User_By_Id(user_id)
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
                    logging.error("Error in db_Users_Update_Last_Name_User")
        else: 
            return False
    except Error as e :
        logging.error(f"Error in db_Users_Update_Last_Name_User : {e}") 
        return False
#######################################################################################
def db_Users_Update_Username_User(user_id:int, username:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= db_Users_Validation_User_By_Id(user_id)
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
                    logging.error("Error in db_Users_Update_Username_User")
        else: 
            return False
    except Error as e :
        logging.error(f"Error in db_Users_Update_Username_User : {e}") 
        return False
#######################################################################################
def db_Users_Update_Phone_Number_User(user_id:int, phone_number:str):
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        user_exist= db_Users_Validation_User_By_Id(user_id)
        if user_exist:
            sql=f"""UPDATE users
                    SET phone_number = '{phone_number}'
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
                    logging.error("Error in db_Users_Update_Phone_Number_User")
        else: 
            return False
    except Error as e :
        logging.error(f"Error in db_Users_Update_Phone_Number_User : {e}") 
        return False
#######################################################################################
