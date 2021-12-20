#====================================================================
# 
# The file contains the shared code to pull from the ProfitSword API
# 
# this mod requires :   ujson:      pip install ujson
#                       dateutil:   pip install python-dateutil
#
#====================================================================

from types import DynamicClassAttribute
import requests
#import asyncio
import ujson
import io
from requests import api
from requests.models import guess_json_utf
from hvmg_lib import *
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import atexit


def pull_daily(data_set_id, start_date, end_date, asof_date):
    """pull the daily data from ProfitSword for data_set_id"""
    return __profitsword_pull__(data_set_id=data_set_id, pull_type=1, filespec='PS_Daily', ext_data_set_id=None, start_date=start_date, end_date=end_date, asof_date=asof_date)

def pull_weekly(data_set_id, start_date, end_date, asof_date):
    """pull the weekly data from ProfitSword for data_set_id"""
    return __profitsword_pull__(data_set_id=data_set_id, pull_type=2, filespec='PS_Weekly', ext_data_set_id=None, start_date=start_date, end_date=end_date, asof_date=asof_date)

def pull_monthly(data_set_id, ext_data_set_id, start_date, end_date, asof_date):
    """pull the monthly data from ProfitSword for data_set_id"""
    return __profitsword_pull__(data_set_id=data_set_id, pull_type=3, filespec='PS_Monthly', ext_data_set_id=ext_data_set_id, start_date=start_date, end_date=end_date, asof_date=asof_date)

def pull_sales_pace_events(start_date, end_date, asof_date):
    """pull the sales pace events data for date period"""
    return __profitsword_pull__(data_set_id=None, pull_type=4, filespec='PS_SalesPaceEvents', ext_data_set_id=None, start_date=start_date, end_date=end_date, asof_date=asof_date)

def pull_sales_pace_rooms(start_date, end_date, asof_date):
    """pull the sales pace rooms data for date period"""
    return __profitsword_pull__(data_set_id=None, pull_type=5, filespec='PS_SalesPaceRooms', ext_data_set_id=None, start_date=start_date, end_date=end_date, asof_date=asof_date)

def pull_sales_pace_transient(start_date, end_date, asof_date):
    """pull the sales pace transient data for date period"""
    return __profitsword_pull__(data_set_id=None, pull_type=6, filespec='PS_SalesPaceTransient', ext_data_set_id=None, start_date=start_date, end_date=end_date, asof_date=asof_date)

def __profitsword_pull_dailyextended__(api_key, file, data_set_id, ext_data_set_id, start_date, end_date, asof_date, url):
    """pull the profitsword dailyextended data for each site"""

    msg_list = get_message_list()

    try:
        # get a list of Sites
        params = { 'access_token':api_key }
        response = requests.get(url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/Sites", params=params)
    except Exception as e:
        msg_list.append("ProfitSword API failure - Sites")
        return False
    if response.status_code != 200:
        msg_list.append("ProfitSword API failure - Sites with status_code=" + str(response.status_code))
        return False

    file.write(b"siteTag, siteName, itemTag, description, accountNumber, statAccount, date, asOfDate, stat, amt, data_set\n")

    asofdate_str = None
    if asof_date != None:
        asofdate_str = asof_date.strftime('%m/%d/%Y')

    total_rowcnt = 0
    total_exccnt = 0

    # loop thru the siteTags getting data for each of them
    for siteObj in response.json():
        siteTag = siteObj['siteTag']
        params = {
            'access_token': api_key,
            'dataSetID': data_set_id,
            'bd': start_date.strftime('%m/%d/%Y'),
            'ed': end_date.strftime('%m/%d/%Y'),
            'asOfDate': asofdate_str,
            'siteTag': siteTag,
            'includeTotals':'N'
        }
        
        print("Processing Site: " + str(siteTag))

        pull_start_time = datetime.now()

        try:
            #Call the API to get the Info
            response = requests.get(url=url, params=params)
        except Exception as e:
            msg_list.append("ProfitSword API failure - DailyExtended")
            return False

        print_elapsed_time("DailyExtended", pull_start_time)

        rowcnt = 0
        exccnt = 0

        if response != None:
            if response.status_code == requests.codes.ok:
                if str.upper(response.text) != '"NO DATA DOWNLOADED."':
                    for dataRow in response.json():
                        rowcnt += 1

                        #DEBUG
                        if rowcnt % 100 == 0:
                            print("Processing (DailyExtended: site=" + str(siteTag) + ", data_set=" + str(data_set_id) + ") " + str(rowcnt))

                        try:
                            file.write(csvstr(dataRow['siteTag'],','))
                            file.write(csvstr(dataRow['siteName'],','))
                            file.write(csvstr(dataRow['itemTag'],','))
                            file.write(csvstr(dataRow['description'],','))
                            file.write(csvstr(dataRow['accountNumber'],','))
                            file.write(csvstr(dataRow['statAccount'],','))
                            file.write(csvstr(dataRow['date'],','))
                            file.write(csvstr(dataRow['asOfDate'],','))
                            file.write(csvstr(dataRow['stat'],','))
                            file.write(csvstr(dataRow['amt'],','))
                            if ext_data_set_id != None:
                                file.write(csvstr(str(ext_data_set_id),''))
                            else:
                                file.write(csvstr(str(data_set_id),''))   
                        except Exception as e:
                            exccnt += 1
                            msg_list.append("ProfitSword API failure - DailyExtended, Row=" + str(rowcnt) + "\nRawData=[" + str(dataRow) + "]\n" + str(e) + "\n")
                        file.write(b"\n")

        print("Processed: " + str(rowcnt) + " rows")
        total_rowcnt += rowcnt
        total_exccnt += exccnt

    # good result return 
    #file.close()

    msg_list.append("Records: " + str(total_rowcnt) + ", Exceptions: " + str(total_exccnt))

    return True

def __profitsword_pull_salespace__(api_key, pull_type, file, start_date, end_date, asof_date, url):
    """pull the profitsword salespace data for each site"""

    msg_list = get_message_list()

    params = {
        'access_token': api_key,
        'asofdate': asof_date.strftime('%m/%d/%Y'),
        'bd': start_date.strftime('%m/%d/%Y'),
        'ed': end_date.strftime('%m/%d/%Y'),
        'siteTag': 'ALL'
        }

    pull_start_time = datetime.now()

    try:
        #Call the API to get the Info
        response = requests.get(url=url, params=params)
    except Exception as e:
        msg_list.append("ProfitSword API failure - SalesPace")
        return False

    print_elapsed_time("SalesPace Pull: ", pull_start_time)

    if pull_type == PULL_TYPE_EVENTS:
        file.write(b"asofdate,column1,status,qty,amtFood,amtBev,amtRent,amtRsrc,amtMisc,siteTag,siteName,bookingCode,bookingName,marketSegmentCode,marketSegmentName,accountCode,accountName,salesManagerCode,salesManagerName,eventCode,eventName,eventTypeCode,eventTypeName\n")
    else:
        file.write(b"asofdate,date,status,qty,amt,siteTag,siteName,bookingCode,bookingName,marketSegmentCode,marketSegmentName,accountCode,accountName,salesManagerCode,salesManagerName\n")

    rowcnt = 0
    exccnt = 0

    if response != None:
        if response.status_code == requests.codes.ok:
            if str.upper(response.text) != '"NO DATA DOWNLOADED."':
                for dataRow in response.json():
                    rowcnt += 1

                    if rowcnt % 100 == 0:
                        print("Processing (SalesPace type=" +  get_pull_type_name(pull_type) + ") " + str(rowcnt))
                    try:
                        if pull_type == PULL_TYPE_EVENTS:
                            file.write(csvstr(dataRow['asofdate'],','))
                            file.write(csvstr(dataRow['column1'],','))
                            file.write(csvstr(dataRow['status'],','))
                            file.write(csvstr(dataRow['qty'],','))
                            file.write(csvstr(dataRow['amtFood'],','))
                            file.write(csvstr(dataRow['amtBev'],','))
                            file.write(csvstr(dataRow['amtRent'],','))
                            file.write(csvstr(dataRow['amtRsrc'],','))
                            file.write(csvstr(dataRow['amtMisc'],','))
                            file.write(csvstr(dataRow['siteTag'],','))
                            file.write(csvstr(dataRow['siteName'],','))
                            file.write(csvstr(dataRow['bookingCode'],','))
                            file.write(csvstr(dataRow['bookingName'],','))
                            file.write(csvstr(dataRow['marketSegmentCode'],','))
                            file.write(csvstr(dataRow['marketSegmentName'],','))
                            file.write(csvstr(dataRow['accountCode'],','))
                            file.write(csvstr(dataRow['accountName'],','))
                            file.write(csvstr(dataRow['salesManagerCode'],','))
                            file.write(csvstr(dataRow['salesManagerName'],','))
                            file.write(csvstr(dataRow['eventCode'],','))
                            file.write(csvstr(dataRow['eventName'],','))
                            file.write(csvstr(dataRow['eventTypeCode'],','))
                            file.write(csvstr(dataRow['eventTypeName'], ''))
                        else:
                            file.write(csvstr(dataRow['asofdate'],','))
                            file.write(csvstr(dataRow['date'],','))
                            file.write(csvstr(dataRow['status'],','))
                            file.write(csvstr(dataRow['qty'],','))
                            file.write(csvstr(dataRow['amt'],','))
                            file.write(csvstr(dataRow['siteTag'],','))
                            file.write(csvstr(dataRow['siteName'],','))
                            file.write(csvstr(dataRow['bookingCode'],','))
                            file.write(csvstr(dataRow['bookingName'],','))
                            file.write(csvstr(dataRow['marketSegmentCode'],','))
                            file.write(csvstr(dataRow['marketSegmentName'],','))
                            file.write(csvstr(dataRow['accountCode'],','))
                            file.write(csvstr(dataRow['accountName'],','))
                            file.write(csvstr(dataRow['salesManagerCode'],','))
                            file.write(csvstr(dataRow['salesManagerName'],";"))
                    except Exception as e:
                        exccnt += 1
                        msg_list.append("ProfitSword API failure - SalesPace PullType=" + get_pull_type_name(pull_type) + ", Row=" + str(rowcnt) + "\nRawData=[" + str(dataRow) + "]\n" + str(e) + "\n")
                    file.write(b"\n")

    # good result return 
    
    #file.flush()
    #file.close()

    msg_list.append("SalesPace Records: " + str(rowcnt) + ", Exceptions: " + str(exccnt))

    return True

def __profitsword_pull__(data_set_id, pull_type, filespec, ext_data_set_id, start_date, end_date, asof_date):
    """ Pull the data from ProfitSword based on data_set_id and pull_type
        data_set_id: the data_set_id to pull for (int)
            see get_dataset_name for more info
        pull_type: 1=daily, 2=weekly, 3=Monthly (int)
        filespec: filename part indicating daily/weekly/monthly (string)
            full filespec is '<yyyymmdd>_<filespec>_<DataSetName>.csv'
        start_date: starting date to pull data for ('mm/dd/yyyy')
        end_date: ending date of pull ('mm/dd/yyyy')
        asof_date: as of date to pull (mm/dd/yyy)
    """
    msg_list = get_message_list()

    start_time = datetime.now()

    url = ""

    if pull_type == PULL_TYPE_DAILY:
        url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/DailyExtended"
    elif pull_type == PULL_TYPE_WEEKLY:
        url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/DailyExtended"
    elif pull_type == PULL_TYPE_MONTHLY:
        url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/DailyExtended"
    elif pull_type == PULL_TYPE_EVENTS:
        url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/SalesPaceEvents"
    elif pull_type == PULL_TYPE_ROOMS:
        url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/SalesPaceRooms"
    elif pull_type == PULL_TYPE_TRANSIENT:
        url = "https://hvmg.Profitsage.net/PS-Handlers/api/DataPortalv3/SalesPaceTransient"
    else:
        msg_list.append("Invalid pull_type: " + str(pull_type))
        return False

    # with the addition of sales_pace pulls, data_set_Id might be None
    data_set_name = ""
    if data_set_id != None:
        data_set_name = get_data_set_name(data_set_id=data_set_id)
        if data_set_name == None:
            msg_list.append("Invalid data set id: " + str(data_set_id))
            return False
        
    if pull_type <= 3:
        filefolder = "F:\\Source Data\\ProfitSword\\DailyExtended\\ToBeLoaded\\"
        filename = filefolder + start_date.strftime('%Y%m%d') + "_" + filespec + "_" + data_set_name + ".csv"
    else:
        if pull_type == PULL_TYPE_EVENTS:
            filefolder = "F:\\Source Data\\ProfitSword\\SalesPaceEvents\\ToBeLoaded\\"
        elif pull_type == PULL_TYPE_ROOMS: 
            filefolder = "F:\\Source Data\\ProfitSword\\SalesPaceRooms\\ToBeLoaded\\"
        elif pull_type == PULL_TYPE_TRANSIENT:
            filefolder = "F:\\Source Data\\ProfitSword\\SalesPaceTransient\\ToBeLoaded\\"
        filename = filefolder + start_date.strftime('%Y%m%d') + "_" + filespec + ".csv"

    #output_file = open(filename, "wt")
    output_file = io.FileIO(filename, "w")
    writer = io.BufferedWriter(output_file, buffer_size=256000)
    #atexit.register(output_file.close)
            
    #DEBUG
    msg_list.append("Pulling type=" + get_pull_type_name(pull_type) + ", Start=" + start_date.strftime('%Y%m%d') + ", End=" + end_date.strftime('%Y%m%d') + ", File=" + filename)

    try:
        #Call the API to get the Token
        ENDPOINT="https://hvmg.Profitsage.net/PS-Handlers/token"
        HEADERS={'Accept':'application/json', 'Content-type':'application/x-www-form-urlencoded'}
        DATA={'grant_type':'password', 'username':'HVMG_Data', 'password':'D@taHAcce$s'}
        response=requests.post(url=ENDPOINT, headers=HEADERS, data=DATA)
        API_KEY=response.json()['access_token']
    except Exception as e:
        msg_list.append("ProfitSword API failure - GenerateToken")
        return False
    #if pull_type <= 3:  # 1,2,3 are daily extended, 4,5,6 are salespace
    #    __profitsword_pull_dailyextended__(API_KEY, output_file, data_set_id, ext_data_set_id, start_date, end_date, asof_date, url)
    #else:
    #    __profitsword_pull_salespace__(API_KEY, pull_type, output_file, start_date, end_date, asof_date, url)

    if pull_type <= 3:  # 1,2,3 are daily extended, 4,5,6 are salespace
        __profitsword_pull_dailyextended__(API_KEY, writer, data_set_id, ext_data_set_id, start_date, end_date, asof_date, url)
    else:
        __profitsword_pull_salespace__(API_KEY, pull_type, writer, start_date, end_date, asof_date, url)

    # done
    print("Done pulling data, writing file...")
    writer.write(b"\n")
    writer.flush()
    writer.close()
    #output_file.close()
    print("Done writing file.")
    
    return True    
    # end def

