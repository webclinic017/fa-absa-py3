
import acm
import FUxCore


def ael_custom_label(parameters, dictExtra):
    vs =  parameters.At('asqlQuery')
    if vs:
       return '(' + vs.StringKey() + ')'
    return None

def ael_custom_dialog_show(shell, params):
    selectedAsqlQuery = params.At('asqlQuery')
    
    asqlQuery =  acm.UX().Dialogs().SelectStoredASQLQuery(shell, acm.FInstrument, selectedAsqlQuery)
    parameters = acm.FDictionary()
    
    if asqlQuery: 
        parameters.AtPut('asqlQuery', asqlQuery)
        return parameters
    else :
        return None
    
def createInstruments(asqlQuery):
    return asqlQuery.Query().Select().SortByProperty('LastIRSensDay', True)
