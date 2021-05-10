""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FReratePerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FReratePerform - Module which reates selected instruments.

DESCRIPTION
    This module executes the rerate procedure based on the
    parameters passed from the script FRerate.


----------------------------------------------------------------------------"""
#Import builtin modules

import time
import FBDPString

#Import Front modules

import ael
import acm
logme = FBDPString.logme
from FBDPCommon import Summary
hook = False
w = None

try:
    from FSpreadHook import rerate_spread
    from FSpreadHook import Wrapper
except ImportError:
    pass
else:
    hook = rerate_spread
    w = Wrapper( None )

def supportedLegType( legType ):
    return legType in ( 'Call Float', 'Call Fixed Adjustable', 'Fixed Adjustable' )

def rerate(args):
    if hook:
        logme('rerate_spread hook enabled!')
        hook_fn = hook
    logme('rate: %f' % (args['rate']))
    rate = args['rate']
    no_date_input = False
    if len(args['date']) == 0:
        no_date_input = True
    else:
        date = ael.date( args['date'] )

    for i in args['instruments']:
        ins = ael.Instrument[i.Oid()]
        if ins.open_end == 'Open End':
            for leg in ins.legs():
                if supportedLegType( leg.type ):
                    spread = 0.0;
                    if hook:
                        spread = hook_fn( ins, w )
                    logme('spread: %f' % ( spread ))
                    logme('new rate: %f' % ( rate + spread ))
                    if no_date_input:
                        date = leg.end_day
                    ins_copy = ins.clone()
                    ins_copy.re_rate( date, rate + spread ) 
        else:
            logme('Ignored non open end instrument {0}'.format(i.Name()) )

    Summary().log(args)



