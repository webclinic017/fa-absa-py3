""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
2001-07-24

MODULE
    FVolaMaint - Module which maintain volatility surfaces.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module maintain the volatility surfaces.

DATA-PREP
    All variables have to be set in this module.
    
    The variables that should be set are:
    aliastypes	String	    A list of alias
    volsuffix	String	    A list of volsuffix
    verbosity	int 	    Integer that indicate the level of information that
    	    	    	    will be generated in the AEL console

REFERENCES
    See modules FVolaMaintGeneral.

----------------------------------------------------------------------------"""
print 'Inside FVolaMaintExecute.'
try:
    import string
except ImportError:
    print 'The module string was not found.'
    print
try:
    import ael
except ImportError:
    print 'The module ael was not found.'
    print
try:
    import time
except ImportError:
    print 'The module time was not found.'
    print
try:
    import FVolaMaintGeneral
except ImportError:
    print 'The module FVolaMaintGeneral was not found.'
    print

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""

if __name__ == "__main__":
    import sys, getopt
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
	    	    	    	   'a:u:p:i:s:v:h:')
        if len(opts) < 3:
            print len(opts)
            raise getopt.error, ''
    except getopt.error, msg:
        print msg
        m = '''Usage: FVolaMaint.py -a ads_address -u username -p password
	[-i AliasType -s VolSuffix -v verbosity -h help]'''
        print m
        sys.exit(2)

    atlas_passw = ''
    aliastypes = ["EUREX", "SAX"]
    volsuffix = ["_SETTLE", "_LAST"]
    verbosity = 1
    
    for o, a in opts:
        if o == '-a': ads_address = a
        if o == '-u': atlas_user = a
        if o == '-p': atlas_passw = a
	if o == '-i': aliastypes = a
	if o == '-s': 
	    volsuffix = eval(sys.argv[a])
        if o == '-v': verbosity = a
        if o == '-h': help_text()

    ael.connect(str(ads_address), str(atlas_user), str(atlas_passw))
    
    FVolaMaintGeneral.update_volsurface(volsuffix, aliastypes)
    
    print
    print "Volatility maintenance finished", time.ctime(time.time())
    
    rec = 'fred@front.com'
    subj = 'Volatility maintenance'
    msg = 'has been succesful!'
   
    #ael.sendmail(rec, subj, msg)
    
    ael.disconnect()
else:
   
    aliastypes = ["EUREX", "SAX"]
    volsuffix = ["_SETTLE", "_LAST"]
    verbosity = 1
    
    FVolaMaintGeneral.update_volsurface(volsuffix, aliastypes)
    
    print
    print "Volatility maintenance finished", time.ctime(time.time())
    
    rec = 'fred@front.com'
    subj = 'Volatility maintenance'
    msg = 'has been succesful!'
   
    #ael.sendmail(rec, subj, msg)
