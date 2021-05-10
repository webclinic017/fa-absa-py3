""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLFXRatesUploadPerform.py"
import acm
import math
import traceback
from FACLFunctions import FACLDateStringToCQSString

class FACLFXRatesUploadPerform:
    
    def __init__(self, writer, msgBuilder, logme, summary):
        self._writer = writer
        self._msgBuilder = msgBuilder
        self._calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self._baseCurrency = None
        self._today = acm.Time().DateToday()
        self._todayAcrFormated = FACLDateStringToCQSString(self._today)
        self._logme = logme
        self._summary = summary

    def SendCurrencies(self, useMarkToMarket, baseCurrencyName, currenciesToProcess):
        self._baseCurrency = acm.FCurrency[baseCurrencyName]
        
        if useMarkToMarket:
            filterCB = self._mtmPriceFilterCB
            getPrice = self._mtmPrice
        else:
            filterCB = self._usedPriceFilterCB
            getPrice = self._usedPrice
        
        currenciesToProcess = currenciesToProcess.Filter(filterCB)
        for c in currenciesToProcess:
            price = '{0:f}'.format(getPrice(c))
            
            params = {'Reference' : c.Name(),
                      'Type' : 'Currency\Currency', 
                      'Market Data\Spot Rate' : price, 
                      'Market Data\Show Spot As Reciprocal' : 'No', 
                      'Information\Fixing Date' : self._todayAcrFormated
                     }
            self._logme('Trying to upload currency: {0} with rate {1} for date {2}'.format(c.Name(), price, self._todayAcrFormated), 'INFO')
            
            armlMessage = self._msgBuilder.CreateInstrument(params)
            self._writer.addMsgToBuffer(armlMessage, c)
            self._logme('ArmlMsg sent:\n %s' % (armlMessage), 'DEBUG')
            
        self._writer.writeBuffer()
    
    def _mtmPriceFilterCB(self, ins):
        included = False
        try:
            price = self._mtmPrice(ins)
            included = price > 0
            
            if not included:
                if math.isnan(price):
                    msg = 'MtM price is NaN'
                else:
                    msg = 'MtM price is %.2f' % (price)
                self._summary.notOk(self._summary.IGNORE, ins, 'UPLOAD', msg, ins.Oid())
        except Exception as e:
            msg = 'Exception occurred: %s' % (e)
            self._summary.notOk(self._summary.FAIL, ins, 'UPLOAD', msg, ins.Oid())
            
        return included
    
    def _mtmPrice(self, ins):
        return ins.Calculation().MarkToMarketPrice(self._calcSpace, self._today, self._baseCurrency).Value().Number()
        
    def _usedPriceFilterCB(self, ins):
        included = False
        try:
            price = self._usedPrice(ins)
            included = price > 0
            if not included:
                if math.isnan(price):
                    msg = 'Used price is NaN'
                else:
                    msg = 'Used price is %.2f' % (price)
                self._summary.notOk(self._summary.IGNORE, ins, 'UPLOAD', msg, ins.Oid())
        except Exception as e:
            msg = 'Exception occurred: %s' % (e)
            self._summary.notOk(self._summary.FAIL, ins, 'UPLOAD', msg, ins.Oid())
        
        return included
    
    def _usedPrice(self, ins):
        return ins.Calculation().MarketPrice(self._calcSpace, self._today, True, self._baseCurrency).Value().Number()
