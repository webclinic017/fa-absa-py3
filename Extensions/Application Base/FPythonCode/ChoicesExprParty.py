
import acm
from ChoicesExprCommon import allEnumValuesExcludeNone, listChoices, listChoicesWithEmpty


def getBusinessStatuses():
    return listChoices('Business Status')

def getConsolidates():
    return listChoices('Consolidate')
    
def getLegalForms():
    return listChoices('Legal Form')
    
def getRatingAgencies():
    return listChoicesWithEmpty('Rating Agency')
        
def getRatings():
    return listChoices('Rating')
    
def getRelations():
    return listChoices('Relation') 
            
def getRating1Choices():
    list = acm.ChoiceList.Rating1ChoiceList()
    return list.ChoicesSorted() if list else []

def getRating2Choices():
    list = acm.ChoiceList.Rating2ChoiceList()
    return list.ChoicesSorted() if list else []

def getRating3Choices():
    list = acm.ChoiceList.Rating3ChoiceList()
    return list.ChoicesSorted() if list else []

def getContryOfRisks():
    return listChoices('Country of Risk')
    
def getUserRatings():
    return listChoices('User Rating')

