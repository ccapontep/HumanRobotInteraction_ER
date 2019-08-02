import os, sys

pdir = os.getenv('PNP_HOME')
sys.path.insert(0, pdir+'/PNPnaoqi/py')

import pnp_cmd_naoqi
from pnp_cmd_naoqi import *

def checkConditions(p):

    p.set_condition('mycondition', True)
    



# Start action server
if __name__ == "__main__":

    p = PNPCmd()

    p.begin()

    checkConditions(p)

    # sequence
    p.exec_action('say', 'hello')     # blocking
    p.exec_action('say', 'Good_morning')     # blocking
    p.exec_action('wait', '2')  # blocking 

    # interrupt
    p.exec_action('wait', '5', interrupt='timeout_2.5', recovery='wait_3;skip_action')  # blocking

    p.exec_action('wait', '5', interrupt='mycondition', recovery='wait_3;skip_action')  # blocking

    # concurrency
    p.start_action('wait', '2') # non-blocking
    p.start_action('wait', '5') # non-blocking

    status = 'run'
    while status == 'run':
        status = p.action_status('wait')
        print(status)
        time.sleep(0.5)

    p.interrupt_action('wait')

    p.end()

