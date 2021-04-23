""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/FSACCRExport.py"
"""----------------------------------------------------------------------------
MODULE
    SACCRExport - Module which export the SACCR XML column on the instrument.

DESCRIPTION
    This is the start-script for the Export SACCR XML procedure. It mainly
    contains the parameter GUI. The script FSACCRExportPerform then takes
    over the execution of the procedure.
----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import SACCRSettings

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',)

qInstruments = FBDPGui.insertInstruments(generic=None, instype=('Credit Balance',))
qStoredFolder = FBDPGui.insertInstrumentStoredFolder()
dealDirName = SACCRSettings.SACCRDealOutFilePath()
dataDirName = SACCRSettings.SACCRMarketDataOutFilePath()
rateFixingsDirName = SACCRSettings.RateFixingFilePath()

def disable_variables(variables, enable=0, disabledTooltip=None):
    for i in variables:
        getattr(ael_variables, i).enable(enable, disabledTooltip)

def cbInputIns(index, fieldValues):
    for i in ('Instruments', 'InstrumentsQuery'):
        if index != getattr(ael_variables, i).sequenceNumber:
            disable_variables((i, ), (not fieldValues[index]),
                'You can only select Instruments or InstrumentsQuery.')
    return fieldValues

# ## Tool Tip


ttSelIns = 'Save SACCR XML for these instruments filtered by instrument filter.'
ttSelQuery = 'Save SACCR XML for these instruments filtered by stored folder.'
ttDealsExportPath = 'Deals export path'
ttAppendDateToDealsFolderName = 'Append date to deals export directory'
ttMarketDataExportPath = 'Market data export path'
ttAppendDateToMarketDataFolderName = 'Append date to market data export directory'
ttDistributedCalculations = ('Use distributed calculations for improved performance')
ttAppendDateToRateFixingsFolderName = 'Append date to rate fixing export directory'
ttRateFixingsExportPath = 'Rate fixing export path'

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['distributedCalculations',
                 'Use distributed calculations',
                 'int', [0, 1], 0,
                 True, False, ttDistributedCalculations, None, True],
        ['Instruments',
                'Instruments',
                'FInstrument', None, qInstruments,
                None, 1, ttSelIns, cbInputIns, None],
        ['InstrumentsQuery',
                'Stored Folder',
                'FStoredASQLQuery', None, qStoredFolder,
                None, 1, ttSelQuery, cbInputIns, None],
        ['AppendDateToDealsXMLDir',
                'Append date to folder name_Output settings',
                'int', ['0', '1'], 1,
                0, 0, ttAppendDateToDealsFolderName, None, None],
        ['DealsExportPath',
                'Deals export path_Output settings',
                'string', None, dealDirName,
                1, 0, ttDealsExportPath, None, None],
        ['AppendDateToMarketDataXmlDir',
                'Append date to folder name_Output settings',
                'int', ['0', '1'], 1,
                0, 0, ttAppendDateToMarketDataFolderName, None, None],
        ['MarketDataExportPath',
                'Market data export path_Output settings',
                'string', None, dataDirName,
                1, 0, ttMarketDataExportPath, None, None],
        ['AppendDateToRateFixingsFilesDir',
                'Append date to folder name_Output settings',
                'int', ['0', '1'], 1,
                0, 0, ttAppendDateToRateFixingsFolderName, None, None],
        ['RateFixingsExportPath',
                'RateFixings export path_Output settings',
                'string', None, rateFixingsDirName,
                1, 0, ttRateFixingsExportPath, None, None],
)


def ael_main(dictionary):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FSACCRExportPerform
    importlib.reload(FSACCRExportPerform)
    import FBDPCurrentContext

    ScriptName = 'Export SACCR XMLs'
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    FBDPCommon.execute_script(FSACCRExportPerform.perform,
            dictionary)
