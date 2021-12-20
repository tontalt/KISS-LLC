#====================================================================
# 
# Code to pull the Demand360 Dailies
#
# this script uses following mods:
#------------------------------
# pip install pysftp
#====================================================================

from hvmg_lib import *
import pysftp
import sys
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

SCRIPT_NAME = "SFTP_Demand_360"

HOST_NAME = "52.149.224.118"
USER_NAME = "greg"
PASSWORD = "DjTujeb54RdTQg4q"
PORT = 22

OUT_PATH_360 = "F:\\Source Data\\Demand360\\ToBeLoaded\\"
OUT_PATH_STR_WEEKLY = "F:\\Source Data\\SmithTravel\\ToBeLoaded\\Weekly\\"
OUT_PATH_STR_MONTHLY = "F:\\Source Data\\SmithTravel\\ToBeLoaded\\Monthly\\"
# DEBUG
#OUT_PATH_360 = ".\\Output_Files\\"

IN_PATH_360 = "TravelClick"     # Demand360

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
    start_date = datetime.today()
    start_date += relativedelta(days=-1)

filespec360 = "_" + start_date.strftime('%Y%m%d') + "_"
# DEBUG 
#filespec360 = "_20211005_"

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

file_cnt_360 = 0

try:
    with pysftp.Connection(HOST_NAME, username=USER_NAME, password=PASSWORD, port=PORT, private_key=".ppk", cnopts=cnopts) as sftp:
        sftp.cwd(IN_PATH_360)
        for filename in sftp.listdir():
            if filespec360 in filename:
                sftp.get(filename, localpath=OUT_PATH_360 + filename)
                file_cnt_360 += 1
                print("Downloaded: " + OUT_PATH_360 + filename)
        msgs.append(str(file_cnt_360) + " files downloaded for Demand360")
except Exception as e:
    append_logfile(SCRIPT_NAME, "SFTP Error: " + str(e))
    exit(1)
        
msgs.append("End " + SCRIPT_NAME + ": elapsed= " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)
