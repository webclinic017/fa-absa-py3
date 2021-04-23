""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/bdp_benchmark_test/./etc/FBDPBenchmarkTest.py"
"""----------------------------------------------------------------------------
MODULE
    FBDPBenchmarkTest - Performs Benchmark Tests

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module calls the FBDPBenchmarkTest_Perform procedure based on the
    parameters setup here.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)

ScriptName = 'FBDPBenchmarkTest'

qInstruments = FBDPGui.insertInstruments(generic=None)

class FBDPBenchmarkTest(FBDPGui.LogVariables):

    def enable_CreateNew(self, enabled):
        self.lastTradeDate.enable(enabled)
        self.firstTradeDate.enable(enabled)
        self.numberOfInstruments.enable(enabled)
        self.numberOfTradesPerIns.enable(enabled)
        
    def enable_Clone(self, enabled):
        self.Instruments.enable(enabled)
        self.numberOfCloneTrades.enable(enabled)

    def object_cb(self, index, fieldValues):        
        tt = 'You can only select one operation.'
        for field in (self.simulate, self.createNew,
                self.cleanUp):
            if self[index] != field:
                if fieldValues[index] == "1":
                    fieldValues[field.sequenceNumber] = 0
                    if field == self.createNew:
                        self.enable_CreateNew(0)
                    elif field == self.simulate:
                        self.enable_Clone(0)
            else:
                enabled = 1 if fieldValues[index] == "1" else 0
                if field == self.createNew:
                    self.enable_CreateNew(enabled)
                elif field == self.simulate:
                    self.enable_Clone(enabled)
        return fieldValues

    def __init__(self, *ael_variables):

        ttFirstDate = 'First date on which trades are created'
        ttLastDate = 'Last date on which trades are created'
        ttNumberOfInstruments = 'Number of instruments to be created'
        ttNumberOfTradesPerIns = 'Number of trades per instrument to be created'
        ttCreate = 'Create new entities'
        ttClone = 'Clone the existing trades'
        ttCleanUp = 'Clean up the BDP benchmark data'
        ttIns = 'Select the instruments to be cloned'
        ttNumberOfClonedTradesPerIns = 'Number of trades per instrument to be cloned'
        ttPortfolio = ''
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['createNew',
                        'Create',
                        'int', [0, 1], 1,
                        0, 0, ttCleanUp, self.object_cb, 1])
        self.createVariable(
                ['simulate',
                        'Clone',
                        'int', [0, 1], 0,
                        0, 0, ttCleanUp, self.object_cb, 1])

        self.createVariable(
                ['cleanUp',
                        'Clean Up',
                        'int', [0, 1], 0,
                        0, 0, ttCleanUp, self.object_cb, 1])
        self.createVariable(
                ['lastTradeDate',
                        'Last Trade Date_Create',
                        'string', [acm.Time.DateToday(), 'Today', '-6m', '-1y'], 'Today',
                        1, 0, ttNumberOfInstruments])
        self.createVariable(
                ['firstTradeDate',
                        'First Trade Date_Create',
                        'string', [acm.Time.DateToday(), 'Today', '-6m', '-1y'], '-6m',
                        1, 0, ttNumberOfInstruments])
        self.createVariable(
                ['numberOfInstruments',
                        'Number of Instruments_Create',
                        'int', None, 1,
                        1, 0, ttNumberOfInstruments, None, 1])
        self.createVariable(
                ['numberOfTradesPerIns',
                        'Number of Trades per Instrument_Create',
                        'int', None, 1000,
                        1, 0, ttNumberOfTradesPerIns, None, 1])
        self.createVariable(
                ['Instruments',
                        'Instruments_Clone',
                        'FInstrument', None, qInstruments,
                        1, 1, ttIns, None, 0])
        self.createVariable(
                ['numberOfCloneTrades',
                        'Number of Trades to Clone_Clone',
                        'int', None, 1,
                        1, 0, ttNumberOfClonedTradesPerIns, None, 0])
        FBDPGui.LogVariables.__init__(self, *ael_variables)
    

ael_variables = FBDPBenchmarkTest()

def ael_main(dictionary):
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPBenchmarkTest_Perform
    importlib.reload(FBDPBenchmarkTest_Perform)

    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPCommon.execute_script(FBDPBenchmarkTest_Perform.perform_test,
            dictionary)
