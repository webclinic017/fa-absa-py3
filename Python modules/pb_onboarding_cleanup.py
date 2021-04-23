"""-----------------------------------------------------------------------
DESCRIPTION
    Task for cleanup of failed on-boarding.

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
                         Jakub Tomaga       Initial iplementation
2019-06-26 CHG1001930222 Tibor Reiss        Update to be more generic
"""

import acm

from at_ael_variables import AelVariableHandler
from at_addInfo import delete as ai_delete
from at_logging import getLogger
from PS_Functions import get_pb_fund_counterparty


LOGGER = getLogger()


ael_variables = AelVariableHandler()
ael_variables.add("fund",
    label="Fund")
ael_variables.add("cfd_account",
    label="CFD Hedge Account",
    mandatory=False)
ael_variables.add_bool("dry_run",
    label="Dry run",
    default=True)
ael_variables.add_bool("portfolios",
    label="Delete portfolios")
ael_variables.add_bool("pswaps",
    label="Delete pswaps")
ael_variables.add_bool("call_accounts",
    label="Delete call accounts")
ael_variables.add_bool("trade_filters",
    label="Delete trade filters")
ael_variables.add_bool("query_folders",
    label="Delete query folder")
ael_variables.add_bool("tasks",
    label="Delete tasks")


def ael_main(config):
    fund = config["fund"]

    if config["call_accounts"]:
        deposits = acm.FDeposit.Select("name like '*{}*'".format(fund))
        acm.BeginTransaction()
        try:
            # Delete addinfos on party
            party = get_pb_fund_counterparty(fund)
            ai_delete(party, "PB_Call_Account")
            ai_delete(party, "PB_Loan_Account")
            # Delete confirmations if exist
            for deposit in deposits:
                trades = [t.Oid() for t in deposit.Trades()]
                for trdnbr in trades:
                    conf = acm.FConfirmation.Select('trade = {}'.format(trdnbr))
                    for c in conf[:]:
                        LOGGER.info("Deleting confirmation {}".format(c.Oid()))
                        c.Delete()
            if config["dry_run"]:
                acm.AbortTransaction()
                LOGGER.info("Dry run successful")
            else:
                acm.CommitTransaction()
                LOGGER.info("Deletion successful")
        except Exception as e:
            acm.AbortTransaction()
            msg = "Could not delete addinfos/confirmations!"
            LOGGER.exception(msg)
            raise RuntimeError("{} Error: {}".format(msg, e))
        acm.BeginTransaction()
        try:
            # Delete trades and instruments
            for deposit in deposits[:]:
                trades = [t.Oid() for t in deposit.Trades()]
                for trdnbr in trades:
                    LOGGER.info("Deleting trade {}".format(trdnbr))
                    acm.FTrade[trdnbr].Delete()
                LOGGER.info("Deleting deposit {}".format(deposit.Name()))
                deposit.Delete()
            if config["dry_run"]:
                acm.AbortTransaction()
                LOGGER.info("Dry run successful")
            else:
                acm.CommitTransaction()
                LOGGER.info("Deletion successful")
        except Exception as e:
            acm.AbortTransaction()
            msg = "Could not delete trades/deposits!"
            LOGGER.exception(msg)
            raise RuntimeError("{} Error: {}".format(msg, e))

    acm.BeginTransaction()
    try:
        if config["pswaps"]:
            pswaps = acm.FPortfolioSwap.Select("name like '*{}*'".format(fund))
            for pswap in pswaps[:]:
                if pswap.Trades():
                    LOGGER.info("Deleting trade {}".format(pswap.Trades()[0].Oid()))
                    pswap.Trades()[0].Delete()
                LOGGER.info("Deleting pswap {}".format(pswap.Name()))
                pswap.Delete()

        if config["portfolios"]:
            if config["cfd_account"]:
                portfolio = acm.FPhysicalPortfolio[config["cfd_account"]]
                LOGGER.info("Deleting portfolio {}".format(portfolio.Name()))
                portfolio.Delete()

            portfolios = acm.FPhysicalPortfolio.Select("name like '*{}*'".format(fund))
            for portfolio in portfolios[:]:
                LOGGER.info("Deleting portfolio {}".format(portfolio.Name()))
                portfolio.Delete()

        if config["trade_filters"]:
            trade_filters = acm.FTradeSelection.Select("name like '*{}*'".format(fund))
            for tf in trade_filters[:]:
                LOGGER.info("Deleting trade filter {}".format(tf.Name()))
                tf.Delete()

        if config["query_folders"]:
            query_folders = acm.FStoredASQLQuery.Select("name like '*{}*'".format(fund))
            for qf in query_folders[:]:
                LOGGER.info("Deleting query folder {}".format(qf.Name()))
                qf.Delete()

        if config["tasks"]:
            tasks = acm.FAelTask.Select("name like '*{}*'".format(fund))
            for task in tasks[:]:
                # Skip the on-boarding task
                if task.Name() == fund:
                    continue
                LOGGER.info("Deleting task {}".format(task.Name()))
                task.Delete()

        if config["dry_run"]:
            acm.AbortTransaction()
            LOGGER.info("Dry run successful")
        else:
            acm.CommitTransaction()
            LOGGER.info("Deletion successful")
    except Exception as e:
        acm.AbortTransaction()
        msg = "Deletion failed!"
        LOGGER.exception(msg)
        raise RuntimeError("{} Error: {}".format(msg, e))

    if not config["dry_run"]:
        LOGGER.info("Run successful")
