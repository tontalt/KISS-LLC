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

SCRIPT_NAME = "ProfitSword_Historical"
CONFIG_FILE = ".\\profitsword_historical.json"

start_time = datetime.now()

if len(sys.argv) > 1:
    try:
        #start_date = datetime.strptime(sys.argv[1], '%m/%d/%Y')
        dict = parse_cmd_line(sys.argv)
        start_date = datetime.strptime(dict["StartDate"], '%m/%d/%Y')
        end_date = datetime.strptime(dict["EndDate"], '%m/%d/%Y')
        asof_date = datetime.strptime(dict["AsOfDate"], '%m/%d/%Y')
    except:
        send_status_email(False, SCRIPT_NAME, "Invalid date passed as param: " + str(sys.argv))
        exit(1)
else:
    with open(CONFIG_FILE) as cfgfile:
        json_data = json.load(cfgfile)
    start_date = json_data['LastRunDate']
    if  start_date == None or len(start_date) == 0:
        send_status_email(False, SCRIPT_NAME, "No StartDate provided, aborting")
        exit()    
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    start_date = datetime(start_date.year, start_date.month, 1)
    start_date += relativedelta(months=1)
    asof_date = None

msgs = get_message_list()

msgs.append("Begin " + SCRIPT_NAME + ": " + str(start_time))

#saved_start_date = start_date # need this for the json file write at the end

mm = start_date.month
yy = start_date.year

# do every day of month, when month changes were done
#while start_date.month == mm:
while start_date.year == yy:
    # DEBUG
    print("Pulling for " + str(start_date))

    retval = pull_daily(data_set_id=-3, start_date=start_date, end_date=start_date, asof_date=asof_date)   # Actuals

    start_date += relativedelta(days=1)
# end while

# update the config file
#json_data['LastRunDate'] = saved_start_date.strftime('%d/%m/%Y')
#with open(CONFIG_FILE, "wt") as cfgfile:
#    json.dump(json_data, fp=cfgfile)

msgs.append("End " + SCRIPT_NAME + ": " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
