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
# NEW cdoe*********
import acm, ael
import csv
import sys
import FBDPGui
import FRunScriptGUI
import datetime
import math
from Eagle_Comm_Absa_Util import _hybridNominalPosition, date_from_timestamp, maturitydate_from_timestamp, get_trades_data, _hybridPrice
import os

directorySelection=FRunScriptGUI.DirectorySelection()
today = acm.Time().DateToday()
calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection() 

rundate = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%Y%m%d')

class BaseCashFlow:
    def __init__(self,trade,leg,cashflow=None):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.leg = leg
        self.cashflow = cashflow
        
    
        
        
    def	_sourceTradeId(self):
        return self.trade.Oid()
        
    def	_entryDateTime(self):
        return date_from_timestamp(self.trade.CreateTime())
        
    def	_legSourceId(self):
        id = 0
        if (self.instrument.InsType() == 'Future/Forward' and ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri'))):
            id = self.leg
                
        return id
        
    def	_cashFlowSourceId(self):
        id = self.leg
        
        if ((self.instrument.InsType() =='Future/Forward') and (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            id = 0
        return id
        
    def	_interestStartDate(self):
        date = date_from_timestamp(self.trade.CreateTime())
        if self.trade.AcquireDay():
            datetime.datetime.strptime(self.trade.AcquireDay(), '%Y-%m-%d').strftime('%Y%m%d')
        return date
    
    def	_interestEndDate(self):
        return maturitydate_from_timestamp(self.trade.ValueDay())
        
    def	_fixingDate(self):
        return maturitydate_from_timestamp(self.trade.ValueDay())
        
    def	_cashFlowType(self):
        type = 'Interest'
        
        if len(self.trade.Payments())>=1:
            for payment in self.trade.Payments(): 
                if payment.CashFlowType() == 'Payment Premium':
                    type = 'Premium'
        return type
        
         
    def	_origCashFlowCurrency(self):
        curr  = self.trade.Currency().Name()
        return curr
        
    def	_interestRate(self):
        return ''
        
    
    def	_rateStatus(self):
        return 'Fixed'
    
    def	_spread(self):
        return ''
    
    
    def _notional(self):
        #print 'self._totalTradeAmount()',self._totalTradeAmount()
        notional = self._totalTradeAmount()
        
                    
        return notional
        
        
    def	_cashFlowAmount(self):
        return self.trade.NetPremium()
        
    def	_cashFlowDate(self):
        date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        return date
    
    def	_cashFlowFlag(self):
        return 'A'
    
    def	_cashFlowDays(self):
        return 1
    
    def	_cashFlowBusinessDays(self):
        return 1
        
    def	_vilatility(self):
        return 0
    
    def	_physicalAmount(self):
        return ''
        
    def	_resetFlag(self):
        return ''
        
        
    def	_invoiceNumber(self):
        return ''
        
    def	_vatCode(self):
        return ''
        
    def	_vatAmount(self):
        return ''
        
    def _totalTradeAmount(self):
        tamount = 0
        contractSize = self.instrument.ContractSize()
        quantity = self.trade.Quantity()
        tamount = quantity * contractSize
        #if self.instrument.InsType() == 'Curr':
        #   tamount = quantity
        return tamount
        
        
    def _buySellIndicator(self):
        indicator = 'BUY'
        if self.trade.Quantity() < 0 :
            indicator = 'SELL'
        return indicator
        
    def _currencyDictionary(self, curr):
        #print self.trade.Oid(),curr
        dict = {}
        dict['USD/GOLD/COMEX']='XAU'
        dict['USD/MAL']='XAH'
        dict['USD/MAL/PHY']='XAH'
        dict['USD/MCU']='XCA'
        dict['USD/MCU/PHY']='XCA'
        dict['USD/MCU/PHY']='XCA'
        dict['USD/MNI']='XNI'
        dict['USD/MNI/PHY']='XNI'
        dict['USD/MPB']='XPB'
        dict['USD/MPB/PHY']='XPB'
        dict['USD/MSN']='XSN'
        dict['USD/MSN/PHY']='XSN'
        dict['USD/MZN']='XZS'
        dict['USD/MZN/PHY']='XZS'
        dict['USD/PLAT/NYMEX']='XPT'
        dict['USD/SILVER/COMEX']='XAG'
        dict['USD/XAG']='XAG'
        dict['USD/XAU']='XAU'
        dict['USD/XPD']='XPD'
        dict['USD/XPT']='XPT'
        dict['USD/XRH']='XRH'
        dict['XAG']='XAG'
        dict['XAU']='XAU'
        dict['XPD']='XPD'
        dict['XPT']='XPT'
        dict['XRH']='XRH'
        dict['XZN']='XZS'
        dict['ZAR/GOLD/SAFEX']='XAU'
        dict['ZAR/PLAT/SAFEX']='XPT'
        dict['ZAR/SILV/SAFEX']='XAG'
        dict['ZAR/XAG']='XAG'
        dict['ZAR/XAU']='XAU'
        dict['ZAR/XPD']='XPD'
        dict['ZAR/XPT']='XPT' 
        dict['ZAR/GLD']='XAU' 
        
        if dict.has_key(curr):      
            return dict[curr]
        else:
            return ''
       
        
class SwapCashFlow(BaseCashFlow):
    def __init__(self, trade, leg, cashflow):
        BaseCashFlow.__init__(self, trade, leg, cashflow)
        
    def _legSourceId(self):
        return self.leg.Oid()
        
    def _cashFlowSourceId(self):
        return self.cashflow.Oid()
        
    def	_interestStartDate(self):
        return datetime.datetime.strptime(self.cashflow.StartDate(), '%Y-%m-%d').strftime('%Y%m%d')
    def	_interestEndDate(self):
        return datetime.datetime.strptime(self.cashflow.EndDate(), '%Y-%m-%d').strftime('%Y%m%d')
    def	_fixingDate(self):
        if self.leg.LegType =='Fixed':
            return '19000101'
        else:
            return datetime.datetime.strptime(self.cashflow.EndDate(), '%Y-%m-%d').strftime('%Y%m%d')
        
    def _origCashFlowCurrency(self):
        return self.leg.Currency().Name()
        
    def	_interestRate(self):
        if self.leg.LegType() =='Fixed':
            return self.cashflow.FixedRate()
        else:
            return self.hybridPrice()
            
    '''def _forwardRate(self):
        forwardRate = self.cashflow.Calculation().ForwardRate(acm.Calculations().CreateStandardCalculationsSpaceCollection())
        if forwardRate == None:
            forwardRate = 0
        return  forwardRate'''
    def hybridPrice(self):
        price = _hybridPrice(self.cashflow)
        if price == None:
            price = 0
        return price
    
    def	_rateStatus(self):
        if self.leg.LegType() =='Fixed':
            return 'Fixed'
        else:
            if self.cashflow.EndDate() < today:
                return 'Float-Fixed'
            else:
                return 'Float'
    
    def _notional(self): 
        
        
        notional = abs(_hybridNominalPosition(self.cashflow)*self.trade.Quantity())
              
        
        if self.trade.Quantity()> 0 and self.leg.PayLeg() :
            notional = notional*(-1)
        elif self.trade.Quantity() < 0 and self.leg.PayLeg()==False:
            notional = notional*(-1)
            
        return notional
        
    def	_cashFlowAmount(self):
        #print type(self._interestRate()),type(self._notional()),self.trade.Oid()
        if ((self._interestRate() != None) or (self._notional() != None)):
           
            return self._notional()*self._interestRate()
        else:
            return 0
    
    def _cashFlowDate(self):
        return maturitydate_from_timestamp(self.cashflow.PayDate())

    def	_cashFlowFlag(self):
        if self._rateStatus()=='Float':
            return 'P'
        else:
            return 'A'
            
    def	_cashFlowDays(self):
        return ael.date(self.cashflow.StartDate()).days_between(ael.date(self.cashflow.EndDate()))  
    
    def	_cashFlowBusinessDays(self):
        return ael.date(self.cashflow.StartDate()).days_between(ael.date(self.cashflow.EndDate()))  
 
    def	_resetFlag(self):
        if self.leg.LegType() =='Float':
            return 'Y'
        else:
            return ''
            
    def	_spread(self):
        return self.leg.Spread()         
          
        
     
    def _isValidCF(self, cf):
        val=0
	if cf.CashFlowType()=='Dividend' and self.leg.Oid()==cf.Leg().Oid():
                val=val+1
        return val       

class EagleEquitiesCashFlowReport:
    def __init__(self, file):
        self.file  = file

    def _fieldNames(self):
        fieldNames = ['010',
        'TRADE_ID',
        'LEG_NUMBER',
        'CASHFLOW_NUMBER',
        'CASHFLOW_TYPE',
        'CASHFLOW_DATE',
        'INTEREST_START_DATE',
        'INTEREST_END_DATE',
        'NOTIONAL',
        'CASHFLOW_CURRENCY',
        'SPREAD',
        'FIXING_DATE']
        
        return fieldNames
    
    def _writeHeader(self):
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        fields = ['010', 'JHB', rundate]
        writer.writerow(fields)
        
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter=',', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        finally:
            #self.file.close()
            print ''
            
    def _writeCashFlowRow(self, baseCashFlow):
        fields = ['030',
            baseCashFlow._sourceTradeId(),	
            baseCashFlow._legSourceId(),	
            baseCashFlow._cashFlowSourceId(),	
            baseCashFlow._cashFlowType(), 
            baseCashFlow._cashFlowDate(),
            baseCashFlow._interestStartDate(),
            baseCashFlow._interestEndDate(),
            baseCashFlow._notional(),	
            baseCashFlow._origCashFlowCurrency(),
            baseCashFlow._spread(),
            baseCashFlow._fixingDate()]
            
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _writeFooter(self, count, checksum):
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['090', count, checksum])
        


        
ael_variables = [
['tradeFilter', 'Trade Filters', 'FTradeSelection', acm.FTradeSelection.Select(''), 'Eagle_Equities_DerivsV3', 1, 1],
['filePath', 'File Path', 'string', None, '/services/frontnt/Task/', 0],
['fileName', 'File Name', 'string', None, 'ABSA_EQT_TDB_CASH_'+rundate+ '.DAT', 0],]


def get_filename():
    """Return the dump's filename."""
    #date_str = maturitydate_from_timestamp(today)
    return '_'.join(['ABSA_COMM_TDB_CASH_']) +'.DAT'
   
def ael_main(parameters):

    filename = parameters['filePath'] + parameters['fileName']

    tfname = parameters['tradeFilter'][0]
    
    file = open(str(filename), 'wb') 
    
    
    #trade  = acm.FTrade[21811415]
    #all_trades = [trade]
    
    report = EagleEquitiesCashFlowReport(file)
    report._writeHeader()
    report._writeColumnNames()
    checksum = 0
    count = 0
    leg = 0
    
    
    for trade in tfname.Trades():
        sourceid=0
        #print 'trade.Instrument().InsType() instttt',trade.Instrument().InsType()
        baseInsr  = BaseCashFlow(trade, leg)
        
        if (trade.Instrument().InsType() == 'TotalReturnSwap' and trade.Instrument().IndexReference()):
            if trade.Instrument().IndexReference().InsType()=='EquityIndex' or trade.Instrument().IndexReference().InsType()=='Stock':
                legs = trade.Instrument().Legs()
                for leg in legs:
                    cashflows = leg.CashFlows()
                    
                    for cashflow in cashflows:
                        if (cashflow.PayDate()>trade.ValueDay()):
                            baseInsr  = SwapCashFlow(trade, leg, cashflow)
                            if baseInsr._isValidCF(cashflow)==0:
                                report._writeCashFlowRow(baseInsr)
                                checksum = checksum + baseInsr._notional()
                                count = count + 1
                                sourceid = sourceid + 1
    
    checksum ="%.2f" %checksum
    report._writeFooter(count, checksum)
    file.close()
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + filename
    
    
    
    
