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
        created=createTimingTable()
        if not created:
            return False
        created=createReserveTable()
        if not created:
            return False
        logging.info("data base is working")
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
def createTimingTable():
    """each hour save as  4 part like 0200 => {0 = not working, 1 = working ,2 = full} for each bit
       0000 : {0 to 15 min ,15 to 30 min,30 min to 45,45 to 60}
    """
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS timing  (
 	 record_date DATE PRIMARY KEY NOT NULL ,
     hour_00 CHAR(4) NOT NULL DEFAULT 0,
     hour_01 CHAR(4) NOT NULL DEFAULT 0,
     hour_02 CHAR(4) NOT NULL DEFAULT 0,
     hour_03 CHAR(4) NOT NULL DEFAULT 0,
     hour_04 CHAR(4) NOT NULL DEFAULT 0,
     hour_05 CHAR(4) NOT NULL DEFAULT 0,
     hour_06 CHAR(4) NOT NULL DEFAULT 0,
     hour_07 CHAR(4) NOT NULL DEFAULT 0,
     hour_08 CHAR(4) NOT NULL DEFAULT 0,
     hour_09 CHAR(4) NOT NULL DEFAULT 0,
     hour_10 CHAR(4) NOT NULL DEFAULT 0,
     hour_11 CHAR(4) NOT NULL DEFAULT 0,
     hour_12 CHAR(4) NOT NULL DEFAULT 0,
     hour_13 CHAR(4) NOT NULL DEFAULT 0,
     hour_14 CHAR(4) NOT NULL DEFAULT 0,
     hour_15 CHAR(4) NOT NULL DEFAULT 0,
     hour_16 CHAR(4) NOT NULL DEFAULT 0,
     hour_17 CHAR(4) NOT NULL DEFAULT 0,
     hour_18 CHAR(4) NOT NULL DEFAULT 0,
     hour_19 CHAR(4) NOT NULL DEFAULT 0,
     hour_20 CHAR(4) NOT NULL DEFAULT 0,
     hour_21 CHAR(4) NOT NULL DEFAULT 0,
     hour_22 CHAR(4) NOT NULL DEFAULT 0,
     hour_23 CHAR(4) NOT NULL DEFAULT 0,
     hour_24 CHAR(4) NOT NULL DEFAULT 0
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
    """reserve(id,user_id,date,start_time,end_time,approved,payment)"""
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS reserve  (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT NOT NULL ,
        date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        approved bool NOT NULl DEFAULT 0,
        payment INT NOT NULL DEFAULT 0
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
    """Services(id,time_slots,price,is_active)"""
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS Services  (
        id INT AUTO_INCREMENT PRIMARY KEY,
        time_slots INT NOT NULL ,
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