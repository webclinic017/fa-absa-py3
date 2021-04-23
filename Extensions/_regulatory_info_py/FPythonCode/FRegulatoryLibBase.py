""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/RegulatoryInfoLib/Adaptations/FRegulatoryLibBase.py"
"""------------------------------------------------------------------------
MODULE
    FRegulatoryLib -
DESCRIPTION:
    This file consists of the default implementation of the API open to customizations to users
VERSION: %R%
--------------------------------------------------------------------------"""
import acm
import FIntegrationUtils
import FRegulatoryCfiCodeGeneration
import FRegulatoryLogger
import ael
import operator
import FRegulatoryLibUtils
from __builtin__ import classmethod
logger = 'FRegulatoryLibBase'
import FRegulatoryUtils
import FRegulatoryLookup
import FInstrumentClassification
import FRegulatoryNotionalAmount
import datetime
import unicodedata
space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
stage1 = (ael.date('2018-03-01'), ael.date('2019-05-15'))
stage2 = (ael.date('2019-05-16'), ael.date('2020-05-15'))
stage3 = (ael.date('2020-05-16'), ael.date('2021-05-15'))
stage4 = (ael.date('2021-05-16'),)


class InstrumentRegInfoBase(object):
    """This file consists of the support functions that are used to populate the ADM.InstrumentRegulatoryInfo. supplying logic and enabling Storage"""

    def __init__(self, instrument):
        """class that maintains all data related to the regulatory on the FTrade"""
        self.instrument = None
        self.current_date = ael.date_today()
        if instrument:
            self.instrument = instrument
            self.reg_info = self.instrument.RegulatoryInfo()
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument")

    def mifid2_rts28_instype(self):
        """get the instype for rts28 as per mifid classification"""
        return FRegulatoryLibUtils.get_rts28(self.instrument)

    def mifid2_rts2_instype(self):
        """get the instype for rts2 as per mifid classification"""
        self.__rts2_classify = FInstrumentClassification.FInstrumentClassification(self.instrument)
        return self.__rts2_classify.mifid2_rts2_instype()

    def mifid2_rts2_inssubtype(self):
        """get the inssubtype for rts2 as per mifid classification"""
        self.__rts2_classify = FInstrumentClassification.FInstrumentClassification(self.instrument)
        return self.__rts2_classify.mifid2_rts2_inssubtype()

    def isin(self):
        """returns the ISIN of the instrument"""
        isin = None
        if self.instrument:
            isin = self.instrument.Isin()
            if not isin:
                isin = FRegulatoryLibUtils.get_isin_from_alias(self.instrument)#check if there is an instrument Alias of the name ISIN
            if not isin:
                isin = FRegulatoryLibUtils.get_isin_from_addinfo(self.instrument)#check if there is an instrument AdditionalInfo of the name ISIN
            if not isin:
                FRegulatoryLogger.INFO(logger, "Instrument <%s> has no Isin on it."%self.instrument.Name())
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its Isin")
        return isin

    def cfi_code(self, set_cfi_code=False):
        """generates and returns the CFI code of the instrument (if not present), else it returns the CFI code on the instrument"""
        cfi_code = None
        if self.instrument:
            taxonomy = TaxonomyBase(self.instrument)
            cfi_code = taxonomy.cfi(None, set_cfi_code)
        return cfi_code

    @classmethod
    def isValidISIN(self, isin_val):
        """verify that the given Isin has a valid ISIN structure and checksum correct"""
        return FRegulatoryLibUtils.isValidISIN(isin_val)

    @classmethod
    def get_large_in_scale(self, average_daily_transactions, exchange_rate):
        """calc based on Orders large in scale compared with normal market size for shares and depositary receipts from RTS 1"""
        adt = float(average_daily_transactions)
        rate = float(exchange_rate)
        lisEUR = 0
        if adt < 50000:
            lisEUR = 15000
        elif adt < 100000:
            lisEUR = 30000
        elif adt < 500000:
            lisEUR = 60000
        elif adt < 1000000:
            lisEUR = 100000
        elif adt < 5000000:
            lisEUR = 200000
        elif adt < 25000000:
            lisEUR = 300000
        elif adt < 50000000:
            lisEUR = 400000
        elif adt < 100000000:
            lisEUR = 500000
        else:
            lisEUR = 650000
        return str(lisEUR * rate)

    def isLiquid(self):
        """Indicates if the security is liquid, as defined by the Committee of European Securities Regulators (CESR) under the Markets in Financial Instruments Directive (MiFID)."""
        if not self.instrument:
            FRegulatoryLogger.WARN(logger, "Invalid instrument")
            return None
        isliquid_status = False
        if self.current_date < ael.date("2018-02-16"):
            FRegulatoryLogger.WARN(logger, "Not supported before 16 Feb 2018")
            return None
        global space
        from_currency = self.instrument.Currency()
        to_currency = acm.FCurrency['EUR']
        unshifted_val = from_currency.Calculation().FXRate(space, to_currency)
        total_issued_euro = int(self.instrument.TotalIssued() * unshifted_val.Number())
        self.rts2_classify = FRegulatoryLookup.RTS2Classification(self.instrument, self.current_date)
        total_nominal_value, businessdays, dates = self.rts2_classify.get_total_nominal_value()
        dates, average_daily_trades, percentage_days_traded, first_trade_ind = self.rts2_classify.get_average_daily_trades(
            businessdays, dates)
        try:
            if (not len(self.instrument.Trades())) or first_trade_ind or (
                    ael.date(str(self.instrument.IssueDay())) <= dates[0] and ael.date(
                    str(self.instrument.IssueDay()))) >= dates[1]:
                if self.instrument.InsType() == "Bond":
                    if self.instrument.SeniorityChlItem() and self.instrument.SeniorityChlItem().Name() == "SNRFOR":
                        if ((total_issued_euro >= 1000000000 and stage1[0] <= self.current_date and stage2[
                            1] >= self.current_date) or (total_issued_euro >= 500000000 and stage3[0] <= self.current_date)):
                            isliquid_status = True
                    elif self.instrument.ValuationGrpChlItem() and self.instrument.ValuationGrpChlItem().Name() == "Government":
                        if total_issued_euro >= 1000000000:
                            isliquid_status = True
                    elif self.instrument.CategoryChlItem() and self.instrument.CategoryChlItem().Name() == "Municipal":
                        if total_issued_euro >= 500000000:
                            isliquid_status = True
                    elif self.instrument.CategoryChlItem() and self.instrument.CategoryChlItem().Name() == "Corporate":
                        if ((total_issued_euro >= 1000000000 and stage1[0] <= ael.date_today() and stage2[
                            1] >= ael.date_today()) or (
                                total_issued_euro >= 500000000 and stage3[0] <= ael.date_today())):
                            isliquid_status = True
                    else:
                        isliquid_status = False
                elif self.instrument.InsType() == "Convertible":
                    if total_issued_euro >= 500000000:
                        isliquid_status = True
                else:
                    FRegulatoryLogger.WARN(logger, "This function is applicable only for Bond instruments")
                    isliquid_status = None
            else:
                if self.instrument.InsType() in ["Bond", "Convertible"]:
                    if total_nominal_value * unshifted_val.Number() > 100000 and percentage_days_traded >= 80:
                        if stage1[0] <= self.current_date and stage1[1] >= self.current_date and average_daily_trades >= 15:
                            isliquid_status = True
                        elif stage2[0] <= self.current_date and stage2[1] >= self.current_date and average_daily_trades >= 10:
                            isliquid_status = True
                        elif stage3[0] <= self.current_date and stage3[1] >= self.current_date and average_daily_trades >= 7:
                            isliquid_status = True
                        elif stage4[0] <= self.current_date and average_daily_trades >= 2:
                            isliquid_status = True
        except Exception, e:
            FRegulatoryLogger.WARN(logger, "Insufficient information to determine liquid status")
        return isliquid_status

    def get_liquidity_band(self, compute = True):
        """get the LiquidityBand for the given instrument on the basis of the average daily turnover"""
        #liquidity_band = self.reg_info.LiquidityBand()
        liquidity_band = self.instrument.AdditionalInfo().RegLiquidityBand()
        if str(liquidity_band) == 'None' and compute:
            average_daily_turnover = self.reg_info.AverageDailyTurnover() 
            if average_daily_turnover:
                FRegulatoryLogger.INFO(logger, "The LiquidityBand cannot be inferred as the averageDailyTurnOver is not present on the instrument.")
            else:
                band = 0
                if average_daily_turnover < 0:
                    liquidity_band = 0
                elif average_daily_turnover < 10:
                    liquidity_band = 1
                elif average_daily_turnover < 80:
                    liquidity_band = 2
                elif average_daily_turnover < 600:
                    liquidity_band = 3
                elif average_daily_turnover < 2000:
                    liquidity_band = 4
                elif average_daily_turnover < 9000:
                    liquidity_band = 5
                else:
                    liquidity_band = 6 # more than 9000 transactions per day
        return liquidity_band
    
    def is_equity_like(self):
        """returns True if the instrument is an equity/equity like instrument"""
        equity_like = False
        ins_type = self.instrument.InsType()
        if not self.mifid2_rts2_instype():
            if ins_type in ['Stock', 'ETF', 'Depositary_Receipt']:
                return True
            elif ins_type in ['Combination']:
                for cons in self.instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_equity_like():
                        equity_like = True
                    else:
                        equity_like = False
                        break
        return equity_like

    def is_bond_like(self):
        """returns True if the instrument is an bond/bond like instrument"""
        bond_like = False
        if self.mifid2_rts2_instype() == 'Bonds':
            bond_like = True
        elif self.instrument.InsType() in ['Combination']:
            for cons in self.instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_bond_like():
                        bond_like = True
                    else:
                        bond_like = False
                        break
        return bond_like

    def is_interest_rate_derivative(self):
        """returns True if the instrument is an interest rate derivative instrument"""
        ir_derivative = False
        if self.mifid2_rts2_instype() == 'Interest Rate Derivatives':
            ir_derivative = True
        elif self.instrument.InsType() in ['Combination']:
            for cons in self.instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                if InstrumentRegInfoBase(cons.Instrument()).is_interest_rate_derivative():
                    ir_derivative = True
                else:
                    ir_derivative = False
                    break
        return ir_derivative

    def is_equity_derivative(self):
        """returns True if the instrument is an equity derivative instrument"""
        equity_derivative = False
        ins_type = self.instrument.InsType()
        if self.mifid2_rts2_instype() == 'Equity Derivatives':
            equity_derivative = True
        elif ins_type in ['Dividend_Point_Index', 'EquityIndex']:
            equity_derivative = True
        elif ins_type in ['Combination']:
            for cons in self.instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                if InstrumentRegInfoBase(cons.Instrument()).is_equity_derivative():
                    equity_derivative = True
                else:
                    equity_derivative = False
                    break
        return equity_derivative

    def is_c10_derivative(self):
        """returns True if the instrument is a C10 derivative instrument"""
        c10_derivative = False
        return c10_derivative

    def is_fx_derivative(self):
        """returns True if the instrument is a FX derivative instrument"""
        fx_derivative = False
        if self.mifid2_rts2_instype() == 'Foreign Exchange Derivatives':
            fx_derivative = True
        elif self.instrument.InsType() in ['Combination']:
            for cons in self.instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                if InstrumentRegInfoBase(cons.Instrument()).is_fx_derivative():
                    fx_derivative = True
                else:
                    fx_derivative = False
                    break
        return fx_derivative

    def is_cfd(self):
        """returns True if the instrument is a cfd instrument"""
        cfd = False
        if self.mifid2_rts2_instype() == 'Financial contracts for differences':
            cfd = True
        elif self.instrument.InsType() in ['Combination']:
            for cons in self.instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                if InstrumentRegInfoBase(cons.Instrument()).is_cfd():
                    cfd = True
                else:
                    cfd = False
                    break
        return cfd

class ISO3166CountryCodeBase(object):                            
    def __init__(self, custom_dict={}):
        self.__custom_dict = custom_dict
        self.__default_dict = FRegulatoryLookup.country_code_dict
        self.__city_state_lookup = FRegulatoryLookup.city_state_dict#this dict can be extended if required here
        self.__subjurisdiction_dict = FRegulatoryLookup.subjurisdiction_codes
        self.integration_utils = FIntegrationUtils.FIntegrationUtils()

    def country_code(self, party):
        """the country code will be returned for the country of the party"""
        party = self.integration_utils.get_party_handle(party)
        country_code = None
        if party and party.Country():
            country = party.Country()
            if type(country) == unicode:
                country = unicodedata.normalize('NFKD', country).encode('ascii', 'ignore')
            if self.__custom_dict and self.__custom_dict.has_key(country):
                country_code = self.__custom_dict[country]
                FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the custom dictionary provided"%country_code)
            if (not country_code) and self.__default_dict and self.__default_dict.has_key(country):#use this as a fall back mechanism
                country_code = self.__default_dict[country]
                FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the default dictionary."%country_code)
        return country_code

    def country_code_from_string(self, country):
        """return country code for the provided country name"""
        if type(country) == unicode:
            country = unicodedata.normalize('NFKD', country).encode('ascii', 'ignore')
        country_code = None
        if country:
            country = country.strip()
            if self.__custom_dict and self.__custom_dict.has_key(country):
                country_code = self.__custom_dict[country]
                FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the custom dictionary provided"%country_code)
            if (not country_code) and self.__default_dict and self.__default_dict.has_key(country):#use this as a fall back mechanism
                country_code = self.__default_dict[country]
                FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the default dictionary."%country_code)
        return country_code

    def subJurisdiction(self, country_name, city_name):
        """return the subjurisdiction if applicable"""
        state_code = ''
        sub_jurisdiction = self.country_code_from_string(country_name)

        if not sub_jurisdiction:
            FRegulatoryLogger.WARN(logger, "countryCode not found for country <%s>."%country_name)
        else:
            if self.__city_state_lookup.has_key(city_name):
                state = self.__city_state_lookup[city_name]
                if self.__subjurisdiction_dict.has_key(country_name):
                    states = self.__subjurisdiction_dict[country_name]
                    if states.has_key(state):
                        state_code = states[state]
                    else:
                        FRegulatoryLogger.WARN(logger, "subjurisdiction not found for state <%s> in country <%s>."%(state, country_name))
            else:
                FRegulatoryLogger.WARN(logger, "subjurisdiction not found for city <%s> as its state not found in city-state lookup."%(city_name))
            if state_code:
                sub_jurisdiction = sub_jurisdiction + '-' + state_code
        return sub_jurisdiction

    def city_code(self, country_name, city_name):
        """generates the business center code for a given city in a country on the basis of the country code and the name of the city"""
        city_code_val = ''
        country_code = self.country_code_from_string(country_name)
        if country_code:
            total_words = city_name.split(' ')
            if len(total_words) > 1:
                for each_word in total_words:
                    if len(city_code_val) == 2:
                        break
                    city_code_val = city_code_val + each_word[0].upper()
            else:
                city_code_val = city_name[0:2].upper()
            city_code_val = country_code + city_code_val
        else:
            FRegulatoryLogger.WARN(logger, "Cannot infer the country code as the country code for <%s> is not available in the lookup. Kindly add it to the custom_dict"%(country_name))
        return city_code_val

class PartyRegInfoBase(object):
    def __init__(self, party):
        self.integration_utils = FIntegrationUtils.FIntegrationUtils()
        self.party = party#self.integration_utils(party)
        self.default_jurisdiction_dic = {'ESMA': ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'GR', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'GB'],
                                         'SEC': ['US'],
                                         'CSRC': ['CN'],
                                         'ASIC': ['AU'],
                                         'SEBI': ['IN'],
                                         'FMA': ['NZ'],
                                         'FSA': ['JP'],
                                        }
        

    def jurisdiction(self):
        """returns the 2 character JurisdictionCountryCode of the party, irrespective of language"""
        jurisdiction = None
        if self.party:
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2015.3:
                jurisdiction = self.party.JurisdictionCountryCode()
            if not jurisdiction:
                try:
                    jurisdiction = self.party.AdditionalInfo().JurisdictionCountryCode()
                except:#it means the JurisdictionCountryCode AdditionalInfo doesnt exist on the Party
                    FRegulatoryLogger.WARN(logger, "The JurisdictionCountryCode AdditionalInfo is not set on the Party")
                    iso_obj = ISO3166CountryCodeBase()
                    jurisdiction = iso_obj.country_code(self.party)
        else:
            FRegulatoryLogger.WARN(logger, "Kindly provide a valid Party to retrieve it's jurisdiction")
        return jurisdiction

    def swift_jurisdiction (self, customer_dic = {}):
        """returns group jurisdiction, like ESMA"""
        jurisdiction = self.jurisdiction()
        swift_jurisdiction = None
        if jurisdiction:
            if customer_dic:
                rever_customer_dic = FRegulatoryLibUtils.reverse_dict(customer_dic)
                if rever_customer_dic.has_key(jurisdiction):
                    swift_jurisdiction = rever_customer_dic[jurisdiction]
            if (not swift_jurisdiction) and self.default_jurisdiction_dic:
                reverse_default_dic = FRegulatoryLibUtils.reverse_dict(self.default_jurisdiction_dic)
                if reverse_default_dic.has_key(jurisdiction):
                    swift_jurisdiction = reverse_default_dic[jurisdiction]
        else:
            if self.party:
                FRegulatoryLogger.WARN(logger, "The jurisdiction is not present on the party <%s>. Hence, the swift code cannot be inferrred"%self.party.Name())
            else:
                FRegulatoryLogger.WARN(logger, "A valid party will have a jurisdiction")
        return swift_jurisdiction

    def MIC(self):
        """returns the MIC alias on the party"""
        mic_code = None
        if self.party:
            if self.party.Aliases(): 
                for alias in self.party.Aliases():
                    if alias.Type().Name() == 'MIC':
                        FRegulatoryLogger.DEBUG(logger, "MIC <%s> being picked from party alias MIC on party <%s>"%(alias.Name(), self.party.Name()))
                        mic_code = alias.Name()
        if not mic_code and self.party and self.party.Free1():
            FRegulatoryLogger.DEBUG(logger, "MIC being mapped from Free Text 1")
            mic_code = self.party.Free1()
        return mic_code

    def LEI(self):
        """returns the LEI of the party. If not present, then it traverses up the hierarchy to look for LEI"""
        lei = None
        if self.party:
            lei = FRegulatoryLibUtils.get_lei(self.party)
        return lei

    def subJurisdiction(self):
        """returns the subjuridiction on the basis of the country and the city details on the party"""
        iso_cc = ISO3166CountryCodeBase()
        return iso_cc.subJurisdiction(self.party.Country(), self.party.City())
    
    def ultimate_parent(self):
        """returns the top node of a Party hierarchy"""
        party = self.party
        while party.Parent():
            if party.Parent():
                party = party.Parent()
        if party != self.party:
            FRegulatoryLogger.DEBUG(logger, "The ultimate parent of party <%s> is: <%s>"%(self.party.Name(), party.Name()))
        else:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> is at the topmost node in the Party hierarchy"%(self.party.Name()))
        return party

    @classmethod
    def countryCodeFromMIC(self, mic_val):
        """return the country code of the party which has the given MIC value"""
        country_code = None
        party = FRegulatoryLibUtils.getPartyFromMIC(mic_val)
        if party:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> Found in ADS with MIC <%s>"%(party.Name(), mic_val))
            country_code_obj = ISO3166CountryCodeBase()
            country_code = country_code_obj.country_code(party)
        else:
            FRegulatoryLogger.INFO(logger, "No Party with MIC <%s> present in ADS"%(mic_val))
        return country_code

    @classmethod
    def partyFromLEI(self, lei_val):
        """return the party which has the given LEI value"""
        party = FRegulatoryLibUtils.getPartyFromLEI(lei_val)
        if party:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> found in ADS with LEI <%s>"%(party.Name(), lei_val))
        else:
            FRegulatoryLogger.INFO(logger, "No Party with LEI <%s> present in ADS"%(lei_val))
        return party

    @classmethod
    def partyFromMIC(self, mic_val):
        """return the party which has the given MIC value"""
        party = FRegulatoryLibUtils.getPartyFromMIC(mic_val)
        if party:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> Found in ADS with MIC <%s>"%(party.Name(), mic_val))
        else:
            FRegulatoryLogger.INFO(logger, "No Party with MIC <%s> present in ADS"%(mic_val))
        return party

    @classmethod
    def isValidLEI(self, lei_val):
        """verify that the given lei follows ISO7064 and that the last two digits are check digits"""
        return FRegulatoryLibUtils.isValidLEI(lei_val)

    @classmethod
    def generateLEIWithCheckSum(self, lei_val):
        """generate the checkSum for the given lei of 18 characters"""
        return FRegulatoryLibUtils.generateLEIWithCheckSum(lei_val)

class TaxonomyBase(object):
    def __init__(self, acm_object):
        self.trade = None
        self.instrument = None
        try:
            if acm_object and acm_object.IsKindOf('FTrade'):
                self.trade = acm_object
                self.trd_reg_info = self.trade.RegulatoryInfo()
            elif acm_object and acm_object.IsKindOf('FInstrument'):
                self.instrument = acm_object.Instrument()
                self.instr_reg_info = self.instrument.RegulatoryInfo()
            else:
                FRegulatoryLogger.WARN(logger, "Please provide the valid acm object either of FTrade or FInstrument type")
        except Exception, e:
            FRegulatoryLogger.ERROR(logger, "Please provide the valid acm object either of FTrade or FInstrument type")

    def cfi(self, cfi_code = None, generate = True):
        """generates and returns the CFI code for the instrument if not present on it. If already present on the instrument, it returns the existing CFICode"""
        if self.instrument:
            if cfi_code:
                self.instr_reg_info.CfiCode(cfi_code)
            else:
                cfi = self.instr_reg_info.CfiCode()
                if (not cfi) and generate:
                    cfi = FRegulatoryCfiCodeGeneration.compute_cfi_code(self.instrument) 
                return cfi
        elif self.trade:
            if (self.trade.Instrument().InsType() == 'Curr') or \
            (self.trade.Instrument().InsType() in ['Option', 'Future/Forward'] and self.trade.Instrument().Underlying().InsType() == 'Curr'):
                if cfi_code:
                    self.trd_reg_info.CfiCode(cfi_code)
                else:
                    cfi = self.trd_reg_info.CfiCode()
                    if (not cfi) and generate:
                        cfi = FRegulatoryCfiCodeGeneration.compute_cfi_code(self.trade) 
                    return cfi
            else:
                FRegulatoryLogger.ERROR(logger, "CfiCode for trades is available for FX trades only.")
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid instrument")

    def upi(self):
        """return or generate UPI"""
        upi = None
        if self.trade:
            upi = FRegulatoryLibUtils.upi(self.trade)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        return upi

class TradeRegInfoBase(object):
    def __init__(self, trade):
        """class that maintains all data related to the regulatory on the FTrade"""
        self.trade = trade
        pass
    
    def tech_record_identification(self):
        """function that returns the technical record identification if present on the trade. If not present, it generates and returns this value"""
        return FRegulatoryLibUtils.tech_record_identification(self.trade)

    def buyer(self):
        """returns the buyer on the deal. It is often the acquirer or the counterparty on the trade depending on the direction of the transaction"""
        buyer = None
        if self.trade:
            us_buyer = FRegulatoryLibUtils.us_buyer(self.trade)
            if us_buyer:
                buyer = FRegulatoryLibUtils.our_org(self.trade)#self.trade.RegulatoryInfo().OurOrg()
                if not buyer:
                    if self.trade.RegulatoryInfo().OurOrganisation():
                        buyer = self.trade.RegulatoryInfo().OurOrganisation()
                    else:
                        buyer = self.trade.Acquirer()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on buyer <%s> or its linked parent party."%buyer.Name())
            else:
                buyer = FRegulatoryLibUtils.their_org(self.trade)#self.trade.RegulatoryInfo().TheirOrg()
                if not buyer:
                    if self.trade.RegulatoryInfo().TheirOrganisation():
                        buyer = self.trade.RegulatoryInfo().TheirOrganisation()
                    else:
                        buyer = self.trade.Counterparty()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on buyer <%s> or its linked parent party."%buyer.Name())
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        return buyer
    
    def us_buyer(self):
        """returns True if we are the buyer of the trade"""
        return FRegulatoryLibUtils.us_buyer(self.trade)

    def us_seller(self):
        """returns True if we are the seller of the trade"""
        is_us_seller = False
        if not FRegulatoryLibUtils.us_buyer(self.trade):
            is_us_seller = True
        return is_us_seller
    
    def seller(self):
        """returns the seller on the deal It is often the acquirer or the counterparty on the trade depending on the direction of the transaction"""
        seller = None
        us_buyer = FRegulatoryLibUtils.us_buyer(self.trade)
        if self.trade:
            if us_buyer:
                seller = FRegulatoryLibUtils.their_org(self.trade)#self.trade.RegulatoryInfo().TheirOrg()
                if not seller:#it means the LEI is not present and hence was not found
                    if self.trade.RegulatoryInfo().TheirOrganisation():
                        seller = self.trade.RegulatoryInfo().TheirOrganisation()
                    else:
                        seller = self.trade.Counterparty()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on seller <%s> or its linked parent party."%seller.Name())
            else:
                seller = FRegulatoryLibUtils.our_org(self.trade)#self.trade.RegulatoryInfo().OurOrg()
                if not seller:
                    if self.trade.RegulatoryInfo().OurOrganisation():
                        seller = self.trade.RegulatoryInfo().OurOrganisation()
                    else:
                        seller = self.trade.Acquirer()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on seller <%s> or its linked parent party."%seller.Name())
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        
        return seller

    def is_increase(self):
        """return if the trade implies an increase or decrease of notional"""
        is_increase_decrease = None
        if self.trade and self.trade.Contract().Oid() != self.trade.Oid():
            trade_nominal = self.trade.Nominal()
            contract_nominal = self.trade.Contract().Nominal()
            if trade_nominal > contract_nominal:
                is_increase_decrease = 'INCR'
            elif trade_nominal < contract_nominal:
                is_increase_decrease = 'DECR'
        return is_increase_decrease
    
    def country_of_branch(self):
        """return country of the branch membership field"""
        country_of_branch = None
        branch_membership = None
        if self.trade:
            regulatory_info = self.trade.RegulatoryInfo()
            branch_membership = regulatory_info.BranchMembership()
            if branch_membership:
                country_of_branch = branch_membership.Country()
            else:
                FRegulatoryLogger.INFO(logger, "BranchMembership is not defined on trade <%d>"%self.trade.Oid())
        if branch_membership and not country_of_branch:
            FRegulatoryLogger.INFO(logger, "Country is not defined on party <%s> assigned as BranchMembership on trade <%d>"%(branch_membership.Name(), self.trade.Oid()))
        return country_of_branch
    
    def country_code_of_branch(self):
        """return country code of the branch membership field"""
        country_code_of_branch = None
        country_of_branch = self.country_of_branch()
        if not country_of_branch:
            FRegulatoryLogger.INFO(logger, "Country is not defined. Hence country code cannot be inferred.")
        else:
            iso_obj = ISO3166CountryCodeBase()
            country_code_of_branch = iso_obj.country_code_from_string(country_of_branch)
        return country_code_of_branch

    def complex_trade_component_id(self):
        """Generates and returns the complex trade component id on the trade (if not present), else it returns the regComplexTrdCmptId AddInfo value on the Trade"""
        complex_cmpt_id = None
        if self.trade:
            complex_cmpt_id = self.trade.AdditionalInfo().RegComplexTrdCmptId()
            if not complex_cmpt_id:
                complex_cmpt_id = FRegulatoryLibUtils.generate_complex_trade_comp_id(self.trade)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        return complex_cmpt_id
    
    def trading_capacity(self):
        """what role do we have in the deal, investor, broker, and so on"""
        trading_capacity = None
        if self.trade:
            trading_capacity = self.trade.RegulatoryInfo().TradingCapacity()
            if (not trading_capacity) or trading_capacity == 'None':
                trading_capacity = 'DEAL'
                reporting_entity = self.trade.RegulatoryInfo().ReportingEntity()
                if reporting_entity:
                    if self.trade.Acquirer():
                        if self.trade.Acquirer() != reporting_entity:
                            trading_capacity = 'AOTC'
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        return trading_capacity

    def cfi_code(self, set_cfi_code=False):
        """generates and returns the CFI code of the Trade (if not present), else it returns the CFI code on the Trade. This is applicable only in case of FX Trades"""
        cfi_code = None
        if self.trade:
            taxonomy = TaxonomyBase(self.trade)
            cfi_code = taxonomy.cfi(None, set_cfi_code)
        return cfi_code

    def notional_amount(self):
        """ Returns notional amount for trade"""
        return FRegulatoryNotionalAmount.FRegulatoryNotionalAmount(self.trade).notional_amount()

class PersonRegInfoBase(object):
    def __init__(self, person):
        self.contact = None
        self.person = None
        try:
            if person.IsKindOf(acm.FContact):
                self.contact = person
            elif FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and person.IsKindOf(acm.FPerson):
                self.person = person
        except:
            pass

    def national_id(self):
        """generate, and possibly store, the NationalId based on the CONCAT"""
        return self.concat()

    def concat(self):
        """generate the CONCAT national ID on the basis of the contact's first and last name and data of birth"""
        national_id = None
        reg_info = None
        partyReg = None
        if self.contact:
            reg_info = self.contact.RegulatoryInfo()
            partyReg = PartyRegInfoBase(self.contact.Party())
        elif self.person:
            reg_info = self.person
            if self.person.Contacts():
                partyReg = PartyRegInfoBase(self.person.Contacts()[0].Party())
        if reg_info:
            national_id = reg_info.NationalId()
            if not national_id:
                first_name = ''
                last_name = ''
                date_of_birth = ''
                if reg_info.FirstName():
                    first_name = (reg_info.FirstName() + '#####')[0:5]
                if reg_info.LastName():
                    last_name = (reg_info.LastName() + '#####')[0:5]
                if reg_info.DateOfBirth():
                    try:
                        date_of_birth = ''.join(ael.date_from_string(reg_info.DateOfBirth()).to_string(ael.DATE_ISO).split('-'))
                    except Exception, e:
                        FRegulatoryLogger.ERROR(logger, "Error while getting the date of birth from Person. Error: <%s>"%str(e)) 
                
                national_id = date_of_birth + first_name.upper() + last_name.upper()
                if partyReg.jurisdiction():
                    national_id = partyReg.jurisdiction() + national_id
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid contact/person")
        return national_id

class UniqueTradeIdentifierBase(object):
    uti_installation = None
    uti_system = None
    uti_category = None
    uti_user_check_sum = None
    def __init__(self, acm_trade, installation='Prod', system='FrontArena', utiCategory="E02", useChecksum=True):
        # Store installation, system, utiCtegory and useChecksum
        # Store them statically since they should be initialized at "Organization" level
        UniqueTradeIdentifierBase.uti_installation = installation
        UniqueTradeIdentifierBase.uti_system = system
        UniqueTradeIdentifierBase.uti_category = utiCategory
        UniqueTradeIdentifierBase.uti_user_check_sum = useChecksum

    def check_sum(self, utiVal):
        """generate check sum for a UTI"""
        return FRegulatoryLibUtils.check_sum(utiVal)

    def generateUTI(self, trade, uti_category=None, uti_system=None, uti_installation=None):
        """generate a UTI, with a bank-defined, structure, to be used across the bank"""
        uti = None
        if uti_category:
            UniqueTradeIdentifierBase.uti_category = uti_category
        if uti_system:
            UniqueTradeIdentifierBase.uti_system = uti_system
        if uti_installation:
            UniqueTradeIdentifierBase.uti_installation = uti_installation
        our_org = FRegulatoryLibUtils.our_org(trade)#trade.RegulatoryInfo().OurOrg()
        lei = None
        if our_org:
            lei = our_org.LegalEntityId()
        if not lei:
            FRegulatoryLogger.ERROR(logger,
                                    "UniqueTradeIdentifier cannot be generated for trade <%d> as either the OurOrganisation or the Acquirer are not set or they do not have a valid LEI." % trade.Oid())
        else:
            uti = UniqueTradeIdentifierBase.uti_category.upper() + lei + UniqueTradeIdentifierBase.uti_system.upper() + UniqueTradeIdentifierBase.uti_installation.upper() + str(
                trade.Oid())
            uti = self.check_sum(uti)
        return uti

    def uti(self, trade, generateIfNotExists=False):
        """Generates and returns the UTI for the trade if not present on it. If already present on the trade, it returns the existing UTI"""
        uti = None
        if trade:
            uti = FRegulatoryLibUtils.get_uti_from_trade_attribute(trade)
            if not uti:
                uti = FRegulatoryLibUtils.get_uti_from_trade_alais(trade)
            if not uti:
                uti = FRegulatoryLibUtils.get_uti_from_trade_addinfo(trade)
            try:
                if (not uti) and acm.FTradeAdditionalInfo.GetMethod('UTI1_Part', 0):
                    uti = trade.AdditionalInfo().UTI1_Part() + trade.AdditionalInfo().UTI2_Part()
            except:
                FRegulatoryLogger.INFO(logger, "The UTI1_Part and UTI2_Part AdditionalInfoSpecs are not present on the Trade")
            if (not uti) and generateIfNotExists:
                uti = self.generateUTI(trade, UniqueTradeIdentifierBase.uti_category, UniqueTradeIdentifierBase.uti_system, UniqueTradeIdentifierBase.uti_installation)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        return uti    

    def is_correct_check_sum(self, uti_val):
        """validate the check sum"""
        b_correct_check_sum = None
        if uti_val:
            b_correct_check_sum = FRegulatoryLibUtils.is_valid_check_sum(uti_val)
        else:
            FRegulatoryLogger.INFO(logger, "Please provide a UTI value to verify checksum")
        return b_correct_check_sum

    def trade_UTI_has_correct_check_sum(self, trade):
        """validate the check sum of a UTI"""
        uti_val = self.uti(trade)
        b_correct_check_sum = False
        if uti_val:
            b_correct_check_sum = FRegulatoryLibUtils.is_valid_check_sum(uti_val)
        else:
            FRegulatoryLogger.INFO(logger, "Trade <%d> does not have UTI on it"%trade.Oid())
        return b_correct_check_sum

    def have_we_generated_UTI(self, trade):
        """was this UTI generated by the bank, or imported"""
        b_generated_uti = False
        if self.uti(trade) == self.generateUTI(trade):
            b_generated_uti = True
        return b_generated_uti
