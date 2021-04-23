
import os
import acm
import ctypes
import xml.etree.cElementTree as ElementTree
import FLogger
import FAptReportUtils

logger = FLogger.FLogger.GetLogger('APT')


class AptDatabasePath(object):
    APT_PATH = FAptReportUtils.FAptReportParameters().get('APT_INSTALLATION_PATH')
    DEFAULT_PATH = os.path.join(APT_PATH, 'Examples')
    USER_PREFERENCES_FILE = 'UserPreferences.xml'
    
    @classmethod
    def get_csidl_appdata_path(cls):
        CSIDL_APPDATA = 26
        buf = ctypes.create_unicode_buffer(1024)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_APPDATA, None, 0, buf)
        return buf.value

    @classmethod
    def get_user_preferences_path(cls):
        user_preferences_path = cls.get_csidl_appdata_path()
        try:
            os.chdir(user_preferences_path)
            for dirpath, dirnames, filenames in os.walk(os.getcwd()):
                for filename in (f for f in filenames if f == cls.USER_PREFERENCES_FILE):
                    return os.path.join(dirpath, filename)
        except WindowsError:
            return
    
    @classmethod
    def get_database_files_path(cls):
        MESSAGE = 'Could not find APTPro user preferences, using default path: %s'
        ERROR = "Databases Path not found in %s"
        user_preferences_file = cls.get_user_preferences_path()
        if not user_preferences_file:
            default_path = cls.DEFAULT_PATH
            logger.info(MESSAGE, cls.DEFAULT_PATH)
            return default_path
            
        root = ElementTree.parse(user_preferences_file)
        try:
            database_files_path = [elem.text for elem in root.findall("/locations/location") if elem.get('type') == "Database"][0]
        except IndexError:
            raise Exception(ERROR % user_preferences_file)
        return database_files_path
        
class AptTimeSeries(object):

    def __init__(self, ins_id):
        self.ins_id = ins_id
        self.ins = acm.FInstrument[ins_id]
        self.hist_prices_internal = self._get_hist_prices_internal()
        self.weekly_data = self._get_weekly_time_series()

    def _needs_dividend_adjust(self):
        if not self.ins:
            logger.warn("Warning, instrument %s not found", self.ins_id)
            return 
        dividends = self.ins.Dividends()
        return 1 if dividends else 0
        
    def _get_hist_dividends_dict(self):
        if not self.ins:
            logger.warn("Warning, instrument %s not found", self.ins_id)
            return
        hist_dividens_dict = dict((div.ExDivDay(), div.Amount()*div.TaxFactor()) for div in self.ins.Dividends())
        return hist_dividens_dict

    def _adjust_hist_price(self, price_obj, hist_dividens_dict):
        ex_div_days = sorted([day for day in hist_dividens_dict])
        divs_size = len(ex_div_days)
        price_day = price_obj.Day()
        price = price_obj.Settle()
        if not price:
            return 0
        if divs_size is 1:
            if price_day < ex_div_days[0]:
                return price*(1-hist_dividens_dict[ex_div_days[0]]/price)
        for i in range(divs_size-1):
            if price_day < ex_div_days[0]:
                return price*(1-hist_dividens_dict[ex_div_days[0]]/price)
            elif ex_div_days[i] < price_day < ex_div_days[i+1]:
                return price*(1-hist_dividens_dict[ex_div_days[i+1]]/price)
        return price
        
    def _get_hist_price(self, price_obj, hist_dividens_dict):
        if hist_dividens_dict:
            return self._adjust_hist_price(price_obj, hist_dividens_dict)
        return price_obj.Settle()
        
    def _get_returns(self, prices):
        _returns = []
        for i in range(len(prices)-1):
            try: 
                _return = (prices[i+1]/prices[i])-1.0
                _returns.append(str(_return if _return > -1 else 0))
            except ZeroDivisionError:
                _returns.append(str(0))
        return _returns
       
    def _get_hist_prices_internal(self):
        if not self.ins:
            logger.warn("Warning, instrument %s not found", self.ins_id)
            return
        m_abs = lambda price: price if price >=0 else 0
        return [m_abs(price) for price in self.ins.HistoricalPrices().SortByProperty('Day') if price.Market().Name() == 'internal']

    def get_daily_time_series(self, attr):
        WARN = "Instrument %s does not have MtM internal prices, setting price to 0.1"
        if not self.hist_prices_internal:
            if self.att == 'Day':
                return acm.Time().DateToday()
            else:
                return '0.1'
            logger.warn(WARN, self.ins_id)
            
        return '  '.join([str(getattr(hist_prices_internal[i], attr)()) for i in range(len(self.hist_prices_internal))])
        
    def get_weekly_dates(self):
        return '  '.join([d for d in sorted(self.weekly_data)])
        
    def get_weekly_returns(self):
        WARN = "Instrument %s does not have MtM internal prices, setting return to 0.0"
        ERROR = "Could not generate weekly time series for instrument %s. Not none zero price found for week starting on %s"
        try:
            try:
                prices = [p[2] for p in (self.weekly_data.get(d) for d in self.weekly_data)]
            except IndexError:
                try:
                    prices = [p[1] for p in (self.weekly_data.get(d) for d in self.weekly_data)]
                except IndexError:
                    prices = [p[0] for p in (self.weekly_data.get(d) for d in self.weekly_data)]
            if len(prices) > 1:
                return '0.0  '+'  '.join(self._get_returns(prices))
            else:
                logger.warn(WARN, self.ins_id)
                return '0.0'
        except IndexError:
            logger.error(ERROR , self.ins_id, self.weekly_data.get(d))
            raise Exception(ERROR % (self.ins_id, self.weekly_data.get(d)))
    
        
    def _get_weekly_time_series(self):
        prices_dict = {}
        hist_dividens_dict = self._get_hist_dividends_dict() if self._needs_dividend_adjust() else None
        if not self.hist_prices_internal:
            today = acm.Time().DateToday()
            last_week = acm.Time().DateAddDelta(today, 0, 0, -5)
            third_day_of_week = acm.Time().DateAddDelta(acm.Time().FirstDayOfWeek(last_week), 0, 0, 2)
            prices_dict[third_day_of_week] = [0]
            return prices_dict
        for p in self.hist_prices_internal:
            price = self._get_hist_price(p, hist_dividens_dict)
            price = price if str(price) != 'nan' else 0.1
            third_day_of_week = acm.Time().DateAddDelta(acm.Time().FirstDayOfWeek(p.Day()), 0, 0, 2)
            if third_day_of_week in prices_dict:
                prices_dict[third_day_of_week].append(price)
            else:
                prices_dict[third_day_of_week] = [price]
        return prices_dict

