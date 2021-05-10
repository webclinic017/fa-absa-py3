"""--------------------------------------------------------------------------
MODULE
   FTimeUtils

DESCRIPTION
    This module houses common time functionality

HISTORY 
Date: 2019-11-18
Jira:  FAFO-51 - Time today in seconds
   
-----------------------------------------------------------------------------"""
import datetime

def get_time_in_seconds(time_default = None):
    """Get Seconds from time."""
    if time_default:
        time = time_defaut
    else:
        time = datetime.datetime.now().time()
        
    h = time.hour
    m = time.minute
    s = time.second
    
    return int(h) * 3600 + int(m) * 60 + int(s)
