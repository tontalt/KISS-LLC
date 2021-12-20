#====================================================================
# 
# Code to pull the Medallia HardRock Dailies
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

SCRIPT_NAME = "SFTP_Medallia_HardRock"
CONFIG_FILE = ".\\sftp_medallia_hardrock.json"

HOST_NAME = "mft.medallia.com"
USER_NAME = "sgahardrock_seminole"
PASSWORD = "tG@8qU5aa$7X"
PORT = 22

OUT_PATH_HARDROCK = "F:\\Source Data\\Medallia\\HardRock\\ToBeLoaded\\"

IN_PATH_HARDROCK = "outbox_Daytona_Beach"

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

# example filespec from the fstp server
#Daytona Beach 2021 Export_2021-10-22_235959.xlsx
filespec = " Export_" + start_date.strftime('%Y-%m-%d')

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

file_cnt_str = 0

try:
    with pysftp.Connection(HOST_NAME, username=USER_NAME, password=PASSWORD, port=PORT, private_key=".ppk", cnopts=cnopts) as sftp:
        sftp.cwd(IN_PATH_HARDROCK)
        for filename in sftp.listdir():
            if filespec in filename:
                sftp.get(filename, localpath=OUT_PATH_HARDROCK + filename)
                file_cnt_str += 1
                msgs.append("Downloaded: " + OUT_PATH_HARDROCK + filename)
        msgs.append(str(file_cnt_str) + " files downloaded for HardRock")
except Exception as e:
    append_logfile(SCRIPT_NAME, "SFTP Error: " + str(e))
    exit(1)

# update the config file
#if len(sys.argv) <= 1:   # dont update the file if were using cmdline params
#    json_data['LastRunDate'] = start_date.strftime('%m/%d/%Y')
#    with open(CONFIG_FILE, "wt") as cfgfile:
#        json.dump(json_data, fp=cfgfile)

msgs.append("End " + SCRIPT_NAME + ": " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
