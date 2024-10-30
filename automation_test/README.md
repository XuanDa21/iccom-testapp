# For now, this automation test does not support log checking, it only executes commands.

# To run this automation test, go to the config.py file and modify the following variables:
- SOC: Choose your board's name.
- SERIAL_PORT: Specify the port you are using.
- Board_NO: the board number.

# Before running, set execute permissions for SERIAL_PORT
- Example: chmod 777 /dev/ttyUSB3
 
# Example command to run
- To see the defined test cases, refer to the testcase.py file to check which test case you are running
- Run a single test case: Python3 _index.py 1
- Run multiple test cases: 
    + Python3 _index.py 1:2
    + Python3 _index.py 1 2 3
- Clean the logs and pyc file: Python3 clean.py