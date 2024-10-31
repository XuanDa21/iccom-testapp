#!/usr/bin/python3
MODULE_TEST="ICCOM"
SOC="M3v3.0"
SERIAL_PORT="/dev/ttyUSB0"
board_NO = "7030"
PLATFORM = ""
if SOC == "E3v1.1":
    PLATFORM="ebisu"
elif SOC.find("H3v3.0") != -1:
    PLATFORM="salvator-x"
elif SOC.find("M3Nv1.1") != -1:
    PLATFORM="salvator-x"    
elif SOC.find("M3v3.0") != -1:
    PLATFORM="salvator-x"
elif SOC.find("M3v1.2") != -1:
    PLATFORM="salvator-x"

FEATBOX=True
FEATBOX=False
PI_IPADDR="xxx"
PI_NUM="xxx"


PASS_MEG="#### Result: OK ####"
FAIL_MEG="#### Result: NG ####"
SKIP_MEG="#### Result: SKIP ####"

RESTART_IF_FAILED=False

BASH_TESTDIR_PATH="~/board-salvator/"

