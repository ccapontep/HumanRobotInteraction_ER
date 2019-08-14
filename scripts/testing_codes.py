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


# Calculate the urgency given the picked items of the patient
agePoints = 0
if int(RecordDict["Age"]) < 10: # if it is a young patient, higher urgency
    agePoints += 3
elif int(RecordDict["Age"]) > 70: # if it's an old patient, higher urgency
    agePoints += 2
else: agePoints += 1

histPoints = 0
if 'smoke cigarettes' in RecordDict['PastMedicalHistory']:
    if 'chest' in RecordDict['LocationofPain'] or len([e for e in ['breathing', 'chest pain', 'coughing'] if e in RecordDict['EmergencySymptoms']]) > 0:
        histPoints += 1.5
    else: histPoints += 1

checkHist = [e for e in ['overweight or obese', 'high cholesterol', 'hypertension', 'diabetes'] if e in RecordDict['PastMedicalHistory']]
if len(checkHist) > 0:
    histPoints += (1.5 * len(checkHist))
if 'recurring symptoms' in RecordDict['PastMedicalHistory']: histPoints += 2

painPoints = 0
if 'some' in RecordDict['PainLevel']:
    painPoints = 1
elif 'moderate' in RecordDict['PainLevel']:
    painPoints = 2
elif 'intense' in RecordDict['PainLevel']:
    painPoints = 3
elif 'very intense' in RecordDict['PainLevel']:
    painPoints = 5
elif 'excruciating' in RecordDict['PainLevel']:
    painPoints = 7

emergPoints = 0
listEmerg = ['bleeding','breathing','unusual behavior','chest pain','choking','coughing','severe vomiting','fainting','serious injury','deep wound','sudden severe pain','sudden dizziness','swallowing poisonous','severe abdominal','head spine','feeling suicide murder']    
checkEmerg = [e for e in listEmerg if e in RecordDict['EmergencySymptoms']]
if len(checkEmerg) > 0:
    emergPoints += (10 * len(checkEmerg) * painPoints)

symPoints = 0
listSym = ['fever or chills','nausea or vomit','limited movement','loss senses','cut','pain','inflammation','dizzy','recurring']
checkSym = [e for e in listSym if e in RecordDict['Symptoms']]
if len(checkSym) > 0:
    symPoints += (2 * len(checkSym) * painPoints)

locPoints = 0
listLoc = ['foot', 'legs', 'arms', 'hands', 'back']
listLoc2 = ['abdomen', 'chest', 'head']
checkLoc = [e for e in listLoc if e in RecordDict['LocationofPain']]
checkLoc2 = [e for e in listLoc2 if e in RecordDict['LocationofPain']]
if len(checkLoc) > 0:
    locPoints += (1.5 * len(checkLoc))
if len(checkLoc2) > 0:
    locPoints += (2 * len(checkLoc2))

conscPoints = 0
if 'medium' in RecordDict['LevelofConsciousness']:
     conscPoints += 2
elif 'barely' in RecordDict['LevelofConsciousness']:
    conscPoints += 7
elif 'unconscious' in RecordDict['LevelofConsciousness']:
    conscPoints += 15




