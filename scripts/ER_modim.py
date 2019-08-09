import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')

from ws_client import *
import ws_client

cmdsever_ip = '10.3.1.1'
cmdserver_port = 9101

mc = ModimWSClient()
mc.setCmdServerAddr(cmdsever_ip, cmdserver_port)
# patient = 'False'
# mc.setGlobalVar(patient, 'False')

# def f():
#     return 1

def i0():
    begin()
    im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    im.display.remove_buttons()
    im.display.loadUrl('HRIER/ERstart.html')

    im.executeModality('TEXT_title','Welcome to Wellness Hospital!')
    say('Welcome to Wellness Hospital', 'en')
    im.executeModality('TEXT_default','Ready to start the interaction?')
    say('Press start to begin the interaction with me.', 'en')

    im.executeModality('BUTTONS',[['start','Start!']])
    im.executeModality('ASR',['start'])

    startQ = im.ask(actionname=None, timeoutvalue=100000000000)
    im.display.remove_buttons()

    if startQ == 'start':
        i1()

    end()

# Interaction to welcome and start interaction
def i1():

    # im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    # im.gitpull()
    begin()
    im.display.remove_buttons()
    im.display.loadUrl('HRIER/ERslide.html')

    im.executeModality('TEXT_title','Welcome to Wellness Hospital!')
    say('Welcome to Wellness Hospital', 'en')
    im.executeModality('TEXT_default','Have you been helped previously?')
    say('Have you been helped previously?','en')

    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
    im.executeModality('ASR',['yes','no'])

    a = im.ask(actionname=None, timeoutvalue=100000000000)
    im.display.remove_buttons()

    # run = True
    #
    # while run:
    # aa = asr()
    # say('the answer given is '+a)

    # if ('yes' in aa) or a == 'yes':
    if a == 'yes':
        im.executeModality('TEXT_default','You are a patient in the database.')
        say('Welcome back', 'en')
        time.sleep(1)
        i2()

    # elif ('no' in aa) or a == 'no':
    elif a == 'no':
        im.executeModality('TEXT_default','I am a new patient.')
        say('Welcome to Wellness Hospital. My name is Marrtino and I will help you setup your emergency in the database', 'en')
        say('I will be asking some questions about your emergency and have you see a doctor as soon as possible, depending on the severity of your emergency', 'en')
        say('I will also be doing routine checks to let you know your remaining wait time. If at any point you have questions, come ask', 'en')
        say('We will take care of you. Thank you for visiting us.', 'en')
        time.sleep(2)
    # elif ('' in aa):
    else:
        im.executeModality('TEXT_default','No answer received')
        time.sleep(3)

    end()


# Interaction to check ticket info and retrieve info for the user
def i2():
    begin()
    import os, re, ast, time
    import numpy as np

    im.display.loadUrl('ERindex.html')
    im.executeModality('TEXT_default', 'Please enter the digits of your ticket number one by one.')
    say('Let me look for you in the database. Please enter your ticket number', 'en')

    # There are three digits in the ticket number, check one by one with buttons
    CorrTick = 'no'
    while CorrTick == 'no':
        # First number:
        im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
        im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
        Num1 = im.ask(actionname=None, timeoutvalue=500)
        say('number '+Num1)
        im.display.remove_buttons()

        # Second number:
        im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
        im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
        Num2 = im.ask(actionname=None, timeoutvalue=200)
        say('number'+Num2)
        im.display.remove_buttons()

        # Second number:
        im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
        im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
        Num3 = im.ask(actionname=None, timeoutvalue=200)
        say('number'+Num3)
        im.display.remove_buttons()

        # Final ticket number
        ticketNumber = str(Num1 + Num2 + Num3)
        time.sleep(1)
        ticketStr = 'Your ticket number is: ' + ticketNumber
        im.executeModality('TEXT_default', ticketStr)
        say('Your ticket number is '+ticketNumber)

        # Check if ticket was entered correctly
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
        im.executeModality('ASR',['yes','no'])
        CorrTick = im.ask(actionname=None, timeoutvalue=100)
        im.display.remove_buttons()
        if CorrTick == 'yes':
            say('Great! Let me look at your information')
        elif CorrTick == 'no':
            im.executeModality('TEXT_default', 'Please enter again the digits of your ticket number one by one.')
            say('Sorry about that. Let us try again')

        # Check the tickets in the system
        directory = "/home/ubuntu/playground/HumanRobotInteraction_ER/patientInfo"

        ticketNums = []
        with open(os.path.join(directory, "PatientTicketNum.txt"), "r") as patientTicketNums:
            for ticket in patientTicketNums.readlines():
                ticketNums.append(str(ticket))
        if CorrTick == 'yes' and len(ticketNums) > 0 and int(ticketNumber) in (map(int, ticketNums)):
            im.executeModality('TEXT_default', 'Your ticket has been found!')
            say('Your ticket has been found in the database', 'en')
            CorrTick == 'yes'
            # break
        elif CorrTick == 'yes' and int(ticketNumber) not in (map(int, ticketNums)):
            im.executeModality('TEXT_default', 'Sorry. Your ticket was not found.')
            say('Your ticket was not found. Let us start again.', 'en')
            im.executeModality('TEXT_default', 'Please enter again the digits of your ticket number one by one.')
            CorrTick = 'no'

    # Retrieve the info of user in database
    RecordDict = dict()
    # RecordNames = ['Name', 'Age', 'PastMedicalHistory', 'EmergencySymptoms', 'Symptoms','LocationofPain', 'LevelofConsciousness', 'TimeAdmitted','UrgencyLevel', 'RemainingWaitTime', 'ChangeinWaitTime']
    im.display.loadUrl('ERretrieve.html')
    im.executeModality('TEXT_title','Review of your Patient Record')
    RecordTxt = ticketNumber + ".txt"
    with open(os.path.join(directory, RecordTxt), "r") as record:
        for line in record.readlines():
            line = line.replace('\n', '')
            item, info = line.split('=')
            RecordDict.update({item : info})
    hello_say = 'Hello, ' + RecordDict["Name"]
    say(hello_say, 'en')
    im.executeModality('TEXT_default', 'What information are you searching for?')
    say('What can I help you with?', 'en')

    AskAgain = True
    while AskAgain == True:
        # Ask what the user wants
        im.executeModality('BUTTONS',[['waittime','Get my Remaining Wait Time'],['update','Update my Records'], ['done', 'Done, exit.']])
        im.executeModality('ASR',['waittime','update', 'done'])
        UserQues = im.ask(actionname=None, timeoutvalue=100000000)
        im.display.remove_buttons()

        if UserQues == 'done':
            im.executeModality('TEXT_default', 'Thank you for checking your record.')
            say('Goodbye!', 'en')
            AskAgain = False


        # Get record of admit, wait and curr times. Caculate the new wait time.
        elif UserQues == 'waittime':
            urgencyStr = RecordDict["UrgencyLevel"]
            admit_time = float(RecordDict["TimeAdmitted"])
            curr_sec = time.time()

            waittingTime = RecordDict["WaitTime"]
            wHour, wMin = waittingTime.split(':')
            waitTimeSec = int(wHour)*60*60 + int(wMin)*60

            remain_time_sec = waitTimeSec - (curr_sec - admit_time)
            remain_min = (round(remain_time_sec) // 60) % 60
            remain_hr = round(remain_time_sec) // 3600
            if remain_min <= 0 or remain_hr <= 0: # if no more remaining time
                remain_str = '0h0m'
                Remain_print = 'Your emergency is a ' + urgencyStr + ' level. \nWe will be with you shortly in 0 min.'
                Remain_say = 'Your emergency ' + urgencyStr + ' level. No more wait time, someone will be with you shortly.'
                im.executeModality('TEXT_default', Remain_print)
                say(Remain_say, 'en')
                time.sleep(5)
            else:
                remain_str = str(int(remain_hr)) + 'h' + str(int(remain_min)) + 'm'
                Remain_print = 'Your emergency is a ' + urgencyStr + ' level. \nWe will be with you shortly in ' + str(int(remain_hr)) + ' hour(s) and ' + str(int(remain_min)) + ' minute(s)'
                Remain_say = 'Your emergency ' + urgencyStr + ' level. We will be with in ' + str(int(remain_hr)) + ' hour and ' + str(int(remain_min)) + ' minutes'
                im.executeModality('TEXT_default', Remain_print)
                say(Remain_say, 'en')
                time.sleep(5)

            RecordDict.update({"RemainingWaitTime" : remain_str}) # update the info in the record

        # If the user wants to update its information Record
        elif UserQues == 'update':
            updateD = True
            while updateD == True:
                im.executeModality('TEXT_default', 'Which would you like to update?')
                say('Pick the item you would like to change.', 'en')

                im.executeModality('BUTTONS',[['history','Past Medical History'],['emergency','Emergency Symptoms'], ['symptoms', 'Symptoms'], ['location', 'Location of Pain'], ['conscious', 'Level of Consciousness'], ['done', 'Done, exit.']])
                im.executeModality('ASR',['history','emergency', 'symptoms', 'location', 'conscious', 'done'])
                HistQues = im.ask(actionname=None, timeoutvalue=10000)
                im.display.remove_buttons()

                if HistQues == 'done':
                    im.executeModality('TEXT_default', 'Thank you for checking your record.')
                    say('Goodbye!', 'en')
                    updateD = False

                if HistQues == 'history':
                    im.executeModality('TEXT_default', 'Select again all that apply.')
                    hist2add = ''
                    histD = True
                    while histD == True:
                        im.executeModality('BUTTONS',[['weight','Overweight/Obese'],['cigar','SmokeCigarettes'], ['chol', 'HighCholesterol'], ['hyper', 'Hypertension'], ['diabetes', 'Diabetes'], ['againSym', 'CurrentSymptomsRecurring'], ['done', 'Done, exit.']])
                        im.executeModality('ASR',['weight','cigar', 'chol', 'hyper', 'diabetes', 'againSym', 'done'])
                        histQ = im.ask(actionname=None, timeoutvalue=10000)
                        im.display.remove_buttons()

                        if not histQ == 'done':
                            say('Item has been added', 'en')
                            hist2add = hist2add + ',' + histQ
                        else: histD = False
                    RecordDict.update({"PastMedicalHistory" : hist2add}) # Update data in record
                    im.executeModality('TEXT_default', RecordDict['PastMedicalHistory'])




    end()

# Interaction to retrieve info for the user
def i3():
    im.display.loadUrl('ERretrieve.html')
    im.executeModality('TEXT_default', 'What information are you searching for?')
    say('Hello there', 'en')

mc.setDemoPath('/home/ubuntu/playground/HumanRobotInteraction_ER')
mc.store_interaction(i2)
mc.store_interaction(i1)
mc.store_interaction(i0)
mc.run_interaction(i1)
# mc.run_interaction(i0)


# mc.store_interaction(f)
# mc.run_interaction(i3)
