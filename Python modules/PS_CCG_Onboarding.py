"""
-----------------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2018-10-02                  Tibor Reiss           Use transactions

This module is used by CCG for their part
of the prime brokerage funds' onboarding process.

It only adds add infos but need to be separated
because only this team is allowed to modify
counterparties in FA.
"""


import acm

from at_ael_variables import AelVariableHandler
from at_logging import bp_start, getLogger
from pb_quirk import (CallAccountQuirk,
                      CollateralPortfolioQuirk,
                      CommoditiesCallAccountQuirk,
                      LoanAccountQuirk,
                      ReportingPortfolioQuirk,
                      SafexCallAccountQuirk,
                      YieldXCallAccountQuirk)
from PS_Functions import get_pb_fund_shortname


LOGGER = getLogger()


ael_variables = AelVariableHandler()
ael_variables.add("counterparty",
                  label="Counterparty",
                  alt="A counterparty to update",
                  cls=acm.FCounterParty,
                  collection=acm.FCounterParty.Select(""))
ael_variables.add("reporting_portfolio",
                  label="Reporting portfolio",
                  alt="Fund's main reporting portfolio",
                  cls=acm.FPhysicalPortfolio,
                  mandatory=False)
ael_variables.add("collateral_portfolio",
                  label="Collateral portfolio",
                  alt="Fund's collateral portfolio",
                  cls=acm.FPhysicalPortfolio,
                  mandatory=False)
ael_variables.add("call_account",
                  label="Call account",
                  alt="Fund's call account",
                  cls=acm.FInstrument,
                  mandatory=False)
ael_variables.add("loan_account",
                  label="Loan account",
                  alt="Fund's loan account",
                  cls=acm.FInstrument,
                  mandatory=False)
ael_variables.add("commodities_call_account",
                  label="Commodities call account",
                  alt="Fund's commodities call account",
                  cls=acm.FInstrument,
                  mandatory=False)
ael_variables.add("safex_call_account",
                  label="SAFEX call account",
                  alt="Fund's SAFEX call account",
                  cls=acm.FInstrument,
                  mandatory=False)
ael_variables.add("yieldx_call_account",
                  label="YieldX call account",
                  alt="Fund's YieldX call account",
                  cls=acm.FInstrument,
                  mandatory=False)


def ael_main(parameters):
    LOGGER.msg_tracker.reset()
    counterparty = parameters["counterparty"]
    reporting_portfolio = parameters["reporting_portfolio"]
    collateral_portfolio = parameters["collateral_portfolio"]
    call_account = parameters["call_account"]
    loan_account = parameters["loan_account"]
    commodities_call_account = parameters["commodities_call_account"]
    safex_call_account = parameters["safex_call_account"]
    yieldx_call_account = parameters["yieldx_call_account"]
    short_name = get_pb_fund_shortname(counterparty)
    process_name = 'ps.onboarding.ccg.{0}'.format(short_name)
    with bp_start(process_name):
        acm.BeginTransaction()
        try:
            LOGGER.info("Updating counterparty '%s'", counterparty.Name())
            if reporting_portfolio is not None:
                counterparty.AddInfoValue(ReportingPortfolioQuirk.ADD_INFO_NAME,
                                          reporting_portfolio)
            if collateral_portfolio is not None:
                counterparty.AddInfoValue(CollateralPortfolioQuirk.ADD_INFO_NAME,
                                          collateral_portfolio)
            if call_account is not None:
                counterparty.AddInfoValue(CallAccountQuirk.ADD_INFO_NAME,
                                          call_account)
            if loan_account is not None:
                counterparty.AddInfoValue(LoanAccountQuirk.ADD_INFO_NAME,
                                          loan_account)
            if commodities_call_account is not None:
                counterparty.AddInfoValue(CommoditiesCallAccountQuirk.ADD_INFO_NAME,
                                          commodities_call_account)
            if safex_call_account is not None:
                counterparty.AddInfoValue(SafexCallAccountQuirk.ADD_INFO_NAME,
                                          safex_call_account)
            if yieldx_call_account is not None:
                counterparty.AddInfoValue(YieldXCallAccountQuirk.ADD_INFO_NAME,
                                          yieldx_call_account)
            counterparty.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            LOGGER.exception("Add infos could not be saved.")
        if LOGGER.msg_tracker.errors_counter:
            raise RuntimeError("ERRORS occurred. Please check the log.")
        else:
            LOGGER.info("Counterparty '%s' has been updated successfully.",
                        counterparty.Name())
