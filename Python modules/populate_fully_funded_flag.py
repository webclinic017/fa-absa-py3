"""
-------------------------------------------------------------------------------
MODULE
    populate_fully_funded_flag.py

DESCRIPTION
    Date                : 2015-10-06
    Purpose             : A correction script to populate financed/fully funded
                          flag per portfolio. Commit in transaction failed for
                          some clients during Prime Broker Strategic deployment
                          and we need to cater for those individually without
                          transaction commit (and commit per trade).
    Department and Desk : Prime Services Client Coverage
    Requester           : Sarshnee Pather
    Developer           : Jakub Tomaga
    CR Number           : CHNG0003159932

"""

import time
import acm
from at_ael_variables import AelVariableHandler
from at_addInfo import save as save_additional_info
from set_pswap_attributes import determine_fully_funded_flag


def populate_fully_funded_flag(portfolio, fully_funded):
    """Populate flag and commit without transaction."""
    trades = portfolio.Trades()
    trade_len = len(trades)

    failed_list = []
    counter = 1
    for trade in trades:
        try:
            save_additional_info(trade, "PB_Fully_Funded", fully_funded)
            print("Trade {0} modified ({1}/{2})".format(
                trade.Oid(), counter, trade_len))
            counter += 1
        except Exception as ex:
            failed_list.append((trade.Oid(), ex))

    if failed_list:
        print("Error occurred on following trades:")
        for trade_id, ex in failed_list:
            print("{0}: {1}".format(trade_id, ex))
    else:
        print("{0} trades amended.".format(trade_len))
        print("Completed successfully")


ael_variables = AelVariableHandler()
ael_variables.add("portfolio",
                  label="Portfolio",
                  cls=acm.FPhysicalPortfolio,
                  multiple=True)
ael_variables.add("portfolio_swap",
                  label="Portfolio swap",
                  cls=acm.FPortfolioSwap,
                  multiple=True)


def ael_main(config):
    """Entry point of the script."""
    portfolio = config["portfolio"][0]
    portfolio_swap = config["portfolio_swap"][0]
    fully_funded = determine_fully_funded_flag(portfolio_swap.Name())

    start_time = time.time()
    populate_fully_funded_flag(portfolio, fully_funded)
    end_time = time.time()
    print("Elapsed time: {0} seconds".format(end_time - start_time))
