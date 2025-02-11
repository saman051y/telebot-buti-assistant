import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from auth.auth import DB_CONFIG
from database.db_admin_list import *
from database.db_bot_setting import *
from database.db_users import db_Users_Insert_New_User
from database.db_weeklysetting import *
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
        created=createBot_setting()
        if not created:
            return False
        created=createAdminTable()
        if not created:
            return False
        logging.info("data base is working")
        return True
    except Error as e:
        logging.error(f"createTables: {e}")
#######################################################################################
def insert_basic_setting():
    result=db_bot_setting_get_all()
    if result is None or len(result)<1:
        db_bot_setting_insert(name="cart",value="5022291508281118")
        db_bot_setting_insert(name="cart_name",value="سمانه نصیری")
        db_bot_setting_insert(name="cart_bank",value="پاسارگاد")
        db_bot_setting_insert(name="bot_is_enable",value="1")
        db_bot_setting_insert(name="main_admin",value="1054820423")
        db_bot_setting_insert(name="welcome_message",value="خوش امدید")
        logging.info("first init info in db_bot_setting is done")

    result =db_admin_get_all()
    if result is None or len(result)<1:
        #setup user
        db_Users_Insert_New_User(user_id=1054820423,phone_number="09383520044",username="saaman",join_date="2024-01-01",name="SYaghoobi")
        db_Users_Insert_New_User(user_id=423977498,phone_number="09033883130",username="Ho3einNa3iri",join_date="2024-01-01",name="HNa3iri")
        db_Users_Insert_New_User(user_id=316900317,phone_number="0911111111",username="samaneh",join_date="2024-01-01",name="samaneh")
        #setup admins
        db_admin_add(admin_id=1054820423,main_admin=False)#saman
        db_admin_add(admin_id=423977498,main_admin=False)#Ho3ein
        db_admin_add(admin_id=316900317,main_admin=True)#samaneh
        logging.info("first init info in db_admin_list is done")
    
    #check exist weekly_setting
    result_weekly_setting=db_WeeklySetting_Get_All()
    if result_weekly_setting is None:
        db_WeeklySetting_Insert(name='saturday' , value='1' )
        db_WeeklySetting_Insert(name='sunday'   , value='1' )
        db_WeeklySetting_Insert(name='monday'   , value='1' )
        db_WeeklySetting_Insert(name='tuesday'  , value='1' )
        db_WeeklySetting_Insert(name='wednesday', value='1' )
        db_WeeklySetting_Insert(name='thursday' , value='1' )
        db_WeeklySetting_Insert(name='friday'   , value='1' )
        db_WeeklySetting_Insert(name='part1', value='09:00:01/15:00:00')
        db_WeeklySetting_Insert(name='part2', value='15:00:01/20:00:00')
        logging.info("db_bot_setting and db_weekly_setting is done")

    logging.info("DB setting is completed")

#######################################################################################
def createUserTable():
    """users(user_id,phone_number,username,join_date,name,last_name)"""
    try:
        sql=f""" CREATE TABLE IF NOT EXISTS users  (
        user_id BIGINT NOT NULL PRIMARY KEY,
        phone_number VARCHAR(11),
        username VARCHAR(255),
        join_date DATE NOT NULL,
        name VARCHAR(255)
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
def createServicesTable():
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
def createBot_setting():
    """  bot_setting(name:varchar(255), value:text,)   """
    try:
        sql=f"""CREATE TABLE IF NOT EXISTS bot_setting (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                value TEXT 
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
        logging.error(f"in createBotSetting : {e}") 
        return False
#######################################################################################
def createAdminTable():
    try:
        sql=f"""CREATE TABLE IF NOT EXISTS admin_list (
    admin_id BIGINT PRIMARY KEY,
    main_admin BOOLEAN NOT NULL
    );
    """
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
        logging.error(f"in createBotSetting : {e}") 
        return False
#######################################################################################
def createWeeklySetting():
    """  weekly_setting(name:varchar(20), value:varchar(20),)   """
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
                     return True
                
            else:
                logging.error("connection to database is not working")
    except Error as e :
        logging.error(f"in createBotSetting : {e}") 
        return False
#######################################################################################