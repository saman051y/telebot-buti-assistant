
from datetime import datetime, timedelta
import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from auth.auth import DB_CONFIG
from functions.time_date import  add_times


def db_make_reserve_transaction(user_id,price,start_time,date,services,duration):
    end_time1 = add_times(time1=start_time,time2=duration)
    end_time=f"{end_time1[:5]}:00"
    successful=False
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    sql_reserve=f"""
                    INSERT INTO reserve (user_id,date,start_time,end_time,payment) 
                    VALUES ({user_id},'{date}','{start_time}','{end_time}',{price});"""
                    cursor.execute(sql_reserve)
                    reserve_id = cursor.lastrowid
                    if reserve_id == 0:
                        raise Exception("Insert failed, reserve_id is 0.")
                    print(reserve_id)
                    # sql_work_time=
                    # cursor.execute(sql_set_time)
                    for service in services:
                        service_id=service[0]
                        sql_services_reserve=f"""
                        INSERT INTO reserve_services (service_id,reserve_id) 
                        VALUES ({service_id},{reserve_id});"""
                        cursor.execute(sql_services_reserve)

                    connection.commit()
                    logging.info(" Transaction committed successfully ")
                    successful=True 

    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred 'make_reserve_transaction', rolling back: {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return successful , reserve_id

##############################################################

def delete_reservation(reserve_id):
    successful=False
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    print(reserve_id)
                    connection.start_transaction()
                    sql_delete_reserve = f"""
                    DELETE FROM reserve 
                    WHERE id = {reserve_id};"""
                    cursor.execute(sql_delete_reserve)

                    sql_services_reserve=f"""
                    DELETE FROM reserve_services
                    WHERE reserve_id = {reserve_id}; """
                    cursor.execute(sql_services_reserve)

                    connection.commit()
                    logging.info(" Transaction committed successfully ")
                    successful=True 

    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred 'delete_reservation', rolling back: {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return successful 