""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementSOD - Module which executes the Start Day script for settlements

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt
    
    import ael, time, FSettlementParams, FSettlementEOD    
       
    ael_variables = [('new_to_stp_run', '"Start Day" - Run STP on settlements in status New', 'bool', [False, True], True)]

    def ael_main(dict):
        dict['eod_run'] = False
        pr = '<< "Start Day" - Run STP on settlements in status New - %s >>' % (__file__)
        ael.log(pr)
        FSettlementEOD.eod_start(dict, FSettlementParams.get_default_params())

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    ael.log('Could not run FSettlementSOD due to ')
    ael.log(str(e))


