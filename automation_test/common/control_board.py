#!/usr/bin/python
from time import sleep
import config
import subprocess

def restart():
    subprocess.call("sshpass -p \"raspberry\" ssh -o StrictHostKeyChecking=no pi@{} \
                     \"python3 ~/01_featbox_software/auto_ctrl.py {} off; \
                       python3 ~/01_featbox_software/auto_ctrl.py {} on;  \
                       python3 ~/01_featbox_software/auto_ctrl.py {} boot\"  2>&1 > /dev/null".format(config.PI_IPADDR,config.PI_NUM,config.PI_NUM,config.PI_NUM))
    sleep(0.5)

def restart_2():
    subprocess.call("sshpass -p \"raspberry\" ssh -o StrictHostKeyChecking=no pi@{} \
                      \"python3 ~/01_featbox_software/auto_ctrl.py {} reset;  \
		        python3 ~/01_featbox_software/auto_ctrl.py {} boot > /dev/null\" 2>&1 > /dev/null".format(config.PI_IPADDR,config.PI_NUM,config.PI_NUM),shell=True)
    sleep(0.5)
