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

SCRIPT_NAME = "ProfitSword_Weekly"
CONFIG_FILE = ".\\profitsword_weekly.json"

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
"""
else:
    with open(CONFIG_FILE) as cfgfile:
        json_data = json.load(cfgfile)
    start_date = json_data['LastRunDate']
    if  start_date == None or len(start_date) == 0:
        abort_script(msgs, SCRIPT_NAME, "No StartDate provided.")
        exit(1)
    #start_date = datetime.strptime(start_date, '%m/%d/%Y')
    #start_date += relativedelta(days=7)

end_date = start_date + relativedelta(days=6)
asof_date = end_date
"""

# DEBUG - this does not allow for cmd line params, needs to change
#start_date = datetime.strptime('1/1/' + str(start_time.year), '%m/%d/%Y')
#end_date = datetime.strptime('1/5/' + str(start_date.year), '%m/%d/%Y')
#asof_date = None

start_date = datetime.strptime('1/1/' + str(start_time.year), '%m/%d/%Y')
end_date = datetime.strptime('12/31/' + str(start_date.year), '%m/%d/%Y')
asof_date = None

err_cnt = 0

tmp_str = "StartDate=%s, EndDate=%s, AsofDate=%s" % (start_date, end_date, asof_date)
msgs.append(tmp_str)
print(tmp_str)

pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(1) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(1))
if pull_weekly(data_set_id= 1, start_date=start_date, end_date=end_date, asof_date=asof_date) == False:  # PrimaryForecast
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(23) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(23))
if pull_weekly(data_set_id=23, start_date=start_date, end_date=end_date, asof_date=asof_date) == False:  # RMS–1Yield
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(27) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(27))
if pull_weekly(data_set_id=27, start_date=start_date, end_date=end_date, asof_date=asof_date) == False:  # RMS-HiltonGRO/IDeaS
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(40) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(40))
if pull_weekly(data_set_id=40, start_date=start_date, end_date=end_date, asof_date=asof_date) == False:  # RMS-HyattPRiO
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

pull_time = datetime.now()
msgs.append("DataSet=" + get_data_set_name(62) + " " + str(pull_time))
print("DataSet=" + get_data_set_name(62))
if pull_weekly(data_set_id=62, start_date=start_date, end_date=end_date, asof_date=asof_date) == False:  # RMS-Duetto
    err_cnt += 1
msgs.append(get_elapsed_time_str(pull_time))

# update the config file
"""
if len(sys.argv) <= 1:   # dont update the file if were using cmdline params
    json_data['LastRunDate'] = start_date.strftime('%m/%d/%Y')
    with open(CONFIG_FILE, "wt") as cfgfile:
        json.dump(json_data, fp=cfgfile)
"""

msgs.append("End " + SCRIPT_NAME + ": DataSets with Errors=" + str(err_cnt) + ", elapsed= " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
