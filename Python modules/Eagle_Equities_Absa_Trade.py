'''----------------------------------------------------------------------------------------------------------------
MODULE
    PS_CommodityMapping
DESCRIPTION
    Developer           : Melusi Maseko
    Date                : 2014-10-09
    Purpose             : Creates an Equities, Options and Forwards trade file for TDB
    Requestor           : Steve Smith
    CR Number           : 
ENDDESCRIPTION


HISTORY
    Date:               2015-07-02      
    CR Number:          MINT-310          
    Developer:          Melusi Maseko         
    Description:        Fix the ISIN (_instID). The ISIN, ExternalID1, ExternalID2 must be of the underlying instrument.                                    

    Date:               2015-08-17      
    CR Number:          MINT-343          
    Developer:          Melusi Maseko         
    Description:        Correct the Nominal_Contract_Indicator. 
    
    Date:               2017-07-19
    CR Number:          FAU-2857          
    Developer:          Melusi Maseko         
    Description:        UPGRADE 2017: Round off INITIAL PRICE to 6 decimal places
                                                INTEREST RATE to 4 decimal places.
                                                SPREAD to 3 decimal places.
                                                STRIKE AMOUNT to 3 decimal places.
                                                QUANTITY to 10 decimal places.
                                                PRIMARY AMOUNT to 2 decimal places.
                                                reset.StartDate() to use of the cashflows
----------------------------------------------------------------------------------------------------------------'''

import acm, ael
import csv
import sys
import FBDPGui
import FRunScriptGUI
import datetime
import at_time
import math
from Eagle_Commodity import InsAsian
from Eagle_Comm_Absa_Util import _convertTodDays, get_trades_data, date_from_timestamp, maturitydate_from_timestamp
import os

directorySelection=FRunScriptGUI.DirectorySelection()
today = acm.Time().DateToday()

rundate = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%Y%m%d')

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
        return self.trade.Oid()

    def _instrProductType(self):
        return ''  

    def _instrSubType(self):
        return ''

    def _optionStyle(self):
        optionStyle = ''
        
        if self.instrument.InsType() == 'Option':            
            if self.instrument.ExerciseType() == 'American':
                optionStyle = 'AMER'
            elif self.instrument.ExerciseType() == 'Bermudan':
                optionStyle = 'Bermudan'
            elif self.instrument.ExerciseType() == 'European':
                 optionStyle = 'EURO'
        return optionStyle

    def _book(self):
        book = self.trade.Portfolio().Name()
        return book[0:15]

    def _siteID(self):
        return 10250696

    def _discountIndex(self):
        return ''
       
    def _referenceRateID(self):
        return ''
   
    def _counterPartyId(self):
        addtionalInfo = self.trade.Counterparty().AdditionalInfo()
        counterpartyID = addtionalInfo.BarCap_Eagle_SDSID()
        return counterpartyID
        
    def _tradeDate(self):
        return date_from_timestamp(self.trade.TradeTime())
        
    def _linkID(self):
        return ''
        
    def _legNumber(self):
        return ''

    def _payReceiveFlag(self):
        return ''
        
    def _instrumentType(self):
        return ''
        
    def _primaryAmount(self):
        return ''

    def _firstvalueDate(self):
        return ''
        
    def _secondvalueDate(self):
        return ''

    def _paymentDay(self):
        return ''

    def _principalExchange(self):
        return 'None'
        
    def _dayCountBasis(self):
        return ''
        
    def _origPrimaryCurrency(self):
        return self.trade.Currency().Name()

    def _paymentCalc(self):
        return ''
                
    def _interestRate(self):
        return ''    

    def _interestCycleType(self):
        return ''

    def _payOffset(self):
        return ''

    def _resetTiming(self):
        return ''

    def _initialPrice(self):
        return ''

    def _fixedFloatInd(self):
        return ''

    def _buySell(self):
        indicator = 'BUY'
        if self.trade.Quantity() < 0 :
            indicator = 'SELL'
        return indicator
    
    def _interestTerm(self):
        return ''
    
    def _quantity(self):
        return round(self.trade.Quantity(), 10)

    def _maturityDate(self):
        return at_time.to_datetime(self.instrument.ExpiryDate()).strftime('%Y%m%d')
        
    def _underlyCallPut (self):
        if  self.instrument.IsCall():
            optionType = 'CALL' 
        else:
            optionType ='PUT'    
        return optionType
    
    def _nominalContractInd (self):
        type = ''
        if self.instrument.Quotation(): type = self.instrument.Quotation().Name() 
        else: type
                
        if type in ('Per Unit', 'Per 100 Units'):return 'N'
        elif type in ('Per Contract', 'Per 100 Contracts'): return 'C'
        else:
            return ''

    def _accrualbasis (self):
        return 'A365F'


    def _underlyQuantity (self):
        return self.underlying.Quotation().QuotationFactor()

    def _strikeAmount (self):
        return ''

    def _strikeDate (self):
        return ''
        
    def _strikeType (self):
        return ''

    def _strikeWeight (self):
        return self.instrument.ContractSize()
        
    def _strikeBasis (self):
        return ''
        
    def _instrCurrency(self):
        return self.trade.Currency().Name()
  
    def _quantoCompoInd(self):
        return ''
 
    def _classID(self):
        class_ID=''
        if self.instrument.Otc():
            if self.instrument.InsType()=='TotalReturnSwap':
                class_ID = 'EQSO'
                
            elif self.instrument.UnderlyingType()=='EquityIndex':
                if self.instrument.InsType()=='Future/Forward':
                    class_ID = 'EQFW'
                elif self.instrument.InsType()=='Option':
                    class_ID = 'EQOD'
                    
            elif self.instrument.UnderlyingType()=='Stock':
                if self.instrument.InsType()=='Future/Forward':
                    class_ID = 'IOO'
                elif self.instrument.InsType()=='Option':
                    class_ID = 'IOO'
            
        else:
        
            if self.instrument.InsType()=='TotalReturnSwap':
                class_ID = 'ISO'
                
            elif self.instrument.UnderlyingType()=='EquityIndex':
                if self.instrument.InsType()=='Future/Forward':
                    class_ID = 'EQFW'
                elif self.instrument.InsType()=='Option':
                    class_ID = 'EQOO'
                    
            elif self.instrument.UnderlyingType()=='Stock':
                if self.instrument.InsType()=='Future/Forward':
                    class_ID = 'IOFE'
                elif self.instrument.InsType()=='Option':
                    class_ID = 'IOE'


        return class_ID


    def _instID(self):
        if self.instrument.Isin()=='':
            #Substring the name to get the underlying instrument's isin
            string = self.instrument.Underlying().Name()
            inst = string.split("_")

            length = len(inst)
            if length >= 0:
                i = inst[0]
                ins = acm.FInstrument[i]
                
                if ins:
                    if ins.Isin():
                        return ins.Isin()+';'+ins.ExternalId1()+';'+ins.ExternalId2()
                    else:
                        return ';'+ins.ExternalId1()+';'+ins.ExternalId2()
                else:
                    return ''

    def _spread (self):
        return ''

    def _intCycleRule (self):
        return ''

    def _resetInterestRule (self):
        return ''

    def _testing(self):
        return ''

    def _isValidCF(self, legnbr):
        count=0
        for cf in self.leg.CashFlows():
            if cf.CashFlowType()=='Dividend' and cf.Leg().Oid()==legnbr:
                count=count+1
        return count

class OptionInstrTrade(BaseInstrTrade):
    def __init__(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)

    def _instrProductType(self):
        #return self.instrument.InsType()    
        return 'Option'
        
    def _instrSubType(self):
        return 'Equity'

    def _linkID(self):
        return ''

    def _legNumber(self):
        return '1'
        
    def _strikeDate (self):
        return at_time.to_datetime(self.instrument.ExpiryDate()).strftime('%Y%m%d')
        
    def _strikeType (self):
        type = self.instrument.StrikeType()
        if type == 'Absolute':
            return 'FIXED'
        else:
            return type.upper()

    def _strikeAmount (self):
        quotationFactor = self.underlying.Quotation().QuotationFactor()
        if quotationFactor == 0.01:
            return round(self.instrument.StrikePrice(), 2) * quotationFactor
        else:
            return round(self.instrument.StrikePrice(), 3)
            
    def _strikeWeight (self):
        type = self.instrument.Quotation().Name()
        if type == 'Per Unit' or type == 'Per Contract':
            return 1
        elif type == 'Per 100 Units' or type == 'Per 100 Contracts':
            return 100
        else:
            return 0

    def _totalTradeAmount(self):
        return self.trade.Quantity()

    def _paymentCalc(self):
        return ''
  
    def _quantoCompoInd(self):
        ind = 'C'
        if self.instrument.QuantoOptionType()== 'Quanto':
            ind = 'Q'        
        return ind 
   
    def _underlyQuantity (self):
        return self.instrument.ContractSize()

class EquitySwapTrade(BaseInstrTrade):
    def __init__(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)    

    def _testing(self):
        return self.trade.Instrument().IndexReference().InsType()

    def _instrSubType(self):
        return 'EquitySwap'
   
    def _instrProductType(self):
        #return self.instrument.InsType() 
        return 'Swap'
        
    def _payReceiveFlag(self):
        payOrReceive = 'P'
        if self.leg.LegType()== 'Fixed' or self.leg.LegType()== 'Float':
            payOrReceive = 'R'
        return payOrReceive

    def _quantity(self):
        indicator = '1'
        if self.trade.Quantity() < 0 :
            indicator = '-1'
        return indicator

    def _resetTiming(self):
        resets = self.leg.Resets()
        for r in resets:
            if r.Day() <= r.CashFlow().StartDate():
                if self.leg.LegType()== 'Total Return':
                    return 'ARR'
                else:
                    return 'ADV'
            else:
                return 'ARR'

    def _primaryAmount(self):
        if self.leg.LegType()== 'Fixed' or self.leg.LegType()== 'Float':
        
            if self.leg.PayLeg():
                p_amt = self.trade.Nominal()
                if p_amt < 0:
                    return round(p_amt * -1, 3)
                else:
                    return round(p_amt, 3)
            else:
                p_amt = self.trade.Nominal()
                if p_amt > 0:
                    return round(p_amt * -1, 3)
                else:
                    return round(p_amt, 3)
           
                return round(self.trade.Nominal()*-1, 3)
        else:
            if self.leg.PayLeg():
                p_amt = self.trade.Quantity()
                if p_amt < 0:
                    return p_amt * -1
                else:
                    return p_amt
            else:
                p_amt = self.trade.Quantity()
                if p_amt > 0:
                    return p_amt * -1
                else:
                    return p_amt
           
                return self.trade.Quantity()*-1
        
    def _totalAmountCalculationPeriod(self):
        #print self.leg.LegType()
        if self.leg.LegType() == 'Fixed':
            return 0
        else:
            #print 'whats this?',self.leg.RollingPeriodUnit()
            return _convertTodDays(self.leg.RollingPeriodUnit())*self.leg.RollingPeriodCount() 

    def _dayCountBasis(self):
        return self.leg.DayCountMethod()

    def _firstvalueDate(self):
        return datetime.datetime.strptime(self.leg.StartDate(), '%Y-%m-%d').strftime('%Y%m%d')
  
    def _secondvalueDate(self):
        return datetime.datetime.strptime(self.leg.EndDate(), '%Y-%m-%d').strftime('%Y%m%d')
       
    def _linkID(self):
        return self.trade.Oid()

    def _totalTradeAmount(self):
        return self.trade.Quantity()
        
    def _legNumber(self):
        return self.leg.Oid()
        
    def _paymentCalc(self):
        return self.leg.Currency().Name()
        
    def _initialPrice(self):
        return round(self.leg.InitialIndexValue()/100, 6)

    def _fixedFloatInd(self):
        ind = ''
        if self.leg.LegType()== 'Fixed':
            ind = 'FIX'
        elif self.leg.LegType()== 'Float':
            ind = 'FLT'
            
        return ind

    def _instrumentType(self):
        insType = 'Equity'
        if self.leg.LegType()== 'Fixed' or self.leg.LegType()== 'Float':
            insType = 'IR'
        return insType

    def _paymentDay(self):
        return datetime.datetime.strptime(self.leg.EndDate(), '%Y-%m-%d').strftime('%d')  

    def _payOffset(self):
        return _convertTodDays(self.leg.PayOffsetUnit)*self.leg.PayOffsetCount() 

    def _strikeAmount (self):
        return round(self.instrument.StrikePrice(), 4)

    def _strikeDate (self):
        return datetime.datetime.strptime(self.instrument.EndDate(), '%Y-%m-%d').strftime('%Y%m%d')
                
    def _strikeType (self):
        type = self.leg.StrikeType()
        if type == 'Absolute':
            return 'FIXED'
        else:
            return type.upper()
 
    def _accrualbasis (self):
        return ''#self.leg.DayCountMethod('Act/365')

    def _interestTerm(self):
        if self.leg.LegType()== 'Float':
            return self.leg.RollingPeriod().upper()
        else:
            return ''
        
    def _underlyCallPut (self):
        return ''
    
    def _nominalContractInd (self):
        return ''

    def _underlyQuantity (self):
        return ''
        
    def _strikeAmount (self):
        return ''

    def _strikeDate (self):
        return ''

    def _strikeWeight (self):
        return ''
    
    def _buySell(self):
        return ''

    def _interestCycleType(self):
        interestCycleType =  {'1y':'A',
                    '364d':'A',
                    '0d':'D',
                    '1d':'D',
                    '1m':'M',
                    '28d':'M',
                    '4w':'M',
                    '3m':'Q',
                    '91d':'Q',
                    '182d':'S',
                    '6m':'S',
                    '1w':'W',
                    '0t':'Z',
                    '1t':'Z'}    
                
        cycle = interestCycleType[self.leg.RollingPeriod()]
        
        return cycle
        
    def _instID(self):
        if self.instrument.Isin()=='':
            if self.leg.IndexRef() and self.leg.IndexRef().Isin() or self.leg.IndexRef().ExternalId1() or self.leg.IndexRef().ExternalId2():
                return self.leg.IndexRef().Isin()+';'+self.leg.IndexRef().ExternalId1()+';'+self.leg.IndexRef().ExternalId2()

            else:
                return ''
    
    def _refRatefloatRef(self):
        string = ''
        
        if not (self.leg.PayLeg()):
            if self.leg.Leg().FloatRateReference():
                string = self.leg.Leg().FloatRateReference().Name()
                array = string.split("-")
                length = len(array)
                if length > 0:
                    return array[length - 2]
                else:
                    return ''
            else:
                return ''    

    def _payFloatRef(self):
        string = ''
        
        if self.leg.PayLeg():
            for l in self.trade.Instrument().Legs():
                if not (l.PayLeg()):
                    
                    if l.FloatRateReference():
                        string = l.FloatRateReference().Name()
                        array = string.split("-")
                        length = len(array)
                        if length > 0:
                            return array[length - 2]
                        else:
                            return 'None'
                    else:
                        return 'None'  
        return 'None'
 
    def _receiveFloatRef(self):
        string = ''
        if not (self.leg.PayLeg()):
            if self.leg.Leg().FloatRateReference():
                string = self.leg.Leg().FloatRateReference().Name()
                array = string.split("-")
                length = len(array)
                if length > 0:
                    return array[length - 2]
                else:
                    return 'None'
            else:
                return 'None'  
        else:
            return self._payFloatRef()
          
       
    def _discountIndex(self):
        if self.leg.LegType()== 'Fixed':
            return 'None'
        else:
            return self._receiveFloatRef()
     
    def _referenceRateID(self):
        if self.leg.LegType()== 'Fixed':
            return 'None'
        else:
            return self._refRatefloatRef()
        
    def _spread (self):
        return round(self.leg.Spread(), 3)
    
    def _intCycleRule (self):
        cycle = ''
        interestCycleRule =  {'None':'N',
                'Following':'F',
                'Preceding':'P',
                'Mod. Following':'MF',
                'Mod. Preceding':'MP',
                'FRN Convention':'FRN',
                'IMM':'IMM',
                'Monthly IMM':'MIMM',
                'EOM':'EOM',
                'CDS Convention':'CDS',
                'BMA Convention':'BMA',
                'FOM':'FOM'}    
   
        if self.leg.LegType()== 'Fixed' or self.leg.LegType()== 'Float':
            cycle = interestCycleRule[self.leg.Leg().PayDayMethod()] 

        return cycle
                

    def _buySell(self):
        indicator = 'BUY'
        if self.trade.Quantity() < 0 :
            indicator = 'SELL'
        return indicator

    def _interestRate(self):
        return round(self.leg.FixedRate(), 4)
        
    def _resetInterestRule (self):
        cycle = ''
        interestCycleRule =  {'None':'N',
                'Following':'F',
                'Preceding':'P',
                'Mod. Following':'MF',
                'Mod. Preceding':'MP',
                'FRN Convention':'FRN',
                'IMM':'IMM',
                'Monthly IMM':'MIMM',
                'EOM':'EOM',
                'CDS Convention':'CDS',
                'BMA Convention':'BMA',
                'FOM':'FOM'}    
   
        if self.leg.LegType()== 'Total Return':
            cycle = interestCycleRule[self.leg.Leg().PayDayMethod()]        
        return cycle
                


    def _isDividend(self):
        for cf in self.leg.CashFlows():
            if cf.cashFlowType()=='Dividend':
                LegNbr = cf.Leg().Oid()
        return LegNbr        
       
class FutureForwardInstrTrade(BaseInstrTrade):

    def _init_(self, trade, leg):
        BaseInstrTrade.__init__(self, trade, leg)
    
    def _tradeId(self):
        return str(self.trade.Oid())+'-'+str(self.leg)


    def _instrProductType(self):
        return 'Option'

    def _instrSubType(self):
        return 'Equity'

    def _optionStyle(self):
        return 'EURO'
        
    def _linkID(self):
        return self.trade.Oid()
       
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

    def _buySell(self):
        indicator = ''
        if self.leg == 1:
            indicator = 'BUY'
        else:
            indicator = 'SELL'
        return indicator
        
    def _quantity(self):
        qty = ''
        if self.trade.Quantity() > 0:
            if self.leg == 0:
                qty = self.trade.Quantity()*-1
            else:
                qty = self.trade.Quantity()
        else:
            if self.leg == 1:
                qty = self.trade.Quantity()*-1
            else:
                qty = self.trade.Quantity()
        return round(qty, 10)

    def _underlyCallPut (self):
        indicator = ''
        if self.trade.Quantity() > 0:
            if self.leg == 0:
                indicator = 'PUT'
            else:
                indicator = 'CALL'
        else:
            if self.leg == 1:
                indicator = 'PUT'
            else:
                indicator = 'CALL'
        return indicator

    def _rollConvention(self):
        return 'Month End' 


    def _projIndexGroupId (self):
        indexGroupId = 4
        if self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal':
            indexGroupId = 3
        elif self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal':
            indexGroupId = 2
        return indexGroupId


    def _totalAmountCalculationPeriod(self):
        return self.leg
        
    def _fixedFloatingIndicator(self):
        indicator =  'FIX'
        if self.leg == 1:
            indicator = 'FLT'
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
        
    def _strikeAmount (self):
        type = self.instrument.Quotation().Name()
        if type == 'Per Unit' or type == 'Per Contract':
            return round(self.trade.Price(), 4)
        elif type == 'Per 100 Units' or type == 'Per 100 Contracts':
            return round(self.trade.Price() / 100, 4)
        else:
            return round(self.trade.Price(), 4)
            
    def _strikeDate (self):
        return datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')

    def _strikeType (self):
        return 'FIXED'

    def _strikeWeight (self):
        type = self.instrument.Quotation().Name()
        if type == 'Per Unit' or type == 'Per Contract':
            return 1
        elif type == 'Per 100 Units' or type == 'Per 100 Contracts':
            return 100
        else:
            return 0
            
    def _quantoCompoInd(self):
        return 'C'
        
    def _underlyQuantity (self):
        return self.instrument.ContractSize()
       

  
class EquitiesAbsaTradeReport:
    def __init__(self, file):
        self.file  = file
      
    def _fieldNames(self):
        fieldNames = ['010',
            'TRADE ID',
            'INST PRODUCT TYPE',
            'INST SUB TYPE',
            'OPTION STYLE',
            'BOOK',
            'SITE ID',
            'COUNTERPARTY ID',
            'TRADE DATE',
            'LINK ID',
            'LEG NUMBER',
            'PAY OR RECEIVE',
            'INST TYPE',
            'PRIMARY AMOUNT',
            'FIRST VALUE DATE',
            'SECOND VALUE DATE',
            'PAYMENT DAY',
            'PRINCIPAL EXCHANGE',
            'DAY COUNT BASIS',
            'DISCOUNT INDEX',
            'REFERENCE RATE ID',
            'ORIG PRIMARY CURRENCY',
            'PAYMENT CAL',
            'INTEREST CYCLE TYPE',
            'PAY OFFSET',
            'RESET TIMING',
            'INITIAL PRICE',
            'FIXED FLOAT IND',
            'INTEREST RATE',
            'INTEREST TERM',
            'BUY OR SELL',
            'QUANTITY',
            'MATURITY DATE',
            'UNDERLYING CALL OR PUT',
            'NOMINAL CONTRACT IND',
            'ACCRUAL BASIS',
            'UNDERLYING QUANTITY',
            'STRIKE AMOUNT',
            'STRIKE DATE',
            'STRIKE TYPE',
            'STRIKE WEIGHT',
            'STRIKE BASIS',
            'INST ID',
            'INST CURRENCY',
            'QUANTO COMPO IND',
            'CLASS ID',
            'SPREAD',
            'INTEREST CYCLE RULE',
            'RESET INTEREST RULE']
            
        return fieldNames
        
    def _writeHeader(self):
        fields = ['010', 'JHB', rundate]
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter=',', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        
        finally:
            print ''
            
    def _writeTradeRow(self, baseInstrTrade):
        fields =['030',
            baseInstrTrade._tradeId(),
            baseInstrTrade._instrProductType(),
            baseInstrTrade._instrSubType(),
            baseInstrTrade._optionStyle(),
            baseInstrTrade._book(),
            baseInstrTrade._siteID(),
            baseInstrTrade._counterPartyId(),
            baseInstrTrade._tradeDate(),
            baseInstrTrade._linkID(),
            baseInstrTrade._legNumber(),
            baseInstrTrade._payReceiveFlag(),
            baseInstrTrade._instrumentType(),
            baseInstrTrade._primaryAmount(),
            baseInstrTrade._firstvalueDate(),
            baseInstrTrade._secondvalueDate(),
            baseInstrTrade._paymentDay(),
            baseInstrTrade._principalExchange(),
            baseInstrTrade._dayCountBasis(),
            baseInstrTrade._discountIndex(),
            baseInstrTrade._referenceRateID(),
            baseInstrTrade._origPrimaryCurrency(),
            baseInstrTrade._paymentCalc(),
            baseInstrTrade._interestCycleType(),
            baseInstrTrade._payOffset(),
            baseInstrTrade._resetTiming(),
            baseInstrTrade._initialPrice(),
            baseInstrTrade._fixedFloatInd(),
            baseInstrTrade._interestRate(),
            baseInstrTrade._interestTerm(),
            baseInstrTrade._buySell(),
            baseInstrTrade._quantity(),
            baseInstrTrade._maturityDate(),
            baseInstrTrade._underlyCallPut(),
            baseInstrTrade._nominalContractInd(),
            baseInstrTrade._accrualbasis(),
            baseInstrTrade._underlyQuantity(),
            baseInstrTrade._strikeAmount(),
            baseInstrTrade._strikeDate(),
            baseInstrTrade._strikeType(),
            baseInstrTrade._strikeWeight(),
            baseInstrTrade._strikeBasis(),
            baseInstrTrade._instID(),
            baseInstrTrade._instrCurrency(),
            baseInstrTrade._quantoCompoInd(),
            baseInstrTrade._classID(),
            baseInstrTrade._spread(),
            baseInstrTrade._intCycleRule(),
            baseInstrTrade._resetInterestRule()]
              
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _writeFooter(self, count, checksum):
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['090', count, checksum])           
        
            
ael_variables = [
['tradeFilter', 'Trade Filters', 'FTradeSelection', acm.FTradeSelection.Select(''), 'Eagle_Equities_DerivsV3', 1, 1],
['filePath', 'File Path', 'string', None, '/services/frontnt/Task/', 0],
['fileName', 'File Name', 'string', None, 'ABSA_EQT_TDB_TRD_'+rundate+'.DAT', 0],]

    
def get_filename():
    """Return the dump's filename."""
    #date_str = maturitydate_from_timestamp(today)
    return '_'.join(['ABSA_EQUITIES_TDB_TRD']) + '.DAT'

#def get_filedate():

    
def ael_main(parameters):

    filename = parameters['filePath'] + parameters['fileName']

    tfname = parameters['tradeFilter'][0]
    
    file = open(str(filename), 'wb') 
    
    report = EquitiesAbsaTradeReport(file)
    
    #Write header and column names as per spec requirement
    report._writeHeader()
    report._writeColumnNames()
    checksum = 0
    count = 0
    
    for trade in tfname.Trades():
        if trade.Instrument().InsType() == 'Option' :
            baseInsr = OptionInstrTrade(trade, 0)
            report._writeTradeRow(baseInsr)
            count = count + 1
            if baseInsr._primaryAmount()== '':
                amt = 0
            else:
                amt = _primaryAmount()              
            checksum = checksum + amt
            
        elif (trade.Instrument().InsType() == 'TotalReturnSwap'and trade.Instrument().IndexReference()):
            if trade.Instrument().IndexReference().InsType()=='EquityIndex' or trade.Instrument().IndexReference().InsType()=='Stock':
                legs = trade.Instrument().Legs()
                i = 0
                for leg in legs:
                    if leg.CashFlows():
                        if leg.CashFlows()[0].CashFlowType() != 'Dividend':
                            baseInsr = EquitySwapTrade(trade, leg)                    
                            report._writeTradeRow(baseInsr)
                            amt = baseInsr._primaryAmount()
                            checksum = checksum + amt
                            count = count + 1
                            i = i+1
            
        elif trade.Instrument().InsType() == 'Future/Forward':
            if ((trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Agri')):

                    baseInsr = FutureForwardInstrTrade(trade, 0)
                    report._writeTradeRow(baseInsr)
                    count = count + 1
                    if baseInsr._primaryAmount()== '':
                        amt = 0
                    else:
                        amt = baseInsr._primaryAmount()   
                    checksum = checksum + amt
 
                    baseInsr = FutureForwardInstrTrade(trade, 1)
                    report._writeTradeRow(baseInsr)
                    count = count + 1
                    if baseInsr._primaryAmount()== '':
                        amt = 0
                    else:
                        amt = baseInsr._primaryAmount()    
                    checksum = checksum + amt
                    
            else:
                baseInsr = FutureForwardInstrTrade(trade, 0)
                report._writeTradeRow(baseInsr)
                count = count + 1
                if baseInsr._primaryAmount()== '':
                    amt = 0
                else:
                    amt = baseInsr._primaryAmount()   
          
                checksum = checksum + amt
                
                baseInsr = FutureForwardInstrTrade(trade, 1)
                report._writeTradeRow(baseInsr)
                count = count + 1
                if baseInsr._primaryAmount()== '':
                    amt = 0
                else:
                    amt = baseInsr._primaryAmount()    
                checksum = checksum + amt
        
    checksum ="%.2f" %checksum
    report._writeFooter(count, checksum)
    
    file.close()
    print checksum
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + filename
