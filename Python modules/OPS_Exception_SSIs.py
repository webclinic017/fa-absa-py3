'''
Developer   : Lawrence Mucheka
Module      : OPS_Exception_SSIs
Date        : 2015-03-19
Description : Generates Excel Report for Settlement Exceptions
CR	    : 

History
=======

Date            CR                  Developer               Description
==========      ==============      ================        ===========================================================================
2015-03-19      CHNG0002839366      Lawrence Mucheka        Initial Implementation
2016-02-25      CHNG0003472591      Lawrence Mucheka        1. Add the following fields to the report
                                                                - Instrument ID
                                                                - External ID 1
                                                                - External ID 2
                                                                - Instrument type
                                                            2. Please show the status explanation on this report, ie the reason why its 
                                                               in exception. eg Missing SSIs
                                                            3. Exceptions need to be rolled until resolved or excluded from report. 
                                                               Please remove post settlement view as it will no longer be required 
                                                               due to rolling effect
                                                            4. Show upcoming exceptions for 1 month in advance                                                            
'''

import ael, acm,  time, csv
import FOperationsDateUtils as Utils
import FBDPGui

from FBDPCommon              import acm_to_ael
from datetime                import datetime
            
class OPSExceptionSSIs():
    """ OPS Settlement SSI Exceptions Report """
    
    reportName = 'OPS_Exception_SSIs'
    settlementExceptionsHeader = [
                                    'Value Day',
                                    'Trade',
                                    'Counterparty',
                                    'Curr',
                                    'Amount',
                                    'StatusExplanation',
                                    'Portfolio',
                                    'InstrumentType',
                                    'CashflowType',
                                    'InstrumentID',
                                    'ISIN',
                                    'ExternalID1',
                                    'ExternalID2',
                                    'Acquirer',
                                    'SettlementId',
                                    'Status'
                                 ]
    
    def __init__(self, exceptionTypes, settlementTypes):     
        """ Constructor """
        
        self.exceptionTypes = exceptionTypes
        self.settlementTypes = settlementTypes
        
        
    def GetRows(self, startDate, endDate, *rest): 
        """ Get settlements in Exception """

        CPTY_TYPE_INTERNAL_DEPARTMENT = 'Intern Dept'

        rows = []
        rows.append(self.settlementExceptionsHeader)
        		
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', 'Exception')
        query.AddAttrNode('ValueDay', 'GREATER_EQUAL', startDate)
        query.AddAttrNode('ValueDay', 'LESS_EQUAL', endDate)
        settlements = query.Select()
        
        for settlement in settlements:
            if(self.IsInException(settlement) and self.IsTypeAllowed(settlement)):                              
                trade = settlement.Trade()
                amount = settlement.Amount()
                
                #Get payments only
                if(trade and amount < 0):                                            
                    counterparty = trade.Counterparty()
                    instrument = trade.Instrument()                       
                    if(counterparty.Type() != CPTY_TYPE_INTERNAL_DEPARTMENT):                        
                        rows.append([
                                        str(settlement.ValueDay()),
                                        str(trade.Oid()),
                                        counterparty.Name(),
                                        trade.Currency().ISIN_UndISIN_Name(),
                                        str(amount),
                                        settlement.StatusExplanationText(),
                                        trade.Portfolio().Name(),
                                        instrument.InsType(),
                                        str(acm_to_ael(settlement).type),
                                        instrument.Name(),
                                        instrument.ISIN_UndISIN_Name(),
                                        instrument.ExternalId1(),
                                        instrument.ExternalId2(),
                                        trade.Acquirer().Name(),
                                        str(settlement.Oid()),
                                        settlement.Status()
                                    ])                 
        return rows
     
    
    def IsInException(self, settlement): 
        """ Return true if settlement has at least one 
            of the exceptions specified in the ExceptionTypes list """

        SHORT_POSITION_EXCEPTION = 4194304

        isInMessageException = any([
                        e for e in self.exceptionTypes 
                            if e in settlement.StatusExplanationText().upper()
                    ])

        return (isInMessageException and 
            ((not settlement.Acquirer() or not settlement.Counterparty()) or
                (not settlement.AcquirerAccount() or not settlement.CounterpartyAccount())))
    
    
    def IsTypeAllowed(self, settlement): 
        """ Return true if settlement type is not any 
            of the types in the settlementTypes list"""           
    
        return not(settlement.Type().upper() in self.settlementTypes)


    def WriteOutput(self, rows, fileName, access='wb'):
        """ Persist data to file """
        
        output = open(fileName, access)
        try:    
            output.write(self.GetBanner())
            csvWriter = csv.writer(output,  dialect='excel-tab').writerows(rows) 
            print 'Wrote secondary output to: %s' %(fileName)        
        except IOError:
            print 'Error writing secondary output to: %s' %(fileName)         
        finally:
            output.close() 
            
            
    def GetBanner(self):
        """Create the banner """
    
        generatedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        generatedTime += ' (UTC+0%i:00)'% ((datetime.now() - datetime.utcnow()).seconds/3600)
        
        return ''.join([
                        '            Report Name: {0}\n'.format(self.reportName),
                        '            Generated Time: {0}\n\n'.format(generatedTime)
                       ]) 
    
'''
AEL Variables :
Variable Name, Display Name, Type, Candidate Values, Default, 
Mandatory, Multiple, Description, Input Hook, Enabled
'''
boolDict = {'Yes': True, 'No': False}
boolDictDisplay = sorted(boolDict.keys())
ael_variables = FBDPGui.DefaultVariables([
                                            'lookBackDays', 'Look Back Days',
                                            'int', None, 7, 1, 0,
                                            'When Value Day is starting', None, 1 
                                         ],
                                         [
                                            'lookForwardDays', 'Look Forward Days',
                                            'int', None, 30, 1, 0,
                                            'When Value Day is ending', None, 1 
                                         ],
                                         [
                                            'rollingBaseDay', 'Rolling Base Day',
                                            'string', None, '2016-03-01', 1, 0,
                                            'Value Day start if not using lookBackDays', None, 1 
                                         ],
                                         [
                                            'fileRoot', 'File Root', 
                                            'string', None, '/services/frontnt/Task/', 1, 0,      
                                            'Location to persist output', None, 1
                                         ],
                                         [
                                            'isLookBackDaysEnabled',
                                            'Lookback days enabled?',
                                            'string', boolDictDisplay, 'No', 1, 0,
                                            'Lookback days enabled?', None, 1
                                         ])    
    
def ael_main(dict):
    """ Main method """
    
    try:
        lookBackDays = dict['lookBackDays']
        lookForwardDays = dict['lookForwardDays']
        rollingBaseDay = dict['rollingBaseDay']
        fileRoot = dict['fileRoot']  
        isLookBackDaysEnabled = boolDict[dict['isLookBackDaysEnabled']]      
    except:
        return 'Error trying to get parameter values'
    
    if isLookBackDaysEnabled:
        startDate = Utils.AdjustDateToday(Utils.GetAccountingCurrencyCalendar(), -lookBackDays)
    else:
        startDate = rollingBaseDay
                
    endDate = Utils.AdjustDateToday(Utils.GetAccountingCurrencyCalendar(), lookForwardDays)
    
    opsExceptionSSIs = OPSExceptionSSIs([
                                            'MISSING ACQUIRER ACCOUNT',
                                            'MISSING COUNTERPARTY ACCOUNT'
                                        ],
                                        [
                                            'SECURITY NOMINAL',
                                            'END SECURITY',
                                            'CREDIT DEFAULT'
                                        ])
                                        
    fileName = '{0}{1}_{2}.xls'.format(fileRoot, opsExceptionSSIs.reportName, ael.date_today().to_string('%y%m%d'))
    opsExceptionSSIs.WriteOutput(opsExceptionSSIs.GetRows(startDate, endDate), fileName)
