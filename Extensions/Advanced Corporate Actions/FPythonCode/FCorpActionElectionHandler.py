""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionElectionHandler.py"

"""----------------------------------------------------------------------------
MODULE
    FCorpActionElectionHandler 

DESCRIPTION
----------------------------------------------------------------------------"""
import acm

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import FBDPCommon
from FCorpActionUtils import HandlerFromParams
import FCorpActionRounding
from FSecLendUtils import GetSecurityLoanRate, SetSecurityLoanRate

def Create(context):
    ins = context.Position().Instrument()
    handler = HandlerFromParams(str(ins.Class()).split(',')[0])
    print('handler', handler)
    if handler is None:
        return InstrumentHandler(context)
    return handler(context)


class HandlerContext(object):

    def __init__(self):
        self._position = None
        self._amount = None
        self._quantity = None
        self._currency = None
        self._newInstrument = None
        self._factor = None
        self._tradeTime = None
        self._valueDay = None
        self._acquireDay = None
        self._paymentType = None
        self._price = 0.0
        self._priceCurrency = None
        self._percentage = None
    
    def Position(self, position=None):
        if position is None:
            return self._position
        self._position = position
        
    def Amount(self, amount=None):
        if amount is None:
            return self._amount
        self._amount = amount
        
    def Currency(self, currency=None):
        if currency is None:
            return self._currency
        self._currency = currency
        
    def Quantity(self, quantity=None):
        if quantity is None:
            return self._quantity
        self._quantity = quantity
        
    def NewInstrument(self, newInstrument=None):
        if newInstrument is None:
            return self._newInstrument
        self._newInstrument = newInstrument

    def Factor(self, factor=None):
        if factor is None:
            return self._factor
        self._factor = factor

    def Price(self, price=None):
        if price is None:
            return self._price
        self._price = price
    
    def PriceCurrency(self, currency=None):
        if currency is None:
            return self._priceCurrency
        self._priceCurrency = currency
        
    def TradeTime(self, tradeTime=None):
        if tradeTime is None:
            return self._tradeTime
        self._tradeTime = tradeTime
        
    def ValueDay(self, valueDay=None):
        if valueDay is None:
            return self._valueDay
        self._valueDay = valueDay
        
    def AcquireDay(self, acquireDay=None):
        if acquireDay is None:
            return self._acquireDay
        self._acquireDay = acquireDay
        
    def PaymentType(self, paymentType=None):
        if paymentType is None:
            return self._paymentType
        self._paymentType = paymentType
        
    def Price(self, price=None):
        if price is None:
            return self._price
        self._price = price
    
    def Percentage(self, percentage=None):
        if percentage is None:
            return self._percentage
        self._percentage = percentage
        
class IHandler(object):

    def __init__(self, context):
        raise NotImplementedError
        
    def OpenPosition(self, result):
        raise NotImplementedError
        
    def ClosePosition(self, result):
        raise NotImplementedError

    def AdjustPosition(self, result):
        raise NotImplementedError
        
    def GenerateCash(self, result):
        raise NotImplementedError


class InstrumentHandler(IHandler):

    def __init__(self, context):
        self._context = context
        self._position = context.Position()
        self._position_trade = self._position.Trades().First()

    def _CreateTrade(self, instrument, currency, quantity, price, 
                     acquirer, counterparty, time, valueDay, acquireDay,
                     portfolio, status='Simulated', type='Corporate Action'):
        tradeStatus = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionTradeStatus')
        trader = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionTrader')          
        t = acm.FTrade()
        t.Currency(currency)
        t.Instrument(instrument)
        t.Price(price)
        t.Quantity(quantity)
        t.TradeTime(time)
        t.ValueDay(valueDay)
        t.AcquireDay(acquireDay)
        t.Acquirer(acquirer)
        t.Counterparty(counterparty)
        t.Type(type)
        t.Status(tradeStatus)
        if trader:
            t.Trader(acm.FUser[trader])
        t.Portfolio(portfolio)
        Summary().ok(t, Summary().CREATE)
        return t
    
    def _CreatePayment(self, paymentType, fromDate, payday, amount, currency, trade):
        payment = acm.FPayment()
        payment.Type(paymentType)
        payment.Currency(currency)
        payment.Amount(amount)
        payment.ValidFrom(fromDate)
        payment.PayDay(payday)
        payment.Trade(trade)
        payment.Party(trade.Acquirer())
        Summary().ok(payment, Summary().CREATE)
        return payment
        
    def ClosePosition(self, result):    
        if self._context.Percentage() > 0:             
            Logme()('InstrumentHandler Close position', 'INFO')
            quantity = (-1.0) * (self._position.Value() * self._context.Percentage() / 100.0)
            quantity = FCorpActionRounding.RoundQuantityUp(quantity, 0)
            result.append(self._CreateTrade(self._position.Instrument(),
                                            self._position_trade.Currency(),
                                            quantity,
                                            self._context.Price(),
                                            self._position_trade.Acquirer(),
                                            self._position_trade.Counterparty(), 
                                            self._context.TradeTime(),
                                            self._context.ValueDay(),
                                            self._context.AcquireDay(),
                                            self._position_trade.Portfolio()))
            self.GeneratePremium(result, quantity)
                         
    def OpenPosition(self, result):
        if self._context.Percentage() > 0:
            Logme()('InstrumentHandler Open position', 'INFO')
            quantity = self._context.Factor() * self._position.Value() * self._context.Percentage() / 100.0
            quantity = FCorpActionRounding.RoundQuantityDown(quantity, 0)
            result.append(self._CreateTrade(self._context.NewInstrument(), 
                                            self._position_trade.Currency(), 
                                            quantity, 
                                            self._context.Price(),
                                            self._position_trade.Acquirer(),
                                            self._position_trade.Counterparty(), 
                                            self._context.TradeTime(),
                                            self._context.ValueDay(),
                                            self._context.AcquireDay(),
                                            self._position_trade.Portfolio()))
            self.GeneratePremium(result, quantity)

    def AdjustPosition(self, result):
        if self._context.Percentage() > 0:
            Logme()('InstrumentHandler Adjust position', 'INFO')
            quantity = (self._context.Factor() - 1) * self._position.Value() * self._context.Percentage() / 100.0
            if self._context.Factor() < 1.0:
                quantity = FCorpActionRounding.RoundQuantityUp(quantity, 0)
            else:
                quantity = FCorpActionRounding.RoundQuantityDown(quantity, 0)
            result.append(self._CreateTrade(self._position.Instrument(),
                                            self._position_trade.Currency(),
                                            quantity,
                                            self._context.Price(),
                                            self._position_trade.Acquirer(),
                                            self._position_trade.Counterparty(),
                                            self._context.TradeTime(),
                                            self._context.ValueDay(),
                                            self._context.AcquireDay(),
                                            self._position_trade.Portfolio()))
            self.GeneratePremium(result, quantity)
                         
    def GenerateCash(self, result):
        if self._context.Percentage() > 0:
            Logme()('InstrumentHandler Generate Cash', 'INFO')
            paymentType = self._context.PaymentType() 
            fromDate = self._context.TradeTime()
            payDate = self._context.ValueDay()
            amount = self._context.Amount() * self._context.Quantity() * self._context.Percentage() / 100.0
            currency = self._context.Currency()
            result.append(self._CreatePayment(paymentType,
                                            fromDate,
                                            payDate,
                                            amount,
                                            currency,
                                            self._position_trade))
    
    def GeneratePremium(self, result, quantity):
        if self._context.Percentage() > 0:
            Logme()('InstrumentHandler Generate Premium', 'INFO')
            paymentType = 'Cash'
            fromDate = self._context.TradeTime()
            payDate = self._context.ValueDay()
            amount = self._context.Price() * quantity
            currency = self._context.PriceCurrency()
            if amount != 0.0:
                result.append(self._CreatePayment(paymentType,
                                                fromDate,
                                                payDate,
                                                amount,
                                                currency,
                                                self._position_trade))
        
    

class SecurityLoanHandler(IHandler):
    
    def __init__(self, context):
        self._context = context
        self._mainTrd = None
        
    def Instrument(self):
        return acm.FBusinessLogicDecorator.WrapObject(self.MainTrade().Instrument())
        
    def FirstLeg(self):
        return self.Instrument().Legs().First()

    def MainTrade(self):
        if self._mainTrd is None:
            self._mainTrd = self._context.Position().Trades().First().Contract()
        #print self._mainTrd.Oid()
        return self._mainTrd
        
    def GenerateCashFlows(self, instrument):
        for leg in instrument.Legs():
            leg.GenerateCashFlows(0)
    
    def _CreatePayment(self, paymentType, fromDate, payday, amount, currency, trade):
        payment = acm.FPayment()
        payment.Type(paymentType)
        payment.Currency(currency)
        payment.Amount(amount)
        payment.ValidFrom(fromDate)
        payment.PayDay(payday)
        payment.Trade(trade)
        payment.Party(trade.Acquirer())
        Summary().ok(payment, Summary().CREATE)
        return payment
    
    def AdjustTrade(self):
        if self._context.Factor() < 1.0:
            quantity = FCorpActionRounding.RoundQuantityUp(self._context.Quantity(), 0)
        else:
            quantity = FCorpActionRounding.RoundQuantityDown(self._context.Quantity(), 0)
        if quantity == 0.0:
            return None
        
        if self.MainTrade() == None:
            print('maintrade is None')
            print(self._context)
            return None
        import FSecLendDealUtils
        status = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionTradeStatus')
        trader = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionTrader')
        mainTrdWrapper = FSecLendDealUtils.SecurityLoanWrapper.Wrap(self.MainTrade())
        adjustTrade = mainTrdWrapper.CreateAdjustTrade(quantity, 
                                                            self._context.ValueDay(), 
                                                            self._context.TradeTime(),
                                                            status)
        adjustTrade.Type('Corporate Action')
        adjustTrade.Market(None)
        if trader:
            adjustTrade.Trader(acm.FUser[trader])
        self.GenerateCashFlows(adjustTrade.Instrument())
        return adjustTrade
        
    def ClosePosition(self, result):
        if self._context.Percentage() > 0:
            Logme()('SecurityLoanHandler--ClosePosition', 'INFO')
            adjustTrade = self.AdjustTrade()
            if adjustTrade:
                result.append(adjustTrade) 
                self.GeneratePremium(result, adjustTrade.Quantity())

    def AdjustPosition(self, result):
        if self._context.Percentage() > 0:
            Logme()('SecurityLoanHandler--AdjustPosition', 'INFO')
            adjustTrade = self.AdjustTrade()
            if adjustTrade:
                result.append(adjustTrade)
                self.GeneratePremium(result, adjustTrade.Quantity())

    def OpenPosition(self, result):
        if self._context.Percentage() > 0:
            Logme()('SecurityLoanHandler--OpenPosition', 'INFO')
            quantity = FCorpActionRounding.RoundQuantityDown(self._context.Quantity(), 0)
            if quantity == 0.0:
                return
            import FSecLendDealUtils
            insAttributes = {'underlying': self._context.NewInstrument(),
                            'rollingPeriod': self.FirstLeg().RollingPeriod(),
                            'openEnd': self.Instrument().OpenEnd(),
                            'noticePeriod': self.Instrument().NoticePeriod(),
                            'dayCountMethod': self.FirstLeg().DayCountMethod(),
                            'legStartPeriod': self.Instrument().LegStartPeriod(),
                            'legEndPeriod': self.Instrument().LegEndPeriod(),
                            'nominalFactor': self.FirstLeg().NominalFactor(),
                            'dividendFactor': self.Instrument().DividendFactor(),
                            'spotDays': self.Instrument().SpotBankingDaysOffset(),
                            'fixedPrice': True if self.FirstLeg().NominalScaling() == 'Initial Price' else False,
                            'currency': self.Instrument().Currency(),
                            'fee': GetSecurityLoanRate(self.MainTrade())}
            
            tradeAttributes = {'quantity': quantity,
                              'acquirer': self.MainTrade().Acquirer(),
                              'portfolio': self.MainTrade().Portfolio(),
                              'counterparty': self.MainTrade().Counterparty(),
                              #'source': self.MainTrade().Market(),
                              'slAccount' : self.MainTrade().AdditionalInfo().SL_Account(),
                              'collateralAgreement' : self.MainTrade().AdditionalInfo().CollateralAgreement()}

            slc = FSecLendDealUtils.SecurityLoanCreator()
            ins = slc.CreateInstrument(**insAttributes)
            trade = slc.CreateTrade(ins, **tradeAttributes)
            SetSecurityLoanRate(trade, GetSecurityLoanRate(self.MainTrade()))
            tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(trade)
            tradeDecorator.TradeTime(self._context.TradeTime())
            tradeDecorator.ValueDay(self._context.ValueDay())
            status = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionTradeStatus')
            trader = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionTrader')
            tradeDecorator.Type('Corporate Action')
            tradeDecorator.Market(None)
            if trader:
                tradeDecorator.Trader(acm.FUser[trader])
            tradeDecorator.Status(status)
            result.append(ins)
            result.append(trade)
            self.GeneratePremium(result, quantity)

    
    def GenerateCash(self, result):
        if self._context.Percentage() > 0:
            Logme()('SecurityLoanHandler Generate Cash', 'INFO')
            paymentType = self._context.PaymentType() 
            fromDate = self._context.TradeTime()
            payDate = self._context.ValueDay()
            amount = self._context.Amount() * self._context.Quantity() * self._context.Percentage() / 100.0
            if amount == 0.0:
                return
            currency = self._context.Currency()
            result.append(self._CreatePayment(paymentType,
                                            fromDate,
                                            payDate,
                                            amount,
                                            currency,
                                            self.MainTrade()))

    def GeneratePremium(self, result, quantity):
        if self._context.Percentage() > 0:
            Logme()('SecurityLoanHandler Generate Premium', 'INFO')
            paymentType = 'Cash'
            fromDate = self._context.TradeTime()
            payDate = self._context.ValueDay()
            amount = self._context.Price() * quantity
            currency = self._context.PriceCurrency()
            if amount != 0.0:
                result.append(self._CreatePayment(paymentType,
                                                fromDate,
                                                payDate,
                                                amount,
                                                currency,
                                                self.MainTrade()))
