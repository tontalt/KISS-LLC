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

SCRIPT_NAME = "SFTP_Medallia_Hyatt"
CONFIG_FILE = ".\\sftp_hyatt.json"

HOST_NAME = "ftp1.medallia.com"
USER_NAME = "hysat"
PASSWORD = "wrew3aTA"
PORT = 22

OUT_PATH_HYATT = "F:\\Source Data\\Medallia\\Hyatt\\ToBeLoaded\\"

IN_PATH_HYATT = "HVMG_Hospitality"

FILE_PREFIX = "Cognos_Hyatt_GSS_HVMG_"

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
    # DEBUG
    start_date = datetime.today()
#    with open(CONFIG_FILE) as cfgfile:
#        json_data = json.load(cfgfile)
#    start_date = json_data['LastRunDate']
#    if  start_date == None or len(start_date) == 0:
#        abort_script(msgs, SCRIPT_NAME, "No StartDate provided.")
#        exit(1)
#    start_date = datetime.strptime(start_date, '%m/%d/%Y')
#    start_date += relativedelta(days=7)

# example filespec from the fstp server
#Cognos_Hyatt_GSS_HVMG_2021-11-03.csv
filespecHYATT = FILE_PREFIX + start_date.strftime('%Y-%m-%d')

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

file_cnt_str = 0

curr_date = start_date
end_date = start_date
end_date += relativedelta(days = -14)  # go back 1/2 month, no further

try:
    file_to_get = ""
    with pysftp.Connection(HOST_NAME, username=USER_NAME, password=PASSWORD, port=PORT, private_key=".ppk", cnopts=cnopts) as sftp:
        sftp.cwd(IN_PATH_HYATT)
        for filename in sftp.listdir():
            # DEBUG 
            # buncha debug shyte till we work out some more details
            curr_date = start_date
            while curr_date >= end_date:
                tmpFilespec = FILE_PREFIX + curr_date.strftime('%Y-%m-%d')
                #DEBUG
                #print("Searching for [" + tmpFilespec + "] in [" + filename + "]")
                if tmpFilespec in filename:
                    file_to_get = OUT_PATH_HYATT + filename
                    #for now only need 1 file
                    curr_date = end_date
                    curr_date += relativedelta(days = -60)
                    break
                curr_date += relativedelta(days=-1) #try prev day
            #end while
        #end for   
        if len(file_to_get) > 0:
            sftp.get(filename, localpath=file_to_get)
            file_cnt_str += 1
            msgs.append("Downloaded: " + file_to_get)

        msgs.append(str(file_cnt_str) + " files downloaded for Hyatt")
except Exception as e:
    append_logfile(SCRIPT_NAME, "SFTP Error: " + str(e))
    exit(1)

# update the config file
#if len(sys.argv) <= 1:   # dont update the file if were using cmdline params
#    json_data['LastRunDate'] = start_date.strftime('%m/%d/%Y')
#    with open(CONFIG_FILE, "wt") as cfgfile:
#        json.dump(json_data, fp=cfgfile)

msgs.append("End " + SCRIPT_NAME + ": elapsed= " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
