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
        im.executeModality('TEXT_default','You are a new patient.')
        say('Welcome to Wellness Hospital. I am a robot and my name is Marrtino. I will help you setup your emergency in the database', 'en')
        # say('I will be asking some questions about your emergency and have you see a doctor as soon as possible, depending on the severity of your emergency', 'en')
        # say('I will also be doing routine checks to let you know your remaining wait time. If at any point you have questions, come ask', 'en')
        # say('We will take care of you. Thank you for visiting us.', 'en')
        time.sleep(2)
        i3()
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
        Num1 = im.ask(actionname=None, timeoutvalue=1000)
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
            urgencyStr = RecordDict["UrgencyLevel"].split('-')[1]
            admit_time = float(RecordDict["TimeAdmitted"])
            updatedT = RecordDict["ChangeinWaitTime"]
            curr_sec = time.time()

            waittingTime = RecordDict["WaitTime"]
            wHour, wMin = waittingTime.split('-')
            waitTimeSec = int(wHour)*60*60 + int(wMin)*60

            remain_time_sec = waitTimeSec - (curr_sec - admit_time)
            remain_min = (round(remain_time_sec) // 60) % 60
            remain_hr = round(remain_time_sec) // 3600
            if remain_min <= 0 or remain_hr <= 0: # if no more remaining time
                remain_str = '0h0m'
                Remain_print = 'Your emergency is a ' + urgencyStr + ' level. We will be with you shortly in 0 min.'
                Remain_say = 'Your emergency ' + urgencyStr + ' level. No more wait time, someone will be with you shortly.'
                im.executeModality('TEXT_default', Remain_print)
                say(Remain_say, 'en')
                time.sleep(5)
            else:
                remain_str = str(int(remain_hr)) + 'h' + str(int(remain_min)) + 'm'
                Remain_print = 'Your emergency is a ' + urgencyStr + ' level. Your wait time ' + updatedT + 'been changed due to other higher emergency patients. We will be with you shortly in ' + str(int(remain_hr)) + ' hour(s) and ' + str(int(remain_min)) + ' minute(s)'
                Remain_say = 'Your emergency is ' + urgencyStr + ' level. We will be with in ' + str(int(remain_hr)) + ' hour and ' + str(int(remain_min)) + ' minutes'
                im.executeModality('TEXT_default', Remain_print)
                say(Remain_say, 'en')
                time.sleep(5)

            # update the info in the record
            RecordDict.update({"RemainingWaitTime" : remain_str})
            RecordDict.update({"ChangeinWaitTime" : 'has not'})


        # If the user wants to update its information Record
        elif UserQues == 'update':
            updateD = True
            while updateD == True:
                im.executeModality('TEXT_default', 'Which would you like to update?')
                say('Pick the item you would like to change.', 'en')

                im.executeModality('BUTTONS',[['emergency','Emergency Symptoms'], ['symptoms', 'Symptoms'], ['location', 'Location of Pain'], ['conscious', 'Level of Consciousness'], ['painlevel', 'Pain Level'], ['done', 'Done, exit.']])
                im.executeModality('ASR',['emergency', 'symptoms', 'location', 'conscious', 'painlevel', 'done'])
                HistQues = im.ask(actionname=None, timeoutvalue=10000)
                im.display.remove_buttons()

                if HistQues == 'done':
                    im.executeModality('TEXT_default', 'Thank you for checking your record.')
                    say('Goodbye!', 'en')
                    updateD = False

                elif HistQues == 'emergency':
                    im.executeModality('TEXT_default', 'Select again all that apply.')
                    emergDone = True
                    emer1 = 0
                    nextEm = False
                    nextEm2 = False
                    while emergDone == True:
                        if nextEm == False and nextEm2 == False:
                            im.executeModality('BUTTONS',[['bleeding','Bleeding that will not stop'],['breathing','Breathing problems'], ['unusual behavior', 'Unusual behavior, confusion, difficulty arousing'], ['chest pain', 'Chest pain'], ['choking', 'Choking'], ['coughing', 'Coughing up or vomiting blood'], ['severe vomiting', 'Severe or persistent vomiting'], ['fainting', 'Fainting or loss of consciousness'], \
                            ['next', 'See more options']])
                            im.executeModality('ASR',['bleeding', 'breathing', 'unusual behavior', 'chest pain', 'choking', 'coughing', 'severe vomiting', 'fainting', 'next'])
                        elif nextEm == True and nextEm2 == False:
                            im.executeModality('BUTTONS',[['serious injury', 'Serious injury due to: 1) vehicle accident, 2) burns/smoke inhalation, 3) near drowning'], ['deep wound', 'Deep or large wound'], ['sudden severe pain', 'Sudden, severe pain anywhere in the body'], ['next2', 'See more options']])
                            im.executeModality('ASR',['serious injury', 'deep wound', 'sudden severe pain', 'next2'])

                        elif nextEm == True and nextEm2 == True:
                            im.executeModality('BUTTONS',[ ['sudden dizziness', 'Sudden dizziness, weakness, or change in vision'], ['swallowing poisonous', 'Swallowing a poisonous substance'], ['severe abdominal', 'Severe abdominal pain or pressure'], ['head spine', 'Head or spine injury'], ['feeling suicide murder', 'Feeling of committing suicide or murder'], ['done', 'Done, exit.']])
                            im.executeModality('ASR',['sudden dizziness', 'swallowing poisonous', 'severe abdominal', 'head spine', 'feeling suicide murder', 'done'])


                        emergQ = im.ask(actionname=None, timeoutvalue=10000)
                        im.display.remove_buttons()

                        if not emergQ == 'done' and not emergQ == 'next' and not emergQ == 'next2':
                            say('Item added', 'en')
                            if emer1 == 0:
                                emerg2add = emergQ
                                emer1 += 1
                            else: emerg2add = emerg2add + '/' + emergQ
                            RecordDict.update({"EmergencySymptoms" : emerg2add}) # Update data in record
                            StrRecord = 'You picked: ' + RecordDict['EmergencySymptoms']
                            im.executeModality('TEXT_default', StrRecord)
                        elif emergQ == 'done': emergDone = False
                        elif emergQ == 'next': nextEm = True
                        elif emergQ == 'next2': nextEm2 = True

                elif HistQues == 'symptoms':
                    im.executeModality('TEXT_default', 'Select again all that apply.')
                    symDone = True
                    symp1 = 0
                    nextSy = False
                    while symDone == True:
                        if nextSy == False:
                            im.executeModality('BUTTONS',[['fever/chills','Fever/Chills'],['nausea/vomit','Nausea/Vomit'], ['limited movement', 'Limited movement/Stiffness'], ['loss sense(s)', 'Loss of one or more: Sight, Hearing, Touch'], ['cut', 'Cut/Scrape'], ['next', 'See more options']])
                            im.executeModality('ASR',['fever/chills', 'nausea/vomit', 'limited movement', 'loss sense(s)', 'cut', 'next'])

                        else:
                            im.executeModality('BUTTONS',[ ['pain', 'Pain'], ['infection', 'Infection'], ['inflammation', 'Swelling/inflammation'], ['dizzy', 'light-headed/dizzy'], ['recurring', 'One or more of these are Recurring'], ['done', 'Done, exit.']])
                            im.executeModality('ASR',['pain', 'infection', 'inflammation', 'dizzy', 'recurring', 'done'])


                        symQ = im.ask(actionname=None, timeoutvalue=10000)
                        im.display.remove_buttons()

                        if not symQ == 'done' and not symQ == 'next':
                            say('Item added', 'en')
                            if symp1 == 0:
                                sym2add = symQ
                                symp1 += 1
                            else: sym2add = sym2add + '/' + symQ
                            RecordDict.update({"Symptoms" : sym2add}) # Update data in record
                            StrRecord = 'You picked: ' + RecordDict['Symptoms']
                            im.executeModality('TEXT_default', StrRecord)
                        elif symQ == 'done': symDone = False
                        elif symQ == 'next': nextSy = True

                elif HistQues == 'location':
                    im.executeModality('TEXT_default', 'Select again all that apply.')
                    locDone = True
                    loc1 = 0
                    while locDone == True:
                        im.executeModality('BUTTONS',[ ['foot', 'Foot(x2)'], ['leg(s)', 'Leg(s)'], ['arm(s)', 'Arm(s)'], ['hand(s)', 'Hand(s)'], ['abdomen', 'Abdomen'], ['chest', 'Chest'], ['back', 'Back'], ['head/face', 'Head/Face'], ['done', 'Done, exit.']])
                        im.executeModality('ASR',['foot', 'leg(s)', 'arm(s)', 'hand(s)', 'abdomen', 'chest', 'back', 'head/face', 'done'])

                        locQ = im.ask(actionname=None, timeoutvalue=10000)
                        im.display.remove_buttons()

                        if not locQ == 'done':
                            say('Item added', 'en')
                            if loc1 == 0:
                                loc2add = locQ
                                loc1 += 1
                            else: loc2add = loc2add + '/' + locQ
                            RecordDict.update({"LocationofPain" : loc2add}) # Update data in record
                            StrRecord = 'You picked: ' + RecordDict['LocationofPain']
                            im.executeModality('TEXT_default', StrRecord)
                        elif locQ == 'done': locDone = False

                elif HistQues == 'conscious':
                    im.executeModality('TEXT_default', 'Select again all that apply.')
                    cons1 = 0
                    im.executeModality('BUTTONS',[ ['fully', 'Fully (awake, aware)'], ['medium', 'Medium (some confusion)'], ['barely', 'Barely (feeling of sleeping or fainting)'], ['none', 'Unconscious (fainted)']])
                    im.executeModality('ASR',['fully', 'medium', 'barely', 'none'])

                    consQ = im.ask(actionname=None, timeoutvalue=10000)
                    im.display.remove_buttons()

                    say(consQ, 'en')
                    if cons1 == 0:
                        cons2add = consQ
                        cons1 += 1
                    else: cons2add = cons2add + '/' + consQ
                    RecordDict.update({"LevelofConsciousness" : cons2add}) # Update data in record
                    StrRecord = 'Your consciousness level is: ' + RecordDict['LevelofConsciousness']
                    im.executeModality('TEXT_default', StrRecord)
                    time.sleep(3)

                elif HistQues == 'painlevel':
                    im.executeModality('TEXT_default', 'Select again all that apply.')
                    pain1 = 0
                    im.executeModality('BUTTONS',[ ['some', 'Some'], ['moderate', 'Moderate'], ['intense', 'Intense'], ['very intense', 'Very Intense'], ['excruciating', 'Excruciating']])
                    im.executeModality('ASR',['some', 'moderate', 'intense', 'very intense', 'abdomen', 'excruciating'])

                    painQ = im.ask(actionname=None, timeoutvalue=10000)
                    im.display.remove_buttons()

                    say(painQ, 'en')
                    if pain1 == 0:
                        pain2add = painQ
                        pain1 += 1
                    else: pain2add = pain2add + '/' + painQ
                    RecordDict.update({"PainLevel" : pain2add}) # Update data in record
                    StrRecord = 'Your pain level is: ' + RecordDict['PainLevel']
                    im.executeModality('TEXT_default', StrRecord)
                    time.sleep(3)

    stringDic = str(RecordDict)
    stringDic = stringDic.replace(', ','\n').replace("'","").replace('{','').replace('}','').replace(': u','=').replace(': ','=')

    recFile = open(os.path.join(directory, RecordTxt), "w")
    recFile.write(stringDic)
    recFile.close()

    end()

# Interaction to retrieve info for the user
def i3():
    begin()
    im.display.loadUrl('ERnewpatient.html')

    im.executeModality('TEXT_default', 'Please enter the digits of your ticket number one by one.')
    say('Please enter the ticket number given to you', 'en')

    # There are three digits in the ticket number, check one by one with buttons
    CorrTick = 'no'
    while CorrTick == 'no':
        # First number:
        im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
        im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
        Num1 = im.ask(actionname=None, timeoutvalue=1000)
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
            say('Great! Let us add your information to your record')
        elif CorrTick == 'no':
            im.executeModality('TEXT_default', 'Please enter again the digits of your ticket number one by one.')
            say('Sorry about that. Let us try again')


    im.executeModality('TEXT_title','Add information to your Patient Record')
    im.executeModality('TEXT_default', 'Please answer the following questions')
    say('Please enter the information being asked by pressing the corresponding buttons', 'en')
    RecordDict = dict()

    # Add name:
    im.executeModality('TEXT_default', 'Enter your FIRST and LAST name:')
    say('Enter your name', 'en')
    nameDone = True
    name1 = 0
    while nameDone == True:
        im.executeModality('BUTTONS',[ ['a', 'A'], ['b', 'B'], ['c', 'C'], ['d', 'D'], ['e', 'E'], ['f', 'F'], ['g', 'G'], ['h', 'H'], ['i', 'I'], ['j', 'J'], ['k', 'K'], ['l', 'L'], ['m', 'M'], ['n', 'N'], ['o', 'O'], ['p', 'P'], ['q', 'Q'], ['r', 'R'], ['s', 'S'], ['t', 'T'], ['u', 'U'], ['v', 'V'], ['w', 'W'], ['x', 'X'], ['y', 'Y'], ['z', 'Z'], ['Space', 'space'], ['back', 'backspace'], ['done', 'Done']])
        # im.executeModality('ASR',['foot', 'leg(s)', 'arm(s)', 'hand(s)', 'abdomen', 'chest', 'back', 'head/face', 'done'])

        nameQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if not nameQ == 'done':
            say(nameQ, 'en')
            if name1 == 0:
                name2add = nameQ
                name1 += 1
            elif name1 != 0 and nameQ != 'Space' and nameQ != 'back': name2add = name2add + nameQ
            elif nameQ == 'Space': name2add = name2add + ' '
            elif nameQ == 'back': name2add = name2add[:-1]

            RecordDict.update({"Name" : name2add}) # Update data in record
            StrRecord = 'Your name is: ' + RecordDict['Name']
            im.executeModality('TEXT_default', StrRecord)
        elif nameQ == 'done': nameDone = False

    # Add age:
    im.executeModality('TEXT_default', 'Enter your current age:')
    say('enter your age', 'en')
    ageDone = True
    age1 = 0
    while ageDone == True:
        im.executeModality('BUTTONS',[ ['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['back', 'backspace'], ['done', 'Done']])
        # im.executeModality('ASR',['foot', 'leg(s)', 'arm(s)', 'hand(s)', 'abdomen', 'chest', 'back', 'head/face', 'done'])

        ageQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if not ageQ == 'done':
            say(ageQ, 'en')
            if age1 == 0:
                age2add = ageQ
                age1 += 1
            elif age1 != 0 and ageQ != 'back': age2add = age2add + ageQ
            elif ageQ == 'back': age2add = age2add[:-1]

            RecordDict.update({"Age" : age2add}) # Update data in record
            StrRecord = 'Your age is: ' + RecordDict['Age']
            im.executeModality('TEXT_default', StrRecord)
        elif ageQ == 'done': ageDone = False

    # Add medical history:
    im.executeModality('TEXT_default', 'Enter your past medical history:')
    say('enter your history', 'en')
    histDone = True
    hist1 = 0
    while histDone == True:
        im.executeModality('BUTTONS',[['overweight or obese','Overweight or Obese'],['smoke cigarettes','Smoke Cigarettes'], ['high cholesterol', 'High Cholesterol'], ['hypertension', 'Hypertension'], ['diabetes', 'Diabetes'], ['recurring symptoms', 'Current Symptoms Recurring'], ['none', 'None'], ['remove', 'Remove last item'], ['done', 'Done']])
        # im.executeModality('ASR',['overweight or obese','smoke cigarettes', 'high cholesterol', 'hypertension', 'diabetes', 'current symptoms recurring', 'done'])
        histQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if not histQ == 'done':
            say(histQ, 'en')
            if hist1 == 0 and histQ != 'remove':
                hist2add = histQ
                hist1 += 1
            elif hist1 != 0 and histQ != 'remove': hist2add = hist2add + '/' + histQ
            elif histQ == 'remove':
                if '/' in hist2add: hist2add = hist2add.rpartition('/')[0]
                else:
                    hist2add = ''
                    hist1 = 0

            RecordDict.update({"PastMedicalHistory" : hist2add}) # Update data in record
            StrRecord = 'Your past history is: ' + RecordDict['PastMedicalHistory']
            im.executeModality('TEXT_default', StrRecord)
        elif histQ == 'done' and hist2add: histDone = False

    # Add emergency symptoms:
    im.executeModality('TEXT_default', 'Enter any symptoms categorized as higher emergency:')
    say('enter your emergency symptoms', 'en')
    emergDone = True
    emer1 = 0
    nextEm = False
    nextEm2 = False
    while emergDone == True:
        if nextEm == False and nextEm2 == False:
            im.executeModality('BUTTONS',[['bleeding','Bleeding that will not stop'],['breathing','Breathing problems'], ['unusual behavior', 'Unusual behavior, confusion, difficulty arousing'], ['chest pain', 'Chest pain'], ['choking', 'Choking'], ['coughing', 'Coughing up or vomiting blood'], ['severe vomiting', 'Severe or persistent vomiting'], ['fainting', 'Fainting or loss of consciousness'], \
            ['remove', 'Remove last item'], ['next', 'See more options']])
            im.executeModality('ASR',['bleeding', 'breathing', 'unusual behavior', 'chest pain', 'choking', 'coughing', 'severe vomiting', 'fainting', 'next'])
        elif nextEm == True and nextEm2 == False:
            im.executeModality('BUTTONS',[['serious injury', 'Serious injury due to: 1) vehicle accident, 2) burns/smoke inhalation, 3) near drowning'], ['deep wound', 'Deep or large wound'], ['sudden severe pain', 'Sudden, severe pain anywhere in the body'], ['remove', 'Remove last item'], ['next2', 'See more options']])
            im.executeModality('ASR',['serious injury', 'deep wound', 'sudden severe pain', 'next2'])

        elif nextEm == True and nextEm2 == True:
            im.executeModality('BUTTONS',[ ['sudden dizziness', 'Sudden dizziness, weakness, or change in vision'], ['swallowing poisonous', 'Swallowing a poisonous substance'], ['severe abdominal', 'Severe abdominal pain or pressure'], ['head spine', 'Head or spine injury'], ['feeling suicide murder', 'Feeling of committing suicide or murder'], ['none', 'None'], ['remove', 'Remove last item'], ['done', 'Done']])
            im.executeModality('ASR',['sudden dizziness', 'swallowing poisonous', 'severe abdominal', 'head spine', 'feeling suicide murder', 'done'])


        emergQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if not emergQ == 'done' and emergQ != 'next' and emergQ != 'next2':
            say(emergQ, 'en')
            if emer1 == 0 and emergQ != 'remove':
                emerg2add = emergQ
                emer1 += 1
            elif emer1 != 0 and emergQ != 'remove': emerg2add = emerg2add + '/' + emergQ
            elif emergQ == 'remove':
                if '/' in emerg2add: emerg2add = emerg2add.rpartition('/')[0]
                else:
                    emerg2add = ''
                    emer1 = 0

            RecordDict.update({"EmergencySymptoms" : emerg2add}) # Update data in record
            StrRecord = 'Your emergency symptoms are: ' + RecordDict['EmergencySymptoms']
            im.executeModality('TEXT_default', StrRecord)
        elif emergQ == 'done' and emerg2add: emergDone = False
        elif emergQ == 'next': nextEm = True
        elif emergQ == 'next2': nextEm2 = True

    # Add symptoms:
    im.executeModality('TEXT_default', 'Enter your symptoms:')
    say('enter your symptoms', 'en')
    symDone = True
    symp1 = 0
    nextSy = False
    while symDone == True:
        if nextSy == False:
            im.executeModality('BUTTONS',[['fever or chills','Fever/Chills'],['nausea or vomit','Nausea/Vomit'], ['limited movement', 'Limited movement/Stiffness'], ['loss senses', 'Loss of one or more: Sight, Hearing, Touch'], ['cut', 'Cut/Scrape'], ['remove', 'Remove last item'], ['next', 'See more options']])
            im.executeModality('ASR',['fever/chills', 'nausea/vomit', 'limited movement', 'loss sense(s)', 'cut', 'next'])

        else:
            im.executeModality('BUTTONS',[ ['pain', 'Pain'], ['infection', 'Infection'], ['inflammation', 'Swelling/inflammation'], ['dizzy', 'light-headed/dizzy'], ['recurring', 'One or more of these are Recurring'], ['none', 'None'], ['remove', 'Remove last item'], ['done', 'Done']])
            im.executeModality('ASR',['pain', 'infection', 'inflammation', 'dizzy', 'recurring', 'done'])


        symQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if not symQ == 'done' and symQ != 'next':
            say(symQ, 'en')
            if symp1 == 0 and symQ != 'remove':
                sym2add = symQ
                symp1 += 1
            elif symp1 != 0 and symQ != 'remove': sym2add = sym2add + '/' + symQ
            elif symQ == 'remove':
                if '/' in sym2add: sym2add = sym2add.rpartition('/')[0]
                else:
                    sym2add = ''
                    symp1 = 0

            RecordDict.update({"Symptoms" : sym2add}) # Update data in record
            StrRecord = 'Your symptoms are: ' + RecordDict['Symptoms']
            im.executeModality('TEXT_default', StrRecord)
        elif symQ == 'done' and sym2add: symDone = False
        elif symQ == 'next': nextSy = True

    # Add location of pain:
    im.executeModality('TEXT_default', 'Enter the location of your pain(s):')
    say('enter your pain locations', 'en')
    locDone = True
    loc1 = 0
    while locDone == True:
        im.executeModality('BUTTONS',[ ['foot', 'Foot(x2)'], ['legs', 'Leg(s)'], ['arms', 'Arm(s)'], ['hands', 'Hand(s)'], ['abdomen', 'Abdomen'], ['chest', 'Chest'], ['back', 'Back'], ['head', 'Head/Face'], ['remove', 'Remove last item'], ['done', 'Done']])
        im.executeModality('ASR',['foot', 'leg(s)', 'arm(s)', 'hand(s)', 'abdomen', 'chest', 'back', 'head/face', 'done'])

        locQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if not locQ == 'done':
            say(locQ, 'en')
            if loc1 == 0 and locQ != 'remove':
                loc2add = locQ
                loc1 += 1
            elif loc1 != 0 and locQ != 'remove': loc2add = loc2add + '/' + locQ
            elif locQ == 'remove':
                if '/' in loc2add: loc2add = loc2add.rpartition('/')[0]
                else:
                    loc2add = ''
                    loc1 = 0

            RecordDict.update({"LocationofPain" : loc2add}) # Update data in record
            StrRecord = 'Your pain location are: ' + RecordDict['LocationofPain']
            im.executeModality('TEXT_default', StrRecord)
        elif locQ == 'done' and loc2add: locDone = False

    # Add level of consciousness:
    im.executeModality('TEXT_default', 'Pick ONE of your level of consciousness:')
    say('enter one of your level of consciousness', 'en')
    consDone = True
    while consDone == True:
        im.executeModality('BUTTONS',[ ['fully', 'Fully (awake, aware)'], ['medium', 'Medium (some confusion)'], ['barely', 'Barely (feeling of sleeping or fainting)'], ['unconscious', 'Unconscious (fainted)'], ['confirm', 'Confirm']])
        im.executeModality('ASR',['fully', 'medium', 'barely', 'none'])

        consQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if consQ != 'confirm':
            say(consQ, 'en')
            cons2add = consQ
            RecordDict.update({"LevelofConsciousness" : cons2add}) # Update data in record
            StrRecord = 'Your consciousness level is: ' + RecordDict['LevelofConsciousness']
            im.executeModality('TEXT_default', StrRecord)
        else: consDone = False

    # Add pain lavel:
    im.executeModality('TEXT_default', 'Pick ONE to describe your pain level:')
    say('pick one of your pain level', 'en')
    painDone = True
    while painDone == True:
        im.executeModality('BUTTONS',[ ['some', 'Some'], ['moderate', 'Moderate'], ['intense', 'Intense'], ['very intense', 'Very Intense'], ['excruciating', 'Excruciating'], ['confirm', 'Confirm']])
        im.executeModality('ASR',['some', 'moderate', 'intense', 'very intense', 'abdomen', 'excruciating'])

        painQ = im.ask(actionname=None, timeoutvalue=100000)
        im.display.remove_buttons()

        if painQ != 'confirm':
            say(painQ, 'en')
            pain2add = painQ
            RecordDict.update({"PainLevel" : pain2add}) # Update data in record
            StrRecord = 'Your pain level is: ' + RecordDict['PainLevel']
            im.executeModality('TEXT_default', StrRecord)
        else: painDone = False

    # Add time admitted:
    curr_sec = time.time()
    loc_time = time.localtime(curr_sec)
    curr_date = ((time.ctime(curr_sec)).split(':')[0])[:-3]
    curr_time = str(loc_time.tm_hour) + 'h ' + str(loc_time.tm_min) + 'm'
    RecordDict.update({"TimeAdmitted" : curr_sec}) # Update data in record
    StrRecord = 'Your date admitted is: ' + curr_date + ', ' + str(loc_time.tm_year)
    im.executeModality('TEXT_default', StrRecord)
    say(StrRecord, 'en')
    time.sleep(2)
    StrRecord = 'Your time admitted is: ' + curr_time
    im.executeModality('TEXT_default', StrRecord)
    say(StrRecord, 'en')
    time.sleep(2)


    # Add info about urgency level and wait time for the patient

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

    totalPoints = agePoints + histPoints + emergPoints + symPoints + locPoints + conscPoints
    RecordDict.update({"UrgencyLevel" : str(totalPoints)}) # Update data in record

    StrRecord = 'Your total urgency score is: ' + str(totalPoints)
    im.executeModality('TEXT_default', StrRecord)
    say(StrRecord, 'en')
    time.sleep(2)

    stringDic = str(RecordDict)
    stringDic = stringDic.replace(', ','\n').replace("'","").replace('{','').replace('}','').replace(': u','=').replace(': ','=')

    # Check the tickets in the system
    directory = "/home/ubuntu/playground/HumanRobotInteraction_ER/patientInfo"
    RecordTxt = ticketNumber + ".txt"
    recFile = open(os.path.join(directory, RecordTxt), "w+")
    recFile.write(stringDic)
    recFile.close()

    im.executeModality('TEXT_default', 'Your record has been saved in the database')
    say('Thank you for adding the information. Please now wait for your turn', 'en')



    end()



mc.setDemoPath('/home/ubuntu/playground/HumanRobotInteraction_ER')
mc.store_interaction(i2)
mc.store_interaction(i1)
mc.store_interaction(i0)
mc.store_interaction(i3)
mc.run_interaction(i1)
# mc.run_interaction(i0)


# mc.store_interaction(f)
# mc.run_interaction(i3)
