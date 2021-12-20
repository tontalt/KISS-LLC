#====================================================================
# 
# Code to pull the ProfitSword Weeklies
# 
#====================================================================

import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from profitsword import *
import sys
import json

SCRIPT_NAME = "ProfitSword_SalesPace"

start_time = datetime.now()

msgs = get_message_list()
msgs.append("Begin " + SCRIPT_NAME + ": " + str(start_time))

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
    end_date = start_date + relativedelta(years=1)
    start_date += relativedelta(days=-1)
    asof_date = start_date

err_cnt = 0

#DEBUG
#start_date = datetime.strptime('1/1/2021', '%m/%d/%Y')
#end_date = datetime.strptime('12/31/2021', '%m/%d/%Y')
#asof_date = datetime.strptime('1/1/2021', '%m/%d/%Y')


pull_time = datetime.now()
msgs.append("DataSet=SalesPaceEvents: " + str(pull_time))
print("DataSet=Events")
if pull_sales_pace_events(start_date=start_date, end_date=end_date, asof_date=asof_date) == False:
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

pull_time = datetime.now()
msgs.append("DataSet=SalesPaceRooms: " + str(pull_time))
print("DataSet=Rooms")
if pull_sales_pace_rooms(start_date=start_date, end_date=end_date, asof_date=asof_date) == False:
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

pull_time = datetime.now()
msgs.append("DataSet=SalesPaceTransient: " + str(pull_time))
print("DataSet=Transient")
if pull_sales_pace_transient(start_date=start_date, end_date=end_date, asof_date=asof_date) == False:
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

msgs.append("End " + SCRIPT_NAME + ": " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
