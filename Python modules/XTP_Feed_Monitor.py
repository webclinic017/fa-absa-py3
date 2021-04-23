"""-----------------------------------------------------------------------------
MODULE	    	XTP_Monitor 

Version: 1.1

DESCRIPTION
This module is for XTP_Monitor purposes.
It executes the XTP_Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add XTP_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def XTP_Monitor(*rest):
    	import os, ael
	try:
    	    status=os.system('start Y:\\Jhb\\Arena\\ini\\CQS_MonitorApps\\PROD\\XTP_Monitor_Application\\FeedV3ControlApplication.exe')
	except:
	    ael.log('XTP Real Time Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('XTP_Monitor loading...')	
    	return status

XTP_Monitor()
