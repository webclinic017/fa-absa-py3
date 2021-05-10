"""-----------------------------------------------------------------------------
PURPOSE              :  Resend failed historical Sparks messages for specific 
                        date today.
                        This is run by RTB on demand.
REQUESTER, DEPATMENT :  Linda Breytenbach, OPS
PROJECT              :  Fix the Front - Sparks
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer              Description
--------------------------------------------------------------------------------
2018-07-19  CHG1000679237  Libor Svoboda          Initial Implementation
"""
import acm
import Sparks_Util
from at_logging import getLogger


LOGGER = getLogger(__name__)
DATE_TODAY = acm.Time.DateToday()

ael_variables = []


def ael_main(variables):
    sparks_util = Sparks_Util.SparksUtil(DATE_TODAY)
    sparks_util.connect_queue_manager()
    try:
        sparks_util.resend_failed_messages(DATE_TODAY)
    except Exception as exc:
        LOGGER.exception('Task failed: %s' % str(exc))
        raise
    else:
        LOGGER.info('Completed successfully')
    finally:
        sparks_util.disconnect_queue_manager()
