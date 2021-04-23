""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FOrderBookCreator.py"
from __future__ import print_function
import acm
import FOrderUtils

class OBListener(object):
    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) == 'insert':
            print('New order book for {0} on market {1} inserted in ADS'.format(
                    param.Instrument().Name(), param.MarketPlace().Name()))
            param.RemoveDependent(self)


class OrderBookCreator(object):
    TICK_SIZE_LIST = 1001
    LIST_ID = 1001 #'IM Default Shares'
    
    def __init__(self, instrument, marketName=None, currency=None, listener=OBListener()):
        self._marketName = marketName
        self._instrument = instrument
        self._currency = currency
        self._listener = listener
    
    def OrderBookQuery(self):
        query = 'instrument="{0}" and marketPlace="{1}" and currency="{2}"'.format(
                    self._instrument.Name(), self.Market().Name(), self.Currency().Name())
        return acm.FOrderBook.Select(query)
    
    def CreateOrderBook(self):
        self.Market().Connect(2000)
        assert self.Market().IsConnected(), "Could not connect to market '%s'"%(self.Market().Name())
        self.OrderBookQuery().AddDependent(self._listener)
        info = self.CreateOrderBookCreateInfo()
        info.Create()
        print("Orderbook '%s' sent to market '%s'"%(self._instrument.Name(), self.Market().Name()))

    def CreateOrderBookCreateInfo(self):
        info = acm.FMarketOrderBookCreateInfo(self.Market())
        info.Name(self._instrument.Name())
        info.Currency(self.Currency())
        info.TickSizeList(self.TickSizeList())
        info.ListId(self.ListId())
        info.MarketInstrumentId(self.MarketInstrumentId())
        info.Isin(self._instrument.Isin())
        #info.MinimumOrderQuantity(0)
        #info.MaximumOrderQuantity(1000000)
        info.InsType(self.OBInstrumentType())
        return info
        
    def OBInstrumentType(self):
        supportedInsTypes = ['Stock', 'Convertible', 'Bond', 'Premium', 'Option', 'Commodity']    
        insType =  self._instrument.InsType()
        
        if insType == 'Curr':
            return 'Currency'
    
        if insType in supportedInsTypes:
            return insType
        
        return 'Stock'
        
    def TickSizeList(self):
        return self.TICK_SIZE_LIST
        
    def ListId(self):
        return self.LIST_ID
        
    def Market(self):
        assert self._marketName, "Market name required"
        return acm.FParty[self._marketName]

    def Currency(self):
        return self._currency or self._instrument.Currency()
        
    def MarketInstrumentId(self):
        return self._instrument.Isin() or self._instrument.Name()


class AIMSOrderBookCreator(OrderBookCreator):
    TICK_SIZE_LIST = 1001
    def Market(self):
        return FOrderUtils.GetPrimaryMarket()
    
class FIXAMASOrderBookCreator(OrderBookCreator):
    TICK_SIZE_LIST = 1600000

def CreateOrderBookMenuItem(eii):
    ins = eii.ExtensionObject().OriginalInstrument()
    marketName = eii.MenuExtension().GetString('Market')
    try:
        AIMSOrderBookCreator(ins).CreateOrderBook()
        FIXAMASOrderBookCreator(ins, marketName).CreateOrderBook()
    except StandardError as e:
        acm.UX.Dialogs().MessageBoxInformation(acm.UX.SessionManager().Shell(), e) 