#====================================================================
# some common/shared routines for HVMG python scripts
# 
#====================================================================

#import smtplib
#import ssl
from datetime import datetime

PULL_TYPE_DAILY = 1
PULL_TYPE_WEEKLY = 2
PULL_TYPE_MONTHLY = 3
PULL_TYPE_EVENTS = 4
PULL_TYPE_ROOMS = 5
PULL_TYPE_TRANSIENT = 6

STATUS_EMAIL_ADDR = "gw@kissllc.com"
LOGFILE_FOLDER = "F:\\logs\\"

__message_list__ = []

def is_integer(num):
    try:
        if isinstance(num, int):
            return True
        return False
    except Exception as e:
        print (str(num) + ": " + str(e))
        return False
    return False

def is_float(num):
    try:
        if isinstance(num, float):
            return True
        return False
    except Exception as e:
        print (str(num) + ": " + str(e))
        return False
    return False

def is_date(adate):
    my_date = ""
    try:
        #1/6/2020 16:57
        my_date = datetime.strptime(str(adate), '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return False
    return True

def is_number(num):
    if is_integer(num):
        return True
    if is_float(num):
        return True
    if is_date(num):
        return True
    return False

def get_message_list():
    return __message_list__

def get_message_list_tostr():
    mystr = ""
    for line in __message_list__:
        mystr += line + "\n"
    return mystr

def abort_script(msgs, script_name, err_msg):
    msgs.append("Abort: " + script_name + " - " + err_msg)
    buff = get_message_list_tostr()
    print(buff)
    append_logfile(script_name, buff)

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

"""
# commented out for now to catch remaining calls...

def send_status_email(status, process_name, email_msg):
    smtp_server = "localhost"
    to_email = STATUS_EMAIL_ADDR
    from_email = "HVMG-VM@hvmg.com"
    password = "ki$s9959!"
    port = 587
    context = ssl.create_default_context()
    if status == True:
        status_txt = "OK"
    else:
        status_txt = "FAIL"

    subject = status_txt + ": " + process_name

    email_body = "From: <{from_email}>\nTo: <{to_email}>\nSubject: {subject}\n\n{email_msg}\n\n".format(from_email=from_email, to_email=to_email, subject=subject, email_msg=email_msg)

    # DEBUG
    # for now just print while in testing
    print(email_body)

    #try:
    #    server = smtplib.SMTP(smtp_server, port)
    #    server.starttls(context=context)
        #server.login(from_email, password=password)
    #    server.sendmail(from_addr=from_email, to_addrs=to_email, msg=email_body)
    #except Exception as e:
        # nothing really to do here
    #    print(e)
    #finally:
    #    server.quit()
"""

def print_elapsed_time(label, start_time):
    """print out the elapsed time in hh:mm:ss for a given start_time"""
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(label + " - Elapsed time=%02d:%02d:%02d" % (elapsed_time.seconds // 3600, elapsed_time.seconds // 60 % 60, elapsed_time.seconds % 60))

def get_elapsed_time_str(start_time):
    """get a string representing the elapsed time in hh:mm:ss for a given start_time"""
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    return("Elapsed time=%02d:%02d:%02d" % (elapsed_time.seconds // 3600, elapsed_time.seconds // 60 % 60, elapsed_time.seconds % 60))

def parse_cmd_line(argv):
    """Parse the command line params and return the values in a dictionary object"""
    """See launch.json for an example"""

    dict = {}

    for param in argv:
        vals = param.split(":")
        if len(vals) == 2:
            if vals[0] == "-s":
                dict["StartDate"] = vals[1]
            elif vals[0] == "-e":
                dict["EndDate"] = vals[1]
            elif vals[0] == "-a":
                dict["AsOfDate"] = vals[1]

    return dict
    
def dblquote(pstr):
    """Place double quotes around string data, also escape any existing double quotes first"""
    pbytes = pstr.encode(encoding="ascii", errors="ignore") # strip out non-ascii chars 
    pstr = pbytes.decode("utf-8")                           # convert from bytes back to string
    pstr = pstr.replace("\"", "\"\"")                       # escape any existing quotes
    return '\"' + pstr + '\"'                               # enquote and return


def csvstr(instr, delim):
    """Place double quotes around string data, also escape any existing double quotes first"""
    
    pstr = str(instr).replace("\"", "\"\"")                     # escape any existing quotes
    pstr = "\"%s\"%s" % (pstr, delim)
    outbytes = pstr.encode(encoding="utf-8", errors="ignore")   # strip out non-ascii chars 
    return(outbytes)

def csvnum(num):
    """add commas to csv column, but no quotes"""
    try:
        pstr = str(num) + ','                                       # add comma
        outbytes = pstr.encode(encoding="utf-8", errors="ignore")   # strip out non-ascii chars 
        return(outbytes)
    except Exception as e:
        return "***,"

def get_pull_type_name(pull_type):
    "translate a pull_type into a name string"
    if pull_type == PULL_TYPE_DAILY:
        return "Daily"
    elif pull_type == PULL_TYPE_WEEKLY:
        return "Weekly"
    elif pull_type == PULL_TYPE_MONTHLY:
        return "Monthly"
    elif pull_type == PULL_TYPE_EVENTS:
        return "Events"
    elif pull_type == PULL_TYPE_ROOMS:
        return "Rooms"
    elif pull_type == PULL_TYPE_TRANSIENT:
        return "Transient"


def get_data_set_name(data_set_id):
    """translate a data_set_id into a name string"""
    if data_set_id == -3:
        return "Actuals"
    elif data_set_id == 1:
        return "Primary Forecast"
    elif data_set_id == 2:
        return "Budget"
    elif data_set_id == 19:
        return "pfc 3-18"
    elif data_set_id == 20:
        return "Flex"
    elif data_set_id == 21:
        return "Prior Management Budget"
    elif data_set_id == 22:
        return "Proforma Budget"
    elif data_set_id == 23:
        return "RMS - OneYield"
    elif data_set_id == 25:
	    return "Prior Management Actuals"
    elif data_set_id == 26:
	    return "Budget Backup"
    elif data_set_id == 27:
	    return "RMS - HiltonGRO-IDeaS"
    elif data_set_id == 28:
	    return "Forecast Backup"
    elif data_set_id == 35:
	    return "Reno Budget"
    elif data_set_id == 39:
	    return "As Is Budget"
    elif data_set_id == 40:
	    return "RMS - HyattPRiO"
    elif data_set_id == 43:
	    return "Closing Forecast"
    elif data_set_id == 44:
	    return "Budget Backup 4-10-20"
    elif data_set_id == 45:
	    return "TEMP Budget"
    elif data_set_id == 46:
	    return "C19 Ramp-Up Forecast"
    elif data_set_id == 47:
	    return "Competitive Set 1"
    elif data_set_id == 48:
	    return "Property CS Data"
    elif data_set_id == 49:
	    return "Backup C19"
    elif data_set_id == 50:
	    return "2 Backup C19"
    elif data_set_id == 51:
	    return "Nashville Underwriting"
    elif data_set_id == 52:
	    return "Budget Backup 8-12-2020"
    elif data_set_id == 53:
	    return "Budget Backup 10-15-2020"
    elif data_set_id == 54:
	    return "Budget Backup 11-4-2020"
    elif data_set_id == 55:
	    return "Budget Backup 11-17-2020"
    elif data_set_id == 56:
	    return "Budget Backup 12-1-2020"
    elif data_set_id == 57:
	    return "Budget 3"
    elif data_set_id == 58:
	    return "Version 1 - Budget "
    elif data_set_id == 59:
	    return "Declined Budget 76.64"
    elif data_set_id == 60:
	    return "Test site"
    elif data_set_id == 61:
	    return "Pre-Opening Budget"
    elif data_set_id == 62:
	    return "RMS - Duetto"
    elif data_set_id == 63:
	    return "Budget Backup 5-11-21"
    elif data_set_id == 64:
	    return "PRIOR"
    elif data_set_id == 65:
	    return "TEST"
    else:
        return None
