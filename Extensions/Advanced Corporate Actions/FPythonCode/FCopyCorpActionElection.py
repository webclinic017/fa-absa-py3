""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCopyCorpActionElection.py"
"""----------------------------------------------------------------------------
MODULE
    FCopyCorpActionElection - GUI Module to copy to a new corporate action 
    Election definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActionElection
import FBDPCommon
import FCorpActionElectionGuiCommon

ADDITIONALINFO_RECORDTYPE = "CorpActionElection"
addInfoNames = FBDPCommon.getAdditionalInfoNames(ADDITIONALINFO_RECORDTYPE)

def populateGuiFromElection(election, fieldValues):
    for var in ael_variables:
        if var.varName == 'CaChoice':
            fieldValues[var.sequenceNumber] = election.CaChoice().Oid()
        elif var.varName == 'Name':
            fieldValues[var.sequenceNumber] = 'Copy of ' + election.GetProperty(var.varName)
        elif var.varName in addInfoNames:
            addinfo = election.AddInfos()
            for i in addinfo:
                spec = i.AddInf()
                name = spec.FieldName()
                if name == var[0]:
                    fieldValues[var.sequenceNumber] = i.FieldValue()    
        else:
            fieldValues[var.sequenceNumber] = election.GetProperty(var.varName)
    return fieldValues

def oid_cb(index, fieldValues):
    if isinstance(fieldValues[index], (int, long)):
        election = acm.FCorporateActionElection[fieldValues[index]]
        if election:
            fieldValues = populateGuiFromElection(election, fieldValues)
    return fieldValues

ael_variables = FCorpActionElectionGuiCommon.ael_variables

FBDPGui.createAdditionalInfoVariables(ael_variables, FCorpActionElectionGuiCommon.ADDITIONALINFO_RECORDTYPE)

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Copy Corporate Action Election')

def ael_main(d):
    caElection = acm.FCorporateActionElection[int(d['Oid'])].Clone()
    FOpenCorpActionElection.run_main(d, caElection, 1)
