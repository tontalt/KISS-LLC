#====================================================================
# 
# STUBS STUBS STUBS YeeHaw!
# 
# function stubs for gss_web_scrape.py. Replace with real code or
# just expand in place, either or should work
# 
#====================================================================

from gss_data import *
from gss_lib import *
from bs4 import BeautifulSoup
import requests
from http import HTTPStatus

#-----------------------------------------------------

def do_login():
    return "dummy session obj"

#-----------------------------------------------------

def build_rpt_request(session, rpt):
    #html = "<html><head><body>"
    #html += "</body></head></html>"
    return ""

#-----------------------------------------------------

def send_rpt_request(session, rpt, request_html):

    resp = requests.get(rpt.get('url'))
    return resp

#-----------------------------------------------------

def validate_rpt_response(session, rpt, http_response):
    if HTTPStatus.OK:
        return True
    return False

#-----------------------------------------------------

def process_rpt_response(session, rpt, http_response):
    # in our case (TEST) just return the html
    return http_response.text
    

#-----------------------------------------------------

def save_response_html(session, rpt, response_html):
    filespec = rpt.get('interim_filespec')
    
    html = response_html.encode(encoding="ascii",errors="ignore")
    with open(filespec, 'wb') as f:
        f.write(html)

    return filespec

#-----------------------------------------------------
# 

def web_scrape(session, interim_filespec, output_filespec):

    try:
        ifile = open(interim_filespec, mode='r')
        html = ifile.read()
        ifile.close()

        soup = BeautifulSoup(html, "lxml")
        table = soup.find('table')

        list_of_rows = []
        for row in table.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll(["th","td"]):
                text = cell.text.replace("\n\n\n\n", "")
                list_of_cells.append(text.strip())
            list_of_rows.append(list_of_cells)

        # fixup the filename from xls to csv
        csvfilespec = output_filespec
        ofile = open(csvfilespec, mode='wt')

        for item in list_of_rows:
            xstr = "\'" + '\', \''.join(item) + "\'"
            ofile.write(xstr)
            #ofile.write("\"" + '\", \"'.join(item) + "\"")
            ofile.write("\n")

        ofile.flush()
        ofile.close()

        return True
    except Exception as e:
        print(str(e))
        return False
