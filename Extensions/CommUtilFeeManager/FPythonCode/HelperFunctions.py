'''
MODULE
    HelperFunctions - class that contains functions used by the rest of the CommUtilFeeManger module

HISTORY
	Date            Developer               Notes
        2017-10-09      Ntuthuko Matthews       created	
	2018-03-27      Ntuthuko Matthews	renamed get_rate_range to get_rate_utilised_ranges	
'''


import ael
import acm
import json
from at_logging import getLogger
from datetime import datetime, date


class HelperFunctions(object):
    LOGGER = getLogger(__name__)
    
    def __init__(self):
        self.parsed_json = None
        self.TEXT_OBJECT_NAME = None

    @staticmethod
    def fee_type(feeType):
        if feeType:
            return {'Commitment':'CMF', 'Utilization':'UTF'}[feeType]
        return None
    
    @staticmethod
    def date_format(date_time, to_format="%Y-%m-%d"):
        _date = None
        from_format = "%d/%m/%Y"
        if isinstance(date_time, int) or isinstance(date_time, long):
            _date = date.fromtimestamp(date_time).isoformat()
        elif isinstance(date_time, str):
            _date = datetime.strptime(date_time, from_format).strftime(to_format)
        else:
            _date = datetime.strptime(date_time.to_string(), from_format).strftime(to_format)
        return ael.date(_date)

    @staticmethod
    def date_from_time(time):
        if isinstance(date_time, int) or isinstance(date_time, long):
            return date.fromtimestamp(date_time).isoformat()
        return None

    @staticmethod
    def date_from_string(date_string, to_format="%d/%m/%Y"):
        from_format = "%Y-%m-%d"
        if isinstance(date_string, str):
            return datetime.strptime(date_string, from_format).strftime(to_format)
        return None
        
    def load_json(self, text):
        self.parsed_json = json.loads(text)
        return self.parsed_json

    def add_json(self, text):
        self.parsed_json = json.dumps(text)
        return self.parsed_json

    def get_period_days(self, dataAccess, trade, cmfTrades, key='UTF'):
        try:
            return cmfTrades._get_date_period()
        except Exception, e:
            self.LOGGER.error('{0}'.format(e))
            return 0

    def drange(self, start, end, step=0.01):
        lst = []
        lst.append(start)
        while end > start:
            start = round((start + step), 2)
            lst.append(start)
        return lst

    def get_rate_utilised_ranges(self, ratesUtilFee, index):
        rate_from = getattr(ratesUtilFee, 'RateFrom{0}'.format(index))
        rate_to = getattr(ratesUtilFee, 'RateTo{0}'.format(index))
        return self.drange(rate_from, rate_to)
    
    def get_rate_list(self, ratesUtilFee, index):
        lst = []
        rate_from = getattr(ratesUtilFee, 'RateFrom{0}'.format(index))
        rate_to = getattr(ratesUtilFee, 'RateTo{0}'.format(index))
        if rate_from>0:
            return [rate_from, rate_to]
        return lst

    def get_rate(self, dataAccess, num, trade):
        rate_dict = {}
        self.TEXT_OBJECT_NAME = trade.Name()
        record = dataAccess.Select(self.TEXT_OBJECT_NAME)
        if not record:
            self.LOGGER.warning('Could not be find a record.')
            return 0

        for k, v in enumerate(record):
            if k < 10:
                rateFrom = str(record['RateFrom{0}'.format(k+1)])
                rateTo = str(record['RateTo{0}'.format(k+1)])
                rate = str(record['Rate{0}'.format(k+1)])
                if rateFrom and rateTo and rate:
                    rate_dict.update({'RateFrom{0}'.format(k+1) : (
                                    self.drange(float(rateFrom), float(rateTo)+1),
                                    float(rate)
                                     )
                                 })
        try:
            return [lst[1] for lst in rate_dict.values() if num in lst[0]][0]
        except Exception, e:
            self.LOGGER.error('Could not determine the Utilization rate. The Facility Limit is less than or equal to the Current Nominal')
            return 0

    def get_trade_list(self):
        """
        This assumes the trade filter is not selected.
        """
        import CommFeeCalculation as calc
        
        #fetch all the trades from mentis portfolios
        mentis_trade_list_raw = [
            trade
            for p in calc.PF_LIST
            for trade in acm.FPhysicalPortfolio[p].Trades()
        ]

        mentis_trade_list = calc.filter_valid_trades(mentis_trade_list_raw)

        loan_trade_list = [
            trade
            for trade in mentis_trade_list
            if trade.Instrument().InsType() not in calc.INS_TYPE_LIST
        ]

        return loan_trade_list
