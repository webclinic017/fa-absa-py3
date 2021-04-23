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
        return 0
    
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
       
        
    
class OptionCashFlow(BaseCashFlow):

        def __init__(self, trade, payment,):
            BaseCashFlow.__init__(self, trade, payment)
        
        #dc added the next small block
        def _cashFlowSourceId(self):
            id = 0
            return id 
            
        def _interestStartDate(self):
            date = date_from_timestamp(self.trade.CreateTime())
            if (self._cashFlowType()=='Premium'):
                date = maturitydate_from_timestamp(self.trade.ValueDay())
            return date
            
        def _interestEndDate(self):
            date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
            if (self._cashFlowType()=='Premium'):
                date = maturitydate_from_timestamp(self.trade.ValueDay())
            return date
                            
        def _fixingDate(self):
            date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
            if (self._cashFlowType()=='Premium'):
                date = maturitydate_from_timestamp(self.trade.ValueDay())
            return date
            
                            
        def _cashFlowType(self):
            #type = 'Interest'
            if self.leg == 1: 
                type = 'Premium'
            else:
                type = 'Interest'
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                    if self.instrument.SettlementType() =='Cash':
                        if self.leg == 1: 
                            type = 'Premium'
                        else:
                            type = 'Interest'
                            
                    elif self.instrument.SettlementType() =='Physical Delivery':
                        if self.leg ==0:
                            type = 'Exercise'
                        elif self.leg ==1:
                            type = 'Option Delivery'
                            
                        else:
                            type = 'Premium'

            return type
           
        def _origCashFlowCurrency(self):
            curr  = self.trade.Currency().Name()
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                        if self.instrument.SettlementType() =='Physical Delivery':
                            if self.leg ==1:
                                curr = self.instrument.Underlying().Currency().Name()
                
            return curr
            
        def _interestRate(self):
            rate = self.trade.Price()
            if rate == 0:
                rate = self._floatLegRate()
                if (math.isnan(rate) or (rate ==0)):
                    rate = 1
                    
            return rate
            
        def _rateStatus(self):
            status =  'Float'
            if (self._cashFlowType()=='Premium'): 
                status =  'Fixed'
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                    if self.instrument.SettlementType() =='Cash':
                        if self.leg == 1: 
                            status =  'Fixed'
                    elif self.instrument.SettlementType() =='Physical Delivery':
                        if self.leg == 2: 
                            status =  'Fixed'
            return status
            
        def _cashFlowAmount(self):
        
            amount = 0;

            if (self._cashFlowType()=='Premium'):
                amount = self.trade.Premium()
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                    
                if self.instrument.SettlementType() =='Cash':
                    if self.leg == 1:
                        amount = self.trade.Premium()
                    
                    
                elif self.instrument.SettlementType() =='Physical Delivery':
                    if self.leg ==1 or self.leg == 2:
                        amount = self.trade.Premium()
                        
                    else:
                        amount = self.instrument.ContractSize()*self.trade.Quantity()
   
            return amount
            
        def	_cashFlowDate(self):
            date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
            if (self._cashFlowType()=='Premium'):
                date = maturitydate_from_timestamp(self.trade.ValueDay())
                
            return date
                            
        def _cashFlowFlag(self):
            flag =  'P'
            if (self._cashFlowType()=='Premium'):
                flag =  'A'
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                if self.instrument.SettlementType() =='Cash':
                    if self.leg == 1:
                        flag =  'A'
                if self.instrument.SettlementType() =='Physical Delivery':
                    if self.leg == 2: 
                        flag = 'A'
            return flag
                        
        def _physicalAmount(self):
            amount =  ''
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                if self.instrument.SettlementType() =='Physical Delivery':
                    if self.leg ==1:
                        amount = self.instrument.ContractSize()*self.trade.Quantity()
            return amount
            
        def _resetFlag(self):
            flag =  ''
            '''if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')
                    and (self.trade.Instrument().IsAsian()==False)):
                    if self.instrument.SettlementType() =='Cash':
                        if self.leg ==1:
                            flag = ''
                    elif self.instrument.SettlementType() =='Physical Delivery':
                        if self.leg ==2:
                            flag = '''
            if (self._cashFlowType()=='Option Delivery') or (self._cashFlowType()=='Interest'):
                flag = 'Y'
                
            return flag
                            
        def _optionStartEndFixedDate(self):
            date = maturitydate_from_timestamp(self.trade.ValueDay())
            if (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal' or self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal') and self.trade.Instrument().IsAsian()== False:
                    if self.instrument.SettlementType() =='Cash':
                        if self.leg == 0:
                            date = maturitydate_from_timestamp(self.trade.ValueDay())
                        else:
                            date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
                            
                    elif self.instrument.SettlementType() =='Physical Delivery':
                        if self.leg ==0:
                            date = maturitydate_from_timestamp(self.trade.ValueDay())
                        else:
                            date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
                            
            return date
            
        def _floatLegRate(self):
            rate = self.instrument.Underlying().Calculation(). MarkToMarketPrice(calc_space, today, self.trade.Instrument().Currency())
            return rate.Value().Number()
            
            
            
          
            
                        
class FutureFowardCashFlow(BaseCashFlow):

    def __init__(self, trade, payment):
        BaseCashFlow.__init__(self, trade, payment)
        
    def	_cashFlowType(self):
        type = 'Interest'
        self.instrument.AdditionalInfo()
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            type = 'Metal Outright'
            if self.leg == 0:
                type = 'Physical Fwd Proceeds'
            else:
                type = 'Physical Flow'
       
        return type        
        
    def _origCashFlowCurrency(self):
        curr  = self.trade.Currency().Name()
        
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            if self.leg == 1:
                curr = self._currencyDictionary(self.instrument.Underlying().Name())
                
                #curr = self.instrument.Underlying().Currency().Name()
        
        return curr
        
    def _interestRate(self):
        rate = self.trade.Price()*self.trade.Instrument().Quotation().QuotationFactor()
        if rate == 0:
            rate = 1
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            if self.leg == 1:
                    rate = ''
                    
        elif  ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            if self.leg == 1:
                    rate = self._floatLegRate()
                    if (math.isnan(rate) or (rate ==0)) :
                        rate = 1
        
        return rate
        
        
    def _floatLegRate(self):
        rate = self.instrument.Underlying().Calculation(). MarkToMarketPrice(calc_space, today, self.trade.Instrument().Currency())
        return rate.Value().Number()
        
    def	_physicalAmount(self):
        amount =  ''
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            if self.instrument.SettlementType() =='Physical Delivery':
                if self.leg ==1:
                    amount = self._totalTradeAmount()
            return amount
            
        
        
    def	_legSourceId(self):
        leg = self.leg 
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            leg = 0
        return leg
        
    def	_rateStatus(self):
        status = 'Fixed'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            if self.leg ==1:
                status = 'Float'
        return status
        
    def _resetFlag(self):
        flag =  ''
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            if self.leg ==1:
                flag = 'Y'
        return flag
        
    def _cashFlowFlag(self):
        flag =  'A'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):

            if self.leg == 1:
                flag = 'P'
        return flag
        
    def	_cashFlowDate(self):
        date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            date = maturitydate_from_timestamp(self.instrument.SettlementDate())
            
        return date
        
    def	_fixingDate(self):
        return datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        
    def	_interestEndDate(self):
        return datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        
    def _notional(self):
        notional = abs(self._totalTradeAmount())
        #notional = abs(self.trade.Nominal()*self.trade.Quantity())
        #print 'self.trade.Nominal()',self.trade.Nominal(),self.trade.Quantity()
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            if self.trade.Quantity() > 0:
                if self.leg ==0:
                    notional = notional*(-1)
            elif self.trade.Quantity() < 0:
                if self.leg ==1: 
                    notional = notional*(-1)
                    
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            if self.trade.Quantity() > 0:
                if self.leg ==0:
                    notional = notional*(-1)
            elif self.trade.Quantity() < 0:
                if self.leg ==1: 
                    notional = notional*(-1) 
                  
        return notional
        
    def _cashFlowAmount(self):
        amount = abs(self._totalTradeAmount())
        
        #
        #if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
        #    or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
        #    if self.trade.Quantity() > 0:
        #        if self.leg ==0:
        #            amount = abs(self.trade.Price())*amount*(-1)*self.trade.Instrument().Quotation().QuotationFactor()
        #        else:
        #            amount = abs(self.trade.Price())*amount*self.trade.Instrument().Quotation().QuotationFactor()
        #    elif self.trade.Quantity() < 0:        
        #        if self.leg ==1: 
        #            amount = amount*(-1)
                    
        
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            self.instrument.AdditionalInfo()
            if self.leg == 0:
                if self.trade.Quantity() > 0:
                    amount = abs(self.trade.Price())*amount*(-1)*self.trade.Instrument().Quotation().QuotationFactor()
                else:
                    amount = abs(self.trade.Price())*amount*self.trade.Instrument().Quotation().QuotationFactor()
                
            else:
                if self.trade.Quantity() < 0:        
                    amount = amount*(-1)      
         
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
                
            amount = abs(amount)
            if self.leg ==0:
                if self.trade.Quantity() > 0:
                    amount = abs(self.trade.Price())*amount*(-1)*self.trade.Instrument().Quotation().QuotationFactor()#Times quatation factor (self.trade.Instrument().Quotation().QuotationFactor())
                else:
                    amount = abs(self.trade.Price())*amount*self.trade.Instrument().Quotation().QuotationFactor()#Times quatation factor (self.trade.Instrument().Quotation().QuotationFactor())
            elif self.leg ==1:
                if self.trade.Quantity() < 0:
                    amount = amount*(-1)
        return amount
        
          
   #add currency stuff here                     
class CurrencyCashflow(BaseCashFlow):

    def __init__(self, trade, payment):
        BaseCashFlow.__init__(self, trade, payment)
        
    def	_cashFlowType(self):
        #type = 'Interest'
        #self.instrument.AdditionalInfo()
        '''if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):'''
        type = 'Metal Outright'
        if self.leg == 0:
            type = 'Physical Fwd Proceeds'
        else:
            type = 'Physical Flow'
       
        return type        
        
    def _origCashFlowCurrency(self):
        curr  = self.trade.Currency().Name()
        
        if self.leg == 1:
            curr = self._currencyDictionary(self.instrument.Name())
        return curr
        
    def _interestRate(self):
        rate = self.trade.Price()
        if rate == 0:
            rate = 1
        if self.leg == 1:
            rate = ''
                    
        return rate
        
    #need to check this!!!    
    def _floatLegRate(self):
        rate = self.instrument.Underlying().Calculation(). MarkToMarketPrice(calc_space, today, self.trade.Instrument().Currency())
        return rate.Value().Number()
        
    def	_physicalAmount(self):
        amount =  ''

        if self.instrument.SettlementType() =='Physical Delivery':
            if self.leg ==1:
                amount = self.trade.Quantity()
        return amount
        
        
        
    def	_legSourceId(self):
        leg = 0
        return leg
        
    def	_rateStatus(self):
        status = 'Fixed'
        if self.leg ==1:
            status = 'Float'
        return status
        
    def _resetFlag(self):
        flag =  ''

        return flag
        
    def _cashFlowFlag(self):
        flag =  'A'

        return flag
        
    def	_cashFlowDate(self):
        date = datetime.datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y%m%d')
            
        return date
        
    def	_fixingDate(self):
        return datetime.datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y%m%d')
        
    def	_interestEndDate(self):
        return datetime.datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y%m%d')
        #check
    def _notional(self):
        notional = abs(self._totalTradeAmount())
                    
        if self.trade.Quantity() > 0:
            if self.leg ==0:
                notional = notional*(-1)*self.trade.Price()
        elif self.trade.Quantity() < 0:
            if self.leg ==1: 
                notional = notional*(-1) 
                  
        return notional
        
    def _cashFlowAmount(self):
        amount = abs(self._totalTradeAmount())
        if self.leg == 0:
            if self.trade.Quantity() > 0:
                amount = abs(self.trade.Price())*amount*(-1)*self.trade.Instrument().Quotation().QuotationFactor()
            else:
                amount = abs(self.trade.Price())*amount*self.trade.Instrument().Quotation().QuotationFactor()
            
        else:
            if self.trade.Quantity() < 0:        
                amount = amount*(-1)      
        return amount
        
        
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
            
          
        
        

class EagleCommCashFlowReport:
    def __init__(self, file):
        self.file  = file

    def _fieldNames(self):
        fieldNames = ['010',
        'SOURCE_TRADE_ID',
        'ENTRY_DATE_TIME',
        'LEG_SOURCE_ID',
        'CASHFLOW_SOURCE_ID',
        'INTEREST_START_DATE',
        'INTEREST_END_DATE',
        'FIXING_DATE',
        'CASHFLOW_TYPE',
        'ORIG_CASHFLOW_CURRENCY',
        'INTEREST_RATE',
        'RATE_STATUS',
        'SPREAD',
        'NOTIONAL',
        'CASHFLOW_AMOUNT',
        'CASHFLOW_DATE',
        'CASHFLOW_FLAG',
        'CASHFLOW_DAYS',
        'CASHFLOW_BUSINESS_DAYS',
        'VOLATILITY',
        'PHYSICAL_AMOUNT',
        'RESETS_FLAG',
        'INVOICE_NUMBER',
        'VAT_CODE',
        'VAT_AMOUNT']
        
        return fieldNames
    
    def _writeHeader(self):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fields = ['010', 'JHB', datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%Y%m%d')]
        writer.writerow(fields)
        
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter='|', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        finally:
            #self.file.close()
            print ''
            
    def _writeCashFlowRow(self, baseCashFlow):
        fields = ['030',
            baseCashFlow._sourceTradeId(),	
            baseCashFlow._entryDateTime(),	
            baseCashFlow._legSourceId(),	
            baseCashFlow._cashFlowSourceId(),	
            baseCashFlow._interestStartDate(),	
            baseCashFlow._interestEndDate(),
            baseCashFlow._fixingDate(),	
            baseCashFlow._cashFlowType(),	
            baseCashFlow._origCashFlowCurrency(),	
            baseCashFlow._interestRate(),	
            baseCashFlow._rateStatus(),	
            baseCashFlow._spread(),	
            baseCashFlow._notional(),	
            baseCashFlow._cashFlowAmount(),	
            baseCashFlow._cashFlowDate(),	
            baseCashFlow._cashFlowFlag(),	
            baseCashFlow._cashFlowDays(),	
            baseCashFlow._cashFlowBusinessDays(),	
            baseCashFlow._vilatility(),	
            baseCashFlow._physicalAmount(),	
            baseCashFlow._resetFlag	(),
            baseCashFlow._invoiceNumber(),	
            baseCashFlow._vatCode(),
            baseCashFlow._vatAmount()]
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _writeFooter(self, count, checksum):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['090', count, checksum])
        


        
ael_variables = FBDPGui.DefaultVariables(['filePath', 'File Path', directorySelection, None, directorySelection, 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1]
)

def get_filename():
    """Return the dump's filename."""
    #date_str = maturitydate_from_timestamp(today)
    return '_'.join(['ABSA_COMM_TDB_CASH']) + '.DAT'
   
def ael_main(ael_dict):

    filePath = ael_dict['filePath']
    output_dir = str(ael_dict['filePath'])
    filename = os.path.join(output_dir, get_filename())

    file = open(str(filename), 'wb') 
    
    #trade  = acm.FTrade[21811415]
    #all_trades = [trade]
    
    report = EagleCommCashFlowReport(file)
    report._writeHeader()
    report._writeColumnNames()
    checksum = 0
    count = 0
    leg = 0
    
    all_trades = get_trades_data()
    
    for trade in all_trades:
        sourceid=0
        #print 'trade.Instrument().InsType() instttt',trade.Instrument().InsType()
        baseInsr  = BaseCashFlow(trade, leg)
        if trade.Instrument().InsType() == 'Future/Forward':
            sourceid=0
            for leg in range(0, 2):
                baseInsr = FutureFowardCashFlow(trade, sourceid)
                report._writeCashFlowRow(baseInsr)
                checksum = checksum + baseInsr._notional()
                count = count + 1   
                sourceid = sourceid + 1
               
        elif trade.Instrument().InsType() == 'Option':
            sourceid=0
            #print 'trade.Instrument().InsType() == Option'
            #print 'trade.Instrument().SettlementType()',trade.Instrument().SettlementType()
            #print 'trade.Instrument().AdditionalInfo().Commodity_SubAsset()',trade.Instrument().AdditionalInfo().Commodity_SubAsset()
            if (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Base Metal' or trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Precious Metal')  and trade.Instrument().IsAsian()== False:
                
                if trade.Instrument().SettlementType() =='Cash':
                    #print 'trade.Instrument().SettlementType()',trade.Instrument().SettlementType()
                    index = 1
                    if trade.ValueDay()>today:
                        index = 2
                    
                    for leg in range(0, index):
                        baseInsr  = OptionCashFlow(trade, sourceid)
                        report._writeCashFlowRow(baseInsr)
                        checksum = checksum + baseInsr._notional()
                        count = count + 1
                        sourceid = sourceid + 1
                        
                       
                elif trade.Instrument().SettlementType() == 'Physical Delivery':
                    sourceid=0
                    index = 2
                    if trade.ValueDay()>today:
                        index = 3
                    
                    for leg in range(0, index):
                        
                        baseInsr  = OptionCashFlow(trade, sourceid)
                        report._writeCashFlowRow(baseInsr)
                        checksum = checksum + baseInsr._notional()
                        count = count + 1
                        sourceid = sourceid + 1
                        
                        
            else:
                index = 1
                if trade.ValueDay()>today:
                    index = 2
                    
                for leg in range(0, index):
                        baseInsr  = OptionCashFlow(trade, sourceid)
                        report._writeCashFlowRow(baseInsr)
                        checksum = checksum + baseInsr._notional()
                        count = count + 1
                        sourceid = sourceid + 1
            
                
        elif trade.Instrument().InsType() == 'PriceSwap':
            legs = trade.Instrument().Legs()
            for leg in legs:
                cashflows = leg.CashFlows()
                
                for cashflow in cashflows:
                    if (cashflow.PayDate()>trade.ValueDay()):
                        baseInsr  = SwapCashFlow(trade, leg, cashflow)
                        report._writeCashFlowRow(baseInsr)
                        checksum = checksum + baseInsr._notional()
                        count = count + 1
                        sourceid = sourceid + 1
        
        elif trade.Instrument().InsType() == 'FXCash':
            sourceid=0
            for leg in range(0, 2):
                baseInsr = CurrencyCashflow(trade, sourceid)
                report._writeCashFlowRow(baseInsr)
                checksum = checksum + baseInsr._notional()
                count = count + 1   
                sourceid = sourceid + 1
                
        if trade.Instrument().InsType() == 'Curr':
            sourceid=0
            for leg in range(0, 2):
                baseInsr = CurrencyCashflow(trade, sourceid)
                report._writeCashFlowRow(baseInsr)
                checksum = checksum + baseInsr._notional()
                count = count + 1   
                sourceid = sourceid + 1       
        
    
    checksum ="%.2f" %checksum
    report._writeFooter(count, checksum)
    file.close()
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + str(filePath)+get_filename()
    
    
    
    
