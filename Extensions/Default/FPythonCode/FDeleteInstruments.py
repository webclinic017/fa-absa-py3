""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FDeleteInstruments.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FDeleteInstruments.py - Script for Delete position and its instrument

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)

import FBDPCommon
importlib.reload(FBDPCommon)

import FBDPInstSelection
importlib.reload(FBDPInstSelection)

import FBDPInstSelectionDialog
importlib.reload(FBDPInstSelectionDialog)

import acm

SCRIPT_NAME = 'Delete Instruments'


#==============================================================================
# Main
#==============================================================================


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FExpVariables')

# ======== AEL variables setup - tool tips ====================================
ttInstruments = 'The instruments to be handled.'
ttRepPath = 'An execution report will be saved in this directory.'
ttLogReport = "Print an execution report in the AEL console."
ttFilePath = 'File will be created or appended'
ttMaxRuntime = 'After this duration, the script will terminate'
ttInsSelectionDisable = 'Cear \'Instruments\' to enable'
ttInsDisable = 'Cear \'Instrument Selection\' to enable'

# ======== AEL variables setup - inserters ====================================
qIns = FBDPGui.insertInstruments(expiryEnd='0d', expiryStart='1900-01-01')

def getInstSelectors():
    instSelectorNames = []
    instSelectors = FBDPInstSelection.GetInstSelections()
    for instSelector in instSelectors:
        instSelectorNames.append(instSelector.Name())
    return instSelectorNames


def selInsCustomDlg(shell, params):
    params['Script Name'] = SCRIPT_NAME
    customDlg = FBDPInstSelectionDialog.FBDPInstSelectionDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def instSelectionCb(index, fieldValues):
    tt = 'You can only select one type of object.'
    for field in [ael_variables.instrument_selection,
            ael_variables.instruments]:
        if ael_variables[index] != field:
            field.enable(not fieldValues[index], tt)
    return fieldValues

# ======= AEL variables ======================================================

global ael_variables
ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['instrument_selection',
                 'Instrument Selection',
                 'string', getInstSelectors(), None,
                 0, 0, ttInstruments, instSelectionCb, 1, None],
        ['instruments',
                 'Instruments',
                 'string', [], None,
                 0, 1, ttInstruments, instSelectionCb, 1, selInsCustomDlg],
        ['max_runtime',
                 'Maximum Runtime (s)_Advanced',
                 'int', None, 3600,
                 0, 0, ttMaxRuntime, None, 1, None],)


def ael_main(execParam):

    # Import Front modules.
    import FBDPCalculatePosition
    importlib.reload(FBDPCalculatePosition)
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPPerform
    importlib.reload(FBDPPerform)
    import FNewExpirationPerform
    importlib.reload(FNewExpirationPerform)
    # Parameter
    execParam['expiration_handling'] = 'Delete'
    execParam['ScriptName'] = SCRIPT_NAME

    insSelector = execParam['instrument_selection']
    insSelList = FBDPInstSelection.GetInstSelections()
    instrumentsList = []
    for insSel in insSelList:
        if insSel.Name() == insSelector:
            instrumentsList = insSel.Run()
            break

    instUserSelectedList = []
    for i in execParam['instruments']:
        instUserSelectedList.append(i)

    execParam['instruments'] = instUserSelectedList + instrumentsList

    #Execute script
    FBDPPerform.execute_perform(FNewExpirationPerform.perform, execParam)
