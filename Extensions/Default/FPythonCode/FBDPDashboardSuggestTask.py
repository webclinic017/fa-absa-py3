""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardSuggestTask.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm


DASHBOARD_TASK_NAME = 'BDP_Dashboard_Suggest'


AGGREGATION_MODULE_NAME = 'FAggregation'
AGGREGATION_PARAMETERS_TEXT = ('diff_test=0;workbook=;report_path=;Logmode=2;'
        'ReportMessageType=Full Log;Logfile=BDP.log;LogToConsole=1;'
        'LogToFile=0;used_context=Standard;sheet_names=;SendReportByMail=0;'
        'bypassTradeValidation=0;aggrule_filters=;MailList=;date=Today;')
EXPIRATION_MODULE_NAME = 'FExpiration'
EXPIRATION_PARAMETERS_TEXT = ('MailList=;alsoArcOrDelIns=1;'
        'expiration_handling=Archive and cash post positions;Testmode=1;'
        'MaxRunTime=3600;cp_in_underlying=0;allowGeneric=0;'
        'instruments=;SendReportByMail=0;cp_instrument=;LogToFile=0;'
        'ReportMessageType=Full Log;Logfile=BDP_Expiration.log;allowLive=0;'
        'portfolios=;report_path=c:\\temp;Logmode=1;LogToConsole=1;'
        'log_report=0;')
DELETEPRICES_MODULE_NAME = 'FDeletePrices'
DELETEPRICES_PARAMETERS_TEXT = ('MailList=;Markets=;DateMtM=Yesterday;'
        'DumpDirPath=;KeepEndOfMonth=0;Testmode=1;SendReportByMail=0;'
        'MtMMarkets=internal;DropExpIns=1;Protected=;LogToFile=0;'
        'CheckForPricesWithoutIns=1;ReportMessageType=Full Log;'
        'Logfile=BDP.log;Instruments=;DateLast=Yesterday;DelSelPrc=0;'
        'SavePrices=0;Logmode=2;LogToConsole=1;MaxRuntime=;')
FXAGGREGATION_MODULE_NAME = 'FFxAggregation'
FXAGGREGATION_PARAMETERS_TEXT = ('TradeQuery=;deaggregate=0;Logmode=2;'
        'ReportMessageType=Full Log;Logfile=BDP.log;LogToConsole=1;LogToFile=0'
        ';SendReportByMail=0;TradingPortfolios=;TradeFilter=;MailList=;'
        'PortfolioGrouper=;Testmode=1;date=Today;')
BENCHMARKTEST_MODULE_NAME = 'FBDPBenchmarkTest'
BENCHMARKTEST_PARAMETERS_TEXT = ('MailList=;createNew=1;simulate=0;'
        'cleanUp=0;lastTradeDate=Today;firstTradeDate=-6m;SendReportByMail=0;'
        'numberOfInstruments=1;numberOfTradesPerIns=1000;Instruments=;'
        'LogToFile=0;numberOfCloneTrades=1;ReportMessageType=Full Log;'
        'Logfile=BDP.log;Instruments=;'
        'Logmode=2;LogToConsole=1;')

TRADEROLLOUT_MODULE_NAME = 'FTradeRollout'
TRADEROLLOUT_PARAMETERS_TEXT = ('MailList=;date=;useAggRules=1;'
        'Testmode=1;aggRuleFilters=;tradeFilters=;SendReportByMail=0;'
        'rolloutToAMBA=0;rolloutToXML=0;filePath=;'
        'useBatching=0;maxBatchSize=500;'
        'LogToFile=0;ReportMessageType=Full Log;'
        'Logfile=BDP.log;Instruments=;'
        'Logmode=2;LogToConsole=1;')

def _getOrCreateTheAelTask(dashboardTaskName=DASHBOARD_TASK_NAME):

    if not dashboardTaskName:
        return None
    if not isinstance(dashboardTaskName, str):
        return None
    aelTask = acm.FAelTask[dashboardTaskName]
    if not aelTask:
        aelTask = acm.FAelTask()
        aelTask.Name(dashboardTaskName)
        aelTask.Commit()
    return aelTask


def _updateTheAelTask(aelTask, moduleName=''):

    if not moduleName:
        return aelTask
    if aelTask.ModuleName() == moduleName:
        return aelTask
    aelTask.ModuleName(moduleName)
    # udpate parameters text
    if moduleName == AGGREGATION_MODULE_NAME:
        aelTask.ParametersText(AGGREGATION_PARAMETERS_TEXT)
    elif moduleName == EXPIRATION_MODULE_NAME:
        aelTask.ParametersText(EXPIRATION_PARAMETERS_TEXT)
    elif moduleName == DELETEPRICES_MODULE_NAME:
        aelTask.ParametersText(DELETEPRICES_PARAMETERS_TEXT)
    elif moduleName == FXAGGREGATION_MODULE_NAME:
        aelTask.ParametersText(FXAGGREGATION_PARAMETERS_TEXT)
    elif moduleName == BENCHMARKTEST_MODULE_NAME:
        aelTask.ParametersText(BENCHMARKTEST_PARAMETERS_TEXT)
    elif moduleName == TRADEROLLOUT_MODULE_NAME:
        aelTask.ParametersText(TRADEROLLOUT_PARAMETERS_TEXT)
    else:
        aelTask.ParametersText()
    # commit and return
    aelTask.Commit()
    return aelTask


def startSuggestTask(moduleName):
    theAelTask = _updateTheAelTask(_getOrCreateTheAelTask(), moduleName)
    acm.StartApplication('Run Script', theAelTask)
