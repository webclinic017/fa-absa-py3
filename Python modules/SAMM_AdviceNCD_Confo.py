"""-----------------------------------------------------------------------------
PROJECT                 :  ABITFA-569
PURPOSE                 :  Decommission platypus and move all existing reports using it to FOP
DEPATMENT AND DESK      :  OPS
REQUESTER               :  Aaeda Salejee
DEVELOPER               :  Ickin Vural
CR NUMBER               :  C000000697493

HISTORY
================================================================================
Date            Change no       Developer           Description
--------------------------------------------------------------------------------
XXXXXX          C000000697493   Ickin Vural         Initial implementation
2016-12-07      CHNG0004172138  Gabriel Marko       Modified according to ABITFA-4072
2017-09-04                      Willie vd Bank      Updated CashFlowBase input parameters and
                                                    replaced SimpleProjectedCashFlow with CashFlowBase
                                                    according to 2017 upgrade requirements
2018-08-02      CHG1000757460   Stuart Wilson       Incorporating new 2018 logo file path to xml template  
"""
from pyPdf import (
    PdfFileWriter,
    PdfFileReader
)
from zak_funcs import formnum
from at_time import acm_date
import FReportAPI
import FXMLReportWriter
import acm
import ael
import glob
import os
import FReportSettings as frs

tradelist = []

REPORTELEMS = [
    "ReturnConfirmationReport",
    "XMLResources",
    "ClientDetail",
    "ReportDetail",
    "HeadingDetail",
    "FooterDetail",
    "ReportElement",
    "Label",
    "Value"
]


class LocalXMLReportWriter(FXMLReportWriter.FXMLWriter):
    def __init__(self, outputhandler, schema=None, translatedict={}):
        FXMLReportWriter.FXMLWriter.__init__(
            self,
            outputhandler,
            schema,
            translatedict
        )

    def WriteReportElement(self, label, value):
        element = self.ReportElement()
        self.Label(label).done()
        self.Value(value).done()
        element.done()


# Add all Report elements onto FXMLReportWriter class
for elemname in REPORTELEMS:
    setattr(
        LocalXMLReportWriter,
        elemname,
        FXMLReportWriter._ElementDescriptor(elemname)
    )


def get_interest_amount(trade):
    if not trade:
        raise ValueError("Missing trade.")

    ins = trade.Instrument()
    quantity = trade.Quantity() or 0.0
    value_day = acm_date(trade.ValueDay())
    cashflowAmount = 0.0
    roundingSpec = ins.RoundingSpecification()

    legs = ins.Legs()
    if len(legs) == 1:
        leg = legs[0]
        staticLegInfo = leg.StaticLegInformation(ins, trade.ValueDay(), None)
        legInfo = leg.LegInformation(trade.ValueDay())
        for cf in leg.CashFlows():
            if value_day >= cf.StartDate() and value_day < cf.EndDate() :
                cfInfo = cf.CashFlowInformation(staticLegInfo)
                cashflowAmount = cfInfo.Rate(legInfo) * cfInfo.CashFlowBase(legInfo, trade.ValueDay(), True).Number()
    cashflowAmount *= quantity

    return cashflowAmount


class ReturnConfirmationReport:
    def __init__(self, trade, Date):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.Date = Date
        self.t = ael.Trade[trade.Oid()]

    def _substringAfterLast(self, string, char):
        array = string.split(char)
        length = len(array)
        return array[length - 1] if length > 0 else ''

    def _purchaseSale(self):
        return 'PURCHASE' if self.trade.Quantity() > 0 else 'SOLD'

    def _fromTo(self):
        return 'from' if self.trade.Quantity() > 0 else 'to'

    def _productName(self):
        ProductName    = ''
        ProductName =  self.trade.AdditionalInfo().MM_Instype()
        if self.trade.Instrument().InsType() == 'CD':
            ProductName = 'CD'
        return ProductName

    def _tenor(self):
        return self.t.value_day.days_between(self.t.insaddr.exp_day, 'Act/365') or 0.0

    def _discountAmount(self):
        DiscountAmount = 0.0
        ais = self.trade.AdditionalInfo()
        if ais.MM_Instype() == 'NCD':
            if ais.MM_Original_Nominal() != None:
                DiscountAmount = float(ais.MM_Original_Nominal()) + self.trade.Premium()
        else:
            DiscountAmount = (self.trade.Instrument().ContractSize() * self.trade.Quantity()) + self.trade.Premium()
        return DiscountAmount

    def _nominal(self):
        return self.trade.Nominal()

    def _matVal(self):
        return self.trade.Nominal() + get_interest_amount(self.trade)

    def _conAmt(self):
        ConsiderationAmount = 0.0
        ConsiderationAmount = self.trade.Premium() + self.trade.Fee()
        return ConsiderationAmount

    def _issuer(self):
        try:
            return self.trade.Instrument().Issuer().Name()
        except:
            return ''
        
        
    def _reportXML(self):
        
        
            
        numFormatter = acm.FNumFormatter('numFormatter')
        percFormatter = acm.FNumFormatter('percFormatter')
        percFormatter.NumDecimals(0)
        percFormatter.ScaleFactor(100)
        dateFormatter = acm.FDateFormatter('dateFormatter')
        dateFormatter.FormatDefinition('%Y/%m/%d')
        writer, strbuf = LocalXMLReportWriter.make_iostring_writer()
        writer.ReturnConfirmationReport()
        
        XMLResources = writer.XMLResources()
        writer.WriteReportElement("img-absa-logo", os.path.join(frs.LOGOS_PATH, 'absa_logo_2018.png') )
        XMLResources.done()
        
        clientDetail = writer.ClientDetail()

        instrument = self.trade.Instrument()
        counterparty = self.trade.Counterparty()
        writer.WriteReportElement("", counterparty.Fullname())
        writer.WriteReportElement("", counterparty.Address())
        writer.WriteReportElement("", counterparty.Address2())
        writer.WriteReportElement("", counterparty.City())
        writer.WriteReportElement("", counterparty.Country())
        writer.WriteReportElement("", counterparty.ZipCode())
        writer.WriteReportElement("", counterparty.Telephone())

        clientDetail.done()

        HeadingDetail = writer.HeadingDetail()

        writer.WriteReportElement("MONEY MARKET ADVICE NOTE", "")
        writer.WriteReportElement(
            "We confirm having %s the following Money Market Instrument %s you." % (
                self._purchaseSale(),
                self._fromTo(),
            ),
            ""
        )

        HeadingDetail.done()

        reportDetail = writer.ReportDetail()

        writer.WriteReportElement(self._productName(), instrument.Name())
        writer.WriteReportElement("REFERENCE NUMBER", self.trade.Name())
        writer.WriteReportElement("COUNTERPARTY CODE", counterparty.Name())
        writer.WriteReportElement("ISSUED BY", self._issuer())
        writer.WriteReportElement("VALUE DATE", self.trade.ValueDay())
        writer.WriteReportElement("MATURITY DATE", instrument.ExpiryDateOnly())
        writer.WriteReportElement("DAYS TO MATURITY", self._tenor())
        writer.WriteReportElement(
            {"FRN": "PRICE",
             "Bill": "DISCOUNT RATE"}.get(instrument.InsType(), "YIELD RATE"),
            "%s%%" % round(self.trade.Price(), 7)
        )
        writer.WriteReportElement("NOMINAL AMOUNT", formnum(self._nominal()))
        if instrument.InsType() != "FRN":
            writer.WriteReportElement("MATURITY VALUE", formnum(self._matVal()))
        writer.WriteReportElement("CONSIDERATION AMOUNT", formnum(self._conAmt()))
        writer.WriteReportElement("BROKERS COMMISSION", str(self.trade.Fee()))
        writer.WriteReportElement("PROFIT CENTRE", self.trade.Portfolio().Name())
        writer.WriteReportElement("ENQUIRIES", "(011) 895 6745/6750")

        reportDetail.done()

        FooterDetail = writer.FooterDetail()

        writer.WriteReportElement("THIS IS A COMPUTER-GENERATED DOCUMENT AND DOES NOT REQUIRE ANY SIGNATURES.", "")
        writer.WriteReportElement("Retain this confirmation for Tax purposes.", "")

        FooterDetail.done()
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
        report.includeRawData = True
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


    def CreateReport(self, filepath, filename, trd, xslPdfTemplate):
        trade = acm.FTrade[int(trd)]

        rootdirectory = str(filepath) + ael.date_today().to_string('%Y%m%d') + '/'
        directory =  rootdirectory + str(tradelist[0]) + '/'

        if os.path.exists(rootdirectory):
            filepath = rootdirectory
        else:
            os.mkdir(rootdirectory)
            filepath = rootdirectory

        if os.path.exists(directory):
            filepath = directory
        else:
            os.mkdir(directory)
            filepath = directory

        report = FReportAPI.FWorksheetReportApiParameters()
        self._setReportAPIParameters(report, filepath, filename, xslPdfTemplate)
        report.CreateReportByXml(self._reportXML())

        try:
            foFilepath = os.path.join(filepath, filename  + '.fo')
            if os.path.exists(foFilepath):
                os.remove(foFilepath)
        except Exception, ex:
            acm.Log('An exception occurred while trying to remove the fo file: ' + str(ex))



xslPdfTemplate = 'SAMM_AdviceNCD_Confo'
today = acm.Time().DateNow()
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory('Y:/Jhb/Markets and Treasury/Money Market Ops/MM Confirmations/')
ael_gui_parameters = {'windowCaption':'NCD Confirmation'}


def getCounterparty():
    return sorted(t.ptyid for t in ael.Party.select() if t.type in ('Counterparty', 'Broker', 'Client'))


def Filter():
    return sorted(f.fltid for f in ael.TradeFilter)


def ASQL(*rest):
    acm.RunModuleWithParameters('SAMM_AdviceNCD_Confo', 'Standard' )
    return 'SUCCESS'


def trade_report(trdnbr, date_string, output_directory, xsl_pdf_template='SAMM_AdviceNCD_Confo'):
    global tradelist

    trade = acm.FTrade[int(trdnbr)]
    dt = ael.date_from_string(date_string)

    if trade.Oid() not in tradelist:
        tradelist.append(trade.Oid())

    if trade.Instrument().InsType() not in ('FRN', 'CD', 'Bill', 'Deposit'):
        acm.Log('Please check if trade is valid!')
        return

    filename = "_".join([
        trade.Counterparty().Fullname().replace('/', ''),
        ' (%s) ' % trade.Oid(),
        dt.to_string('%d %b %Y'),
        trade.Instrument().InsType()
    ])

    report = ReturnConfirmationReport(trade, date_string)
    report.CreateReport(
        output_directory,
        filename,
        str(trade.Oid()),
        xsl_pdf_template
    )

    acm.Log('Generating Report')

    return filename


ael_variables = [
    ['OutputDirectory', 'Output Directory', directorySelection, None, directorySelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
    ['Counterparty', 'Counterparty', 'string', getCounterparty(), 'ALL', 0, 0, 'To run for a Counterparty', None, 1],
    ['TradeFilter', 'Trade Filter', 'string', Filter(), 'ALL', 0, 0, 'To run for a Trade Filter', None, 1],
    ['TradeNumber', 'Trade Number', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
    ['Date', 'Date', 'string', today, today, 1]
]


def ael_main(parameters):

    outputDirectory = parameters['OutputDirectory']
    Counterparty = parameters['Counterparty']
    TradeFilter = parameters['TradeFilter']
    tradeNumber = parameters['TradeNumber']
    Date = parameters['Date']
    trdlst = []

    if tradeNumber not in (None, '') and Counterparty == 'ALL' and TradeFilter == 'ALL':
        trdlst = str(tradeNumber).split(',')
        if not trdlst:
            acm.Log('No trades to process.')

    if Counterparty not in (None, '', 'ALL'):
        try:
            p = ael.Party[Counterparty]
            trd = ael.Trade.select('counterparty_ptynbr = %d' %(p.ptynbr))
            trdlst.extend([t.trdnbr for t in trd])
        except:
            acm.Log('Invalid Counterparty!')

    if TradeFilter not in (None, '', 'ALL'):
        try:
            tf = ael.TradeFilter[TradeFilter]
            trdlst.extend([t.trdnbr for t in tf.trades()])
        except:
            acm.Log('Invalid Filter!')

    # Use the report file name of the last valid trade report as output file name
    filename = ""
    for trdnbr in trdlst:
        filename = trade_report(trdnbr, Date, outputDirectory) or filename

    outputFileName = str(outputDirectory) + ael.date_today().to_string('%Y%m%d') +  '/' + filename + ".pdf"
    inputFileNames = glob.glob(str(outputDirectory) +  ael.date_today().to_string('%Y%m%d') + '/' + str(tradelist[0]) + '/' +  "*.pdf")

    output = PdfFileWriter()
    for pdfFileName in inputFileNames:
        output.addPage(PdfFileReader(file(pdfFileName, "rb")).getPage(0)) # adds the first page of each document

    outputStream = file(outputFileName, "wb")
    output.write(outputStream)
    outputStream.close()
    os.startfile(outputFileName)
    del tradelist[:]
