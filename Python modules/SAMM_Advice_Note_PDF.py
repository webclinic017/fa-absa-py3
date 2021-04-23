"""-----------------------------------------------------------------------------
PROJECT                 :  ABITFA-569
PURPOSE                 :  Decommission platypus and move all existing reports using it to FOP
                           
DEPATMENT AND DESK      :  OPS
REQUESTER               :  Aaeda Salejee
DEVELOPER               :  Ickin Vural
CR NUMBER               :  C000000697493

-----------------------------------------------------------------------------
Changes:
Date            Change Number   Developer         Description
2018            CHG1000757460   Stuart Wilson     Changes to incorporate new 2018 logo and remove Barclays affiliation
"""

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
import FReportSettings as frs

tradelist = []

reportelems = '''ReturnConfirmationReport XMLResources ClientDetail ReportDetail HeadingDetail FooterDetail ReportElement Label Value'''

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
    
    def __init__(self, trade, Date):
        self.trade      = trade
        self.instrument = trade.Instrument()
        self.Date = Date
        self.t = ael.Trade[trade.Oid()]
        
    
    def _broughtSold(self):
        BoughtSold = ''
        if self.t.quantity > 0:
            BoughtSold = 'BOUGHT'
        else:
            BoughtSold = 'SOLD'
        return BoughtSold
        
    def _toFrom(self):
        FromTo = ''
        if self.t.quantity > 0:
            FromTo = 'FROM'
        else:
            FromTo = 'TO'
        return FromTo

    def _tenor(self):
        Tenor = 0
        Tenor = self.t.value_day.days_between(self.t.insaddr.exp_day, 'Act/365')
        return Tenor
        
    def _yieldRate(self):
        Yieldrate = ''
        Yieldrate = str('%.5f' %((self.t.price/100) / (1-((self.t.price/100)*(self.t.value_day.days_between(self.t.insaddr.exp_day))/365)) * 100))
        return Yieldrate
        
    def _discountAmount(self):
        DiscountAmount = ' '
        if self.t.add_info('MM_Instype') == 'NCD':
            DiscountAmount = str(formnum(float(self.t.add_info('MM_Original_Nominal')) + self.t.premium))
        else:
            DiscountAmount = str(formnum(self.t.insaddr.contr_size * self.t.quantity + self.t.premium))
        return DiscountAmount
        
    def _nominalAmount(self):
        Nominal = ''
        Nominal = str(formnum(float(self.t.add_info('MM_Original_Nominal'))))
        return Nominal
        
    def _maturityVal(self):
        MaturityDate = ''
        MaturityDate = str(self.t.insaddr.exp_day)
        return MaturityDate
        
    def _considerationAmt(self):
        ConsiderationAmount = ''
        ConsiderationAmount = str(formnum(self.t.premium + self.t.fee))
        return ConsiderationAmount
        
    def unexCor(self):
        UnexCor_Code = ''
        try:
            UnexCor_Code = self.trade.Counterparty().AdditionalInfo().UnexCor_Code()
        except:
            pass
        return UnexCor_Code
        
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
        
        writer.WriteReportElement("", self.trade.Counterparty().Fullname())
        writer.WriteReportElement("", self.trade.Counterparty().Address())
        writer.WriteReportElement("", self.trade.Counterparty().Address2())
        writer.WriteReportElement("", self.trade.Counterparty().City())
        writer.WriteReportElement("", self.trade.Counterparty().Country())
        writer.WriteReportElement("", self.trade.Counterparty().ZipCode()) 
        writer.WriteReportElement("", self.trade.Counterparty().Telephone())
          
        
        clientDetail.done()
        
        HeadingDetail = writer.HeadingDetail()
         
        writer.WriteReportElement("MONEY MARKET ADVICE NOTE", "")
        writer.WriteReportElement("We confirm having "+ self._broughtSold() + " the following Money Market Instrument " + self._toFrom(), "")
        
        
        
        HeadingDetail.done()
                
        reportDetail = writer.ReportDetail()
                        
        writer.WriteReportElement("COMM PAPER:", self.instrument.Name())
        writer.WriteReportElement("REFERENCE NUMBER:", self.trade.Name())
        writer.WriteReportElement("COUNTERPARTY CODE:", self.trade.Counterparty().Name())
        writer.WriteReportElement("NUTRON CODE:", self.trade.Counterparty().HostId())
        writer.WriteReportElement("UNEXCOR CODE:", self.unexCor())
        writer.WriteReportElement("ISSUED BY:", self.instrument.Issuer().Name())
        writer.WriteReportElement("VALUE DATE:", self.trade.ValueDay())
        writer.WriteReportElement("MATURITY DATE:", self.instrument.ExpiryDateOnly())
        writer.WriteReportElement("DAYS TO MATURITY:", self._tenor())
        writer.WriteReportElement("DISCOUNT RATE:", str('%.5f' %self.t.price) + "%")
        writer.WriteReportElement("YIELD RATE:", self._yieldRate()+ "%")
        writer.WriteReportElement("DISCOUNT AMOUNT:", "R" + self._discountAmount())
        writer.WriteReportElement("NOMIAL AMOUNT:", "R" + self._nominalAmount())
        writer.WriteReportElement("MATURITY VALUE:", self._maturityVal())
        writer.WriteReportElement("CONSIDERATION AMOUNT:", "R" + self._considerationAmt())
        writer.WriteReportElement("BROKERS COMMISSION:", "R" + str(formnum(self.t.fee)))
        writer.WriteReportElement("PROFIT CENTRE:", str(self.t.prfnbr.prfid))
        writer.WriteReportElement("ENQUIRIES:", '(011) 895-6734 / 6724')
        
        reportDetail.done()
    
        
        writer.done()
        
    
        
        # Update Additional Infos
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
        except Exception, ex:
            acm.Log('An exception occurred while trying to update Add Infos: ' + str(ex))
            
       
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
    
    def CreateReport(self, filepath, filename, xslPdfTemplate):
        
        
        trade = acm.FTrade[int(filename)]
        
        filename  = 'MM advise confirmation_' + str(trade.Name())
        
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
 


xslPdfTemplate     = 'SAMM_Advice_Note_PDF'
today              = acm.Time().DateNow()
outputSelection = acm.FFileSelection()
outputSelection.PickDirectory(True)
outputSelection.SelectedDirectory('Y:/Jhb/Markets and Treasury/Money Market Ops/MM Confirmations/')

ael_gui_parameters = {'windowCaption':'Money Market Confirmation'}


def ASQL(*rest):
    acm.RunModuleWithParameters('SAMM_Advice_Note_PDF', 'Standard' )
    return 'SUCCESS'


ael_variables = [
                    ['OutputDirectory', 'Output Directory', outputSelection, None, outputSelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
                    ['TradeNumber', 'Trade Number', 'string', None, None, 0, 0, 'To run for a soecific trade, enter the trade number here.', None, 1],
                    ['Date', 'Date', 'string', today, today, 1]]

def ael_main(parameters):

    
    outputDirectory = parameters['OutputDirectory']
    tradeNumber = parameters['TradeNumber']
    Date = parameters['Date']
    
        
    if tradeNumber != None and tradeNumber != '':
    
        for trd in str(tradeNumber).split(','):
        
            try:

                trade = acm.FTrade[int(trd)]
                t = ael.Trade[int(trd)]
                
                if (t.trdnbr) not in tradelist:
                    tradelist.append(t.trdnbr)
                
                if trade.Instrument().InsType() in ('Bill')\
                            and trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']\
                            and trade.Status() not in ['Void', 'Simulated']:
                                report = ReturnConfirmationReport(trade, Date)
                                report.CreateReport(outputDirectory, str(trade.Oid()), xslPdfTemplate)
                                acm.Log('Generating Report')
                            
                else:
                    acm.Log('Please check trade is valid!')
            except:
                acm.Log('No trades to process')
                
    outputFileName = str(outputDirectory) + ael.date_today().to_string('%Y%m%d') + '/' + 'MM advise confirmation' + ' '+ time.ctime().replace(':', '') + ".pdf"

    inputFileNames = glob.glob(str(outputDirectory) + ael.date_today().to_string('%Y%m%d') + '/' + str(tradelist[0]) + '/' + "/*.pdf") 
    
    output = PdfFileWriter()

    for pdfFileName in inputFileNames:
        output.addPage(PdfFileReader(file(pdfFileName, "rb")).getPage(0)) # adds the first page of each document
        
    outputStream = file(outputFileName, "wb")
    output.write(outputStream)
    outputStream.close()
    os.startfile(outputFileName)
    del tradelist[:]
