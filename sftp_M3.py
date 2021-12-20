#====================================================================
# 
# Code to pull the M3 Dailies
#
# this script uses following mods:
#------------------------------
# pip install pysftp
#====================================================================

from hvmg_lib import *
import pysftp
import sys
import os
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import xml.etree.ElementTree as ET
import atexit

SCRIPT_NAME = "SFTP_M3"

HOST_NAME = "export.sftp.m3as.com"
USER_NAME = "kiss-sftp"
PASSWORD = "R3gnc9b"
PORT = 22

OUT_PATH_XML = "F:\\Source Data\\M3\\GL\\Downloads\\"
OUT_PATH_CSV = "F:\\Source Data\\M3\\GL\\ToBeLoaded\\"

IN_PATH = "HVL/General Ledger Detail"

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

#DEBUG
#start_date = datetime.strptime('10/9/2021', '%m/%d/%Y')

srchstr = start_date.strftime('%Y_%m_%d')
file_cnt_download = 0
file_cnt_convert = 0
downloaded = []

#------------------------------------------------------------
# download the files that match the search criteria 
# from the spft server

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

try:
    with pysftp.Connection(HOST_NAME, username=USER_NAME, password=PASSWORD, port=PORT, private_key=".ppk", cnopts=cnopts) as sftp:
        sftp.cwd(IN_PATH)
        for filename in sftp.listdir():                 # get the entire directory and search thru the files
            if srchstr in filename:                     # if our filename srchstr is in this file then...
                downloaded.append(filename)             # keep a list of downloaded files for post processing
                filespec = OUT_PATH_XML + filename      # create the filespec
                sftp.get(filename, localpath=filespec)  # download the file
                file_cnt_download += 1                  # update file count
                print("Downloaded: " + filespec)        # in case were running batch or console mode
    msgs.append(str(file_cnt_download) + " files downloaded for M3")
except Exception as e:
    abort_script(msgs, SCRIPT_NAME, "SFTP Error: " + str(e))
    exit(1)

#------------------------------------------------------------
# open each downloaded file and convert it from xml to csv

fields = {}

try:
    for filename in downloaded:

        orig_filespec = OUT_PATH_XML + filename    # save it for delete later

        # empty out the fields from last iteration
        fields.clear()

        filename = filename.replace(".xml", ".csv")
        filespec = OUT_PATH_CSV + filename
        file = open(filespec, "wt")
        atexit.register(file.close)
        file.write("Details Amount, Reference, Description, PostDate, GLAccount, InvoiceDate, InvoiceNo, VendorID, TransType, BatchType, BatchID, PropertyName, PropertyCode, CompanyName, CompanyCode\n")

        tree = ET.parse(orig_filespec)
        root = tree.getroot()
        #for item in tree.findall(".//Tablix1/Details_Collection/Details"):
        for tablix in root:         # <Tablix1>
            for dc in tablix:       # <Details_Collection>
                for item in dc:     # <Details>
                    # read the fields from the xml
                    fields['Amount'] = item.get('Amount')
                    fields['Reference'] = item.get('Reference')
                    fields['Description'] = item.get('Description')
                    fields['PostDate'] = item.get('PostDate')
                    fields['GLAccount'] = item.get('GLAccount')
                    fields['InvoiceDate'] = item.get('InvoiceDate')
                    fields['InvoiceNo'] = item.get('InvoiceNo')
                    fields['VendorID'] = item.get('VendorID')
                    fields['TransType'] = item.get('TransType')
                    fields['BatchType'] = item.get('BatchType')
                    fields['BatchID'] = item.get('BatchID')
                    fields['PropertyName'] = item.get('PropertyName')
                    fields['PropertyCode'] = item.get('PropertyCode')
                    fields['CompanyName'] = item.get('CompanyName')
                    fields['CompanyCode'] = item.get('CompanyCode')
                    # write the fields to the csv
                    file.write(str(fields['Amount']) + ',')
                    file.write(dblquote(str(fields['Reference'])) + ',')
                    file.write(dblquote(str(fields['Description'])) + ',')
                    file.write(str(fields['PostDate']) + ',')
                    file.write(str(fields['GLAccount']) + ',')
                    file.write(str(fields['InvoiceDate']) + ',')
                    file.write(str(fields['InvoiceNo']) + ',')
                    file.write(str(fields['VendorID']) + ',')
                    file.write(str(fields['TransType']) + ',')
                    file.write(str(fields['BatchType']) + ',')
                    file.write(str(fields['BatchID']) + ',')
                    file.write(dblquote(str(fields['PropertyName'])) + ',')
                    file.write(str(fields['PropertyCode']) + ',')
                    file.write(dblquote(str(fields['CompanyName'])) + ',')
                    file.write(str(fields['CompanyCode']) + '\n')
        # end for
        file.close()
        file_cnt_convert += 1
        os.remove(orig_filespec)
        msgs.append(str(file_cnt_convert) + " files converted to csv for M3")
    # end for
except Exception as e:
    abort_script(msgs, SCRIPT_NAME, "XML to CSV Error: " + str(e))
    exit(1)

#------------------------------------------------------------
# done

msgs.append("End " + SCRIPT_NAME + ": elapsed= " + get_elapsed_time_str(start_time))

buff = get_message_list_tostr()
print(buff)
append_logfile(SCRIPT_NAME, buff)

exit(0)