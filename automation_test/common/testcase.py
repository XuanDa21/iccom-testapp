#!/usr/bin/python
import sys
import datetime
import os
from datetime import datetime
sys.path.append(os.path.relpath('common/'))
import config

current_date = datetime.now().strftime("%d%m%y")
formatted_date = datetime.now().strftime("%Y%m%d")
board_NO = config.board_NO

start_time = datetime.now()
list_TC = {
    1:'BSPv5.3.4_ICCOM_{}_{}_Normal_1_{}'.format(config.SOC,board_NO, formatted_date),
    2:'BSPv5.3.4_ICCOM_{}_{}_Normal_2_{}'.format(config.SOC,board_NO, formatted_date),     
}
