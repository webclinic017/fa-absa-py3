""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FDividendPointIndexProcessing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDividendPointIndexProcessing- Module which regenerates dividend cashflows

DESCRIPTION
    This is the start-script for the procedure to calculate and store
    dividends. It mainly contains the parameter GUI. 
    The script FDividendPointIndexProcessingPerform then takes
    over the execution of the procedure.
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)

ScriptName = 'FDividendPointIndexProcessing'
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', 
        ScriptName)

acm_dates = [acm.Time.DateToday(), 'Today']

# Tool Tips

ttStartDate = ('Start date for processing.')
ttEndDate = ('End date for processing.')
ttInstruments = 'Choose the Dividend Point Index Instruments you wish to process.'
ttMoveTo = 'Choose to move the points/skew to Mid, Last or Call/Put.'

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['StartDate',
                'Start Date',
                'string', acm_dates, 'Today',
                1, False, ttStartDate, None],
        ['EndDate',
                'End Date',
                'string', acm_dates, 'Today',
                1, False, ttEndDate, None],
        ['Instruments',
                'Dividend Point Index Instruments',
                'FDividendPointIndex', None, None,
                None, 1, ttInstruments, None, None],
)


def ael_main(dictionary):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPCurrentContext
    import FDividendPointIndexProcessingPerform
    importlib.reload(FDividendPointIndexProcessingPerform)
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    dictionary['ScriptName'] = ScriptName
    FBDPCommon.execute_script(FDividendPointIndexProcessingPerform.perform, dictionary)

