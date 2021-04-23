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
    2014-04-02  CHNG0001698152  Heinrich Cronje         Production issue fix. First check if the original trade exist
                                                        before retreiving the instrument. Also, does not seem that the
                                                        original trade's details are not being used. This script needs
                                                        be relooked and optimized where possible.
----------------------------------------------------------------------------------------------------------------'''

import acm
import csv
import sys
import FBDPGui
import FRunScriptGUI
import datetime
import math
from Eagle_Commodity import InsAsian
from Eagle_Comm_Absa_Util import _convertTodDays, get_trades_data, date_from_timestamp, maturitydate_from_timestamp
import os

directorySelection=FRunScriptGUI.DirectorySelection()
today = acm.Time().DateToday()

class BaseInstrTrade:
    def __init__(self, trade, leg):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.underlying = self.instrument.Underlying()
        self.originalTrade = trade.Contract()
        self.originalInstrument = None
        if self.originalTrade:
            self.originalInstrument = self.originalTrade.Instrument()
        self.leg = leg
        
    def _tradeId(self):
        #print 'tradeIdTye: ' + str(type(self.trade.Oid()))
        return self.trade.Oid()
    
    def _inputDate(self):
    
        return date_from_timestamp(self.trade.CreateTime())
    
    def _tradeReference(self):
        return self.trade.Oid()
        
    def _internalTradeLinkID(self):
        return ''
        
    def _internalTradeType(self):
        return self.instrument.InsType()
        
    def _tradeEvent(self):
        return 'N'
        
    def _tradeDate(self):
        return date_from_timestamp(self.trade.TradeTime())
        
    def _tradeTime(self):
        return date_from_timestamp(self.trade.TradeTime())
        
    def _effectiveDate(self):
        return maturitydate_from_timestamp(self.trade.ValueDay())
        
    def _maturityDate(self):
        return maturitydate_from_timestamp(self.trade.maturity_date())
        
    def _principalID(self):
        return 10250696
        
    def _tradePortfolio(self):
        #print 'portfolioType: ' + str(type(self.trade.Portfolio()))
        name = ''
        if self.trade.Portfolio()!= None:
            name = self.trade.Portfolio().Name()[:14]
            
        return name
        
    def _tradeArea(self):
        return self.trade.AcquirerId()
        
    def _counterPartyId(self):
        #return self.trade.Counterparty().Name()
        addtionalInfo = self.trade.Counterparty().AdditionalInfo()
        counterpartyID = addtionalInfo.BarCap_Eagle_SDSID()
        #if self.name == 'Barclays Bank PLC':
        # counterpartyID  = '40780564'
        return counterpartyID
    def _traderID(self):
        return self.trade.TraderId()
    
    def _executionBroker(self):
        return self.trade.Broker()
        
    def _instrumentType(self):
        return self.instrument.InsType()
        
    def _instrumentDescription(self):
        return ''
        
    def _buySellIndicator(self):
        indicator = 'BUY'
        if self.trade.Quantity() < 0 :
            indicator = 'SELL'
        return indicator
        
    def _exchangeID(self):
        return ''
        
    def _executionBrokerRate(self):
        return ''
    
    def _reference(self):
        return ''
        
    def _legNumber(self):
        return 0
        
    def _legStartDate(self):
        #datetime.datetime.strptime(self.instrument.ExpiryDate(),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        #self.trade.AcquireDay()
        mystartdate = datetime.datetime.strptime(self.trade.AcquireDay(), '%Y-%m-%d').strftime('%Y%m%d')
        if self.instrument.InsType() == 'Curr':
            mystartdate = datetime.datetime.strptime(self.trade.TradeTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        return mystartdate
        
    def _settlementDate(self):
        #To Do : Double check logic

        date = datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        if self.instrument.InsType() == 'Curr':
            date = datetime.datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y%m%d')       
        return date
        
    def _legMaturityDate(self):
        date = datetime.datetime.strptime(self.instrument.ActualExpiryDay(), '%Y-%m-%d').strftime('%Y%m%d')
        if self.instrument.InsType() == 'Curr':
            date = datetime.datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y%m%d')
        return date
        
    def _indexCommodityCode(self):
        return self.instrument.AdditionalInfo().Commodity_Label()
     
    def _indexCommodityDescription(self):
        return self.instrument.AdditionalInfo().Commodity_Desc()
        
    def _unitOfMeasurement(self):
        return self.instrument.AdditionalInfo().Openlink_Unit()
        
        
    def _settlementType(self):
        type = ''
        if self.instrument.SettlementType() =='Cash':
            type = 'Cash'
        elif self.instrument.SettlementType() == 'Physical Delivery':
            type = 'Physical'
        return type
        
    def _deliveryType(self):
        type = self.instrument.AdditionalInfo().Commodity_Deli()
        if type is None:
            if self.instrument.SettlementType() =='Cash':
                type = 'Cash'
            elif self.instrument.SettlementType() == 'Physical Delivery':
                type = 'Physical'
        return type
        
    def _settlementCurrency(self):
        curr  = self.trade.Currency().Name()
        # To Do : if phisical get currency of the phyisical
        return curr
        
    def _totalTradeAmount(self):
        contractSize = self.instrument.ContractSize()
        quantity = self.trade.Quantity()
        #To Do : where quantity on the leg should take into account whether we are receiving or paying the amount
        return abs(quantity * contractSize)
        
        
        
    def _totalAmountCalculationPeriod(self):
        return 1
        
    def _counterCurrency(self):
        return ''
        
    def _counterAmount(self):
        return ''
        
    def _optionType(self):
        optionType = ''
        if self.instrument.InsType() == 'Option' :
            if  self.instrument.IsCall():
                optionType = 'CALL' 
            else:
                optionType ='PUT'
        
        return optionType
        
    def _optionStype(self):
        optionStyle = ''
        
        if self.instrument.InsType() == 'Option':
            
            if self.instrument.ExerciseType() == 'American':
                optionStyle = 'American'
            elif self.instrument.ExerciseType() == 'Bermudan':
                optionStyle = 'Bermudan'
            elif self.instrument.ExerciseType() == 'European':
                 optionStyle = 'European'
                
       
        return optionStyle
        
    def _valuationModel(self):
        return ''
        
    def _strikePrice(self):
        price = ''
        if self.instrument.InsType() == 'Option':
            price = self.instrument.StrikePrice()
        return price
        
    def _numberOfLots(self):
        return 0
        
    def _tradePrice(self):
        return self.trade.Price()
        
    def _fixedFloatingIndicator(self):
       return 'Fixed'
        
    def _fixedLegRate(self):
        rate = self.trade.Price()
        if self.instrument.InsType() == 'Option':
            rate = self.instrument.StrikePrice()
        return rate
        
    def _floatingSpread(self):
        return 0
        
    def _compoundingType(self):
        return 0
        
    def _projectionIndexTenor(self):
        return 0
    
    def _legYieldBasis(self):
        return 'None'
        
    def _payReceiveFlag(self):
        return 'Receive'
        
    def _compoundingPeriod(self):
        return 0
        
    def _paymentPeriod(self):
        return 1 
        
    def _paymentDateOffset(self):
        return self.instrument.PayDayOffset()
        
    def _pricingContract(self):
        return 1
        
    def _resetDateRoll(self):
        return 0
        
    def _resetOffSet(self):
        return 0
        
    def _pricingOnLastTrading(self):
        return 0
        
    def _dailyVolumeTrading(self):
        return 0
        
    def _indexPricingConvention(self):
        return ''
    
    def _resetPeriod(self):
        return 0
    
    def _averagePeriod(self):
        return 1
        
    def _roundingRule(self):
        return 4
        
    def _discountIndex(self):
        indexString = self._indexDictionary(self.trade.Currency().Name())
        return indexString
        
    def _tradePortfolioName(self):
        return self.trade.PortfolioId()
        
        
    def _OrigCounterPartyName(self):
        name = self.trade.Counterparty().Name()
        #if name == 'Barclays Bank PLC':
        #name = 'BARBCO ONE LIMITED'
        return name
        
    def _exchangeName(self):
        return ''
        
    def _cashFlowType(self):
        return ''
        
    def _lifeToDateOffset(self):
        return 0
        
    def _resetConvention(self):
        return ''
        
    def _rollConvention(self):
        return 'Normal'
        
    def _packageId(self):
        return ''
        
    def _packageComponentTradeCount(self):
        return ''
        
    def _breakDate(self):
        return ''
        
    def _ultimatePackageId(self):
        return ''
        
    def _exchangeFlag(self):
        return 0
    
    def _marketName(self):
        return 'OTC'
        
    def _spanMarginingFlag(self):
        return 0
        
    def _projIndexGroupId (self):
        return 4 
        
    def _vatCode(self):
        return ''
        
    
    def _legalHierachy(self):
        # To Do : use additional Info from instruments to extract the value
        return  ''
        
    def _instrumentClass(self):
        return 0
        
    def _powerProduct(self):
        return ''
        
    def _buyOutDate(self):
        return ''
        
    def _agreementType(self):
        return ''
        
    def _deliveryStartDate(self):
        return ''
        
    def _deliveryEndDate(self):
        return ''
    
    def _deliveryLocation(self):
        return ''
        
    def _optionNoteIndicator(self):
        return ''
        
    def _intervalType(self):
        return ''
        
    def _documentType(self):
        return ''
        
    def _heatRate(self):
        return ''
        
    def _collateralExclusion(self):
        return 'No'
    
    def _dailyVolume(self):
        return ''
        
    def _libraID(self):
        return ''
        
    def _underlyingInstType(self):
        return ''
        
    def _independentAMT(self):
        return ''
        
    def _salesPersonID(self):
        if self.trade.SalesPerson() is not None:
            self.trade.SalesPerson().Oid()
           
        
    def _indexSupGroupId(self):
        return 'None'
        
    def _referenceRateUOM(self):
        return ''
        
    def _unitConvFactor(self):
        return ''
        
    def _indexMultiplier(self):
        return 1
        
    def _counterPartyType(self):
        return 'CLIENT'
        
    def _ransysAnalysisProcessed(self):
        return 'N'
        
    def _exchangeProductCode(self):
        return ''
        
    def _contractSize(self):
        return self.instrument.ContractSize()
        
    def _clientOrHouse(self):
        return 'HOUSE'
        
        
    def _indexDictionary(self, curr):
        dict = {}
        dict['DKK'] = 'CIBOR.DKK'
        dict['MYR'] = 'KLIBOR.MYR'
        dict['AUD'] = 'LIBOR.AUD'
        dict['CAD'] = 'LIBOR.CAD'
        dict['CHF'] = 'LIBOR.CHF'
        dict['EUR'] = 'LIBOR.EUR'
        dict['GBP'] = 'LIBOR.GBP'
        dict['JPY'] = 'LIBOR.JPY'
        dict['NOK'] = 'LIBOR.NOK'
        dict['NZD'] = 'LIBOR.NZD'
        dict['SEK'] = 'LIBOR.SEK'
        dict['TRY'] = 'LIBOR.TRY'
        dict['USD'] = 'LIBOR.USD'
        dict['ZAR'] = 'LIBOR.ZAR'
        dict['PLN'] = 'WIBOR.PLN'
        dict['XPT'] = 'LIBOR.USD'
        
        try:
            return dict[curr]
        except Exception, e:
            print 'ERROR: Currency %s is not catered for.' %curr
            return ''
                              
class OptionInstrTrade(BaseInstrTrade):
    def __init__(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)
        
    def _instrumentType(self):
        type = self.instrument.InsType()
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            type = 'EO-PUT'
            if self.instrument.IsCall():
                type = 'EO-CALL'
                  
        elif ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            type = 'MTL-MO-PUT'
            if self.instrument.IsCall():
                type = 'MTL-MO-CALL'
        return type
    
            
    def _instrumentDescription(self):
        desc = ''
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            desc = 'Asian Price Energy Call Option'
            
        elif ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            desc = 'Metal Average Price Call'
        return desc
        
    def _valuationModel(self):
        model = 'B-S'
        if self.trade.Instrument().IsAsian():
            model = 'Vorst'
        return model
        
    def _cashFlowType(self):
        return 'upfront'
        
    def _fixedFloatingIndicator(self):
        return 'Float'
        
   
    def _projIndexGroupId (self):
        indexGroupId = 4
        if self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal':
            indexGroupId = 3
        elif self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal':
            indexGroupId = 2
            
        return indexGroupId 
   
        
    def _settlementType(self):
        type = 'Cash'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            if self.instrument.SettlementType() =='Cash':
                type = 'Cash'
            elif self.instrument.SettlementType() == 'Physical Delivery':
                type = 'Physical'
        return type
        
        
        
class SwapInstrTrade(BaseInstrTrade):
    def __init__(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)
        
    def _instrumentType(self):
        type = self.instrument.InsType()
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            type = 'ENGY-SWAP'
                  
        elif ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            type = 'MTL-SWAP'
        return type
        
    def _instrumentDescription(self):
        type = self.instrument.InsType()
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            desc = 'Energy Swap'
                  
        elif ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            desc = 'Metal Swap'
        return desc
        
    def _legNumber(self):
        return self.leg.Oid()
        
    def _settlementType(self):
        return 'Cash'
        
    def _deliveryType(self):
        return 'Cash'
        
    def _totalTradeAmount(self):
        contractSize = self.instrument.ContractSize()
        quantity = self.trade.Quantity()
        amount = abs(quantity * contractSize)
        if quantity > 0 and self.leg.PayLeg() :
            amount = amount*(-1)
        elif quantity < 0 and self.leg.PayLeg()==False:
            amount = amount*(-1)
        return amount
        
    def _totalAmountCalculationPeriod(self):
        #print self.leg.LegType()
        if self.leg.LegType() == 'Fixed':
            return 0
        else:
            #print 'whats this?',self.leg.RollingPeriodUnit()
            return _convertTodDays(self.leg.RollingPeriodUnit())*self.leg.RollingPeriodCount() 
            
    def _tradePrice(self):
        price = 0
        legs = self.instrument.Legs()
        for leg in legs:
            if leg.LegType()=='Fixed':
                price = leg.FixedRate()
        return price
        
    def _fixedFloatingIndicator(self):
       return self.leg.LegType()
       
    def _fixedLegRate(self):
        rate = 0
        if self.leg.LegType()=='Fixed':
            rate = self.leg.FixedRate()
        return rate
        
    def _payReceiveFlag(self):
        if self._totalTradeAmount()>0:
            return 'Receive'
        else:
            return 'Pay'
    def _compoundingPeriod(self):
        return self._totalAmountCalculationPeriod()
        
    def _paymentPeriod(self):
        return self._totalAmountCalculationPeriod() 
        
    def _paymentDateOffset(self):
        return _convertTodDays(self.leg.PayOffsetUnit)*self.leg.PayOffsetCount() 
        
    def _resetDateRoll(self):
        
        return datetime.datetime.strptime(self.leg.RollingPeriodBase(), '%Y-%m-%d').strftime('%d')  
    
    def _resetPeriod(self):
        return self._totalAmountCalculationPeriod()
        
    def _averagePeriod(self):
        return self._totalAmountCalculationPeriod()
        
    def _resetConvention(self):
        return 'Normal'
        
    def _rollConvention(self):
        return 'Month End'
        
    def _marketName(self):
        return 'OTC'
        
    def _projIndexGroupId (self):
        indexGroupId = 4
        if self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal':
            indexGroupId = 3
        elif self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal':
            indexGroupId = 2
        return indexGroupId
        
    
        
class FutureForwardInstrTrade(BaseInstrTrade):
    def _init_(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)
        
    def _instrumentType(self):
        
        type = self.instrument.InsType()
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            type = 'ENGY-SWAP'
            
        elif ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            type = 'MTL-OUTRIGHT'
            
        return type
        
    def _instrumentDescription(self):
        desc = ''
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            desc = 'Energy Swap'
            
        elif ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            desc = 'Metal Outright'
        return desc
        
    def _valuationModel(self):
        model =  'Mtl-Phys MG-DIS'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
                model = 'Discounting'
                
        return model
        
        
        
    def _cashFlowType(self):
        type = 'Physical Fwd Proceeds'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            type = 'Upfront'
        return type
        
        
        
    def _rollConvention(self):
        return 'Month End' 
        
        

    def _projIndexGroupId (self):
        indexGroupId = 4
        if self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal':
            indexGroupId = 3
        elif self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal':
            indexGroupId = 2
            
        return indexGroupId
            
            
    def _payReceiveFlag(self):
        flag = 'Receive'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            if self.trade.Quantity() > 0:
                if self.leg ==0:
                    flag = 'Pay'
            elif self.trade.Quantity() < 0:
                if self.leg ==1: 
                    flag = 'Pay'
                    
        return flag           
        
                
    
        
    def _totalAmountCalculationPeriod(self):
        return self.leg
        
    def _fixedFloatingIndicator(self):
        indicator =  'Fixed'
        if self.leg == 1:
            indicator = 'Float'
            
        return indicator
        
    def _fixedLegRate(self):
        rate = self.trade.Price()*self.trade.Instrument().Quotation().QuotationFactor()
        if self.leg ==1:
            rate = 0
            
        return rate
        
    def _rollConvention(self):
        return 'Month End'
        
    def _legNumber(self):
        return self.leg
        
    def _totalTradeAmount(self):
        contractSize = self.instrument.ContractSize()
        quantity = self.trade.Quantity()
        #To Do : where quantity on the leg should take into account whether we are receiving or paying the amount
        amount =  abs(quantity * contractSize)
        
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            if self.trade.Quantity() > 0:
                if self.leg ==0:
                    amount = amount*(-1)
            elif self.trade.Quantity() < 0:
                if self.leg ==1: 
                    amount = amount*(-1)
        return amount
        
    def _contractSize(self):
        return self.instrument.ContractSizeInQuotation()
        
    def _averagePeriod(self):
        period = 1
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Agri')):
            period = 0
            
        return period
        
    def _settlementType(self):
        type = 'Cash'
        if ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal')):
            type = 'Physical'
            
        return type
        
    def _tradePrice(self):
        price = self.trade.Price()*self.trade.Instrument().Quotation().QuotationFactor()
        return price 
        
        
class CurrencyInstrTrade(BaseInstrTrade):
    def _init_(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)
        
    def _instrumentType(self):
        return 'MTL-OUTRIGHT'
    
    def _instrumentDescription(self):
        return 'Metal Outright'
      		
    def _settlementDate(self):
        return 

    def _indexCommodityCode(self):
        code =''
        if((self.instrument.Name()=='XAU')and(self.trade.Currency().Name()=='ZAR')):
            code='GOLD.ZAR'
        elif((self.instrument.Name()=='XAU')and(self.trade.Currency().Name()=='USD')):
            code='GOLD.USD'
        elif((self.instrument.Name()=='XPD')and(self.trade.Currency().Name()=='ZAR')):
            code='PALLADIUM.ZAR'
        elif((self.instrument.Name()=='XPD')and(self.trade.Currency().Name()=='USD')):
            code='PALLADIUM.USD'
        elif((self.instrument.Name()=='XAG')and(self.trade.Currency().Name()=='ZAR')):
            code='SILVER.ZAR'
        elif((self.instrument.Name()=='XAG')and(self.trade.Currency().Name()=='USD')):
            code='SILVER.USD'
        elif((self.instrument.Name()=='XPT')and(self.trade.Currency().Name()=='ZAR')):
            code='PLATINUM.ZAR'
        elif((self.instrument.Name()=='XPT')and(self.trade.Currency().Name()=='USD')):
            code='PLATINUM.USD'
            
        return code  
 
    def _indexCommodityDescription(self):
        desc =''
        if((self.instrument.Name()=='XAU')and(self.trade.Currency().Name()=='ZAR')):
            desc='GOLD.ZAR'
        elif((self.instrument.Name()=='XAU')and(self.trade.Currency().Name()=='USD')):
            desc='GOLD.USD'
        elif((self.instrument.Name()=='XPD')and(self.trade.Currency().Name()=='ZAR')):
            desc='PALLADIUM.ZAR'
        elif((self.instrument.Name()=='XPD')and(self.trade.Currency().Name()=='USD')):
            desc='PALLADIUM.USD'
        elif((self.instrument.Name()=='XAG')and(self.trade.Currency().Name()=='ZAR')):
            desc='SILVER.ZAR'
        elif((self.instrument.Name()=='XAG')and(self.trade.Currency().Name()=='USD')):
            desc='SILVER.USD'
        elif((self.instrument.Name()=='XPT')and(self.trade.Currency().Name()=='ZAR')):
            desc='PLATINUM.ZAR'
        elif((self.instrument.Name()=='XPT')and(self.trade.Currency().Name()=='USD')):
            desc='PLATINUM.USD'
            
        return desc   
  
    def _unitOfMeasurement(self):
            return 'TOZ'
    
    def _settlementType(self):
            return 'Physical'
  
    def _deliveryType(self):
        deltype = ''
        if self.instrument.Name()=='XAU':
            deltype = 'GOLD'
        elif self.instrument.Name()=='XPD':
            deltype = 'PALLADIUM'
        elif self.instrument.Name()=='XPT':
            deltype = 'PLATINUM'
        elif self.instrument.Name()=='XAG':
            deltype = 'SILVER'

        return deltype
  
    def _settlementDate(self):
        #To Do : Double check logic
        date = datetime.datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y%m%d')  
        return date 
    
    def _totalTradeAmount(self):
        return self.trade.Quantity()
  
    def _totalAmountCalculationPeriod(self):
        return 0

    def _optionType(self):
        return ''
  
    def _optionStype(self):
        return ''
  
    def _valuationModel(self):
        return 'Mtl-Phys MG-DIS'
  
    def _strikePrice(self):
        return ''
  
    def _tradePrice(self):
        return self.trade.Price()
  
    def _fixedLegRate(self):
        return self.trade.Price()
  
    def _resetDateRoll(self):
        return 0 
        
    def _resetOffSet(self):
        return 0
  
    def _averagePeriod(self):
        return 0
  
    def _roundingRule(self):
        return 5
  
    def _cashFlowType(self):
        return 'Physical Fwd Proceeds'
  
    def _rollConvention(self):
        return 'Month End'
  
    def _projIndexGroupId (self):
        return 2 
  
    def _instrumentClass(self):
        return 0
  
    def _independentAMT(self):
        return 0
        
    def _contractSize(self):
        return 1
        
    def _clientOrHouse(self):
        return 'HOUSE'
        
    def _averagePeriod(self):
        period = 1
           
        return period
    
  
class ComAbsaTradeReport:
    def __init__(self, file):
        self.file  = file
      
    def _fieldNames(self):
        fieldNames = ['010',
            'Trade ID',
            'Trade Input Date',
            'Trade Reference',
            'Internal Trade Link ID',
            'Internal Trade Type',
            'Trade Event',
            'Trade Date',
            'Trade Time',
            'Effective Date',
            'Trade Maturity Date',
            'Principal ID',
            'Trade Portfolio',
            'Trade Area',
            'Counterparty ID',
            'Trader ID',
            'Execution Broker ID',
            'Instrument Type',
            'Instrument Description',
            'Buy/sell indicator',
            'Exchange ID',
            'Execution Brokerage Rate',
            'Reference',
            'Leg Number',
            'Leg Start Date',
            'Settlement Date',
            'Leg Maturity Date',
            'Index/Commodity Code',
            'Index/commodity description',
            'Unit of Measurement',
            'Settlement Type',
            'Delivery Type',
            'Settlement Currency',
            'Total Trade Amount',
            'Trade Amount Calculation Period',
            'Counter Currency',
            'Counter Amount',
            'Option Type',
            'Option Style',
            'Valuation Model',
            'Strike Price',
            'Number of lots',
            'Trade Price',
            'Fixed/Floating Indicator',
            'Fixed Leg Rate',
            'Floating Spread',
            'Compounding Type',
            'Projection Index Tenor',
            'Leg Yield Basis',
            'Pay/Receive Flag',
            'Compounding Period',
            'Payment Period',
            'Payment Date Offset',
            'Pricing Contract',
            'Reset Date Roll',
            'Reset Offset',
            'Pricing-on-Last-Trading-Day',
            'Daily Volume Trade Flag',
            'Index Pricing Convention',
            'Reset Period',
            'Averaging Period',
            'Rounding Rule',
            'Discount Index',
            'Trade Portfolio Name',
            'Orig Counterparty Name',
            'Exchange Name',
            'Cash Flow Type',
            'Life to date Offset',
            'Reset Convention',
            'Roll Convention',
            'Package ID',
            'Package Component Trade Count',
            'Break Date',
            'Ultimate Package Id',
            'Exchange Flag',
            'Market Name',
            'Span Margining Flag',
            'Proj Index Group Id',
            'VAT code',
            'Legal Hierarchy',
            'Instrument Class',
            'Power_Product',
            'Buyout Date',
            'Agreement Type',
            'Delivery Start Date',
            'Delivery End Date',
            'Delivery Location',
            'Option Note Indicator',
            'Interval Type',
            'Document Type',
            'Heat Rate',
            'Collateral Exclusion',
            'Daily Volume',
            'Libra ID',
            'UNDERLYING_INS_TYPE',
            'INDEPENDENT_AMT',
            'SALESPERSON_ID',
            'INDEX_SUBGROUP_ID',
            'REFERENCE_RATE_UOM',
            'UNIT_CONV_FACTOR',
            'INDEX_MULTIPLIER',
            'COUNTERPARTY_TYPE',
            'RANSYS_PROCESSED',
            'EXCHANGE_PRODUCT_CODE',
            'CONTRACT_SIZE',
            'CLIENT_OR_HOUSE']
            
        return fieldNames
        
    def _writeHeader(self):
        fields = ['010', 'JHB', datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y%m%d')]
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter='|', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        
        finally:
            #self.file.close()
            print ''
            
    def _writeTradeRow(self, baseInstrTrade):
        fields =['030',
            baseInstrTrade._tradeId(),
            baseInstrTrade._inputDate(),
            baseInstrTrade._tradeReference(),
            baseInstrTrade._internalTradeLinkID(),
            baseInstrTrade._internalTradeType(),
            baseInstrTrade._tradeEvent(),
            baseInstrTrade._tradeDate(),
            baseInstrTrade._tradeTime(),
            baseInstrTrade._effectiveDate(),
            baseInstrTrade._maturityDate(),
            baseInstrTrade._principalID(),
            baseInstrTrade._tradePortfolio(),
            baseInstrTrade._tradeArea(),
            baseInstrTrade._counterPartyId(),
            baseInstrTrade._traderID(),
            baseInstrTrade.	_executionBroker(),
            baseInstrTrade.	_instrumentType(),
            baseInstrTrade._instrumentDescription(),
            baseInstrTrade.	_buySellIndicator(),
            baseInstrTrade._exchangeID(),
            baseInstrTrade._executionBrokerRate(),
            baseInstrTrade._reference(),
            baseInstrTrade._legNumber(),
            baseInstrTrade._legStartDate(),
            baseInstrTrade.	_settlementDate(),
            baseInstrTrade._legMaturityDate(),
            baseInstrTrade.	_indexCommodityCode(),
            baseInstrTrade._indexCommodityDescription(),
            baseInstrTrade._unitOfMeasurement(),
            baseInstrTrade._settlementType(),
            baseInstrTrade.	_deliveryType(),
            baseInstrTrade. _settlementCurrency(),
            baseInstrTrade.	_totalTradeAmount(),
            baseInstrTrade.	_totalAmountCalculationPeriod(),
            baseInstrTrade._counterCurrency(),
            baseInstrTrade._counterAmount(),
            baseInstrTrade._optionType(),
            baseInstrTrade._optionStype(),
            baseInstrTrade._valuationModel(),
            baseInstrTrade._strikePrice(),
            baseInstrTrade.	_numberOfLots(),
            baseInstrTrade.	_tradePrice(),
            baseInstrTrade._fixedFloatingIndicator(),
            baseInstrTrade._fixedLegRate(),
            baseInstrTrade. _floatingSpread(),
            baseInstrTrade._compoundingType(),
            baseInstrTrade.	_projectionIndexTenor(),
            baseInstrTrade._legYieldBasis(),
            baseInstrTrade.	_payReceiveFlag(),
            baseInstrTrade._compoundingPeriod(),
            baseInstrTrade._paymentPeriod(),
            baseInstrTrade._paymentDateOffset(),
            baseInstrTrade._pricingContract(),
            baseInstrTrade.   _resetDateRoll(),
            baseInstrTrade._resetOffSet(),
            baseInstrTrade.	_pricingOnLastTrading(),
            baseInstrTrade._dailyVolumeTrading(),
            baseInstrTrade._indexPricingConvention(),
            baseInstrTrade._resetPeriod(),
            baseInstrTrade._averagePeriod(),
            baseInstrTrade.	_roundingRule(),
            baseInstrTrade.	_discountIndex(),
            baseInstrTrade.	_tradePortfolioName(),
            baseInstrTrade.	_OrigCounterPartyName(),
            baseInstrTrade.	_exchangeName(),
            baseInstrTrade.	_cashFlowType(),
            baseInstrTrade.	_lifeToDateOffset(),
            baseInstrTrade._resetConvention(),
            baseInstrTrade._rollConvention(),
            baseInstrTrade.	_packageId(),
            baseInstrTrade._packageComponentTradeCount(),
            baseInstrTrade._breakDate(),
            baseInstrTrade.	_ultimatePackageId(),
            baseInstrTrade.	_exchangeFlag(),
            baseInstrTrade._marketName(),
            baseInstrTrade._spanMarginingFlag(),
            baseInstrTrade.	_projIndexGroupId (),
            baseInstrTrade._vatCode(),
            baseInstrTrade. _legalHierachy(),
            baseInstrTrade.	_instrumentClass(),
            baseInstrTrade.	_powerProduct(),
            baseInstrTrade.	_buyOutDate(),
            baseInstrTrade.	_agreementType(),
            baseInstrTrade.	_deliveryStartDate(),
            baseInstrTrade.	_deliveryEndDate(),
            baseInstrTrade.  _deliveryLocation(),
            baseInstrTrade.	_optionNoteIndicator(),
            baseInstrTrade.	_intervalType(),
            baseInstrTrade.   _documentType(),
            baseInstrTrade. _heatRate(),
            baseInstrTrade.	_collateralExclusion(),
            baseInstrTrade. _dailyVolume(),
            baseInstrTrade. _libraID(),
            baseInstrTrade.   _underlyingInstType(),
            baseInstrTrade.   _independentAMT(),
            baseInstrTrade.   _salesPersonID(),
            baseInstrTrade.	_indexSupGroupId(),
            baseInstrTrade.   _referenceRateUOM(),
            baseInstrTrade.	_unitConvFactor(),
            baseInstrTrade.  _indexMultiplier(),
            baseInstrTrade._counterPartyType(),
            baseInstrTrade._ransysAnalysisProcessed(),
            baseInstrTrade. _exchangeProductCode(),
            baseInstrTrade.   _contractSize(),
            baseInstrTrade._clientOrHouse()]
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
    return '_'.join(['ABSA_COMM_TDB_TRD']) + '.DAT'
    
def ael_main(ael_dict):
    
        
    filePath = ael_dict['filePath']
    output_dir = str(ael_dict['filePath'])
    filename = os.path.join(output_dir, get_filename())

    
    file = open(str(filename), 'wb') 
    all_trades = get_trades_data()
    
    report = ComAbsaTradeReport(file)
    report._writeHeader()
    report._writeColumnNames()
    checksum = 0
    count = len(all_trades) 
    
    for trade in all_trades:
        #print trade.Instrument().Name()  #block this out!!!
        if trade.Instrument().InsType() == 'Option' :
            baseInsr = OptionInstrTrade(trade, 0)
            checksum = checksum + baseInsr. _totalTradeAmount()
            report._writeTradeRow(baseInsr)
        elif trade.Instrument().InsType() == 'PriceSwap':
            
            legs = trade.Instrument().Legs()
            i = 0
            for leg in legs:
                
                baseInsr = SwapInstrTrade(trade, leg)
                report._writeTradeRow(baseInsr)
                checksum = checksum + baseInsr._totalTradeAmount()
                count = count + i
                i = i+1
            
        elif trade.Instrument().InsType() == 'Future/Forward':
            if ((trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Agri')):
                for i in range(0, 2):
                    baseInsr1 = FutureForwardInstrTrade(trade, i)
                    report._writeTradeRow(baseInsr1)
                    checksum = checksum + baseInsr1._totalTradeAmount()
                    if i > 0:
                        count = count + i
                    
                    
            else:
                baseInsr = FutureForwardInstrTrade(trade, 0)
                report._writeTradeRow(baseInsr)
                checksum = checksum + baseInsr._totalTradeAmount()
                
        elif trade.Instrument().InsType() == 'FXCash':
            baseInsr = FutureForwardInstrTrade(trade, 0)
            report._writeTradeRow(baseInsr)
            
        elif trade.Instrument().InsType() == 'Curr':
                baseInsr = CurrencyInstrTrade(trade, 0)
                report._writeTradeRow(baseInsr)
                checksum = checksum + baseInsr._totalTradeAmount()
                
        
               
    checksum ="%.2f" %checksum
    report._writeFooter(count, checksum)
    
    file.close()
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + str(filePath)+get_filename()
    
