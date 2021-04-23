# ----------------------------------------------------------------------------
#    (c) Copyright 2021 SunGard Front Arena. All rights reserved.
# ----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FArchiveInstruments_ABSA.py - Script for Archive position and its instrument based on date and INSTYPE

DESCRIPTION

Script is used to filter untraded instruments based on date filter and archive them
Script fetch details and pass to default FInstrumentArchive scripts with instrument selection list

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import FArchiveInstruments
from FBDPCurrentContext import Logme
import FBDPGui
import acm
import ael

reload(FBDPGui)

# ==============================================================================
# Main
# ==============================================================================

SCRIPT_NAME = 'Archive Instruments'

INSTRUMENT_QUERY = """
SELECT instrument.insid, instrument.instype , instrument.exp_day, instrument.archive_status 
FROM instrument 
WHERE NOT EXISTS(SELECT 1 FROM trade where trade.insaddr=instrument.insaddr)
AND (exp_day {}) 
AND instype= {} 
AND generic = 0 
AND archive_status = {}
"""

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
                                                       'LogVariables')

TOOLTIP_EXP_ACT = 'Expiration Handling alternatives.'
TOOLTIP_MAX_RUNTIME = 'After this duration, the script will terminate'
TOOLTIP_CPINSTRUMENT = 'Instrument used in cash posting trades.'
TOOLTIP_LOG_REPORT = "Print an execution report in the AEL console."
TOOLTIP_INSTYPE = "Select instrument type from list"
TOOLTIP_Date_Period="Select date period (e.g. -1Y, -3W, -10D)"

# ======== AEL variables setup - candidate values =============================

ACTION_NEW_EXPIRATION_ARCHIVE = 'Archive'
ACTION_NEW_EXPIRATION_DEARCHIVE = 'De-archive'


actions = [ACTION_NEW_EXPIRATION_ARCHIVE, ACTION_NEW_EXPIRATION_DEARCHIVE]
# ======== AEL variables setup - inserters ====================================
def _get_instype_from_enum(insType):
    enumeration = acm.FEnumeration["enum(InsType)"]
    return enumeration.Enumeration(insType)

def _get_date_from_period(date_period): 
    today = ael.date_today()
    try:
        return today.add_period(date_period)
    except Exception as e:
        Logme()('Invalid date: %s' % str(e), 'ERROR' )
        raise Exception('Invalid date: %s' % str(e))

def _get_untraded_instruments(instype, archive_status, end_date, start_date=None):
    untraded_instruments = []
    today = ael.date_today().to_string(ael.DATE_ISO)
    if end_date > today:
        Logme()('Invalid date: %s period can not be future date' % end_date, 'ERROR' )
        raise Exception('Invalid date: %s period can not be future date' % end_date, 'ERROR' )
    
    if start_date:
        Logme()('Selection Range: Start date: %s and End Date: %s' 
                            % (start_date, end_date), 'NOTIME_INFO')
        query_date_range = 'BETWEEN ' + "\'" + start_date + "\'" +  ' and ' + "\'" + end_date + "\'"
    else:
        Logme()('Selection Range: End Date: %s' % end_date, 'NOTIME_INFO')
        query_date_range = '<= ' + "\'" + end_date + "\'"
    query = INSTRUMENT_QUERY.format(query_date_range, _get_instype_from_enum(instype), archive_status )
    Logme()('Running query:\n  %s' % '  '.join(query.splitlines()), 'INFO')
    untraded_instruments = ael.dbsql(query)
    return untraded_instruments

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
    expirationHandlingIndex = ael_variables.expiration_handling.sequenceNumber
    expirtionActionValue = fieldValues[expirationHandlingIndex]

    cpInstrumentEnable = expirtionActionValue in ACTION_NEW_EXPIRATION_ARCHIVE

    if cpInstrumentEnable:
        tt = TOOLTIP_CPINSTRUMENT
    else:
        tt = 'only valid when cash posting'
    ael_variables.cp_instrument.enable(int(cpInstrumentEnable), tt)
    # Then call the callback of this field.
    fieldValues = ael_variables.cp_instrument.callback(fieldValues)
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

def cbExpirationHandling(index, fieldValues):
    """
    Callback for field expiration_handling.
    """
    # Then call enabler on dependent fields -- call enablers on fields
    #     alsoArchiveInstruments, cp_instrument, and cp_in_underlying.
    #tt = 'Instrument operation, no need for trade selection.'
    #ael_variables.TradeQuery.enable(0, tt)
    
    fieldValues = enCPInstrument(fieldValues)

    return fieldValues

def cbOnArchivedInst(index, fieldValues):
    fieldValues = enInstrument(fieldValues)
    return fieldValues
    
# ======= AEL variables ======================================================
global ael_variables
ael_variables = FBDPGui.TestVariables(
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled] FArchiveInstruments.cbExpirationHandling,
    ['expiration_handling',
     'Action',
     'string', actions, ACTION_NEW_EXPIRATION_ARCHIVE,
     1, 0, TOOLTIP_EXP_ACT, cbExpirationHandling, 1, None],

    ['instype',
     'Instrument Type',
     'string', sorted([s for s in acm.FEnumeration['enum(InsType)'].Enumerators()]), '',
     1, 0, TOOLTIP_INSTYPE, 1, None],

    ['max_runtime',
     'Maximum Runtime (s)_Advanced',
     'int', None, 3600,
     0, 0, TOOLTIP_MAX_RUNTIME, None, 1, None],

    ['cp_instrument',
     'Cash posting instrument_Advanced',
     'FInstrument', None, None,
     0, 1, TOOLTIP_CPINSTRUMENT, cbCPInstrument, 0, None],

    ['start_period',
     'Start Date Period',
     'string', '', '',
     0, 0, TOOLTIP_Date_Period, 1, None],

    ['end_period',
     'End Date Period',
     'string', '', '-1Y',
     1, 0, TOOLTIP_Date_Period, 1, None],
    )


def ael_main(parameters):
    # Parameters    
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(SCRIPT_NAME,
                      parameters['Logmode'],
                      parameters['LogToConsole'],
                      parameters['LogToFile'],
                      parameters['Logfile'],
                      parameters['SendReportByMail'],
                      parameters['MailList'],
                      parameters['ReportMessageType'])
                      
    
    # Required parameters for FInstrumentArchive script
    archive_ins_parameters = {
        'ScriptName': 'Archive Instruments',
        'instrument_selection': 'Untraded Instruments ABSA filtering',
        'expiration_handling': 'Archive',
        'TradeQuery': [],
        'TradingPortfolios': [],
        'TradeFilter': [],
        'PortfolioGrouper': [],
        'cp_in_underlying': 0,
        'deepArchive': 0,
        'alsoArchiveInstrument': 1,
        'alsoArchiveDerivative': 0,
        'preservePL': 0,
    }

    instype = parameters['instype']
    action_to_perform = 0 if parameters['expiration_handling'] == 'Archive' else 1
    end_date = _get_date_from_period(parameters['end_period'])
    
    if parameters['start_period']:
        start_date = _get_date_from_period(parameters['start_period'])
        if start_date > end_date:
            raise Exception('Invalid date period: %s start period can not be after %s end period' 
                            % (start_date, end_date), 'ERROR' )
                            
        result_set = _get_untraded_instruments(instype, action_to_perform, 
                            end_date.to_string(ael.DATE_ISO), start_date.to_string(ael.DATE_ISO))
    else:
        result_set = _get_untraded_instruments(instype, action_to_perform, end_date.to_string(ael.DATE_ISO))
    
    if not result_set:
        Logme()('No instruments found to archive. Skipping...', 'INFO')
        
    instrument_ids = [row[0] for row in result_set[0]]
    #instrument_ids = ['EUR/EUROSTOXX/18DEC2020/1970']

    if not instrument_ids:
        Logme()('No instruments found to archive. Skipping...', 'INFO')
        
    else:
        Logme()("Found %i instruments..." % len(instrument_ids), 'INFO')
        
        archive_ins_parameters['instruments']   = instrument_ids
        archive_ins_parameters.update(parameters)
        
        # Call core archive script
        FArchiveInstruments.ael_main(archive_ins_parameters)

