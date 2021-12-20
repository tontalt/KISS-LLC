#====================================================================
# 
# Data for each site (Medallia) (HVMG Web Scraping) 
# currently expect to need one dictionary entry per site to be scraped
# or convert to .json 
# *** or other but time is of the essence***
# 
#====================================================================

from gss_lib import *
import requests

#----------------------------------------
# Data for TEST (currently w3schools.com)
#----------------------------------------

SITE_DATA = {
    'name': 'TEST', 
    'url': 'https://www.w3schools.com/html/html_tables.asp',
    'interim_filespec': 'F:\\WebScraping\\Interim\\Test.xls',
    'output_filespec':  'F:\\WebScraping\\Output\\Test.csv'
}

