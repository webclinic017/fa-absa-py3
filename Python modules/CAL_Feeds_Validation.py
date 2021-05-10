import amb
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils
import CAL_Types as Clas
from datetime import datetime
import acm
import at_time as at_time

class CalTradeValidator(object):
    
    def __init__(self, mbf_trade_object):
        self.__trade_mbf = mbf_trade_object
        self.trade_number = int(AMBA_Utils.get_AMBA_Object_Value(self.__trade_mbf, "TRDNBR"))
        valueDay = AMBA_Utils.get_AMBA_Object_Value(mbf_trade_object, "VALUE_DAY")        
        self.__trade = acm.FTrade[self.trade_number]
        self.__trade_status = self.__trade.Status().lower()
        
        self.valueDayDateObj = at_time.to_datetime(valueDay)
        self.dateNowObj = at_time.to_datetime(datetime.now().date().strftime("%Y-%m-%d"))
        
        space =  acm.Calculations().CreateStandardCalculationsSpaceCollection()
        pv_object = self.__trade.Calculation().PresentValue(space)
        self.pv = pv_object.Number()
        
    def is_settled_trade(self):
        if acm.FTrade[self.trade_number] is not None:
            return self.valueDayDateObj and self.dateNowObj and (self.valueDayDateObj < self.dateNowObj and self.pv == 0)
        else:
            pass
    
    def is_late_trade(self):
        
        trading_datetime = datetime.strptime(self.__trade.TradeTime(), "%Y-%m-%d %H:%M:%S")
        execution_datetime = at_time.datetime_from_string(self.__trade.ExecutionTime())
        self.__trade_status = self.__trade.Status().lower()
        
        if self.__trade_status not in ["void", "terminated", "confirmed void", "simulated"]:
        
            return trading_datetime.date() < execution_datetime.date()
            
        else:
            False
        
    def is_cancelled_trade(self):
        return self.__trade_status in ["void", "terminated", "confirmed void"] and self.__trade_status not in ["simulated"]
            
    def is_amended_trade(self):
        
        trading_datetime = datetime.strptime(self.__trade.TradeTime(), "%Y-%m-%d %H:%M:%S")
        execution_datetime = at_time.datetime_from_string(self.__trade.ExecutionTime())
        self.__trade_status = self.__trade.Status().lower()
        
        if self.__trade_status not in ["void", "terminated", "confirmed void", "simulated"] and not (trading_datetime.date() < execution_datetime.date()):
            return self.__trade_mbf.mbf_get_value().lower() == "!trade"
            
    def is_new_trade(self):
        if self.__trade_status not in ["void", "terminated", "confirmed void", "simulated"]:
            return self.__trade_mbf.mbf_get_value().lower() == "+trade"
