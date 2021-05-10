""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementMTMessageTypes.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementMTMessageTypes - used for MTMessages column in Prime/ATS

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm
import FOperationsUtils as Utils
import FSwiftMessageTypeCalculator as Calculator

def PreviewSettlement(settlement):
    mt = Calculator.Calculate(settlement)
    if mt:
        return str(mt)
    return ''

ael_variables = [('settlement_oid', 'Settlement Oid', 'int', [], '0', 0)]
def ael_main(dictionary):
    ''' ael_main and ael_variables are used for diaplaying a preview of the
    document from the Operations Manager Application.'''
    settlement_oid = int(dictionary['settlement_oid'])
    try:
        settlement = acm.FSettlement[settlement_oid]
        if settlement:
            # check because trade might have been voided and settlement recalled
            return PreviewSettlement(settlement)
    except Exception as e:
        Utils.LogAlways('Error while receiving  MT type: %s' % (e))
    return ""
