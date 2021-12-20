#====================================================================
# 
# Code to cleanup the logfiles created by all the python scripts
#
#====================================================================

from hvmg_lib import *
import sys
import os
import datetime
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

SCRIPT_NAME = "HVMG_Logfile_Cleanup"

current_date = datetime.today()
target_date = current_date + relativedelta(months=-3)

print(SCRIPT_NAME)
print("CurrentDate=" + current_date.strftime('%Y%m%d'))
print("TargetDate=" + target_date.strftime('%Y%m%d'))

file_cnt = 0

for file in os.listdir(LOGFILE_FOLDER):
    filespec = LOGFILE_FOLDER + file
    if os.path.isfile(filespec):
        create_date = datetime.fromtimestamp(os.path.getctime(filespec))
        if create_date <= target_date:
            print("Got one: " + file + " Created: " + create_date.strftime('%Y%m%d') + " Target: " + target_date.strftime('%Y%m%d'))
            os.remove(filespec) # delete the file
            file_cnt += 1
        else:
            print("Not one: " + file + " Created: " + create_date.strftime('%Y%m%d') + " Target: " + target_date.strftime('%Y%m%d'))

print(SCRIPT_NAME + ": Files Deleted=" + str(file_cnt))
exit(0)


   