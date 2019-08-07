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

def i1():

    # im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    # im.gitpull()
    begin()
    im.display.loadUrl('HRIER/ERslide.html')

    im.executeModality('TEXT_title','Welcome to Wellness Hospital!')
    say('Welcome to Wellness Hospital', 'en')
    im.executeModality('TEXT_default','Have you been helped previously?')
    say('Have you been helped previously?','en')

    im.display.remove_buttons()
    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
    im.executeModality('ASR',['yes','no'])

    a = im.ask(actionname=None, timeoutvalue=10)

    # run = True
    #
    # while run:
    # aa = asr()
    say('the answer given is '+a)

    # if ('yes' in aa) or a == 'yes':
    if a == 'yes':
        im.executeModality('TEXT_default','You are a patient in the database.')
        say('Welcome back')
        time.sleep(2)
        i2()

    # elif ('no' in aa) or a == 'no':
    elif a == 'no':
        im.executeModality('TEXT_default','I am a new patient.')
        say('Welcome to Wellness Hospital. My name is Marrtino and I will help you setup your emergency in the database', 'en')
        say('I will be asking some questions about your emergency and have you see a doctor as soon as possible, depending on the severity of your emergency', 'en')
        say('I will also be doing routine checks to let you know your remaining wait time. If at any point you have questions, come ask', 'en')
        say('We will take care of you. Thank you for visiting us.', 'en')
        time.sleep(3)
    # elif ('' in aa):
    elif ('' in a):
        im.executeModality('TEXT_default','No answer received')
        time.sleep(3)

    end()



def i2():
    begin()

    im.display.loadUrl('ERindex.html')
    im.executeModality('TEXT_default', 'Please enter the digits of your ticket number one by one.')
    say('Let me look for you in the database. Please enter your ticket number', 'en')

    # There are three digits in the ticket number, check one by one with buttons
    # First number:
    im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
    im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
    Num1 = im.ask(actionname=None, timeoutvalue=10)
    say('number '+Num1)

    # Second number:
    im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
    im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
    Num2 = im.ask(actionname=None, timeoutvalue=10)
    say('number'+Num2)

    # Second number:
    im.executeModality('BUTTONS',[['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9']])
    im.executeModality('ASR',['0','1','2', '3', '4', '5', '6', '7', '8', '9'])
    Num3 = im.ask(actionname=None, timeoutvalue=10)
    say('number'+Num3)

    ticketNumber = str(int(Num1)*100 + int(Num2)*10 + int(Num3))
    say('Your ticket number is '+ticketNumber)


    import os
    import numpy as np

    directory = "/home/ubuntu/playground/HumanRobotInteraction_ER/patientInfo"

    ticketNums = []
    with open(os.path.join(directory, "PatientTicketNum.txt"), "r") as patientTicketNums:
        for ticket in patientTicketNums.readlines():
            ticketNums.append(str(ticket))
            # say('the ticket number is '+str(ticket), 'en')

    # say('Have you been helped previously?','en')
    # im.executeModality('ASR',['yes','no'])

    # im.display.loadUrl('slide.html')
    # im.execute('ciao')
    # time.sleep(3)
    # im.display.loadUrl('index.html')


def i3():
    # im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    im.display.loadUrl('slide.html')
    im.askUntilCorrect('question')
    time.sleep(3)
    im.display.loadUrl('index.html')
    f()

mc.setDemoPath('/home/ubuntu/playground/HumanRobotInteraction_ER')
mc.store_interaction(i2)
mc.run_interaction(i1)


# mc.store_interaction(f)
# mc.run_interaction(i3)
