""" Compiled: NONE NONE """

import acm

def RemoveFirstLine(text):
    newText = ''
    lineNumber = 0
    for i in text.split('\n'):
        lineNumber = lineNumber + 1
        if lineNumber != 2 and lineNumber != len(text.split('\n')):
            newText = newText + i + '\n'

    return newText


def AddStatusExplanation(document, text):
    statusExplanation = document.StatusExplanation() + text + "\n"
    while len(statusExplanation) > 254:
        statusExplanation = RemoveFirstLine(statusExplanation)
    document.StatusExplanation(statusExplanation)


def ChangeStatusAndTextOfDocument(document, oldStatusesNeeded, newStatus, text, operationsCommitter):
    if document == None:
        return
    statusExplanationUpdated = False
    for i in oldStatusesNeeded:
        if i == document.Status():
            if newStatus:
                document.Status(newStatus)
            statusExplanationUpdated = True
            if not document.StatusExplanation().endswith(text + "\n"):
                AddStatusExplanation(document, text)
            operationsCommitter.AddObject(document)
            break
    if not statusExplanationUpdated:
        textStatus = 'Unsuspected Trident status update:' + text
        if not document.StatusExplanation().endswith(text + "\n"):
            AddStatusExplanation(document, textStatus)
            operationsCommitter.AddObject(document)
    return statusExplanationUpdated

def DocumentNotRequired(confirmation, document, operationsCommitter):
    ChangeStatusAndTextOfDocument(document, ['Pending generation', 'Generated'], 'Exception', "Document not required", operationsCommitter)



def GetBottommostConfirmation(confirmation):
    referencedConfirmation = confirmation.ConfirmationReference()
    if referencedConfirmation:
        return GetBottommostConfirmation(referencedConfirmation)
    else:
        return confirmation

def SetConfirmationStatus(confirmation, status, operationsCommitter):
    if confirmation.Status() != 'Matched':
        confirmation.Status(status)
        operationsCommitter.AddObject(confirmation)


def Matched(confirmation, document, operationsCommitter, tridentID):
    status = confirmation.Status()
    ChangeStatusAndTextOfDocument(document, ['Sent successfully'], None, "Matched", operationsCommitter)

    if status == "Matching Failed" or status == "Pending Matching" or status == "Partial Match":
        SetConfirmationStatus(confirmation, 'Matched', operationsCommitter)
        if confirmation.IsNewestInConfirmationChain():
            if GetBottommostConfirmation(confirmation).EventChlItem().Name() == 'New Trade' and confirmation.EventChlItem().Name() != "Cancellation":
                trade = confirmation.Trade()
                if trade.Status() == 'BO Confirmed':
                    trade.Status('BO-BO Confirmed')
                trade.YourRef(tridentID)
                operationsCommitter.AddObject(trade)


def MatchFailed(confirmation, document, operationsCommitter):
    status = confirmation.Status()
    if status == "Matching Failed" or status == "Pending Matching" or status == "Partial Match":
        SetConfirmationStatus(confirmation, 'Matching Failed', operationsCommitter)
    ChangeStatusAndTextOfDocument(document, ['Sent successfully'], None, "Match Failed", operationsCommitter)

def DocumentNotRequiredPostRelease(confirmation, document, operationsCommitter):
    status = confirmation.Status()
    ChangeStatusAndTextOfDocument(document, ['Sent successfully'], None, "Document not required", operationsCommitter)

    if status == "Pending Matching" or confirmation.Status() == "Matching Failed":
        SetConfirmationStatus(confirmation, 'Partial Match', operationsCommitter)

def CounterpartyToProduce(confirmation, document, operationsCommitter):
    if confirmation.Status() == 'Pending Document Generation':
        if confirmation.Documents():
            if document.Status() == 'Pending Generation':
                document.Status('Generated')
                document.Commit()
        confirmation.Status('Pending Approval')
        confirmation.Commit()
        confirmation.Status('Authorised')
        confirmation.Commit()
        
    if confirmation.Status()== 'Authorised':
        SetConfirmationStatus(confirmation, 'Released', operationsCommitter)
    ChangeStatusAndTextOfDocument(document, ['Generated'], 'Sending', "Counterparty To Produce", operationsCommitter)

def Sending(confirmation, document, operationsCommitter):
    if document and not document.StatusExplanation().endswith("Counterparty To Produce" + "\n"):
        if document.Status() =='Generated':
            ChangeStatusAndTextOfDocument(document, ['Generated'], 'Sending', "Dispatched", operationsCommitter)
        else:
            ChangeStatusAndTextOfDocument(document, ['Sent successfully'], None, "Dispatched", operationsCommitter)
    if confirmation.Status() == 'Pending Document Generation':
        confirmation.Status('Pending Approval')
        confirmation.Commit()
        confirmation.Status('Authorised')
        confirmation.Commit()
    if confirmation.Status()== 'Authorised':
         SetConfirmationStatus(confirmation, 'Released', operationsCommitter)



def Generated(confirmation, document, operationsCommitter):
        if document.Status() =='Sent successfully':
            ChangeStatusAndTextOfDocument(document, ['Sent successfully'], None, "Awaiting Dispatch", operationsCommitter)
        ChangeStatusAndTextOfDocument(document, ['Exception', "Pending generation"], 'Generated', "Awaiting Dispatch", operationsCommitter)


def CreateAddInfo(record, addInfoName, value):
    if value:
        addInfo = acm.FAdditionalInfo()
        addInfo.Recaddr(record.Oid())
        addInfo.AddInf(acm.FAdditionalInfoSpec[addInfoName])
        addInfo.Value(value)
        addInfo.Commit()

def UpdateAddInfo(record, addInfoName, value):
        addInfos = acm.FAdditionalInfo.Select('recaddr = %i' %record.Oid())
        for addInfo in addInfos:
            if addInfo.AddInf().Name() == addInfoName:
                addInfo.Value(value)
                addInfo.Commit()
    
def SetAffirmationChoiceList(trade, choiceList):
    affirmationChoiceList = acm.FChoiceList.Select("list = 'Affirmation'")
    for i in affirmationChoiceList:
        if i.Name() == choiceList:
            if trade.AdditionalInfo().Affirmation() == None:
                CreateAddInfo(trade, 'Affirmation', i)
            else:
                trade.AdditionalInfo().Affirmation(i)

def SetAffirmationCpRef(trade, tridentID):      
    if trade.AdditionalInfo().Affirmation_CP_Ref() == None:
        CreateAddInfo(trade, 'Affirmation_CP_Ref', tridentID)
    else:
        UpdateAddInfo(trade, 'Affirmation_CP_Ref', tridentID)

def AffirmationAcknowledged(confirmation, document, operationsCommitter, tridentID):
    trade = confirmation.Trade()
    SetAffirmationChoiceList(trade, 'Affirmed')
    operationsCommitter.AddObject(trade)

def AffirmationFinancialsAgreed(confirmation, document, operationsCommitter, tridentID):
    trade = confirmation.Trade()
    SetAffirmationChoiceList(trade, 'Affirmed')
    operationsCommitter.AddObject(trade)

def AffirmationCounterpartyDoesNotRecogniseDeal(confirmation, document, operationsCommitter, tridentID):
    trade = confirmation.Trade()
    SetAffirmationChoiceList(trade, 'Disputed')
    operationsCommitter.AddObject(trade)

def AffirmationTermsDisputed(confirmation, document, operationsCommitter, tridentID):
    trade = confirmation.Trade()
    SetAffirmationChoiceList(trade, 'Disputed')
    operationsCommitter.AddObject(trade)

def UpdateCPRefAddInfo(confirmation, document, operationsCommitter, tridentID):
    trade = confirmation.Trade()
    trade.YourRef(tridentID)
    operationsCommitter.AddObject(trade)

