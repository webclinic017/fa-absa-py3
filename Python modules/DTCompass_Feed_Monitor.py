"""-----------------------------------------------------------------------------
MODULE	    	DTCompass_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for DTCompass Trade Monitor purposes.
It executes the CQS DTCompass Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add DTCompass_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def DTCompass_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\DTCompass_Monitoring_Application\\FeedV3ControlApplication.exe')
	except:
	    ael.log('DTCompass Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('DTCompass Feed Screen loading...')	
    	return status

DTCompass_Feed()

