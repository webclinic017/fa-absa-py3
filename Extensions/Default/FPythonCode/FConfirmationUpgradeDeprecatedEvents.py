""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/upgrade/FConfirmationUpgradeDeprecatedEvents.py"
import acm
import FOperationsUtils as Utils

RESEND       = "Resend"
AMENDMENT    = "Amendment"
CANCELLATION = "Cancellation"
CHASER       = "Chaser"

def __GetChaserConfirmations(confirmation):
    return acm.FConfirmation.Select('chasingConfirmation = %d' % confirmation.Oid())

def __GetReferenceConfirmations(confirmation):
    return confirmation.Confirmations()

def __GetDeprecatedConfirmations(confirmation):
    deprecatedConfirmations = list()
    for chaserConfirmation in __GetChaserConfirmations(confirmation):
        deprecatedConfirmations.append(chaserConfirmation)
    for referenceConfirmation in __GetReferenceConfirmations(confirmation):
        deprecatedConfirmations.append(referenceConfirmation)
    return deprecatedConfirmations

def __IsDeprecatedConfirmation(confirmation):
    eventName = confirmation.EventChlItem().Name()
    return (eventName == RESEND or
            eventName == AMENDMENT or
            eventName == CANCELLATION or
            eventName == CHASER)


def __UpdateDeprecatedConfirmations(confirmation, confirmationInstruction, eventChlItem, confirmationSet):
    if __IsDeprecatedConfirmation(confirmation):
        confirmation.Type(confirmation.EventChlItem().Name())
        confirmation.ConfInstruction(confirmationInstruction)
        confirmation.EventChlItem(eventChlItem)
        confirmationSet.add(confirmation)
    
    for deprecatedConfirmation in __GetDeprecatedConfirmations(confirmation):
        __UpdateDeprecatedConfirmations(deprecatedConfirmation,
                                        confirmationInstruction,
                                        eventChlItem,
                                        confirmationSet)

def UpgradeDeprecatedConfirmations():
    query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    query.AddAttrNode('EventChlItem.Name', 'NOT_EQUAL', RESEND)
    query.AddAttrNode('EventChlItem.Name', 'NOT_EQUAL', AMENDMENT)
    query.AddAttrNode('EventChlItem.Name', 'NOT_EQUAL', CANCELLATION)
    query.AddAttrNode('EventChlItem.Name', 'NOT_EQUAL', CHASER)
    
    confirmations = query.Select()
    confirmationSet = set()
    Utils.Log(True, 'Updating deprecated confirmations ...')
    
    for confirmation in confirmations: 
        for deprecatedConfirmation in __GetDeprecatedConfirmations(confirmation):
            __UpdateDeprecatedConfirmations(deprecatedConfirmation,
                                            confirmation.ConfInstruction(),
                                            confirmation.EventChlItem(),
                                            confirmationSet)
        
    counter = 0
    for updatedConfirmation in confirmationSet:
        try:
            updatedConfirmation.Commit()
            counter += 1
            if (counter % 20 == 0):
                Utils.Log(True, '%d confirmations updated, please wait ...' % counter)
        except Exception as error:
            Utils.Log(True, 'Error while committing confirmation %d: %s' % (updatedConfirmation.Oid(), error))
    
    Utils.Log(True, 'Update of deprecated confirmations complete. %d confirmations updated' % counter)
