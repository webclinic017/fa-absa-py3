"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportAPIBase -FReportBuilder class contains logic for building reports. The
    constuctor takes a parameters object which defines the content of the report.
    A report is based on a workbook or one or more trading sheet templates.
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""
import acm

import time
import threading

import FReportAPIBaseUtils
import FPrimeXmlUtils        
import FAMBOutput
import FLogger
import FMacroGUI

logger = FLogger.FLogger( 'FAReporting' )

class FReportBuilder( object ):          
    
    def __init__( self, params ):
        self.params = params
        self.xml_report_writer = FPrimeXmlUtils.PrimeXmlReportWriter()
        self.generatedFilePaths = []

    def isSet(self, property):
        if property:
            return True
        else:
            return False                         
    
    @classmethod
    def getReportBuilder( cls, params ):
        """factory function for getting builder instance"""
        return FReportBuilder( params )
    
    ''' Private methods for creating reports '''    
    def removeSheetSheetingSimulations( self, reportGrid, sheetType ):
        """remove sheet settings"""
        if self.doSimulateSheetSettings( sheetType ):
            for settingsSheetType, selectedSheetSettings in self.params.sheetSettings.items():
                for columnId, value in selectedSheetSettings.items():
                    if value == '': continue
                    reportGrid.RemoveGlobalSimulation( columnId )
                    logger.LOG( 'Removed column simulation: %s < %s >.', settingsSheetType, columnId ) 

    def doSimulateSheetSettings( self, sheetType ):
        """simulate sheet settings"""
        simulateSettings = ( ( sheetType == 'FPortfolioSheet' and self.params.overridePortfolioSheetSettings == 'True' ) or
                             ( sheetType == 'FTimeSheet' and self.params.overrideTimeSheetSettings == 'True' ) or 
                             ( sheetType == 'FTradeSheet' and self.params.overrideTradeSheetSettings == 'True' )
                            )
        return simulateSettings
        
    def simulateSheetSettings( self, reportGrid, sheetType ):
        """simulate sheet settings"""
        
        if self.doSimulateSheetSettings( sheetType ):
            for settingsSheetType, selectedSheetSettings in self.params.sheetSettings.items():
                if sheetType == settingsSheetType:
                    for columnId, value in selectedSheetSettings.items():
                        if value == '': continue
                        successful = False
                        error = ''
                        try:
                            successful = reportGrid.SimulateGlobalValue( columnId, value )
                        except StandardError as e:
                            successful = False
                            error = str( e )
                        if not successful:
                            logger.ELOG( 'Simulation failed: %s < %s >; %s', sheetType, columnId, error )
                        else:
                            logger.LOG( 'Simulated column: %s < %s, %s >.', sheetType, columnId, value )
    
    """Split the names and values.Ignore escaped characters and
    treat comma separated values inside [] as multiple values"""
    def splitMacros(self, macros):
        
        
        startIndex = 0
        splitMacrosList = []
        isEnclosed = False
        
        if macros.find(',', 0, len(macros)) != -1:
        
            for index in range(0, len(macros)):
                
                if isEnclosed == False:
                    
                    if macros[index] == '[':
                        if index > 0 and macros[index-1] != '\\':
                            isEnclosed = True
                            continue
                        else:
                            continue
                
                
                    elif macros[index] == ',':
                        if index > 0 and macros[index-1] != '\\':
                            splitMacrosList.append(macros[startIndex:index])
                        else:
                            continue

                        startIndex = index+1
                        
                        if macros.find(',', startIndex, len(macros)) == -1:
                            #Add the last macro as well
                            splitMacrosList.append(macros[startIndex:len(macros)])
                            
                else:
                    if macros[index] == ']':
                        if index > 0 and macros[index-1] != '\\':
                            isEnclosed = False
                                    
                            if macros.find(',', index, len(macros)) == -1:
                                #Add the last macro as well
                                splitMacrosList.append(macros[startIndex:len(macros)])
                        else:
                            continue
            if len(splitMacrosList) == 0:
                splitMacrosList.append(macros[0:len(macros)])
        else:
            #Just add the string
            splitMacrosList.append(macros[0:len(macros)])
        
        return splitMacrosList
    
    
    def macrosAndValuesToDictionary(self, splitMacrosList):
        dict = acm.FDictionary()
        
        for macro in splitMacrosList:
            finalMacro = ''
            
            for index in range(0, len(macro)):
                prevChar = ''
                
                if index != 0:
                    prevChar = macro[index-1]
                
                if  (macro[index] != '[' and macro[index] != ']') or prevChar == '\\' :
                    finalMacro = finalMacro + macro[index]
            
            nameValue = []
            startIndex = 0
            for index in range(0, len(finalMacro)):
                if index >=0 and index < len(finalMacro) and finalMacro[index] == '=' and finalMacro[index-1] != '\\':
                
                    nameValue.append(finalMacro[startIndex:index])
                    nameValue.append(finalMacro[index+1:len(finalMacro)])
                    startIndex = index+1
            
            if len(nameValue) == 2:
                dict.AtPut(nameValue[0], nameValue[1])
                
        return dict
    
    
    
    def macrosToSheetParamInfo(self):
        """Supply the FSheetParameterizationInfo object
        with the macros input by the user. Separate each
        macro name and it's value and add them as key,value
        in a dictionary. The FSheetParameterizationInfo object
        is later passed into the OpenSheet method"""
        
        paramInfo = None
        
        if self.params.macros != None:
            split = self.splitMacros(self.params.macros)
            dict = self.macrosAndValuesToDictionary(split)
            
            if dict.Size() > 0:
                paramInfo = acm.FSheetParameterizationInfo()
                paramInfo.Macros(dict)
        
        return paramInfo
            
    def createReportGridBySheet(self, tradingSheet, includeRows, containerName, infoManMacroInfoFromGUI = None):   
        """create a report grid for the specified sheet. """
        
        FReportAPIBaseUtils.generateReportName(self, tradingSheet, containerName )
        output = acm.FXmlReportOutput('')
        output.EnableWhitespace(False)        
        reportGrid = None
        try:                            
            reportGrid = acm.Report.CreateReport(self.params.reportName, output)
            gridConfig = acm.Report.CreateGridConfiguration(self.params.instrumentParts, includeRows, True, self.params.expandTimebucketChildren )
            sheetSetup = None
            if tradingSheet.IsKindOf('FDealSheet'):
                gridConfig = gridConfig.Merge(acm.Report.CreateDealGridConfiguration(True, False, self.params.instrumentParts))
            if tradingSheet.IsKindOf('FPortfolioSheetBase'):
                sheetDefinition = acm.Sheet().GetSheetDefinition(tradingSheet.Class() )
                sheetSetup = sheetDefinition.CreateSheetSetup()
                if self.params.timeBuckets:
                    sheetSetup.TimeBucketsTemplate(self.params.timeBuckets.TimeBuckets() )
                if self.params.verticalScenario:
                    sheetSetup.VerticalScenario(self.params.verticalScenario.Scenario() )

            if tradingSheet.IsKindOf('FOrderSheet') and self.params.orders:
                # FOrderSheet report: If the user has specified a set of orders, the filtering should be disabled
                enableFilter = False
                gridConfig = gridConfig.Merge(acm.Report.CreateOrderGridConfiguration(enableFilter) )
            
            paramInfo = self.macrosToSheetParamInfo()
            reportGrid.OpenSheet(tradingSheet, gridConfig, sheetSetup, paramInfo)

            output.IncludeFormattedData(self.params.includeFormattedData)
            output.IncludeDefaultData(self.params.includeDefaultData)
            output.IncludeRawData(self.params.includeRawData)
            output.IncludeFullData(self.params.includeFullData)
            output.IncludeColorInformation(self.params.includeColorInformation)
            
            self.addContentToReportGrid( reportGrid, tradingSheet, infoManMacroInfoFromGUI)
            
            return reportGrid, output
        except Exception as details:   
            logger.ELOG( 'Report grid creation for ' + tradingSheet.Category() + ' (' + self.params.reportName + ') failed: ' + str(details) )            
            return None, None        
    
    def useMacroGUI(self, queries):
        if self.params.useMacroGUI == "True":
            providedMacros = acm.FArray()
            for query in queries:
                infoManQueryMacros = acm.FInformationManagerQueryMacros()
                infoManQueryMacros.PopulateFromQuery(query)
                providedMacros.Add(infoManQueryMacros)                
            
            shell = acm.UX.SessionManager().Shell()
            fInformationManagerQueriesMacros = acm.UX.Dialogs().GetMultipleInfoManagerQueriesMacros(shell, queries, providedMacros)
            
            return fInformationManagerQueriesMacros
                
    def addContentToReportGrid( self, reportGrid, tradingSheet, infoManMacroInfoFromGUI = None ):
        """add additional content to report grid"""
        
        result = acm.FArray()        
        if not reportGrid:  
            pass            
        elif tradingSheet.IsKindOf('FPortfolioSheet'):
            self.addPortfolios(reportGrid, self.params.portfolios)
            self.addPortfolios(reportGrid, self.params.tradeFilters)
            if self.params.storedASQLQueries:
                self.insertItems(reportGrid, self.params.storedASQLQueries)             
            if self.params.trades:
                self.insertItems(reportGrid, self.params.trades)
            self.addInfoManQueriesTrades(reportGrid, infoManMacroInfoFromGUI, result)
            self.insertItems(reportGrid, result)
            
        elif tradingSheet.IsKindOf('FVerticalPortfolioSheet'):
            self.insertItems(reportGrid, self.params.portfolios)             
            self.insertItems(reportGrid, self.params.tradeFilters)             
            if self.params.storedASQLQueries:            
                self.insertItems(reportGrid, self.params.storedASQLQueries)             
            if self.params.trades:
                self.insertItems(reportGrid, self.params.trades)             
            self.addInfoManQueriesTrades(reportGrid, infoManMacroInfoFromGUI, result)
            self.insertItems(reportGrid, result)
        
        elif tradingSheet.IsKindOf('FMoneyFlowSheet'):
            self.insertItems(reportGrid, self.params.portfolios)             
            self.insertItems(reportGrid, self.params.tradeFilters)             
            if self.params.storedASQLQueries:            
                self.insertItems(reportGrid, self.params.storedASQLQueries)             
            if self.params.trades:
                self.insertItems(reportGrid, self.params.trades)             
            self.addInfoManQueriesTrades(reportGrid, infoManMacroInfoFromGUI, result)
            self.addInfoManQueriesInstrument(reportGrid, infoManMacroInfoFromGUI, result)
            self.insertItems(reportGrid, result)        
            
        elif tradingSheet.IsKindOf('FRiskMatrixSheet'):                
            self.insertItems(reportGrid, self.params.portfolios)             
            self.insertItems(reportGrid, self.params.tradeFilters)             
            self.addInfoManQueriesTrades(reportGrid, infoManMacroInfoFromGUI, result)
            self.insertItems(reportGrid, result)            
            
        elif tradingSheet.IsKindOf('FTradeSheet'):
            if self.params.tradeRowsOnly:
                self.addPortfolioTrades(reportGrid, self.params.portfolios, result)            
                self.addPortfolioTrades(reportGrid, self.params.tradeFilters, result)            
                self.addStoredASQLQueryTrades(reportGrid, result)
                self.addTrade(reportGrid, result)                
                result = result.Sort()
            else:            
                if self.params.portfolios:            
                    result.AddAll(self.params.portfolios)            
                if self.params.tradeFilters:            
                    result.AddAll(self.params.tradeFilters)            
                if self.params.storedASQLQueries:            
                    result.AddAll(self.params.storedASQLQueries)
                self.addTrade(reportGrid, result)
            self.addInfoManQueriesTrades(reportGrid, infoManMacroInfoFromGUI, result)
            self.insertItems(reportGrid, result)             
            if self.params.instrumentParts:      
                builder = reportGrid.GridBuilder()      
                builder.Refresh()      
                builder.RowTreeIterator().Tree().Expand(True, 100)      
                
        elif tradingSheet.IsKindOf('FOrderSheet'):
            self.insertItems(reportGrid, self.params.orders)
            
        elif tradingSheet.IsKindOf('FTimeSheet'):                
            timeBuckets = self.params.timeBuckets
            if timeBuckets and timeBuckets.IsKindOf('FStoredTimeBuckets'):
                timeBuckets = timeBuckets.TimeBuckets()
                builder = reportGrid.GridBuilder()      
                builder.DefaultTimeBuckets(timeBuckets)      
            self.insertItems(reportGrid, self.params.portfolios, 10)             
            self.insertItems(reportGrid, self.params.tradeFilters, 10)
            
        elif tradingSheet.IsKindOf('FDealSheet'):
            result = acm.FArray()            
            if self.params.storedASQLQueries:
                self.insertItems(reportGrid, self.params.storedASQLQueries)
            if self.params.storedASQLQueriesInstrument:
                self.insertItems(reportGrid, self.params.storedASQLQueriesInstrument)            
            self.addInfoManQueriesTrades(reportGrid, infoManMacroInfoFromGUI, result)
            self.addInfoManQueriesInstrument(reportGrid, infoManMacroInfoFromGUI, result)
            self.insertItems(reportGrid, result)
            
    def addPortfolios(self, reportGrid, toAdd):     
        """ Add portfolio(s) to portfolio sheet. """                
            
        if not toAdd:            
            return            
            
        grouper = self.params.grouping
        if grouper.IsKindOf('FStoredPortfolioGrouper'):
            grouper = grouper.PortfolioGrouper()
            
        comparator = None                 
        builder = reportGrid.GridBuilder()      
            
        for prf in toAdd:                                        
            strPrf = None
            if prf.IsKindOf('FPhysicalPortfolio'):
                strPrf = 'portfolio '
            elif prf.IsKindOf('FTradeSelection'):
                strPrf = 'trade filter '
            if strPrf:
                logger.LOG( 'Added ' + strPrf + str(prf.Name()) + ' to ' + reportGrid.Value().AsString() )
                builder.AddPortfolio(prf, grouper, comparator, not self.params.portfolioRowOnly, self.params.instrumentParts,\
                                     self.params.zeroPositions, True, self.params.expiredPositions, self.params.instrumentRows)

    def insertItems(self, reportGrid, toInsert, expandLevels = 0):     
        """ Insert object(s) in sheet. """                
            
        if not toInsert:            
            return            
        
        builder = reportGrid.GridBuilder()      
        
        grouper = self.params.grouping
        if grouper.IsKindOf('FStoredPortfolioGrouper'):
            grouper = grouper.PortfolioGrouper()
        
        for item in toInsert:
            
            self.logInsertItems(reportGrid, item)
            
            tree = builder.InsertItem(item)
            
            if tree:
                
                if grouper and item.IsKindOf('FTrade') == False:
                    try:
                        self.applyGrouper(tree, grouper)
                    except AttributeError:
                        pass
                
                if tree.IsKindOf('FBuiltTreeProxy'):
                    
                    visibilityController = tree.VisibilityController()
                    
                    if visibilityController != None and visibilityController.IsKindOf('FPortfolioTreeVisibilityController'):
                    
                        if visibilityController.IsShowExpiredPositionsSupported():
                            visibilityController.ShowExpiredPositions(self.params.expiredPositions)
                            
                        if visibilityController.IsShowZeroPositionsSupported():
                            
                            if visibilityController.IsInstrumentLevelZeroPositionSupported():
                                visibilityController.InstrumentLevelZeroPosition(True)
                            
                            visibilityController.ShowZeroPositions(self.params.zeroPositions)
                        
                        if visibilityController.IsShowInstrumentRowsSupported():
                            visibilityController.ShowInstrumentRows(self.params.instrumentRows)
                            
                        builder.Refresh()
                            
                if expandLevels > 0:
                    builder.Refresh()
                    tree.Expand(True, expandLevels)
        
    
    def applyGrouper(self, tree, grouper):
        
        if tree.IsKindOf('FBuiltTreeProxy'):
            tree.ApplyGrouper(grouper)
            
        else:
            iter = tree.Iterator()
            
            if iter.HasChildren():
                c = iter.FirstChild()
                while c:
                    self.applyGrouper(c.Tree(), grouper)
                    c = iter.NextSibling()

    
    def logInsertItems(self, reportGrid, item):     
        """ Log objects inserted with insertItems func, simplifies when inserting FIndexedCollection. """                
            
        if not item:            
            return            
            
        strPrf = None
        if item.IsKindOf('FPhysicalPortfolio'):
            strPrf = 'portfolio '
        elif item.IsKindOf('FTradeSelection'):
            strPrf = 'trade filter '
        elif item.IsKindOf('FStoredASQLQuery'):
            strPrf = 'stored ASQL query '
        elif item.IsKindOf('FIndexedCollection'):
            for collItem in item:                                        
                self.logInsertItems(reportGrid, collItem)
        if strPrf:
            logger.LOG("Added " + strPrf + "'" + str(item.Name()) + "' to " + reportGrid.Value().AsString())
        
    def addPortfolioTrades(self, reportGrid, toAdd, result):
        """add portfolios trades to trade sheet. """
        
        if not toAdd:            
            return            
            
        for prf in toAdd:      
            strPrf = None
            if prf.IsKindOf('FPhysicalPortfolio'):
                strPrf = 'portfolio '
            elif prf.IsKindOf('FTradeSelection'):
                strPrf = 'trade filter '                            
            if strPrf:
                trades = prf.Trades()
                if trades and trades.Size():
                    result.AddAll(trades)
                    logger.LOG( "Added trades in " + strPrf + "'" + str(prf.Name()) + "' to " + reportGrid.Value().AsString() )                
        
    def addStoredASQLQueryTrades(self, reportGrid, result):
        """add trades in asql query result to trade sheet. """
        
        if not self.params.storedASQLQueries:            
            return            
            
        
        for storedQuery in self.params.storedASQLQueries:      
            if not storedQuery.QueryClass() == acm.FTrade:
                msg = "Wrong query class of stored asql query '" + str(storedQuery.Name()) + "'. Expected FTrade, got " + str(storedQuery.QueryClass().Name()) + '. Report ' + reportGrid.Value().AsString()
                logger.LOG(msg)                
                raise Exception(msg)
        
            query = storedQuery.Query()        
            queryResult = query.Select_Triggered()        
            queryResultResult = queryResult.Result()        
        
            if queryResultResult and queryResultResult.Size():        
                result.AddAll(queryResultResult)
                logger.LOG( "Added trades found by stored asql query '" + str(storedQuery.Name()) + "' to " + reportGrid.Value().AsString() )                

    def infoManQueryResult(self, reportGrid, queries, queryType, infoManMacroInfoFromGUI, infoManMacroInfoOffset, result):
        macros={}
        
        if self.params.useMacroGUI == "True":
            indexMacros = infoManMacroInfoOffset
            for query in queries:
                
                sqlAndParams = acm.FSQLAndParameters()
                sqlAndParams.SetSQL(query)
                sqlAndParams.SetParameters(infoManMacroInfoFromGUI[indexMacros])
                
                result.Add(sqlAndParams)
                indexMacros = indexMacros + 1        
        else:
            if self.params.macros:
                FMacroGUI.split_macrostring(self.params.macros, macros)
            
            for query in queries:
                if not query.SubType() == queryType:
                    msg = "Wrong sub type of FSQL query '" + str(query.Name()) + "'. Expected " + str(queryType) + ", got " + str(query.SubType()) + '. Report ' + reportGrid.Value().AsString()
                    logger.LOG(msg)                
                    raise Exception(msg)
                
                infoManQueryMacros = acm.FInformationManagerQueryMacros()
                infoManQueryMacros.PopulateFromQuery(query)
                infoManQueryMacros.SetMacroValuesByName(macros)
                
                sqlAndParams = acm.FSQLAndParameters()
                sqlAndParams.SetSQL(query)
                sqlAndParams.SetParameters(infoManQueryMacros)
            
                result.Add(sqlAndParams)

    def addInfoManQueriesTrades(self, reportGrid, infoManMacroInfoFromGUI, result):
        """add trades in fsql query result to trade sheet. """                                          
        if not self.params.infoManQueriesTrades:            
            return
        self.infoManQueryResult(reportGrid, self.params.infoManQueriesTrades, 'Trade', infoManMacroInfoFromGUI, 0, result)
            
    def addInfoManQueriesInstrument(self, reportGrid, infoManMacroInfoFromGUI, result):
        """add trades in fsql query result to trade sheet. """                           
        if not self.params.infoManQueriesInstrument:            
            return 
            
        offsetInfoManMacroInfoFromGUI = 0
        if self.params.infoManQueriesTrades:
            offsetInfoManMacroInfoFromGUI = self.params.infoManQueriesTrades.Size()
        self.infoManQueryResult(reportGrid, self.params.infoManQueriesInstrument, 'Instrument', infoManMacroInfoFromGUI, offsetInfoManMacroInfoFromGUI, result)
        

    def addTrade(self, reportGrid, result):
        """add trades to grid"""
        if self.params.trades:
            result.AddAll(self.params.trades)

    def periodic_cb(self, nbrOfCells):
        """perform memory clearing operations suitable for large batch reports"""
        for eb in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
            eb.Reset()
        acm.Memory().GcWorldStoppedCollect()    
        acm.FCache.Select01('.StringKey = "evaluators"', "").Statistics()
        acm.FCache.Select01('.StringKey = "evaluator builders"', "").Statistics()        

        
    def createReportOutput(self, sheets, terminateReportGrid = False, infoManMacroInfoFromGUI = None):	
        """create the report XML. """
        reportGrids = []
        for tradingSheet, containerName in sheets:
            xml_sheet_output = ''
            output = None
            if not tradingSheet.TradingSheetDefinition().AllowCreateReport():
                logger.LOG('Omitted sheet: ' + tradingSheet.SheetName() + '. Report creation not allowed for sheet type: ' + tradingSheet.Category())                
                continue
            else:
                reportGrid, output = self.createReportGridBySheet(tradingSheet, not self.params.clearSheetContent, containerName, infoManMacroInfoFromGUI)
                if not reportGrid:
                    continue
                
                reportGrids.append(reportGrid)
                sheetType = str( tradingSheet.ClassName() )
                self.gc( reportGrid )
                self.applyWaitForRemote( reportGrid )
                backgroundFinalize = acm.Memory().GcBackgroundFinalization()
                try:
                    acm.Memory().GcBackgroundFinalization(False)
                    xml_sheet_output = self.generateReportGridOutput( reportGrid, sheetType, output )
                    
                finally:
                    acm.Memory().GcBackgroundFinalization(backgroundFinalize)
            
            xml_sheet_writer = FPrimeXmlUtils.PrimeXmlSheetWriter( sheet_name=tradingSheet.SheetName() )
            xml_sheet_writer.xml_chunks( xml_chunk=xml_sheet_output )
            self.xml_report_writer.xml_sheet_writers( sheet_writer=xml_sheet_writer )
        
        return reportGrids
           
    def gc( self, reportGrid):
        """perform garbage collection"""
        if self.params.performanceStrategy == self.params.getPerformanceStrategies()[0]:
            reportGrid.SetPeriodicCB( self.periodic_cb, int(self.params.gcInterval))
            reportGrid.EnableCellCache(False)
            
    def applyWaitForRemote( self, reportGrid ):
        if self.params.waitForRemote:
            reportGrid.MaxAsynchIterations(5)
            
    def generateReportGridOutput( self, reportGrid, sheetType, output ):
        """generate grid"""
        try:
            self.simulateSheetSettings( reportGrid, sheetType )
            reportGrid.Generate()
        finally:
            self.removeSheetSheetingSimulations( reportGrid, sheetType )
        return output.AsString()
        
    def performReportCreation(self, sheets):   
        """perform creation of report(s). """
        
        queriesForMacroGUI = acm.FArray()
        if self.params.useMacroGUI == "True":
            if self.params.infoManQueriesTrades and self.params.infoManQueriesInstrument:
                queriesForMacroGUI.AddAll(self.params.infoManQueriesTrades)
                queriesForMacroGUI.AddAll(self.params.infoManQueriesInstrument)
            elif self.params.infoManQueriesTrades:
                queriesForMacroGUI.AddAll(self.params.infoManQueriesTrades)
            elif self.params.infoManQueriesInstrument:
                queriesForMacroGUI.AddAll(self.params.infoManQueriesInstrument)
        
        infoManMacroInfoFromGUI = None
        if self.params.useMacroGUI == "True":
            infoManMacroInfoFromGUI = self.useMacroGUI(queriesForMacroGUI)        
        
        for reportNbr in range(self.params.numberOfReports):
            lastReportTime = time.time()              
            FReportAPIBaseUtils.generateFileName(self, sheets)
            self.xml_report_writer.reset() 
            
            
            self.reportGrids = self.createReportOutput(sheets, False, infoManMacroInfoFromGUI)
            
            report_xml_output = self.xml_report_writer.get_xml_output()
                              
            self.produceOutput( report_xml_output )
            self.pollForEvents( reportNbr, lastReportTime )
            
            for grid in self.reportGrids:
                grid.Terminate()
            
            self.reportGrids = None
            
        return report_xml_output       
        logger.LOG('Report creation finished.')                        
    
    def pollForEvents( self, reportNbr, lastReportTime ):
        """poll for events between reports"""
        if reportNbr < (self.params.numberOfReports - 1):
            time.sleep(max(0.0, lastReportTime + self.params.updateInterval - time.time()))
            acm.PollDbEvents()
                
    def additionalProcessing(self, function, reportXml=''):                            
        """call function specified in the Processing tab (GUI). """
        
        if not function:            
            return        
        try:
            func = FReportAPIBaseUtils.getAttributeFromModule( function )
            return func(self, self.params.param, reportXml)    
        except Exception as details:
            logger.ELOG('Additional processing, error in function: ' + function + ' (' + str( details ) + ')' )

    def produceOutput(self, reportXml):
        """write output to difference sources"""
        reportXml = str(reportXml)
        
        #Pre processing xml
        if self.params.preProcessXml:
            reportXml = self.additionalProcessing(self.params.preProcessXml, reportXml)

        outputDir = FReportAPIBaseUtils.createOutputDir(self)

        if self.params.xmlToFile:
            FReportAPIBaseUtils.writeXMLToFile(self, reportXml, outputDir)

        if self.params.htmlToFile or self.params.htmlToPrinter:
            FReportAPIBaseUtils.writeHTMLToFile(self, reportXml, outputDir)

        if self.params.secondaryOutput:
            FReportAPIBaseUtils.writeToSecondaryOutput(self, reportXml, outputDir)
        
        if self.params.xmlToAmb:
            FAMBOutput.sendXMLToAMB(reportXml, self.params.ambAddress, self.params.ambSender, self.params.ambSubject, self.params.ambXmlMessage)
        
        self.additionalProcessing(self.params.function)
    
    def produceOutputReturnHtml(self, reportXml):
        reportXml = str(reportXml)
        
        #Pre processing xml
        if self.params.preProcessXml:
            reportXml = self.additionalProcessing(self.params.preProcessXml, reportXml)
            
        return FReportAPIBaseUtils.createHTML(self, reportXml, "")
    
    def generateReportXml( self ):
        """generate report xml only"""
        sheets = FReportAPIBaseUtils.getTradingSheets(self)
        reportXml = self.performReportCreation(sheets)
        return reportXml
        
    def generateReport( self ):
        """generate report"""
        sheets = FReportAPIBaseUtils.getTradingSheets(self)
        if self.params.multiThread:            
            thread = acm.FThread()
            logger.LOG('Multi threaded report creation.')            
            thread.Run(self.performReportCreation, [sheets])            
        else:            
            self.performReportCreation(sheets) 

    #For testing purposes mainly
    def generateReportReturnXml( self ):
        """generate report"""
        sheets = FReportAPIBaseUtils.getTradingSheets(self)
        return self.performReportCreation(sheets) 
    
    def create_report_by_xml( self, inputXml):
        """create report with existing xml"""
        if self.params.fileName == '':
            self.params.fileName = 'untitled'
        self.produceOutput(inputXml)       
   
