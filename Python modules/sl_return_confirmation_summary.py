"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Genrates the Return Confirmation Summary reports per 
                           Counterparty in PDF format using FXSLTemplate 
                           SL_Retun_Confirmation.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  468171

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-03-25 263474    Francois Truter    Initial Implementation
2010-04-19 300774    Francois Truter    Added funtionality to run the report 
                                        for a selection of trades. Changed
                                        Original Quantity column to Previous
                                        Quantity
2010-10-19 468171    Francois Truter    Excluded trades with Global One 
                                        timestamp
2010-11-30 508754    Francois Truter    Sorting by instrument code
2014-05-06 CHNG0001798994    Manan Ghosh    Replaced the character '/' from file name as the file name is based on 
											Counterparty name and SBL AGENCY I/DESK has the character resulting in error while creation of confirmation report.
-----------------------------------------------------------------------------"""
import acm
import sl_functions
import ArenaFunctionBridge
import FXMLReportWriter
import FReportAPI
import FRunScriptGUI
import os
import string

reportelems = '''ReturnConfirmationReport ClientDetail ReportDetail ReportElement Label Value HeaderRow DataRow Field Alignment Width'''

class LocalXMLReportWriter(FXMLReportWriter.FXMLWriter):
    def __init__(self, outputhandler, schema=None, translatedict={}):
        FXMLReportWriter.FXMLWriter.__init__(self, outputhandler, schema, translatedict)
    
    def WriteReportElement(self, label, value):
        element = self.ReportElement()
        self.Label(label).done()
        self.Value(value).done()
        element.done()
        
    def WriteField(self, value, alignment, width):
        field = self.Field(value)
        self.Value(value).done()
        if alignment:
            self.Alignment(alignment).done()
        if width:
            self.Width(width).done()
        field.done()

# Add all Report elements onto FXMLReportWriter class
for elemname in reportelems.split(" "):
    elemname = elemname.strip()
    setattr(LocalXMLReportWriter, elemname, FXMLReportWriter._ElementDescriptor(elemname))

class SecurityLoanRecord:

    @staticmethod
    def WriteXmlHeader(writer):
        headerRow = writer.HeaderRow()
        writer.WriteField('Origanal Ref', 'left', '18mm')
        writer.WriteField('Trade Ref', 'left', '18mm')
        writer.WriteField('ISIN', 'left', '30mm')
        writer.WriteField('Share Code', 'left', '20mm')
        writer.WriteField('Previous Quantity', 'right', '25mm')
        writer.WriteField('Quantity Returned', 'right', '25mm')
        writer.WriteField('Original Loan Date', 'left', '23mm')
        writer.WriteField('Settlement Date', 'left', '23mm')
        writer.WriteField('Rate', 'right', '15mm')
        writer.WriteField('Original Loan Price', 'right', '17mm')
        writer.WriteField('Loan Value', 'right', '35mm')
        writer.WriteField('VAT', 'left', '10mm')
        headerRow.done()

    @staticmethod
    def SortKey(securityLoanRecord):
        return securityLoanRecord._sortKey()
    
    def __init__(self, trade):
        trade_id = str(trade.Oid())
        self.trade = trade
        self.instrument = trade.Instrument()
        self.underlying = self.instrument.Underlying()
        self.originalTrade = trade.Contract()
        self.originalInstrument = self.originalTrade.Instrument()
        self.replacementTrade = None
        if trade.ConnectedTrdnbr() != trade.Oid() and trade.ConnectedTrdnbr() != self.originalTrade.Oid():
            self.replacementTrade = trade.ConnectedTrade()
        
        self.price = None
        self.quantity = None
        self.previousQuantity = None
        self.originalPrice = None
        self.originalQuantity = None
        
    def _sortKey(self):
        return (self._securityCode(), self.originalTrade.Oid(), self.trade.Oid())
        
    def _substringAfterLast(self, string, char):
        array = string.split(char)
        length = len(array)
        if length > 0:
            return array[length - 1]
        else:
            return ''
    
    def _securityCode(self):
        return self._substringAfterLast(self.underlying.Name(), '/')
        
    def _quantity(self):
        if self.quantity == None:
            self.quantity = sl_functions.underlying_quantity(self.trade.Quantity(), self.instrument)
            if self.replacementTrade:
                self.quantity = self.quantity - sl_functions.underlying_quantity(self.replacementTrade.Quantity(), self.replacementTrade.Instrument())
        
        return self.quantity
        
    def _previousQuantity(self):
        if self.previousQuantity == None:
            self.previousQuantity = sl_functions.underlying_quantity(self.trade.Quantity(), self.instrument)
            
        return self.previousQuantity
        
    def _price(self):
        if self.price == None:
            quotation = self.underlying.Quotation()
            self.price = ArenaFunctionBridge.instrument_used_price(self.underlying.Oid(), acm.Time.DateNow(), self.instrument.Currency().Oid()) * quotation.QuotationFactor()
        
        return self.price
        
    def _marketValue(self):
        return self._quantity() * self._price()
        
    def _originalQuantity(self):
        if self.originalQuantity == None:
            self.originalQuantity = sl_functions.underlying_quantity(self.originalTrade.Quantity(), self.originalInstrument)
        
        return self.originalQuantity
        
    def _originalPrice(self):
        if self.originalPrice == None:
            quotation = self.underlying.Quotation()
            self.originalPrice = self.originalTrade.RefPrice() * ArenaFunctionBridge.fx_rate(self.underlying.Currency().Oid(), self.originalInstrument.Currency().Oid(), self.trade.TradeTime()) * quotation.QuotationFactor()
            
        return self.originalPrice
    
    def _originalValue(self):
        return self._originalQuantity() * self._originalPrice()
        
    def _fee(self):
        leg = self.instrument.Legs()[0]
        if leg:
            return leg.FixedRate()
        else:
            return 'Not Available'
            
    def _originalStartDate(self):
        leg = self.originalInstrument.Legs()[0]
        if leg:
            return leg.StartDate()
        else:
            return 'Not Available'
        
    def _vat(self):
        if self.instrument.AdditionalInfo().SL_VAT():
            return 'Yes'
        else:
            return 'No'
        
    def WriteXmlData(self, writer):
        numFormatter = acm.FNumFormatter('numFormatter')
        dateFormatter = acm.FDateFormatter('dateFormatter')
        dateFormatter.FormatDefinition('%Y/%m/%d')

        dataRow = writer.DataRow()
        writer.WriteField(self.originalTrade.Oid(), 'left', None)
        writer.WriteField(self.trade.Oid(), 'left', None)
        writer.WriteField(self.underlying.Isin(), 'left', None)
        writer.WriteField(self._securityCode(), 'left', None)
        writer.WriteField(numFormatter.Format(self._previousQuantity()), 'right', None)
        writer.WriteField(numFormatter.Format(self._quantity()), 'right', None)
        writer.WriteField(dateFormatter.Format(self._originalStartDate()), 'left', None)
        writer.WriteField(dateFormatter.Format(self.instrument.ExpiryDate()), 'reft', None)
        writer.WriteField(self._fee(), 'right', None)
        writer.WriteField(numFormatter.Format(self._originalPrice()), 'right', None)
        writer.WriteField(numFormatter.Format(self._originalValue()), 'right', None)
        writer.WriteField(self._vat(), 'reft', None)
        dataRow.done()
            
class ReturnConfirmationSummaryReport:

    def __init__(self, counterparty, trades):
        self.counterparty = counterparty
        self.securityLoanRecords = []
        for trade in trades:
            self.securityLoanRecords.append(SecurityLoanRecord(trade))
            
    def _writeClientDetail(self, writer):
        '''Address and contact details temporarily left out, until counterparty 
        details have been updated on the system'''
        name = self.counterparty.Name()
        '''address1 = self.counterparty.Address()
        address2 = self.counterparty.Address2()
        city = self.counterparty.City()
        country = self.counterparty.Country()
        zip = self.counterparty.ZipCode()
        contact = self.counterparty.Attention()
        telephone = self.counterparty.Telephone()'''
        
        clientDetail = writer.ClientDetail()
        writer.WriteReportElement("To:", name)
        '''writer.WriteReportElement("Address:", address1)
        if address2 and address2 != "" and address2 != address1 and address2 != city and address2 != country:
            writer.WriteReportElement("", address2)
        if city and city != "":
            writer.WriteReportElement("", city)
        if country and country != "":
            writer.WriteReportElement("", country)
        writer.WriteReportElement("", zip)
        writer.WriteReportElement("Contact", contact)
        writer.WriteReportElement("Telephone", telephone)'''
        clientDetail.done()

    def _reportXML(self):
        numFormatter = acm.FNumFormatter('numFormatter')
        dateFormatter = acm.FDateFormatter('dateFormatter')
        dateFormatter.FormatDefinition('%Y/%m/%d')

        writer, strbuf = LocalXMLReportWriter.make_iostring_writer()
        writer.ReturnConfirmationReport()
        self._writeClientDetail(writer)
        reportDetail = writer.ReportDetail()
        SecurityLoanRecord.WriteXmlHeader(writer)
        self.securityLoanRecords.sort(key=SecurityLoanRecord.SortKey)
        for record in self.securityLoanRecords:
            record.WriteXmlData(writer)
        reportDetail.done()
        writer.done()
        
        return strbuf.getvalue()
        
    def _setReportAPIParameters(self, report, filepath, filename, xslPdfTemplate):
        report.ambAddress = ''
        report.ambSender = ''
        report.ambSubject = ''
        report.ambXmlMessage = False
        report.clearSheetContent = False
        report.compressXmlOutput = False
        report.createDirectoryWithDate = False
        report.dateFormat = '%d%m%y'
        report.expiredPositions = False
        report.fileDateFormat = ''
        report.fileDateBeginning = False
        report.fileName = filename
        report.filePath = filepath
        report.function = None
        report.gcInterval = 5000
        report.gridOutput = False
        report.gridUseLoopbackGridClient = False
        report.gridRowPartitionCbArg = None
        report.gridRowPartitionCbClass = None
        report.gridExcludeRowCbClass = "FReportGridCallbacks.ExcludeRowManager"
        report.gridAggregateXmlCbClass = None
        report.gridTimeout = None
        report.gridRowSet = None
        report.grouping = 'Default'
        report.htmlToFile = False
        report.htmlToPrinter = False
        report.htmlToScreen = False
        report.includeDefaultData = False
        report.includeFormattedData = False
        report.includeFullData = False
        report.includeRawData = False
        report.instrumentParts = False
        report.instrumentRows = False
        report.maxNrOfFilesInDir = 1000
        report.multiThread = False
        report.numberOfReports = 1
        report.orders = None
        report.overridePortfolioSheetSettings = False
        report.overrideTimeSheetSettings = False
        report.overrideTradeSheetSettings = False
        report.overwriteIfFileExists = True
        report.param = None
        report.performanceStrategy = 'Periodic full GC to save memory'
        report.portfolioReportName = ''
        report.portfolioRowOnly = False
        report.portfolios = None
        report.preProcessXml = None
        report.printStyleSheet = 'FStandardCSS'
        report.printTemplate = 'FStandardTemplateClickable'
        report.reportName = ''
        report.secondaryFileExtension = '.pdf'
        report.secondaryOutput = True
        report.secondaryTemplate = xslPdfTemplate
        report.sheetSettings = {}
        report.snapshot = True
        report.storedASQLQueries = None
        report.template= None
        report.tradeFilters = None
        report.tradeRowsOnly = False
        report.trades = None
        report.updateInterval = 60
        report.workbook = None
        report.xmlToAmb = False
        report.xmlToFile = False
        report.zeroPositions = False
        report.guiParams = None
        report.reportApiObject = None
    
    def CreateReport(self, filepath, filename, xslPdfTemplate):
        report = FReportAPI.FWorksheetReportApiParameters()
        self._setReportAPIParameters(report, filepath, filename, xslPdfTemplate)
        report.CreateReportByXml(self._reportXML())
        try:
            foFilepath = os.path.join(filepath, filename + '.fo')
            if os.path.exists(foFilepath):
                os.remove(foFilepath)
        except Exception, ex:
            acm.Log('An exceptio occurred while trying to remove the fo file: ' + str(ex))
    
def _createCouterpartyDictionary(trades, excludeGlobalOneStampedTrades):
    dictionary = {}
    for trade in trades:
        if excludeGlobalOneStampedTrades and trade.SLGlobalOneTimeStampExists():
            continue
        counterparty = trade.Counterparty()
        if counterparty in dictionary:
            dictionary[counterparty].append(trade)
        else:
            dictionary[counterparty] = [trade]
            
    return dictionary
    
def _getUniqueFilename(filepath, filename):
    counter = 1
    newFilename = filename
    fullFilepath = os.path.join(filepath, newFilename + '.pdf')
    while os.path.exists(fullFilepath):
        newFilename = filename + '_' + str(counter)
        fullFilepath = os.path.join(filepath, newFilename + '.pdf')
        counter += 1
        
    return newFilename
    
def _getFileName(filepath, counterparty, startDate, endDate):
    filename = string.replace(counterparty.Name(), ' ', '_')
    if startDate and endDate:
        startDateparts = acm.Time().DateToYMD(startDate)
        endDateparts = acm.Time().DateToYMD(endDate)
        filename =  '%(filename)s_%(startYear)04i%(startMonth)02i%(startDay)02i_%(endYear)04i%(endMonth)02i%(endDay)02i' % \
            {'filename': filename, 'startYear': startDateparts[0], 'startMonth': startDateparts[1], 'startDay': startDateparts[2], 'endYear': endDateparts[0], 'endMonth': endDateparts[1], 'endDay': endDateparts[2]}

    return _getUniqueFilename(filepath, filename)
    
def WriteConfirmationSummary(outputDirectory, trades, excludeGlobalOneStampedTrades, includeDates, startDate, endDate):
    if not trades:
        acm.Log('No trades to process')
    else:
        counterpartyDictionary = _createCouterpartyDictionary(trades, excludeGlobalOneStampedTrades)
        for counterparty in counterpartyDictionary.keys():
            filename = ''
            if includeDates:
                filename = _getFileName(outputDirectory, counterparty, startDate, endDate)
            else:
                filename = _getFileName(outputDirectory, counterparty, None, None)
                
            filename = string.replace(filename, '/', '_')
                
            report = ReturnConfirmationSummaryReport(counterparty, counterpartyDictionary[counterparty])
            report.CreateReport(outputDirectory, filename, xslPdfTemplate)
    
outputDirectoryKey = 'OutputDirectokry'
startDateKey = 'StartDate'
endDateKey = 'EndDate'
portfolioKey = 'Portfolio'
counterpartyKey = 'Counterparty'
tradeKey = 'Trades'

xslPdfTemplate = 'SL_Return_Confirmation_Summary'
today = acm.Time().DateNow()
directorySelection=FRunScriptGUI.DirectorySelection()
ael_gui_parameters = {'windowCaption':'Security Lending: Return Confirmation Report'}
#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
                    [outputDirectoryKey, 'Output Directory', directorySelection, None, directorySelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
                    [portfolioKey, 'Portfolio', 'FPhysicalPortfolio', None, None, 0, 1, 'The porfolio which returns will be processed.', None, 1],
                    [counterpartyKey, 'Counterparty', 'FParty', None, None, 0, 1, 'The counterparty for which returns will be processed', None, 1],
                    [startDateKey, 'Start Date', 'date', None, today, 1, 0, 'The date from which returns will be processed.', None, 1],
                    [endDateKey, 'End Date', 'date', None, today, 1, 0, 'The date until which returns will be processed.', None, 1],
                    [tradeKey, 'Trades', 'FTrade', None, None, 0, 1, 'To run for specific trades, enter the trade numbers here.', None, 1]
                ]

def ael_main(parameters):

    outputDirectory = parameters[outputDirectoryKey]
    portfolios = parameters[portfolioKey]
    counterparties = parameters[counterpartyKey]
    startDate = parameters[startDateKey]
    endDate = parameters[endDateKey]
    selectedTrades = parameters[tradeKey]
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    
    if selectedTrades:
        op = query.AddOpNode('OR')
        for trade in selectedTrades:
            op.AddAttrNode('Oid', 'EQUAL', trade.Oid())
    else:
        if len(portfolios) > 0:
            op = query.AddOpNode('OR')
            for portfolio in portfolios:
                op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
                
        if len(counterparties) > 0:
            op = query.AddOpNode('OR')
            for counterparty in counterparties:
                op.AddAttrNode('Counterparty.Name', 'EQUAL', counterparty.Name())
                
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'SecurityLoan'))
            
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.OpenEnd', 'EQUAL', acm.EnumFromString('OpenEndStatus', 'Terminated'))
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.AdditionalInfo.SL_SweepingBatchNo', 'EQUAL', 0)
            
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', str(startDate))
            
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.ExpiryDate', 'LESS_EQUAL', str(endDate))

    
    trades = query.Select()
    excludeGlobalOneStampedTrades = True
    WriteConfirmationSummary(outputDirectory.SelectedDirectory().Text(), trades, excludeGlobalOneStampedTrades, not selectedTrades, startDate, endDate)
