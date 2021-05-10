""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationHooksTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationHooksTemplate

DESCRIPTION
    Changes to any of these settings require a restart of the
    confirmation ATS for the changes to take affect
----------------------------------------------------------------------------"""

def GetExpiryDayCount(confirmation):
    """
    DESCRIPTION: This function return the number of days forward for
                 expiry day calculations.
    INPUT:       An FConfirmation. Treat input as read-only.
    OUTPUT:      An integer.
    """
    return 10


def GetMTMessage(confirmation, MTMessage):
    """
    DESCRIPTION: This function returns the number the SWIFT message that should
                 be created for a confirmation.
    INPUT:       A FConfirmation. Treat input as read-only.
                 The MT message (as string) that the core think should be created.
    OUTPUT:      A MT Message type represented as a string.
    """
    return MTMessage

def GetTradesToBeProcessed(fObject):
    """
    DESCRIPTION:    This function adds trades that should be processed that is not processed by default.
    INPUT:          An FObject. Most likey a FTrade or an FInstrument. Treat input as read-only.

    OUTPUT:         A list of FTrades.
    """
    return list()

def CancellationAndNewInsteadOfAmendment(oldConfirmation, newConfirmation, newXML):
    """
    DESCRIPTION:    This function determines if a cancellation and new should be send instead of an amendment. It will
                    be called for both freeform and SWIFT messages. If this hook is implemented the parameters
                    cancellationAndNewInsteadOfAmendmentSWIFT and cancellationAndNewInsteadOfAmendmentFreeForm
                    will be ignorded.

    INPUT:          A FConfirmation that is the old confirmation
                    A FConfirmation that is the new confirmation
                    The XML for the new confirmation
    OUTPUT:         A boolean.

    Tips:           To get the XML used by the old confirmation:
                    if confirmation and confirmation.Documents():
                        documents = confirmation.Documents()
                        if not documents.IsEmpty():
                            document = documents.First() #a confirmation can have many documents
                            if document.Data() !='':
                                oldDocument = document.Data().decode("hex").decode("zlib")
                    Please note that the parameter called xmlStoredInOperationsDocument in the FDocumentationParameters
                    needs to be set to True for this to work.

                    To determine if it is a SWIFT confirmation
                    confirmation.IsApplicableForSWIFT():

    """
    return False