'''
Developer   : Lawrence Mucheka
Module      : SAOPSCACollateralBasedOnTrades
Date        : 2015-04-28
Description : Generates Excel Report for SAOPS Cash Analysis Collateral trades-based cashflows 
CR	    : 

History
=======

Date            CR                      Developer                       Description
====            ======                  ================                =============
2015-04-28      CHNG0003050591                        Lawrence Mucheka                Initial Implementation
'''

import ael, acm,  time, csv
import FOperationsUtils as Utils
import FBDPGui

from FOperationsTradeFilter import EODFilterHandler, FilterSpecification
from datetime               import datetime
from itertools              import groupby
            
            
class SAOPSCACollateralBasedOnTrades():
    """ SAOPS CA Collateral Based On Trades Report"""
    
    reportName = 'SAOPSCACollateralBasedOnTrades'
    
    def __init__(self, moneyflowTypesToAlwaysExclude, queryFolders):     
        """ SAOPSCACollateralBasedOnTrades Constructor"""
        
        self.moneyflowTypesToAlwaysExclude = moneyflowTypesToAlwaysExclude
        self.queryFolders = queryFolders

        self.defaultRowLabel = 'Cash Flow'   
        self.rows = []
        self.allData = {}
        self.mfSpace = acm.FCalculationSpaceCollection().GetSpace("FMoneyFlowSheet", "Standard")
        self.header = [
                            '',
                            'Acquirer', 
                            'Counterparty',
                            'Trade Nbr',
                            'Approx. Load',
                            'Approx. Load Ref',
                            'Trade Time',
                            'Trxnbr', 
                            'Instr', 
                            'Instype', 
                            'Instrument Open End', 
                            'ExtrnID1', 
                            'Trade Your Ref', 
                            'Trade Status', 
                            'Trade Nominal', 
                            'Nominal', 
                            'Type', 
                            'PayD', 
                            'Curr', 
                            'Proj', 
                            'Trade Counterparty', 
                            'Instrument Issuer',
                            'Instrument Underlying Issuer',
                            'Portfolio',
                            'Instrument Underlying Isin',                     
                            'Isin'
                      ]    
        
        
    def WriteOutput(self, rows, fileName, access='wb'):
        """ Persist rows to the file: fileName"""
        
        outputFile = open(fileName, access)
        try:    
            outputFile.write(self.GetBanner())
            csv.writer(outputFile,  dialect='excel-tab').writerows(rows)
            print 'Wrote secondary output to: %s' %(fileName)        
        except IOError:
            print 'Error writing output to: %s' %(fileName)         
        finally:
            outputFile.close() 
    
    
    def GetBanner(self):
        """Create the banner """
    
        generatedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        generatedTime += ' (UTC+0%i:00)'% ((datetime.now() - datetime.utcnow()).seconds/3600)
        
        return ''.join([
                            '            Type: Cash Analysis Report\n',
                            '            Report Name: {0}\n'.format(self.reportName),
                            '            Generated Time: {0}\n\n'.format(generatedTime)
                       ]) 
                      
                      
    def IsAllowed(self, moneyFlow): 
        """ Return true if moneyFlow type is not any 
            of the types in the moneyflowTypesToAlwaysExclude list"""           
    
        return not(moneyFlow.Type().upper() in self.moneyflowTypesToAlwaysExclude)                   
   
      
    def FillRows(self, startDate, endDate, *rest): 
        """ Fill the row array with data """
        
        rawPayDayList = [] 
        allMoneyFlows = []         

        self.rows.append(self.header)        
        
        #Get trades based on query folder
        trades = EODFilterHandler(self.queryFolders, None, FilterSpecification(acm.FTrade)).GetObjects()      

        #Get the allowed cash flows
        map(lambda t:allMoneyFlows.extend(filter(lambda m:m.IsKindOf(acm.FCashFlowMoneyFlow) and
            self.IsAllowed(m), filter(lambda n:startDate <= n.PayDay() <= endDate, t.MoneyFlows()))), trades)            

        map(lambda x:rawPayDayList.append(x.PayDay()), allMoneyFlows)
        
        #For each of the available cashflow dates, add the corresponding cashflow rows for each currency
        for payDay in [k for k, _ in groupby(sorted(rawPayDayList))]:
            currencyKeyedData = {}
            map(lambda m:currencyKeyedData.update({m.Currency().Name():filter(lambda l:l.Currency().Name() == m.Currency().Name(),
                filter(lambda s:s.PayDay() == payDay, allMoneyFlows))}), filter(lambda s:s.PayDay() == payDay, allMoneyFlows))
            self.AddDateLevelRow(payDay, currencyKeyedData)


    def AddDateLevelRow(self, payDay, currencyKeyedData):
        """ Add the whole currencyKeyedData set of rows for this date: payDay """

        self.rows.append([payDay])
        for currency in currencyKeyedData.keys():
            self.rows.append([currency])
            map(lambda moneyFlow:self.AddMoneyFlowRow(moneyFlow), currencyKeyedData[currency])                
            

    def AddMoneyFlowRow(self, moneyFlow):
        """ Add the single money flow row for this moneyflow: moneyFlow"""

        CAP = 'Cash Analysis Projected'
        CATN = 'Cash Analysis Trade Nominal'
        CAN = 'Cash Analysis Nominal'

        trade = moneyFlow.Trade()
        ins = moneyFlow.Instrument()
        und = ins.Underlying()                    
        counterparty = trade.Counterparty()
        ai = trade.AdditionalInfo()
      
        self.rows.append([
                            self.defaultRowLabel,
                            trade.Acquirer().StringKey(),
                            moneyFlow.Counterparty().StringKey(),
                            trade.Oid(),
                            ai.Approx_46_load() or '',
                            ai.Approx_46_load_ref() or '',
                            trade.TradeTime(),
                            str(trade.TrxTrade().Oid()) if trade.TrxTrade() else '',
                            ins.Name(),
                            ins.InsType(),
                            ins.OpenEnd(),
                            ins.ExternalId1(),
                            trade.YourRef(),
                            trade.Status(),
                            self.mfSpace.CreateCalculation(moneyFlow, CATN).FormattedValue().replace(',', ''),
                            self.mfSpace.CreateCalculation(moneyFlow, CAN).FormattedValue().replace(',', ''),                                            
                            moneyFlow.Type(),
                            moneyFlow.PayDay(),
                            moneyFlow.Currency().ISIN_UndISIN_Name(),
                            self.mfSpace.CreateCalculation(moneyFlow, CAP).FormattedValue().replace(',', ''),
                            trade.Counterparty().Name(),
                            ins.Issuer().Name if ins.Issuer() else '',
                            und.Issuer().Name() if und and und.Issuer() else '',
                            trade.Portfolio().Name(),
                            und.Isin() if und else '',                                        
                            ins.Isin()  
                        ])     
    
      
'''
AEL Variables :
Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
Multiple, Description, Input Hook, Enabled
'''

ael_variables = FBDPGui.DefaultVariables(['fileRoot', 'File Root', 
                                            'string', None, '/services/frontnt/Task/', 1, 0, '', None, 1],
                                         ['mfAlwaysExclude', 'Moneyflow Types to always exclude(CSV)', 
                                            'string', None, 'Call Fixed Rate Adjustable,Redemption Amount', 0, 0, '', None, 1],
                                         ['queryFolderName', 'Query Folder Name', 
                                            'string', None, 'SAOPS_CA_Collateral_2_Trades', 1, 0, '', None, 1],
                                         ['lookBackDays', 'Look Back Days',
                                            'int', None, 5, 1, 0, 'Pay Day Offset-For the Start Date(INT)', None, 1],
                                         ['lookForwardDays', 'Look Forward Days',
                                            'int', None, 20, 1, 0, 'Pay Day Offset-For the End Date(INT)', None, 1])    
    
def ael_main(dict):
    """ SAOPSCACollateralBasedOnTrades Main method"""
    
    try:
        fileRoot = dict['fileRoot']        
        moneyflowTypesToAlwaysExclude = dict['mfAlwaysExclude'].upper().split(',')
        queryFolderName = dict['queryFolderName']
        lookBackDays = dict['lookBackDays']
        lookForwardDays = dict['lookForwardDays']
    except:
        return 'Could not get parameter values!'
    
    startDate = Utils.AdjustDateToday(Utils.GetAccountingCurrencyCalendar(), -lookBackDays)
    endDate = Utils.AdjustDateToday(Utils.GetAccountingCurrencyCalendar(), lookForwardDays)
    
    report = SAOPSCACollateralBasedOnTrades(moneyflowTypesToAlwaysExclude, [queryFolderName])
                                        
    fileName = '{0}{1}.xls'.format(fileRoot, report.reportName)
    report.FillRows(startDate, endDate)
    report.WriteOutput(report.rows, fileName)
