from database.db_setwork import *
from database.db_users import *
from database.db_service import *
from database.db_setwork import *
from database.db_weeklysetting import *

from functions.time_date import *
from messages.commands_msg import *
from messages.markups_text import *
from messages.messages_function import *
##############################################################################
#part1=convertDateToDayAsPersiancalendar(date='2024-10-03')
date='2024-10-04'
if 8 in [3,2,5,6,1]:
    print("result")

# parts_defult = db_WeeklySetting_Get_Parts
#     part1_default = str(parts_defult[0])
#     part2_default = str(parts_defult[1])
#     all_part=[]
#     parts=str(db_WeeklySetting_Get_Parts)
#     for i in range [:2]:
        
#         if parts[i] =='Null':
#             part_start_time = 'Null'
#             part_end_time = 'Null'
#         else :
#             part_start_time= parts[i][1].split('/')[0]
#             part_end_time = parts[i][1].split('/')[1]
#         all_part += [part_start_time ,part_end_time ]
#     db_Setwork_Insert_New_date(date= date , part1_start_time=all_part[0] , part1_end_time=all_part[1] , part2_start_time=all_part[2] , part2_end_time=[3])



# print(f'result of exist day :\n{resultt}')
# print(f'result of generate day :\n{result}')
# 
# 
# if name == 'part2':
                # if parts[0] != 'None':
                    # part1 = parts[0][1]
                    # pert1_end_time = part1.split('/')[1]
                    # check_start_time_part2 = datetime.strptime(end_time, time_format).time()
                    # check_end_time_part1 = datetime.strptime(pert1_end_time, time_format).time()
                    # if not check_end_time_part1 < check_start_time_part2:
                        # bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_part2_period)
                        # return
            # check when update part1 -> part1 be behind part2
            # if name == 'part1':
                # if parts[1] != 'None':
                    # part2 = parts[1][0]
                    # pert2_start_time = part2.split('/')[0]
                    # check_start_time_part2 = datetime.strptime(pert2_start_time, time_format).time()
                    # check_end_time_part1 = datetime.strptime(end_time, time_format).time()
                    # if not check_end_time_part1 > check_start_time_part2:
                        # bot.send_message(chat_id=msg.chat.id, text=text_set_work_error_input_compare_part1_period)
                        # return
# 
#############################################################################   db 
####################### sql for create table
# 
# use beauty_ass;
# CREATE TABLE reservations (
#     reservation_id INT PRIMARY KEY AUTO_INCREMENT,
#     user_id INT NOT NULL,
#     reservation_date DATE NOT NULL,
#     start_time TIME NOT NULL,
#     end_time TIME NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     CHECK (start_time >= '09:00:00' AND end_time <= '14:00:00'), -- Must be within work hours
#     CHECK (start_time < end_time), -- Ensures that start time is before end time
#     CHECK (MINUTE(start_time) % 15 = 0) ,
#     CHECK (MINUTE(end_time) % 15 != 0),
#     -- Ensure times are on 15-min slots
#     UNIQUE (reservation_date, start_time, end_time) -- Prevent overlapping reservations
# );

# ######################## insert
# INSERT INTO reservations (user_id, reservation_date, start_time, end_time)
# VALUES (1, '2024-09-25', '09:45:00', '10:29:00');

# ########################  get free time in set work
# WITH RECURSIVE time_slots AS (
#     -- Generate 15-min time slots starting from 9:00 AM (300 minutes = 20 slots)
#     SELECT '09:00:00' AS slot_start_time,
#            ADDTIME('09:00:00', '00:14:00') AS slot_end_time
#     UNION ALL
#     SELECT ADDTIME(slot_start_time, '00:15:00') AS slot_start_time,
#            ADDTIME(slot_encreateBotSettingd_time, '00:15:00') AS slot_end_time
#     FROM time_slots
#     WHERE slot_end_time < '13:59:00' -- Stop before 2:00 PM (to include 1:45 PM - 2:00 PM slot)
# ),
# numeric_time_slots AS (
#   SELECT 
#     ROW_NUMBER() OVER (ORDER BY slot_start_time) AS SlotNumber,
#     slot_start_time, slot_end_time
#   FROM time_slots  
# )
# reserved_slots AS (
#     SELECT start_time, end_time
#     FROM reservations
#     WHERE reservation_date = '2024-09-25'
# )
# -- Fetch time slots that are not reserved
# SELECT slot_start_time, slot_end_time ,SlotNumber
# FROM numeric_time_slots t
# LEFT JOIN reserved_slots r
#     ON t.slot_start_time BETWEEN r.start_time AND r.end_time
#     OR t.slot_end_time BETWEEN r.start_time AND r.end_time
#     OR (r.start_time <= t.slot_start_time AND r.end_time >= t.slot_end_time)
# WHERE r.start_time IS NULL;
