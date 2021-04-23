'''
Implementation of Murabaha uploader in Python -- specification
and representation of instruments to be created in the 
Murabaha transaction.

Project:    Murabaha Uploader
Department: Markets Structuring
Requester:  Gisella Nicola Bascelli
Developer:  Peter Fabian
CR Number:  CHNG0001979991


HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
2014-10-14  2362375     Nico Louw       Added Prod types to FWD Hedge and
                                        ZC Bond Instruments.
-------------------------------------------------------------------------------

'''
import acm
import at_choice


#TODO: type check?
def value_or_exc(value, err):
    if value:
        return value
    else:
        raise ValueError(err)


class MurabahaLeg(object):
    def __init__(self, pay_leg):
        self.pay_leg = pay_leg
        self.properties = {}
        
    def setProperty(self, property_, value):
        self.properties[property_] = value
        

class MurabahaInstrument(object):
    """ This should be an abstract class for all instruments created in 
        Murabaha transaction
    """
    def __init__(self, data_provider, ins_name_storage, logger):
        self._data_provider = data_provider
        self._constants = {}
        self._variables = {}
        self._m_legs = ()
        self.logger = logger
        self.acm_ins = acm.Create(self._ins_type)
        if not self.acm_ins:
            raise RuntimeError("Ins type %s could not be created" % self._ins_type)
        
        # in case we upgrade to new, better Front Arena, increase the number here
        self._max_ins_name_length = 39  
        # to ensure instruments have unique names (even in one upload)
        self._ins_name_storage = ins_name_storage
        
    def get_variable_data(self):
        raise NotImplementedError('Subclasses must implement this method')
    
    def _get_first_recieve_leg(self):
        for leg in self._m_legs:
            if not leg.pay_leg:
                return leg
    
    def _get_first_pay_leg(self):
        for leg in self._m_legs:
            if leg.pay_leg:
                return leg
    
    def _log_property(self, obj, property_, value):
        try:
            value_name = value.Name()
        except:
            value_name = value
            
        self.logger.log("%s %s: %s\t\t=> %s" 
                        % (self.__class__.__name__, obj, property_, value_name), 
                        self.logger.DEBUG)
    
    def commit(self):
        properties = dict(self._constants.items() + self._variables.items())
        try:
            for property_, value in properties.iteritems():
                self._log_property("ins", property_, value)
                self.acm_ins.SetProperty(property_, value)
            for m_leg in self._m_legs:
                leg = self.acm_ins.CreateLeg(m_leg.pay_leg)
                for property_, value in m_leg.properties.iteritems():
                    self._log_property("leg", property_, value)
                    leg.SetProperty(property_, value)
            self.acm_ins.Commit()
        except TypeError as _:
            self.logger.log("Error setting property %s to value %s" % (property_, value))
            raise
        return self.acm_ins

        
class FwdHedge(MurabahaInstrument):
    """Step 1 in the Murabaha transaction -- Fwd hedge
    """
    def __init__(self, data_provider, ins_name_storage, logger):
        self._ins_type = "FFuture"
        super(FwdHedge, self).__init__(data_provider, ins_name_storage, logger)
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "ContractSize": 1,
            "PayDayOffset": 5,
            "ValuationGrpChlItem": value_or_exc(at_choice.get("ValGroup", "EQ_MASTER"), 
                                                   "'EQ_MASTER' val group not found"),
            "SpotBankingDaysOffset": 0,
            "MtmFromFeed": False,
            "Otc": True,
            "PayType": value_or_exc(acm.EnumFromString("PayType", "Forward"), 
                                                   "'Forward' pay type not found"),
            "QuoteType": value_or_exc(acm.EnumFromString("QuoteType", "Per 100 Units"), 
                                                   "'Per 100 Units' quote type not found"),
            "ExpiryPeriod_unit": value_or_exc(acm.EnumFromString("DatePeriodUnit", "Days"), 
                                                   "'Days' date period unit not found"),
            # there are some properties which default to different values when 
            # created from AMBA and from python code, so here they are:
            "Quotation": value_or_exc(acm.FQuotation['Per 100 Units'], 
                                                   "'Per 100 Units' quotation not found"),
            "ProductTypeChlItem": value_or_exc(at_choice.get("Product Type", "Forward"), 
                                                   "'Forward' product type not found"),
        }

    @staticmethod
    def identifier():
        return "OTC Fwd Hedge"

    def get_variable_data(self):
        self._variables = {
            "Name": self._generate_ins_name(),
            "ExpiryTime": self._exp_time(),
            "ExpiryDate": self._exp_time(),
            "Underlying": self._underlying(),
            "ExpiryPeriod_count": self._exp_period_count(),
            "SettlementType": value_or_exc(acm.EnumFromString("SettlementType", self._data_provider.settlement_type()), 
                                      "Settlement type %s not found for OTC Fwd" % self._data_provider.settlement_type()),
        }
    
    def _generate_ins_name(self):
        """ Generate next valid instrument name according
            to input parameters
            
            Must not be called to get ins name because it will
            return a name of non-existing instrument. 
        """
        underlying = self._data_provider.underlying()
        expiry = self._data_provider.expiry_day()
        date = expiry.strftime("%d%b").upper() # to get sth like 05JAN
        client_name = self._data_provider.client_name()
        base_name = "/".join([underlying, "FWD", date, "OTC", client_name])
        ord_no = self._ins_name_storage.next_ord_no_for_ins(base_name)
        if ord_no:
            ins_name = "%s#%s" % (base_name, ord_no)
        else:
            ins_name = base_name
        return ins_name[:self._max_ins_name_length]
    
    def _exp_date(self):
        return self._data_provider.expiry_day().strftime("%Y-%m-%d")
    
    def _exp_time(self):
        expiry_time = self._exp_date() + " 23:50:00"
        return expiry_time
    
    def _underlying(self):
        undName = self._data_provider.underlying()
        return acm.FInstrument[undName]
    
    def _exp_period_count(self):
        if self._data_provider.expiry_day() > self._data_provider.trade_date():
            delta = self._data_provider.expiry_day() - self._data_provider.trade_date()
        else:
            delta = self._data_provider.trade_date() - self._data_provider.expiry_day()
        return delta.days
        

class FwdDeposit(MurabahaInstrument):
    def __init__(self, data_provider, ins_name_storage, logger):
        self._ins_type = "FDeposit"
        super(FwdDeposit, self).__init__(data_provider, ins_name_storage, logger)
        
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "ValuationGrpChlItem": value_or_exc(at_choice.get("ValGroup", "AC_GLOBAL_Funded"), 
                                                   "AC_GLOBAL_Funded val group not found"),
            "MtmFromFeed": False,
            "Otc": True,
            #
            "ExpiryPeriod_unit": value_or_exc(acm.EnumFromString("DatePeriodUnit", "Months"), 
                                                   "'Months' date period unit not found"),
            "PriceFindingChlItem": value_or_exc(at_choice.get("PriceFindingGroup", "Close"), 
                                                   "'Close' price finding not found"),
            "Quotation": value_or_exc(acm.FQuotation['Yield'], 
                                                   "'Yield' quotation not found"),
            "RoundingSpecification": value_or_exc(acm.FRoundingSpec['Rounding_FX_2Dec'], 
                                                   "'Rounding_FX_2Dec' rounding spec not found"),
            "SpotBankingDaysOffset": 0,
        }
        
        leg = MurabahaLeg(False)
        self._m_legs = [leg]
        leg.properties = {
            "DayCountMethod": value_or_exc(acm.EnumFromString("DaycountMethod", "Act/365"), 
                                                   "'Act/365' daycount method not found"),
            "LegType": value_or_exc(acm.EnumFromString("LegType", "Float"), 
                                                   "'Float' leg type not found"),
            "LongStub": False,
            "PayCalendar": acm.FCalendar["ZAR Johannesburg"],
            "RollingPeriod": "0d",
            "ResetRollingAtEnd": False,
            "ResetCalendar": acm.FCalendar["ZAR Johannesburg"],
            "ResetDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Following"), 
                                                   "'Following' reset day method not found"),
            "ResetDayOffset": 0,
            "ResetType": value_or_exc(acm.EnumFromString("ResetType", "Compound"), 
                                                   "'Compound' reset type not found"),
            "StartPeriod": "10d",
            #
            "AmortDaycountMethod": value_or_exc(acm.EnumFromString("DaycountMethod", "Act/365"), 
                                                   "'Act/365' daycount method not found"),
            "Decimals": 11,
            "PriceInterpretationType": value_or_exc(acm.EnumFromString("PriceInterpretType", "As Reference"), 
                                                     "'As Reference' price interpretation type not found"),
            "StrikeType": value_or_exc(acm.EnumFromString("StrikeType", "Absolute"), 
                                                   "'Absolute' strike type not found"),
            # without the following option the end interest is not calculated
            "FloatRateFactor": 1.0,
        }
    
    @staticmethod
    def identifier():
        return "FRN"
    
    def get_variable_data(self):
        self._variables = {
            "Name": value_or_exc(self._generate_ins_name(), 
                                                   "Ins name not valid for fwd deposit"),
            #
            "ExpiryPeriod_count": self._exp_period_count(),
        }
        
        leg = self._m_legs[0]
        leg.properties.update({
            "StartDate": self._start_day(),
            "EndDate": self._end_day(),
            "Spread": self._data_provider.spread()+0.075,
            "FloatRateReference": self._float_rate(),
            "RollingPeriodBase": self._end_day(),
            "EndPeriod": self._end_period(),
            "AmortStartDay": self._start_day(),
            "AmortEndDay": self._end_day(),
            "ResetPeriod": self._reset_period(),
        })
    
    def _generate_ins_name(self):
        """ Generate next valid instrument name according
            to input parameters
            
            Must not be called to get ins name because it will
            return a name of non-existing instrument. 
        """
        curr = self._constants["Currency"].Name()
        start_date = self._data_provider.start_day().strftime("%y%m%d").upper()
        end_date = self._data_provider.end_day().strftime("%y%m%d").upper()
        ins_date = start_date + "-" + end_date
        client_name = self._data_provider.client_name()
        base_name = "/".join([curr, "JI", ins_date, client_name])
        ord_no = self._ins_name_storage.next_ord_no_for_ins(base_name)
        # the name of the instrument is linked to MurabahaInstrumentNameStore
        # be careful to change it here without adjusting the other class
        if ord_no:
            ins_name = "%s#%s" % (base_name, ord_no)
        else:
            ins_name = base_name
        return ins_name[:self._max_ins_name_length]
    
    def _end_day(self):
        return self._data_provider.end_day().strftime("%Y-%m-%d")
    
    def _start_day(self):
        return self._data_provider.start_day().strftime("%Y-%m-%d")
        
    def _end_period(self):
        daycount = int(self._data_provider.deposit_term())
        return "%sd" % daycount
    
    def _float_rate(self):
        if self._data_provider.deposit_term() < 0:
            raise ValueError("Incorrect deposit term")
        if self._data_provider.deposit_term() <= 80:
            return acm.FInstrument["ZAR-JIBAR-1M"]
        else:
            return acm.FInstrument["ZAR-JIBAR-3M"]
            
    def _reset_period(self):
        if self._data_provider.deposit_term() < 0:
            raise ValueError("Incorrect deposit term")
        if self._data_provider.deposit_term() < 92:
            return "1m"
        else:
            return "3m"

    def _exp_period_count(self):
        if self._data_provider.deposit_term() < 0:
            raise ValueError("Incorrect deposit term")
        if self._data_provider.deposit_term() < 92:
            return 1
        else:
            return 3

    def contr_size(self):
        return 1000000
            
class MurabahaSwap(MurabahaInstrument):
    def __init__(self, data_provider, ins_name_storage, logger):
        self._ins_type = "FSwap"
        super(MurabahaSwap, self).__init__(data_provider, ins_name_storage, logger)
        
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "PayDayOffset": 0,
            "ValuationGrpChlItem": value_or_exc(at_choice.get("ValGroup", "AC_OIS_ZAR"), 
                                                   "'AC_OIS_ZAR' val group not found"),
            "MtmFromFeed": False,
            "Otc": True,
            "QuoteType": value_or_exc(acm.EnumFromString("QuoteType", "Pct of Nominal"), 
                                                   "'Pct of Nominal' quote type not found"),
            #
            "SpotBankingDaysOffset": 0,
            
        }
        
        rec_leg = MurabahaLeg(False)
        rec_leg.properties = {
            "DayCountMethod": value_or_exc(acm.EnumFromString("DaycountMethod", "Act/365"), 
                                                   "'Act/365' daycount method not found"),
            "LegType": value_or_exc(acm.EnumFromString("LegType", "Float"), 
                                                   "'Float' leg type not found"),
            "LongStub": False,
            "PayCalendar": acm.FCalendar["ZAR Johannesburg"],
            "RollingPeriod": "0d",
            "ResetRollingAtEnd": False,
            "ResetCalendar": acm.FCalendar["ZAR Johannesburg"],
            "ResetDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Following"), 
                                                   "'Following' reset day method not found"),
            "ResetDayOffset": 0,
            "ResetType": value_or_exc(acm.EnumFromString("ResetType", "Compound"), 
                                                   "'Compound' reset type not found"),
            "StartPeriod": "10d",
            #
            "FloatRateFactor": 1.0,
            "PayDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Mod. Following"), 
                                                   "'Mod. Following' pay day method not found"),
            "PriceInterpretationType": value_or_exc(acm.EnumFromString("PriceInterpretType", "As Reference"), 
                                                     "'As Reference' price interpretation type not found"),
            "StrikeType": value_or_exc(acm.EnumFromString("StrikeType", "Absolute"), 
                                                   "'Absolute' strike type not found"),
        }
        
        pay_leg = MurabahaLeg(True)
        pay_leg.properties = {
            "DayCountMethod": value_or_exc(acm.EnumFromString("DaycountMethod", "Act/365"), 
                                                   "'Act/365' daycount method not found"),
            "LegType": value_or_exc(acm.EnumFromString("LegType", "Zero Coupon Fixed"), 
                                                   "'Zero Coupon Fixed' leg type not found"),
            "LongStub": False,
            "PayCalendar": acm.FCalendar["ZAR Johannesburg"],
            "RollingPeriod": "0d",
            "ResetType": value_or_exc(acm.EnumFromString("ResetType", "Compound"), 
                                                   "'Compound' reset type not found"),
            "StartPeriod": "10d",
            #
            "FloatRateFactor": 0.0,
            "FloatRateFactor2": 0.0,
            "FloatRateReference": None,
            "PayDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Mod. Following"), 
                                                   "'Mod. Following' pay day method not found"),
            "PriceInterpretationType": value_or_exc(acm.EnumFromString("PriceInterpretType", "As Reference"), 
                                                     "'As Reference' price interpretation type not found"),
            "ResetCalendar": acm.FCalendar["ZAR Johannesburg"],
            "ResetDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Mod. Following"), 
                                                   "'Mod. Following' reset day method not found"),
            "ResetDayOffset": 0,
            "StrikeType": value_or_exc(acm.EnumFromString("StrikeType", "Absolute"), 
                                                   "'Absolute' strike type not found"),
        }
        
        
        self._m_legs = [rec_leg, pay_leg]
    
    @staticmethod
    def identifier():
        return "Swap"
    
    def get_variable_data(self):
        self._variables = {
            "Name": value_or_exc(self._generate_ins_name(), 
                                               "Ins name not valid for Swap"),
            "ExpiryPeriod_count": self._exp_period_count(),
        }
        
        rec_leg = self._get_first_recieve_leg()
        rec_leg.properties.update({
            "StartDate": self._start_day(),
            "EndDate": self._end_day(),
            "Spread": self._spread(),
            "FloatRateReference": self._float_rate(),
            "RollingPeriodBase": self._end_day(),
            "EndPeriod": self._end_period(),
            "AmortStartDay": self._start_day(),
            "AmortEndDay": self._end_day(),
            "ResetPeriod": self._reset_period(),
        })
        
        pay_leg = self._get_first_pay_leg()
        pay_leg.properties.update({
            "StartDate": self._start_day(),
            "EndDate": self._end_day(),
            "FixedRate": self._fixed_rate(),
            "RollingPeriodBase": self._end_day(),
            "EndPeriod": self._end_period(),
            "AmortStartDay": self._start_day(),
            "AmortEndDay": self._end_day(),
        })
        
    def _generate_ins_name(self):
        """ Generate next valid instrument name according
            to input parameters
            
            Must not be called to get ins name because it will
            return a name of non-existing instrument. 
        """
        curr = self._constants["Currency"].Name()
        start_date = self._data_provider.start_day().strftime("%y%m%d").upper()
        end_date = self._data_provider.end_day().strftime("%y%m%d").upper()
        date = start_date + "-" + end_date
        client_name = self._data_provider.client_name()
        base_name = "/".join([curr, "IRS", "F-JI", date, client_name])
        ord_no = self._ins_name_storage.next_ord_no_for_ins(base_name)
        # the name of the instrument is linked to MurabahaInstrumentNameStore
        # be careful to change it here without adjusting the other class
        if ord_no:
            ins_name = "%s#%s" % (base_name, ord_no)
        else:
            ins_name = base_name
        return ins_name[:self._max_ins_name_length]
        
    def _end_day(self):
        return self._data_provider.end_day().strftime("%Y-%m-%d")
    
    def _start_day(self):
        return self._data_provider.start_day().strftime("%Y-%m-%d")
        
    def _end_period(self):
        daycount = int(self._data_provider.deposit_term())
        return "%sd" % daycount
    
    def _float_rate(self):
        if self._data_provider.deposit_term() < 0:
            raise ValueError("Incorrect deposit term")
        if self._data_provider.deposit_term() <= 80:
            return acm.FInstrument["ZAR-JIBAR-1M"]
        else:
            return acm.FInstrument["ZAR-JIBAR-3M"]
            
    def _reset_period(self):
        if self._data_provider.deposit_term() < 0:
            raise ValueError("Incorrect deposit term")
        if self._data_provider.deposit_term() < 92:
            return "1m"
        else:
            return "3m"
    
    def _fixed_rate(self):
        return self._data_provider.fixed_rate() * 100
    
    def _spread(self):
        return self._data_provider.spread()
    
    def contract_size(self):
        return 1000000
    
    def _exp_period_count(self):
        return (self._data_provider.end_day() - self._data_provider.start_day()).days
        
class InternalDeposit(MurabahaInstrument):
    def __init__(self, data_provider, ins_name_storage, logger):
        self._ins_type = "FDeposit"
        super(InternalDeposit, self).__init__(data_provider, ins_name_storage, logger)
        
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "ValuationGrpChlItem": value_or_exc(at_choice.get("ValGroup", "AC_GLOBAL_Funded"), 
                                                   "AC_GLOBAL_Funded val group not found"),
            "MtmFromFeed": False,
            "Otc": True,
            "PayOffsetMethod": value_or_exc(acm.EnumFromString("DatePeriodMethod", "Business Days"), 
                                                   "'Business Days' pay offset method not found"),
            "QuoteType": value_or_exc(acm.EnumFromString("QuoteType", "Yield"), 
                                                   "'Yield' quote type not found"),
            "RoundingSpecification": value_or_exc(acm.FRoundingSpec['Rounding_FX_2Dec'], 
                                                   "'Rounding_FX_2Dec' rounding spec not found"),
            "PriceFindingChlItem": value_or_exc(at_choice.get("PriceFindingGroup", "Close"), 
                                                   "'Close' price finding group not found"),
            #
            "ExpiryPeriod_unit": value_or_exc(acm.EnumFromString("DatePeriodUnit", "Months"), 
                                                   "'Months' date period unit not found"),
            "Quotation": value_or_exc(acm.FQuotation['Yield'], 
                                                   "'Yield' quotation not found"),
            "SpotBankingDaysOffset": 0,
        }
        
        leg = MurabahaLeg(False)
        self._m_legs = [leg]
        leg.properties = {
            "DayCountMethod": value_or_exc(acm.EnumFromString("DaycountMethod", "Act/365"), 
                                                   "'Act/365' daycount method not found"),
            "LegType": value_or_exc(acm.EnumFromString("LegType", "Fixed"), 
                                                   "'Fixed' leg type not found"),
            "LongStub": False,
            "PayCalendar": acm.FCalendar["ZAR Johannesburg"],
            "RollingPeriod": "0d",
            "ResetRollingAtEnd": False,
            "ResetPeriod": "1d",
            "ResetCalendar": acm.FCalendar["ZAR Johannesburg"],
            "ResetDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Following"), 
                                                   "'Following' reset day method not found"),
            "ResetDayOffset": 0,
            # acm.EnumFromString("ResetType", "None") this throws runtime error, not sure why
            "ResetType": 0,
            "PayDayMethod": value_or_exc(acm.EnumFromString("BusinessDayMethod", "Following"), 
                                                   "'Following' pay day method not found"),
            "NominalAtEnd": True,
            "StrikeType": value_or_exc(acm.EnumFromString("StrikeType", "Absolute"), 
                                                   "'Absolute' strike type not found"),
            "PriceInterpretationType": value_or_exc(acm.EnumFromString("PriceInterpretType", "As Reference"), 
                                                    "'As Reference' price interpretation type not found"),
            #
            "AmortDaycountMethod": value_or_exc(acm.EnumFromString("DaycountMethod", "Act/365"), 
                                                   "'Act/365' daycount method not found"),
            "Decimals": 11,
            # without the following option the end interest is not calculated
            "FloatRateFactor": 1.0,
        }
    
    @staticmethod
    def identifier():
        return "Internal Deposit"
    
    def get_variable_data(self):
        self._variables = {
            "Name": value_or_exc(self._generate_ins_name(), 
                                               "Incorrect instrument name for internal deposit"),
            #
            "ExpiryPeriod_count": self._exp_period_count(),
        }
        
        leg = self._m_legs[0]
        leg.properties.update({
            "StartDate": self._start_day(),
            "EndDate": self._end_day(),
            "RollingPeriodBase": self._end_day(),
            "EndPeriod": self._end_period(),
            "AmortStartDay": self._start_day(),
            "AmortEndDay": self._end_day(),
            "FixedRate": self._fixed_rate(),
        })
    
    def _generate_ins_name(self):
        """ Generate next valid instrument name according
            to input parameters
            
            Must not be called to get ins name because it will
            return a name of non-existing instrument. 
        """
        # don't forget to add # when more instrument with same dates are created in one batch
        input_insid = self._data_provider.input_insid()
        client_name = self._data_provider.client_name()
        base_name = "/".join([input_insid, client_name])
        ord_no = self._ins_name_storage.next_ord_no_for_ins(base_name)
        # the name of the instrument is linked to MurabahaInstrumentNameStore
        # be careful to change it here without adjusting the other class
        if ord_no:
            ins_name = "%s#%s" % (base_name, ord_no)
        else:
            ins_name = base_name
        return ins_name[:self._max_ins_name_length]
        
    def _end_day(self):
        return self._data_provider.end_day().strftime("%Y-%m-%d")
    
    def _start_day(self):
        return self._data_provider.start_day().strftime("%Y-%m-%d")
        
    def _fixed_rate(self):
        return self._data_provider.fixed_rate() * 100
        
    def _end_period(self):
        daycount = int(self._data_provider.deposit_term())
        return "%sd" % daycount
    
    def _exp_period_count(self):
        if self._data_provider.deposit_term() < 0:
            raise ValueError("Incorrect deposit term")
        if self._data_provider.deposit_term() < 92:
            return 1
        else:
            return 3
    
    def contract_size(self):
        return 1000000
        
class ClientDeposit(InternalDeposit):

    @staticmethod
    def identifier():
        return "Client Deposit"

