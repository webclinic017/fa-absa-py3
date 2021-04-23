""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FExpiration.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FExpiration.py - Script for maintenance when instruments expire.

DESCRIPTION
        This module performs instrument maintenance such as clearing the
        listleafs, orderbooks, price definitions and own orders.
        If wanted the expired instrument could also be deleted or archived.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)


import FExpirationAction


ScriptName = 'Expiration'


#==============================================================================
# Main
#==============================================================================

default_report_path = 'c:\\temp'


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FExpVariables')


ael_gui_parameters = {'InsertItemsShowExpired': True}

# ======== AEL variables setup - candidate values =============================

actions = FExpirationAction.ACTION_LIST_CURRENT

# ======== AEL variables setup - inserters ====================================

qIns = FBDPGui.insertInstruments(expiryEnd='0d', expiryStart='1900-01-01')
qPhysPort = FBDPGui.insertPhysicalPortfolio()

# ======== AEL variables setup - callback functions ===========================

        # The following helper functions are listed in alphabetical order.


def _expirationHandlingUpgrade(fieldValues):
    """
    Helper function to handle expiration action upgrade.  Transform old (V1)
    expiration action to new (V2) action and set/clear the appropriate fields
    """
    expActionIndex = ael_variables.expiration_handling.sequenceNumber
    expAction = fieldValues[expActionIndex]
    # Check if upgrade handling required.
    needUpgradeHandling = False
    if expAction == FExpirationAction.ARC_INS_AND_CASH_POST_POS:
        needUpgradeHandling = True
        expAction = FExpirationAction.ARC_AND_CASH_POST_POS
    elif expAction == FExpirationAction.DEL_INS_AND_CASH_POST_POS:
        needUpgradeHandling = True
        expAction = FExpirationAction.DEL_AND_CASH_POST_POS
    elif expAction == FExpirationAction.ARC_INS_AND_TRD_W_OUT_CASH_POST:
        needUpgradeHandling = True
        expAction = FExpirationAction.ARC_POS_W_OUT_CASH_POST
    elif expAction == FExpirationAction.DEL_INS_AND_TRD_W_OUT_CASH_POST:
        needUpgradeHandling = True
        expAction = FExpirationAction.DEL_POS_W_OUT_CASH_POST
    # Handle upgrade.
    if needUpgradeHandling:
        fieldValues[expActionIndex] = expAction
        alsoArcOrDelInsIndex = ael_variables.alsoArcOrDelIns.sequenceNumber
        fieldValues[alsoArcOrDelInsIndex] = 1
    return fieldValues


def _isCashPostingAction(expirationAction):
    """
    Predicate, return True if the expiration action is a cash posting action.
    """
    return (expirationAction in (
            FExpirationAction.ARC_AND_CASH_POST_POS,
            FExpirationAction.DEL_AND_CASH_POST_POS))


def _isPositionRelatedAction(expirationAction):
    """
    Predicate, return True if the expiration action is a position-related
    action.
    """
    return (expirationAction in (
            FExpirationAction.ARC_AND_CASH_POST_POS,
            FExpirationAction.DEL_AND_CASH_POST_POS,
            FExpirationAction.ARC_POS_W_OUT_CASH_POST,
            FExpirationAction.DEL_POS_W_OUT_CASH_POST))


        # Enabler functions ---------------------------------------------------
        # An enabler function do the followings:
        #     (1) Enable/Disable its designated field based on the given
        #         field values.
        #     (2) Call its designated field's callback function if there is
        #         one. Pass on the given field values along the way.
        #     (3) Return the field values returned from the callback function.
        #
        # The following enabler functions are listed in alphabetical order.

def enAllowGeneric(fieldValues):
    """
    Enabler for field allowGeneric.
    """
    # Field enabled if field allowLive value is set.
    allowLiveFieldIndex = ael_variables.allowLive.sequenceNumber
    allowLiveFieldValue = fieldValues[allowLiveFieldIndex]
    allowGenericFieldEnable = allowLiveFieldValue
    if allowGenericFieldEnable:
        tt = ttAllowGeneric
    else:
        tt = 'only valid when cash posting'
    ael_variables.allowGeneric.enable(int(allowGenericFieldEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.allowGeneric.callback(fieldValues)
    return fieldValues


def enAlsoArcOrDelIns(fieldValues):
    """
    Enabler for field alsoArcOrDelIns.
    """
    # Field enabled if field alsoArcOrDelIns value is enabled and cleared.
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]
    alsoArcOrDelInsEnable = _isPositionRelatedAction(expirtionActionValue)
    if alsoArcOrDelInsEnable:
        tt = ttAlsoArcOrDelIns
    else:
        tt = 'only valid when expiration action is position related'
    ael_variables.alsoArcOrDelIns.enable(int(alsoArcOrDelInsEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.alsoArcOrDelIns.callback(fieldValues)
    return fieldValues


def enCPInstrument(fieldValues):
    """
    Enabler for field cp_instrument.
    """
    # Field enabled if the expiration action is a cash posting action.
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirationHandlingValue = fieldValues[expirationHandlingIndex]
    cpInstrumentEnable = _isCashPostingAction(expirationHandlingValue)
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
    # Field enabled if the expiration action is a cash posting action.
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirationHandlingValue = fieldValues[expirationHandlingIndex]
    cpInUnderlyingEnable = _isCashPostingAction(expirationHandlingValue)
    if cpInUnderlyingEnable:
        tt = ttCPInUnderlying
    else:
        tt = 'only valid when cash posting'
    ael_variables.cp_in_underlying.enable(int(cpInUnderlyingEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.cp_in_underlying.callback(fieldValues)
    return fieldValues


def enPortfolios(fieldValues):
    """
    Enabler for field portfolios.
    """
    # Field enabled if field alsoArcOrDelIns value is enabled and cleared.
    alsoArcOrDelInsEnabled = ael_variables.alsoArcOrDelIns.isEnabled()
    alsoArcOrDelInsIndex = ael_variables.alsoArcOrDelIns.sequenceNumber
    alsoArcOrDelInsValue = int(fieldValues[alsoArcOrDelInsIndex])
    portfoliosEnable = alsoArcOrDelInsEnabled and not alsoArcOrDelInsValue
    if portfoliosEnable:
        tt = ttPortfolios
    else:
        tt = 'only valid when not archiving or deleting instrument.'
    ael_variables.portfolios.enable(int(portfoliosEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.portfolios.callback(fieldValues)
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

def cbAllowGeneric(index, fieldValues):
    """
    Callback for field allowGeneric.
    """
    # First modify value for this field -- set to 0 if disabled.
    allowGenericEnabled = ael_variables.allowGeneric.isEnabled()
    if not allowGenericEnabled:
        fieldValues[index] = 0
    # Then call enabler on dependent fields -- no dependent field.
    return fieldValues


def cbAllowLive(index, fieldValues):
    """
    Callback for field allowLive.
    """
    # First modify value for this field -- nothing to modify.
    # Then call enabler on dependent fields -- call enabler for allowGeneric.
    fieldValues = enAllowGeneric(fieldValues)
    return fieldValues


def cbAlsoArcOrDelIns(index, fieldValues):
    """
    Callback for field alsoArcOrDelIns.
    """
    # First modify value for this field -- set to 1 if disabled.
    alsoArcOrDelInsEnabled = ael_variables.alsoArcOrDelIns.isEnabled()
    if not alsoArcOrDelInsEnabled:
        fieldValues[index] = 1
    # Then call enabler on dependent fields -- call enabler on portfolios.
    fieldValues = enPortfolios(fieldValues)
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
    # EXTRA: invoke upgrade handling
    fieldValues = _expirationHandlingUpgrade(fieldValues)
    # First modify value for this field -- nothing to modify.
    # Then call enabler on dependent fields -- call enablers on fields
    #     alsoArcOrDelIns, cp_instrument, and cp_in_underlying.
    fieldValues = enAlsoArcOrDelIns(fieldValues)
    fieldValues = enCPInstrument(fieldValues)
    fieldValues = enCPInUnderlying(fieldValues)
    return fieldValues


def cbPortfolios(index, fieldValues):
    """
    Callback for field portfolios.
    """
    # First modify value for this field -- clear if disabled.
    portfoliosEnabled = ael_variables.portfolios.isEnabled()
    if not portfoliosEnabled:
        fieldValues[index] = None
    # Then call enabler on dependent fields -- no dependent field.
    return fieldValues


# ======== AEL variables setup - tool tips ====================================


ttExpAct = 'Expiration Handling alternatives.'
ttAlsoArcOrDelIns = 'Also archive or delete instrument.'
ttInstruments = 'The instruments to be handled.'
ttPortfolios = ('The portfolios to be handled. Leave it blank to select all '
        'portfolios.')
ttCPInUnderlying = 'Use the Underlying when cash posting derivatives.'
ttCPInstrument = 'Instrument used in cash posting trades.'
ttRenameWarrants = 'Expired warrants will be renamed to name_<exp_date>.'
ttRepPath = 'An execution report will be saved in this directory.'
ttLogReport = "Print an execution report in the AEL console."
ttAllowLive = 'Include live instruments in archivation and deletion.'
ttAllowGeneric = 'Include generic instruments in archivation and deletion.'
ttMaxRunTime = ('The execution will be terminated after this amount of time '
        'in seconds')

# ======= AEL variables ======================================================


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['expiration_handling',
                'Action',
                'string', actions, None,
                1, 0, ttExpAct, cbExpirationHandling, 1],
        ['alsoArcOrDelIns',
                 'Also archive or delete instrument(s)',
                 'int', [1, 0], 1,
                 0, 0, ttAlsoArcOrDelIns, cbAlsoArcOrDelIns, 1],
        ['instruments',
                 'Instrument(s)',
                 'FInstrument', None, qIns,
                 1, 1, ttInstruments, None, 1],
        ['portfolios',
                 'Portfolio(s)',
                 'FPhysicalPortfolio', None, qPhysPort,
                 0, 1, ttPortfolios, cbPortfolios, 0],
        ['cp_instrument',
                 'Cash posting instrument_Advanced',
                 'FInstrument', None, None,
                 0, 1, ttCPInstrument, cbCPInstrument, 0],
        ['cp_in_underlying',
                 'Cash post derivative in its underlying_Advanced',
                 'int', [1, 0], 0,
                 0, 0, ttCPInUnderlying, cbCPInUnderlying, 0],
        ['allowLive',
                 'Include live instruments_Advanced',
                 'int', [1, 0], 0,
                 0, 0, ttAllowLive, cbAllowLive, 1],
        ['allowGeneric',
                 'Include generic instruments_Advanced',
                 'int', [1, 0], 0,
                 0, 0, ttAllowGeneric, cbAllowGeneric, 1],
        ['report_path',
                 'Report Directory Path_Logging',
                 'string', [], default_report_path,
                 0, 0, ttRepPath, None, 1],
        ['log_report',
                 'Log Report In Console_Logging',
                 'int', [1, 0], None,
                 0, 0, ttLogReport, None, 1],
        ['MaxRunTime',
                'Max runtime_Advanced',
                'float', None, '3600',
                0, 0, ttMaxRunTime, None, 1])


def ael_main(dictionary):
    # Import Front modules.
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    import FBDPCalculatePosition
    importlib.reload(FBDPCalculatePosition)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPInstrument
    importlib.reload(FBDPInstrument)
    import FDMInstrumentExpiry
    importlib.reload(FDMInstrumentExpiry)
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    dictionary['instruments'] = FBDPCommon.convertEntityList(
            dictionary['instruments'], dictionary)
    FBDPCommon.execute_script(FDMInstrumentExpiry.perform_instrument_expiry,
            dictionary)
