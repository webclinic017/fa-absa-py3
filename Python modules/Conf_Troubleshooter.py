import acm
import logging
import os


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _test():
    """FIXME."""
    trade = acm.FTrade[122174150]
    _test_trade(trade)


def _test_trade(trade):
    """FIXME."""
    _trade_matches_confirmation_trade_query_folders(trade)
    _trade_matches_confirmation_events(trade)
    _trade_confirmation_creation_is_prevented(trade)


def _trade_matches_confirmation_trade_query_folders(trade):
    """FIXME."""
    import FConfirmationParameters
    logger.info("Testing if trade {trade_oid} satisfies all FConfirmationParameters.tradeFilterQueries:".format(
        trade_oid=trade.Oid()
    ))
    for query_folder_name in FConfirmationParameters.tradeFilterQueries:
        query_folder = acm.FStoredASQLQuery[query_folder_name]
        if query_folder is None:
            logger.warning("A query folder with the name '{query_folder_name}' does not exist.".format(
                query_folder_name=query_folder_name
            ))
            continue
        logger.info(' - {query_folder_name}: {satisfies}'.format(
        query_folder_name=query_folder_name,
        satisfies=query_folder.Query().IsSatisfiedBy(trade)
        ))


def _trade_matches_confirmation_events(trade):
    from FConfirmationEventFactory import FConfirmationEventFactory
    logger.info("Testing if trade {trade_oid} satisfies any FConfirmationParameters.confirmationEvents:".format(
        trade_oid=trade.Oid()
    ))
    confirmation_events = FConfirmationEventFactory.GetConfirmationEvents()
    for confirmation_event in confirmation_events:
        logger.info(" - {event_name}: {satisfies}".format(
            event_name=confirmation_event.eventName,
            satisfies=confirmation_event.baseRule.IsSatisfiedBy(trade)
        ))


def _trade_confirmation_creation_is_prevented(trade):
    """FIXME."""
    import FConfirmationParameters
    from FConfirmationUnderlyingObject import UnderlyingTrade
    logger.info(
        "Testing if confirmations created for trade {trade_oid} satisfy any FConfirmationParameters.preventConfirmationCreationQueries:".format(
            trade_oid=trade.Oid()
        ))
    underlying_object = UnderlyingTrade(trade)
    satisfied_confirmation_events = _get_satisfied_confirmation_events(trade)
    confirmations = create_confirmations(underlying_object, satisfied_confirmation_events)
    if len(confirmations) == 0:
        logger.info(" - No confirmations to prevent creation of.")
    else:
        for confirmation in confirmations:
            _confirmation_matches_query_folders(confirmation,
                FConfirmationParameters.preventConfirmationCreationQueries)


def _confirmation_matches_query_folders(confirmation, query_folder_names):
    """FIXME."""
    logger.info(" - Testing '{event_name}' confirmation:".format(
        event_name=confirmation.EventChlItem().Name()
    ))
    for query_folder_name in query_folder_names:
        query_folder = acm.FStoredASQLQuery[query_folder_name]
        if query_folder is None:
            logger.warning("A query folder with the name '{query_folder_name}' does not exist.".format(
                query_folder_name=query_folder_name
            ))
            continue
        logger.info('  - {query_folder_name}: {satisfies}'.format(
            query_folder_name=query_folder_name,
            satisfies=query_folder.Query().IsSatisfiedBy(confirmation)
        ))


def _get_satisfied_confirmation_events(trade):
    from FConfirmationEventFactory import FConfirmationEventFactory
    satisfied_confirmation_events = list()
    confirmation_events = FConfirmationEventFactory.GetConfirmationEvents()
    for confirmation_event in confirmation_events:
        if confirmation_event.baseRule.IsSatisfiedBy(trade):
            satisfied_confirmation_events.append(confirmation_event)
    return satisfied_confirmation_events


def create_confirmations(underlyingObject, events):
    """FIXME."""
    from FConfirmationCreator import FConfirmationCreator
    confirmations = list()
    for event in events:
        method = acm.FMethodChain(acm.FSymbol(str(event.receiver)))
        receiver = method.Call([underlyingObject.GetTrade()])
        if receiver != None:
            if receiver.IsKindOf(acm.FParty):
                method = "Trade." + event.receiver
                if event.subType == 'Default':
                    newConfirmation = acm.Operations.CreateConfirmation(underlyingObject.GetTrade(), event.eventName,
                        None, receiver, method, None)
                    FConfirmationCreator.AddConfirmationData(underlyingObject, newConfirmation)
                    confirmations.append(newConfirmation)
                else:
                    for subTypeObject in FConfirmationCreator.SubjectList(event, underlyingObject):
                        if FConfirmationCreator.IsSubTypeSatisfied(event, subTypeObject, underlyingObject.GetTrade()):
                            newConfirmation = acm.Operations.CreateConfirmation(underlyingObject.GetTrade(),
                                event.eventName, subTypeObject, receiver, method, None)
                            FConfirmationCreator.AddConfirmationData(underlyingObject, newConfirmation)
                            confirmations.append(newConfirmation)
            else:
                message = "Method chain '{receiver}' returned '{receiver_class_name}', expected 'FParty'. No confirmation will be created for this receiver."
                logger.warning(message.format(
                    receiver=event.receiver,
                    receiver_class_name=receiver.Class().Name()
                ))
        else:
            message = "Method chain '{receiver}' did not return a value. No confirmation will be created for this receiver."
            logger.warning(message.format(
                receiver=event.receiver
            ))
    return confirmations


_test()
