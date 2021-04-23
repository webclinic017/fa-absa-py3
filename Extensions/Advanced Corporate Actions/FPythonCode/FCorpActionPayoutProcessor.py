""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionPayoutProcessor.py"

"""----------------------------------------------------------------------------
MODULE
    FCorpActionPayoutProcessor

DESCRIPTION
----------------------------------------------------------------------------"""
import datetime

import acm

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme

import FCorpActionElectionHandler
import FCorpActionUtils

__all__ = ['ProcessPayouts', 
           'PayoutProcessor']
'''
[ExerciseRights, NameChangeDerivative, Liquidation, ContractSizeChange, DividendOption, DividendReinvestment, BonusIssue, NameChange, PriorityIssue, ScripDividend]
'''
'''
[RightsDistribution, ExerciseRights, CashDistribution, NewIssueStock, NameChangeDerivative, Liquidation, ContractSizeChange, DividendOption, DividendReinvestment, Elective, BonusIssue, NameChange, TenderOfferStock, MergerStock, BuybackStock, CapitalAdjustmentDerivative, SplitStock, PriorityIssue, ReverseStockSplit, StockDividend, ScripDividend, SpinOffStock]
'''

def ProcessPayouts(caPosition, instrumentPosition, templateHelper):
    result = []
    for payout in caPosition.CaChoice().CaPayouts():
        payoutProcessor = PayoutProcessor(caPosition, payout, templateHelper)
        subresult = payoutProcessor.Process(instrumentPosition)
        result.extend(subresult)
    return result


class PayoutProcessor(object):

    def __init__(self, caPosition, payout, templateHelper):
        self._payout = payout
        self._caPosition = caPosition
        self._action = payout.CaChoice().CorpAction()
        self._templateHelper = templateHelper
        self._factor = None
        self._taxFactor = self._caPosition.AdditionalInfo().TaxRate()
        
    def Process(self, position):
        result = []
        context = self._CreateContext(position)
        context.Quantity(self._GetQuantity(context))
        handler = FCorpActionElectionHandler.Create(context)
        handlerMethod = getattr(handler, self.AdjustMethod(), None)
        print(('handlerMethod', handlerMethod))
        if handlerMethod is not None:
            handlerMethod(result)
        return result
        
    def AdjustMethod(self):       
        #need more advanced logic here
        if self.Amount(): return 'GenerateCash'
        elif bool(self.Rate()) is False: return 'ClosePosition'
        elif self.NewInstr(): 
            if self.NewInstr() != self._action.Instrument():
                return 'OpenPosition'
            else:
                return 'AdjustPosition'
        else: return 'AdjustPosition'
            
    def Action(self):
        return self._action
        
    def Currency(self):
        return self._payout.Currency()

    def SettleDate(self):
        return self._action.SettleDate()

    def TradeTime(self):
        tradetime = FCorpActionUtils.GetCorpActionValidDate(self._action)
        return tradetime

    def Rate(self):
        return self._payout.PayoutRate()
        
    def NewInstr(self):
        return self._payout.NewInstrument()
        
    def Amount(self):
        if self._payout.PayoutAmount():
            return self._payout.PayoutAmount()
        if self._payout.PayoutNetAmount():
            return self._payout.PayoutNetAmount()
        if self._payout.PayoutGrossAmount():
            return self._payout.PayoutGrossAmount() * self._taxFactor
        return 0
    
    def Price(self):
        return self._payout.Price()
    
    def PriceCurrency(self):
        return self._payout.PriceCurrency()

    def PaymentType(self):
        if self.Amount():
            return self._templateHelper.GetPaymentType()
        return None
    
    def Percentage(self):
        return self._caPosition.Percentage()

    def Factor(self):
        #TODO: store normalized rate so that no adjustment is needed
        if self._factor is None:
            self._factor = self._templateHelper.GetAdjustFactor(self.Rate())
        return self._factor
        
    def _GetQuantity(self, context):
        adjustMethodHelper = CreateAdjustMethodHelper(self.AdjustMethod())
        return adjustMethodHelper.GetQuantity(context)        
        
    def _CreateContext(self, position):
        context = FCorpActionElectionHandler.HandlerContext()
        context.Position(position)
        context.NewInstrument(self.NewInstr())
        context.Factor(self.Factor())
        context.Amount(self.Amount())
        context.Currency(self.Currency())
        context.TradeTime(self.TradeTime())
        context.ValueDay(self.SettleDate())
        context.AcquireDay(self.SettleDate())
        context.PaymentType(self.PaymentType())
        context.Price(self.Price())
        context.PriceCurrency(self.PriceCurrency())
        context.Percentage(self.Percentage())
        return context
    
def CreateAdjustMethodHelper(adjustMethod):
    helperName = '{0}Helper'.format(adjustMethod)
    helper = getattr(__import__(__name__), helperName, None)
    if helper is None:
        return AdjustMethodHelper()
    return helper()    
    
def CreateTemplateHelper(action):
    helperName = '{0}Helper'.format(action.Template())
    helper = getattr(__import__(__name__), helperName, None)
    if helper is None:
        return TemplateHelper()
    return helper()




class TemplateHelper(object):
    def __init__(self):
        print((self.__class__.__name__))

    def GetAdjustFactor(self, payoutRate):
        return payoutRate

    def GetPaymentType(self):
        return 'Cash'

class SplitStockHelper(TemplateHelper):
    pass

class ReverseStockSplitHelper(SplitStockHelper):
    pass

class SpinOffStockHelper(SplitStockHelper):
    pass

class CashDistributionHelper(SplitStockHelper):
    pass

class StockDividendHelper(TemplateHelper):
    def GetPaymentType(self):
        return 'Cash'

    def GetAdjustFactor(self, payoutRate):
        return payoutRate + 1
    
class ScripDividendHelper(StockDividendHelper):
    pass

class DividendReinvestmentHelper(StockDividendHelper):
    pass

class TenderOfferStockHelper(TemplateHelper):
    pass

class MergerStockHelper(TemplateHelper): 
    pass

class BuybackStockHelper(TemplateHelper):
    pass

class RightsDistributionHelper(TemplateHelper):
    pass

class LiquidationHelper(TemplateHelper):
    pass



class AdjustMethodHelper(object):
    def __init__(self):
        print((self.__class__.__name__))
            
    def GetQuantity(self, context):
        raise NotImplementedError

class GenerateCashHelper(AdjustMethodHelper):

    def GetQuantity(self, context):
        return context.Position().Value()

class ClosePositionHelper(AdjustMethodHelper):

    def GetQuantity(self, context):
        val = -1 * context.Position().Value() * context.Percentage() / 100.0
        print(val)
        return val
        
        
class OpenPositionHelper(AdjustMethodHelper):

    def GetQuantity(self, context):
        val = context.Position().Value() * context.Factor() * context.Percentage() / 100.0
        print(val)
        return val
        

class AdjustPositionHelper(AdjustMethodHelper):

    def GetQuantity(self, context):
        val = context.Position().Value() * (context.Factor() - 1)  * context.Percentage() / 100.0
        print(val)
        return val

