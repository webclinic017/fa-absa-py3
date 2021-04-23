'''----------------------------------------------------------------------------------------------------------------
MODULE
    PS_CommodityMapping
DESCRIPTION
    Developer           : Phumzile Mgcima
    Date                : 2012-11-09
    Purpose             : Creates a count per porfolio and counterparty
    Requestor           : Phumzile Mgcima
    CR Number           : 
ENDDESCRIPTION

HISTORY
    Date:       CR Number:      Developer:              Description:
----------------------------------------------------------------------------------------------------------------'''

import acm, ael
import csv
import sys
import FBDPGui
import FRunScriptGUI
import datetime
import math
from Eagle_Comm_Absa_Cash import OptionCashFlow, FutureFowardCashFlow
from Eagle_Comm_Absa_Util import _estimatedValue, _hybridNominalPosition, get_trades_data, date_from_timestamp, maturitydate_from_timestamp
from EaglePriceSwapWriter import writePriceSwapsResets
import os
directorySelection=FRunScriptGUI.DirectorySelection()
today = acm.Time().DateToday()
calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection() 
tag = acm.CreateEBTag() 

class BaseCommReset:
    def __init__(self,trade,exoticEvent,leg,cashflow=None,reset=None):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.leg = leg
        self.exoticEvent = exoticEvent
        self.cashflow = cashflow
        self.reset = reset
        
    def	_sourceTradeID(self):
        return self.trade.Oid()
        
            
    def	_sourceLegID(self):	
        id = 0
        if (self.instrument.InsType() =='Future/Forward' and ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri'))):
                id = self.leg
            
              
        return id
        
    def	_sourceCashID(self):
    
	id = self.leg
        if (self.instrument.InsType() =='Future/Forward' and ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri'))):
            id = 0
            
        return id
        
    def	_sourceResetID(self):
        id = 0
        if self.trade.Instrument().InsType()=='Option':
            if self.trade.Instrument().IsAsian():
                if self.exoticEvent:
                    id = self.exoticEvent.Oid()
        return id
        
    def	_resetType(self):
        type =  'PROJECTED'
        if self.trade.Instrument().InsType()=='Option':
            if self.trade.Instrument().IsAsian():
                if self.exoticEvent:
                    if self.exoticEvent.EventValue()!=-1:
                        type = 'FIXED'
        return type
        
    def	_resetValue(self):
        value = self._floatLegRate()
        #print isinstance(value,float)
        
        if (self.trade.Instrument().InsType()=='Option'
            and self.trade.Instrument().IsAsian()):
                if self.exoticEvent:
                    value = self.exoticEvent.EventValue()
                    if value == -1:
                        value = self._floatLegRate()
                        if ((math.isnan(value)==True) or (isinstance(value, float)==False)):
                            value = self.trade.Price
                            if value ==0:
                                value = 1
                                
        elif ((math.isnan(value)==True) or (isinstance(value, float)==False)):
        #if isinstance(value,float)==False :
            value = self.trade.Price()
            if value == 0:
                value = 1
                
        
            
        
                       
            
        return value
        
        
        
    def	_resetDate(self):
        date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        if self.trade.Instrument().InsType()=='Option':
            if self.trade.Instrument().IsAsian():
                if self.exoticEvent:
                    date = datetime.datetime.strptime(self.exoticEvent.Date(), '%Y-%m-%d').strftime('%Y%m%d')
        return date
	
    def	_notional(self):
        
        
           
        notional = self._totalTradeAmount()
        if (((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri'))
            and self.trade.Instrument().InsType()=='Future/Forward'):
            notional = notional = self._correspondingCashFlow()._notional()
         
        if self.trade.Instrument().InsType() == 'Option' and self.trade.Instrument().IsAsian():
            lengthAdjust=0
            for exoticEvent in self.trade.Instrument().ExoticEvents():
                if exoticEvent.Type()!='Average price':
                    lengthAdjust=lengthAdjust+1
            length = (len(self.trade.Instrument().ExoticEvents())-lengthAdjust)
            #print 'length',length
            notional = notional/float(length)
        
       
        return notional
            
    def	_rfisDate(self):
        date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        if self.trade.Instrument().InsType()=='Option':
            if self.trade.Instrument().IsAsian():
                if self.exoticEvent:
                    date = datetime.datetime.strptime(self.exoticEvent.Date(), '%Y-%m-%d').strftime('%Y%m%d')
        return date
        
    def _totalTradeAmount(self):
        contractSize = self.instrument.ContractSize()
        quantity = self.trade.Quantity()
        
        
        return quantity * contractSize
        
    def _correspondingCashFlow(self):
        baseCashlflow = None
        if self.trade.Instrument().InsType() == 'Option':
            baseCashlflow = OptionCashFlow(self.trade, self.leg)
        elif self.trade.Instrument().InsType() == 'Future/Forward':
            baseCashlflow = FutureFowardCashFlow(self.trade, self.leg)
        
        return baseCashlflow
        
    def _floatLegRate(self):
        rate = 0
        
        rate = self.instrument.Underlying().Calculation(). MarkToMarketPrice(calc_space, today, self.trade.Instrument().Currency())
        
        
        return rate.Value().Number()
        
    
class SwapCommReset(BaseCommReset):
    def __init__(self, trade, exoticEvent, leg, cashflow, reset):
        BaseCommReset.__init__(self, trade, exoticEvent, leg, cashflow, reset)
        self.leg = leg
        self.cashflow =cashflow
        self.reset = reset
    
    def _sourceLegID(self):
        return self.leg.Oid()
    def	_sourceCashID(self):
        return self.cashflow.Oid()
    def	_sourceResetID(self):
        return self.reset.Oid()
    def	_resetType(self):
        if self.reset.Day() < today:
            return 'FIXED'
        else:
            return 'PROJECTED'
     
    def _resetValue(self): 
        if self._resetType() == 'Fixed':
            return self.reset.FixingValue()
        else:
            value = 0
            try:
                sheetType  = 'FMoneyFlowSheet'
                context    = acm.GetDefaultContext()
                columnName = 'Cash Analysis Fixing Estimate'
                calcSpace  = acm.Calculations().CreateCalculationSpace( context, sheetType )
                v = calcSpace.CalculateValue( self.reset, columnName ).Value()                
                value = v.Value().Number()
            except:
                pass
            return value
            
    def	_resetDate(self):
        datetime.datetime.strptime(self.reset.Day(), '%Y-%m-%d').strftime('%Y%m%d')
        
        
    def	_notional(self):
        #notional = abs(self.trade.Quantity())
        
        notional = abs(_hybridNominalPosition(self.cashflow)*self.trade.Quantity())
        
        #print 'swap notional',notional,self.trade.Oid()
        if self.trade.Quantity()> 0 and self.leg.PayLeg() :
            notional = notional*(-1)
        elif self.trade.Quantity() < 0 and self.leg.PayLeg()==False:
            notional = notional*(-1)
            
        
        if self.leg.ResetPeriod()!='0d':
        
            if self.reset.ResetType()=='Unweighted':
                weight = len(self.cashflow.Resets())
                notional = (notional/float(weight))
            else:
                days_betwn_cashflows = ael.date(self.cashflow.StartDate()).days_between(ael.date(self.cashflow.EndDate()))  
                #bus_days_betwn_resets = ael.date(self.reset.StartDate()).bankingdays_between(ael.date(self.reset.Day()),ael.Calendar['ZAR Johannesburg']) 
                bus_days_betwn_resets = ael.date(self.reset.StartDate()).days_between(ael.date(self.reset.Day()))  
                     
                
                #print 'bus_days_betwn_resets',type(bus_days_betwn_resets)
                weight = bus_days_betwn_resets/float(days_betwn_cashflows)
                #print self.trade.Oid(), weight ######
                notional = notional*weight
            
        return notional
        
    def _resetDate(self):
        return datetime.datetime.strptime(self.reset.Day(), '%Y-%m-%d').strftime('%Y%m%d')
        
    def __cashflowNotional(self):
        return self.cashflow.Calculation().Nominal(calc_space, self.trade).Value().Number()
     
    def	_rfisDate(self):
        return self._resetDate()
  
        
    
class EagleCommResetReport:

    def __init__(self, file):
        self.file  = file

     
    def _fieldNames(self):

        fieldNames = ['010',
            'SOURCE_TRADE_ID',
            'SOURCE_LEG_ID',
            'SOURCE_CASH_ID',
            'SOURCE_RESET_ID',
            'RESET_TYPE',
            'RESET_VALUE',
            'RESET_DATE',
            'NOTIONAL',
            'RFIS_DATE']
            
        return fieldNames
        
    def _writeHeader(self):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fields = ['010', 'JHB', datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y%m%d')]
        #print 'datetime.datetime.strptime(str(today), '').strftime('')',datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y%m%d'),today
        
        writer.writerow(fields)
        
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter='|', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        finally:
            #self.file.close()
            print ''
            
    def _writeResetRow(self, baseCommReset):
        fields  = ['030',
        baseCommReset._sourceTradeID(),
        baseCommReset._sourceLegID(),
        baseCommReset._sourceCashID(),
        baseCommReset._sourceResetID(),
        baseCommReset._resetType(),
        baseCommReset._resetValue(),
        baseCommReset._resetDate(),
        baseCommReset._notional(),
        baseCommReset._rfisDate()]
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _writeFooter(self, count, checksum):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fields = ['090', count, checksum]
        writer.writerow(fields)
        

        
ael_variables = FBDPGui.DefaultVariables(['filePath', 'File Path', directorySelection, None, directorySelection, 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1]
)

def get_filename():
    """Return the dump's filename."""
    date_str = maturitydate_from_timestamp(today)
    return '_'.join(['ABSA_COMM_TDB_RESET']) + '.DAT'
        
   
def ael_main(ael_dict):
    filePath = ael_dict['filePath']
    output_dir = str(ael_dict['filePath'])
    filename = os.path.join(output_dir, get_filename())

    file = open(str(filename), 'wb') 
    
    report = EagleCommResetReport(file)
    report._writeHeader()
    report._writeColumnNames()
    checksum = 0
    count = 0
    leg = 0
    
    all_trades = get_trades_data()
    
    for trade in all_trades:
        
        baseInsr  = BaseCommReset(trade, None, leg)
       
        if trade.Instrument().InsType() == 'Option':
            
            leg = 0
            if trade.Instrument().IsAsian() :
                for exoticEvent in trade.Instrument().ExoticEvents():
                    if exoticEvent.Type()=='Average price':
                        #print leg
                        baseInsr  = BaseCommReset(trade, exoticEvent, leg)
                        flag = baseInsr._correspondingCashFlow()._resetFlag()
                        if flag =='Y':
                            report._writeResetRow(baseInsr)
                            checksum = checksum + baseInsr._resetValue()
                            count = count + 1
            else:
                #print 'Here ..... 4'
                cashSourceId = 0
                if trade.Instrument().SettlementType() == 'Physical Delivery':
                    cashSourceId = 1
                    
                baseInsr  = BaseCommReset(trade, None, cashSourceId)
                fields  = ['030',
                baseInsr._sourceTradeID(),
                baseInsr._sourceLegID(),
                baseInsr._sourceCashID(),
                baseInsr._sourceResetID(),
                baseInsr._resetType(),
                baseInsr._resetValue(),
                baseInsr._resetDate(),
                baseInsr._notional(),
                baseInsr._rfisDate()]
                #print fields
                report._writeResetRow(baseInsr)
                checksum = checksum + baseInsr._resetValue()
                count = count + 1
                
        elif trade.Instrument().InsType() == 'Future/Forward':
            if ((trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Agri')):
            
                for i in range(0, 2):
                    
                    baseInsr = BaseCommReset(trade, None, i)
                    flag = baseInsr._correspondingCashFlow()._resetFlag()
                    if flag =='Y':
                            
                        checksum = checksum + baseInsr._resetValue()
                        report._writeResetRow(baseInsr)
                        count = count +1
                    
            
        elif trade.Instrument().InsType() == 'Curr': 
            if ((trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Agri')):
            
                for i in range(0, 2):
                    
                    baseInsr = BaseCommReset(trade, None, i)
                    flag = baseInsr._correspondingCashFlow()._resetFlag()
                    if flag =='Y':
                            
                        checksum = checksum + baseInsr._resetValue()
                        report._writeResetRow(baseInsr)
                        count = count +1
                        
       
        
            
    swapDict  = writePriceSwapsResets(file)
    count = count + swapDict.get('counter')
    checksum = checksum + swapDict.get('checksum')
    
   
    checksum ="%.2f" %checksum
    report._writeFooter(count, checksum)
    
    file.close()
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + str(filePath)+get_filename()


        

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

