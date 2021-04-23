""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTnpToAcmTradeFX.py"
"""--------------------------------------------------------------------------
MODULE
    FTnpToAcmTradeFX

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Used for handling creation of FX spot, forward and swap trades in TAB
-----------------------------------------------------------------------------"""

import acm
import FTnpUtils
from ACMPyUtils import Transaction
from FTradeCreator import FXTradeFromTreeSpecCreator

def TnpToAcmFxTrade(base):
    
    class TnpToAcmFxTrade(base):
        
        @classmethod
        def IsApplicable(cls, tnpMessage):
            if FTnpUtils.IsDealMessage(tnpMessage):
                tnpOrder = FTnpUtils.OriginatingSalesOrder(tnpMessage.TNPDEAL)
            else:
                tnpOrder = tnpMessage.TNPORDER
            return FTnpUtils.IsFxOrder(tnpOrder)
            
        def GetTrade(self):
            trade = self._GetBasicTrade()
            self._AddPositionAttributes(trade)
            self._CallTradeCreationHook(trade)
            self.AddExtraTradeData(trade)
            return trade
        
        def AddExtraTradeData(self, trade):
            super(TnpToAcmFxTrade, self).AddExtraTradeData(trade)
            if FTnpUtils.IsDealMessage(self._tnp):
                self._AddFxTradeDetails(self._tnpOrder, trade, True)
            else:
                self._AddFxTradeDetails(self._tnpOrder, trade, False)
        
        @classmethod            
        def _Price(cls, order):
            if order.dwPriceCondition() == cls.TnpConst().TNP_PC_UNLIMITED:
                try:
                    return FXTradeFromTreeSpecCreator.GetFXPrice(cls._Instrument(order),
                                                                 cls._Currency(order),
                                                                 cls._FxValueDay(order))
                except (ValueError, TypeError):
                    cls.Log().warning('No price found for instrument {0}'.format(cls._Instrument(order).Name()))
            return order.dPrice()
        
        @classmethod
        def CommitTrade(cls, trade):
            if trade.IsFxSwap():
                otherLeg = cls._OtherFxSwapLeg(trade)
                cls._CommitFxSwap(trade, otherLeg)
            else:
                trade.Commit()
        
        def DeleteTrade(self):
            trade = self.FindTrade()
            if trade:
                if trade.IsFxSwap():
                    otherLeg = self._OtherFxSwapLeg(trade)
                    with Transaction():
                        super(TnpToAcmFxTrade, self).DeleteTrade(trade)
                        super(TnpToAcmFxTrade, self).DeleteTrade(otherLeg)
                else:
                    return super(TnpToAcmFxTrade, self).DeleteTrade(trade)
        
        @classmethod
        def _CommitFxSwap(cls, trade, otherTrade):
            try:
                otherTrade.Status(trade.Status())
                with Transaction():
                    trade.Commit()
                    otherTrade.Commit()
                cls.Log().success('Linked trade {0} and {1} as an FX Swap'.format(trade.Name(), otherTrade.Name()))
            except Exception as e:
                cls.Log().error('Failed to link trade {0} and {1} as FX Swap, error: {2}'.format(trade.Name(), otherTrade.Name(), str(e)))
                
        def CommitViaAMBA(self):
            return not FTnpUtils.IsFxSwapOrder(self._tnpOrder)
        
        @classmethod
        def FxExtendedDataField(cls):
            return cls._Settings().FxExtendedDataField()
        
        @classmethod
        def _FxType(cls, tnpOrder):
            return FTnpUtils.OrderProcessType(tnpOrder)
        
        @classmethod
        def _FxSwapId(cls, tnpOrder):
            return cls._FxInfo(tnpOrder, 2)
        
        @classmethod
        def _FxValueDay(cls, tnpOrder):
            return FTnpUtils.FxValueDay(tnpOrder)
        
        @classmethod
        def _FxInfo(cls, tnpOrder, index):
            try:
                return FTnpUtils.GetFreeTextField(tnpOrder, cls.FxExtendedDataField()).split('|')[index]
            except (IndexError, AttributeError):
                return None
            
        @staticmethod
        def _OtherFxSwapLeg(trade):
            if trade.IsFxSwapNearLeg():
                return trade.FxSwapFarLeg()
            elif trade.IsFxSwapFarLeg():
                return trade.FxSwapNearLeg()
        
        @classmethod
        def _OtherFxSwapOrder(cls, tnpOrder):
            swapId = cls._FxSwapId(tnpOrder)
            for order in FTnpUtils.AllCachedOrders():
                if FTnpUtils.IsSalesOrder(order) and cls._FxSwapId(order) == swapId and not tnpOrder.szOrderId() == order.szOrderId():
                    return order
        
        @classmethod
        def _OtherFxSwapLegForOrder(cls, tnpOrder):
            otherOrder = cls._OtherFxSwapOrder(tnpOrder)
            if otherOrder:
                return FTnpUtils.FindTradeFromOrder(otherOrder)
        
        @classmethod
        def _OtherFxSwapLegForDeal(cls, tnpOrder):
            otherOrder = cls._OtherFxSwapOrder(tnpOrder)
            if otherOrder:
                trades = [trade for trade in FTnpUtils.FindFillsForOrder(otherOrder) if not trade.IsFxSwap()]
                if trades:
                    return trades[0]
            return None
        
        def _AddFxTradeDetails(self, tnpOrder, trade, isTradeFromDeal=True):
            fxType = self._FxType(tnpOrder)
            decorator = acm.FBusinessLogicDecorator.WrapObject(trade)
            if fxType == 'FXSpot':
                trade.SetFxSpotBit()
                decorator.ValueDay(self._FxValueDay(tnpOrder))
            elif fxType == 'FXForward':
                trade.SetFxForwardBit()
                decorator.ValueDay(self._FxValueDay(tnpOrder))
            elif fxType == 'FXSwap': 
                decorator.ValueDay(self._FxValueDay(tnpOrder))
                if not trade.IsFxSwap():
                    self._CreateFxSwap(tnpOrder, trade, fxType, isTradeFromDeal)
                    
        @classmethod
        def _CreateFxSwap(cls, tnpOrder, trade, fxType, isTradeFromDeal):
            if isTradeFromDeal:
                otherTrade = cls._OtherFxSwapLegForDeal(tnpOrder)
            else:
                otherTrade = cls._OtherFxSwapLegForOrder(tnpOrder)
            if otherTrade:
                if fxType == 'FXNear':
                    cls._LinkFxSwapTrades(trade, otherTrade)
                else:
                    cls._LinkFxSwapTrades(otherTrade, trade)
                cls._CommitFxSwap(trade, otherTrade)
                    
        @staticmethod
        def _LinkFxSwapTrades(nearTrade, farTrade):
            nearTrade.SetFxSwapNearLegBit()
            farTrade.SetFxSwapFarLegBit()
            nearTrade.ConnectedTrade(nearTrade)
            farTrade.ConnectedTrade(nearTrade)
                    
    return TnpToAcmFxTrade
