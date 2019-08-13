# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

directory = "/home/ccapontep/Documents/1_AIRO/Y2S2/Elective_in_AI/HRI/ER_Robot/HumanRobotInteraction_ER/patientInfo"

import os

ticketNumber = '012'

RecordTxt = ticketNumber + ".txt"
RecordDict = dict()

# Creating the ticket dictionary from record
with open(os.path.join(directory, RecordTxt), "r") as record:
    for line in record.readlines():
        line = line.replace('\n', '')
        item, info = line.split('=')
        RecordDict.update({item : info})


# Get the remaining time
# Test
import time
#seconds = time.time()
#print"Seconds since epoch =", seconds
#
#curr_time = time.localtime(seconds)
#print"Current time is: ", curr_time
#print"The hour: ", curr_time.tm_hour
#print"The minutes: ", curr_time.tm_min
#print"The seconds: ", curr_time.tm_sec

# From the code
admit_time = float(RecordDict["TimeAdmitted"])
curr_sec = time.time()

waittingTime = RecordDict["WaitTime"]
wHour, wMin = waittingTime.split('-')
waitTimeSec = int(wHour)*60*60 + int(wMin)*60

remain_time_sec = waitTimeSec - (curr_sec - admit_time)
remain_min = (round(remain_time_sec) // 60) % 60
remain_hr = round(remain_time_sec) // 3600
if remain_min < 0 or remain_hr < 0: # if no more remaining time
    remain_str = '0h0m'
else:
    remain_str = str(int(remain_hr)) + 'h' + str(int(remain_min)) + 'm'
    
stringDic = str(RecordDict)
stringDic = stringDic.replace(', ','\n').replace("'","").replace('{','').replace('}','').replace(': ','=')

recFile = open(os.path.join(directory, RecordTxt), "w")
recFile.write(stringDic)
recFile.close()


# Add time admitted:
curr_sec = time.time()
loc_time = time.localtime(curr_sec)
curr_date = ((time.ctime(curr_sec)).split(':')[0])[:-3]
curr_time = str(loc_time.tm_hour) + ' hours and ' + str(loc_time.tm_min) + ' minutes'
RecordDict.update({"TimeAdmitted" : curr_sec}) # Update data in record
StrRecord = 'Your date admitted is: ' + curr_date
StrRecord2 = 'Your time admitted is: ' + curr_time




