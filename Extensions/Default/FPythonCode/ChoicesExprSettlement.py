
import acm
import ael
from ChoicesExprCommon import listChoices, listChoicesWithEmpty


def strInVec(str, vec) :
    for v in vec :
        if v == str :
            return 1
    
    return 0
    
def getInstrumentSettleCategories(object):
    return listChoicesWithEmpty('Settle Category')

def getTradeSettleCategories(object):
    return listChoicesWithEmpty('TradeSettleCategory')
    
def GetSettleInstructionTypes(object):
    ssiTypes = ["Cash", "Security", "Delivery versus Payment"]
    return ssiTypes
    
def GetNettingRuleTypes(object):
    nettingRuleTypes = ["Net", "Close Trade Net", "Securities DvP Net"]
    return nettingRuleTypes


def getCPCodes(party, aliasType):
    if(party and aliasType) :
        aliases = party.Aliases()
        return [alias for alias in aliases if alias.Type() == aliasType]
    return []
    
def getDSSCodes(party):
    if(party) :
        aliases = party.Aliases()
        return [alias for alias in aliases if alias.Type().Name() == 'DataSourceScheme']
    return []

def getAccountSubNetworks(object): 
    choices = listChoices('Sub Network')
    list = acm.FArray()
    if (object.Currency() and object.Currency().Name() != 'EUR') or not object.Currency():
        for choice in choices:
            if choice.Name() != 'EBA' and choice.Name() != 'TARGET2':
                list.Add(choice)
    else:
        list.AddAll(choices)
    return list

def getNationalClearingSystem(object):
    return listChoices("National Clearing System")

