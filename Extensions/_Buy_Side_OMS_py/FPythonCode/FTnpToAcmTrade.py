""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTnpToAcmTrade.py"
"""--------------------------------------------------------------------------
MODULE
    FTnpToAcmTrade

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Class for creating an ACM trade from a TNP message (TNPORDER and TNPDEAL) in TAB
-----------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils
import FTnpUtils
from FTradeCreator import TradeCreator
from FParameterSettings import ParameterSettingsCreator
from collections import OrderedDict

class TnpToAcmTrade(object):
    
    SETTINGS = None
    
    def __init__(self, tnpMessage):
        self._tnp = tnpMessage
    
    def GetTrade(self):
        """ Returns an ACM trade based on the TNP message, stored position attributes, hooks, etc. """
        trade = self._GetBasicTrade()
        self._AddPositionAttributes(trade)
        self.AddExtraTradeData(trade)
        self._CallTradeCreationHook(trade)
        return trade
    
    def GetTradeAsAMBAMessage(self, trade=None):
        """ Returns AMBA trade message based on the TNP message, stored position attributes, hooks, etc. """
        trade = trade or self.GetTrade()
        msgType = 'INSERT TRADE' if trade.IsInfant() else 'UPDATE TRADE' 
        return FTnpUtils.AMBAMessageForObjects([trade], msgType)
    
    def _GetBasicTrade(self):
        """ Returns a trade based only on the information in the TNP message """
        return acm.FTrade()

    def _AddPositionAttributes(self, trade):
        """ Enriches trade with position information stored in ADS """
        positionProperties = self.PositionAttributes()
        self._UpdateTradeProperties(trade, positionProperties, onlyIfNone=True)
    
    def AddExtraTradeData(self, trade):
        """ Used for adding data that is specific to a certain asset class or trading venue e.g. FX swaps.
            This method should be overriden in such implementations """
        pass

    def _CallTradeCreationHook(self, trade):
        pass
    
    def FindTrade(self):
        """ Returns the trade based in the TNP message from the ADS if possible"""
        return None
    
    def CommitViaAMBA(self):
        return True
    
    def TNP(self):
        return self._tnp
    
    def TNPSeqNo(self):
        return self._tnp.ui64SeqNo()
    
    @classmethod
    def CommitTrade(cls, trade):
        trade.Commit()
    
    def DeleteTrade(self, trade=None):
        trade = trade or self.FindTrade()
        if trade:
            setting = self._Settings().OnOrderCompleted()
            if setting == 'Delete':
                return self._DeleteTrade(trade)
            elif setting == 'Archive':
                return self._ArchiveTrade(trade)
            elif setting == 'Void':
                return self._VoidTrade(trade)
            else:
                self.Log().error('Invalid setting for "OnOrderCompleted". Setting should be Delete, Archive or Void')
    
    def _DeleteTrade(self, trade):
        if self.CommitViaAMBA():
            return FTnpUtils.AMBAMessageForObjects([trade], 'DELETE TRADE')
        else:
            trade.Delete()

    def _ArchiveTrade(self, trade):
        trade.Status('Void')
        trade.ArchiveStatus(1)
        if self.CommitViaAMBA():
            return FTnpUtils.AMBAMessageForObjects([trade], 'UPDATE TRADE')
        else:
            trade.Commit()
        
    def _VoidTrade(self, trade):
        trade.Status('Void')
        if self.CommitViaAMBA():
            return FTnpUtils.AMBAMessageForObjects([trade], 'UPDATE TRADE')
        else:
            trade.Commit()
    
    def PositionAttributes(self):
        if self._PositionReference():
            return self._PositionAttributes(self._PositionReference())
        else:
            return dict()
    
    def _PositionReference(self):
        return None
    
    @classmethod
    def _UpdateTradeProperties(cls, trade, properties, onlyIfNone=False):
        if onlyIfNone:
            properties = cls._NotSetProperties(trade, properties)
        decorator = acm.FBusinessLogicDecorator.WrapObject(trade)
        TradeCreator.SetProperties(decorator, properties)    

    @staticmethod
    def _PositionAttributes(reference):
        positionAttributes = acm.FCustomArchive[reference]
        if positionAttributes is not None:
            attributes = positionAttributes.FromArchive('attributes')
            return dict((k, attributes[k]) for k in attributes)
        
    @staticmethod
    def _NotSetProperties(trade, positionAttributes):
        return {k:v for k, v in positionAttributes.iteritems() 
                if acm.FMethodChain(k).Call([trade]) in [None, '']}

    @classmethod
    def _CallHook(cls, tnp, trade, hookName):
        """ Parameters to hook function are TNP-message, acm-Trade and log module """
        function = getattr(cls._Settings(), hookName)()
        if function:
            FAssetManagementUtils.CallFunction(function, tnp, trade, cls.Log())
            
    @classmethod
    def _Settings(cls):
        if not cls.SETTINGS:
            cls.SETTINGS = ParameterSettingsCreator.FromRootParameter('TABSettings')
        return cls.SETTINGS
    
    @staticmethod
    def TnpConst():
        return FTnpUtils.TnpDependecies.TNP_CONST
    
    @staticmethod
    def Log():
        return FTnpUtils.TnpDependecies.LOG


class TnpOrderToAcmTrade(TnpToAcmTrade):
    
    ''' Read/Write/Delete protection only on owner. Read protection for other levels '''
    PROTECTION = 3504
    
    def __init__(self, tnpMessage):
        super(TnpOrderToAcmTrade, self).__init__(tnpMessage)
        self._tnpOrder = tnpMessage.TNPORDER
    
    def _GetBasicTrade(self):
        trade = self.FindTrade() or self._CreateDefaultTrade()
        orderProperties = self._TradePropertiesFromOrder()
        self._UpdateTradeProperties(trade, orderProperties, onlyIfNone=False)
        return trade

    def _CreateDefaultTrade(self):
        t = acm.FTrade()
        t.Type = 'Reservation'
        t.Protection = self.PROTECTION
        return t

    def _CallTradeCreationHook(self, trade):
        self._CallHook(self._tnpOrder, trade, 'ReservedTradeHook')
    
    def FindTrade(self):
        return FTnpUtils.FindTradeFromOrder(self._tnpOrder)
    
    def _PositionReference(self):
        return FTnpUtils.PositionReferenceForOrder(self._tnpOrder)
    
    def _TradePropertiesFromOrder(self):
        properties = OrderedDict()
        for prop, func in self.MappingDict().iteritems():
            properties[prop] = func(self._tnpOrder)
        return properties
    
    @classmethod
    def _RemainingQuantity(cls, order):
        remainingQuantity = order.dQuantity() - (FTnpUtils.TradedQuantity(order) + FTnpUtils.QuantityToShape(order))
        if order.dwBidOrAsk() == cls.TnpConst().TNP_ASK:
            remainingQuantity = -remainingQuantity
        return remainingQuantity
            
    @classmethod   
    def _Instrument(cls, order):
        tnpOrderBook = FTnpUtils.TnpOrderBook(order)
        name = FTnpUtils.OrderBookName(tnpOrderBook)
        try:
            alias = acm.FInstrumentAlias.Select('type = "TAB" and alias = "{0}"'.format(name))[0]
        except IndexError:
            raise Exception('No Orderbook found with TAB alias {0}'.format(name))
        return alias.Instrument()
    
    @classmethod
    def _Currency(cls, order):
        tnpOrderBook = FTnpUtils.TnpOrderBook(order)
        return acm.FCurrency[tnpOrderBook.szTradingCurrency()]
    
    @classmethod
    def _Status(cls, order):
        if order.TNPSALESORDERSTATE.dwSalesOrderState() == cls.TnpConst().TNP_SOS_INACTIVE:
            return 'Simulated'
        else:
            return 'Reserved'
    
    @classmethod            
    def _Price(cls, order):
        from FTradeCreator import DecoratedTradeCreator
        if order.dwPriceCondition() == cls.TnpConst().TNP_PC_UNLIMITED:
            try:
                return float(DecoratedTradeCreator.Price(cls._Instrument(order), cls._Settings().PriceColumn()))
            except (ValueError, TypeError):
                cls.Log().warning('No price found for instrument {0}'.format(cls._Instrument(order).Name()))
        return order.dPrice()
    
    @classmethod
    def MappingDict(cls):
        return OrderedDict([('Instrument', cls._Instrument),
                            ('Quantity', cls._RemainingQuantity),
                            ('Price', cls._Price),
                            ('OptionalKey', lambda order: order.szOrderId()),
                            ('Currency', cls._Currency),
                            ('Status', cls._Status),
                            ('Trader', lambda order: order.TNPSALESPERSONID.szSalesPersonId()),
                            ('TradeTime', lambda order: \
                                FTnpUtils.DateTimeFromTnp(order.TNPORDERCREATIONDATETIME.szOrderCreationDateTime())),
                            ])
        
class TnpDealToAcmTrade(TnpToAcmTrade):
    
    def __init__(self, tnpMessage, amb):
        super(TnpDealToAcmTrade, self).__init__(tnpMessage)
        acm.PollAllDbEvents()
        self._tnpDeal = tnpMessage.TNPDEAL
        self._amb = amb
        self._tnpOrder = FTnpUtils.OriginatingSalesOrder(self._tnpDeal)
        if self.FindTrade() is not None:
            self._existingTrade = self.FindTrade().Clone()
        else:
            self._existingTrade = None
    
    def _GetBasicTrade(self):
        trade = self.AcmTradeFromAmb()
        self._SetTradeAttributes(trade)
        tradeTime = FTnpUtils.DateTimeFromTnp(str(self._tnpDeal.szAgreementDateTime()))
        acm.FBusinessLogicDecorator.WrapObject(trade).TradeTime(tradeTime)
        return trade

    def _CallTradeCreationHook(self, trade):
        self._CallHook(self._tnpDeal, trade, 'NewDealHook')
    
    def FindTrade(self):
        return FTnpUtils.FindTradeFromDeal(self._tnpDeal)
    
    def AcmTradeFromAmb(self):
        return acm.AMBAMessage.CreateObjectFromMessage(str(self._amb))
    
    def _Status(self):
        if FTnpUtils.IsDeleteDeal(self._tnpDeal):
            return 'Void'
        if self._existingTrade:
            return self._existingTrade.Status()
        else:
            return 'Exchange'
    
    def _SetTradeAttributes(self, trade):
        trade.Status(self._Status())
        trade.OrderUuid(self._tnpOrder.szOrderId())
        if FTnpUtils.Counterparty(self._tnpDeal):
            trade.Counterparty(FTnpUtils.Counterparty(self._tnpDeal))
    
    def _PositionReference(self):
        return FTnpUtils.PositionReferenceForOrder(self._tnpOrder)

class TnpBulkDealToAcmTrade(TnpDealToAcmTrade):
    
    def _AddPositionAttributes(self, trade):
        pass
    
    def _CallTradeCreationHook(self, trade):
        self._CallHook(self._tnpDeal, trade, 'BulkDealHook')


""" TNP-ACM trade wrapper factory:
    Returns the correct wrapper class for a TNP-message. The base ones are for TNPORDER, TNPDEAL and 
    TNPDEAL for bulked orders. If a message fulfills the method IsApplicable() on any of the classes 
    returned by WrapperClassExtensions the base wrapper will be extended with that class. """

def GetTnpAcmWrapperClass(tnpMessage, amb=None):
    if FTnpUtils.IsDealMessage(tnpMessage):
        if FTnpUtils.IsBulkDeal(tnpMessage.TNPDEAL):
            return ExtendedWrapperClass(tnpMessage, TnpBulkDealToAcmTrade)(tnpMessage, amb)
        else:
            return ExtendedWrapperClass(tnpMessage, TnpDealToAcmTrade)(tnpMessage, amb) 
    elif FTnpUtils.IsOrderMessage(tnpMessage):
        return ExtendedWrapperClass(tnpMessage, TnpOrderToAcmTrade)(tnpMessage)
    
def WrapperClassExtensions(baseWrapperClass):
    for functionPath in TnpToAcmTrade._Settings().WrapperClassExtensions():
        yield FAssetManagementUtils.CallFunction(functionPath, baseWrapperClass)

def ExtendedWrapperClass(tnpMessage, baseWrapperClass):
    for cls in WrapperClassExtensions(baseWrapperClass):
        if cls.IsApplicable(tnpMessage):
            baseWrapperClass = cls
    return baseWrapperClass
