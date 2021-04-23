"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FConfirmationCancellationXMLHook

DESCRIPTION
    This module is used to define a ConfirmationCancellationXMLHook that can be used to
    customise Front Arena's confirmation cancellation XML behaviour.

NOTES
    Please note that although the name of this module starts with an F, it is not a core
    module.  The module has been named this way as it is analogous to the core
    FConfirmationEventHook module and due to this customisation being modelled as 'how might
    this be implemented if it was provided by core Front Arena'.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-25      FAOPS-226       Cuen Edwards            Letitia Carboni         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from FOperationsHook import DefaultHook
import types
from FOperationsTypeComparators import PrimitiveTypeComparator


class ConfirmationCancellationXMLHook(DefaultHook):

    def __init__(self, moduleName, hookName):
        DefaultHook.__init__(self, moduleName, hookName, PrimitiveTypeComparator(bytes))

    def GenerateCancellationXML(self, cancellationTemplate, cancellationConfirmation, overrideXML):
        return self.CallHook(cancellationTemplate, cancellationConfirmation, overrideXML)
