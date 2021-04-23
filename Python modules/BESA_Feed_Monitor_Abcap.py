"""-----------------------------------------------------------------------------
MODULE	    	BESA_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for BESA Trade Monitor purposes.
It executes the CQS BESA Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add BESA_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def BESA_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start Y:\\Jhb\\Arena\\ini\\CQS_MonitorApps\\PROD\\BESA_Monitoring_Application\\FeedV3ControlApplication.exe "Besa Trade Abcap"')
	except:
	    ael.log('BESA Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('BESA Feed Screen loading...')	
    	return status

BESA_Feed()
