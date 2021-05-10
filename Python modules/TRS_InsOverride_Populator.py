"""-----------------------------------------------------------------------------
MODULE
    TRS_InsOverride_Populator

DESCRIPTION
    Date                : 24/10/2018
    Purpose             : To automate the identification and population of TRS
                          deals with no insoverride in addinfo.
    Department and Desk : PCG
    Requester           : Nhlanhleni Mchunu
    Developer           : John Moss, Qaqamba Ntshobane
    CR Number           : TODO

HISTORY
================================================================================
Date                Change no               Developer               Description
--------------------------------------------------------------------------------

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import at_addInfo
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)


def get_ael_variables():

    variables = AelVariableHandler()
    variables.add('insoverride',
                  label='InsOverride Option',
                  default='Total Return Swap - Bond',
                  alt='Value to populate the InsOverride field with'
                  )
    variables.add('portfolio',
                  label='Portfolio',
                  default='JOB16',
                  alt='Portfolio where the TRS deals will be found'
                  )
    return variables

ael_variables = get_ael_variables()


def ael_main(params):

    num_of_trades = 0
    portf = params['portfolio']
    insoverride = params['insoverride']
    portfolio = acm.FPhysicalPortfolio[portf]

    try:
        for trade in portfolio.Trades():
            ins = trade.Instrument()

            if ins.InsType() == 'TotalReturnSwap' and\
               trade.add_info('InsOverride') == '' and not\
               trade.Status() in ['Void', 'Terminated'] and not\
               ins.IsExpired():

                LOGGER.info('Trade Number: %s', trade.Oid())
                at_addInfo.save_or_delete(trade, 'InsOverride', insoverride)
                num_of_trades += 1

        LOGGER.info('Run  Date: %s', acm.Time.DateToday())
        LOGGER.info('Number of Trades Updated: %s' % (num_of_trades))
        LOGGER.info('Completed Succefully!')

    except Exception:
        LOGGER.info('Failed to update trades.')
        raise
    
