"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentBusinessProcessEventHandler
    
DESCRIPTION
    This module contains an event-handler used for event-driven document
    business process processing.

    This event handler does not perform any actual processing itself but
    rather filters events and then delegates any actual processing to the
    processor for a particular document.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import DocumentBusinessProcessGeneral
from DocumentEventHandler import DocumentEventHandler


LOGGER = getLogger(__name__)


class DocumentBusinessProcessEventHandler(DocumentEventHandler):
    """
    Definition of an event-handler for document business processes.
    """

    def get_name(self):
        """
        Get the name of the document event handler.
        """
        return 'Document Business Process Event Handler'

    def handles(self, message, event_object):
        """
        Determine whether or not to trigger the event handler for an
        event on the specified object.
        """
        if self._is_document_business_process(event_object):
            return DocumentBusinessProcessGeneral.get_document_processor(event_object).is_processable(event_object)
        return False

    def handle_event(self, message, business_process):
        """
        Perform any event handling.
        """
        current_state_name = business_process.CurrentStateName()
        event = business_process.CurrentStep().Event()
        event_description = event.Name()
        if event.IsRetryEvent():
            event_description += ' (Retry)'
        if event.IsRevertEvent():
            event_description += ' (Revert)'
        message = "Event on '{state_chart_name}' business process, current state '{state_name}' ("
        message += "triggered by '{event_description}')."
        LOGGER.info(message.format(
            state_chart_name=business_process.StateChart().Name(),
            state_name=current_state_name,
            event_description=event_description
        ))
        DocumentBusinessProcessGeneral.get_document_processor(business_process).process(business_process)

    @staticmethod
    def _is_document_business_process(event_object):
        """
        Determine whether or not an event object is a document
        business process.
        """
        if not event_object.IsKindOf(acm.FBusinessProcess):
            return False
        return DocumentBusinessProcessGeneral.is_document_business_process(event_object)
