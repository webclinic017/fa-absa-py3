import logging

#General
sourceSystem="Frontarena"

#Logging
#Level 1=Info, 2=Debug, 3=Warn, 4=Error
logLevel=1

#SQL Connection
SQLServer='JHBPCM05002V05A\JF1_MAIN1_LIVE'
DatabaseName='MMG-DDM-PEGASUS'


#AMB Settings
ambAddress = 'jhbpsm02649n01:9300'
readerSubjectList = ['MMG_DDM_REQUEST']
writerMBName = 'P_DDM_ATS_GEN_SENDER'
writerSubjectList = 'ATS_DDM_REQUEST'

#When the ATS should restart
restartIfMemoryThresholdExceeded = True
memoryThreshold=1048576

#Intraday worker
intradayWorkerATSNameTemplate = 'DDM_ATS_INTRADAY_WORKER'
intradayAMBAReaderSubjectList = ['P_DDM_AMBA/INSTRUMENT', 'P_DDM_AMBA/TRADE']
intradayWorkerReaderMBName = 'P_DDM_ATS_INTRA_RECEIVER'

#Request controls
batchTradeSize=400
requestControlATSNameTemplate = 'DDM_ATS_REQUEST_CONTROL'
requestControlReaderSubjectTemplate = 'MMG_DDM_REQUEST_CONTROL'
requestControlReaderMBName = 'P_DDM_ATS_REQC_RECEIVER'

#Request workers
requestWorkerInstances=20
requestWorkerATSNameTemplate = 'DDM_ATS_REQUEST_WORKER'
requestWorkerReaderSubjectTemplate = 'ATS_DDM_REQUEST_WORKER'
requestWorkerReaderMBTemplate = 'P_DDM_ATS_RECEIVER'


#Trade Event (External MMG component that receives AMB events)
tradeEventListenerInstances=1
tradeEventListenerSubjectTemplate = 'ATS_DDM_TRADE'


#Attributes
includeStaticAttributes = True
includeDynamicAttributes = True
includeInstrument = True
includeUnderlyingInstruments = True
includeInstrumentLegs = True
includeMultiLeggedReportAttributes = True
includeSalesCredits = True
includeMoneyFlows = True
includeHistoricalCashFlows = False

#Attribute generation
dynamicAttributesWorkbookName = 'DDM_DynamicAttributes'
tradeSheetName = 'TRADE'
tradePortfolioSheetName = 'TRADEPORTFOLIO'
instrumentSheetName = 'INSTRUMENT'
legSheetName = 'LEG'
moneyFlowSheetName = 'MONEYFLOW'

#Number formatting
decimalFormat = '{0:0.08f}'

#Report Generation
tradeNumberGrouperId=5608
tradeSheetTemplateName='DDM_TRADE'
tradePortfolioSheetTemplate='DDM_TRADE_PORTFOLIO'
instrumentSheetTemplateName='DDM_INSTRUMENT'
legSheetTemplateName = 'DDM_LEG'
moneyFlowSheetTemplateName = 'DDM_MONEYFLOW'
tradeSheetXsl = 'DDM_TRADING_SHEET_TRANSFORM'
portfolioSheetXsl = 'DDM_PORTFOLIO_SHEET_TRANSFORM'
cashSheetXsl = 'DDM_CASH_SHEET_TRANSFORM'



