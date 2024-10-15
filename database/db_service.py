
import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
    # """Services(id,name,time_slots,price,is_active)"""
def db_Service_Insert_Service(name :str,time,price:int,is_active:bool):
    try:
        sql =f"""INSERT INTO services (name,time,price,is_active) 
        VALUES ('{name}','{time}',{price},{is_active});"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     id= cursor.lastrowid
                     cursor.close()
                     connection.close()
                     return id
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" insertService : {e}") 
##############################################################################
def db_Service_Update_Service_Price(service_id:int,price:int):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("updateServicePrice: id is not valid")
        return False
    try:
        sql = f"""UPDATE services 
                  SET price = {price} 
                  WHERE id = {service_id};"""
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
        logging.error(f" updateServicePrice: {e}")
##############################################################################
def db_Service_Update_Service_Time(service_id:int,time:str):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("updateServiceTimeSlot: id is not valid")
        return False
    try:
        sql = f"""UPDATE services 
                  SET time = '{time}' 
                  WHERE id = {service_id};"""
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
        logging.error(f" updateServiceTimeSlot: {e}")
##############################################################################
def db_Service_Update_Service_Name(service_id:int,name:str):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("updateServiceName: id is not valid")
        return False
    try:
        sql = f"""UPDATE services 
                  SET name = '{name}' 
                  WHERE id = {service_id};"""
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
        logging.error(f" updateServiceName: {e}") 

##############################################################################
def db_Service_Update_Service_Is_Active(service_id:int , is_active:bool):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("enableService: id is not valid")
        return False
    try:
        sql = f"""UPDATE services 
                  SET is_active = '{is_active}'  
                  WHERE id = {service_id};"""
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
        logging.error(f" update is_active service: {e}") 
##############################################################################
def db_Service_Get_Is_Active_Services(service_id:int) -> bool:
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("getIsActiveServices: id is not valid")
        return False
    try:
        sql = f"""select is_active FROM services
                  WHERE id = {service_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     is_active=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return bool(is_active[0] )
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" getIsActiveServices: {e}") 
##############################################################################
def db_Service_Enable_Service(service_id:int):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("enableService: id is not valid")
        return False
    try:
        sql = f"""UPDATE services 
                  SET is_active = TRUE 
                  WHERE id = {service_id};"""
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
        logging.error(f" enableService: {e}") 
##############################################################################
def db_Service_Disable_Service(service_id:int):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("disableService: id is not valid")
        return False
    try:
        sql = f"""UPDATE services 
                  SET is_active = FALSE 
                  WHERE id = {service_id};"""
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
        logging.error(f" disableService: {e}") 
##############################################################################
def db_Service_Get_Service_With_Id(service_id:int):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("getServiceWithId: id is not valid")
        return False
    try:
        sql = f"""SELECT * FROM services 
                  WHERE id = {service_id};"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     service=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return service
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" getServiceWithId: {e}") 
##############################################################################
def db_Service_Get_Service_With_Name(service_name:str):
    try:
        sql = f"""SELECT * FROM services 
                  WHERE name = '{service_name}';"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     service=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     if service is None:
                        logging.error("service name not fund")
                        return None
                     return service
                       
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" getServiceWithName: {e}") 
##############################################################################
def db_Service_Get_All_Services():
    try:
        sql = f"""SELECT * FROM services ;"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     service=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     if service is None:
                        logging.error("service name not fund")
                        return None
                     return service
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f" getAllServices: {e}") 

##############################################################################
def db_Service_Service_Valid_Id(service_id:int):
    try:
        sql = f"""SELECT COUNT(*) 
                  FROM services 
                  WHERE id = {service_id};"""
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
        logging.error(f"serviceValidId : {e}")
        return False
########################################################
def db_Service_Delete_Service(service_id:int):
    valid_id=db_Service_Service_Valid_Id(service_id=service_id)
    if not valid_id:
        logging.error("DeleteService: id is not valid")
        return False
    try:
        sql = f"""DELETE FROM services 
                WHERE id = {service_id};"""
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
        logging.error(f"DeleteService : {e}")
########################################################