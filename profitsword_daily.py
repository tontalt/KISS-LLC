#====================================================================
# 
# Code to pull the ProfitSword API Dailies
# 
#====================================================================

import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from profitsword import *
import sys

SCRIPT_NAME = "ProfitSword_Daily"

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
    start_date += relativedelta(days=-1)
    end_date = start_date
    asof_date = None

#DEBUG
#start_date = datetime.strptime("1/1/2020", '%m/%d/%Y')
#end_date = datetime.strptime("1/31/2020", '%m/%d/%Y')
#asof_date= None

retval = pull_daily(data_set_id=-3, start_date=start_date, end_date=end_date, asof_date=asof_date)   # Actuals

msgs.append("End " + SCRIPT_NAME + ": " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
