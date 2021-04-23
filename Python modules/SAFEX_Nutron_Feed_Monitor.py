"""-----------------------------------------------------------------------------
MODULE	    	SAFEX_Nutron_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for SAFEX_Nutron_Feed_Monitor purposes.
It executes the SAFEX_Nutron_Feed_Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add SAFEX_Nutron_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def SAFEX_Nutron_Feed_Monitor(*rest):
    	import os, ael
	try:
    	    status=os.system('start Y:\\Jhb\\Arena\\ini\\CQS_MonitorApps\\PROD\\Safex_Monitor_Application\\SafexFeedMonitorv3.exe')
	except:
	    ael.log('SAFEX Nutron Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('SAFEX_Nutron_Monitor_Application loading...')	
    	return status

SAFEX_Nutron_Feed_Monitor()
