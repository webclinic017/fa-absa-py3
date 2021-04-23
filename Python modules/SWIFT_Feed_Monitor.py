"""-----------------------------------------------------------------------------
MODULE	    	SWIFT_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for SWIFT Trade Monitor purposes.
It executes the SWIFT Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add SWIFT_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def SWIFT_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\Swift_Monitor_Application\\FeedV3ControlApplication.exe"')
	except:
	    ael.log('SWIFT Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('SWIFT Feed Screen loading...')	
    	return status

SWIFT_Feed()
