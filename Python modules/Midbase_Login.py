#Shortcut to Midbase Login from Prime.
def Midbase_Login(*rest):
    	import os, ael
	try:
    	    status=os.system('start C:\\ACMB\\Midbase\\Midbase.exe')
	except:
	    ael.log('Midbase Login can not be started!')
	    ael.log('Consult IT for support.')
	print "Midbase is not part of Prime."
	print "This link is only to jumpstart" 
	print "Midbase in Windows."
    	print "Please wait a few seconds for"
	print "the Midbase logon."
	ael.log('Midbase Login Screen loading...')	
    	return status

Midbase_Login()
