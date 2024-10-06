import glob
import logging
import os
#####################
def get_latest_log_file():
    log_path = "./logs/"
    log_files = glob.glob(f"{log_path}*.log")
    #sort file with date and time 
    log_files.sort(key=os.path.getmtime)
    
    if len(log_files) <2:
        return log_files[-1]
    #last file
    return log_files[-2]

#####################
def remove_old_logs():
    log_path = "./logs/"
    log_files = glob.glob(f"{log_path}*.log")
    log_files.sort(key=os.path.getmtime)

    if len(log_files) > 7:
        for file in log_files[:-7]:
            os.remove(file)
            logging.info(f"old log removed: {file}")
#####################
def get_last_errors(log_file,errorLines=3):
    """return error line , default 3 line"""
    with open(log_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    #filter line for finding errors
    error_lines = [line for line in lines if 'ERROR' in line]
    
    #get last errors
    return error_lines[-errorLines:] if len(error_lines) >= 3 else error_lines
#####################
def log_test_error():
    logging.error("test1")
    logging.error("test2")
    logging.error("test3")
    logging.error("test4")
    logging.error("test5")
    logging.error("test6")