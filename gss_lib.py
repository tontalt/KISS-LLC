#====================================================================
# 
# some common/shared routines for HVMG GSS web scraping code
# 
#====================================================================
import datetime
import dateutil
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
import io
from gss_lib import *


LOGFILE_FOLDER = "F:\\logs\\"

__message_list__ = []

def get_message_list():
    return __message_list__

def get_message_list_tostr():
    mystr = ""
    for line in __message_list__:
        mystr += line + "\n"
    return mystr

def append_logfile(process_name, msg):
    """Append a line to the logfile for this process"""
    try:
        filespec = LOGFILE_FOLDER + datetime.today().strftime('%Y_%m_') + process_name + ".txt"
        logfile = open(filespec, "at")
        logfile.write(msg)
        logfile.close()
    except Exception as e:
        return False
    return True