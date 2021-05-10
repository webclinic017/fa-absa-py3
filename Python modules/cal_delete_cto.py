"""-----------------------------------------------------------------------------
PURPOSE              :  Script that deletes custom text objects used in the CAL 
                        process.
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2018-11-13  CHG1001100033  Libor Svoboda       Initial Implementation
"""
import acm
from at_logging import getLogger
from cal_config import CTO_SUBTYPE


LOGGER = getLogger(__name__)

ael_variables = []


def ael_main(_kwargs):
    LOGGER.msg_tracker.reset()
    ctos = acm.FCustomTextObject.Select('subType="%s"' % CTO_SUBTYPE)
    LOGGER.info('Found %s CTOs with subtype %s.' % (len(ctos), CTO_SUBTYPE))
    for cto in ctos[:]:
        cto_name = cto.Name()
        try:
            cto.Delete()
        except:
            LOGGER.exception('Failed to delete CTO "%s".' % cto_name)
        else:
            LOGGER.info('Deleted CTO "%s".' % cto_name)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
