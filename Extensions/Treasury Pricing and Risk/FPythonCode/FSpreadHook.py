from __future__ import print_function
""" PRIME 4.0.0.p4 """

"""
--------------------------------------------------------------------------
MODULE
    FSpreadHook - Module where customization can be done.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module contains a number of AEL hook function templates, which,
    if defined, is called by BDP Fixing.
    Customers can do their own customization for 

RENAME Remove "_template" from those functions that should be called and used.
--------------------------------------------------------------------------
"""

import ael
import string
from FBDPString import logme
import FBDPInstrument
import ArenaFunctionBridge

"""aef-------------------------------------------------------------------------
hook::calculate_spread

Module: **FSpreadHook**

@param reset:Reset

    This hook is called from the Fixing script. If a value is returned, this value
    will become the spread for the reset. Rename the function to 'calculate_spread'
    to activate it. Creates a new file, the file format should be as the following table. 
    Places the file in any directory and changes filename string correspondingly.
    
#   Balance	    Spread Long Position (+)	Spread Short Position (-)
    50000                  -.25                             -.25
    1000000	              0.5			             0.5
    2000000	              0.75			            0.75
    5000000	              0.75			            0.85
    10000000	              0.85			             0.9
    15000000	               0.9			            0.95
----------------------------------------------------------------------------"""


def calculate_spread_template(reset, wrapper ):
    if( wrapper.obj == None ):  # use wrapper to avoid loading the file multiple times
        filename = 'c:\\SpreadTiers.txt'
        token = ''
        wrapper.obj = CalculateSpread( filename, token ) 
    cs = wrapper.obj

    cashFlow = reset.parent()
    leg = cashFlow.parent()
    trade = leg.parent().trades().members()[0]
    balance = 0
    loan = True
    for cf in leg.cash_flows():
        if( cf.type == 'Redemption Amount' ):
            balance = ArenaFunctionBridge.cashflow_projected_cf(cf.cfwnbr)*trade.quantity
            if( balance < 0 ):  
                balance = -balance
                loan = False
            break

    pair = cs.get_spread( balance )
    if( loan ):
        spread = pair[1]
    else: 
        spread = pair[0]
    return spread
    
"""aef-------------------------------------------------------------------------
hook::rerate_spread

Module: **FSpreadHook**

@param instrument:Instrument

    This hook is called from the FPerformRerate script. If a value is returned, this value
    will become the spread for the instrument. Rename the function to 'rerate_spread'
    to activate it. The input file format is the same as the above.
    
----------------------------------------------------------------------------"""
  
def rerate_spread_template(ins, wrapper ):
    if( wrapper.obj == None ):  # use wrapper to avoid loading the file multiple times
        filename = 'c:\\RerateSpread.txt'
        token = ''
        wrapper.obj = CalculateSpread( filename, token ) 
    cs = wrapper.obj

    leg = ins.legs()[0]
    trade = ins.trades().members()[0]
    #print ('leg type:', leg.type)
    balance = 0
    loan = True
    for cf in leg.cash_flows():
        if( cf.type == 'Redemption Amount' ):
            balance = ArenaFunctionBridge.cashflow_projected_cf(cf.cfwnbr)*trade.quantity
            if( balance < 0 ):
                balance = -balance
                loan = False
            break

    pair = cs.get_spread( balance )
    if( loan ):
        spread = pair[1]
    else: 
        spread = pair[0]
    return spread

class Wrapper:
    def __init__( self, obj ):
        self.obj = obj

class CalculateSpread:
    def __init__(self, filename, token ):
        self.spreads = [ ( 0, 0, 0 ) ]
        self.filename = filename
        self.token = token
        self.readfile()
           
    def readfile( self ):
        try:
            f = open( self.filename, 'r')
            for line in f:
                if( len(line) == 0 or line.isspace() ):
                    continue
                if line[0] == '#':
                    continue
                if( len(self.token) == 0 ):
                    x = line.split()
                else: 
                    x = line.split(self.token)
                #print (float(x[0]), float(x[1]), float(x[2]))
                self.spreads.append( (float(x[0]), float(x[1]), float(x[2])) )
                
            f.close()
        except IOError:
            print ('I/O error: Failed to open file: ' + self.filename)
        except:
            print ('Unexpected error while reading ' + self.filename)
            f.close()

        return 0

    def get_spread( self, balance ):
        for record in self.spreads:
            up_bound = record[0]
            if ( balance < up_bound or balance == up_bound ):
                return (record[1], record[2])
        return (0, 0)
       
