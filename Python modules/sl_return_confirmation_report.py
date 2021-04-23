"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Genrates the Return Confirmation reports in PDF 
                           format using FXSLTemplate SL_Retun_Confirmation.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  326240

HISTORY
================================================================================
DATE            DEVELOPER               DESCRIPTION
----------      ----------------------  ----------------------------------------
2010-01-12      Francois Truter         Initial Implementation
2010-06-03      Francois Truter         Removed Security Name field
                                        Renamed Settle Date - Return Settle Date
                                        Renamed Trade Date - Original Loan Date
                                        Changed Dividend Factor to display as %
                                        Replaced Price with Original Loan Price

-----------------------------------------------------------------------------"""
import acm
import sl_functions
import ArenaFunctionBridge
import FXMLReportWriter
import FReportAPI
import FRunScriptGUI
import os

reportelems = '''ReturnConfirmationReport ClientDetail ReportDetail ReportElement Label Value'''

class LocalXMLReportWriter(FXMLReportWriter.FXMLWriter):
    def __init__(self, outputhandler, schema=None, translatedict={}):
        FXMLReportWriter.FXMLWriter.__init__(self, outputhandler, schema, translatedict)
    
    def WriteReportElement(self, label, value):
        element = self.ReportElement()
        self.Label(label).done()
        self.Value(value).done()
        element.done()

# Add all Report elements onto FXMLReportWriter class
for elemname in reportelems.split(" "):
    elemname = elemname.strip()
    setattr(LocalXMLReportWriter, elemname, FXMLReportWriter._ElementDescriptor(elemname))

class ReturnConfirmationReport:
    
    def __init__(self, trade):
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
        self.originalPrice = None
        self.originalQuantity = None
        
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
        
    def _reportXML(self):
        numFormatter = acm.FNumFormatter('numFormatter')
        percFormatter = acm.FNumFormatter('percFormatter')
        percFormatter.NumDecimals(0)
        percFormatter.ScaleFactor(100)
        dateFormatter = acm.FDateFormatter('dateFormatter')
        dateFormatter.FormatDefinition('%Y/%m/%d')

        writer, strbuf = LocalXMLReportWriter.make_iostring_writer()
        writer.ReturnConfirmationReport()
        clientDetail = writer.ClientDetail()
        writer.WriteReportElement("Client", self.trade.CounterpartyId())
        clientDetail.done()
        reportDetail = writer.ReportDetail()
        writer.WriteReportElement("Original Contract Reference", self.originalTrade.Oid())
        writer.WriteReportElement("Trade Reference", self.trade.Oid())
        writer.WriteReportElement("Original Loan Date", dateFormatter.Format(self.originalInstrument.StartDate()))
        writer.WriteReportElement("Return Settle Date", dateFormatter.Format(self.instrument.ExpiryDate()))
        writer.WriteReportElement("Security", self._securityCode())
        writer.WriteReportElement("ISIN Code", self.underlying.Isin())
        writer.WriteReportElement("Currency", self.instrument.Currency().Name())            
        writer.WriteReportElement("Quantity Returned", numFormatter.Format(self._quantity()))
        writer.WriteReportElement("Original Quantity", numFormatter.Format(self._originalQuantity()))
        writer.WriteReportElement("Original Loan Price", numFormatter.Format(self._originalPrice()))
        writer.WriteReportElement("Original Value", numFormatter.Format(self._originalValue()))
        writer.WriteReportElement("Description", 'Return')
        writer.WriteReportElement("Market Value", numFormatter.Format(self._marketValue()))
        writer.WriteReportElement("Fee Type", "% of market")
        writer.WriteReportElement("Fee % (Incl. VAT)", self.instrument.Legs()[0].FixedRate())
        
        minimumFee = self.instrument.AdditionalInfo().SL_Minimum_Fee()
        if minimumFee == None:
            writer.WriteReportElement("Minimum Fee", "")
        else:
            writer.WriteReportElement("Minimum Fee", numFormatter.Format(minimumFee))
        
        dividendFactor = self.instrument.AdditionalInfo().SL_Dividend_Factor()
        if dividendFactor == None:
            writer.WriteReportElement("Dividend Factor", "")
        else:
            writer.WriteReportElement("Dividend Factor", percFormatter.Format(dividendFactor))
            
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
            foFilepath = os.path.join(filepath.SelectedDirectory().Text(), filename + '.fo')
            if os.path.exists(foFilepath):
                os.remove(foFilepath)
        except Exception as ex:
            acm.Log('An exceptio occurred while trying to remove the fo file: ' + str(ex))
 
outputDirectoryKey = 'OutputDirectokry'
startDateKey = 'StartDate'
endDateKey = 'EndDate'
portfolioKey = 'Portfolio'
tradeNumberKey = 'TradeNumber'

xslPdfTemplate = 'SL_Return_Confirmation_Report'
today = acm.Time().DateNow()
directorySelection=FRunScriptGUI.DirectorySelection()
ael_gui_parameters = {'windowCaption':'Security Lending: Return Confirmation Report (Per Trade)'}
#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
                    [outputDirectoryKey, 'Output Directory', directorySelection, None, directorySelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
                    [portfolioKey, 'Portfolio', 'FPhysicalPortfolio', None, None, 0, 1, 'The porfolio which returns will be processed.', None, 1],
                    [startDateKey, 'Start Date', 'date', None, today, 1, 0, 'The date from which returns will be processed.', None, 1],
                    [endDateKey, 'End Date', 'date', None, today, 1, 0, 'The date until which returns will be processed.', None, 1],
                    [tradeNumberKey, 'Trade Number', 'int', None, None, 0, 0, 'To run for a soecific trade, enter the trade number here.', None, 1]
                ]

def ael_main(parameters):

    outputDirectory = parameters[outputDirectoryKey]
    portfolios = parameters[portfolioKey]
    startDate = parameters[startDateKey]
    endDate = parameters[endDateKey]
    tradeNumber = parameters[tradeNumberKey]
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    
    if tradeNumber != None and tradeNumber != '':
        op = query.AddOpNode('AND')
        op.AddAttrNode('Oid', 'EQUAL', tradeNumber)
    else:
        if len(portfolios) > 0:
            op = query.AddOpNode('OR')
            for portfolio in portfolios:
                op.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
            
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'SecurityLoan'))
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.OpenEnd', 'EQUAL', acm.EnumFromString('OpenEndStatus', 'Terminated'))
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', str(startDate))
        
        op = query.AddOpNode('AND')
        op.AddAttrNode('Instrument.ExpiryDate', 'LESS_EQUAL', str(endDate))

    
    trades = query.Select()
    if not trades:
        acm.Log('No trades to process')
    else:
        for trade in trades:
            report = ReturnConfirmationReport(trade)
            report.CreateReport(outputDirectory, str(trade.Oid()), xslPdfTemplate)
