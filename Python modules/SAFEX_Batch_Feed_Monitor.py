"""-----------------------------------------------------------------------------
MODULE	    	SAFEX_Batch_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for SAFEX Batch Trade Monitor purposes.
It executes the SAFEX Batch Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add SAFEX_Batch_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def SAFEX_Batch_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\Safex_Batch_Monitor_Application\\FeedMonitoringApplication.exe "SAFEX Batch Trade Monitor"')
	except:
	    ael.log('SAFEX Batch Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('SAFEX RT Feed Screen loading...')	
    	return status

SAFEX_Batch_Feed()
