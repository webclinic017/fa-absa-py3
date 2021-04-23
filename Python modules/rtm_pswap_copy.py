"""
Description: Bulk booking of portfolio swaps as a copy of the existing one.
Project: Risk Transfer Mechanism
Developer: Jakub Tomaga
Date: 06/12/2017
"""

import acm
import csv
import time
from at_ael_variables import AelVariableHandler


def rtm_name(book):
    """Construct RTM portfolio swap name."""
    name = "RTM_" + book.replace("ACS RTM - ", "").replace("ACS RTM ST - ", "").replace(" ", "_")
    return name


def copy_pswap(original, name, acs_portfolio, absa_portfolio, acs_cpty, acs_acquirer, synthetic_portfolio, start_date):
    """Copy a deal package and book the second leg of the portfolio swap."""
    acm.BeginTransaction()
    try:       
        # Copy first portfolio swap
        dealpackage = original.Copy()
        dealpackage.InstrumentPackage().Name(name)
        
        # Set up trade for ACS leg of the RTM
        dealpackage.TradeLinks()[0].Trade().Portfolio(acs_portfolio)
        dealpackage.TradeLinks()[0].Trade().Counterparty(acs_cpty)
        dealpackage.TradeLinks()[0].Trade().Acquirer(acs_acquirer)
        dealpackage.TradeLinks()[0].Trade().ValueDay(start_date)
        dealpackage.TradeLinks()[0].Trade().AcquireDay(start_date)
        dealpackage.TradeLinks()[0].Trade().TradeTime(start_date)
        
        # Set up new instrument level attributes
        pswap_link = dealpackage.InstrumentPackage().InstrumentLinks()[0]
        pswap_link.Instrument().Name(name)
        pswap_link.Instrument().MtmFromFeed(False)
        pswap_link.Instrument().StartDate(start_date)
        pswap_link.Instrument().FundPortfolio(synthetic_portfolio)
        
        # Set up rate indices
        ml_link = dealpackage.InstrumentPackage().InstrumentLinks()[1]
        ml_link.Instrument().Name("ML_{0}".format(name))
        ml_link.Instrument().MtmFromFeed(False)
        cl_link = dealpackage.InstrumentPackage().InstrumentLinks()[2]
        cl_link.Instrument().Name("CL_{0}".format(name))
        cl_link.Instrument().MtmFromFeed(False)
        savedDp = dealpackage.SaveNew().First()
        
        # Delete all legs on the copied pswap
        for leg in list(savedDp.InstrumentPackage().InstrumentLinks()[0].Instrument().Legs()):
            leg.Delete()

        # Set up Bank leg of the RTM
        trade = savedDp.TradeLinks()[0].Trade()
        new_trade = trade.Clone()
        new_trade.Counterparty(trade.Acquirer())
        new_trade.Acquirer(trade.Counterparty())
        new_trade.Portfolio(absa_portfolio)
        new_trade.Quantity(-1 * trade.Quantity())
        new_trade.ValueDay(start_date)
        new_trade.AcquireDay(start_date)
        new_trade.TradeTime(start_date)
        new_trade.Commit()
        
        acm.CommitTransaction()
    except Exception as ex:
        acm.AbortTransaction()
        print("Did not create deal package {0}:{1}".format(name, ex))


ael_variables = AelVariableHandler()
ael_variables.add("input_file",
                  label="Input file")
ael_variables.add("start_date",
                  label="Start date")

def ael_main(config):
    """Entry point of the script."""
    master_start = time.time()
    dp = acm.FDealPackage.Select("")[0]
    input_file = config["input_file"]
    start_date = config["start_date"]
    with open(input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            original_book = row[0]
            synthetic_portfolio = row[1]
            acs_portfolio = row[2]
            acs_cpty = row[3]
            acs_acquirer = row[4]
            absa_portfolio = row[5]
            absa_cpty = row[6]
            absa_acquirer = row[7]
            skip = row[8]
            
            if skip == "FALSE":
                start = time.time()
                pswap_name = rtm_name(synthetic_portfolio)
                print("Creating deal package {0}".format(pswap_name))
                copy_pswap(dp, pswap_name, acs_portfolio, absa_portfolio, acs_cpty, acs_acquirer, synthetic_portfolio, start_date)
                end = time.time()
                print("Time elapsed: {0} seconds".format(end - start))
    master_end = time.time()
    print("Completed in {0} seconds".format(master_end - master_start))
