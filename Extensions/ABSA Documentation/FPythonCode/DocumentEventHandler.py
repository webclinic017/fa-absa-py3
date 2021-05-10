"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentEventHandler

DESCRIPTION
    This module is used to define the API of an event-handler used for event-driven
    document processing.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
-----------------------------------------------------------------------------------------------------------------------------------------
"""


class DocumentEventHandler(object):
    """
    Definition of an event-handler for document processing.
    """

    def get_name(self):
        """
        Get the name of the Document Event Handler.
        """
        raise NotImplementedError()

    def handles(self, message, event_object):
        """
        Determine whether or not to trigger the event handler for an
        event on the specified object.
        """
        raise NotImplementedError()

    def handle_event(self, message, event_object):
        """
        Perform any event handling.
        """
        raise NotImplementedError()
