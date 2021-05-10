'''--------------------------------------------------------------------------------------
MODULE
    sbl_auto_bo_checker

DESCRIPTION
    Date                : 2020-05-25
    Purpose             : Help users check if a Security loan meets all the
                          SBL Auto BO rules and should be automatically BO confirmed
    Department and Desk : SBL and Collateral
    Requester           : Shaun Du Plessis, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-10

HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2020-05-25      PCGDEV-10      Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''

import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from PCG_SBL_Autoconfirm_FO_Trades import PCGAutoConfirmation

LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
ael_variables.add("trades",
                  label = "Trade numbers",
                  alt = "Trade numbers to try to auto bo",
                  default = "",
                  multiple=True,
                  mandatory = False)


def ael_main(dictionary):
    trades =  dictionary["trades"]
    if trades:
        sbl_engine = PCGAutoConfirmation(trades)
        for trade_number in trades:
            LOGGER.info("Processing trade {trd}".format(trd=trade_number))
            trade = acm.FTrade[trade_number]
            sbl_engine.verify(trade)
        sbl_engine.print_errors()
        LOGGER.info("Completed successfully")
    else:
        LOGGER.info("No SBL trades to check")
