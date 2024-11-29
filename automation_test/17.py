#!/usr/bin/python3
from time import sleep
import sys
import os
sys.path.append(os.path.relpath('common/'))
from conserial import SerialThread
import print_result
import config
import restart_board
commands = (
    "iccom-test -c 0 -s 2048 -m 120 & "
    "iccom-test -c 1 -s 2048 -m 120 & "
    "iccom-test -c 2 -s 2048 -m 120 & "
    "iccom-test -c 3 -s 2048 -m 120 & "
    "iccom-test -c 4 -s 2048 -m 120 & "
    "iccom-test -c 5 -s 2048 -m 120 & "
    "iccom-test -c 6 -s 2048 -m 120 & "
    "iccom-test -c 7 -s 2048 -m 120 & "
)

if __name__ == '__main__':
    a=SerialThread(config.SERIAL_PORT,1, config.MODULE_TEST)
    a.start()
    print_result.print_item(a,1,"SystemEvaluation")
    restart_board.execute(a)
    a.send("modprobe iccom")
    a.send(commands, 0.001, False)
    a.send("\x03")
    sleep(0.01)
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
