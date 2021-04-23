import acm
import ael
import time
import threading
import FPrimeXmlUtils
import FLogger
import DDM_ATS_PARAMS as params

logger = FLogger.FLogger('CRT_ManualFeed')

class DDMReportBuilder:
    #report parameters
    clearSheetContent = True
    gcInterval = 5000
    includeDefaultData = True
    includeFormattedData = True
    includeFullData = False
    includeRawData = False
    includeColorInformation = False
    instrumentParts = False
    multiThread = False
    numberOfReports = 1
    overridePortfolioSheetSettings = False
    overrideTimeSheetSettings = False
    overrideTradeSheetSettings = False
    performanceStrategy = 'Periodic full GC to save memory'
    reportName = ''
    sheetSettings = {}
    templateName = None
    tradeNumbers = None
    thread = None
    xslStyleSheetName = None
    workbookName = None
    
    rawReportOutput = None
    transformedReportOutput = None
    
    def __init__(self):
        self.xmlReportWriter = FPrimeXmlUtils.PrimeXmlReportWriter()

    def isSet(self, property):
        if property:
            return True
        else:
            return False
    
    def getPerformanceStrategies(self):
        perf_strategy_gc = "Periodic full GC to save memory"
        perf_strategy_speed = "No extra GC"
        return [perf_strategy_gc, perf_strategy_speed] 
 
    def doSimulateSheetSettings( self, sheetType ):
        """simulate sheet settings"""
        simulateSettings = ( ( sheetType == 'FPortfolioSheet' and self.overridePortfolioSheetSettings == 'True' ) or
                             ( sheetType == 'FTimeSheet' and self.overrideTimeSheetSettings == 'True' ) or 
                             ( sheetType == 'FTradeSheet' and self.overrideTradeSheetSettings == 'True' )
                            )
        return simulateSettings
   
    def removeSheetSheetingSimulations( self, reportGrid, sheetType ):
        """remove sheet settings"""
        if self.doSimulateSheetSettings( sheetType ):
            for settingsSheetType, selectedSheetSettings in self.sheetSettings.items():
                for columnId, value in selectedSheetSettings.items():
                    if value == '': continue
                    reportGrid.RemoveGlobalSimulation( columnId )
                    logger.LOG( 'Removed column simulation: %s < %s >.', settingsSheetType, columnId ) 

    def simulateSheetSettings( self, reportGrid, sheetType ):
        """simulate sheet settings"""
        
        if self.doSimulateSheetSettings( sheetType ):
            for settingsSheetType, selectedSheetSettings in self.sheetSettings.items():
                if sheetType == settingsSheetType:
                    for columnId, value in selectedSheetSettings.items():
                        if value == '': continue
                        successful = False
                        error = ''
                        try:
                            successful = reportGrid.SimulateGlobalValue( columnId, value )
                        except StandardError, e:
                            successful = False
                            error = str( e )
                        if not successful:
                            logger.ELOG( 'Simulation failed: %s < %s >; %s', sheetType, columnId, error )
                        else:
                            logger.LOG( 'Simulated column: %s < %s, %s >.', sheetType, columnId, value )
                            
    def getTradingSheets(self):
        sheets = acm.FArray()
        
        #from template
        #if self.isSet(self.templateName): //Lukas review
        if self.templateName:
            template = acm.FTradingSheetTemplate[self.templateName]
            if not template:
                raise Exception("Could not load sheet template '" + self.templateName + "'")
            sheets.Add( ( template.TradingSheet(),  self.templateName ) )
            #logger.LOG('Using trading sheet template(s): %s (%s)' %((self.templateName),str(template.SubType())))
            
        #from workbook
        #if self.isSet(self.workbookName): //Lukas review
        if self.workbookName:
            workbook = acm.FWorkbook[self.workbookName]
            if not workbook:
                raise Exception("Could not load workbook '" + self.workbookName + "'")
                
            logger.LOG( 'Using workbook: ' + self.workbookName )
            for sheet in workbook.Sheets():
                sheets.Add( ( sheet, self.workbookName ) )
        
        if not sheets:
            msg = 'No sheet found! Please specify a valid trading sheet'
            logger.WLOG(msg)            
            raise Exception(msg)        
    
        return sheets
    
    
    def periodic_cb(self, nbrOfCells):
        """perform memory clearing operations suitable for large batch reports"""
        for eb in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
            eb.Reset()
        acm.Memory().GcWorldStoppedCollect()    
        acm.FCache.Select01('.StringKey = "evaluators"', "").Statistics()
        acm.FCache.Select01('.StringKey = "evaluator builders"', "").Statistics()
        
    def gc( self, reportGrid):
        if self.performanceStrategy == self.getPerformanceStrategies():
            reportGrid.SetPeriodicCB( self.periodic_cb, int(self.gcInterval))
            reportGrid.EnableCellCache(False)
    
    def addContentToReportGrid(self, reportGrid, tradingSheet):
        if not reportGrid:  
            return
        
        if tradingSheet.IsKindOf('FPortfolioSheet'):  
            #This needs some improvement....not really tested for more than one trade with the Or on the trade filter
            builder = reportGrid.GridBuilder()
            
            if self.tradeNumbers:
                
                #Create a temp trade filter using AEL
                tf = ael.TradeFilter.new()
                tf.fltid = "ddmTempFilter"
                #Set the first trade
                query = []
                tradeCount=0
                for tradeNumber in self.tradeNumbers:
                    tradeCount=tradeCount + 1
                    operator = ''
                    if tradeCount > 1:
                        operator = 'Or'
                    query.append((operator, '', 'Trade number', 'equal to', str(tradeNumber), ''))
                    tf.set_query(query)
               
                #Apply the query
                tf.apply()           
                #query = tf.get_query()
                  
                #Now fetch the trade filter as a acm FTradeSelection object to insert into the portfolio sheet
                acm_tf = acm.FTradeSelection[tf.fltnbr]
                #print acm_tf.Inspect()
                
                #get the trade number grouper
                storedPortfolioGrouper = acm.FStoredPortfolioGrouper[params.tradeNumberGrouperId]
                if not storedPortfolioGrouper:
                    raise Exception('Trade number stored portfolio grouper not found')
                elif not storedPortfolioGrouper.Grouper():
                    raise Exception('Grouper not defined on stored portfolio grouper')
                grouper = storedPortfolioGrouper.Grouper()
                
                #print acm_tf.Trades()
                builder.AddPortfolio(acm_tf, grouper, None, True, True, True, True, True, True, True) 
        
        else:
            #print '******************************** reached'
            result = acm.FArray()
            if self.tradeNumbers:
                for tradeNumber in self.tradeNumbers:
                    if tradeNumber.find(',') > -1:
                        s = tradeNumber.split(',')
                        for trd in s:
                            #print '*************** trade nr found *********',trd
                            print "Found trade: ", trd
                            trade = acm.FTrade[trd]
                            result.Add(trade)
                            ael.poll()
                    else:
                        trade = acm.FTrade[tradeNumber]
                        result.Add(trade)
            builder = reportGrid.GridBuilder()
            
            for item in result:                                        
                builder.InsertItem(item)
                
        if self.instrumentParts:      
            builder = reportGrid.GridBuilder()      
            builder.Refresh()      
            builder.RowTreeIterator().Tree().Expand(True, 100)
        
    def createReportGridBySheet(self, tradingSheet, includeRows, containerName):
        output = acm.FXmlReportOutput('')
        output.Clear()
        output.EnableWhitespace(False)        
        
        try:
            reportGrid = acm.Report.CreateReport(self.reportName, output)
            gridConfig = acm.Report.CreateGridConfiguration(self.instrumentParts, includeRows)
            reportGrid.OpenSheet(tradingSheet, gridConfig)
            output.IncludeFormattedData(self.includeFormattedData)
            output.IncludeDefaultData(self.includeDefaultData)
            output.IncludeRawData(self.includeRawData)
            output.IncludeFullData(self.includeFullData)
            self.addContentToReportGrid( reportGrid, tradingSheet )
            return reportGrid, output
            
        except Exception, details: 
            logger.ELOG( 'Report grid creation for ' + tradingSheet.Category() + ' (' + self.reportName + ') failed: ' + str(details) )            
            return None, None 
    
    def generateReportGridOutput(self, reportGrid, sheetType, output):
        try:
            self.simulateSheetSettings( reportGrid, sheetType )
            output.Clear()
            reportGrid.Generate()
        finally:
            self.removeSheetSheetingSimulations( reportGrid, sheetType )
        result = output.AsString()
        return result
    
    def createReportOutput(self, sheets):
        for tradingSheet, containerName in sheets:
            xml_sheet_output = ''
            output = None
            if not tradingSheet.TradingSheetDefinition().AllowCreateReport():
                logger.LOG('Omitted sheet: ' + tradingSheet.SheetName() + '. Report creation not allowed for sheet type: ' + tradingSheet.Category())
            else:
                reportGrid, output = self.createReportGridBySheet(tradingSheet, not self.clearSheetContent, containerName)
                if not reportGrid:
                    continue   
                sheetType = str( tradingSheet.ClassName() ) 
                self.gc( reportGrid ) 
                backgroundFinalize = acm.Memory().GcBackgroundFinalization() 
                try:
                    acm.Memory().GcBackgroundFinalization(False)
                    xml_sheet_output = self.generateReportGridOutput( reportGrid, sheetType, output )
                finally:
                    acm.Memory().GcBackgroundFinalization(backgroundFinalize)
            
            
            xml_sheet_writer = FPrimeXmlUtils.PrimeXmlSheetWriter( sheet_name=tradingSheet.SheetName() )
            xml_sheet_writer.xml_chunks( xml_chunk=xml_sheet_output )
            self.xmlReportWriter.xml_sheet_writers( sheet_writer=xml_sheet_writer )
    
    def doReportTransformation(self):
        if not self.rawReportOutput:
            return None
        
        if not self.xslStyleSheetName:
            raise Exception('XSL stylesheet name not specified')
            
        #Load the XSL stylesheet
        pt = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', self.xslStyleSheetName)
        if not pt:
            raise Exception("XSL template '" + self.xslStyleSheetName + "' not found")
        xsl = pt.Value()
        xslTransform = acm.CreateWithParameter('FXSLTTransform', xsl)
        if not xslTransform:
            raise Exception("Could not load XSL transform component from template '" + self.xslStyleSheetName + "'")
        
        self.transformedReportOutput = xslTransform.Transform(self.rawReportOutput) 
        
    
    def performReportCreation(self, sheets):
        for reportNbr in range(self.numberOfReports):
            lastReportTime = time.time()
            self.createReportOutput(sheets)
            report_xml_output = self.xmlReportWriter.get_xml_output()
            acm.PollDbEvents()
        self.rawReportOutput = report_xml_output
        self.doReportTransformation()
       
    def generateReportOutput(self):
        #Create a new instance of the xml report writer
        self.xmlReportWriter = FPrimeXmlUtils.PrimeXmlReportWriter()
        #logger.LOG("Starting report '%s' generation..." % self.reportName)
        self.rawReportOutput=None
        self.transformedReportOutput=None
        sheets = self.getTradingSheets()
        if self.multiThread:            
            self.thread = acm.FThread()
            self.thread.Run(self.performReportCreation, [sheets])   
            logger.LOG('Multi threaded report creation (threadId:%s).' %str(self.thread.Name()))  
        else:            
            self.performReportCreation(sheets) 
            
def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    
    return TrdFilter

def TemplateExtracts():
    TmplExtracts=[]
    TmplExtracts.append('CRT_Trade')
    TmplExtracts.append('CRT_Cash')
    
    return TmplExtracts
    
def FileExtracts():
    FlExtracts=[]
    FlExtracts.append('Trade_Extract')
    FlExtracts.append('Cash_Extract')
    
    return FlExtracts
    
def XSLTExtracts():
    xsltFormat = []
    xsltFormat.append('FCRTTradeExtract')
    xsltFormat.append('FCRTCashExtract')
    
    return xsltFormat

today              = acm.Time().DateNow()
tf                 = acm.FTradeFilter()

ael_variables = [
                    ['ReportName', 'Report Name', 'string', None, 'CRT_Extract', 1],
                    ['DrctValue', 'Drop path', 'string', None, 'C:\Personal\Projects\Eben\Front Arena\ExtractsTasks', 1],
                    ['XsltExtract', 'XSLT Format', 'string', XSLTExtracts(), 'FCRTTradeExtract', 1],
                    ['FileExtract', 'File Extract Name', 'string', FileExtracts(), 'Trade_Extract', 1],
                    ['TrdFilter', 'Trade Filter', 'string', TrdFilter(), 'CRT-Inflation-ResultSet', 1],
                    ['TradeNumber', 'Trade Number , del', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
                    ['Templates', 'Templates Filter', 'string', TemplateExtracts(), 'CRT_Trade', 1],
                    ['Date', 'Date', 'string', today, today, 1]]

def ExtractTrades(parameters):
    showLegs = acm.FACMServer().GetUserPreferences().ShowLegsInSheet()
    acm.FACMServer().GetUserPreferences().ShowLegsInSheet(True)

    reportBuilder = DDMReportBuilder()
    reportBuilder.clearSheetContent = True
    reportBuilder.includeDefaultData = False
    reportBuilder.includeFormattedData = True
    reportBuilder.includeFullData = False
    reportBuilder.includeRawData = False
    reportBuilder.includeColorInformation = False
    reportBuilder.instrumentParts = True
    reportBuilder.reportName = parameters['ReportName']
    reportBuilder.templateName = parameters['Templates']
    reportBuilder.xslStyleSheetName = parameters['XsltExtract']
            
    reportBuilder.rawReportOutput = None
    reportBuilder.transformedReportOutput = None

    if parameters['TradeNumber'] == '':
        #run with the trade filter
        print 'Generating specified trade numbers off filter'
        trdFilter = ael.TradeFilter[parameters['TrdFilter']]
        trades = ','.join( [str(t.trdnbr) for t in trdFilter.trades()] )
        print trades
        reportBuilder.tradeNumbers = [trades]            
    else:
        print 'Generating off specified trade numbers:', parameters['TradeNumber']
        reportBuilder.tradeNumbers = [parameters['TradeNumber']]
       
    reportBuilder.generateReportOutput()
    f = open(parameters['FileExtract'], 'w')
    f.write(reportBuilder.transformedReportOutput)
    f.close()
    
    acm.FACMServer().GetUserPreferences().ShowLegsInSheet(showLegs)

def ael_main(parameters):
    ExtractTrades(parameters)
