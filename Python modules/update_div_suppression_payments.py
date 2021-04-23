import time

import acm
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add("portfolio",
                  label="Portfolio",
                  cls=acm.FPhysicalPortfolio,
                  collection=sorted(acm.FPhysicalPortfolio.Select("")))
ael_variables.add_bool("dry_run",
                  label="Dry run")           

def ael_main(config):
    # Portfolio to be updated
    start = time.time()
    portfolio = config["portfolio"]
    dry_run = config["dry_run"]
    for trade in portfolio.Trades():
        for payment in trade.Payments():
            if payment.Type() == "Cash" and payment.Text() == "DividendSuppression":
                print("Updating payments on trade {0}".format(trade.Oid()))
                if not dry_run:
                    payment.Type("Dividend Suppression")
                    payment.Text("")
                    payment.Commit()
                print("Payment updated")
    end = time.time()
    print("Completed sucessfully in {0} seconds".format(end - start))
