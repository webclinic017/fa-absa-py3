#  Developer           : Heinrich Cronje
#  Purpose             : SND implementation
#  Department and Desk : Operations
#  Requester           : Miguel
#  CR Number           : 662927
import acm, clr
from SettlementCommitter import SettlementCommitter


def __setSettlementTrade(new_S, settlement):
    if settlement.Trade():
        new_S.Trade(settlement.Trade())
    else:
        new_S.Trade(None)
        
def create_Split(settlement, amount):
    new_S = acm.FSettlement()
    new_S.Status('New')
    new_S.RelationType('Split')
    new_S.Type('None')
    new_S.ToPortfolio(settlement.ToPortfolio())
    new_S.FromPortfolio(settlement.FromPortfolio())
    new_S.Currency(settlement.Currency())
    new_S.Acquirer(settlement.Acquirer())
    new_S.AcquirerName(settlement.AcquirerName())
    new_S.AcquirerAccountRef(settlement.AcquirerAccountRef())
    new_S.Counterparty(settlement.Counterparty())
    new_S.CounterpartyName(settlement.CounterpartyName())
    new_S.CounterpartyAccountRef(settlement.CounterpartyAccountRef())
    new_S.NettingRule(None)
    __setSettlementTrade(new_S, settlement)
    new_S.Protection(settlement.Protection())
    new_S.Owner(settlement.Owner())
    new_S.ValueDay(settlement.ValueDay())
    new_S.Amount(amount)
    return new_S

def IsSettlementSplit(settlement):
    potentialSplitParents = acm.FSettlement.Select('splitParent=%i' %settlement.Oid())
    if potentialSplitParents:
        return True
    elif settlement.Parent():
        parent = settlement.Parent()
        return IsSettlementSplit(parent)
    return False

def raiseErrorMessage(message):
    if message:
        func = acm.GetFunction('msgBox', 3)
        func("Error", message, 0)
    
def getLastErrorMessage(obj):
    error = str(obj.getLastErrorMessage())
    raiseErrorMessage(error)
        
def splitSettlement(settlement):
    
    #Check is Settlement is in status Authorised
    if settlement.Status() != 'Authorised':
        message = 'Settlement ' + str(settlement.Oid()) + ' is not Authorised.'
        raiseErrorMessage(message)
        return
        
    #Check is settlement that is selected is the highest netted settlement
    if (not settlement.RelationType().__contains__('Net')) or settlement.Parent():
        message = 'Settlement ' + str(settlement.Oid()) + ' is not the highest level netted settlement.'
        raiseErrorMessage(message)
        return
    
    #import FA_SM_SplitNettedAmount as FA_SM_SplitNettedAmount
    clr.AddReference("FA_SM_SplitNettedAmount")
    import FA_SM_SplitNettedAmount
    
    settlementToSplit = settlement
    if IsSettlementSplit(settlementToSplit):
        msg = 'Settlement ' + str(settlementToSplit.Oid()) + ' is already split.'
        raiseErrorMessage(msg)
        return
    
    obj = FA_SM_SplitNettedAmount.SplitNetWrapperMain()
    if obj.Initialize(settlementToSplit.Amount(), settlementToSplit.Currency().Name()) == 0:
        if obj.getResult() == 1:
            amountList = acm.FArray()
            nbrOfSplit = obj.getNumberOfLines()
            splitAmounts = obj.getSplitAmounts().split('|')
            i = 0
            while i < nbrOfSplit:
                amountList.Add(float(splitAmounts[i]))
                i = i + 1

            settlementCommitter = SettlementCommitter()
            settlementCommitter.SetSplitNetFlag('Split')
            settlementCommitter.SetAddInfoValue('SND_Split')
            for s in amountList:
                splitSettlement = create_Split(settlementToSplit, s)
                settlementCommitter.AddChild(splitSettlement)
            
            settlementToSplit.Status('Void')
            settlementCommitter.AddParent(settlementToSplit)
            
            settlementCommitter.Commit()
    else:
        getLastErrorMessage(obj)
    obj.Finalize()
    obj = None

def startDialog_cb(eii,*rest):
    shell = eii.Parameter('shell')
    if eii.ExtensionObject().IsKindOf(acm.FIndexedCollection):
        settlement = eii.ExtensionObject().At(0)
        if settlement:
            splitSettlement(settlement)
        
#splitSettlement(acm.FSettlement[])

