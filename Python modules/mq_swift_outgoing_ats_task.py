'''
This ATS handles all outgoing SWIFT messages from python scripts to be placed onto MQ
This is kept as a seperate ATS script to cater for future outgoing SWIFT placements
'''
import acm
import demat_isin_mgmt
import traceback
from time import sleep

ael_variables = []
ael_gui_parameters = {'windowCaption':'Outgoing Custom Swift Task'}

def ael_main(dict):
    acm.PollAllEvents()
    try:
        #Add all custom outgoing swift sending functions here
        sleep(90)
        demat_isin_mgmt.send_isin_requests()
    except Exception, ex:
        print('Exception:', ex)  #TODO: Add extra config values where log output will be appended to
        traceback.print_exc()

    
