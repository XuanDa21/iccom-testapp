#!/usr/bin/python3
from time import sleep

#--------- UKV config ------------#
MODULE_TEST="ICCOM"
SOC="M3v3.0"
SERIAL_PORT="/dev/ttyUSB0"
board_NO = "7030"
PLATFORM = ""
if SOC == "E3v1.1":
    NUM_CPU=2
    PLATFORM="ebisu"
elif SOC.find("H3v3.0") != -1:
    NUM_CPU=8
    PLATFORM="salvator-x"
elif SOC.find("M3Nv1.1") != -1:
    NUM_CPU=2
    PLATFORM="salvator-x"    
elif SOC.find("M3v3.0") != -1:
    NUM_CPU=6
    PLATFORM="salvator-x"
elif SOC.find("M3v1.2") != -1:
    NUM_CPU=6
    PLATFORM="salvator-x"

FEATBOX=True
FEATBOX=False
PI_IPADDR="192.168.10.174"
PI_NUM="0x15"


PASS_MEG="#### Result: OK ####"
FAIL_MEG="#### Result: NG ####"
SKIP_MEG="#### Result: SKIP ####"

RESTART_IF_FAILED=False

BASH_TESTDIR_PATH="~/board-salvator/"

