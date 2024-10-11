import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from auth.auth import DB_CONFIG
#######################################################################################
def createTables():
    try:
        created= createUserTable()
        if not created:
            return False
        created=createSetWorkTable()
        if not created:
            return False
        created=createReserveTable()
        if not created:
            return False
        created=createServicesTable()
        if not created:
            return False
        created=createReserveServicesTable()
        if not created:
            return False
        created=createWeeklySetting()
        if not created:
            return False
        logging.info("data base is working")
        return True
    except Error as e:
        logging.error(f"createTables: {e}")
#######################################################################################
def createUserTable():
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS users  (
        user_id BIGINT NOT NULL PRIMARY KEY,
        phone_number VARCHAR(11),
        username VARCHAR(255),
        join_date DATE NOT NULL,
        name VARCHAR(255),
        last_name VARCHAR(255)
    );"""
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
        logging.error(f"in createUserTable : {e}")
        return False
#######################################################################################
def createSetWorkTable():
    """
    date,part1_start_time,part1_end_time,part2_start_time,part2_end_time,part3_start_time,part3_end_time)
    date like 2024-09-04
    each part start input start with 1 secend like 09:00:01 and min={00,15,45}
    each part end input start with 0 second like 09:00:00 and min={00,15,45}
    """
    try:
        sql=f"""
                CREATE TABLE IF NOT EXISTS setwork (
 	            id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE UNIQUE,   
                part1_start_time TIME NULL,
                part1_end_time TIME NULL,
                part2_start_time TIME NULL,
                part2_end_time TIME NULL
                );"""
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
        logging.error(f"in createTimingTable : {e}")
        return False
#######################################################################################
def createReserveTable():
    """ 
        start_time and end_time like 09:30:00
        reservation_date like 2024-05-25
    """
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS reserve (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT NOT NULL ,
        date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        approved bool NOT NULl DEFAULT 0,
        payment INT NOT NULL DEFAULT 0 ,
        -- CHECK (start_time < end_time),                  -- Ensures that start time is before end time 
        -- CHECK (MINUTE(start_time) % 15 = 0),            -- Ensure times are on 15-min slots
        -- CHECK (MINUTE(end_time) % 15 != 0),             -- Ensure times end at 14,29,44,59 Mins
        UNIQUE (date, start_time, end_time)             -- Prevent overlapping reservations
    );"""
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
        logging.error(f"in createReserveTable : {e}") 
        return False
#######################################################################################
def createServicesTable():# todo work on this
    """Services(id,name,time_slots,price,is_active)"""
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS services  (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL ,
        time TIME NOT NULL ,
        price INT NOT NULL DEFAULT 0,
        is_active BOOL NOT NULL DEFAULT TRUE
    );"""
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
        logging.error(f"in createReserveTable : {e}") 
        return False
#######################################################################################
def createReserveServicesTable():
    """createReserveServicesTable(id,reserve_id,service_id)"""
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS reserve_services (
        id INT AUTO_INCREMENT PRIMARY KEY,
        reserve_id INT NOT NULL ,
        service_id INT NOT NULL DEFAULT 0);"""
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
        logging.error(f"in createReserveTable : {e}") 
        return False
#######################################################################################
def createWeeklySetting():
    """  createBotSetting(name:varchar(20), value:varchar(20),)   """
    try:
        sql=f"""CREATE TABLE IF NOT EXISTS weekly_setting (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(20) UNIQUE NOT NULL,
                value VARCHAR(17) NOT NULL
                );"""
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()# when something is created or updated or inserted;
                     cursor.close()
                     connection.close()
                     DefualtValueWeeklySetting()
                     return True
                
            else:
                logging.error("connection to database is not working")
    except Error as e :
        logging.error(f"in createBotSetting : {e}") 
        return False
#######################################################################################
def DefualtValueWeeklySetting() :
    try:
        sql_check=f"""SELECT COUNT(*) FROM weekly_setting"""
        sql_insert=f"""
                    INSERT INTO weekly_setting (name, value)
                    VALUES 
                        ('saturday', '1'),
                        ('sunday', '1'),
                        ('monday', '1'),
                        ('tuesday', '1'),
                        ('wednesday', '1'),
                        ('thursday', '1'),
                        ('friday', '1'),
                        ('part1', '09:00:01/15:00:00'),
                        ('part2', '15:00:01/20:00:00');
                    """
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql_check)
                     count = cursor.fetchone()[0]# when something is created or updated or inserted;
                     if count == 0:
                         cursor.execute(sql_insert)
                         connection.commit()
                     cursor.close()
                     connection.close()
                     return True
            else:
                logging.error("connection to database is not working")
    except Error as e :
        logging.error(f"in DefualtValueBotSetting : {e}") 
        return False
#######################################################################################