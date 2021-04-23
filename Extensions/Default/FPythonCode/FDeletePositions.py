""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FDeletePositions.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FDeletePositions.py - Script for delete positions

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)

import FBDPCommon
importlib.reload(FBDPCommon)

import FBDPInstSelectionDialog
importlib.reload(FBDPInstSelectionDialog)


SCRIPT_NAME = 'Delete Positions'


#==============================================================================
# Main
#==============================================================================


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FExpVariables')


ael_gui_parameters = {'InsertItemsShowExpired': True}
# ======== AEL variables setup - inserters ====================================
qIns = FBDPGui.insertInstruments(expiryEnd='0d', expiryStart='1900-01-01')

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

def enCPInstrument(fieldValues):
    """
    Enabler for field cp_instrument.
    """
    # Field enabled if the expiration action is a cash posting action.

    preservePL = int(fieldValues[ael_variables.preservePL.sequenceNumber])
    cpInstrumentEnable = preservePL == 1

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
    preservePL = int(fieldValues[ael_variables.preservePL.sequenceNumber])
    cpInUnderlyingEnable = preservePL == 1

    if cpInUnderlyingEnable:
        tt = ttCPInUnderlying
    else:
        tt = 'only valid when cash posting'
    ael_variables.cp_in_underlying.enable(int(cpInUnderlyingEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.cp_in_underlying.callback(fieldValues)
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

    enCPInstrument(fieldValues)
    enCPInUnderlying(fieldValues)

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


# ======== AEL variables setup - tool tips ====================================


ttPreservePL = 'Preserve P&L.'
ttInstruments = 'The instruments to be handled.'
ttCPInUnderlying = 'Use the Underlying when cash posting derivatives.'
ttCPInstrument = 'Instrument used in cash posting trades.'
ttRepPath = 'An execution report will be saved in this directory.'
ttLogReport = "Print an execution report in the AEL console."
ttFilePath = 'File will be created or appended'
ttMaxRuntime = 'After this duration, the script will terminate'

# ======= AEL variables ======================================================


ael_variables = FBDPGui.FxPositionVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['instruments',
                 'Instrument(s)_Positions',
                 'FInstrument', [], qIns,
                 1, 1, ttInstruments, None, 1, None],
        ['preservePL',
                 'Preserve P&L_Positions',
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
    execParam['expiration_handling'] = 'Delete Positions'

    # Execute script
    FBDPPerform.execute_perform(FNewExpirationPerform.perform, execParam)
