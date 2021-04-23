"""-----------------------------------------------------------------------------
MODULE	    	Fenics_Feed_Monitor 

Version: 1.1

DESCRIPTION
This module is for Fenics Trade Monitor purposes.
It executes the CQS Fenics Tradefeed Monitor Application from within Prime.
The AEL get intalled in File > Install AEL module.
Add Fenics_Feed_Monitor to a User rights Profile and allocate to relevant Back office users.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael

def Fenics_Feed(*rest):
    	import os, ael
	try:
    	    status=os.system('start \\\\V036SYB004001\\CQS_MonitorApps\\PROD\\Fenics_Monitoring_Application\\FeedMonitoringApplication.exe')
	except:
	    ael.log('Fenics Feed Monitor can not be started!')
	    ael.log('Consult IT for support.')
	ael.log('Fenics Feed Screen loading...')	
    	return status

Fenics_Feed()
