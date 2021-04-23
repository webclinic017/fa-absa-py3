"""-----------------------------------------------------------------------------
MODULE	    	YieldX_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for YieldX Trade Monitor purposes.
It executes the CQS YieldX Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add YieldX_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def YieldX_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start Y:\Jhb\Arena\ini\CQS_MonitorApps\PROD\YieldX_Monitoring_Applications\\FeedMonitoringApplication.exe')
	except:
	    ael.log('YieldX Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('YieldX Feed Screen loading...')	
    	return status

YieldX_Feed()

