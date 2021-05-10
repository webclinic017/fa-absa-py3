"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Re-generate cashflows for an instrument selection.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Paul Jacot-Guillarmod
CR NUMBER               :  494829

-----------------------------------------------------------------------------"""

import acm

def update_cashflows(instruments):
    for instrument in instruments:
        instrument.SLGenerateCashflows()

ael_variables = [('instruments', 'Re-Generate Cashflows', 'FInstrument', None, None, 0, 1)]

def ael_main(args):
    instruments = args['instruments']
    update_cashflows(instruments)

