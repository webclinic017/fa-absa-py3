import CAL_Types as Clas
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils
import amb
import acm
from datetime import datetime
import CAL_Feeds_Utils
import at_time
from SecureConfigReader import SecureConfigReader
import xml.dom.minidom as xml
import FOperationsUtils as Utils

CONFIG_MODULE = 'CALConfigSettings'
traderIdAndHRMapping = {}

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

important_trd_fields = set(['acquire_day',
                            'curr.insid',
                            'fee',
                            'premium',
                            'price',
                            'quantity',
                            'time',
                            #'trade_curr',
                            #'trade_process',
                            #'type',
                            #'pv',
                            'value_day'])

trd_fields_to_acm = {"acquire_day" : "AcquireDay",
                     "curr.insid" : "Currency().Name",
                     "fee" : "Fee",
                     "premium" : "Premium",
                     "price" : "Price",
                     "quantity" : "Quantity",
                     "time" : "TradeTime",
                     "value_day" : "ValueDay"
                    }
                            
class CalFeedsDataExtractor(object):
    
    def __init__(self, mbf_trade_object):
        
        self.__trade_mbf = mbf_trade_object
        trade_number = int(AMBA_Utils.get_AMBA_Object_Value(self.__trade_mbf, "TRDNBR"))
        self.__trade = acm.FTrade[trade_number]
        configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, "CALTraderHRIds")

        domXml = xml.parseString(configuration)
    
        traderNodes = domXml.getElementsByTagName('Trader')

        for traderNode in traderNodes:
            userId = traderNode.getAttribute('UserId')
            hrId = traderNode.getElementsByTagName('HRId')[0].childNodes[0].data
            traderIdAndHRMapping[userId] =  hrId   
    
    def __extract_static_cal_data(self, cal_trade_data, class_name):
        
        secureConfigReader = SecureConfigReader(CONFIG_MODULE)
        
        cal_trade_data.orgin_trd_sys =  secureConfigReader.getElementValue('TradeSystem')
        event_entry_location = secureConfigReader.getElementValue('EventEntryLocation')
        
        if self.__trade.Portfolio() and self.__trade.Portfolio().PortfolioOwner():
            cal_trade_data.event_entry_location = self.__trade.Portfolio().PortfolioOwner().Country()
        else:
            cal_trade_data.event_entry_location = event_entry_location
            
        cal_trade_data.book_system = secureConfigReader.getElementValue('BookSystem')
        cal_trade_data.region_code = "EMEA"
                    
        trade_counterparty = self.__trade.Counterparty()
        
        cal_trade_data.counterparty_id = ''
        
        if trade_counterparty:
            if hasattr(trade_counterparty.AdditionalInfo(), "BarCap_SMS_CP_SDSID"):
                cal_trade_data.counterparty_id = trade_counterparty.AdditionalInfo().BarCap_SMS_CP_SDSID()
                if not cal_trade_data.counterparty_id:
                    cal_trade_data.counterparty_id = '0'
            else:
                cal_trade_data.counterparty_id = '0'
        
        cal_trade_data.business_date = datetime.now().date().strftime("%Y/%m/%d")
        
        if self.__trade.Instrument().Otc():
            cal_trade_data.is_otc = "Yes"
        
        else:
            cal_trade_data.is_otc = "No"
        
        trading_datetime = datetime.strptime(self.__trade.TradeTime(), DATE_FORMAT)
        
        cal_trade_data.trade_date = trading_datetime.date()
        
        if self.__trade.Portfolio():
            cal_trade_data.book_id = self.__trade.Portfolio().Oid()
            cal_trade_data.book_name = self.__trade.PortfolioId()       
        
        traderId = self.__trade.TraderId()
        
        if traderId in traderIdAndHRMapping:
            traderId = traderIdAndHRMapping[traderId]        
        
        cal_trade_data.trade_booked_by_gid = traderId
        #booked_by_user = acm.FUser[cal_trade_data.trade_booked_by_gid.upper()]
        
        cal_trade_data.trade_booked_by_AB = 0
        
        if acm.FUser[self.__trade.TraderId()]:
            user = acm.FUser[self.__trade.TraderId()]
            if hasattr(user, 'AdditionalInfo') and hasattr(user.AdditionalInfo(), "AB_Number"):
                cal_trade_data.trade_booked_by_AB = acm.FUser[self.__trade.TraderId()].add_info('AB Number')
                
        #self.__extract_trader_id(trader_type = "trade_updated_by")
        #updated_by_user = acm.FUser[cal_trade_data.trade_updater_gid.upper()]
        
        cal_trade_data.trade_id = self.__trade.Oid()

        cal_trade_data.settlement_date = self.__trade.AcquireDay()
        cal_trade_data.trade_quantity = self.__trade.Quantity()
        cal_trade_data.trade_price = self.__trade.Price()
        
        if self.__trade.Nominal() < 0:
            cal_trade_data.trade_side = "Sell"
         
        else:
            cal_trade_data.trade_side = "Buy"
            
        cal_trade_data.trade_rate = self.__trade.InterestRateAtTradeTime()
        
        version = AMBA_Utils.get_AMBA_Object_Value(self.__trade_mbf, "VERSION_ID")
        
        if ((version == None) or (len(version)==0) or (not isinstance(int(version), int))):
            version = 0        
        
        cal_trade_data.version_number = version
        
        if class_name == 'N':
            if self.__trade.TradeTime().split(' ')[1] == '00:00:00':
                print('Zero hours trade time:%s, Execution time being assigned to Event_entry_time '%self.__trade.TradeTime())
                execution_time = at_time.datetime_from_string(self.__trade.ExecutionTime())            
                cal_trade_data.event_entry_time = execution_time.strftime(DATE_FORMAT)
            else:
                cal_trade_data.event_entry_time = self.__trade.TradeTime()
        else:
            if acm.FUser[self.__trade.TraderId()]:
                user = acm.FUser[self.__trade.TraderId()]
                if hasattr(user, 'AdditionalInfo') and hasattr(user.AdditionalInfo(), "AB_Number"):
                    cal_trade_data.trade_updater_AB = acm.FUser[self.__trade.UpdateUser().Name()].add_info('AB Number')             
            
            updaterId = self.__trade.UpdateUser().Name()
            
            if updaterId in traderIdAndHRMapping:
                updaterId = traderIdAndHRMapping[updaterId] 
            
            cal_trade_data.trade_updater_gid = updaterId
            cal_trade_data.event_entry_time = datetime.fromtimestamp(self.__trade.UpdateTime())            
            cal_trade_data.event_entry_time = cal_trade_data.event_entry_time.strftime(DATE_FORMAT)
        
        try:
            space =  acm.Calculations().CreateStandardCalculationsSpaceCollection()
            pv_object = self.__trade.Calculation().PresentValue(space)
            cal_trade_data.pv = pv_object.Number()
            if class_name == 'C':
                cal_trade_data.pv = 0
                cal_trade_data.pv_delta = pv_object.Number()
        
        except:
            cal_trade_data.pv = ""
        
        cal_trade_data.pv_delta = ""
        
        IsinInstrumentIdentity = self.__trade.Instrument().Isin()
        
        CusipInstrumentIdentity = None
        
        SedolInstrumentIdentity = None
        
        if (IsinInstrumentIdentity is not None) and len(IsinInstrumentIdentity)>0 :
            cal_trade_data.product_description = str(IsinInstrumentIdentity)
            cal_trade_data.product_description_type = 'ISIN'
        
        elif (CusipInstrumentIdentity is not None) and len(CusipInstrumentIdentity)>0:
            cal_trade_data.product_description = str(CusipInstrumentIdentity)
            cal_trade_data.product_description_type = 'CUSIP'
            
        elif (SedolInstrumentIdentity is not None) and len(SedolInstrumentIdentity)>0 :
            cal_trade_data.product_description = str(SedolInstrumentIdentity)
            cal_trade_data.product_description_type = 'SEDOL'
            
        else:
            cal_trade_data.product_description_type = 'None'
        
        cal_trade_data.currency = self.__trade.Instrument().Currency().Name()
        
        cal_trade_data.product_type = self.__trade.Instrument().InsType()
        
	if self.__trade.Instrument().Underlying():	
            cal_trade_data.underlying_instrument = self.__trade.Instrument().Underlying().Cid()            
        else:
            cal_trade_data.underlying_instrument = ''

        return cal_trade_data
    
    def __extract_trader_id(self, trader_type = "trade_booked_by"):
        
        if self.__trade.TraderId() == "":
            return ""
        
        user_principals = None
        
        if trader_type == "trade_booked_by":
            user_principals = acm.FPrincipalUser.Select('user=%s' % self.__trade.Trader().Oid())
            
        elif trader_type == "trade_updated_by":
            user_principals = acm.FPrincipalUser.Select('user=%s' % self.__trade.UpdateUser().Oid())
            
        trader_id = ""
        
        for user_principal in user_principals:
        
            if user_principal != None:
                if user_principal.Type() != None:
                    if user_principal.Type() == "Kerberos":
                        principal_string = user_principal.Principal()
                        trader_id = principal_string.split('@')[0]
                        return trader_id
                else:
                    return self.__trade.Trader().Name()
            else:
                return self.__trade.Trader().Name()
        
        return self.__trade.Trader().Name() 
    def __extract_trade_amendments(self, cal_trade_data):
        """Extract changes made to important trade fields."""
        
        global important_trd_fields
        
        changed_field_names = []
        old_values = []
        new_values = []
        
        for trd_field in important_trd_fields:
            amended_version = trd_field.upper()
            previous_version = '!' + trd_field.upper()
            amended_field = AMBA_Utils.object_by_name(self.__trade_mbf, ['!'], amended_version)
            
            if amended_field:
                
                changed_field_names.append(trd_field.upper())
                old_values.append(AMBA_Utils.get_AMBA_Object_Value(self.__trade_mbf, previous_version))
                new_values.append(AMBA_Utils.get_AMBA_Object_Value(self.__trade_mbf, amended_version))
        
        if len(changed_field_names) == 0:
            return None
        
        cal_trade_data.amended_field = changed_field_names
        cal_trade_data.old_value = old_values
        cal_trade_data.new_value = new_values
        
        return cal_trade_data
    
    def extract_late_or_cancelled_trade_data(self, is_cancelled_trade = False):
        if is_cancelled_trade:
            cal_trade_data = Clas.CalTrade(Clas.Clas_Flag.Cancelled)
            cal_trade_data = self.__extract_static_cal_data(cal_trade_data, Clas.Clas_Flag.Cancelled)
            if cal_trade_data:            
                cal_trade_data = self.calculate_pv_delta(cal_trade_data)            
        else:
            cal_trade_data = Clas.CalTrade(Clas.Clas_Flag.Late)
            cal_trade_data = self.__get_late_activity_indicator(cal_trade_data)
            cal_trade_data = self.__extract_static_cal_data(cal_trade_data, Clas.Clas_Flag.Late)
        
        return cal_trade_data
        
    def extract_amended_trade_data(self):
        
        cal_trade_data = Clas.CalTrade(Clas.Clas_Flag.Amended)
        cal_trade_data = self.__extract_static_cal_data(cal_trade_data, Clas.Clas_Flag.Amended)
        cal_trade_data = self.__extract_trade_amendments(cal_trade_data)
        
        if cal_trade_data:            
            cal_trade_data = self.calculate_pv_delta(cal_trade_data)
            return cal_trade_data
            
        else:
            return None
    
    def extract_new_trade_data(self):
        
        cal_trade_data = Clas.CalTrade(Clas.Clas_Flag.New)
        cal_trade_data = self.__extract_static_cal_data(cal_trade_data, Clas.Clas_Flag.New)        
        
        return cal_trade_data        
    
    def calculate_pv_delta(self, cal_trade_data):
    
        old_trade = self.__trade
        
        for n in range(len(cal_trade_data.amended_field)):
            acm_amended_field = trd_fields_to_acm[cal_trade_data.amended_field[n].lower()]

            try:
                getattr(old_trade, acm_amended_field)(cal_trade_data.old_value[n])
                
            except:
                continue
        
        space =  acm.Calculations().CreateStandardCalculationsSpaceCollection()
        pv_object = old_trade.Calculation().PresentValue(space)
        previous_pv = pv_object.Number()
        
        current_pv = cal_trade_data.pv
        
        pv_difference = current_pv - previous_pv
        
        cal_trade_data.pv_delta = pv_difference
        
        return cal_trade_data
    
    def __get_late_activity_indicator(self, cal_trade_data):
        
        trade_datetime = at_time.to_datetime(self.__trade.TradeTime()) #datetime.strptime(self.__trade.TradeTime(), "%Y-%m-%d %H:%M:%S")
        trade_update_datetime = at_time.to_datetime(self.__trade.UpdateTime()) #datetime.fromtimestamp(self.__trade.UpdateTime())
        
        if trade_datetime.date() == trade_update_datetime.date():
            cal_trade_data.activity_ind = "T0"
        
        elif trade_datetime.date() < trade_update_datetime.date():
            cal_trade_data.activity_ind = "Post T0"
        
        return cal_trade_data
