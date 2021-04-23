"""Placeholder module.

This empty module is a placeholder used by users from FX TCU.
"""

ael_variables = []

import ael

def ael_main(parameters):
    #def test(bb):
    for item in ael.ServerData.select():
        if item.customer_name == 'Production':
            TESTMESSAGES = False
            print('Test environment parameter value is', TESTMESSAGES)
        else:
            print('Run using test message BICS =', TESTMESSAGES)
    return 'AAAA'
