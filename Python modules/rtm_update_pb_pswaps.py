import acm

import os
import acm
import csv
import time
from at_time import to_datetime
from at_ael_variables import AelVariableHandler

pswap_list = [
    "RTM_40923",
    "RTM_41293",
    "RTM_41350",
    "RTM_47324",
    "RTM_48694",
    "RTM_60814",
    "RTM_47365",
    "RTM_47332",
    "RTM_60392",
    "RTM_60772",
    "RTM_48389",
    "RTM_60129_EqPairs_LT",
    "RTM_60798",
    "RTM_60491",
    "RTM_60822",
    "RTM_60632",
    "RTM_60616",
    "RTM_60905",
    "RTM_60962",
    "RTM_60970",
    "RTM_60996",
    "RTM_61077",
    "RTM_61028",
    "RTM_61127"
]

ael_variables = AelVariableHandler()

def ael_main(config):
    errors = []
    count = 0
    pswap_len = len(pswap_list)
    start_all = time.time()
    for pswap in pswap_list:
        try:
            start = time.time()
            count += 1
            print("Processing DealPackage {0} ({1}/{2})".format(pswap, count, pswap_len))
            dealpackage = acm.FDealPackage.Select01("instrumentPackage='{0}'".format(pswap), None)
            if dealpackage:
                editable = dealpackage.Edit()
                pswap_link = editable.InstrumentPackage().InstrumentLinks()[0]
                synthetic_portfolio = pswap_link.Instrument().FundPortfolio()
                trades = sorted(synthetic_portfolio.Trades(), key=lambda t: t.CreateTime())
                new_start_date = trades[0].CreateTime()
                date = str(to_datetime(new_start_date)).split(" ")[0]
                print("\tFirst trade booked in portfolio {0} on {1}".format(synthetic_portfolio.Name(), date))
                if date >= pswap_link.Instrument().StartDate():
                    print("\tWARNING: PSwap was booked before ({0}) the first date - no date adjustments needed".format(pswap_link.Instrument().StartDate()))
                else:
                    pswap_link.Instrument().StartDate(date)
                    print("\tPSwap's start date for {0} set to {1}".format(pswap, date))
                    pswap_trades = acm.FPortfolioSwap[pswap].Trades()
                    for trade in pswap_trades:
                        trade.TradeTime(date)
                        trade.Commit()
                        print("\t\tTrade Time for {0} set to {1} ({2})".format(trade.Oid(), date, trade.Portfolio().Name()))
                editable.SetAttribute('cashEnabled', False)
                print("\tPSwap's cash leg disabled")
                savedDp = editable.Save().First()
                end = time.time()
                print("\tSuccessfully updated DealPackage {0} in {1} seconds".format(pswap, end - start))
            else:
                err_msg = "ERROR: DealPackage {0} not found".format(pswap)
                errors.append(err_msg)
                print(err_msg)
        except Exception as ex:
            err_msg = "ERROR: Processing of DealPackage {0} failed: {1}".format(pswap, ex)
            errors.append(err_msg)
            print(err_msg)
        print()
    end_all = time.time()
    if errors:
        print("Completed in {0} seconds with following errors:".format(end_all - start_all))
        for err_msg in errors:
            print("\t", err_msg)
    else:
        print("Completed successfully in {0} seconds.".format(end_all - start_all))
