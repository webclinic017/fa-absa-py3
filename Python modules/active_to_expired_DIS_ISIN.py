"""---------------------------------------------------------------------------------------------------------------------
MODULE
    active_to_expired_DIS_ISIN

DESCRIPTION
    This module changes all ISINs in 'active' status that have Instrument end date < today to 'expired' status in the
     business process.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-02-19      FAOPS-690       Ntokozo Skosana         Seven Khoza             Initial Implementation.
2020-09-30      FAOPS-908       Ntokozo Skosana         Wandile Sithole         Use logger instead of print statements.
------------------------------------------------------------------------------------------------------------------------
"""
import acm
import datetime
from at_ael_variables import AelVariableHandler
from at_logging import getLogger

LOGGER = getLogger(__name__)
TODAYS_DATE = datetime.datetime.now()
DIS_ISIN_REQUEST_STATE_CHART_NAME = 'DIS ISIN Management'
past_expiry = acm.FStateChartEvent('Past expiry date')

ael_variables = AelVariableHandler()


def get_state_chart_status_of_isin(state_chart, status):
    """
    Return state chart in a specified status
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    state_chart_node = asql_query.AddOpNode('AND')
    state_chart_node.AddAttrNode('StateChart.Name', 'EQUAL', state_chart)
    state_chart_node.AddAttrNode('CurrentStateName', 'EQUAL', status)
    return asql_query.Select()


def ael_main(params):

    business_process = get_state_chart_status_of_isin(DIS_ISIN_REQUEST_STATE_CHART_NAME, 'Active')
    no_of_instruments_updated = 0

    for bp in business_process:
        try:
            instrument = bp.Subject()
            expiry_date = instrument.ExpiryDate()
            instrument_expiry = datetime.datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')

            if instrument_expiry < TODAYS_DATE:
                LOGGER.info('Updating instrument {0} to Expired in Business process {1}.'
                            .format(instrument.Name(), bp.Oid()))
                no_of_instruments_updated += 1
                bp.HandleEvent(past_expiry, params=None, notes=None)
                bp.Commit()
        except Exception as error:
            LOGGER.exception(error)
    if no_of_instruments_updated:
        LOGGER.info("{} instruments have been moved from active to expired status.".format(no_of_instruments_updated))
    else:
        LOGGER.info("No instruments that are in active status have passed their expiry date.")
