#!/usr/bin/python
from time import sleep
import sys
import os
sys.path.append(os.path.relpath('common/'))
import conserial
import print_result
import config
import restart_board

if __name__ == '__main__':
    a=conserial.serial_thread(config.SERIAL_PORT,1, config.MODULE_TEST)
    a.start()
    a.send("modprobe iccom")
    a.send("echo scan  > /sys/kernel/debug/kmemleak")
    a.send("echo clear > /sys/kernel/debug/kmemleak")
    for i in range(8):
        a.send(" iccom-test -s 2048 -n 1000 -c {}".format(i))
    a.send("echo scan > /sys/kernel/debug/kmemleak")
    a.send("cat /sys/kernel/debug/kmemleak")
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
