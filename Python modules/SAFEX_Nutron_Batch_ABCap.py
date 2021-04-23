"""-----------------------------------------------------------------------------
MODULE	    	SAFEX_Nutron_Batch_Monitor  

Version: 1.1

DESCRIPTION
This module is for SAFEX_Nutron_Batch_Monitor purposes.
It executes the SAFEX_Nutron_Batch_Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add SAFEX_Nutron_Batch_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def SAFEX_Nutron_Batch_Monitor(*rest):
    	import os, ael
	try:
    	    status=os.system('start Y:\\Jhb\\Arena\\ini\\CQS_MonitorApps\\PROD\\MITS_BATCH_Monitoring_Application\\FeedMonitoringApplication.exe "SAFEX_Nutron_Batch_ABCap"')
	except:
	    ael.log('SAFEX Batch Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('SAFEX_Nutron_Batch_Monitor loading...')	
    	return status

SAFEX_Nutron_Batch_Monitor()
