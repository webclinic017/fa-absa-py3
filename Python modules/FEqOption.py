""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""-----------------------------------------------------------------------------
MODULE
    FEqOption - Valuation of plain vanilla options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Calculates the theoretical price of an option. 
    European and American options with discrete dividends are handled.

-----------------------------------------------------------------------------"""
import ael
import FOptionParams

"""-----------------------------------------------------------------------------
FUNCTION        
    pv() 

DESCRIPTION
    Calculates the theoretical price of a plain vanilla option. 

ARGUMENTS
    i           Instrument      Plain vanilla option to be valued
    calc        int             Flag specifying whether a theoretical price
                                should be calculated or not.  0=>No calculation 
                                1=>Perform calculation
    ref                         Optimisation parameter.

RETURNS
   [res         float           Value of instrument
    expday      date            Maturity date
    curr        string          Currency in which the option was valued
    fixed       string          Constant = 'Fixed']                                     
-----------------------------------------------------------------------------"""
def pv(i,calc=1,ref=0):
    try:
        extra_days = 0
        if calc:        
            optionParams = FOptionParams.FOptionParams(i)   
            res = optionParams.pv()     
            extra_days = optionParams.extra_days
        else: res = 0.0
    except FOptionParams.FOptionError, msg:
        print '\nModule: FEqOption'
        print 'Error :', msg
        print 'Instr :', i.insid
        res = 0.0
    return [ [ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ] ]
        
        




