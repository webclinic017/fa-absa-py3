"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NonZARMaturityAutoReleaseTasK

DESCRIPTION
    Auto-Releasing Non Zar Maturity Settlements For Deposits and FRN trade. Task to run at 2pm Business Days.
    Auto-Releasing Zar Maturities for Deposits at 10am Business days

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-19      FAOPS-393       Tawanda Mukhalela       Wandile Sithole         Non-Zar Deposits and FRN Autorelease on Matched MT320
2019-11-25      FAOPS-635       Tawanda Mukhalela       Wandile Sithole         Zar Deposits  Autorelease on Matched Maturity Notice
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
from MatchedNonZarMT320ConfirmationSTPHook import MatchedNonZarMT320ConfirmationSTPHook
from PICandOasisOutgoingMaturitiesSTPHook import PICandOasisOutgoingMaturitiesSTPHook


LOGGER = getLogger(__name__)


def ael_main(ael_parameters):
    LOGGER.info('Non Zar and Zar Maturities Settlement Auto-Release task Started ..')
    non_zar_hook = MatchedNonZarMT320ConfirmationSTPHook()
    zar_hook = PICandOasisOutgoingMaturitiesSTPHook()
    non_zar_query_folder = acm.FStoredASQLQuery['NonZar_Maturities_Deposit_FRN_Trades']
    zar_query_folder = acm.FStoredASQLQuery['Zar_Maturities_Deposit_Oasis_PIC']
    non_zar_trades_to_process = non_zar_query_folder.Query().Select()
    zar_trades_to_process = zar_query_folder.Query().Select()
    auto_release_maturity_settlement(non_zar_trades_to_process, non_zar_hook)
    auto_release_maturity_settlement(zar_trades_to_process, zar_hook)


def auto_release_maturity_settlement(trades, stp_hook):
    for trade in trades:
        for confirmation in trade.Confirmations():
            try:
                if not stp_hook.is_valid_confirmation(confirmation):
                    continue
                stp_hook.PerformSTP(confirmation)
                break
            except Exception as ex:
                message = "An exception occurred processing trade '{trade_oid}', "
                message += "skipping..."
                LOGGER.warning(message.format(trade_oid=trade.Oid()), exc_info=True)
