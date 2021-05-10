"""---------------------------------------------------------------------------------------------------------------------
MODULE
    demat_dis_total_issue_update

DESCRIPTION
    This module updates the Total Issuse Size of all DIS & Demat instruments with the 'Authorised Nominal' amount from
    the 'DIS ISIN Management' and 'MM ISIN Management' business processes, respectively.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-05-07      FAOPS-784       Ntokozo Skosana         Martin Wortmann         Initial Implementation.
------------------------------------------------------------------------------------------------------------------------
"""
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from demat_isin_mgmt_menex import current_ins_authorised_amount


DIS_ISIN_REQUEST_STATE_CHART_NAME = 'DIS ISIN Management'
MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'
LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
state_chart_names = [DIS_ISIN_REQUEST_STATE_CHART_NAME, MMSS_ISIN_REQUEST_STATE_CHART_NAME]


def get_business_processes(state_chart_name):
    """
    Takes state chart name as an input and returns business processes in that state-chart.
    """
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    state_chart_node = asql_query.AddOpNode('AND')
    state_chart_node.AddAttrNode('StateChart.Name', 'EQUAL', state_chart_name)
    return asql_query.Select()


def ael_main(params):

    no_of_instruments_updated = 0

    for state_chart_name in state_chart_names:
        LOGGER.info('---------------------------- {} ----------------------------'.format(state_chart_name))
        business_processes = get_business_processes(state_chart_name)

        no_of_instruments_updated_in_state_chart = 0

        for bp in business_processes:
            instrument = bp.Subject()
            try:
                if instrument.TotalIssued != current_ins_authorised_amount(instrument):
                    instrument.TotalIssued = current_ins_authorised_amount(instrument)
                    instrument.Commit()
                    no_of_instruments_updated_in_state_chart += 1
                    no_of_instruments_updated += 1
            except Exception as ex:
                LOGGER.info(ex)
                continue

        LOGGER.info('No. of instruments updated in {} business process: {}'
                    .format(state_chart_name, no_of_instruments_updated_in_state_chart))

    LOGGER.info('Total no. of instruments update: {}'.format(no_of_instruments_updated))
