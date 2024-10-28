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
    # Normal
    1:'BSPv5.3.4_ICCOM_{}_{}_Normal_1_{}'.format(config.SOC,board_NO, formatted_date),
    2:'BSPv5.3.4_ICCOM_{}_{}_Normal_2_{}'.format(config.SOC,board_NO, formatted_date),
    3:'BSPv5.3.4_ICCOM_{}_{}_Normal_3_{}'.format(config.SOC,board_NO, formatted_date),
    4:'BSPv5.3.4_ICCOM_{}_{}_Normal_4_{}'.format(config.SOC,board_NO, formatted_date),
    5:'BSPv5.3.4_ICCOM_{}_{}_Normal_5_{}'.format(config.SOC,board_NO, formatted_date),
    6:'BSPv5.3.4_ICCOM_{}_{}_Normal_6_{}'.format(config.SOC,board_NO, formatted_date),
    7:'BSPv5.3.4_ICCOM_{}_{}_Normal_7_{}'.format(config.SOC,board_NO, formatted_date), 
    
    # Abnormal  
    8:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_1_{}'.format(config.SOC,board_NO, formatted_date),  
    9:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_2_{}'.format(config.SOC,board_NO, formatted_date),  
    10:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_3_{}'.format(config.SOC,board_NO, formatted_date),  
    11:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_4_{}'.format(config.SOC,board_NO, formatted_date),  
    12:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_5_{}'.format(config.SOC,board_NO, formatted_date),  
    13:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_6_{}'.format(config.SOC,board_NO, formatted_date),
    14:'BSPv5.3.4_ICCOM_{}_{}_Abnormal_7_{}'.format(config.SOC,board_NO, formatted_date), 
    
    # Boundary
    15:'BSPv5.3.4_ICCOM_{}_{}_Boundary_1_{}'.format(config.SOC,board_NO, formatted_date),
    16:'BSPv5.3.4_ICCOM_{}_{}_Boundary_2_{}'.format(config.SOC,board_NO, formatted_date),
    
    # System Evaluation
    17:'BSPv5.3.4_ICCOM_{}_{}_SystemEvaluation_1_{}'.format(config.SOC,board_NO, formatted_date),
    18:'BSPv5.3.4_ICCOM_{}_{}_SystemEvaluation_2_{}'.format(config.SOC,board_NO, formatted_date),    
    19:'BSPv5.3.4_ICCOM_{}_{}_SystemEvaluation_3_{}'.format(config.SOC,board_NO, formatted_date),
    20:'BSPv5.3.4_ICCOM_{}_{}_SystemEvaluation_4_{}'.format(config.SOC,board_NO, formatted_date),
    21:'BSPv5.3.4_ICCOM_{}_{}_SystemEvaluation_5_{}'.format(config.SOC,board_NO, formatted_date),
}
