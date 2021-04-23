
"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportAPI - API that allows Python code to trigger the generation of reports.
    This API allows the specification of the same parameters as the Run Script GUI
    with FWorksheetReport. When creating report from Python code, the same defaults
    are used as visible when opening FWorksheetReport with Run Script GUI.
    
    A report is based on a workbook or one or more trading sheet templates.
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import os
import acm
import ael
import FReportAPIBase
import FReportSheetSettingsTab
import FReportUtils
import FLogger
try:
    basestring
except NameError: #Python3
    basestring = str
    
logger = FLogger.FLogger('FAReporting')

class FReportParametersBase( object ):
    
    def __init__( self ):
        self.__ambAddress = ''
        self.__ambSender = ''
        self.__ambSubject = ''
        self.__ambXmlMessage = None
        self.__clearSheetContent = None
        self.__compressXmlOutput = None
        self.__createDirectoryWithDate = None
        self.__yearWithCentury = None
        self.__dateFormat = ''
        self.__expiredPositions = None
        self.__fileDateFormat = ''
        self.__fileDateBeginning = None
        self.__fileName = None
        self.__filePath = ""
        self.__function = None
        self.__gcInterval = None
        self.__grouping = ''
        self.__headerImage = None
        self.__headerImagePath = ''
        self.__htmlToFile = None
        self.__htmlToPrinter = None
        self.__htmlToScreen = None
        self.__includeDefaultData = None
        self.__includeFormattedData = None
        self.__includeFullData = None
        self.__includeRawData = None
        self.__includeColorInformation = None
        self.__instrumentParts = None
        self.__expandTimebucketChildren = None
        self.__instrumentRows = None
        self.__maxNrOfFilesInDir = None
        self.__multiThread = None
        self.__numberOfReports = None
        self.__orders = None
        self.__overridePortfolioSheetSettings = None
        self.__overrideTimeSheetSettings = None
        self.__overrideTradeSheetSettings = None
        self.__overwriteIfFileExists = None
        self.__param = None
        self.__performanceStrategy = ''
        self.__portfolioReportName = ''
        self.__portfolioRowOnly = None
        self.__portfolios = None
        self.__preProcessXml = None
        self.__printStyleSheet = ''
        self.__printTemplate = ''
        self.__reportName = ''
        self.__secondaryFileExtension = ''
        self.__secondaryOutput = None
        self.__secondaryTemplate = ''
        self.__useUtf8ByteOrderMark = None
        self.__sheetSettings = None
        self.__snapshot = None
        self.__storedASQLQueries = None
        self.__storedASQLQueriesInstrument = None
        self.__infoManQueriesTrades = None
        self.__infoManQueriesInstrument = None
        self.__macros = None
        self.__useMacroGUI = None
        self.__template= None
        self.__timeBuckets= None
        self.__verticalScenario = None
        self.__tradeFilters = None
        self.__tradeRowsOnly = None
        self.__trades = None
        self.__updateInterval = None
        self.__workbook = None
        self.__xmlToAmb = None
        self.__xmlToFile = None
        self.__zeroPositions = None
        self.__guiParams = None
        self.__reportApiObject = None
        self.__macros = None
    
    def init_from_gui_params( self, params ): 
        init_from_gui_params( self, params )
        
    ''' Private methods '''
    def getPerformanceStrategies(self):
        perf_strategy_gc = "Periodic full GC to save memory"
        perf_strategy_speed = "No extra GC"
        return [perf_strategy_gc, perf_strategy_speed]        

    def getListFromExtensions(self, extensions):
        str = extensions.AsString().replace(']', '').replace('[', '').replace(' ', '')
        extensionsList = str.split(',')
        extensionsList.sort()
        return extensionsList    

    def getPrintTemplateNames(self):
        ctx = acm.GetDefaultContext()
        extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'print templates')    
        return self.getListFromExtensions(extensions)        

    def getSecondaryTemplateNames(self, ext = ''):
        if ext != '':        
            ext = ' ' + ext.replace('.', '')
        ctx = acm.GetDefaultContext()
        extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'secondary templates' + ext)
        return self.getListFromExtensions(extensions)
        
    def getCSSNames(self):
        ctx = acm.GetDefaultContext()
        extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'style sheets')
        return self.getListFromExtensions(extensions)

    def getObject(self, object, className):
        if className == 'FTrade':
            return self.getTrade(object)
        elif className == 'FPhysicalPortfolio':
            return self.getPhysicalPortfolio(object)
        elif className == 'FTradeSelection':
            return self.getTradeSelection(object)
        elif className == 'FTradingSheetTemplate':
            return self.getTradingSheetTemplate(object)
        elif className == 'FWorkbook':
            return self.getWorkbookObj(object)

    def getObjectAsArray(self, object, className):
        """
            Returns object as FArray.
            Object can be one of the following:
            string, int, tuple, list, FArray, FBusinessObject.
            Makes it possible to enter values in script in different formats
            e.g report.portfolio = 'PORTFOLIO1', 'PORTFOLIO2' (tuple) or
            report.portfolio = acm.FPhysicalPortfolio['PORTFOLIO1'].
        """
        objList = acm.FArray()
        #list
        if type(object) is list:
            for el in object:
                objList.Add(self.getObject(el, className))
        else:
            #tuple
            if isinstance(object, tuple):
                for el in object:
                    objList.Add(self.getObject(el, className))
            #int / string
            elif isinstance(object, int) or isinstance(object, basestring):
                objList.Add(self.getObject(object, className))
            #FBusinessObject: FTrade, FPhysicalPortfolio, etc.
            elif object.IsKindOf(className):
                objList.Add(object)
            #FArray of FBusinessObject
            elif object.IsKindOf('FArray'):
                for el in object:
                    if not el.IsKindOf(className):
                        msg = el.StringKey() + ' is not a ' + className
                        logger.ELOG(msg)
                        raise Exception(msg)
                objList = object
            #Wrong type
            else:
                msg = object.StringKey() + ' is not a ' + className
                logger.ELOG(msg)
                raise Exception(msg)
        return objList

    def getTradingSheetTemplate(self, tpl):
        res = acm.FTradingSheetTemplate.Select01('name = ' + tpl, '')
        if not res:
            msg = 'Template ' + str(tpl) + ' does not exist!'
            logger.ELOG( msg )
            raise Exception(msg)
        return res

    def getPhysicalPortfolio(self, p):
        res = acm.FPhysicalPortfolio[p]
        if not res:
            msg = 'Portfolio ' + str(p) + ' does not exist!'
            logger.ELOG(msg)
            raise Exception(msg)
        return res

    def getTrade(self, t):
        res = acm.FTrade[t]
        if not res:
            msg = 'Trade ' + str(t) + ' does not exist!'
            logger.ELOG( msg )
            raise Exception(msg)
        return res

    def getTradeSelection(self, t):
        res = acm.FTradeSelection[t]
        if not res:
            msg = 'Trade filter ' + str(t) + ' does not exist!'
            logger.ELOG( msg )
            raise Exception(msg)
        return res

    def getWorkbookObj(self, wb):
        res = acm.FWorkbook[wb]
        if not res:
            msg = 'Workbook ' + str(wb) + ' does not exist!'
            logger.ELOG( msg )
            raise Exception(msg)
        return res

    def getFileSelection(self, path):
        selection = acm.FFileSelection()
        selection.PickDirectory(True)
        #string / FFileSelection
        if isinstance(path, basestring):
            selection.SelectedDirectory = path
        else:
            selection.SelectedDirectory = path.SelectedDirectory()
        return selection

    ''' Private Getters '''
    #General tab --------------------------------
    def getWorkbook(self):
        return self.__workbook
    def getTemplate(self):
        return self.__template
    def getSheet(self):
        return self.__sheet
    def getInstrumentParts(self):
        return self.__instrumentParts
    def getExpandTimebucketChildren(self):
        return self.__expandTimebucketChildren
    def getClearSheetContent(self):
        return self.__clearSheetContent
    def getSnapshot(self):
        return self.__snapshot
    def getMultiThread(self):
        return self.__multiThread
    def getNumberOfReports(self):
        return self.__numberOfReports
    def getUpdateInterval(self):
        return self.__updateInterval
    def getMacros(self):
        return self.__macros

    #Add Sheet Content tab --------------------------
    def getPortfolios(self):
        return self.__portfolios
    def getTradeFilters(self):
        return self.__tradeFilters
    def getTradeRowsOnly(self):
        return self.__tradeRowsOnly
    def getStoredASQLQueries(self):
        return self.__storedASQLQueries
    def getStoredASQLQueriesInstrument(self):
        return self.__storedASQLQueriesInstrument        
    def getInfoManQueriesTrades(self):
        return self.__infoManQueriesTrades
    def getInfoManQueriesInstrument(self):
        return self.__infoManQueriesInstrument        
    def getMacros(self):
        return self.__macros
    def getUseMacroGUI(self):
        return self.__useMacroGUI        
    def getPortfolioRowOnly(self):
        return self.__portfolioRowOnly
    def getExpiredPositions(self):
        return self.__expiredPositions
    def getZeroPositions(self):
        return self.__zeroPositions
    def getInstrumentRows(self):
        return self.__instrumentRows
    def getGrouping(self):
        return self.__grouping
    def getTimeBuckets(self):
        return self.__timeBuckets
    def getVerticalScenario(self):
        return self.__verticalScenario
    
    def getTrades(self):
        return self.__trades
    def getOrders(self):
        return self.__orders

    #Output Settings tab ------------------------
    def getIncludeRawData(self):
        return self.__includeRawData
    def getIncludeFullData(self):
        return self.__includeFullData
    def getIncludeFormattedData(self):    
        return self.__includeFormattedData
    def getIncludeDefaultData(self):    
        return self.__includeDefaultData
    def getIncludeColorInformation(self):    
        return self.__includeColorInformation
    def getHeaderImage(self):
        return self.__headerImage
    def getHeaderImagePath(self):
        return self.__headerImagePath
    def getHtmlToFile(self):
        return self.__htmlToFile
    def getHtmlToScreen(self):
        return self.__htmlToScreen
    def getHtmlToPrinter(self):
        return self.__htmlToPrinter
    def getXmlToFile(self):
        return self.__xmlToFile
    def getFilePath(self):
        return self.__filePath
    def getFileName(self):
        return self.__fileName
    def getCompressXmlOutput(self):
        return self.__compressXmlOutput
    def getCreateDirectoryWithDate(self):
        return self.__createDirectoryWithDate
    def getYearWithCentury(self):
        return self.__yearWithCentury        
    def getDateFormat(self):
        return self.__dateFormat
    def getFileDateFormat(self):
        return self.__fileDateFormat
    def getFileDateBeginning(self):
        return self.__fileDateBeginning
    def getOverwriteIfFileExists(self):
        return self.__overwriteIfFileExists
    def getPrintTemplate(self):
        return self.__printTemplate
    def getPrintStyleSheet(self):
        return self.__printStyleSheet
    def getSecondaryOutput(self):
        return self.__secondaryOutput
    def getSecondaryTemplate(self):
        return self.__secondaryTemplate
    def getSecondaryFileExtension(self):
        return self.__secondaryFileExtension
    def getUseUtf8ByteOrderMark(self):
        return self.__useUtf8ByteOrderMark
    
    #sheet settings tabs--------------------------
    def getOverridePortfolioSheetSettings( self ):
        return self.__overridePortolioSheetSettings
        
    def getOverrideTimeSheetSettings( self ):
        return self.__overrideTimeSheetSettings
    
    def getOverrideTradeSheetSettings( self ):
        return self.__overrideTradeSheetSettings
    
    #AMB tab-------------------------------------
    def getXmlToAmb(self):
        return self.__xmlToAmb
    def getAmbAddress(self):
        return self.__ambAddress
    def getAmbSender(self):
        return self.__ambSender
    def getAmbSubject(self):
        return self.__ambSubject
    def getAmbXmlMessage(self):
        return self.__ambXmlMessage
    def getPerformanceStrategy(self):
        return self.__performanceStrategy
    def getWaitForRemote(self):
        return self.__waitForRemote

    #Post processing tab ------------------------
    def getFunction(self):
        return self.__function
    def getParam(self):
        return self.__param
    def getPreProcessXml(self):
        return self.__preProcessXml

    #Not set in GUI -----------------------------
    def getReportName(self):
        return self.__reportName
    def getPortfolioReportName(self):
        return self.__portfolioReportName
    def getSheetSettings(self):
        return self.__sheetSettings


    ''' Private Setters '''
    #General tab --------------------------------
    def setWorkbook(self, workbook):

        """ Allowed types: FWorkbook, str (valid workbook name). """
        if not workbook:            
            self.__workbook = ''
            return

        array = self.getObjectAsArray(workbook, 'FWorkbook')
        self.__workbook = array[0]        
        
    def setTemplate(self, template):
        """ Allowed types:
            str (valid template name), list (list of valid template names),
            FArray of FTradingSheetTemplate, FTradingSheetTemplate.
        """        
        if not template:            
            self.__template = ''
            return

        array = self.getObjectAsArray(template, 'FTradingSheetTemplate')
        self.__template = array        
        
    def setSheet(self, sheet):
        """ Allowed types:
            FTradingSheet object or FArray of FTradingSheet.
        """
        if not sheet:
            self.__sheet = ''
            return
        array = self.getObjectAsArray(sheet, 'FTradingSheet')
        self.__sheet = array
    
    def setInstrumentParts(self, instrumentParts):
        self.__instrumentParts = instrumentParts

    def setExpandTimebucketChildren(self, expandTimebucketChildren):
        self.__expandTimebucketChildren = expandTimebucketChildren
    
    def setClearSheetContent(self, clearSheetContent):
        self.__clearSheetContent = clearSheetContent
        
    def setSnapshot(self, snapshot):
        self.__snapshot = snapshot

    def setMultiThread(self, multiThread):
        self.__multiThread = multiThread

    def setNumberOfReports(self, numberOfReports):
        self.__numberOfReports = numberOfReports

    def setUpdateInterval(self, updateInterval):
        self.__updateInterval = updateInterval
        
    def setMacros(self, macros):
        self.__macros = macros

    #Add Portfolio tab --------------------------
    def setPortfolios(self, portfolios):
        """ Allowed types:
            str (valid portfolio name), list (list of valid portfolio names),
            FArray of FPhysicalPortfolio, FPhysicalPortfolio.
        """
        self.__portfolios = ''
        if not portfolios:
            return

        array = self.getObjectAsArray(portfolios, 'FPhysicalPortfolio')
        self.__portfolios = array

    def setTradeFilters(self, tradeFilters):
        """ Allowed types:
            str (valid trade filter name), list (list of valid trade filter names),
            FArray of FTradeSelection, FTradeSelection.
        """
        self.__tradeFilters = ''
        if not tradeFilters:
            return

        array = self.getObjectAsArray(tradeFilters, 'FTradeSelection')
        self.__tradeFilters = array
    
    def setTradeRowsOnly(self, tradeRowsOnly):
        self.__tradeRowsOnly = tradeRowsOnly

    def setStoredASQLQueries(self, storedASQLQueries):
        """ Allowed types:
            str (valid stored ASQL query name), list (list of valid stored ASQL query names),
            FArray of FStoredASQLQuery, FStoredASQLQuery.
        """
        self.__storedASQLQueries = ''
        if not storedASQLQueries:
            return

        array = self.getObjectAsArray(storedASQLQueries, 'FStoredASQLQuery')
        self.__storedASQLQueries = array
    
    def setStoredASQLQueriesInstrument(self, storedASQLQueriesInstrument):
        """ Allowed types:
            str (valid stored ASQL query name), list (list of valid stored ASQL query names),
            FArray of FStoredASQLQuery, FStoredASQLQuery.
        """
        self.__storedASQLQueriesInstrument = ''
        if not storedASQLQueriesInstrument:
            return

        array = self.getObjectAsArray(storedASQLQueriesInstrument, 'FStoredASQLQuery')
        self.__storedASQLQueriesInstrument = array    

    def setInfoManQueriesTrades(self, infoManQueriesTrades):
        """ Allowed types:
            str (valid stored FSQL query name), list (list of valid stored FSQL query names),
            FArray of FSQL, FSQL.
        """
        self.__infoManQueriesTrades = ''
        if not infoManQueriesTrades:
            return

        array = self.getObjectAsArray(infoManQueriesTrades, 'FSQL')
        self.__infoManQueriesTrades = array

    def setInfoManQueriesInstrument(self, infoManQueriesInstrument):
        """ Allowed types:
            str (valid stored FSQL query name), list (list of valid stored FSQL query names),
            FArray of FSQL, FSQL.
        """
        self.__infoManQueriesInstrument = ''
        if not infoManQueriesInstrument:
            return

        array = self.getObjectAsArray(infoManQueriesInstrument, 'FSQL')
        self.__infoManQueriesInstrument = array
        
    def setMacros(self, macros):
        self.__macros = macros

    def setUseMacroGUI(self, useMacroGUI):
        self.__useMacroGUI = useMacroGUI
        
    def setPortfolioRowOnly(self, portfolioRowOnly):
        self.__portfolioRowOnly = portfolioRowOnly
    
    def setExpiredPositions(self, expiredPositions):
        self.__expiredPositions = expiredPositions
    
    def setZeroPositions(self, zeroPositions):
        self.__zeroPositions = zeroPositions
    
    def setInstrumentRows(self, instrumentRows):
        self.__instrumentRows = instrumentRows
    
    def setGrouping(self, grouping):
        #if string, from Python script.
        try:
            if isinstance(grouping, basestring):
                if len(grouping) < 1:
                    grouping = acm.FDefaultGrouper()
                else:
                    grouping = [grouping]
            
            if type( grouping ) == type( acm.FDefaultGrouper() ):
                pass
            else:
                #if FArray, from Run Script.
                if len(grouping) < 1:
                    grouping = acm.FDefaultGrouper()
                else:
                    grouping = grouping[0]
                    grouperName = grouping
                    if isinstance(grouping, basestring):
                        grouping = acm.Risk().GetAllPortfolioGroupers().At(grouping)
                        # GetAllPortfolioGroupers returns FStoredPortfolioGrouper
                        # instances for the groupers in the database
                        if grouping and grouping.IsKindOf(acm.FStoredPortfolioGrouper):
                            grouping = grouping.Grouper()
                
        except Exception as details:
            msg = 'Error setting grouper. Please provide the grouper name as a string. ' + str(details)
            logger.ELOG( msg )
            raise Exception(msg)

        if not grouping:
            msg = 'Grouper ' + str(grouperName) + ' does not exist!'
            logger.ELOG( msg )
            raise Exception(msg)
        self.__grouping =  grouping
        

    def setVerticalScenario(self, scenario):
        self.__verticalScenario = scenario
        if scenario and scenario.IsKindOf('FIndexedCollection'):
             self.__verticalScenario = scenario[0]

    def setTimeBuckets(self, timeBuckets):
        self.__timeBuckets = None
        if timeBuckets is None:
            return
        #if string, from Python script.
        try:
            if isinstance(timeBuckets, basestring):
                if len(timeBuckets) < 1:
                    return
                else:
                    timeBuckets = [timeBuckets]
            
            #if FArray, from Run Script.
            if len(timeBuckets) < 1:
                return
            else:
                timeBuckets = timeBuckets[0]
                timeBucketsName = timeBuckets
                if isinstance(timeBuckets, basestring):
                    timeBuckets = acm.FStoredTimeBuckets[timeBuckets]
                
        except Exception as details:
            msg = 'Error setting time buckets. Please provide the stored time buckets name as a string. ' + str(details)
            logger.ELOG( msg )
            raise Exception(msg)

        if not timeBuckets:
            msg = 'Time buckets ' + str(timeBucketsName) + ' does not exist!'
            logger.ELOG( msg )
            raise Exception(msg)
        self.__timeBuckets = timeBuckets
    
    def setTrades(self, trades):
        """ Allowed types:
            int,
            list (list of valid trade numbers),
            FArray of FTrade, FTrade.
        """
        if not trades:
            self.__trades = ''
            return

        array = self.getObjectAsArray(trades, 'FTrade')
        self.__trades = array
        
    def setOrders(self, orders):
        """ Allowed types:
            int,
            list (list of valid order numbers),
            FArray of FOwnOrder, FOwnOrder.
        """
        if not orders:
            self.__orders = ''
            return

        array = self.getObjectAsArray(orders, 'FOwnOrder')
        self.__orders = array

    #Using 'True' / 'False' strings for the Output settings
    #Output Settings tab ------------------------
    def setIncludeRawData(self, includeRawData):
        self.__includeRawData = includeRawData
    def setIncludeFullData(self, includeFullData):
        self.__includeFullData = includeFullData
    def setIncludeDefaultData(self, includeDefaultData):
        self.__includeDefaultData = includeDefaultData
    def setIncludeFormattedData(self, includeFormattedData):
        self.__includeFormattedData = includeFormattedData
    def setIncludeColorInformation(self, includeColorInformation):
        self.__includeColorInformation = includeColorInformation
    def setHeaderImage(self, headerImage):
        self.__headerImage = headerImage
    def setHeaderImagePath(self, path):
        self.__headerImagePath = path
    def setHtmlToFile(self, htmlToFile):
        self.__htmlToFile = htmlToFile
    def setHtmlToScreen(self, htmlToScreen):
        self.__htmlToScreen = htmlToScreen
    def setHtmlToPrinter(self, htmlToPrinter):
        self.__htmlToPrinter = htmlToPrinter
    def setXmlToFile(self, xmlToFile):
        self.__xmlToFile = xmlToFile
    def setFilePath(self, filePath):
        self.__filePath = self.getFileSelection(filePath)
    def setFileName(self, fileName):
        self.__fileName = fileName
    def setCompressXmlOutput(self, compressXmlOutput):
        self.__compressXmlOutput = compressXmlOutput
    def setCreateDirectoryWithDate(self, createDirectoryWithDate):
        self.__createDirectoryWithDate = createDirectoryWithDate
    def setYearWithCentury(self, yearWithCentury):
        self.__yearWithCentury = yearWithCentury
    def setDateFormat(self, dateFormat):
        self.__dateFormat = dateFormat
    def setFileDateFormat(self, dateFormat):
        self.__fileDateFormat = dateFormat
    def setFileDateBeginning(self, dateBeginning):
        self.__fileDateBeginning = dateBeginning
    def setOverwriteIfFileExists(self, overwriteIfFileExists):
        self.__overwriteIfFileExists = overwriteIfFileExists

    def setPrintTemplate(self, printTemplate):
        context = acm.GetDefaultContext()
        found = False
        if printTemplate:
            for extensionName in self.getPrintTemplateNames():
                if extensionName == printTemplate: found = True
            if not found:
                msg = 'Print template ' + printTemplate + ' does not exist!'
                logger.ELOG( msg ) 
                raise Exception( msg )

        self.__printTemplate = printTemplate

    def setPrintStyleSheet(self, printStyleSheet):
        context = acm.GetDefaultContext()
        found = False
        for name in self.getCSSNames():
            if name == printStyleSheet: found = True
        if not found:
            msg = 'Print style sheet ' + printStyleSheet + ' does not exist!'
            logger.ELOG( msg )
            raise Exception( msg )
        else:
            self.__printStyleSheet = printStyleSheet

    def setSecondaryOutput(self, secondaryOutput):
        self.__secondaryOutput = secondaryOutput

    def setSecondaryTemplate(self, secondaryTemplate):
        context = acm.GetDefaultContext()
        found = False
        for extensionName in self.getSecondaryTemplateNames():
            if extensionName == secondaryTemplate: found = True
        if not found:
            msg = 'Print template ' + secondaryTemplate + ' does not exist!'
            logger.ELOG( msg )
            raise Exception( msg )
        else:
            self.__secondaryTemplate = secondaryTemplate

    def setSecondaryFileExtension(self, secondaryFileExtension):
        self.__secondaryFileExtension = secondaryFileExtension
        
    def setUseUtf8ByteOrderMark(self, useUtf8ByteOrderMark):
        self.__useUtf8ByteOrderMark = useUtf8ByteOrderMark
    
    #sheet settings tabs--------------------------------------
    def setOverridePortfolioSheetSettings( self, override ):
        self.__overridePortolioSheetSettings = override
        
    def setOverrideTimeSheetSettings( self, override ):
        self.__overrideTimeSheetSettings = override
    
    def setOverrideTradeSheetSettings( self, override ):
        self.__overrideTradeSheetSettings = override
        
    #AMB tab ------------------------------------------------
    def setXmlToAmb(self, xmlToAmb):
        self.__xmlToAmb = xmlToAmb
    def setAmbAddress(self, ambAddress):
        self.__ambAddress = ambAddress
    def setAmbSender(self, ambSender):
        self.__ambSender = ambSender
    def setAmbSubject(self, ambSubject):
        self.__ambSubject = ambSubject
    def setAmbXmlMessage(self, ambXmlMessage):
        self.__ambXmlMessage = ambXmlMessage
    def setPerformanceStrategy(self, performanceStrategy):
        if not performanceStrategy in self.getPerformanceStrategies():
            raise Exception("Invalid performance strategy: " + str(performanceStrategy) + \
                " valid choices = " + str(performance_strategies) )
        self.__performanceStrategy = performanceStrategy
    def setWaitForRemote(self, waitForRemote):
        self.__waitForRemote = waitForRemote

    #Post processing tab ------------------------------------
    def setFunction(self, function):
        self.__function = function
        
    def setParam(self, param):
        self.__param = param

    def setPreProcessXml(self, preProcessXml):
        self.__preProcessXml = preProcessXml

    #Not set in GUI -----------------------------
    def setReportName(self, reportName):
        self.__reportName = reportName
    
    def setPortfolioReportName(self, portfolioReportName):
        self.__portfolioReportName = portfolioReportName
    
    def setSheetSettings(self, sheetSettings ):
        self.__sheetSettings = sheetSettings


    '''Public Properties '''
    #General tab --------------------------------
    workbook = property(getWorkbook, setWorkbook)
    template = property(getTemplate, setTemplate)
    sheet = property(getSheet, setSheet)
    instrumentParts = property(getInstrumentParts, setInstrumentParts)
    expandTimebucketChildren = property(getExpandTimebucketChildren, setExpandTimebucketChildren)
    clearSheetContent = property(getClearSheetContent, setClearSheetContent)
    snapshot = property(getSnapshot, setSnapshot)
    multiThread = property(getMultiThread, setMultiThread)
    numberOfReports = property(getNumberOfReports, setNumberOfReports)
    updateInterval = property(getUpdateInterval, setUpdateInterval)
    macros = property(getMacros, setMacros)

    #Add Sheet Content tab -------------------------
    portfolios = property(getPortfolios, setPortfolios)
    tradeFilters = property(getTradeFilters, setTradeFilters)
    storedASQLQueries = property(getStoredASQLQueries, setStoredASQLQueries)
    storedASQLQueriesInstrument = property(getStoredASQLQueriesInstrument, setStoredASQLQueriesInstrument)
    infoManQueriesTrades = property(getInfoManQueriesTrades, setInfoManQueriesTrades)
    infoManQueriesInstrument = property(getInfoManQueriesInstrument, setInfoManQueriesInstrument)
    macros = property(getMacros, setMacros)
    useMacroGUI = property(getUseMacroGUI, setUseMacroGUI)
    tradeRowsOnly = property(getTradeRowsOnly, setTradeRowsOnly)
    portfolioRows = property(getPortfolioRowOnly, setPortfolioRowOnly)
    expiredPositions = property(getExpiredPositions, setExpiredPositions)
    zeroPositions = property(getZeroPositions, setZeroPositions)
    instrumentRows = property(getInstrumentRows, setInstrumentRows)
    grouping = property(getGrouping, setGrouping)
    timeBuckets = property(getTimeBuckets, setTimeBuckets)
    verticalScenario = property(getVerticalScenario, setVerticalScenario)
    trades = property(getTrades, setTrades)
    orders = property(getOrders, setOrders)    

    #Output settings tab ------------------------
    includeRawData = property(getIncludeRawData, setIncludeRawData)
    includeFullData = property(getIncludeFullData, setIncludeFullData)
    includeDefaultData = property(getIncludeDefaultData, setIncludeDefaultData)
    includeFormattedData = property(getIncludeFormattedData, setIncludeFormattedData)
    includeColorInformation = property(getIncludeColorInformation, setIncludeColorInformation)
    headerImage = property(getHeaderImage, setHeaderImage)
    headerImagePath = property(getHeaderImagePath, setHeaderImagePath)
    htmlToFile = property(getHtmlToFile, setHtmlToFile)
    htmlToScreen = property(getHtmlToScreen, setHtmlToScreen)
    htmlToPrinter = property(getHtmlToPrinter, setHtmlToPrinter)
    xmlToFile = property(getXmlToFile, setXmlToFile)
    filePath = property(getFilePath, setFilePath)
    fileName = property(getFileName, setFileName)
    compressXmlOutput = property(getCompressXmlOutput, setCompressXmlOutput)
    createDirectoryWithDate = property(getCreateDirectoryWithDate, setCreateDirectoryWithDate)
    yearWithCentury = property(getYearWithCentury, setYearWithCentury)
    dateFormat = property(getDateFormat, setDateFormat)
    fileDateFormat = property(getFileDateFormat, setFileDateFormat)
    fileDateBeginning = property(getFileDateBeginning, setFileDateBeginning)
    overwriteIfFileExists = property(getOverwriteIfFileExists, setOverwriteIfFileExists)
    printTemplate = property(getPrintTemplate, setPrintTemplate)
    printStyleSheet = property(getPrintStyleSheet, setPrintStyleSheet)
    secondaryOutput = property(getSecondaryOutput, setSecondaryOutput)
    secondaryTemplate = property(getSecondaryTemplate, setSecondaryTemplate )
    secondaryFileExtension = property(getSecondaryFileExtension, setSecondaryFileExtension)
    useUtf8ByteOrderMark = property(getUseUtf8ByteOrderMark, setUseUtf8ByteOrderMark)

    #Sheet settings tabs --------------------------------------------------
    overridePortfolioSheetSettings = property( getOverridePortfolioSheetSettings, setOverridePortfolioSheetSettings )
    overrideTimeSheetSettings = property( getOverrideTimeSheetSettings, setOverrideTimeSheetSettings )
    overrideTradeSheetSettings = property( getOverrideTradeSheetSettings, setOverrideTradeSheetSettings )
    
    #AMB
    xmlToAmb = property(getXmlToAmb, setXmlToAmb)
    ambAddress = property(getAmbAddress, setAmbAddress)
    ambSender  = property(getAmbSender, setAmbSender)
    ambSubject = property(getAmbSubject, setAmbSubject)
    ambXmlMessage = property(getAmbXmlMessage, setAmbXmlMessage)
    performanceStrategy = property(getPerformanceStrategy, setPerformanceStrategy)
    waitForRemote = property(getWaitForRemote, setWaitForRemote)

    #Post processing tab ------------------------------------------
    function = property(getFunction, setFunction)
    param = property(getParam, setParam)
    preProcessXml = property(getPreProcessXml, setPreProcessXml)

    #Not set in GUI -----------------------------------------------
    reportName = property(getReportName, setReportName)
    portfolioReportName = property(getPortfolioReportName, setPortfolioReportName)
    sheetSettings = property(getSheetSettings, setSheetSettings)

    ''' Public methods '''                
    @classmethod
    def GenerateReportXml( cls, params ):
        report_generator = FReportAPIBase.FReportBuilder.getReportBuilder( params )
        return report_generator.generateReportXml()
        
    def RunScript(self):
        """ Executes script """
        report_generator = FReportAPIBase.FReportBuilder.getReportBuilder( self )
        report_generator.generateReport()

    # Made for testing purposes. The output running the result can be inspected and used to verify that
    # the report produced matches what was ordered
    def RunScriptReturnReportXml(self):
        """ Executes script """
        report_generator = FReportAPIBase.FReportBuilder.getReportBuilder( self )
        return report_generator.generateReportReturnXml()

    # Made for testing purposes. The output running the result can be inspected and used to verify that
    # the report produced matches what was ordered
    def RunScriptReturnReportHtml(self, report_xml_ouput):
        """ Executes script """
        report_generator = FReportAPIBase.FReportBuilder.getReportBuilder( self )
        return report_generator.produceOutputReturnHtml(report_xml_ouput)
    
    def CreateReportByXml(self, inputXml):
        report_generator = FReportAPIBase.FReportBuilder( self )
        report_generator.create_report_by_xml( inputXml )

class FWorksheetReportParameters( FReportParametersBase ):        
    """
        Deprecated.
        Class for generating reports programmatically.
        Default parameters set from FExtensionValues.
    """
    
    def __init__(self, *settings):
        logger.WLOG( 'Deprecation Warning: The class FWorksheetReportParameters is deprecated. Prefer FWorksheetReportApiParameters.' )
        FReportParametersBase.__init__( self )
        init_from_ext_values( self, 'default' )
        for setting in settings:
            logger.LOG('Overriding settings with parameters < %s >', setting)
            init_from_ext_values( self, 'setting' ) 

class FWorksheetReportGuiParameters( FReportParametersBase ):
    """
        Class for generating reports when using RunScriptGui.
        Default parameters from FParameters and ael_variables defaults
    """
    def __init__( self, **kwds ):
        FReportParametersBase.__init__( self )
        self.gcInterval = 5000
        self.maxNrOfFilesInDir = 100
        self.portfolioReportName = ''
        self.reportName = ''
        self.guiParams = None
        
        for arg, value in kwds.items():
            if hasattr( self, arg ):
                setattr( self, arg, value )
            else:
                logger.WLOG( 'Skipping invalid keyword argument < %s >', arg )
    
        if self.guiParams:
            self.init_from_gui_params( self.guiParams )

class FWorksheetReportApiParameters( FReportParametersBase ):        
    """
        Class for generating reports programmatically.
        Default parameters set from constructor params
    """
    def __init__( self, **kwds):
        FReportParametersBase.__init__( self )
        self.ambAddress = '127.0.0.1:9137'
        self.ambSender = 'AMBA_SENDER'
        self.ambSubject = 'AMBA/XMLREPORT'
        self.ambXmlMessage = True
        self.clearSheetContent = False
        self.compressXmlOutput = False
        self.createDirectoryWithDate = True
        self.dateFormat = '%d%m%y'
        self.yearWithCentury = False
        self.expiredPositions = False
        self.fileDateFormat = '%y%m%d'
        self.fileDateBeginning = False
        self.fileName = None
        self.filePath = "c:\\"
        self.function = None
        self.gcInterval = 5000
        self.grouping = 'Default'
        self.htmlToFile = True
        self.htmlToPrinter = False
        self.htmlToScreen = True
        self.includeDefaultData = True
        self.includeFormattedData = True
        self.includeFullData = False
        self.includeRawData = False
        self.includeColorInformation = True
        self.instrumentParts = False
        self.expandTimebucketChildren = False
        self.instrumentRows = True
        self.maxNrOfFilesInDir = 1000
        self.multiThread = False
        self.numberOfReports = 1
        self.orders = None
        self.overridePortfolioSheetSettings = False
        self.overrideTimeSheetSettings = False
        self.overrideTradeSheetSettings = False
        self.overwriteIfFileExists = True
        self.param = None
        self.performanceStrategy = 'Periodic full GC to save memory'
        self.portfolioReportName = ''
        self.portfolioRowOnly = False
        self.portfolios = None
        self.preProcessXml = None
        self.printStyleSheet = 'FStandardCSS'
        self.printTemplate = 'FStandardTemplateClickable'
        self.reportName = ''
        self.secondaryFileExtension = '.xls'
        self.secondaryOutput = False
        self.secondaryTemplate = 'FTABTemplate'
        self.useUtf8ByteOrderMark = False
        self.sheetSettings = {}
        self.snapshot = True
        self.storedASQLQueries = None
        self.storedASQLQueriesInstrument = None
        self.infoManQueriesTrades = None
        self.infoManQueriesInstrument = None
        self.macros = None
        self.useMacroGUI = None
        self.template= None
        self.timeBuckets= None
        self.verticalScenario= None
        self.tradeFilters = None
        self.tradeRowsOnly = True
        self.trades = None
        self.updateInterval = 60
        self.waitForRemote = False
        self.workbook = None
        self.xmlToAmb = False
        self.xmlToFile = False
        self.zeroPositions = False
        self.guiParams = None
        self.reportApiObject = None
        self.macros = ''
        
        for arg, value in kwds.items():
            if hasattr( self, arg ):
                setattr( self, arg, value )
            else:
                logger.WLOG( 'Skipping invalid keyword argument < %s >', arg )
    
        if self.guiParams:
            self.init_from_gui_params( self.guiParams )
        
        if self.reportApiObject:
            init_from_report_api_object( self, self.reportApiObject )
    
class FWorksheetReportSerializableParameters( object ):
    """
        Copy of a gui or api report object that is seriazable
        Parameters are serilizable
    """
    
    def __init__( self, reportApiObject ):
        init_from_report_api_object( self, reportApiObject )
        self.convert_acm_to_pod()
        
        self.__hash = 0
        for attr in self.__dict__:
            value = getattr( self, attr )
            self.__hash ^= hash( str( value ) )
                
    def __cmp__(self, other):
        
        if not isinstance(other, self.__class__):
            return -1
        
        compare = None
        for attr in self.__dict__:
            value = str( getattr( self, attr ) )
            other_value = str( getattr( other, attr ) )
            compare = compare or cmp( value, other_value )
        
        return compare

    def __hash__(self):
        return self.__hash

        
    def convert_acm_to_pod( self ):
        """converts acm types to python types that can be serialized"""
        if self.workbook: 
            self.workbook = self.workbook.StringKey()
        else:
            self.workbook = None
        
        if self.template:
            self.template =  tuple( [ item.StringKey() for item in self.template ] )
        else:
            self.template = ()
        
        if self.portfolios:
            self.portfolios =  tuple( [ item.StringKey() for item in self.portfolios ] )
        else:
            self.portfolios = ()
        
        if self.tradeFilters:
            self.tradeFilters =  tuple( [ item.StringKey() for item in self.tradeFilters ] )
        else:
            self.tradeFilters = ()
        
        if self.storedASQLQueries:
            self.storedASQLQueries =  tuple( [ item.StringKey() for item in self.storedASQLQueries ] )
        else:
            self.storedASQLQueries = ()
        
        if self.storedASQLQueriesInstrument:
            self.storedASQLQueriesInstrument =  tuple( [ item.StringKey() for item in self.storedASQLQueriesInstrument ] )
        else:
            self.storedASQLQueriesInstrument = ()        

        if self.infoManQueriesTrades:
            self.infoManQueriesTrades = tuple( [ item.StringKey() for item in self.infoManQueriesTrades ] )
        else:
            self.infoManQueriesTrades = ()        
        
        if self.infoManQueriesInstrument:
            self.infoManQueriesInstrument = tuple( [ item.StringKey() for item in self.infoManQueriesInstrument ] )
        else:
            self.infoManQueriesInstrument = ()        

        if self.macros:
            self.macros = tuple( [ item.StringKey() for item in self.macros ] )
        else:
            self.macros = ()

        if self.useMacroGUI:
            self.useMacroGUI = tuple( [ item.StringKey() for item in self.useMacroGUI ] )
        else:
            self.useMacroGUI = ()
        
        if self.trades:
            self.trades =  tuple( [ item.StringKey() for item in self.trades  ] )
        else:
            self.trades = ()
        
        if self.grouping and not isinstance( self.grouping, str ):
            self.grouping = self.grouping.StringKey()
        elif self.grouping and isinstance( self.grouping, str ):
            pass
        else:
            self.grouping = 'Default'
        
        if self.filePath:
            path = str( self.filePath.SelectedDirectory() )
            self.filePath = os.path.normpath( path )
        
        if self.timeBuckets: 
            self.timeBuckets = self.timeBuckets.StringKey()
        else:
            self.timeBuckets = None
        
        self.guiParams = None
        
        
    def RunScript( self ):
        report_params = FWorksheetReportApiParameters(reportApiObject=self)
        report_params.RunScript()

def init_from_output_settings_tab( obj, variableDictionary ):
    falseTrue = ['False', 'True']

    obj.includeRawData = falseTrue.index(variableDictionary['Include Raw Data'])
    obj.includeFullData = falseTrue.index(variableDictionary['Include Full Data'])
    obj.includeFormattedData = falseTrue.index(variableDictionary['Include Formatted Data'])
    obj.includeDefaultData = falseTrue.index(variableDictionary['Include Default Data'])         
    obj.includeColorInformation = falseTrue.index(variableDictionary['Include Color Information'])
    obj.headerImage = falseTrue.index(variableDictionary['Include header image'])
    obj.headerImagePath = variableDictionary['Header image path']
    obj.htmlToFile = falseTrue.index(variableDictionary['HTML to File'])
    obj.htmlToScreen = falseTrue.index(variableDictionary['HTML to Screen'])
    obj.htmlToPrinter = falseTrue.index(variableDictionary['HTML to Printer'])
    obj.xmlToFile = falseTrue.index(variableDictionary['XML to File'])
    obj.filePath = variableDictionary['File Path']
    obj.fileName = variableDictionary['File Name']
    obj.compressXmlOutput = falseTrue.index(variableDictionary['Compress Output'])
    obj.createDirectoryWithDate = falseTrue.index(variableDictionary['Create directory with date'])
    obj.dateFormat = variableDictionary['Date format']
    obj.yearWithCentury = variableDictionary['Year with century']
    obj.fileDateFormat = variableDictionary['File date format']
    obj.fileDateBeginning = falseTrue.index(variableDictionary['File date beginning'])
    obj.overwriteIfFileExists = falseTrue.index(variableDictionary['Overwrite if file exists'])
    obj.printTemplate = variableDictionary['Print template (XSL)']
    obj.printStyleSheet = variableDictionary['Print style sheet (CSS)']
    obj.headerImage = variableDictionary['Include header image']
    obj.headerImagePath = variableDictionary['Header image path']
    obj.secondaryOutput = falseTrue.index(variableDictionary['Secondary output'])
    obj.secondaryTemplate = variableDictionary['Secondary template']
    obj.secondaryFileExtension = variableDictionary['Secondary file extension']
    obj.useUtf8ByteOrderMark = falseTrue.index(variableDictionary['Utf8 BOM'])


def init_from_advanced_settings_tab( obj, variableDictionary ):
    falseTrue = ['False', 'True']

    obj.includeDefaultData = falseTrue.index(variableDictionary['Include Default Data'])
    obj.includeFormattedData = falseTrue.index(variableDictionary['Include Formatted Data'])
    obj.includeFullData = falseTrue.index(variableDictionary['Include Full Data'])
    obj.includeRawData = falseTrue.index(variableDictionary['Include Raw Data'])
    obj.includeColorInformation = falseTrue.index(variableDictionary['Include Color Information'])
    obj.waitForRemote = falseTrue.index(variableDictionary['Wait for Remote Work'])

    obj.xmlToFile = falseTrue.index(variableDictionary['XML to File'])
    obj.compressXmlOutput = falseTrue.index(variableDictionary['Compress Output'])
    
    obj.xmlToAmb = falseTrue.index(variableDictionary['Send XML File to AMB'])
    obj.ambAddress = variableDictionary['AMB Address']
    obj.ambSender  = variableDictionary['AMB Sender Name']
    obj.ambSubject = variableDictionary['AMB Subject']
    obj.ambXmlMessage = falseTrue.index(variableDictionary['AMB XML Message'])
    obj.performanceStrategy = variableDictionary['Performance Strategy']

def init_from_processing_tab( obj, variableDictionary ):
    obj.function = variableDictionary['function']
    obj.param = variableDictionary['param']
    obj.preProcessXml = variableDictionary['preProcessXml']
            
def init_from_gui_params( obj, variableDictionary ):
    
    falseTrue = ['False', 'True']
    
    obj.workbook = variableDictionary['wbName']            
    obj.template = variableDictionary['template']
    obj.portfolios = variableDictionary['portfolios']
    obj.tradeFilters = variableDictionary['tradeFilters']
    obj.storedASQLQueries = variableDictionary['storedASQLQueries']    
    obj.storedASQLQueriesInstrument = variableDictionary['storedASQLQueriesInstrument']
    obj.infoManQueriesTrades = variableDictionary['infoManQueriesTrades']
    obj.infoManQueriesInstrument = variableDictionary['infoManQueriesInstrument']
    obj.macros = variableDictionary['macros']
    obj.useMacroGUI = variableDictionary['useMacroGUI']
    obj.grouping = variableDictionary['grouping']            
    obj.timeBuckets = variableDictionary['timeBuckets']            
    obj.verticalScenario = variableDictionary['verticalScenario']            
    obj.trades = variableDictionary['trades']

    obj.instrumentParts = falseTrue.index(variableDictionary['instrumentParts'])
    obj.expandTimebucketChildren = falseTrue.index(variableDictionary['expandTimebucketChildren'])
    obj.clearSheetContent = falseTrue.index(variableDictionary['clearSheetContent'])      
    obj.snapshot = falseTrue.index(variableDictionary['snapshot'])
    obj.multiThread = (not obj.snapshot) and falseTrue.index(variableDictionary['multiThread'])       
    if obj.snapshot:
        obj.numberOfReports = 1
    else:
        obj.numberOfReports = variableDictionary['numberOfReports']
    obj.updateInterval = variableDictionary['updateInterval']
    obj.macros = variableDictionary['macros']
    
    #Add Sheet Content tab -------------------------
    obj.tradeRowsOnly = falseTrue.index(variableDictionary['tradeRowsOnly'])
    obj.portfolioRowOnly = falseTrue.index(variableDictionary['portfolioRowOnly'])
    obj.zeroPositions = falseTrue.index(variableDictionary['zeroPositions'])      
    obj.expiredPositions = falseTrue.index(variableDictionary['expiredPositions'])      
    obj.instrumentRows = falseTrue.index(variableDictionary['instrumentRows'])      
    
    #Settings Tabs
    obj.sheetSettings = FReportSheetSettingsTab.getSelectedSheetSettings( variableDictionary.get('allSheetSettingsBySheetType' ), variableDictionary )
    obj.overridePortfolioSheetSettings = variableDictionary['FPortfolioSheet_overrideSheetSettings']
    obj.overrideTradeSheetSettings = variableDictionary['FTradeSheet_overrideSheetSettings']
    
    #Output settings tab ------------------------
    init_from_output_settings_tab( obj, variableDictionary )        
    
    #Advanced Settings tab
    init_from_advanced_settings_tab( obj, variableDictionary )
        
    #Post processing tab ------------------------    
    init_from_processing_tab( obj, variableDictionary )
    
def init_from_ext_values( obj, name ):
    """ Set attributes of this class from extension value with name ReportSettings_name,
        where each line contains attribute=value.
        The name of the extension value containing the settings can be passed as
        constructor parameter to FWorksheetReportParameters. If no name is provided
        default will be used.
    """
    ext = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', 'ReportingSettings_' + name)
    if not ext:
        logger.WLOG('Extension value ReportingSettings_' + name + ' does not exist! Using ReportingSettings_default.')
        return
    
    extList = ext.Value().split('\n')
    for el in extList:
        if el.find('=') == -1:
            break
        attr = el.split('=')[0]
        value = el.split('=')[1]                
        if value.find('[') != -1:
            #Convert str "[portfolio1, portfolio2]" to list of strings.
            value = value.replace(', ', ',')
            value = value[1:-1].split(',')                
        elif value.find(',') != -1:
            #Convert str "portfolio1, portfolio2" to list of strings.
            value = value.replace(', ', ',')
            value = value.split(',')                
        try:
            #Convert strings like "1", "True" etc to real types.
            value = eval(value)        
        except Exception as details:
            pass                    
        obj.__setattr__(attr, value)    

def init_from_report_api_object( obj, api_obj ):
    for attr, value in api_obj.__dict__.items():
        if not attr.startswith( '__' ):
            attr = attr.replace( '_FReportParametersBase__', '' )
            setattr( obj, attr, value )
