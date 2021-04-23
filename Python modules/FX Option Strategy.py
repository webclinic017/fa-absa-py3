"""-----------------------------------------------------------------------------
MODULE
    FX Option Strategy

DESCRIPTION
    Date                : 2011-02-15
    Purpose             : Creates a FX Option Strategy GUI to book FX Strategies
    Department and Desk : FX Options
    Requester           : Justin Nichols
    Developer           : Herman Hoon
    CR Number           : 572767
ENDDESCRIPTION

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-02-15 572767           Herman Hoon        Initial implementation
2011-03-02 589474           Herman Hoon        Included Save New functionality and added Value Add Sales Credit
2011-04-05 618606           Herman Hoon        Prevent non-business dates in the date fields
2011-04-12 624212           Herman Hoon        Include the new Synthetic Forward strategy type
2013-11-18 CHNG0001527675   Conicov Andrei     In the 2013.3 version, class FAdditionalInfo, the Value method has been replaced by FiledValue  
-----------------------------------------------------------------------------"""

import acm
import FUxCore
import ael

class OptionsStrategy(FUxCore.LayoutDialog):
    """Generating option strategy"""

    def __init__(self):
        self.strategy = 'Straddle'
        
        self.businessLogicHandler = self._createBusinessLogicHandler()

        self.ins1Orig = acm.FOption()
        self.ins1 = self.ins1Orig.Clone()
        self.insDecorator1 = acm.FOptionDecorator(self.ins1, self.businessLogicHandler)
        self.trade1Orig = acm.FTrade()
        self.trade1 = self.trade1Orig.Clone()
        self.trade1.Type('Normal')
        self.tradeDecorator1 = acm.FTradeLogicDecorator(self.trade1, self.businessLogicHandler)
        self.tradeDecorator1.Instrument(self.ins1)
        
        self.ins2Orig = acm.FOption()
        self.ins2 = self.ins2Orig.Clone()
        self.insDecorator2 = acm.FOptionDecorator(self.ins2, self.businessLogicHandler)
        self.trade2Orig = acm.FTrade()
        self.trade2 = self.trade2Orig.Clone()
        self.trade2.Type('Normal')
        self.tradeDecorator2 = acm.FTradeLogicDecorator(self.trade2, self.businessLogicHandler)
        self.tradeDecorator2.Instrument(self.ins2)
        
        self.defaultID = 'Option-Curr-Default'
        self.defaultIns = acm.FOption[self.defaultID]
        self._setDefaultInsValues(self.ins1)
        self._setDefaultInsValues(self.ins2)
        
        choice = acm.FChoiceList.Select("name = %s" % (self.strategy))[0]
        self.insDecorator1.ProductTypeChlItem(choice)
        self.insDecorator2.ProductTypeChlItem(choice)
        
        self.domCurr = ''
        self.forCurr = ''
        self.direction1 = 1
        self.direction2 = 1
        
        self.strikeQuotation = 'Per Unit'
        self.insDecorator1.StrikeQuotation(acm.FQuotation[self.strikeQuotation])
        self.insDecorator2.StrikeQuotation(acm.FQuotation[self.strikeQuotation])
        
        self.insDecorator1.OptionType('Put')
        self.insDecorator2.OptionType('Call')
        
        self.priceType = 1
        self.insQuotation = 'Pct of Nominal'
        self.tradeCurr = ''
        
        self.quantity1 = 0
        self.quantity2 = 0
        
        # Indicators
        self.initCurrency = 1
        self.initShowTrades = True
        self.showTrades = False
        self.setStrategyID = 1
        
        self.directionChange = 1
        self.callPutChange = 1
        self.updateValues = 1
        self.flipped = 0
        
        self.saveEnabled = False
        self.tradesExist = False
        
    def _createBusinessLogicHandler(self):
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        return businessLogicGUIDefaultHandler
    
    def _setDefaultInsValues(self, instrument):
        instrument.ValuationGrpChlItem(self.defaultIns.ValuationGrpChlItem())
        instrument.PayType(self.defaultIns.PayType())
        instrument.SettlementType(self.defaultIns.SettlementType())

    def InitControls(self):
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)
        
        doubleDefault = acm.GetDomain('double').DefaultFormatter()
        doubleDefault.NumDecimals(2)
        
        fourDecFormat = doubleDefault.Clone()
        fourDecFormat.NumDecimals(4)
        
        self.b_curr_pair = self.binder.AddBinder('curr_Pair', acm.GetDomain('FCurrencyPair'), None)
        
        self.b_expiry1 = self.binder.AddBinder('expiry1', acm.GetDomain('date'), None)
        self.b_expiry2 = self.binder.AddBinder('expiry2', acm.GetDomain('date'), None)
        
        self.b_cut1 = self.binder.AddBinder('cut1', acm.GetDomain('FMTMMarket'), None)
        self.b_cut2 = self.binder.AddBinder('cut2', acm.GetDomain('FMTMMarket'), None)
        
        self.b_delivery1 = self.binder.AddBinder('delivery1', acm.GetDomain('date'), None)
        self.b_delivery2 = self.binder.AddBinder('delivery2', acm.GetDomain('date'), None)
        
        self.b_strike1 = self.binder.AddBinder('strike1', acm.GetDomain('double'), fourDecFormat)
        self.b_strike2 = self.binder.AddBinder('strike2', acm.GetDomain('double'), fourDecFormat)

        self.b_for_amount1 = self.binder.AddBinder('for_amount1', acm.GetDomain('double'), None)
        self.b_for_amount2 = self.binder.AddBinder('for_amount2', acm.GetDomain('double'), None)
        
        self.b_dom_amount1 = self.binder.AddBinder('dom_amount1', acm.GetDomain('double'), None)
        self.b_dom_amount2 = self.binder.AddBinder('dom_amount2', acm.GetDomain('double'), None)
        
        self.b_price1 = self.binder.AddBinder('price1', acm.GetDomain('double'), fourDecFormat)
        self.b_price2 = self.binder.AddBinder('price2', acm.GetDomain('double'), fourDecFormat)
        
        self.b_premium1 = self.binder.AddBinder('premium1', acm.GetDomain('double'), None)
        self.b_premium2 = self.binder.AddBinder('premium2', acm.GetDomain('double'), None)
        
        self.b_portfolio = self.binder.AddBinder('portfolio', acm.GetDomain('FPhysicalPortfolio'), None)
        self.b_acquirer = self.binder.AddBinder('acquirer', acm.GetDomain('FInternalDepartment'), None)
        self.b_trader = self.binder.AddBinder('trader', acm.GetDomain('FUser'), None)
        self.b_salesPerson = self.binder.AddBinder('salesPerson', acm.GetDomain('FUser'), None)
        self.b_salesCredit = self.binder.AddBinder('salesCredit', acm.GetDomain('double'), None)
        self.b_valueAddCredit = self.binder.AddBinder('valueAddCredit', acm.GetDomain('double'), None)
        self.b_tradeDate = self.binder.AddBinder('tradeDate', acm.GetDomain('date'), None)
        self.b_valueDate = self.binder.AddBinder('valueDate', acm.GetDomain('date'), None)
        self.b_status = self.binder.AddBinder('status', acm.GetDomain(acm.FEnumeration['enum(TradeStatus)']), None)
        

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        
        if str(aspectSymbol) == 'ControlValueChanged' and self.updateValues == 1:
            self._Changed(True)
            # Currency Pair Update
            if parameter == self.b_curr_pair:
                self._updateCurrencyPair()
            
            # Expiry1 update    
            elif parameter == self.b_expiry1:  
                self._updateExpiry1()
                
            # Expiry2 update    
            elif parameter == self.b_expiry2:  
                self._updateExpiry2()
            
            # Delivery1 update
            elif parameter == self.b_delivery1:  
                self._updateDelivery1()

            # Delivery2 update
            elif parameter == self.b_delivery2:  
                self._updateDelivery2()
            
            # Trade time update
            elif parameter == self.b_tradeDate:
                self._updateTradeDate()
            
            # Value date update
            elif parameter == self.b_valueDate:
                self._updateValueDate()

            # Cut1 update    
            elif parameter == self.b_cut1:  
                value = self.b_cut1.GetValue()
                self.b_cut2.SetValue(value)
                self.insDecorator1.FixingSource(value)
            
            # Cut2 update    
            elif parameter == self.b_cut2:  
                value = self.b_cut2.GetValue()
                self.b_cut1.SetValue(value)
                self.insDecorator2.FixingSource(value)
            
            # strike1 update
            elif parameter == self.b_strike1:
                self.insDecorator1.StrikePrice(self.b_strike1.GetValue())
                if self.strategy in ('Straddle', 'Synthetic Forward'):
                    self.b_strike2.SetValue(self.b_strike1.GetValue())
                
                self._updateForAmount1()
                self._updatePremium1()

            # strike2 update
            elif parameter == self.b_strike2:
                self.insDecorator2.StrikePrice(self.b_strike2.GetValue())
                if self.strategy in ('Straddle', 'Synthetic Forward'):
                    self.b_strike1.SetValue(self.b_strike2.GetValue())
                    
                self._updateForAmount2()
                self._updatePremium2()

            # for_amount1 update
            elif parameter == self.b_for_amount1:
                self._updateForAmount1()

                if self.strategy in ('Synthetic Forward'):
                    self.b_for_amount2.SetValue(self.b_for_amount1.GetValue())
                    self._updateForAmount2()
    
                self._updatePremium1()
                    
            # for_amount2 update
            elif parameter == self.b_for_amount2:
                self._updateForAmount2()
                
                if self.strategy in ('Synthetic Forward'):
                    self.b_for_amount1.SetValue(self.b_for_amount2.GetValue())
                    self._updateForAmount1()
                    
                self._updatePremium2()
                
            # dom_amount1 update
            elif parameter == self.b_dom_amount1:
                self._updateDomAmount1()
                
                if self.strategy in ('Synthetic Forward'):
                    self.b_dom_amount2.SetValue(self.b_dom_amount1.GetValue())
                    self._updateDomAmount2()
                
                self._updatePremium1()

            # dom_amount2 update
            elif parameter == self.b_dom_amount2:
                self._updateDomAmount2()
                
                if self.strategy in ('Synthetic Forward'):
                    self.b_dom_amount1.SetValue(self.b_dom_amount2.GetValue())
                    self._updateDomAmount1()
                
                self._updatePremium2()

            # price1 update
            elif parameter == self.b_price1:
                self.tradeDecorator1.Price(self.b_price1.GetValue())
                self._updatePremium1()
            
            # price2 update
            elif parameter == self.b_price2:
                self.tradeDecorator2.Price(self.b_price2.GetValue())
                self._updatePremium2()
            
            # premium1 update
            elif parameter == self.b_premium1:
                self.tradeDecorator1.Premium(-1 * self.direction1 * abs(self.b_premium1.GetValue()))
                self._updatePrice1()
            
            # premium1 update
            elif parameter == self.b_premium2:
                self.tradeDecorator2.Premium(-1 * self.direction2 * abs(self.b_premium2.GetValue()))
                self._updatePrice2()
        
    
    def _updateDomAmount1(self):
        self.updateValues = 0
        val1 = self.b_dom_amount1.GetValue()
        val2 = self.b_strike1.GetValue()
        if val1 and val2:
            if (self.strikeQuotation == 'Per Unit' and self.flipped == 0) or (self.strikeQuotation == 'Per Unit Inverse' and self.flipped == 1):
                self.b_for_amount1.SetValue(val1 / val2)
            else:
                self.b_for_amount1.SetValue(val1 * val2)
        
            if self.flipped == 0:
                quant = self.direction1 * self.b_for_amount1.GetValue()
            else:
                quant = self.direction1 * self.b_dom_amount1.GetValue()
            self.quantity1 = quant
        self.updateValues = 1
        
    
    def _updateDomAmount2(self):
        self.updateValues = 0
        val1 = self.b_dom_amount2.GetValue()
        val2 = self.b_strike2.GetValue()
        if val1 and val2:
            if (self.strikeQuotation == 'Per Unit' and self.flipped == 0) or (self.strikeQuotation == 'Per Unit Inverse' and self.flipped == 1):
                self.b_for_amount2.SetValue(val1 / val2)
            else:
                self.b_for_amount2.SetValue(val1 * val2)
            
            if self.flipped == 0:
                quant = self.direction2 * self.b_for_amount2.GetValue()
            else:
                quant = self.direction2 * self.b_dom_amount2.GetValue()
            self.quantity2 = quant
        self.updateValues = 1


    def _updateForAmount1(self):
        self.updateValues = 0
        val1 = self.b_for_amount1.GetValue()
        val2 = self.b_strike1.GetValue()
        if val1 and val2:
            if (self.strikeQuotation == 'Per Unit' and self.flipped == 0) or (self.strikeQuotation == 'Per Unit Inverse' and self.flipped == 1):
                self.b_dom_amount1.SetValue(val1 * val2)
            else:
                self.b_dom_amount1.SetValue(val1 / val2)
        
            if self.flipped == 0:
                quant = self.direction1 * self.b_for_amount1.GetValue()
            else:
                quant = self.direction1 * self.b_dom_amount1.GetValue()
            self.quantity1 = quant
        self.updateValues = 1

        
    def _updateForAmount2(self):
        self.updateValues = 0
        val1 = self.b_for_amount2.GetValue()
        val2 = self.b_strike2.GetValue()
        if val1 and val2:
            if (self.strikeQuotation == 'Per Unit' and self.flipped == 0) or (self.strikeQuotation == 'Per Unit Inverse' and self.flipped == 1):
                self.b_dom_amount2.SetValue(val1 * val2)
            else:
                self.b_dom_amount2.SetValue(val1 / val2)
        
            if self.flipped == 0:
                quant = self.direction2 * self.b_for_amount2.GetValue()
            else:
                quant = self.direction2 * self.b_dom_amount2.GetValue()
            self.quantity2 = quant
        self.updateValues = 1

        
    def _updatePrice1(self):
        premium1 = self.tradeDecorator1.Premium()
        for_amount1 = self.b_for_amount1.GetValue()
        dom_amount1 = self.b_dom_amount1.GetValue()
        
        if for_amount1 and dom_amount1 and premium1:
            if self.priceType == 1:
                value = (premium1 * 100) / for_amount1
            elif self.priceType == 2:
                value = (premium1 * 1000) / for_amount1
            elif self.priceType == 3:
                value = (premium1 * 100) / dom_amount1
            elif self.priceType == 4:
                value = (premium1 * 10000) / dom_amount1
            
            self.updateValues = 0
            self.b_premium1.SetValue(premium1)
            self.b_price1.SetValue(self.direction1 * -1 * value)
            self.updateValues = 1
        elif premium1 == 0.0:
            self.updateValues = 0
            self.b_premium1.SetValue(0.0)
            self.b_price1.SetValue(0.0)
            self.updateValues = 1
    
    def _updatePrice2(self):
        premium2 = self.tradeDecorator2.Premium()
        for_amount2 = self.b_for_amount2.GetValue()
        dom_amount2 = self.b_dom_amount2.GetValue()
        
        if for_amount2 and dom_amount2 and premium2:
            if self.priceType == 1:
                value = (premium2 * 100) / for_amount2
            elif self.priceType == 2:
                value = (premium2 * 1000) / for_amount2
            elif self.priceType == 3:
                value = (premium2 * 100) / dom_amount2
            elif self.priceType == 4:
                value = (premium2 * 10000) / dom_amount2
            
            self.updateValues = 0
            self.b_premium2.SetValue(premium2)
            self.b_price2.SetValue(self.direction2 * -1 * value)
            self.updateValues = 1
        elif premium2 == 0.0:
            self.updateValues = 0
            self.b_premium2.SetValue(0.0)
            self.b_price2.SetValue(0.0)
            self.updateValues = 1
            
        
    def _updateCurrencyPair(self):
        curr_pair = self.b_curr_pair.GetValue()
        
        self.forCurr = curr_pair.Currency1()
        self.domCurr = curr_pair.Currency2()
        
        if self.initCurrency == 1:
            self.insDecorator1.DomesticCurrency(self.domCurr)
            self.insDecorator2.DomesticCurrency(self.domCurr)
            
            self.insDecorator1.ForeignCurrency(self.forCurr)
            self.insDecorator2.ForeignCurrency(self.forCurr)
            
            self.tradeCurr = self.forCurr
            self.insDecorator1.Currency(self.tradeCurr)
            self.insDecorator2.Currency(self.tradeCurr)
            self._updatePremCurr()
            
            self.insQuotation = 'Pct of Nominal'
            self.priceType = 1
            
            self.strikeQuotation = 'Per Unit'
            
            tradeDate = self.b_tradeDate.GetValue()
            valueDate = curr_pair.SpotDate(tradeDate)
            self.b_valueDate.SetValue(valueDate)
            
            if self.b_expiry1.GetValue():
                self._updateExpiry1()
        
        self.c_price.Label('%%%s Price' % (self.forCurr.Name()))
        self.c_strike.Label('%s Per %s Strike' % (self.domCurr.Name(), self.forCurr.Name()))
        
        self.c_domAmountLabel.Label(self.domCurr.Name() + ' Amount:') 
        self.c_forAmountLabel.Label(self.forCurr.Name() + ' Amount:') 
        
        self.c_callPut1.Label('%s Put / %s Call' % (self.forCurr.Name(), self.domCurr.Name())) 
        self.c_callPut2.Label('%s Call / %s Put' % (self.forCurr.Name(), self.domCurr.Name()))
    
    def _checkBankingDay(self, value, fieldName):
        cal1 = self.forCurr.Calendar()
        cal2 = self.domCurr.Calendar()
        if cal1.IsNonBankingDay(cal1, cal2, value):
            return cal1.ModifyDate(cal1, cal2, value, 'Following')
        return value
    
    def _updateTradeDate(self):
        value = self.b_tradeDate.GetValue()
        value = self._checkBankingDay(value, 'Trade time')
        
        self.updateValues = 0
        self.b_tradeDate.SetValue(value)
        curr_pair = self.b_curr_pair.GetValue()
        valueDate = curr_pair.SpotDate(value)
        self.b_valueDate.SetValue(valueDate)
        self.updateValues = 1
    
    def _updateValueDate(self):
        value = self.b_valueDate.GetValue()
        value = acm.Time.AsDate(value)
        value = self._checkBankingDay(value, 'Value date')
        self.updateValues = 0
        self.b_valueDate.SetValue(value)
        self.updateValues = 1
        
    def _updateExpiry1(self):
        value = self.b_expiry1.GetValue()
        value = acm.Time.AsDate(value)
        value = self._checkBankingDay(value, 'Expiry day')

        self.updateValues = 0
        self.b_expiry1.SetValue(value)
        self.insDecorator1.ExpiryDate(value)
        self.b_delivery1.SetValue(self.insDecorator1.DeliveryDate())
        
        if self.strategy != 'Custom':
            self.b_expiry2.SetValue(value)
            self.insDecorator2.ExpiryDate(value)
            self.b_delivery2.SetValue(self.insDecorator2.DeliveryDate())
        self.updateValues = 1

    def _updateExpiry2(self):
        value = self.b_expiry2.GetValue()
        value = acm.Time.AsDate(value)
        value = self._checkBankingDay(value, 'Expiry day')
        
        self.updateValues = 0
        self.b_expiry2.SetValue(value)
        self.insDecorator2.ExpiryDate(value)
        self.b_delivery2.SetValue(self.insDecorator2.DeliveryDate())
        
        if self.strategy != 'Custom':
            self.b_expiry1.SetValue(value)
            self.insDecorator1.ExpiryDate(value)
            self.b_delivery1.SetValue(self.insDecorator1.DeliveryDate())
        self.updateValues = 1

    def _updateDelivery1(self):
        value = self.b_delivery1.GetValue()
        value = acm.Time.AsDate(value)
        
        self.updateValues = 0
        self.insDecorator1.DeliveryDate(value)
        self.b_delivery1.SetValue(self.insDecorator1.DeliveryDate())
        
        if self.strategy != 'Custom':
            self.insDecorator2.DeliveryDate(value)
            self.b_delivery2.SetValue(self.insDecorator2.DeliveryDate())
        self.updateValues = 1
    
    def _updateDelivery2(self):
        value = self.b_delivery2.GetValue()
        value = acm.Time.AsDate(value)

        self.updateValues = 0
        self.insDecorator2.DeliveryDate(value)
        self.b_delivery2.SetValue(self.insDecorator2.DeliveryDate())
        
        if self.strategy != 'Custom':
            self.insDecorator1.DeliveryDate(value)
            self.b_delivery1.SetValue(self.insDecorator1.DeliveryDate())
        self.updateValues = 1
    
    def _updatePremium1(self):
        price1 = self.b_price1.GetValue()
        for_amount1 = self.b_for_amount1.GetValue()
        dom_amount1 = self.b_dom_amount1.GetValue()
        
        if for_amount1 and dom_amount1 and price1:
            if self.priceType == 1:
                value = for_amount1 * (price1 / 100)
            elif self.priceType == 2:
                value = for_amount1 * (price1 / 10000)
            elif self.priceType == 3:
                value = dom_amount1 * (price1 / 100)
            elif self.priceType == 4:
                value = dom_amount1 * (price1 / 10000)
            self.updateValues = 0
            self.b_premium1.SetValue(self.direction1 * -1 * value)
            self.updateValues = 1
        elif price1 == 0.0:
            self.updateValues = 0
            self.b_premium1.SetValue(0.0)
            self.updateValues = 1

    def _updatePremium2(self):
        price2 = self.b_price2.GetValue()
        for_amount2 = self.b_for_amount2.GetValue()
        dom_amount2 = self.b_dom_amount2.GetValue()
        
        if for_amount2 and dom_amount2 and price2:
            if self.priceType == 1:
                value = for_amount2 * (price2 / 100)
            elif self.priceType == 2:
                value = for_amount2 * (price2 / 10000)
            elif self.priceType == 3:
                value = dom_amount2 * (price2 / 100)
            elif self.priceType == 4:
                value = dom_amount2 * (price2 / 10000)
            self.updateValues = 0
            self.b_premium2.SetValue(self.direction2 * -1 * value)
            self.updateValues = 1
        elif price2 == 0.0:
            self.updateValues = 0
            self.b_premium2.SetValue(0.0)
            self.updateValues = 1

    def _updatePremCurr(self):
        self.c_premCurr.SetData(self.tradeCurr)
    
    # Buttons Callbacks
    def _CallPut1Changed(self, arg=0, arg2=0):
        if self.insDecorator1.OptionType() == 'Put':
            self.c_callPut1.Label('%s Call / %s Put' % (self.forCurr.Name(), self.domCurr.Name())) 
            self.insDecorator1.OptionType('Call')
        else:
            self.c_callPut1.Label('%s Put / %s Call' % (self.forCurr.Name(), self.domCurr.Name())) 
            self.insDecorator1.OptionType('Put')
        
        if self.strategy != 'Custom' and self.callPutChange == 1:
            self.callPutChange = 0
            self._CallPut2Changed()
            self.callPutChange = 1
        self._Changed(True)

    def _CallPut2Changed(self, arg=0, arg2=0):
        if self.insDecorator2.OptionType() == 'Put':
            self.c_callPut2.Label('%s Call / %s Put' % (self.forCurr.Name(), self.domCurr.Name())) 
            self.insDecorator2.OptionType('Call')
        else:
            self.c_callPut2.Label('%s Put / %s Call' % (self.forCurr.Name(), self.domCurr.Name())) 
            self.insDecorator2.OptionType('Put')
        
        if self.strategy != 'Custom' and self.callPutChange == 1:
            self.callPutChange = 0
            self._CallPut1Changed()
            self.callPutChange = 1
        self._Changed(True)

    def _StrikeQuotationChanged(self, arg=0, arg2=0):
        if self.strikeQuotation == 'Per Unit':
            self.c_strike.Label('%s Per %s Strike' % (self.forCurr.Name(), self.domCurr.Name()))
            self.strikeQuotation = 'Per Unit Inverse'
        else:
            self.c_strike.Label('%s Per %s Strike' % (self.domCurr.Name(), self.forCurr.Name()))
            self.strikeQuotation = 'Per Unit'
        
        self.insDecorator1.StrikeQuotation(acm.FQuotation[self.strikeQuotation])
        self.insDecorator2.StrikeQuotation(acm.FQuotation[self.strikeQuotation])
        
        self._updateForAmount1()
        self._updatePremium1()
        self._updateForAmount2()
        self._updatePremium2()
        
        self._Changed(True)
     
    def _Direction1Changed(self, arg=0, arg2=0):
        if self.direction1 == 1:
            self.c_direction1.Label('Sell')
        else:
            self.c_direction1.Label('Buy')
            
        self.direction1 = -1 * self.direction1
        self.quantity1 = -1 * self.quantity1
        
        self.updateValues = 0
        self._updatePremium1()
        self.updateValues = 1
        
        if self.directionChange == 1:
            
            if self.strategy == 'Custom':
                pass
            elif self.strategy in ('Collar', 'Synthetic Forward'):
                self.directionChange = 0
                self._Direction2Changed()
                self.directionChange = 1
            else:
                self.direction2 = -1 * self.direction1
                self.directionChange = 0
                self._Direction2Changed()
                self.directionChange = 1
        
        self._Changed(True)
            
        
    def _Direction2Changed(self, arg=0, arg2=0):
        if self.direction2 == 1:
            self.c_direction2.Label('Sell')
        else:
            self.c_direction2.Label('Buy')
            
        self.direction2 = -1 * self.direction2
        self.quantity2 = -1 * self.quantity2
        
        self.updateValues = 0
        self._updatePremium2()
        self.updateValues = 1
        
        if self.directionChange == 1:
            if self.strategy == 'Custom':
                pass
            elif self.strategy in  ('Collar', 'Synthetic Forward'):
                self.directionChange = 0
                self._Direction1Changed()
                self.directionChange = 1
            else:
                self.direction1 = -1 * self.direction2
                self.directionChange = 0
                self._Direction1Changed()
                self.directionChange = 1
        
        self._Changed(True)
        
    def _Flip(self):
        # flip currencies
        tempCurr = self.forCurr
        self.forCurr = self.domCurr
        self.domCurr = tempCurr
        
        self.insDecorator1.DomesticCurrency(self.domCurr)
        self.insDecorator2.DomesticCurrency(self.domCurr)
        
        self.insDecorator1.ForeignCurrency(self.forCurr)
        self.insDecorator2.ForeignCurrency(self.forCurr)
        
        # flip strike quotation
        if self.strikeQuotation == 'Per Unit':
            self.c_strike.Label('%s Per %s Strike' % (self.forCurr.Name(), self.domCurr.Name()))
            self.strikeQuotation = 'Per Unit Inverse'
        else:
            self.c_strike.Label('%s Per %s Strike' % (self.domCurr.Name(), self.forCurr.Name()))
            self.strikeQuotation = 'Per Unit'
        
        self.insDecorator1.StrikeQuotation(acm.FQuotation[self.strikeQuotation])
        self.insDecorator2.StrikeQuotation(acm.FQuotation[self.strikeQuotation])
        
        # flip amounts
        tempAmount = -1 * self.tradeDecorator1.AmountForeign()
        self.tradeDecorator1.AmountDomestic(tempAmount)
        
        tempAmount = -1 * self.tradeDecorator2.AmountForeign()
        self.tradeDecorator2.AmountDomestic(tempAmount)
        
        # flip amounts
        if self.flipped == 1:
            self.quantity1 = (self.direction1 * self.b_for_amount1.GetValue())
            self.quantity2 = (self.direction2 * self.b_for_amount2.GetValue())
        else:
            self.quantity1 = (-1 * self.direction1 * self.b_dom_amount1.GetValue())
            self.quantity2 = (-1 * self.direction2 * self.b_dom_amount2.GetValue())
        
        # flip types
        if self.insDecorator1.OptionType() == 'Put':
            self.insDecorator1.OptionType('Call')
        else:
            self.insDecorator1.OptionType('Put')
        
        if self.insDecorator2.OptionType() == 'Put':
            self.insDecorator2.OptionType('Call')
        else:
            self.insDecorator2.OptionType('Put')
        
    
    def _PriceChanged(self, arg=0, arg2=0):
        if self.priceType == 1:
            self.c_price.Label('%s Per %s Price' % (self.domCurr.Name(), self.forCurr.Name()))
            self.insQuotation = 'Points of UndCurr'
            self.tradeCurr = self.domCurr
            self.priceType = 2
        elif self.priceType == 2:
            self.c_price.Label('%%%s Price' % (self.domCurr.Name()))
            self.insQuotation = 'Pct of Nominal'
            self.tradeCurr = self.domCurr
            self._Flip()
            self.flipped = 1
            self.priceType = 3
        elif self.priceType == 3:
            self._Flip()
            self.flipped = 0
            self.c_price.Label('%s Per %s Price' % (self.forCurr.Name(), self.domCurr.Name()))
            self.insQuotation = 'Points of UndCurr'
            self.tradeCurr = self.forCurr
            self._Flip()
            self.flipped = 1
            self.priceType = 4
        elif self.priceType == 4:
            self._Flip()
            self.flipped = 0
            self.c_price.Label('%%%s Price' % (self.forCurr.Name()))
            self.insQuotation = 'Pct of Nominal'
            self.tradeCurr = self.forCurr
            self.priceType = 1
            
        self.insDecorator1.Currency(self.tradeCurr)
        self.insDecorator2.Currency(self.tradeCurr)
        
        self.insDecorator1.Quotation(acm.FQuotation[self.insQuotation])
        self.insDecorator2.Quotation(acm.FQuotation[self.insQuotation])
        
        self._updatePremium1()
        self._updatePremium2()
        self._updatePremCurr()
        
        self._Changed(True)
   

    def _StrategyChanged(self, arg=0, arg2=0):
        self.strategy = self.c_strategy.GetData()
        if self.strategy in ('Collar', 'Synthetic Forward'):
            self.direction1 = 1
            self.c_direction1.Label('Buy')
            self.direction2 = -1
            self.c_direction2.Label('Sell')
        else:
            self.direction1 = 1
            self.c_direction1.Label('Buy')
            self.direction2 = 1
            self.c_direction2.Label('Buy')
            
        self.quantity1 = self.direction1 * abs(self.quantity1)
        self.quantity2 = self.direction2 * abs(self.quantity2)
        
        self._updatePremium1()
        self._updatePremium2()
        
        self.insDecorator1.OptionType('Call')
        self.insDecorator2.OptionType('Put')
        
        if self.b_curr_pair.GetValue() != None:
            self._CallPut1Changed()
            if self.strategy == 'Custom':
                 self._CallPut2Changed()
        
        if self.strategy != 'Custom':
            self.b_expiry2.SetValue(self.b_expiry1.GetValue())
        
        if self.strategy in ('Straddle', 'Synthetic Forward'):
            self.b_strike2.SetValue(self.b_strike1.GetValue())
        
        if self.strategy in ('Synthetic Forward'):
            self.b_for_amount2.SetValue(self.b_for_amount1.GetValue())
            
        choice = acm.FChoiceList.Select("name = %s" % (self.strategy))[0]

        self.insDecorator1.ProductTypeChlItem(choice)
        self.insDecorator2.ProductTypeChlItem(choice)
        
        self._Changed(True)
        
        
    def _StrategyIdChanged(self, arg=0, arg2=0):
        tradeNbr = self.c_strategyId.GetData()
        tradeNbr = tradeNbr.replace(',', '')
        try:
            tradeNbr = int(tradeNbr)
        except Exception as err:
            self.c_strategyId.SetData('')
            
        if tradeNbr:
            trade = acm.FTrade[tradeNbr]
            if trade:
                instrument = trade.Instrument()
                if trade.Instrument().InsType() == 'Option' and trade.Instrument().UnderlyingType() == 'Curr':
                    trxTrade = 0
                    trades = trade.TrxTrades()
                    for t in trades:
                        if t != trade:
                            trxTrade = t
                            
                    if trxTrade != 0 and self.setStrategyID == 1:
                        self._OpenStrategy(trade, trxTrade)
                        
            
    def _ForwarSpotChanged(self, arg=0, arg2=0):
        fs = self.c_forwardSpot.Label()
        if fs == 'Spot':
            self.c_forwardSpot.Label('Forward')
            valueDate = self.insDecorator1.DeliveryDate()
        else:
            self.c_forwardSpot.Label('Spot')
            tradeDate = self.b_tradeDate.GetValue()
            valueDate = self.b_curr_pair.GetValue().SpotDate(tradeDate)
        
        self.b_valueDate.SetValue(valueDate)
        
        self._Changed(True)
    
    def _CounterpartyChanged(self, arg=0, arg2=0):
        self._Changed(True)
    
    @staticmethod
    def _setAdditionalInfo(object, additionalInfoName, value):
        spec = acm.FAdditionalInfoSpec[additionalInfoName]
        if not spec:
            raise Exception('Could not load FAdditionalInfo [%s].' % additionalInfoName)

        query = 'addInf = %i and recaddr = %i' % (spec.Oid(), object.Oid())
        additionalInfo = acm.FAdditionalInfo.Select01(query, 'More than one FAdditionalInfo returned for ' + query)
        if not additionalInfo:
            additionalInfo = acm.FAdditionalInfo()
            additionalInfo.AddInf(spec)
            additionalInfo.Recaddr(object.Oid())

        additionalInfo.FieldValue(value)
        additionalInfo.Commit()
    
    def _CommitInstrument(self, instrument, clone):
        try:
            instrument.Apply(clone)
            instrument.Quotation(acm.FQuotation[self.insQuotation])
            instrument.Commit()
        except Exception as err:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'Instrument did not commit %s' % (err))
            return False
        return True

    def _CommitTrade1(self, instrument):
        trade = self.trade1
        trade.Instrument(instrument)
        trade.Currency(self.tradeCurr)
        trade.Price(self.b_price1.GetValue())
        trade.Quantity(self.quantity1)
        trade.Premium(self.b_premium1.GetValue())
        
        trade.TradeTime(self.b_tradeDate.GetValue())
        trade.AcquireDay(self.b_valueDate.GetValue())
        trade.ValueDay(self.b_valueDate.GetValue())
        trade.Counterparty(self._GetParty())
        trade.Acquirer(self.b_acquirer.GetValue())
        trade.Trader(self.b_trader.GetValue())
        trade.Portfolio(self.b_portfolio.GetValue())
        trade.Status(self.b_status.GetValue())
        
        if self.b_salesPerson.GetValue() != None:
            trade.SalesPerson(self.b_salesPerson.GetValue())
        if self.b_salesCredit.GetValue() != None:
            trade.SalesCredit(self.b_salesCredit.GetValue())
        
        try:
            self.trade1Orig.Apply(trade)
            self.trade1Orig.Commit()
            self.trade1Orig.TrxTrade(self.trade1Orig.Oid())
            self.trade1Orig.Commit()
            if self.b_valueAddCredit.GetValue() != None:
                self._setAdditionalInfo(self.trade1Orig, 'ValueAddCredits', self.b_valueAddCredit.GetValue())
                self.trade1Orig.Commit()
        except Exception as err:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'Trade did not commit %s' % (err))
            return False
            
        self.c_tradeNbr1.SetData(self.trade1Orig.Oid())

        return self.trade1Orig.Oid()

    def _GetParty(self):
        if acm.FCounterParty[self.c_counterparty.GetData()]:
            return acm.FCounterParty[self.c_counterparty.GetData()]
        if acm.FClient[self.c_counterparty.GetData()]:
            return acm.FClient[self.c_counterparty.GetData()]
        return None

    def _CommitTrade2(self, instrument, trxNbr):
        trade = self.trade2
        
        trade.Instrument(instrument)
        trade.Currency(self.tradeCurr)
        trade.Price(self.b_price2.GetValue())
        trade.Quantity(self.quantity2)
        trade.Premium(self.b_premium2.GetValue())
        
        trade.TradeTime(self.b_tradeDate.GetValue())
        trade.AcquireDay(self.b_valueDate.GetValue())
        trade.ValueDay(self.b_valueDate.GetValue())
        trade.Counterparty(self._GetParty())
        trade.Acquirer(self.b_acquirer.GetValue())
        trade.Trader(self.b_trader.GetValue())
        trade.Portfolio(self.b_portfolio.GetValue())
        trade.Status(self.b_status.GetValue())
        
        trade.TrxTrade(trxNbr)
        
        try:
            self.trade2Orig.Apply(trade)
            self.trade2Orig.Commit()
        except Exception as err:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'Trade did not commit %s' % (err))
            return False
        
        self.c_tradeNbr2.SetData(self.trade2Orig.Oid())

    
    def _Commit(self):
        if self._ValidateInputs():
            if self._CommitInstrument(self.ins1Orig, self.ins1):
                self.c_insName1.SetData(self.ins1Orig.Name())
                trxNbr = self._CommitTrade1(self.ins1Orig)
                
                if trxNbr:
                    if self._CommitInstrument(self.ins2Orig, self.ins2):
                        self.c_insName2.SetData(self.ins2Orig.Name())
                        
                        self._CommitTrade2(self.ins2Orig, trxNbr)
                        
                        self.setStrategyID = 0
                        self.c_strategyId.SetData(trxNbr)
                        self.setStrategyID = 1
                        
                        if self.showTrades and self.initShowTrades:
                            acm.StartApplication("Instrument Definition", self.trade1Orig)
                            acm.StartApplication("Instrument Definition", self.trade2Orig)
                            self.initShowTrades = False
                        
                        self._Changed(False)
                        self.tradesExist = True
                        
                        self.ins1 = self.ins1Orig.Clone()
                        self.insDecorator1 = acm.FOptionDecorator(self.ins1, self.businessLogicHandler)
                        self.ins2 = self.ins2Orig.Clone()
                        self.insDecorator2 = acm.FOptionDecorator(self.ins2, self.businessLogicHandler)
                        

    def _Save(self, arg=0, arg2=0):
        self._Commit()
    
    def _SaveNew(self, arg=0, arg2=0):
        if self.tradesExist:
            response1 = acm.UX().Dialogs().MessageBoxYesNo(self.fuxDlg.Shell(), 'Question', 'Do you wish to create new instruments?')
            if response1 == 'Button1':
                self.ins1Orig = acm.FOption()
                self.ins2Orig = acm.FOption()
                self.ins1.Name(self.insDecorator1.SuggestName())
                self.ins2.Name(self.insDecorator2.SuggestName())
            
            response2 = acm.UX().Dialogs().MessageBoxOKCancel(self.fuxDlg.Shell(), 'Question', 'Do you really want to create new trades?')
            if response2 == 'Button1':
                self.trade1Orig = acm.FTrade()
                self.trade2Orig = acm.FTrade()
                
            if (response1 == 'Button1' and response2 == 'Button1') or response2 == 'Button1':
                self._Commit()
        else:
            self._Commit()

    def _Changed(self, trueFalse):
        self.saveEnabled = trueFalse
        self.c_save.Enabled(self.saveEnabled)
        self.c_saveNew.Enabled(self.saveEnabled)

    def _ValidateInputs(self):
        
        if self.b_curr_pair.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Currency Pair.')
            return False
        
        if self.b_expiry1.GetValue() in (None, '1899-12-30 00:00:00'):
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter an Expiry Date for trade 1.')
            return False
            
        if self.b_expiry2.GetValue() in (None, '1899-12-30 00:00:00'):
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter an Expiry Date for trade 2.')
            return False
        
        if self.b_delivery1.GetValue() in (None, '1899-12-30 00:00:00'):
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Delivery Date for trade 1.')
            return False
        
        if self.b_delivery2.GetValue() in (None, '1899-12-30 00:00:00'):
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Delivery Date for trade 2.')
            return False
            
        if self.b_strike1.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Strike Price for trade 1.')
            return False
            
        if self.b_strike2.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Strike Price for trade 2.')
            return False
            
        if self.b_for_amount1.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Foreign Amount for trade 1.')
            return False
            
        if self.b_for_amount2.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Foreign Amount for trade 2.')
            return False
            
        if self.b_dom_amount1.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Domestic Amount for trade 1.')
            return False
            
        if self.b_dom_amount2.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Domestic Amount for trade 2.')
            return False
            
        if self.b_price1.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Price for trade 1.')
            return False
            
        if self.b_price2.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Price for trade 2.')
            return False
        
        if self.b_premium1.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Premium for trade 1.')
            return False
            
        if self.b_premium2.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Premium for trade 2.')
            return False
        
        if self.b_portfolio.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Portfolio.')
            return False
            
        if self.b_acquirer.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Acquirer.')
            return False
        
        if self.b_trader.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Trader.')
            return False
            
        if self.b_tradeDate.GetValue() in (None, '1899-12-30 00:00:00'):
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Trade Date.')
            return False
            
        if self.b_valueDate.GetValue() in (None, '1899-12-30 00:00:00'):
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Value Date.')
            return False
        
        if self.b_trader.GetValue() == None:
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Trader.')
            return False
    
        if self.c_counterparty.GetData() == '':
            acm.UX().Dialogs().MessageBoxInformation(self.fuxDlg.Shell(), 'You must enter a Counterparty.')
            return False
        
        return True
        
        
    def _setPriceType(self):
        self.insQuotation = self.insDecorator1.Quotation().Name()
        self.tradeCurr = self.insDecorator1.Currency()
        
        if self.insQuotation == 'Pct of Nominal' and self.tradeCurr == self.forCurr:
            self.c_price.Label('%%%s Price' % (self.forCurr.Name()))
            self.priceType = 1
        elif self.insQuotation == 'Points of UndCurr' and self.tradeCurr == self.domCurr:
            self.c_price.Label('%s Per %s Price' % (self.domCurr.Name(), self.forCurr.Name()))
            self.priceType = 2
        elif self.insQuotation == 'Pct of Nominal' and self.tradeCurr == self.domCurr:
            self.c_price.Label('%%%s Price' % (self.domCurr.Name()))
            tempCurr = self.forCurr
            self.forCurr = self.domCurr
            self.domCurr = tempCurr
            self.insDecorator1.DomesticCurrency(self.domCurr)
            self.insDecorator2.DomesticCurrency(self.domCurr)
        
            self.insDecorator1.ForeignCurrency(self.forCurr)
            self.insDecorator2.ForeignCurrency(self.forCurr)
            self.priceType = 3
            self.flipped = 1
        elif self.insQuotation == 'Points of UndCurr' and self.tradeCurr == self.forCurr:
            self.c_price.Label('%s Per %s Price' % (self.forCurr.Name(), self.domCurr.Name()))
            tempCurr = self.forCurr
            self.forCurr = self.domCurr
            self.domCurr = tempCurr
            self.insDecorator1.DomesticCurrency(self.domCurr)
            self.insDecorator2.DomesticCurrency(self.domCurr)
        
            self.insDecorator1.ForeignCurrency(self.forCurr)
            self.insDecorator2.ForeignCurrency(self.forCurr)
            self.priceType = 4
            self.flipped = 1
            
    def _OpenStrategy(self, trade, trxTrade):
    
        self.trade1Orig = trade
        self.trade1 = self.trade1Orig.Clone()
        self.tradeDecorator1 = acm.FTradeLogicDecorator(self.trade1, self.businessLogicHandler)
        
        self.ins1Orig = self.trade1.Instrument()
        self.ins1 = self.ins1Orig.Clone()
        self.insDecorator1 = acm.FOptionDecorator(self.ins1, self.businessLogicHandler)
        
        self.trade2Orig = trxTrade
        self.trade2 = self.trade2Orig.Clone()
        self.tradeDecorator2 = acm.FTradeLogicDecorator(self.trade2, self.businessLogicHandler)
        
        self.ins2Orig = self.trade2.Instrument()
        self.ins2 = self.ins2Orig.Clone()
        self.insDecorator2 = acm.FOptionDecorator(self.ins2, self.businessLogicHandler)
        self.tradeDecorator2.Instrument(self.ins2)
        
        self.strategy = self.insDecorator1.ProductTypeChlItem().Name()
        self.c_strategy.SetData(self.strategy)
        
        self.initCurrency = 0
        self.b_curr_pair.SetValue(self.trade1.CurrencyPair())
        self.initCurrency = 1
        
        self.b_expiry1.SetValue(self.insDecorator1.ExpiryDate())
        self.b_expiry2.SetValue(self.insDecorator2.ExpiryDate())
        
        self.b_delivery1.SetValue(self.insDecorator1.DeliveryDate())
        self.b_delivery2.SetValue(self.insDecorator2.DeliveryDate())
        
        self.b_cut1.SetValue(self.insDecorator1.FixingSource())
        self.b_cut2.SetValue(self.insDecorator2.FixingSource())
        
        self.b_strike1.SetValue(self.insDecorator1.StrikePrice())
        self.b_strike2.SetValue(self.insDecorator2.StrikePrice())
        
        self._setPriceType()
        self._updatePremCurr()
        self.strikeQuotation = self.insDecorator1.StrikeQuotation().Name()
        
        if (self.trade1.Quantity() > 0 and self.flipped == 0) or (self.trade1.Quantity() < 0 and self.flipped == 1):
            self.direction1 = 1
            self.c_direction1.Label('Buy')
        else:
            self.direction1 = -1
            self.c_direction1.Label('Sell')
        
        if (self.trade2.Quantity() > 0 and self.flipped == 0) or (self.trade2.Quantity() < 0 and self.flipped == 1):
            self.direction2 = 1
            self.c_direction2.Label('Buy')
        else:
            self.direction2 = -1
            self.c_direction2.Label('Sell')
        
        if self.insDecorator1.OptionType() == 'Put':
            self.c_callPut1.Label('%s Put / %s Call' % (self.forCurr.Name(), self.domCurr.Name())) 
        else:
            self.c_callPut1.Label('%s Call / %s Put' % (self.forCurr.Name(), self.domCurr.Name())) 
        
        if self.insDecorator2.OptionType() == 'Put':
            self.c_callPut2.Label('%s Put / %s Call' % (self.forCurr.Name(), self.domCurr.Name())) 
        else:
            self.c_callPut2.Label('%s Call / %s Put' % (self.forCurr.Name(), self.domCurr.Name())) 
        
        if self.flipped == 0:
            self.b_for_amount1.SetValue(abs(self.tradeDecorator1.AmountForeign()))
            self.b_for_amount2.SetValue(abs(self.tradeDecorator2.AmountForeign()))
        else:
            self.b_for_amount1.SetValue(abs(self.tradeDecorator1.AmountDomestic()))
            self.b_for_amount2.SetValue(abs(self.tradeDecorator2.AmountDomestic())) 
        
        if self.strikeQuotation == 'Per Unit':
            self.c_strike.Label('%s Per %s Strike' % (self.domCurr.Name(), self.forCurr.Name()))
        else:
            self.c_strike.Label('%s Per %s Strike' % (self.forCurr.Name(), self.domCurr.Name()))
        
        if self.trade1.ValueDay() == self.insDecorator1.DeliveryDate():
            self.c_forwardSpot.Label('Forward')
        
        self.updateValues = 0
        
        self.b_price1.SetValue(self.trade1.Price())
        self.b_price2.SetValue(self.trade2.Price())
        
        self.b_premium1.SetValue(self.trade1.Premium())
        self.b_premium2.SetValue(self.trade2.Premium())
        
        self.c_counterparty.SetData(self.trade1.Counterparty())
        self.b_portfolio.SetValue(self.trade1.Portfolio())
        self.b_acquirer.SetValue(self.trade1.Acquirer())
        self.b_trader.SetValue(self.trade1.Trader())
        self.b_tradeDate.SetValue(self.trade1.TradeTime())
        self.b_valueDate.SetValue(self.trade1.ValueDay())
        self.b_status.SetValue(self.trade1.Status())
        self.b_salesPerson.SetValue(self.trade1.SalesPerson())
        self.b_salesCredit.SetValue(self.trade1.SalesCredit())
        self.trade1.RegisterInStorage()
        self.b_valueAddCredit.SetValue(self.trade1.AdditionalInfo().ValueAddCredits())
        self.updateValues = 1
        
        self.c_tradeNbr1.SetData(self.trade1.Oid())
        self.c_tradeNbr2.SetData(self.trade2.Oid())
        
        self.c_insName1.SetData(self.ins1.Name())
        self.c_insName2.SetData(self.ins2.Name())
        self.tradesExist = True
        self._Changed(False)
    
    def _ClearValues(self):
        self.__init__()
    
        dict = self.binder.GetValuesByName()
        for key in dict.Keys():
            dict.AtPut(key, None)
        self.binder.SetValuesByName(dict)
        
        self.c_tradeNbr1.SetData('')
        self.c_tradeNbr2.SetData('')
        
        self.c_insName1.SetData('')
        self.c_insName2.SetData('')
        self.c_strategyId.SetData('')
        
        self._SetDefaultValues()
        
    def _Clear(self, arg=0, arg2=0):
        if self.saveEnabled:
            response1 = acm.UX().Dialogs().MessageBoxOKCancel(self.fuxDlg.Shell(), 'Question', 'The current trades have not been saved.\nDo you wish to disregard the changes?')
            if response1 == 'Button1':
                self._ClearValues()
        else:
            self._ClearValues()
    
    def _ShowTrades(self, arg=0, arg2=0):
        value = self.c_show.Checked()
        self.showTrades = value
        self.initShowTrades = True
    
            
    def _SetDefaultValues(self):
        # Default Values
        self.c_forwardSpot.Label('Spot')
        self.c_show.Checked(False)
        
        nsTime = acm.Time()
        self.b_tradeDate.SetValue(nsTime.TimeNow())
        
        self.c_strategy.SetData('Straddle')
        self.direction1 = 1
        self.c_direction1.Label('Buy')
        self.direction2 = 1
        self.c_direction2.Label('Buy')

        from FBDPGui import Parameters
        param = Parameters('FXO_Strategy_Params')
        if param.currPair not in (None, 'None', ''):
            self.b_curr_pair.SetValue(acm.FCurrencyPair[param.currPair])
            self._updateCurrencyPair()
            self.b_expiry1.SetValue(nsTime.TimeNow())
            
        self.b_strike1.SetValue(param.strike1)
        self.b_strike2.SetValue(param.strike2)
        self.c_counterparty.SetData(param.counterparty)
        self.b_portfolio.SetValue(param.portfolio)
        self.b_acquirer.SetValue(param.acquirer)
        self.b_for_amount1.SetValue(param.forAmount1)
        self.b_for_amount2.SetValue(param.forAmount2)
        self.b_premium1.SetValue(param.premium1)
        self.b_premium2.SetValue(param.premium2)
        self.b_price1.SetValue(param.price1)
        self.b_price2.SetValue(param.price2)
        self.b_cut1.SetValue(param.cut1)
        self.b_cut2.SetValue(param.cut2)
        self.b_status.SetValue(param.status)
        if param.trader == '':
            self.b_trader.SetValue(acm.User().Name())
        else:
            self.b_trader.SetValue(param.trader)
        self._Changed(False)

    def _PopulateCounterparty(self):
        parties = acm.FCounterParty.Select('').AsSet()
        parties.Union(acm.FClient.Select(''))
        parties_list = sorted(parties, key=lambda this: this.Name())
        for i in parties_list:
            self.c_counterparty.AddItem(i.Name()) 
    
    def PopulateData(self):
        self.c_strategy.AddItem('Straddle')
        self.c_strategy.AddItem('Strangle')
        self.c_strategy.AddItem('Collar')
        self.c_strategy.AddItem('Synthetic Forward')
        self.c_strategy.AddItem('Custom')
        
        self._PopulateCounterparty()
        
        self.c_insName1.Editable(False)
        self.c_insName2.Editable(False)
        self.c_tradeNbr1.Editable(False)
        self.c_tradeNbr2.Editable(False)
        self.c_premCurr.Editable(False)
        
    def HandleCreate(self, dlg, layout):
        self.fuxDlg = dlg
        self.fuxDlg.Caption('FX Option Strategy')
        self.binder.AddLayout(layout)
        
        self.c_strategy = layout.GetControl('strategy')
        self.c_strategy.AddCallback('Changed', self._StrategyChanged, self)
        
        self.c_strategyId = layout.GetControl('strategyId')
        self.c_strategyId.AddCallback('Changed', self._StrategyIdChanged, self)
        
        self.c_direction1 = layout.GetControl('direction1')
        self.c_direction1.AddCallback('Activate', self._Direction1Changed, self)
        
        self.c_direction2 = layout.GetControl('direction2')
        self.c_direction2.AddCallback('Activate', self._Direction2Changed, self)
        
        self.c_strike = layout.GetControl('strike')
        self.c_strike.AddCallback('Activate', self._StrikeQuotationChanged, self)
        
        self.c_domAmountLabel = layout.GetControl('domAmountLabel')
        self.c_forAmountLabel = layout.GetControl('forAmountLabel')
        
        self.c_callPut1 = layout.GetControl('callPut1')
        self.c_callPut1.AddCallback('Activate', self._CallPut1Changed, self)
        
        self.c_callPut2 = layout.GetControl('callPut2')
        self.c_callPut2.AddCallback('Activate', self._CallPut2Changed, self)
        
        self.c_price = layout.GetControl('price')
        self.c_price.AddCallback('Activate', self._PriceChanged, self)
        
        self.c_counterparty = layout.GetControl('counterparty')
        self.c_counterparty.AddCallback('Changed', self._CounterpartyChanged, self)
        
        self.c_insName1 = layout.GetControl('insName1')
        self.c_insName2 = layout.GetControl('insName2')
        
        self.c_tradeNbr1 = layout.GetControl('tradeNbr1')
        self.c_tradeNbr2 = layout.GetControl('tradeNbr2')
        
        self.c_premCurr = layout.GetControl('premCurr')
        
        self.c_forwardSpot = layout.GetControl('forwardSpot')
        self.c_forwardSpot.AddCallback('Activate', self._ForwarSpotChanged, self)
        
        self.c_save = layout.GetControl('save')
        self.c_save.AddCallback('Activate', self._Save, self)
        
        self.c_saveNew = layout.GetControl('saveNew')
        self.c_saveNew.AddCallback('Activate', self._SaveNew, self)
        
        self.c_new = layout.GetControl('new')
        self.c_new.AddCallback('Activate', self._Clear, self)
        
        self.c_show = layout.GetControl('showTrades')
        self.c_show.AddCallback('Activate', self._ShowTrades, self)
        
        self.PopulateData()
        self._SetDefaultValues()
        
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. BeginHorzBox('None')
        b.  BeginVertBox('None')
        b.   AddSpace(10)
        b.   AddButton('new', 'New')
        b.   AddSpace(10)
        b.   AddInput('strategyId', 'Strategy ID')
        b.   AddOption('strategy', 'Strategy')
        self.b_curr_pair.BuildLayoutPart(b, 'Currency Pair')
        b.  EndBox()
        
        b.  BeginVertBox('None')
        b.   AddSpace(10)
        b.   AddLabel('temp', '')
        b.  EndBox()
        b. EndBox()
        
        b. BeginVertBox('None')
        b.  AddSpace(20)
        b. EndBox()
        
        # Labels
        b. BeginVertBox('EtchedIn', 'Vanilla European')
        b. BeginHorzBox('None')
        b.  BeginVertBox('None')
        b.   AddLabel('expLabel', 'Expiry:')
        b.   AddLabel('cutLabel', 'Cut Time:')
        b.   AddLabel('delLabel', 'Delivery:')
        b.   AddLabel('dirLabel', 'Direction:')
        b.   AddButton('strike', '     FX2 per FX1 Strike    ', 0, 1)
        b.   AddLabel('optTypeLabel', 'Option Type:')
        b.   AddLabel('forAmountLabel', 'FX2 Amount:      ')
        b.   AddLabel('domAmountLabel', 'FX1 Amount:      ')
        b.   AddButton('price', '        %FX2 Price             ', 0, 1)
        b.   AddLabel('premium', 'Premium:')
        b.   AddLabel('insName', 'Instrument Name:')
        b.   AddLabel('tradeNbr', 'Trade Number:')
        b.  EndBox()
        
        # Inputs
        b. BeginVertBox('None')
        b.  BeginHorzBox('None')
        self.b_expiry1.BuildLayoutPart(b, '')
        self.b_expiry2.BuildLayoutPart(b, '')
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_cut1.BuildLayoutPart(b, '')
        self.b_cut2.BuildLayoutPart(b, '') 
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_delivery1.BuildLayoutPart(b, '')
        self.b_delivery2.BuildLayoutPart(b, '')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.   AddButton('direction1', 'Buy', 0, 0)
        b.   AddSpace(60)
        b.   AddButton('direction2', 'Buy', 0, 0)
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_strike1.BuildLayoutPart(b, '') 
        self.b_strike2.BuildLayoutPart(b, '')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.   AddButton('callPut1', '     FX2 Put / FX1 Call      ', 0, 1)
        b.   AddSpace(20)
        b.   AddButton('callPut2', '     FX1 Put / FX2 Call      ', 0, 1)
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_for_amount1.BuildLayoutPart(b, '') 
        self.b_for_amount2.BuildLayoutPart(b, '') 
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_dom_amount1.BuildLayoutPart(b, '') 
        self.b_dom_amount2.BuildLayoutPart(b, '') 
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_price1.BuildLayoutPart(b, '')
        self.b_price2.BuildLayoutPart(b, '')
        b.  EndBox()
        b.  BeginHorzBox('None')
        self.b_premium1.BuildLayoutPart(b, '')
        self.b_premium2.BuildLayoutPart(b, '')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.   AddInput('insName1', '')
        b.   AddInput('insName2', '')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.   AddInput('tradeNbr1', '')
        b.   AddInput('tradeNbr2', '')
        b.  EndBox()
        b. EndBox()
        b. EndBox()
        b. EndBox()
        
        b. BeginVertBox('None')
        b.  AddSpace(20)
        b. EndBox()

        # Common trade details
        b. BeginHorzBox('None')
        b. BeginVertBox('None')
        b.  AddOption('counterparty', 'Counterparty')
        self.b_portfolio.BuildLayoutPart(b, 'Portfolio')
        self.b_acquirer.BuildLayoutPart(b, 'Acquirer')
        self.b_tradeDate.BuildLayoutPart(b, 'Trade Time')
        b.  BeginHorzBox('None')
        self.b_valueDate.BuildLayoutPart(b, 'Value Day')
        b.   AddButton('forwardSpot', 'Spot')
        b.  EndBox()
        b.  AddInput('premCurr', 'Premium Currency')
        self.b_trader.BuildLayoutPart(b, 'Trader')
        self.b_salesPerson.BuildLayoutPart(b, 'Sales Person')
        self.b_salesCredit.BuildLayoutPart(b, 'Sales Credit')
        self.b_valueAddCredit.BuildLayoutPart(b, 'Value Add')
        self.b_status.BuildLayoutPart(b, 'Status')
        b.  EndBox()
        b. EndBox()
        
        b. BeginVertBox('None')
        b.   AddSpace(15)
        b.  EndBox()
        
        b. BeginVertBox('None')
        b.   AddCheckbox('showTrades', 'Show Underlying Trades when Saved')
        b.   AddSpace(5)
        b.  BeginHorzBox('None')
        b.   AddButton('save', 'Save')
        b.   AddSpace(10)
        b.   AddButton('saveNew', 'Save New')
        b.  EndBox()
        b. EndBox()
        b.EndBox()
        
        return b


def start_dialog(shell):
    """Construct and start option dialog"""
    optionsDlg = OptionsStrategy()
    optionsDlg.InitControls()
    acm.UX().Dialogs().ShowCustomDialog(shell, optionsDlg.CreateLayout(), optionsDlg)

def start_dialog_cb(eii):
    """Callback from menu extension to start dialog"""
    if eii.ExtensionObject().IsKindOf(acm.FIndexedCollection):
        # Called from instrument context menu, use ins as default
        ins = eii.ExtensionObject().At(0)
        shell = eii.ExtensionObject().Shell()
    else:
        shell = eii.Parameter('shell')
    start_dialog(shell)

def start_from_script():
    """Demonstrate starting application from command line"""
    shell = acm.UX().SessionManager().Shell()
    start_dialog(shell)

start_from_script()
