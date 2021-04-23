""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FArchiveInstruments.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FArchiveInstruments.py - Script for Archive position and its instrument

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

SCRIPT_NAME = 'Archive Instruments'


#==============================================================================
# Main
#==============================================================================


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FExpVariables')

# ======== AEL variables setup - tool tips ====================================

ttExpAct = 'Expiration Handling alternatives.'
ttAlsoArcIns = 'Also Archive instrument.'
ttPreservePL = 'Preserve P&L.'
ttInstruments = 'The instruments to be handled.'
ttInstrumentSelections = 'Queries to get the Instruments to be handled.'
ttCPInUnderlying = 'Use the Underlying when cash posting derivatives.'
ttCPInstrument = 'Instrument used in cash posting trades.'
ttRenameWarrants = 'Expired warrants will be renamed to name_<exp_date>.'
ttRepPath = 'An execution report will be saved in this directory.'
ttLogReport = "Print an execution report in the AEL console."
ttToXML = 'Write the deleted trades into the XML file'
ttFilePath = 'File will be created or appended'
ttInsertArchivedInstrument = ('Pop up the Select Archived Instruments '
        'diaglog when insert the items for instrument field.')
ttMaxRuntime = 'After this duration, the script will terminate'
ttInsSelectionDisable = 'Cear \'Instruments\' to enable'
ttInsDisable = 'Cear \'Instrument Selection\' to enable'

# ======== AEL variables setup - candidate values =============================

ACTION_NEW_EXPIRATION_ARCHIVE = 'Archive'
ACTION_NEW_EXPIRATION_DEARCHIVE = 'De-archive'


actions = [ACTION_NEW_EXPIRATION_ARCHIVE, ACTION_NEW_EXPIRATION_DEARCHIVE]
# ======== AEL variables setup - inserters ====================================

qIns = FBDPGui.insertInstruments(expiryEnd='0d', expiryStart='1900-01-01')

def instSelectionCb(index, fieldValues):
    tt = 'You can only select one type of object.'
    for field in [ael_variables.instrument_selection,
            ael_variables.instruments]:
        if ael_variables[index] != field:
            field.enable(not fieldValues[index], tt)
    return fieldValues

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

# ======== AEL variables setup - callback functions ===========================

# Enabler functions ---------------------------------------------------
# An enabler function do the followings:
#     (1) Enable/Disable its designated field based on the given
#         field values.
#     (2) Call its designated field's callback function if there is
#         one. Pass on the given field values along the way.
#     (3) Return the field values returned from the callback function.
#
# The following enabler functions are listed in alphabetical order.

def enAlsoArciveInstruments(fieldValues):
    """
    Enabler for field alsoArciveInstruments.
    """
    # Field enabled if field alsoArciveInstruments value is enabled and cleared
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]
    alsoArcInsEnable = expirtionActionValue in (
        ACTION_NEW_EXPIRATION_ARCHIVE, "")
    if alsoArcInsEnable:
        tt = ttAlsoArcIns
    else:
        tt = 'only valid when expiration action is archive.'
    ael_variables.alsoArchiveInstrument.enable(int(alsoArcInsEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.alsoArchiveInstrument.callback(fieldValues)
    return fieldValues


def enPreservePL(fieldValues):
    """
    Enabler for field PreservePL.
    """
    # Field enabled if field alsoArciveInstruments value is enabled and cleared
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]
    alsoPreservePLEnable = (
        expirtionActionValue in ACTION_NEW_EXPIRATION_ARCHIVE
    )
    if alsoPreservePLEnable:
        tt = ttPreservePL
    else:
        tt = 'only valid when expiration action is archive.'
    ael_variables.preservePL.enable(int(alsoPreservePLEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.preservePL.callback(fieldValues)
    return fieldValues

def enCPInstrument(fieldValues):
    """
    Enabler for field cp_instrument.
    """
    # Field enabled if the expiration action is a cash posting action.
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]

    cpInstrumentEnable = expirtionActionValue in ACTION_NEW_EXPIRATION_ARCHIVE

    if cpInstrumentEnable:
        tt = ttCPInstrument
    else:
        tt = 'only valid when cash posting'
    ael_variables.cp_instrument.enable(int(cpInstrumentEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.cp_instrument.callback(fieldValues)
    return fieldValues


def enCPInUnderlying(fieldValues):
    """
    Enabler for field cp_in_underlying.
    """
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]
    cpInUnderlyingEnable = (
        expirtionActionValue in ACTION_NEW_EXPIRATION_ARCHIVE
    )

    if cpInUnderlyingEnable:
        tt = ttCPInUnderlying
    else:
        tt = 'only valid when cash posting'
    ael_variables.cp_in_underlying.enable(int(cpInUnderlyingEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.cp_in_underlying.callback(fieldValues)
    return fieldValues

def enInstrument(fieldValues):

    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]

    if expirtionActionValue in ACTION_NEW_EXPIRATION_ARCHIVE:
        ael_variables.instruments[10] = qIns

    elif expirtionActionValue in ACTION_NEW_EXPIRATION_DEARCHIVE:
        ael_variables.instruments[10] = selInsCustomDlg
        """
        instIndex = ael_variables.instruments.sequenceNumber
        instValue = fieldValues[instIndex]
        if instValue and type(instValue) == type(''):
            instList = instValue.split(',')
            for inst in instList:
                aelInst = ael.Instrument[inst]
                if aelInst:
                    acmInst = FBDPCommon.ael_to_acm(aelInst)
        """
    return fieldValues

# Callback functions -------------------------------------------------
# A callback function do the followings:
#     (1) Modify its designated field in the given field values.
#     (2) One by one, call the dependent fields' enablers in turns.
#         Pass on the field values along the way.
#     (3) Return the field values that had been processed through
#         these enabler.
#
# The following callback functions are listed in alphabetical order.

def cbPreservePL(index, fieldValues):
    """
    Callback for field PreservePL.
    """
    # First modify value for this field -- set to 1 if disabled.
    alsoPreservePLEnabled = ael_variables.preservePL.isEnabled()
    if not alsoPreservePLEnabled:
        fieldValues[index] = 0

    return fieldValues


def cbAlsoArciveInstruments(index, fieldValues):
    """
    Callback for field alsoArciveInstruments.
    """
    # First modify value for this field -- set to 1 if disabled.
    alsoArcInsEnabled = ael_variables.alsoArchiveInstrument.isEnabled()
    if not alsoArcInsEnabled:
        fieldValues[index] = 0

    if int(fieldValues[index]):
        tt = 'Instrument operation, no need for trade selection.'
        ael_variables.TradeQuery.enable(0, tt)
        ael_variables.TradeFilter.enable(0, tt)
        ael_variables.TradingPortfolios.enable(0, tt)
    else:
        tt = 'Select on of the following object for trade selection.'
        #ael_variables.TradeQuery.enable(1, tt)
        ael_variables.TradeFilter.enable(1, tt)
        ael_variables.TradingPortfolios.enable(1, tt)

    return fieldValues


def cbCPInstrument(index, fieldValues):
    """
    Callback for field cp_instrument.
    """
    # First modify value for this field -- set to 0 if disabled.
    cpInstrumentEnabled = ael_variables.cp_instrument.isEnabled()
    if not cpInstrumentEnabled:
        fieldValues[index] = None
    # Then call enabler on dependent fields -- no dependent field.
    return fieldValues


def cbCPInUnderlying(index, fieldValues):
    """
    Callback for field cp_in_underlying.
    """
    # First modify value for this field -- set to 0 if disabled.
    cpInUnderlyingEnabled = ael_variables.cp_in_underlying.isEnabled()
    if not cpInUnderlyingEnabled:
        fieldValues[index] = 0
    # Then call enabler on dependent fields -- no dependent field.
    return fieldValues


def cbExpirationHandling(index, fieldValues):
    """
    Callback for field expiration_handling.
    """
    # Then call enabler on dependent fields -- call enablers on fields
    #     alsoArciveInstruments, cp_instrument, and cp_in_underlying.
    tt = 'Instrument operation, no need for trade selection.'
    ael_variables.TradeQuery.enable(0, tt)

    fieldValues = enAlsoArciveInstruments(fieldValues)
    fieldValues = enPreservePL(fieldValues)
    fieldValues = enCPInstrument(fieldValues)
    fieldValues = enCPInUnderlying(fieldValues)
    fieldValues = enInstrument(fieldValues)

    return fieldValues


def cbOnArchivedInst(index, fieldValues):
    fieldValues = enInstrument(fieldValues)
    return fieldValues


# ======= AEL variables ======================================================

global ael_variables
ael_variables = FBDPGui.FxPositionVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['expiration_handling',
                'Action',
                'string', actions, ACTION_NEW_EXPIRATION_ARCHIVE,
                1, 0, ttExpAct, cbExpirationHandling, 1, None],
        ['instrument_selection',
                 'Instrument Selection_Positions',
                 'string', getInstSelectors(), None,
                 0, 0, ttInstrumentSelections, instSelectionCb, 1, None],
        ['instruments',
                 'Instrument(s)_Positions',
                 'FInstrument', [], None,
                 0, 1, ttInstruments, instSelectionCb, 1, None],
        ['alsoArchiveInstrument',
                 'Also archive instrument(s)_Positions',
                 'int', [1, 0], 0,
                 0, 0, ttAlsoArcIns, cbAlsoArciveInstruments, 1, None],
        ['preservePL',
                 'Preserve P&L',
                 'int', [1, 0], 1,
                 0, 0, ttPreservePL, cbPreservePL, 1, None],
        ['cp_instrument',
                 'Cash posting instrument_Advanced',
                 'FInstrument', None, None,
                 0, 1, ttCPInstrument, cbCPInstrument, 0, None],
        ['cp_in_underlying',
                 'Cash post derivative in its underlying_Advanced',
                 'int', [1, 0], 0,
                 0, 0, ttCPInUnderlying, cbCPInUnderlying, 0, None],
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
    execParam['ScriptName'] = SCRIPT_NAME
    execParam['TradingPortfolios'] = FBDPCommon.convertEntityList(
        execParam['TradingPortfolios'], execParam)

    insSelector = execParam['instrument_selection']
    insSelList = FBDPInstSelection.GetInstSelections()
    instrumentsList = []
    for insSel in insSelList:
        if insSel.Name() == insSelector:
            instrumentsList = insSel.Run()
            break

    instUserSelectedList = []
    for i in execParam['instruments']:
        if FBDPCommon.is_acm_object(i):
            instUserSelectedList.append(i.Name())
        else:
            instUserSelectedList.append(i)

    execParam['instruments'] = instUserSelectedList + instrumentsList

    FBDPGui.setPortfolioGrouper(execParam)

    # Execute script
    FBDPPerform.execute_perform(FNewExpirationPerform.perform, execParam)
