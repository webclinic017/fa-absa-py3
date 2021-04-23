""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FExportBase.py"
"""-------------------------------------------------------------------------------------------------------
MODULE

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION


-------------------------------------------------------------------------------------------------------"""
import acm
import datetime
import FIntegration
import FColumnToXMLGenerator
import FExportProcess
import FExportUtils
import FileCreator
import FFileTransporter
import FPostTransformation
import FExportBaseConfiguration
import FBusinessProcessUtils
import FSyncronizeBPWithCurrentState
import FSyncronizeBPWithTransHist
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")



def CreateIntegration(params):
    custom_integration_module = FExportUtils.import_custom_integration_module(params.Custommodule)
    if custom_integration_module and 'TradeTransitions' in dir(custom_integration_module):
        try:
            trade_transition = custom_integration_module.TradeTransitions()
        except Exception as e:
            logger.warn("Error in Custom Integration Trade Transition. " + str(e.message) +
                        '. Using default Trade Transition')
            trade_transition = FIntegration.TradeTransitions()
    else:
        trade_transition = FIntegration.TradeTransitions()

    integration = FIntegration.FIntegration(integrationId=params.stateChartName,
                                            tradeTransitions = trade_transition)
    integration.XSLTTemplateFinderFunction(lambda _: params.xsltTemplateName)
    integration.SheetTemplateFinderFunction(lambda _: params.tradingSheetTemplateName)
    integration.FilenameFunction(FExportBaseConfiguration.FilenameFunction)
    integration.FilePathFunction(lambda _: params.FilePath)
    integration.ContactFinderFunction(lambda _: None)
    integration.FileTransferFinderFunction(lambda _: FExportBaseConfiguration.FileTransferFinderFunction(params))
    integration.ExportEventId(FExportBaseConfiguration.ExportEventId())
    integration.ChartId(params.stateChartName)
    integration.TradeACMQueryPrefix(params.tradeQuery)
    integration.PartyFinderFunction(FExportBaseConfiguration.PartyFinderFunction)
    integration.InstrumentExport = params.InstrumentExport
    try:
        integration.TradeExport = params.TradeExport
        integration.QueryIntersection = params.QueryIntersection
    except:
        pass
    integration.insFile = params.Instrument_iFileName
    integration.TradeFile = params.FileName
    integration.InstrumentACMQueryPrefix = FExportBaseConfiguration.InstrumentACMQueryPrefix
    integration.InstrumentChartId = FExportBaseConfiguration.InstrumentChartId
    integration.LinkedExportObjects(((lambda t: t.Instrument(), integration.InstrumentChartId(params.Instrument_istateChartName), 'Instruments'),))
    integration.InstrumentStateChart = params.Instrument_istateChartName
    postTransformationFunction = None
    if not params.postTransformationFunction == '':
        split_str = params.postTransformationFunction.split('.')
        module = __import__(split_str[0])
        postTransformationFunction = getattr(module, split_str[1])
    
    integration.PostTransformationFunction(postTransformationFunction)
    integration.iPostTransformationFunction(postTransformationFunction)
    return integration

def UpdateInstrumentExportStates(businessProcesses):
    for bp in businessProcesses.BusinessProcesses():
        try:
            # Revalidate that the business process is still in the required state for an export
            if bp.Subject_type() == "Instrument":
                ins = bp.Subject()
                if "InsStatus" in dir(ins.AdditionalInfo()):
                    ins_status = ins.AdditionalInfo().InsStatus()
                    for st in FIntegration.InstrumentTransitions():
                        if FBusinessProcessUtils.IsValidEvent(bp, st.EventId()) and ins_status == st.ToStatus():
                            bp.HandleEvent(st.EventId())
                            bp.Commit()		
        except RuntimeError as e:
            logger.error('Business process %d failed to handle event "%s"', bp.Oid(), e)

def UpdateObjectExportStates(params, integration, instrumentQueries = dict(), retryFailedExports=False):
    exportStateUpdater = None
    if not hasattr(params, 'QueryIntersection') or (params.TradeExport == 'true' and params.QueryIntersection == 'true'):
        if  hasattr(params, 'UsTransHist') and params.UsTransHist == 'false':
            exportStateUpdater = FSyncronizeBPWithCurrentState.FSyncronizeBPWithCurrentState(integration, additionalQueryDictionary = instrumentQueries)
            exportStateUpdater.InitialiseIntegration()
        else:
            exportStateUpdater = FSyncronizeBPWithTransHist.FSyncronizeBPWithTransHist(integration, additionalQueryDictionary = instrumentQueries)
            exportStateUpdater.InitialiseIntegration()
    else:
        if params.InstrumentExport == 'true':
            exportStateUpdater = FSyncronizeBPWithTransHist.FSyncronizeBPWithTransHistInsExport(integration, additionalQueryDictionary = instrumentQueries)
            exportStateUpdater.InitialiseIntegration()
        if params.TradeExport == 'true':
            exportStateUpdater = FSyncronizeBPWithTransHist.FSyncronizeBPWithTransHistTradeExport(integration, additionalQueryDictionary = instrumentQueries)
            exportStateUpdater.InitialiseIntegration()
    if exportStateUpdater:
        exportStateUpdater.Execute()
    if retryFailedExports:
        if params.TradeExport == 'true':
            FExportUtils.RevertBusinessProcessesInErrorState(integration.ChartId())
        if params.InstrumentExport == 'true':
            FExportUtils.RevertBusinessProcessesInErrorState(integration.InstrumentStateChart)

def CreateExportProcess(integration, tradeQueries, alwaysGenerateFile, exportParameters, testMode, additionalQueries):
    exportProcess = []
    if not hasattr(exportParameters, 'QueryIntersection') or (exportParameters.QueryIntersection == 'true' and exportParameters.TradeExport == 'true'):
        exportProcess = exportProcess + [FExportProcess.FExportProcess(integration, tradeQueries, additionalQueryDictionary = additionalQueries,
            additionalParameters = exportParameters, testMode=testMode, alwaysGenerateFile = alwaysGenerateFile)]
    else: 
        if exportParameters.InstrumentExport == 'true':
            exportProcess = exportProcess + [FExportProcess.FExportInsProcess(integration, tradeQueries, additionalQueryDictionary = additionalQueries,
                additionalParameters = exportParameters, testMode=testMode, alwaysGenerateFile = alwaysGenerateFile)]
        if exportParameters.TradeExport == 'true':
            exportProcess = exportProcess + [FExportProcess.FExportTradeProcess(integration, tradeQueries, additionalQueryDictionary = additionalQueries,
                additionalParameters = exportParameters, testMode=testMode, alwaysGenerateFile = alwaysGenerateFile)]
    for process in exportProcess:
        ExportObjects(integration, tradeQueries, alwaysGenerateFile, exportParameters, testMode, additionalQueries, process)
	
def ExportObjects(integration, tradeQueries, alwaysGenerateFile, exportParameters, testMode, additionalQueries, exportProcess):
	
    bpn = exportProcess.LoadBusinessProcesses()
    if exportParameters.InstrumentExport == 'true':
        UpdateInstrumentAmendmendStates(exportProcess)
    if exportParameters.UpdateExportStateOnly == 'false':
        CreateFile(bpn, exportProcess, exportParameters, alwaysGenerateFile)
        FPostTransformation.FPostTransformation(exportProcess).Execute()
        FFileTransporter.FFileExporter(exportProcess).Execute(retries=0, retryDelay=60)
        if exportParameters.InstrumentExport == 'true':
            UpdateInstrumentExportStates(exportProcess)
        return exportProcess.BusinessProcesses()

def CreateFile(bpn, exportProcess, exportParameters, alwaysGenerateFile):

    FColumnToXMLGenerator.FColumnToXMLGenerator(exportProcess).Execute(validateOutput=True)
    header = exportParameters.header
    footer = exportParameters.footer
    now = datetime.datetime.now()
    variables = {
            '%SHEET_TEMPLATE%':exportParameters.tradingSheetTemplateName,
            '%NTRADES%':str(bpn),
            '%RECIPIENTS%': exportParameters.EmailRecipient
    }
    for variable, value in variables.items():
        header = header.replace(variable, value)
        footer = footer.replace(variable, value)
    _filecreator = FileCreator.FFileCreator(exportProcess, header, footer)
    _filecreator.Execute()
    if alwaysGenerateFile == 'true' and not bpn:
        if  not _filecreator._exportProcess.SingleExportsAsList():
            sheetTemplateId = exportProcess._SheetTemplateId(exportProcess.TradeQueryIdList()[0])
            partyId = exportProcess._PartyId(None)
            import FSingleExportIdentifier
            singleExportIdentifier = FSingleExportIdentifier.FSingleExportIdentifier(exportProcess, partyId, sheetTemplateId)
            key = singleExportIdentifier.KeyValue()
            if not exportProcess._singleExport.has_key(key):
                exportProcess._singleExport[key] = FExportProcess.FSingleExport(singleExportIdentifier, exportProcess.Integration())
            FColumnToXMLGenerator.FColumnToXMLGenerator(exportProcess).Execute(validateOutput=True)
        try:
            field = _filecreator._GetFileData(_filecreator._exportProcess.SingleExportsAsList()[0])
            with open(field[2], "wb") as outputFile:
                outputFile.write("")
        except IOError as e:
            raise Exception("Failed to write file: " + str(e))
    

def UpdateInstrumentAmendmendStates(businessProcesses):
    for bp in businessProcesses.BusinessProcesses():
        try:
            # Revalidate that the business process is still in the required state for an export
            if bp.Subject_type() == "Instrument":
                ins = bp.Subject()
                if "InsStatus" in dir(ins.AdditionalInfo()):
                    ins_status = ins.AdditionalInfo().InsStatus()
                    if FBusinessProcessUtils.IsValidEvent(bp, 'Inst. Amended') and ins_status == 'Amend':
                        bp.HandleEvent('Inst. Amended')
                        bp.Commit()
                        ins.AdditionalInfo().InsStatus('Default')
                        ins.AdditionalInfo().Commit()
                        ins.Commit()
        except RuntimeError as e:
            logger.error('Business process %d failed to handle event "%s"', bp.Oid(), e)

def RunExport(params):

    if not hasattr(params, 'TradeExport') or params.TradeExport == 'true':
        trade_state_chart = acm.FStateChart[params.stateChartName]
        if not trade_state_chart:
            custom_integration_module = FExportUtils.import_custom_integration_module(params.Custommodule)
            if custom_integration_module and 'CreateExportStateChart' in dir(custom_integration_module):
                custom_integration_module.CreateExportStateChart(params.stateChartName)
            else:
                FExportUtils.CreateStandardExportStateChart(params.stateChartName)
    
        trade_state_chart = acm.FStateChart[params.stateChartName]
        FExportUtils.create_add_info("StateChart", 'StateChartType')
        if 'AdditionalInfo' in dir(trade_state_chart):
            trade_state_chart.AdditionalInfo().StateChartType('Export')
            trade_state_chart.Commit()
    if (params.InstrumentExport == 'true'):
        state_chart = acm.FStateChart[params.Instrument_istateChartName]
        if state_chart == None:
            FExportUtils.CreateInstrumentExportStateChart_adv(params.Instrument_istateChartName)
    if not hasattr(params, 'TradeExport') or params.TradeExport == 'true' or params.InstrumentExport == 'true':
        integration = CreateIntegration(params)
        retryFailedExports = (params.RetryFailedExports == 'true')
        additionalQueries = {'Instruments': params.Instrument_iQuery}
        UpdateObjectExportStates(params, integration, additionalQueries, retryFailedExports)
        testMode = not params.UpdateBusinessProcesses
        testMode = FExportBaseConfiguration.TestModeAlAndaluz(testMode)
        CreateExportProcess(integration, [params.tradeQuery], params.AlwaysGenerateFile, params, testMode, additionalQueries)