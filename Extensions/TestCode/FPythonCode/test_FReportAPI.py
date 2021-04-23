from __future__ import print_function
import acm
import ael

import os
import datetime
import time
import unittest

import FReportAPI
from random import choice

import BDPTestCommon

TEMPLATE_1 = 'FReportAPI_unittest1'
TEMPLATE_2 = 'FReportAPI_unittest2'

WORKBOOK = 'FReportAPI_unittest' #Empty portfolio sheet with default columns.
WORKBOOK_NOT_EXISTING = 'not_existing_workbook_name'

TEMPLATE_NOT_EXISTING_1 = 'not_existing_template_name1'
TEMPLATE_NOT_EXISTING_2 = 'not_existing_template_name2'

PORTFOLIO_NOT_EXISTING_1 = 'not_existing_portfolio_name1'
PORTFOLIO_NOT_EXISTING_2 = 'not_existing_portfolio_name1'

EXCEPTION_MESSAGE = 'Exception should have been raised for test to be successful'

''' Class used to test type checking '''
class DummyObject(object):
    def __init__(self):
        pass       
         
    def IsKindOf(self, className):        
        return False        
    def ClassName(self):
        return acm.FSymbol('DummyObject')
    def StringKey(self):
    	return 'dummystring'
    	

class TestReportAPI(unittest.TestCase):  

    def setUp(self):  

        m = None
        try:
            m = __import__('FReportAPIUnittestConfig')  
            reload(m)
            TEMPLATE_1 = m.GetTemplates()[0]
            TEMPLATE_2 = m.GetTemplates()[1]            
            WORKBOOK = m.GetWorkbook()
        except Exception as details:            
            ael.log('WARNING: ' + str(details) + ' Using default values.')
            print ('WARNING: ', details, ' Using default values.')
            
        ael.log('Using templates: ' + TEMPLATE_1 + ', ' + TEMPLATE_2)
        ael.log('Using workbook: ' + WORKBOOK)
        print ('Using templates: ', TEMPLATE_1, ', ', TEMPLATE_2)
        print ('Using workbook: ', WORKBOOK)
            
        #Creating portfolio with name 'testport' + suffix.
        self.suffix = str(datetime.date.today()) + '-' + str(time.clock())
        print ('setUp:', self.suffix)
        counterpartyName = 'testcount' + self.suffix
        acquirerName = 'testacq' + self.suffix
        portfolioName = 'testport' + self.suffix
        self.instrumentName = 'testins' + self.suffix
        self.dict = {
            'Counterparties': [{'Id': counterpartyName}, {'Id': acquirerName}], 
            'Portfolio': {'Id': portfolioName, 'Currency': 'EUR'}, 
            'Trades': [{'AcquireDay': '2007-01-10',
                        'Acquirer': acquirerName,
                        'Counterparty': counterpartyName,
                        'Currency': 'EUR',
                        'Instrument': self.instrumentName,
                        'Premium': '-500',
                        'Price': '5',
                        'Quantity': '100',
                        'TradeTime': '2007-01-08 14:02',
                        'ValueDay': '2007-01-10'},
                       {'AcquireDay': '2007-01-11',
                        'Acquirer': acquirerName,
                        'Counterparty': counterpartyName,
                        'Currency': 'EUR',
                        'Instrument': self.instrumentName,
                        'Premium': '-600',
                        'Price': '6',
                        'Quantity': '100',
                        'TradeTime': '2007-01-09 13:01',
                        'ValueDay': '2007-01-11'}]}

        BDPTestCommon.createPortfolios(self.dict)
        BDPTestCommon.createCounterparties(self.dict)
        ins = BDPTestCommon.createStockOld(self.instrumentName, 'EUR', 2)
        ins.Commit()
        self.testPortfolio = acm.FPhysicalPortfolio[portfolioName]
        BDPTestCommon.createTrade(self.testPortfolio, self.dict['Trades'][0])
        BDPTestCommon.createTrade(self.testPortfolio, self.dict['Trades'][1])
   
    def tearDown(self):    
        #Removing portfolio.
        BDPTestCommon.deleteTrades(self.dict)
        BDPTestCommon.deleteInstrument(self.instrumentName)    
        BDPTestCommon.deleteCounterparties(self.dict)
        BDPTestCommon.deletePortfolio(self.dict)            
    
    def __getTemplateByName(self, tplName):
        template = acm.FTradingSheetTemplate.Select01('name = ' + tplName, '')    
        return template
    
#==============================================================================
    ''' Tests which should succeed '''
#============================================================================== 
    def test_TSTReport(self):
        """ Testing Report API - creating report based on trading sheet template """        
        report = FReportAPI.FWorksheetReportParameters()                                
        report.htmlToScreen = False
        report.template = self.__getTemplateByName(TEMPLATE_1)           
        report.RunScript()                    
#==============================================================================        
    def test_TSTReportAddPortfolio(self):
        """ Testing Report API - creating report based on trading sheet template, adding portfolio """        
        report = FReportAPI.FWorksheetReportParameters()                                
        report.htmlToScreen = False
        report.template = self.__getTemplateByName(TEMPLATE_1)  
        report.portfolios = self.testPortfolio
        report.RunScript()     
#==============================================================================        
    def test_MultipleTSTReport(self):
        """ Testing Report API - creating report based on multiple trading sheet templates """
        report = FReportAPI.FWorksheetReportParameters()                                
        report.htmlToScreen = False
        tpl_list = acm.FArray()
        tpl_list.Add(self.__getTemplateByName(TEMPLATE_1))
        tpl_list.Add(self.__getTemplateByName(TEMPLATE_2))        
        report.template = tpl_list
        report.RunScript()           
#==============================================================================    
    def test_MultipleTSTReportWithPortfolio(self):
        """ Testing Report API - creating report based on multiple trading sheet templates, adding portfolio """
        report = FReportAPI.FWorksheetReportParameters()                                
        report.htmlToScreen = False
        tpl_list = acm.FArray()
        tpl_list.Add(self.__getTemplateByName(TEMPLATE_1))
        tpl_list.Add(self.__getTemplateByName(TEMPLATE_2))        
        report.template = tpl_list
        report.portfolios = self.testPortfolio                         
        report.RunScript()    
#==============================================================================        
    def test_WBReportAddPortfolio(self):
        """ Testing Report API - creating report based on workbook, adding portfolio """                
        report = FReportAPI.FWorksheetReportParameters()                                
        report.htmlToScreen = False
        report.workbook = acm.FWorkbook[WORKBOOK]
        report.portfolios = self.testPortfolio                         
        report.RunScript()       
#==============================================================================    
    def test_TemplateExists(self):        
        """ Testing Report API - test that valid template is entered """         
        report = FReportAPI.FWorksheetReportParameters()                                                 
        report.htmlToScreen = False
        #list                
        report.template = [TEMPLATE_1, TEMPLATE_2]         
        #string
        report.template = TEMPLATE_1         
        #FArray
        tpl_list = acm.FArray()
        tpl_list.Add(self.__getTemplateByName(TEMPLATE_1))
        tpl_list.Add(self.__getTemplateByName(TEMPLATE_2))        
        report.template = tpl_list         
        #FTradingSheetTemplate
        report.template = self.__getTemplateByName(TEMPLATE_1)
#==============================================================================      
    def test_WorkbookExists(self):        
        """ Testing Report API - test that valid workbook is entered """                 
        report = FReportAPI.FWorksheetReportParameters()                                                         
        report.htmlToScreen = False
        #string
        report.workbook = WORKBOOK        
        #FWorkbook
        report.workbook = acm.FWorkbook[WORKBOOK]
#==============================================================================        
    def test_PortfolioExists(self):
        """ Testing Report API - test that valid portfolio is entered """
        report = FReportAPI.FWorksheetReportParameters()                                                 
        report.htmlToScreen = False
        #list                
        report.portfolios = [self.testPortfolio.Name(), self.testPortfolio.Name()]         
        #string
        report.portfolios = self.testPortfolio.Name()
        #FArray
        pf_list = acm.FArray()
        pf_list.Add(self.testPortfolio)
        pf_list.Add(self.testPortfolio)        
        report.portfolios = pf_list   
        #FPhysicalPortfolio
        report.portfolios = self.testPortfolio   
#==============================================================================
    def test_PDFReport(self):
        """ Testing Report API - creating PDF output """
        report = FReportAPI.FWorksheetReportParameters()
        report.htmlToScreen = False
        report.template = TEMPLATE_1
        report.secondaryOutput = True
        report.secondaryFileExtension = '.pdf'
        report.secondaryTemplate = 'FStandardPDF'
        report.RunScript()
#==============================================================================
    def test_ExcelReport(self):
        """ Testing Report API - creating Excel output """
        report = FReportAPI.FWorksheetReportParameters()
        report.htmlToScreen = False
        report.template = TEMPLATE_1
        report.secondaryOutput = True
        report.secondaryFileExtension = '.xls'
        report.secondaryTemplate = 'FTABTemplate'
        report.RunScript()
#==============================================================================
    def test_CsvReport(self):
        """ Testing Report API - creating CSV output """
        report = FReportAPI.FWorksheetReportParameters()
        report.htmlToScreen = False
        report.template = TEMPLATE_1
        report.secondaryOutput = True
        report.secondaryFileExtension = '.csv'
        report.secondaryTemplate = 'FCSVTemplate'
        report.RunScript()
#==============================================================================
    def test_exportedSheetReport(self):
        """ Testing Report API - creating a report on an exported portfolio sheet """		
        filePath = os.path.join(os.getcwd(), 'Test\\defaultPortfolioSheet.shx')
        serialiser = acm.FXmlSerializer()
        sheet = serialiser.Import(filePath)			
        report = FReportAPI.FWorksheetReportParameters()
        report.htmlToScreen = False
        report.sheet = sheet
        report.portfolios = self.testPortfolio.Name()		
        report.RunScript()				
#==============================================================================
    ''' Tests which will cause exception '''
#==============================================================================   
    def test_TemplateNotExistsList(self):        
        """ Testing Report API - test that invalid template/type is not entered (list)"""         
        report = FReportAPI.FWorksheetReportParameters()                                                 
        report.htmlToScreen = False
        #testing list
        try:
            report.template = [TEMPLATE_NOT_EXISTING_1, TEMPLATE_NOT_EXISTING_1]
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
#==============================================================================            
    def test_TemplateNotExistsString(self):        
        """ Testing Report API - test that invalid template/type is not entered (string)"""         
        report = FReportAPI.FWorksheetReportParameters()          
        report.htmlToScreen = False
        #testing string
        try:
            report.template = TEMPLATE_NOT_EXISTING_1
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
#==============================================================================         
    def test_TemplateNotExistsArray(self):        
        """ Testing Report API - test that invalid template/type is not entered (FArray)"""         
        report = FReportAPI.FWorksheetReportParameters() 
        report.htmlToScreen = False
        #testing FArray
        try:
            tpl_list = acm.FArray()
            tpl_list.Add(self.__getTemplateByName(TEMPLATE_1))
            tpl_list.Add(self.__getTemplateByName(TEMPLATE_2))     
            not_template = self.testPortfolio
            tpl_list.Add(DummyObject())                    #wrong type
            report.template = tpl_list
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
#==============================================================================         
    def test_TemplateNotExistsTST(self):        
        """ Testing Report API - test that invalid template/type is not entered (FTradingSheetTemplate)"""         
        report = FReportAPI.FWorksheetReportParameters() 
        report.htmlToScreen = False
        #testing FTradingSheetTemplate
        try:
            report.template = DummyObject()                #wrong type
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
    
    
#==============================================================================             
    def test_WorkbookNotExistsString(self):        
        """ Testing Report API - test that invalid workbook/type is not entered (string)"""         
        report = FReportAPI.FWorksheetReportParameters()                                                         
        report.htmlToScreen = False
        #testing string
        try:
            report.workbook = WORKBOOK_NOT_EXISTING        
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
        
#==============================================================================                     
    def test_WorkbookNotExistsWB(self):        
        """ Testing Report API - test that invalid workbook/type is not entered (FWorkbook)"""         
        report = FReportAPI.FWorksheetReportParameters()                                                         
        report.htmlToScreen = False
        #testing FWorkbook
        try:        
            report.workbook = DummyObject()                #wrong type
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)        
#==============================================================================         
    def test_PortfolioNotExistsList(self):
        """ Testing Report API - test that invalid portfolio/type is not entered (list) """
        report = FReportAPI.FWorksheetReportParameters()                                                 
        report.htmlToScreen = False
        #Testing list                
        try:
            report.portfolios = [PORTFOLIO_NOT_EXISTING_1, PORTFOLIO_NOT_EXISTING_2]         
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
#==============================================================================                 
    def test_PortfolioNotExistsString(self):
        """ Testing Report API - test that invalid portfolio/type is not entered (string)"""
        report = FReportAPI.FWorksheetReportParameters()     
        report.htmlToScreen = False
        #Testing string
        try:
            report.portfolios = PORTFOLIO_NOT_EXISTING_1
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
#==============================================================================                 
    def test_PortfolioNotExistsArray(self):
        """ Testing Report API - test that invalid portfolio/type is not entered (FArray) """
        report = FReportAPI.FWorksheetReportParameters()             
        report.htmlToScreen = False
        #Testing FArray
        try:
            pf_list = acm.FArray()
            pf_list.Add(self.testPortfolio)
            pf_list.Add(self.testPortfolio)                    
            pf_list.Add(DummyObject())                     #wrong type
            report.portfolios = pf_list   
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)
#==============================================================================         
    def test_PortfolioNotExistsPF(self):
        """ Testing Report API - test that invalid portfolio/type is not entered (FPhysicalPortfolio) """
        report = FReportAPI.FWorksheetReportParameters()             
        report.htmlToScreen = False
        #Testing FPhysicalPortfolio
        try:                       
            report.portfolios = DummyObject()              #wrong type
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)              
#==============================================================================                     
    def test_NoSheetFound(self):
        """ Testing Report API - neither of workbook or template set """
        report = FReportAPI.FWorksheetReportParameters()                   
        report.htmlToScreen = False
        try:
            report.RunScript()
        except Exception as details:
            print (details)
            return            
        raise Exception(EXCEPTION_MESSAGE)






