import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')

from ws_client import *
import ws_client

cmdsever_ip = '10.3.1.1'
cmdserver_port = 9101

mc = ModimWSClient()
mc.setCmdServerAddr(cmdsever_ip, cmdserver_port)

# def f():
#     return 1

def i1():
    # im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    # im.gitpull()
    im.display.loadUrl('HRIER/ERslide.html')

    im.executeModality('TEXT_title','Welcome to Wellness Hospital!')
    im.executeModality('TEXT_default','Hello!')
    im.executeModality('TTS','Welcome')
    # im.executeModality('IMAGE','images/hri2.jpg')

    im.display.remove_buttons()
    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
    im.executeModality('ASR',['yes','no'])

    a = im.ask(actionname=None, timeoutvalue=10)
    im.executeModality('TEXT_default',a)

    time.sleep(3)

    im.display.loadUrl('ERindex.html')


def i2():
    # im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    im.display.loadUrl('slide.html')
    im.execute('ciao')
    time.sleep(3)
    im.display.loadUrl('index.html')


def i3():
    # im.setDemoPath("/home/ubuntu/playground/HumanRobotInteraction_ER")
    im.display.loadUrl('slide.html')
    im.askUntilCorrect('question')
    time.sleep(3)
    im.display.loadUrl('index.html')
    f()

mc.setDemoPath('/home/ubuntu/playground/HumanRobotInteraction_ER')
mc.run_interaction(i1)
# mc.store_interaction(f)
# mc.run_interaction(i3)
