"""-----------------------------------------------------------------------------
MODULE	    	SAFEX_RT_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for SAFEX RT Trade Monitor purposes.
It executes the SAFEX RT Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add SAFEX_RT_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def SAFEX_RT_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\Safex_RT_Monitor_Application\\FeedMonitoringApplication.exe "SAFEX RT Trade Monitor"')
	except:
	    ael.log('SAFEX RT Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('SAFEX RT Feed Screen loading...')	
    	return status

SAFEX_RT_Feed()
