"""-----------------------------------------------------------------------------
MODULE	    	SAFEX_Nutron_RT_Monitor 

Version: 1.1

DESCRIPTION
This module is for SAFEX_Nutron_RT_Monitor purposes.
It executes the SAFEX_Nutron_RT_Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add SAFEX_Nutron_RT_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def SAFEX_Nutron_RT_Monitor(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\MITS_RT_Monitoring_Application\\FeedMonitoringApplication.exe "SAFEX_Nutron_RT"')
	except:
	    ael.log('SAFEX Real Time Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('SAFEX_Nutron_RT_Monitor loading...')	
    	return status

SAFEX_Nutron_RT_Monitor()
