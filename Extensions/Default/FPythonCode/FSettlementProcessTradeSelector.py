""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementProcessTradeSelector.py"
import acm
import FOperationsTradesFromInstrument
import FSettlementUtils
from FOperationsEnums import InsType


class SettlementProcessTradeSelector:
    
    def __init__(self, fObject, defaulfProcessFilterHandler, amendmentProcessFilterHandler):
        
        self.__defaultProcessFilterHandler = defaulfProcessFilterHandler
        self.__amendmentProcessFilterHandler = amendmentProcessFilterHandler
        self.__amendmentProcessTrades = list()
        self.__defaultProcessTrades = list()
        self.__fObject = fObject
        
    def GetAmendmentProcessTrades(self):
        return self.__amendmentProcessTrades
    
    def GetDefaultProcessTrades(self):
        return self.__defaultProcessTrades
    
    def HasAmendmentProcessTrades(self):
        return (len(self.__amendmentProcessTrades) > 0)
    
    def GetNumberOfTrades(self):
        return len(self.__defaultProcessTrades) + len(self.__amendmentProcessTrades)
    
    def __IsAmendmentProcessTrade(self, trade):
        return self.__amendmentProcessFilterHandler.IsAmendmentProcessTrade(trade)
            
    def __FilterAndAddDefaultProcessTrade(self, trade):
        self.__defaultProcessFilterHandler.FilterAndAddTrade(trade, self.__defaultProcessTrades)
        self.__AddClosedClosingTrades()
        
    def __IsAddClosedPayoutTrade(self):
        isAddClosedTrade = False
        if FSettlementUtils.IsClosingTrade(self.__fObject):
            if self.__fObject.Instrument().InsType() == InsType.FUTURE_FORWARD or \
               self.__fObject.Instrument().InsType() == InsType.VARIANCE_SWAP:
                isAddClosedTrade = True
        return isAddClosedTrade

    def __AddClosedClosingTrades(self):
        closingTrades = FSettlementUtils.GetClosingPayoutTrades(self.__fObject)
        if len(closingTrades):
            for t in closingTrades:
                self.__defaultProcessFilterHandler.FilterAndAddTrade(t, self.__defaultProcessTrades)
        elif self.__IsAddClosedPayoutTrade():
            closedTrade = acm.FTrade[self.__fObject.ContractTrdnbr()]
            self.__defaultProcessFilterHandler.FilterAndAddTrade(closedTrade, self.__defaultProcessTrades)
                
    def FilterAndAddTrades(self):
        #Trade
        if self.__fObject.IsKindOf(acm.FTrade):
            if self.__IsAmendmentProcessTrade(self.__fObject):
                self.__amendmentProcessTrades.append(self.__fObject)
                return
            self.__FilterAndAddDefaultProcessTrade(self.__fObject)
            
        #Instrument
        elif self.__fObject.IsKindOf(acm.FInstrument):
            tradeList = FOperationsTradesFromInstrument.GetTradesFromInstrument(self.__fObject)
            for trade in tradeList:
                if self.__IsAmendmentProcessTrade(trade):
                    self.__amendmentProcessTrades.append(trade)
                    continue
                self.__defaultProcessFilterHandler.FilterAndAddTrade(trade, self.__defaultProcessTrades)
                
        # BusinessEvent
        elif self.__fObject.IsKindOf(acm.FBusinessEvent):
            paymentLinks = self.__fObject.PaymentLinks()
            tradeSet = set()
            for paymentLink in paymentLinks:
                payment = paymentLink.Payment()
                tradeSet.add(payment.Trade())
            for trade in tradeSet:
                if self.__IsAmendmentProcessTrade(trade):
                    self.__amendmentProcessTrades.append(trade)
                    continue
                self.__defaultProcessFilterHandler.FilterAndAddTrade(trade, self.__defaultProcessTrades)
    
        self.__defaultProcessTrades = FSettlementUtils.GetNonExcludedTrades(self.__defaultProcessTrades)
                