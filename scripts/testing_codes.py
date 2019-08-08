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

with open(os.path.join(directory, RecordTxt), "r") as record:
    for line in record.readlines():
        line = line.replace('\n', '')
        item, info = line.split('=')
        RecordDict.update({item : info})
