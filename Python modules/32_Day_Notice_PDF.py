"""-----------------------------------------------------------------------------
PROJECT                 :  32-Day Deposit Notice Confirmation
PURPOSE                 :  To generate the 32-Day Deposit Notice Confirmation
                            Add terms and conditons to the end of the confirmation and chnage the confirmation so haeader and footer details are not hardcoded in the template
                           
DEPATMENT AND DESK      :  OPS, OPS
REQUESTER               :  Miguel Da Silva, Shauleen van der Byl 
DEVELOPER               :  Tshepo Mabena, Jaysen Naicker
CR NUMBER               :  835702, CHNG0000252776

-----------------------------------------------------------------------------"""


from pyPdf import PdfFileWriter, PdfFileReader
import glob

import acm, ael, time
import sl_functions
import ArenaFunctionBridge
import FXMLReportWriter
import FReportAPI
import FRunScriptGUI
import os
import datetime
import string
from zak_funcs import formnum

imagepath = 'Y:/Jhb/Arena/Prime/FOP/images/'
replist = []

reportelems = '''ReturnConfirmationReport ConfirmationReport ClientDetail Notice ConfirmationHead ReportDetail FooterDetail HeadingDetail Computer FooterDetail ReportElement Label Value Date'''

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

def AccType(t):

    return '32 Days Notice Call Deposit'
    
def AccNumber(t):

    return str(t.insaddr.insid)
    
def TransactionNo(t):

    TransNo = ''    
    l         = t.insaddr.legs()[0]
    cashflows = l.cash_flows()
            
    for cf in cashflows:
        
        if cf.pay_day == l.start_day:
            TransNo = cf.cfwnbr
        
    return str(TransNo)
    
def DepositDate(t):
        
    l           = t.insaddr.legs()[0]
    DepositDate = l.start_day
            
    return DepositDate

def InitialDeposit(t):
    
    l         = t.insaddr.legs()[0]
    cashflows = l.cash_flows()
            
    for cf in cashflows:
        
        if cf.pay_day == l.start_day:
            Initial_dep = cf.nominal_amount()
    
    return formnum(Initial_dep)

        
def reportXML(reportList):
    numFormatter = acm.FNumFormatter('numFormatter')
    percFormatter = acm.FNumFormatter('percFormatter')
    percFormatter.NumDecimals(0)
    percFormatter.ScaleFactor(100)
    dateFormatter = acm.FDateFormatter('dateFormatter')
    dateFormatter.FormatDefinition('%Y/%m/%d')

    writer, strbuf = LocalXMLReportWriter.make_iostring_writer()
    writer.ReturnConfirmationReport()
    
    for trdno in reportList:
        trade = acm.FTrade[trdno]
        t = ael.Trade[int(trdno)]
        confirmationReport = writer.ConfirmationReport()
        
        ConfirmationHead = writer.ConfirmationHead()
        writer.WriteReportElement("CONFIRMATION", "")
        ConfirmationHead.done()
        
        HeadingDetail = writer.HeadingDetail()
        writer.WriteReportElement("ABSA CAPITAL 32 DAYS NOTICE CALL DEPOSIT", "")
        HeadingDetail.done()
        
        clientDetail = writer.ClientDetail()
        writer.WriteReportElement("TO:", trade.Counterparty().Fullname())
        writer.WriteReportElement("FAX:", trade.Counterparty().Telephone())
        writer.WriteReportElement("FROM:", "ABSA BANK LIMITED") 
        writer.WriteReportElement("DATE:", DepositDate(t).to_string("%d %B %Y"))  
        clientDetail.done()
       
        Notice = writer.Notice()    
        writer.WriteReportElement("Confirmation in terms of Absa Capital 32 Days Notice Call Deposit - Standard Terms and Conditions dated " + DepositDate(t).to_string("%d %B %Y") + ":", "")
        Notice.done()
        
        reportDetail = writer.ReportDetail()
        writer.WriteReportElement("The following transaction was applied to your account:", "")
        writer.WriteReportElement("1. ACCOUNT TYPE:", '32 Days Notice Call Deposit')
        writer.WriteReportElement("2. ACCOUNT NUMBER:", AccNumber(t))
        writer.WriteReportElement("3. TRADE NUMBER:", trade.Name())
        writer.WriteReportElement("4. TRANSACTION NUMBER:", TransactionNo(t))
        writer.WriteReportElement("5. DEPOSIT DATE:", DepositDate(t).to_string("%d %B %Y"))
        writer.WriteReportElement("6. INITIAL DEPOSIT AMOUNT:", InitialDeposit(t))
        writer.WriteReportElement("7. COUPON INTEREST RATE:", "SFX-ZAR-OND plus 0.4% (or 40 basis points) nacm")
        reportDetail.done()
        
        Computer = writer.Computer()
        writer.WriteReportElement("THIS IS A COMPUTER-GENERATED DOCUMENT AND DOES NOT REQUIRE ANY SIGNATURES.", "")
        Computer.done()
        
        footerDetail = writer.FooterDetail()
        writer.WriteReportElement("For purposes of this Confirmation if for any relevant reset date the specified Coupon Interest Rate is unavailable, including weekends, the rate obtained on the preceding reset date will be deemed to be the Coupon Interest Rate for that reset date. If such rate ceases to be published by SAFEX and the parties cannot agree on a replacement rate, the rate for that reset date will be determined in accordance with 'ZAR-DEPOSIT-Reference Banks' as defined and contemplated in the 2006 ISDA Definitions (published by the International Swaps and Derivatives Association Inc.) as amended or substituted form time to time.", "")
        footerDetail.done()

        date = writer.Date()
        writer.WriteReportElement("", DepositDate(t).to_string("%d %B %Y"))
        date.done()
        
        confirmationReport.done()
    
        try:
            found = 0
            spec = ael.AdditionalInfoSpec['Confo Date Sent']
            for ai in self.t.additional_infos():
                if ai.addinf_specnbr == spec:
                    found = 1
                    break
                    
            if found == 1:
                ai_c = ai.clone()
                ai_c.value = str(ael.date_today())
                ai_c.commit()
            else:
                t_c = self.t.clone()
                ai_new = ael.AdditionalInfo.new(t_c)
                ai_new.value = str(ael.date_today())
                ais = ael.AdditionalInfoSpec['Confo Date Sent']
                ai_new.addinf_specnbr = ais
                ai_new.commit()
        

            found = 0
            spec = ael.AdditionalInfoSpec['Confo Text']
            for ai in self.t.additional_infos():
                if ai.addinf_specnbr == spec:
                    found = 1
                    break
                    
            if found == 1:
                ai_c = ai.clone()
                ai_c.value = 'Generated by ' + ael.userid()
                ai_c.commit()
            else:
                t_c = self.t.clone()
                ai_new = ael.AdditionalInfo.new(t_c)
                ai_new.value = 'Generated by ' + ael.userid()
                ais = ael.AdditionalInfoSpec['Confo Text']
                ai_new.addinf_specnbr = ais
                ai_new.commit()
                
            ael.poll()
        except:
            pass
            
    confirmationReport = writer.ConfirmationReport()
    ConfirmationHead = writer.ConfirmationHead()
    writer.WriteReportElement("", "")
    ConfirmationHead.done()
    
    
    HeadingDetail = writer.HeadingDetail()
    writer.WriteReportElement("", "")
    HeadingDetail.done()
    
    clientDetail = writer.ClientDetail()
    writer.WriteReportElement("", "")
    clientDetail.done()
   
    Notice = writer.Notice()    
    writer.WriteReportElement("", "")
    Notice.done()
    
    reportDetail = writer.ReportDetail()
    writer.WriteReportElement("", "")
    reportDetail.done()
    
    Computer = writer.Computer()
    writer.WriteReportElement("", "")
    Computer.done()
    
    footerDetail = writer.FooterDetail()
    writer.WriteReportElement("", "")
    footerDetail.done()
    confirmationReport.done()
    
    date = writer.Date()
    writer.WriteReportElement("", ael.date_today().to_string("%d %B %Y"))
    date.done()
        
    writer.done()
    
    return strbuf.getvalue()
           
    
def setReportAPIParameters(report, filepath, filename, xslPdfTemplate):
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

def CreateReport(filepath, reportList, xslPdfTemplate):
    
    trade = acm.FTrade[int(reportList[0])]
    filename  = '32_Day_Notice_Confirmation_' + str(trade.Name())
    
    rootdirectory = str(filepath) + ael.date_today().to_string('%Y%m%d') + '/'
    directory =  rootdirectory + str(replist[0]) + '/'
    
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
    setReportAPIParameters(report, filepath, filename, xslPdfTemplate)
    report.CreateReportByXml(reportXML(reportList))
    try:
        foFilepath = os.path.join(filepath, filename  + '.fo')
       
        if os.path.exists(foFilepath):
            os.remove(foFilepath)
    except Exception, ex:
        acm.Log('An exception occurred while trying to remove the fo file: ' + str(ex))


xslPdfTemplate     = '32_Day_notice_PDF'
today              = acm.Time().DateNow()
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory('Y:/Jhb/Operations Secondary Markets/Money Market Ops/MM Confirmations/')
ael_gui_parameters = {'windowCaption':'32 Day Notice Confirmation'}


def getCounterparty():

    counterparty = []
    
    for t in ael.Party.select():
        if t.type in ['Counterparty', 'Broker', 'Client']:
            counterparty.append(t.ptyid)
    counterparty.sort()
    
    return counterparty 
    
def ASQL(*rest):
    acm.RunModuleWithParameters('32_Day_Notice_PDF', 'Standard' )
    return 'SUCCESS'

ael_variables = [
                    ['OutputDirectory', 'Output Directory', directorySelection, None, directorySelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
                    ['TradeNumber', 'Trade Number', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
                    ['Date', 'Date', 'string', today, today, 1]]

def ael_main(parameters):
    
    outputDirectory = parameters['OutputDirectory']
    tradeNumber = parameters['TradeNumber']
    Date = parameters['Date']
    Cpty = ''
    
    if tradeNumber != None and tradeNumber != '':
        
        for trd in str(tradeNumber).split(','):
            
            try:
                
                trade = acm.FTrade[int(trd)]
                t = ael.Trade[int(trd)]
                if trade.Instrument().InsType() in ('Deposit')\
                            and trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']\
                            and trade.Status() not in ['Void', 'Simulated']:  
                    if Date == ael.date_from_time(trade.CreateTime()).to_string('%Y-%m-%d'): 
                        for leg in trade.Instrument().Legs():
                            if leg.RollingPeriod() == '1m':  
                                replist.append(trade.Name())
                                                
                else:
                    acm.Log('Please check trade is valid!')

            except:
                acm.Log('No trades to process')

    if len(replist) > 0:
        CreateReport(outputDirectory, replist, xslPdfTemplate)
        acm.Log('Generating Report')
        
    outputFileName = str(outputDirectory) + ael.date_today().to_string('%Y%m%d') + '/' + '32_Day_Notice_Confirmation' + '_' + ael.date_today().to_string('%Y%m%d')+ '.pdf'
    
    inputFileName = str(outputDirectory) + ael.date_today().to_string('%Y%m%d') + '/' + str(replist[0]) + '/' + '32_Day_Notice_Confirmation' + '_' + str(replist[0]) + ".pdf"
    
    output = PdfFileWriter()
    tc = PdfFileReader(file(imagepath + "Absa Capital 32 Days Notice_tc.pdf", "rb")) 
    hf = PdfFileReader(file(imagepath + "Header_Footer_15Alice.pdf", "rb")) 
   
    instream  = file(inputFileName, "rb")
    inpdf = PdfFileReader(instream)

    for page in range(inpdf.getNumPages()-1):
        temp = inpdf.getPage(page)
        temp.mergePage(hf.getPage(0))
        output.addPage(temp)
        
    temp = inpdf.getPage(inpdf.getNumPages()-1)
    
    temp.mergePage(tc.getPage(0))
    
    output.addPage(temp)
    
    for page in range(tc.getNumPages()-1):
        output.addPage(tc.getPage(page + 1))
        
    outputStream = file(outputFileName, "wb")
    output.write(outputStream)
    outputStream.close()
    
    os.startfile(outputFileName)
    del replist[:]