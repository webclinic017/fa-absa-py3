"""-----------------------------------------------------------------------------
MODULE
    ACS_move_trades

DESCRIPTION
    Date                : 2017-05-04
    Purpose             : Move all ACS trades from *TRD to *STL portfolio
    Department and Desk : ACS
    Requester           : Raymond Phillips
    Developer           : Ondrej Bahounek
    CR Number           : 4527387
ENDDESCRIPTION

HISTORY
=============================================================================================
Date       Change no    Developer          Description
---------------------------------------------------------------------------------------------
2017-05-04 4527387      Ondrej Bahounek    Initial implementation: ABITFA-4859
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)

PORTF_OLD_SUFFIX = "-TRD"
PORTF_NEW_SUFFIX = "-STL"

ael_variables = AelVariableHandler()
ael_variables.add("trade_filter",
                  label="Trades",
                  cls="FTradeSelection",
                  mandatory=True,
                  multiple=True)


def move_trade_to_portf(trade, portf):
    if trade.MirrorTrade() and trade.MirrorPortfolio().Name() == trade.PortfolioId():
        
        # consider main mirror trade as the trade with higher OID
        # this trade will be the one that's commited
        mirror_nbr = max([trd.Oid() for trd in acm.FTrade.Select('mirrorTrade=%d' %trade.Oid())])
            
        if mirror_nbr == trade.Oid():
            raise RuntimeError("Can't select mirror trade to trade %d" %trade.Oid())
        
        mirror_trade = acm.FTrade[mirror_nbr]
        try:
            mirror_trade.MirrorTrade().Portfolio(portf)
            trade.Commit()
        except:
            mirror_trade.MirrorPortfolio(portf)
            mirror_trade.Commit()
    else:
        trade.Portfolio(portf)
        trade.Commit()


def move_trades(trades):
    LOGGER.info("Trades to move: %d", len(trades))
    for toid in trades:
        trade = acm.FTrade[toid]
        portf = trade.PortfolioId()
        if portf.endswith(PORTF_OLD_SUFFIX):
            # replace portfolio suffix
            new_portf = portf[:portf.rfind(PORTF_OLD_SUFFIX)] + PORTF_NEW_SUFFIX
            LOGGER.info("Trade %d: '%s' --> '%s'", trade.Oid(), portf, new_portf)
            move_trade_to_portf(trade, new_portf)


def ael_main(ael_dict):
    tf = ael_dict["trade_filter"][0]
    LOGGER.info("Trade filter: '%s'", tf.Name())
    trades = [t.Oid() for t in tf.Trades()]
    move_trades(trades)
    LOGGER.info("Completed successfully.")
