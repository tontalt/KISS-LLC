#====================================================================
# 
# Code to pull the STR Dailies
#
# this script uses following mods:
#------------------------------
# pip install pysftp
#====================================================================

from hvmg_lib import *
import pysftp
import sys
import json
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

SCRIPT_NAME = "SFTP_STR"
CONFIG_FILE = ".\\sftp_str.json"

HOST_NAME = "52.149.224.118"
USER_NAME = "greg"
PASSWORD = "DjTujeb54RdTQg4q"
PORT = 22

OUT_PATH_STR_WEEKLY = "F:\\Source Data\\SmithTravel\\STR_Weekly\\ToBeLoaded\\"
OUT_PATH_STR_MONTHLY = "F:\\Source Data\\SmithTravel\\STR_Monthly\\ToBeLoaded\\"

IN_PATH_STR = "STRData"         # STR

start_time = datetime.now()

msgs = get_message_list()
msgs.append("Begin " + SCRIPT_NAME + ": " + str(start_time))

if len(sys.argv) > 1:
    try:
        start_date = datetime.strptime(sys.argv[1], '%m/%d/%Y')
    except:
        abort_script(msgs, SCRIPT_NAME, "Invalid date passed as param: " + str(sys.argv))
        exit(1)
else:
    #start_date = datetime.today()
    with open(CONFIG_FILE) as cfgfile:
        json_data = json.load(cfgfile)
    start_date = json_data['LastRunDate']
    if  start_date == None or len(start_date) == 0:
        abort_script(msgs, SCRIPT_NAME, "No StartDate provided.")
        exit(1)
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    last_run_date = start_date + relativedelta(days=7)

filespecSTR_Monthly = "hospventplus36mo_" + start_date.strftime('%Y%m')

# loop thru the previous dates until we get to the 2nd previous Sunday
# which will have the correct name of the file we want

ii = 100            # break condition, avoid runaway
sun_cnt = 0         # cound of sundays (must be 2)

# turned off for testing - calc prev sunday not working, as expected
#while ii > 0:
#    start_date += relativedelta(days=-1)
#    dayofweek = start_date.weekday()  # aka Sunday
#    if dayofweek == 6:
#        sun_cnt += 1
#        if sun_cnt == 2:
#            #ii = 0
#            break
#    ii -= 1
#if ii == 0:
#    msgs.append("***Warning: No date match found for last Sunday (ii=0)!!!")

filespecSTR_Weekly  = "hospventplus6wk_"  + start_date.strftime('%Y%m%d')

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

file_cnt_str = 0

try:
    with pysftp.Connection(HOST_NAME, username=USER_NAME, password=PASSWORD, port=PORT, private_key=".ppk", cnopts=cnopts) as sftp:
        sftp.cwd(IN_PATH_STR)
        for filename in sftp.listdir():
            if filespecSTR_Weekly in filename:
                filespec = OUT_PATH_STR_WEEKLY + filename
                sftp.get(filename, localpath=filespec)
                msgs.append("File Retrieved: " + filespec)
                file_cnt_str += 1
            elif filespecSTR_Monthly in filename:
                filespec = OUT_PATH_STR_MONTHLY + filename
                sftp.get(filename, localpath=filespec)
                msgs.append("File Retrieved: " + filespec)
                file_cnt_str += 1
        msgs.append(str(file_cnt_str) + " files downloaded for STR")
except Exception as e:
    append_logfile(SCRIPT_NAME, "SFTP Error: " + str(e))
    exit(1)

# update the config file
if len(sys.argv) <= 1:   # dont update the file if were using cmdline params
    json_data['LastRunDate'] = last_run_date.strftime('%m/%d/%Y')
    with open(CONFIG_FILE, "wt") as cfgfile:
        json.dump(json_data, fp=cfgfile)

msgs.append("End " + SCRIPT_NAME + ": elapsed= " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
