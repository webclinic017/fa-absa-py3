""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/blacklistedInstrumentQuery.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    blacklistedInstrumentQuery

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

def ael_custom_dialog_show(shell, params):

    selectedAsqlQuery = None
    if params:
        selectedAsqlQuery = params.At('initialData').At('columnParameterNamesAndInitialValues')
    asqlQuery =  acm.UX().Dialogs().SelectStoredASQLQuery(shell, acm.FInstrument, selectedAsqlQuery)
    parameters = acm.FDictionary()
    
    if asqlQuery: 
        parameters.AtPut(acm.FSymbol('ExclusionListInstrumentQuery'), asqlQuery)
        return parameters
    else:
        return None
    
def ael_custom_dialog_main(parameters, dictExtra):
    config = acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues( parameters )
    columnLabel = parameters.At('ExclusionListInstrumentQuery').Name()
    config = acm.Sheet().Column().CreatorConfigurationFromInitialCustomLabel( acm.FSymbol(columnLabel), config )
    return_value = {acm.FSymbol("columnCreatorConfiguration") : config}
    return return_value

