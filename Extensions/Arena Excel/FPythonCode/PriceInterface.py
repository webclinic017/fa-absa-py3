""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/PriceInterface.py"
import acm

from SingleValueTask import TaskInterface, TaskArguments


def FindPrice(insid, curr=None, market='SPOT'):
    ins = acm.FInstrument[insid]
    if ins is None:
        raise ValueError('Instrument {0} not found'.format(insid))
    curr = curr or ins.Currency()
    prices = [p for p in ins.Prices() if p.Market().Name().upper() == market.upper() and p.Currency().Name() == curr]
    prices = sorted(prices, key = lambda p: p.UpdateTime(), reverse=True)
    try:
        return prices[0]
    except IndexError:
        return None
    
def CreatePrice(insid, curr=None, market='SPOT', date=None):
    p = acm.FPrice()
    p.Instrument(insid)
    p.Currency(curr or acm.FInstrument[insid].Currency())
    p.Market(market)
    p.Day(date or acm.Time.DateValueDay())
    return p
    
class PriceArguments(TaskArguments):

    def __init__(self, *args):
        super(PriceArguments, self).__init__(*args)
        self._insid = None
        self._currencyName = None
        self._marketName = None
        self._priceType = None
        self._price = None
    
    @property
    def InstrumentId(self):
        if self._insid is None:
            self._insid = self.Get(0)
        return self._insid
        
    @property        
    def CurrencyName(self):
        if self._currencyName is None:
            self._currencyName = self.Get(1)
        return self._currencyName

    @property
    def PriceType(self):
        if self._priceType is None:
            self._priceType = self.Get(2)
        return self._priceType      
        
    @property        
    def MarketName(self):
        if self._marketName is None:
            self._marketName = self.Get(3)
        return self._marketName
        
    @property        
    def Price(self):
        if self._price is None:
            self._price = float(self.Get(4).replace(',', '.'))
        return self._price        

        
class SetPrice(TaskInterface):

    def __init__(self, *args):
        self._priceArgs = PriceArguments(*args)
        self.Set()
        
    def Result(self):
        return self._result
        
    def Set(self):
        try:
            price = FindPrice(self._priceArgs.InstrumentId, 
                              self._priceArgs.CurrencyName, 
                              self._priceArgs.MarketName)
            if price is None:
                price = CreatePrice(self._priceArgs.InstrumentId, 
                                    self._priceArgs.CurrencyName, 
                                    self._priceArgs.MarketName)                          
            method = getattr(price, self._priceArgs.PriceType)
            method(self._priceArgs.Price)
            price.Commit()
            self._result = ('{0.PriceType} Price for {0.InstrumentId} set to '
                            '{0.Price} {0.CurrencyName} at {1}'.format(self._priceArgs,
                                                                       acm.Time.DateTimeFromTime(price.UpdateTime())))
        except Exception as err:
            self._result = 'Error setting price: {0}'.format(err)
