"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        Regenerate selected loans
DESK                 :  SBL PCG
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-03  CHG0102113     Libor Svoboda       Initial Implementation
"""
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from sbl_monthly_fee_payments import regenerate_cashflows


LOGGER = getLogger(__name__)


ael_variables = AelVariableHandler()
ael_variables.add(
    'loans',
    label='Sec loan trades',
    cls='FTrade',
    multiple=True,
)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    loans = ael_params['loans']
    LOGGER.info('Selected %s loans to regenerate.' % len(loans))
    for trade in loans:
        instrument = trade.Instrument()
        try:
            regenerate_cashflows(instrument)
        except:
            LOGGER.exception('Trade %s: failed to regenerate instrument %s.' 
                             % (trade.Oid(), instrument.Name()))
        else:
            LOGGER.info('Trade %s: Regenerated instrument %s.' 
                        % (trade.Oid(), instrument.Name()))
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
