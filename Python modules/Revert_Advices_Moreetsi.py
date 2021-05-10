import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import DocumentBusinessProcessGeneral
import DocumentGeneral
from PreSettlementAdviceGeneral import get_advice_state_chart_name, get_advice_event_name


LOGGER = getLogger(__name__)


ael_variables = AelVariableHandler()


ael_variables.add(
    'incident_number',
    label = 'Incident Number',
    cls = 'string',
    collection = None,
    default = None,
    mandatory = True,
    multiple = False,
    alt = 'The incident number logged for the errors.'
)


def ael_main(ael_parameters):
    incident_number = ael_parameters['incident_number']
    counterparties = set()
    # Revert to previous state.
    for business_process in get_active_advice_business_processes_in_error():
        try:
            message = "Pre-settlement advice {oid} found in 'Error' state, triggering revert "
            message += "to previous state."
            LOGGER.info(message.format(
                oid=business_process.Oid()
            ))
            revert_advice_business_process(business_process, incident_number)
            counterparties.add(business_process.Subject())
        except Exception as exception:
            LOGGER.exception(exception)
    # Trigger amendment check.
    for counterparty in counterparties:
        message = "Pre-settlement advice/s for counterparty '{counterparty_name}' reverted "
        message += "from 'Error' state, triggering amendment check..."
        LOGGER.info(message.format(
            counterparty_name=counterparty.Name()
        ))
        trigger_amendment_check(counterparty)


def get_active_advice_business_processes_in_error():
    asql_query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
    asql_query.AddAttrNode('StateChart.Name', 'EQUAL', get_advice_state_chart_name())
    asql_query.AddAttrNode('Subject_type', 'EQUAL', 'Party')
    event_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_event_add_info_name())
    event_attribute_name = 'AdditionalInfo.{event_method_name}'.format(
        event_method_name=event_method_name
    )
    asql_query.AddAttrNode(event_attribute_name, 'EQUAL', get_advice_event_name())
    instrument_type_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_instype_add_info_name())
    instrument_type_attribute_name = 'AdditionalInfo.{instrument_type_method_name}'.format(
        instrument_type_method_name=instrument_type_method_name
    )
    asql_query.AddAttrNode(instrument_type_attribute_name, 'EQUAL', 'Swap')
    asql_query.AddAttrNode('CurrentStateName', 'EQUAL', 'Error')
    to_date_method_name = DocumentGeneral.get_additional_info_method_name(
        DocumentBusinessProcessGeneral.get_business_process_to_date_add_info_name())
    to_date_attribute_name = 'AdditionalInfo.{to_date_method_name}'.format(
        to_date_method_name=to_date_method_name
    )
    asql_query.AddAttrNode(to_date_attribute_name, 'GREATER_EQUAL', acm.Time.DateToday())
    return asql_query.Select()


def revert_advice_business_process(business_process, incident_number):
    notes = acm.FArray()
    notes.Add("Reverting advice to previous state and triggering amendment check ({incident_number}).".format(
        incident_number=incident_number
    ))
    business_process.HandleEvent('Revert', None, notes)
    business_process.Commit()


def trigger_amendment_check(counterparty):
    counterparty.Touch()
    counterparty.Commit()
