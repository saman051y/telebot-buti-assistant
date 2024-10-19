import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from auth.auth import DB_CONFIG

def db_admin_add(admin_id:int, main_admin:bool=False):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "INSERT INTO admin_list (admin_id, main_admin) VALUES (%s, %s);"
                    cursor.execute(sql, (admin_id, main_admin))
                    connection.commit()
                    return True
    except mysql.connector.Error as e:
        logging.error(f"Error db_admin_add: {e}")
        return False
#######################################################################################
def db_admin_update(admin_id, main_admin):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "UPDATE admin_list SET main_admin = %s WHERE admin_id = %s;"
                    cursor.execute(sql, (main_admin, admin_id))
                    connection.commit()
                    return True
    except mysql.connector.Error as e:
        logging.error(f"Error db_admin_update: {e}")
#######################################################################################
def db_admin_get_all():
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM admin_list;"
                    cursor.execute(sql)
                    admins = cursor.fetchall()
                    if admins:
                        return admins
                    else:
                        return None
    except mysql.connector.Error as e:
        logging.error(f"Error db_admin_get_all: {e}")
        return None
#######################################################################################
def db_admin_get_main_admin():
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM admin_list WHERE main_admin = TRUE;"
                    cursor.execute(sql)
                    main_admin = cursor.fetchone()
                    return main_admin[0]
    except mysql.connector.Error as e:
        logging.error(f"Error db_admin_get_main_admin: {e}")
        return None
#######################################################################################
def db_admin_remove_admin(admin_id: int):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = f"DELETE FROM admin_list WHERE admin_id = {admin_id};"
                    cursor.execute(sql)
                    connection.commit()  # Commit the transaction
                    return True
    except mysql.connector.Error as e:
        logging.error(f"Error db_admin_remove_admin: {e}")
        return False
#######################################################################################
def db_admin_set_main_admin(admin_id):
    sql_update_false = "UPDATE admin_list SET main_admin = FALSE WHERE main_admin = TRUE;"
    sql_update_true = f"UPDATE admin_list SET main_admin = TRUE WHERE admin_id = {admin_id};"

    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute(sql_update_false)  # Set all other main_admins to false
                    cursor.execute(sql_update_true)   # Set the specified admin_id to true
                    connection.commit()
    except mysql.connector.Error as e:
        logging.error(f"Error setting main admin: {e}")
