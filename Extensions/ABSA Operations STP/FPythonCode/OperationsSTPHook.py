"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    OperationsSTPHook

DESCRIPTION
    This module is used to define the API of a hook used for event-driven
    Operations STP (straight-through-processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-05      FAOPS-448       Hugo Decloedt           Kgomotso Gumbo          Initial implementation.
                                Cuen Edwards
                                Stuart Wilson
-----------------------------------------------------------------------------------------------------------------------------------------
"""


class OperationsSTPHook(object):
    """
    Definition of a hook used to perform Operations STP.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        raise NotImplementedError()

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        raise NotImplementedError()

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        raise NotImplementedError()
