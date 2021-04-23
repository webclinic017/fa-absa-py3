"""-----------------------------------------------------------------------------
MODULE	    	HERMES JSE Monitor 

Version: 1.2

DESCRIPTION
This module is for HERMES JSE  Trade Monitor purposes.
It executes the HERMES JSE Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add HERMES JSE Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def JSE_HERMES_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\Hermes_Monitoring_Application\\FeedMonitoringApplication.exe "Hermes"')
	except:
	    ael.log('JSE HERMES Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('JSE HERMES Feed Screen loading...')	
    	return status

JSE_HERMES_Feed()

