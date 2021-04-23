import amb
import acm
from CAL_Feeds_Validation import CalTradeValidator
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils
from CAL_Feeds_Reporting import CalFeedsOutput
import CAL_Feeds_Reporting as CAL_Reporting
import CAL_Types as Clas
import CAL_Feeds_Extraction as CAL_Extract

import FOperationsUtils as Utils


class CalFeedsProcessor(object):
    
    def __init__(self, amba_mbf):
        self.amba_message = amba_mbf
        self.trade_check = None
    
    def process_trade_ambas(self):
        
        mbf_trade_object = self.get_cal_trade_obj_from_amba()
        if mbf_trade_object:
            tag_name = mbf_trade_object.mbf_get_value().lower()
            if tag_name not in ["+trade", "!trade"]:
                return None
        
        else:
            print('Returning None')
            return None

        try:
            self.trade_check = CalTradeValidator(mbf_trade_object)
        
        except Exception as error: 
            Utils.Log(True, error)
            return None

        self.process_affected_trades(mbf_trade_object)       
    
    def get_cal_trade_obj_from_amba(self):
    
        trade_obj = AMBA_Utils.object_by_name(self.amba_message, ["+", "!"], "TRADE")
        
        if trade_obj:
            return trade_obj
        else:
            return None
    
    def process_affected_trades(self, mbf_trade_object):
        
        data_extraction = CAL_Extract.CalFeedsDataExtractor(mbf_trade_object)

        self.__trade_mbf = mbf_trade_object
        self.trade_number = int(AMBA_Utils.get_AMBA_Object_Value(self.__trade_mbf, "TRDNBR"))

        trade = acm.FTrade[self.trade_number]


        if trade and trade.Trader() is not None:

            if self.trade_check.is_settled_trade():
                print("Settled trade detected.")

            if self.trade_check.is_cancelled_trade():
                print("Cancelled trade detected.")
                cal_trade_data = data_extraction.extract_late_or_cancelled_trade_data(is_cancelled_trade = True)
                cal_output = CalFeedsOutput()
                output_row = cal_trade_data.get_csv_row()
                cal_output.add_row_to_csv(output_row)
                
            elif self.trade_check.is_amended_trade():
                print("Amended trade detected.")
                cal_trade_data = data_extraction.extract_amended_trade_data()
                if cal_trade_data == None:
                    return None
                
                cal_output = CalFeedsOutput()
                output_row = cal_trade_data.get_csv_row()
                cal_output.add_row_to_csv(output_row)
            
            elif self.trade_check.is_late_trade():
                print("Late trade detected.")
                cal_trade_data = data_extraction.extract_late_or_cancelled_trade_data(is_cancelled_trade = False)
                cal_output = CalFeedsOutput()
                output_row = cal_trade_data.get_csv_row()
                cal_output.add_row_to_csv(output_row)
            
            elif self.trade_check.is_new_trade():
                print("New trade detected.")
                cal_trade_data = data_extraction.extract_new_trade_data()
                cal_output = CalFeedsOutput()
                output_row = cal_trade_data.get_csv_row()
                cal_output.add_row_to_csv(output_row)
        else:
            print('Trade failed validation conditions:')
            print(('TradeId:%s'%self.trade_number)) 
               
            if trade.Trader():
                print(('Trader:%s'%trade.Trader().Name()))
                print(('Trader UserGroup:%s'%trade.Trader().UserGroup().Name()))
                if trade.UpdateUser():
                    print(('Update UserGroup:%s'%trade.UpdateUser().UserGroup().Name()))
                
        return
