#====================================================================
#
# MAINLINE for HVMG GSS web scraping code
#
#====================================================================

from gss_lib import *
from bs4 import BeautifulSoup
from gss_stubs import *
from gss_data import *
import requests

# SSO/2FA session token stuff
session = ""

# report data
rpt_request_list    = []
rpt_response_list   = []

SCRIPT_NAME     = "GSS_Web_Scrape"

#-----------------------------------------------------
# MAINLINE
#-----------------------------------------------------

start_time = datetime.now()

msgs = get_message_list()
msgs.append("Begin " + SCRIPT_NAME + ": " + str(start_time))

"""
if len(sys.argv) > 1:
    try:
        dict = parse_cmd_line(sys.argv)
        start_date = datetime.strptime(dict["StartDate"], '%m/%d/%Y')
    except Exception as e:
        abort_script(msgs, SCRIPT_NAME, "Invalid date passed as param: " + str(sys.argv))
        exit(1)
else:
    print("Aborting")
"""

# DEBUG
selected_site = SITE_DATA
# DEBUG

#---------------------------------
# stage 1: login/connx
#---------------------------------

# do login, get session token

session = do_login()

#---------------------------------
# stage 2: gen rpts, get response
#---------------------------------

# we need to fill in the rpt_request_list here
# somehow... these will be the sites (see gss_data.py)
# that we pull web scrapes for

rpt_request_list.append(selected_site)

rpt_cnt = 0
rpt_response_list.clear()

# DEBUG
# There is nothing in rpt_request_list atm so fill this 
# in here and vroom vroom
#rpt_response_list.append("Propertyranker.xls")
#rpt_response_list.append("Sattracktable.xls")
# DEBUG

# for each report to pull...
for rpt in rpt_request_list:
    try:
        # build report request
        request_html = build_rpt_request(session, rpt)

        # send report request
        http_response = send_rpt_request(session, rpt, request_html)

        # verify good response
        http_status = validate_rpt_response(session, rpt, http_response)

        # post process rpt request
        response_html = process_rpt_response(session, rpt, http_response)

        # save response into a file
        filespec = save_response_html(session, rpt, response_html)
        rpt_response_list.append(filespec)

        # loop back for all reports
        scrap = "Successfully requested report " + rpt.get('name')
        msgs.append(scrap)
        print(scrap)
        rpt_cnt += 1

    except Exception as e:
        msgs.append("Exception (stage 2) during report: " + rpt.get('name') + " - " + str(e))
        print(str(e))

### end for rpt

#---------------------------------
# stage 3: web-scrape the needed
#   data from the response obj
#---------------------------------

# for each report pulled
for rpt_file in rpt_response_list:
    try:
        # call web scraper (BS)
        web_scrape(session, rpt_file, rpt.get('output_filespec'))
    except Exception as e:
        msgs.append("Exception (stage 3) during report: " + rpt.get('name') + " - " + str(e))
        print(str(e))
        print("Aborting")
        exit(1)

#---------------------------------
# Done
#---------------------------------

print("Success!")
exit(0)

