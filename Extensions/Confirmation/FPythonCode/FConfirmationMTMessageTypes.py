""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationMTMessageTypes.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationMTMessageTypes - used for MTMessages column in Prime/ATS

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm
import FOperationsUtils as Utils
import FSwiftMessageTypeCalculator as Calculator

def PreviewConfirmation(confirmation):
    mt = Calculator.Calculate(confirmation)
    if mt:
        return str(mt)
    return ''

ael_variables = [('confirmation_oid', 'Confirmation Oid', 'int', [], '0', 0)]
def ael_main(dictionary):
    ''' ael_main and ael_variables are used for diaplaying a preview of the
    document from the Operations Manager Application.'''
    confirmation_oid = int(dictionary['confirmation_oid'])
    try:
        confirmation = acm.FConfirmation[confirmation_oid]
        if confirmation:
            # check because trade might have been voided and confirmation recalled
            return PreviewConfirmation(confirmation)
    except Exception as e:
        Utils.LogAlways('Error while receiving  MT type: %s' % (e))
    return ""
