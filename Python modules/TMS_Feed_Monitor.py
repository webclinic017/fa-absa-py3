"""-----------------------------------------------------------------------------
MODULE	    	TMS_Feed_Monitor 

Version: 1

DESCRIPTION
This module is for Front Arena to BarCap TMS Trade Monitor purposes.
It executes the CQS TMS Tradefeed Monitor Application from within Prime.
The AEL get installed in File > Install AEL module.
Add TMS_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
END DESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def TMS_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\TMS_Monitor_Application\\FeedV3ControlApplication.exe')
	except:
	    ael.log('TMS Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('TMS Feed Screen loading...')
    	return status

TMS_Feed()
