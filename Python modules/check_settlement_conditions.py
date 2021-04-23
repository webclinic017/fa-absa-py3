"""

This script is used to diagnose the filter condition on which 
the failure is occurring when settlement is not generated.

Date: 2015-09-08
Requester: Anwar Banoo
Developer: Manan Ghosh

"""

import acm, ael

from FSettlementParameters import tradeFilterQueries, preventSettlementCreationQueries

def log(message, status = True):

    if status:
        ael.log(message)

def check_conditions(trade,  logging = False):

    if trade:
        log( 'Trade filter queries check ')

        for tradeFilter in tradeFilterQueries:
            isTradeSatisfiedBy = acm.FStoredASQLQuery[tradeFilter].Query().IsSatisfiedBy(trade)
            log( '\n'*2  )
            log( "[%s] Trade Filter condition %s satisfied by trade [%i] " % (tradeFilter, (isTradeSatisfiedBy and 'is' or 'is not'), trade.Oid()))


ael_variables = [['Trade',  'Trade No',       'int', None, None, 0, 0],
                 ['Logging', 'Detailed logging', 'bool', [False, True], False, 0, 0]]


def ael_main(params):

    trade_id     = params['Trade']
    logging      = params['Logging']

    trade = None
    settlement = None

    if trade_id:
        trade = acm.FTrade[trade_id]


    check_conditions(trade,  logging)

    log( 'Check on the Trade/Settlement conditions completed !!')
