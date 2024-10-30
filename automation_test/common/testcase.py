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
    1: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_1_{formatted_date}',
    2: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_2_{formatted_date}',
    3: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_3_{formatted_date}',
    4: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_4_{formatted_date}',
    5: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_5_{formatted_date}',
    6: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_6_{formatted_date}',
    7: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Normal_7_{formatted_date}', 
    
    # Abnormal  
    8: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_1_{formatted_date}',  
    9: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_2_{formatted_date}',  
    10: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_3_{formatted_date}',  
    11: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_4_{formatted_date}',  
    12: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_5_{formatted_date}',  
    13: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_6_{formatted_date}',
    14: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Abnormal_7_{formatted_date}', 
    
    # Boundary
    15: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Boundary_1_{formatted_date}',
    16: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_Boundary_2_{formatted_date}',
    
    # System Evaluation
    17: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_SystemEvaluation_1_{formatted_date}',
    18: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_SystemEvaluation_2_{formatted_date}',    
    19: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_SystemEvaluation_3_{formatted_date}',
    20: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_SystemEvaluation_4_{formatted_date}',
    21: f'BSPv5.3.5_ICCOM_{config.SOC}_{board_NO}_SystemEvaluation_5_{formatted_date}',
}

