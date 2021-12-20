#====================================================================
# 
# Code to pull the ProfitSword Monthlies
# 
#====================================================================

import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from profitsword import *
import sys

SCRIPT_NAME = "ProfitSword_Monthly"

start_time = datetime.now()

msgs = get_message_list()
msgs.append("Begin " + SCRIPT_NAME + ": " + str(start_time))

#-------------------------------------------
# get cmd line params, if any

if len(sys.argv) > 1:
    try:
        dict = parse_cmd_line(sys.argv)
        start_date = datetime.strptime(dict["StartDate"], '%m/%d/%Y')
        end_date = datetime.strptime(dict["EndDate"], '%m/%d/%Y')    
        asof_date = datetime.strptime(dict["AsOfDate"], '%m/%d/%Y')    
    except:
        abort_script(msgs, SCRIPT_NAME, "Invalid date passed as param: " + str(sys.argv))
        exit(1)
else:
    start_date = datetime.today()
    end_date = datetime.strptime('12/31/' + str(start_time.year), '%m/%d/%Y')
    asof_date = datetime.strptime(str(start_time.month) + "/1/" + str(start_time.year), '%m/%d/%Y')

err_cnt = 0

#-------------------------------------------
# pull the Forecast (data_set=1) data

#DEBUG
#start_date = datetime(2021, 1, 1)
#end_date   = datetime(2021, 12, 31)
#asof_date  = start_date
#start_date = datetime.strptime('11/1/2021', '%m/%d/%Y')

start_date = datetime.strptime(str(start_time.month) + "/1/" + str(start_time.year), '%m/%d/%Y')
pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(1) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(1))
if pull_monthly(data_set_id=1, ext_data_set_id=1000, start_date=start_date, end_date=end_date, asof_date=asof_date) == False: # 1st day of month-1
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

#-------------------------------------------
# pull the Budget (data_set=2) data

#DEBUG
#start_date = datetime.strptime('1/1/2021', '%m/%d/%Y')
#end_date = datetime.strptime('12/31/2021', '%m/%d/%Y')
#asof_date = datetime.strptime('11/1/2021', '%m/%d/%Y')

start_date = datetime.strptime('1/1/' + str(start_time.year), '%m/%d/%Y')
pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(2) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(2))
if pull_monthly(data_set_id=2, ext_data_set_id=2, start_date=start_date, end_date=end_date, asof_date=asof_date) == False:   # Budget
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

#-------------------------------------------
# all done

msgs.append("End " + SCRIPT_NAME + ": Number of DataSets with Errors=" + str(err_cnt) + ", elapsed= " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)