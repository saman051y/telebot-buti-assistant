
import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG

    # """createReserveServicesTable(id,reserve_id,service_id)"""
############################################3
def insertReserveService(service_id:int,reserve_id):
    try:
        sql =f"""INSERT INTO reserve_services (service_id,reserve_id) 
        VALUES ({service_id},{reserve_id});"""
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
        logging.error(f"DeleteReserveService : {e}")
############################################3
def getResSerWithResId(reserve_id):
    try:
        sql=f"""SELECT service_id FROM reserve_services 
        WHERE reserve_id = {reserve_id}"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    services= cursor.fetchall()
                    cursor.close()
                    connection.close()
                    return services
            else:
                logging.error("connection to database is not working")
                return False
    except Error as e:
        logging.error(f"DeleteReserveService : {e}")
##################################################
def DeleteReserveService(reserve_service_id:int):
    valid_id=reserveServiceValidId(reserve_id=reserve_service_id)
    if not valid_id:
        logging.error("DeleteReserveService: id is not valid")
        return False
    try:
        sql = f"""DELETE FROM reserve_services 
                WHERE id = {reserve_service_id};"""
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
        logging.error(f"DeleteReserveService : {e}")
##################################################
def reserveServiceValidId(reserve_service_id:int):
    try:
        sql = f"""SELECT COUNT(*) 
                  FROM reserve 
                  WHERE id = {reserve_service_id};"""
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
        logging.error(f"reserveServiceValidId : {e}")
        return False