import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
#from DocumentGeneral import get_document_event
from FConfirmationCreator import FConfirmationCreator
from FConfirmationUnderlyingObject import UnderlyingTrade


LOGGER = getLogger(__name__)


ael_variables = AelVariableHandler()


ael_variables.add(
    'confirmations',
    label = 'Confirmations',
    cls = acm.FConfirmation,
    collection = None,
    default = None,
    mandatory = True,
    multiple = True,
    alt = 'The pre-release confirmations to regenerate.'
)

def get_document_event(document_event_name):
    """
    Get the event to associate with confirmations for a specified
    document event name.
    """
    # Importing inside function to avoid creating cyclic import
    # dependencies.
    from FConfirmationEventFactory import FConfirmationEventFactory
    for event in FConfirmationEventFactory.GetConfirmationEvents():
        if event.eventName == document_event_name:
            return event
    exception_message = "Unable to find a confirmation event with "
    exception_message += "the name '{name}'."
    raise ValueError(exception_message.format(
        name=document_event_name
    ))










def ael_main(ael_parameters):
    confirmations = ael_parameters['confirmations']
    for confirmation in confirmations:
        try:
            _regenerate(confirmation)
            LOGGER.info('Regenerated confirmation {oid}'.format(
                oid=confirmation.Oid()
            ))
        except Exception as exception:
            LOGGER.exception(exception)


def _regenerate(confirmation):
    if confirmation.IsPreRelease():
        trade = confirmation.Trade()
        event_name = confirmation.EventChlItem().Name()
        sub_type_object = confirmation.Subject()
        event = get_document_event(event_name)
        trade_receiver_method = acm.FMethodChain(acm.FSymbol(str(event.receiver)))
        receiver = trade_receiver_method.Call([trade])
        confirmation_receiver_method = "Trade." + event.receiver
        regenerated_confirmation = acm.Operations.CreateConfirmation(trade, event.eventName,
            sub_type_object, receiver, confirmation_receiver_method, None)
        FConfirmationCreator.AddConfirmationData(UnderlyingTrade(trade), regenerated_confirmation)
        _copy_additional_infos(confirmation, regenerated_confirmation)
        confirmation = confirmation.StorageImage()
        confirmation.Apply(regenerated_confirmation)
        confirmation.Commit()
    else:
        message = "Confirmation {oid} is not in a pre-release status. "
        message += "Please regenerate using Operations Manager."
        message = message.format(oid=confirmation.Oid())
        raise ValueError(message)


def _copy_additional_infos(from_confirmation, to_confirmation):
    for additional_info in from_confirmation.AddInfos():
        field_name = additional_info.AddInf().FieldName()
        value = additional_info.FieldValue()
        to_confirmation.AddInfoValue(field_name, value)
