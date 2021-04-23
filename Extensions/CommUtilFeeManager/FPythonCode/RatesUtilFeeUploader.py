'''
MODULE
    RatesUtilFeeUploader - This module provides content how handle Commitment fees.

HISTORY
	Date            Developer               Notes
        2018-03-27      Ntuthuko Matthews       created
'''


from at_logging import getLogger
from DataAccessUtil import DataAccess
from DataClass import RatesUtilFee


class RatesUtilFeeModel(object):
    LOGGER = getLogger(__name__)
    
    def __init__(self, trade):
        self.record = None
        self.ratesUtilFee = None
        self.TEXT_OBJECT_NAME = trade.Name()
        self.dataAccess = DataAccess()

    def Put(self, ratesUtilFee):
        try:
            self.ratesUtilFee = ratesUtilFee
            temp = [{'RateFrom{0}'.format(i): str(getattr(self.ratesUtilFee, 'RateFrom{0}'.format(i))) 
                                                    if getattr(self.ratesUtilFee, 'RateFrom{0}'.format(i)) else "0",
                     'RateTo{0}'.format(i): str(getattr(self.ratesUtilFee, 'RateTo{0}'.format(i))) 
                                                    if getattr(self.ratesUtilFee, 'RateTo{0}'.format(i)) else "",
                     'Rate{0}'.format(i): str(getattr(self.ratesUtilFee, 'Rate{0}'.format(i))) 
                                                    if getattr(self.ratesUtilFee, 'RateTo{0}'.format(i)) else ""
                    } for i in range(1, self.ratesUtilFee.Size())
                ]
            self.record = {}
            
            for i in temp:
                self.record.update(i)

            self.dataAccess.Save([self.record], self.TEXT_OBJECT_NAME)
        except Exception as e:
            self.LOGGER.exception('Object not saved {0}'.format(str(e)))

    def New(self):
        self.ratesUtilFee = RatesUtilFee()
        return self.ratesUtilFee

    def Get(self):
        self.record = self.dataAccess.Select(self.TEXT_OBJECT_NAME)
        self.ratesUtilFee = self.New()

        if self.record:
            for i in range(1, self.ratesUtilFee.Count()):
                rate_from = 'RateFrom{0}'.format(i)
                rate_to = 'RateTo{0}'.format(i)
                rate = 'Rate{0}'.format(i)
                
                setattr(self.ratesUtilFee, rate_from, str(self.record['RateFrom{0}'.format(i)]))
                setattr(self.ratesUtilFee, rate_to, str(self.record['RateTo{0}'.format(i)]))
                setattr(self.ratesUtilFee, rate, str(self.record['Rate{0}'.format(i)]))

        return self.ratesUtilFee

    def Remove(self, tradeNumber):
        self.TEXT_OBJECT_NAME = tradeNumber
        self.dataAccess.Delete(self.TEXT_OBJECT_NAME)

    def Dispose(self):
        self.dataAccess = None
        self.ratesUtilFee = None

