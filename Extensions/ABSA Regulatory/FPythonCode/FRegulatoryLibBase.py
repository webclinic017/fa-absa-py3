"""------------------------------------------------------------------------
MODULE
    FRegulatoryLibBase -
DESCRIPTION:
    This file consists of the default implementation of the API open to customizations to users
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import acm
import FRegulatoryCfiCodeGeneration
import FRegulatoryLogger
import ael
import operator
import FRegulatoryLibUtils
try:
    import __builtin__
except:
    import builtins
logger = 'FRegulatoryLibBase'
import FRegulatoryLookup
import FInstrumentClassification
import FRegulatoryNotionalAmount
import datetime
import unicodedata
import FRegulatoryISITCode
config_param = None
try:
    import FRegulatoryConfigParam
    config_param = FRegulatoryConfigParam.FRegulatoryConfigParam()
except:
    pass
space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

stage1 = (ael.date('2018-03-01'), ael.date('2019-05-15'))
stage2 = (ael.date('2019-05-16'), ael.date('2020-05-15'))
stage3 = (ael.date('2020-05-16'), ael.date('2021-05-15'))
stage4 = (ael.date('2021-05-16'),)


class InstrumentRegInfoBase(object):
    """This file consists of the support functions that are used to populate the ADM.InstrumentRegulatoryInfo. supplying logic and enabling Storage"""
    ext_fin_ins_identification_type_code = {'BLOM' : 'BB_TICKER', 'FIGI' : 'FIGI', \
                        'CUSP' : 'CUSIP', 'RCMD' : 'RED_CODE', 'RICC' : 'RIC', \
                        'SEDL' : 'SEDOL', 'VALO' : 'VALOREN', 'WKNR' : 'WKN'}
    countrycode_identifier = {'GB' : 'SEDOL', 'US' : 'CUSIP', 'NT': 'SEDOL'}

    def __init__(self, instrument=None):
        """class that maintains all data related to the regulatory on the FTrade"""
        self.instrument = None
        self.current_date = ael.date_today()
        if instrument:
            self.instrument = instrument
            self.reg_info = self.instrument.RegulatoryInfo()
        self.parent_list = []

    def mifid2_rts28_instype(self, instrument=None):
        """get the instype for rts28 as per mifid classification"""
        mifid2_rts28_type = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            mifid2_rts28_type = FRegulatoryLibUtils.get_rts28(instrument)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its MiFID-II RTS28 InsType")
        return mifid2_rts28_type

    def mifid2_rts2_instype(self, instrument=None):
        """get the instype for rts2 as per mifid classification"""
        mifid2_rts2_type = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            self.__rts2_classify = FInstrumentClassification.FInstrumentClassification(instrument)
            mifid2_rts2_type = self.__rts2_classify.mifid2_rts2_instype()
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its MiFID-II RTS2 InsType")
        return mifid2_rts2_type

    def mifid2_rts2_inssubtype(self, instrument=None):
        """get the inssubtype for rts2 as per mifid classification"""
        mifid2_rts2_subtype = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            self.__rts2_classify = FInstrumentClassification.FInstrumentClassification(instrument)
            mifid2_rts2_subtype = self.__rts2_classify.mifid2_rts2_inssubtype()
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its MiFID-II RTS2 InsSubType")
        return mifid2_rts2_subtype

    def __get_instrument(self, instrument=None):
        ins = self.instrument
        if instrument and instrument.IsKindOf(acm.FInstrument):
            ins = instrument
        return ins

    def Isin(self, instrument=None):
        """returns the ISIN of the instrument"""
        isin = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            isin = instrument.Isin()
            if not isin:
                FRegulatoryLogger.INFO(logger, "Instrument <%s> has no Isin on it." % instrument.Name())
                isin = FRegulatoryLibUtils.get_isin_from_similar_isin(instrument)
                if isin:
                    FRegulatoryLogger.INFO(logger, "Instrument <%s> has no Isin on it. The SimilarIsin <%s> is being identified as the Isin of the instrument" % (instrument.Name(), isin))
            if not isin:
                isin = FRegulatoryLibUtils.get_isin_from_alias(instrument)  # check if there is an instrument Alias of the name ISIN
            if not isin:
                isin = FRegulatoryLibUtils.get_isin_from_addinfo(instrument)  # check if there is an instrument AdditionalInfo of the name ISIN
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its Isin")
        return isin

    def cfi_code(self, instrument=None, set_cfi_code=False):
        """generates and returns the CFI code of the instrument (if not present), else it returns the CFI code on the instrument"""
        cfi_code = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            taxonomy = TaxonomyBase(instrument)
            cfi_code = taxonomy.cfi(None, None, set_cfi_code)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its CfiCode")
        return cfi_code

    def isValidIsin(self, instrument=None, isin_val=None):
        """verify that the given Isin has a valid ISIN structure and checksum correct"""
        is_valid_isin = False
        if isin_val:
            is_valid_isin = FRegulatoryLibUtils.isValidIsin(isin_val)
        else:
            ins = self.__get_instrument(instrument)
            isin = self.Isin(ins)
            is_valid_isin = FRegulatoryLibUtils.isValidIsin(isin)
        return is_valid_isin

    @classmethod
    def get_large_in_scale(cls, average_daily_transactions, exchange_rate):
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

    def isLiquid(self, instrument=None):
        """Indicates if the security is liquid, as defined by the Committee of European Securities Regulators (CESR) under the Markets in Financial Instruments Directive (MiFID)."""
        instrument = self.__get_instrument(instrument)
        if not instrument:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its isLiquid")
            return None
        isliquid_status = False
        if self.current_date < ael.date("2018-02-16"):
            FRegulatoryLogger.WARN(logger, "Not supported before 16 Feb 2018")
            return None
        global space
        space.Clear()
        from_currency = instrument.Currency()
        to_currency = acm.FCurrency['EUR']
        unshifted_val = from_currency.Calculation().FXRate(space, to_currency)
        total_issued_euro = int(instrument.TotalIssued() * unshifted_val.Number())
        self.rts2_classify = FRegulatoryLookup.RTS2Classification(instrument, self.current_date)
        total_nominal_value, businessdays, dates = self.rts2_classify.get_total_nominal_value()
        dates, average_daily_trades, percentage_days_traded, first_trade_ind = self.rts2_classify.get_average_daily_trades(
            businessdays, dates)
        try:
            if (not len(instrument.Trades())) or first_trade_ind or (
                            ael.date(str(instrument.IssueDay())) <= dates[0] and ael.date(
                        str(instrument.IssueDay()))) >= dates[1]:
                if instrument.InsType() == "Bond":
                    if instrument.SeniorityChlItem() and instrument.SeniorityChlItem().Name() == "SNRFOR":
                        if ((total_issued_euro >= 1000000000 and stage1[0] <= self.current_date and stage2[
                            1] >= self.current_date) or (total_issued_euro >= 500000000 and stage3[0] <= self.current_date)):
                            isliquid_status = True
                    elif instrument.ValuationGrpChlItem() and instrument.ValuationGrpChlItem().Name() == "Government":
                        if total_issued_euro >= 1000000000:
                            isliquid_status = True
                    elif instrument.CategoryChlItem() and instrument.CategoryChlItem().Name() == "Municipal":
                        if total_issued_euro >= 500000000:
                            isliquid_status = True
                    elif instrument.CategoryChlItem() and instrument.CategoryChlItem().Name() == "Corporate":
                        if ((total_issued_euro >= 1000000000 and stage1[0] <= ael.date_today() and stage2[
                            1] >= ael.date_today()) or (
                                        total_issued_euro >= 500000000 and stage3[0] <= ael.date_today())):
                            isliquid_status = True
                    else:
                        isliquid_status = False
                elif instrument.InsType() == "Convertible":
                    if total_issued_euro >= 500000000:
                        isliquid_status = True
                else:
                    FRegulatoryLogger.WARN(logger, "This function <isLiquid> is applicable only for Bond instruments")
                    isliquid_status = None
            else:
                if instrument.InsType() in ["Bond", "Convertible"]:
                    if total_nominal_value * unshifted_val.Number() > 100000 and percentage_days_traded >= 80:
                        if stage1[0] <= self.current_date and stage1[1] >= self.current_date and average_daily_trades >= 15:
                            isliquid_status = True
                        elif stage2[0] <= self.current_date and stage2[1] >= self.current_date and average_daily_trades >= 10:
                            isliquid_status = True
                        elif stage3[0] <= self.current_date and stage3[1] >= self.current_date and average_daily_trades >= 7:
                            isliquid_status = True
                        elif stage4[0] <= self.current_date and average_daily_trades >= 2:
                            isliquid_status = True
        except Exception as e:
            FRegulatoryLogger.WARN(logger, "Insufficient information to determine liquid status.")
        return isliquid_status

    def get_liquidity_band(self, instrument=None, compute=True):
        """get the LiquidityBand for the given instrument on the basis of the average daily turnover"""
        instrument = self.__get_instrument(instrument)
        liquidity_band = None
        if instrument:
            reg_info = instrument.RegulatoryInfo()
            if acm.FAdditionalInfoSpec['regLiquidityBand']:
                liquidity_band = reg_info.AdditionalInfo().RegLiquidityBand()
            if str(liquidity_band) == 'None' and compute:
                average_daily_turnover = reg_info.AverageDailyTurnover()
                if average_daily_turnover:
                    liquidity_band = 0
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
                        liquidity_band = 6  # more than 9000 transactions per day
                else:
                    FRegulatoryLogger.INFO(logger, "The LiquidityBand cannot be inferred as the averageDailyTurnOver is not present on the instrument.")
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its get_liquidity_band")
        return liquidity_band

    def is_equity_like(self, instrument=None):
        """returns True if the instrument is an equity/equity like instrument"""
        equity_like = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            equity_like = False
            ins_type = instrument.InsType()
            if not self.mifid2_rts2_instype(instrument):
                if ins_type in ['Stock', 'ETF', 'Depositary_Receipt']:
                    return True
                elif ins_type in ['Combination']:
                    for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                        if InstrumentRegInfoBase(cons.Instrument()).is_equity_like():
                            equity_like = True
                        else:
                            equity_like = False
                            break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_equity_like")
        return equity_like

    def is_equity(self, instrument=None):
        """returns True or False based on if the Instrument is of Equity type"""
        instrument = self.__get_instrument(instrument)
        is_equity = None
        if instrument:
            is_equity = False
            ins_type = instrument.InsType()
            if ins_type in ['Stock', 'Depositary_Receipt', 'Certificate', 'Warrant']:
                is_equity = True
            elif ins_type in ['Combination']:
                for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_equity():
                        is_equity = True
                    else:
                        is_equity = False
                        break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_equity")
        return is_equity

    def is_bond_like(self, instrument=None):
        """returns True if the instrument is an bond/bond like instrument"""
        instrument = self.__get_instrument(instrument)
        bond_like = None
        if instrument:
            bond_like = False
            if self.mifid2_rts2_instype(instrument) == 'Bonds':
                bond_like = True
            elif instrument.InsType() in ['Combination']:
                for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_bond_like(instrument):
                        bond_like = True
                    else:
                        bond_like = False
                        break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_bond_like")
        return bond_like

    def is_interest_rate_derivative(self, instrument=None):
        """returns True if the instrument is an interest rate derivative instrument"""
        instrument = self.__get_instrument(instrument)
        ir_derivative = None
        if instrument:
            ir_derivative = False
            if self.mifid2_rts2_instype(instrument) == 'Interest Rate Derivatives':
                ir_derivative = True
            elif instrument.InsType() in ['Combination']:
                for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_interest_rate_derivative(instrument):
                        ir_derivative = True
                    else:
                        ir_derivative = False
                        break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_interest_rate_derivative")
        return ir_derivative
        
    def is_equity_derivative(self, instrument=None):
        """returns True if the instrument is an equity derivative instrument"""
        instrument = self.__get_instrument(instrument)
        equity_derivative = None
        if instrument:
            equity_derivative = False
            ins_type = instrument.InsType()
            if self.mifid2_rts2_instype(instrument) == 'Equity Derivatives':
                equity_derivative = True
            elif ins_type in ['Dividend_Point_Index', 'EquityIndex']:
                equity_derivative = True
            elif ins_type in ['Combination']:
                for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_equity_derivative(instrument):
                        equity_derivative = True
                    else:
                        equity_derivative = False
                        break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_equity_derivative")
        return equity_derivative

    def is_c10_derivative(self, instrument=None):
        """returns True if the instrument is a C10 derivative instrument"""
        c10_derivative = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            c10_derivative = False
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_c10_derivative")
        return c10_derivative

    def is_fx_derivative(self, instrument=None):
        """returns True if the instrument is a FX derivative instrument"""
        fx_derivative = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            fx_derivative = False
            if self.mifid2_rts2_instype(instrument) == 'Foreign Exchange Derivatives':
                fx_derivative = True
            elif instrument.InsType() in ['Combination']:
                for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_fx_derivative(instrument):
                        fx_derivative = True
                    else:
                        fx_derivative = False
                        break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_fx_derivative")
        return fx_derivative

    def is_cfd(self, instrument=None):
        """returns True if the instrument is a cfd instrument"""
        cfd = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            cfd = False
            if self.mifid2_rts2_instype(instrument) == 'Financial contracts for differences':
                cfd = True
            elif instrument.InsType() in ['Combination']:
                for cons in instrument.Constituents(acm.Time.DateFromYMD(1970, 1, 1)):
                    if InstrumentRegInfoBase(cons.Instrument()).is_cfd():
                        cfd = True
                    else:
                        cfd = False
                        break
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_cfd")
        return cfd

    @classmethod
    def get_conversion_factor(cls, currency1, currency2):
        """return the conversion factor between the two currencies provided"""
        conversion_factor = 0
        curr_pair = acm.FCurrencyPair.Select01("currency1 = '%s' and currency2 = '%s'" % (currency1, currency2), None)
        if not curr_pair:
            curr_pair = acm.FCurrencyPair.Select01("currency1 = '%s' and currency2 = '%s'" % (currency2, currency1), None)
            if curr_pair:
                conversion_factor = curr_pair.PointValueInverse()
        else:
            conversion_factor = curr_pair.PointValue()
        return conversion_factor, curr_pair

    def is_basket_cds(self, instrument=None):
        """returns True if the instrument is a basket CDS"""
        instrument = self.__get_instrument(instrument)
        basket_cds = None
        if instrument:
            basket_cds = False
            for leg in instrument.Legs():
                if leg.LegType() == 'Credit Default' and leg.CreditRef().InsType() == 'Combination':
                    basket_cds = True
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_basket_cds")
        return basket_cds

    def is_commodity_derivative(self, instrument=None):
        """returns True if the instrument is a commodity derivative"""
        commodity_classification = ['Commodity Index', 'Commodity Variant', 'Commodity', 'Average Future/Forward', 'Precious Metal Rate', 'Rolling Schedule', 'PriceSwap', 'PriceIndex']
        is_cmdty_derivative = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            is_cmdty_derivative = False
            if instrument.InsType() in commodity_classification or \
                            instrument.Underlying() and instrument.Underlying().InsType() in commodity_classification:
                is_cmdty_derivative = True
            if (not is_cmdty_derivative) and instrument.Underlying() and instrument.Underlying().InsType() == 'Combination':
                cmdty_counter = 0
                other_counter = 0
                for ins_map in instrument.Underlying().InstrumentMaps():
                    if ins_map.Instrument().InsType() in commodity_classification:
                        cmdty_counter = cmdty_counter + 1
                    else:
                        other_counter = other_counter + 1
                    if cmdty_counter > 0 and other_counter == 0:
                        is_cmdty_derivative = True
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_commodity_derivative")
        return is_cmdty_derivative

    def ISITC_type_code(self, instrument=None):
        """returns the ISITC Type code classification for the instrument"""
        isitic_code = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            isitic_code_obj = FRegulatoryISITCode.ISITCodeType(instrument)
            isitic_code = isitic_code_obj.get_isitic_classification()
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its ISITC_type_code")
        return isitic_code
    
    @classmethod
    def get_instrument_alias_type(cls, country_code):
        """get the instrument alias type that needs to be referred to for the given country code"""
        alias_type = None       
        if country_code in cls.countrycode_identifier.keys():
            alias_type = cls.countrycode_identifier[country_code]
        else:
            FRegulatoryLogger.WARN(logger, "The countrycode_identifier dictionary does not have the country code <%s> provided." % country_code)
        return alias_type
    
    @classmethod
    def get_identifier_from_external_fin_ins_identification_type_code(cls, identification_type_code):
        """get the identifier from the external finanicial instrument identification type code"""
        identifier_type = None
        if identification_type_code in cls.ext_fin_ins_identification_type_code:
            identifier_type = cls.ext_fin_ins_identification_type_code[identification_type_code]
        else:
            FRegulatoryLogger.WARN(logger, "External Financial Instrument Identification type code <%s> is not present in dict ext_fin_ins_identification_type_code" % identification_type_code)
        return identifier_type
        
    @classmethod
    def get_instrument_from_external_fin_ins_identification_type_code(cls, identification_type_code, identifier_value):
        """get the instrument with the provided identifier value from the external finanicial instrument identification type code"""
        identifier_type = cls.get_identifier_from_external_fin_ins_identification_type_code(identification_type_code)
        instruments = None
        if identifier_type:
            instruments = cls.get_instruments(identifier_type, identifier_value)
        return instruments
    
    @classmethod
    def get_instrument_from_alias(cls, identifier_type, identifier_value):
        """get the instrument for the given alias type and value"""
        instrument = None
        alias = None
        alias_type = acm.FInstrAliasType[identifier_type]
        if alias_type:
            query = "type=%d and alias=%s" % (alias_type.Oid(), str(identifier_value))
            alias = acm.FInstrumentAlias.Select01(query, None)
        else:
            FRegulatoryLogger.WARN(logger, "AliasType <%s> does not exist in ADS" % (identifier_type))   
        if alias:
            instrument = alias.Instrument()
        return instrument

    @classmethod
    def get_instruments_from_similar_isin(cls, isin_val):
        """get the instruments with similar isin value as that of the value provided"""
        instruments = []
        add_info_spec = acm.FAdditionalInfoSpec['regSimilarIsin']
        if add_info_spec:
            addinfos = acm.FAdditionalInfo.Select("addInf=%d and fieldValue = '%s'" % (add_info_spec.Oid(), isin_val))

            for addinfo in addinfos:
                if addinfo.RecType() == 'InstrRegulatoryInfo':
                    instruments.append(addinfo.Parent().Instrument())
                elif addinfo.RecType() == 'Instrument':
                    instruments.append(addinfo.Parent())
                elif addinfo.RecType() in ['TradeRegulatoryInfo', 'Trade']:
                    FRegulatoryLogger.WARN(logger, "AddInfo <%s> is linked to <%s>. This is applicable only in case of FXSwaps. Instrument for these deals being currency. Hence, not considering the currency instrument." % (add_info_spec, addinfo.RecType()))
        return instruments
    
    @classmethod
    def get_instruments_from_isin(cls, isin_value):
        """get instruments with the isin value provided - either in the ISIN field of the instrument or on its SimilarIsin field"""
        instruments = []
        instrument = acm.FInstrument.Select01("isin = '%s'" % isin_value, None)
        if instrument:
            instruments.append(instrument)
        sim_isin_ins = cls.get_instruments_from_similar_isin(isin_value)
        if sim_isin_ins:
            instruments.extend(sim_isin_ins)
        return instruments

    @classmethod
    def get_instruments(cls, identifier_type, identifier_value):
        """get instruments with the provided identifier value in the alias of the provided identifer type"""
        instruments = []
        if identifier_type.upper() == 'ISIN':
            FRegulatoryLogger.WARN(logger, "getting the instruments for the given isin", identifier_value)
            instruments = cls.get_instruments_from_isin(identifier_value)
        # elif identifier_type.upper() in ['SEDOL', 'CUSIP', 'BB_TICKER', 'FIGI', 'RIC', 'RED_CODE', 'VALOREN', 'WKN', 'BB_UNIQUE']:
        else:  # the condition is generic to also allow instrument alias of proprietary types
            instrument = cls.get_instrument_from_alias(identifier_type, identifier_value)
            if instrument:
                instruments.append(instrument)
        return instruments
    
    @classmethod
    def getInstrumentFromNationalInstrumentIdentifierScheme(cls, identifier_value, identifier_type=None, country_code=None, ext_fin_type_code=None, proprietary=None):
        """get instruments from the provided national instrument identifier scheme"""
        instruments = None
        process_further = True
        country_code_identifier = None
        ext_fin_type_identifier = None
        if country_code:
            country_code_identifier = cls.get_instrument_alias_type(country_code)         
        if ext_fin_type_code:
            ext_fin_type_identifier = cls.get_identifier_from_external_fin_ins_identification_type_code(ext_fin_type_code)
        if identifier_type:
            if identifier_type and identifier_type == 'TS':
                identifier_type = 'BB_TICKER'
            if country_code and country_code_identifier != identifier_type:
                FRegulatoryLogger.WARN(logger, "The country code infers to <%s>. Whereas the Identifier type provided is <%s>. Cannot process this further." % (country_code_identifier, identifier_type))
                process_further = False
            if ext_fin_type_code and ext_fin_type_identifier != identifier_type:
                FRegulatoryLogger.WARN(logger, "External Financial Instrument Identification type code value infers to <%s>. Whereas the Identifier type provided is <%s>. Cannot process this further." % (ext_fin_type_identifier, identifier_type))
                process_further = False
        else:
            if (not country_code) and (not ext_fin_type_code):
                identifier_type = 'ISIN'  # defaulting the identifier_type to ISIN when no other value is provided.
            if proprietary:
                identifier_type = 'PROPRIETARY'
        if process_further:
            if identifier_type:
                instruments = cls.get_instruments(identifier_type, identifier_value)
            elif country_code:               
                instruments = cls.get_instruments(country_code_identifier, identifier_value)
            elif ext_fin_type_code:
                instruments = cls.get_instrument_from_external_fin_ins_identification_type_code(ext_fin_type_code, identifier_value)
        return instruments

    def __get_issuer_country(self, party):
        country_of_issuer = None
        if party.RiskCountry():
            country_of_issuer = party.RiskCountry()
            if country_of_issuer:
                country_of_issuer = country_of_issuer.Name()
        elif party.Country():
            country_of_issuer = party.Country()
        return country_of_issuer

    def country_of_issue(self, instrument=None):
        """returns the value of the country of risk on the issuer"""
        country_of_issuer_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            party = instrument.Issuer()
            if party:
                original_party = party
                self.parent_list = []
                country_of_issuer_val = self.__get_issuer_country(party)
                if not country_of_issuer_val:
                    while party.Parent() and not country_of_issuer_val:
                        if party.Parent().Name() not in self.parent_list:
                            party = party.Parent()
                            country_of_issuer_val = self.__get_issuer_country(party)
                            self.parent_list.append(party.Parent().Name())
                        else:
                            FRegulatoryLogger.ERROR(logger, "Cannot get country of issuer for party <%s> as there is a setup issue with cyclic dependency while configuring party parent."%original_party.Name())
                            break                           
            else:
                FRegulatoryLogger.WARN(logger, "Cannot infer the country of issue as the instrument <%s> does not have an issuer set on it."%instrument.Name()) 
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its country_of_issue")
        return country_of_issuer_val

    def country_code(self, instrument=None):
        """returns the value of the country_code of the issuer party"""
        instrument = self.__get_instrument(instrument)
        country_code_val = None
        if instrument:
            country_of_issue_val = self.country_of_issue(instrument)
            if country_of_issue_val:
                country_code_val = ISO3166CountryCodeBase().country_code_from_string(country_of_issue_val)
            else:
                FRegulatoryLogger.WARN(logger, "Cannot infer country code for instrument <%s> as the issuer's country is not set."%instrument.Name())
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its country_code")
        return country_code_val    

    def bbg_collateral_type(self, instrument=None):
        """returns collateral type of the instrument available from DataLoader"""
        collateral_type_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                collateral_type_val = instrument.GetProviderDataFieldValue('COLLAT_TYP')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its bbg_collateral_type")
        return collateral_type_val

    def is_jurisdiction(self, jurisdiction, instrument=None, jurisdiction_lookup = None):
        """return True if the Issuer of the instrument falls within the given jurisdiction, else return False"""
        is_jurisdiction_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if instrument.Issuer():
                is_jurisdiction_val = FRegulatoryLibUtils.is_party_in_jurisdiction(instrument.Issuer(), jurisdiction, jurisdiction_lookup)
            else:
                FRegulatoryLogger.WARN(logger,\
                    "IsJurisdiction cannot be inferred for instrument <%s> as Issuer is not set on it"\
                    %instrument.Name())
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_jurisdiction")
        return FRegulatoryLibUtils.get_tristate_choiceList(is_jurisdiction_val)

    def is_regulatory_authority(self, regulatory_authority, instrument=None, regulatory_authority_lookup = None):
        """return True if the Issuer of the instrument is governed by the given regulatory authority, else return False"""
        regulatory_authority_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if instrument.Issuer():
                regulatory_authority_val = FRegulatoryLibUtils.is_party_in_regulatory_authority(instrument.Issuer(), regulatory_authority, regulatory_authority_lookup)
            else:
                FRegulatoryLogger.WARN(logger,\
                    "IsRegulatoryAuthority cannot be inferred for instrument <%s> as Issuer is not set on it"\
                    %instrument.Name()) 
            return FRegulatoryLibUtils.get_tristate_choiceList(regulatory_authority_val)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_regulatory_authority")
        
    def bond_type(self, instrument=None):
        """retuns bond type of the instrument inferred from the Provider data available from DataLoader"""
        bond_type_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                collat_typ = instrument.GetProviderDataFieldValue('COLLAT_TYP')
                is_covered = instrument.GetProviderDataFieldValue('IS_COVERED')
                industry_sector = instrument.GetProviderDataFieldValue('INDUSTRY_SECTOR')
                security_typ2 = instrument.GetProviderDataFieldValue('SECURITY_TYP2')
                bullet = instrument.GetProviderDataFieldValue('BULLET')
                security_typ = instrument.GetProviderDataFieldValue('SECURITY_TYP')
                inflation_linked_indicator = instrument.GetProviderDataFieldValue('INFLATION_LINKED_INDICATOR')
                catastrophe = instrument.GetProviderDataFieldValue('CATASTROPHE')
                market_sector_des = instrument.GetProviderDataFieldValue('MARKET_SECTOR_DES')
                if collat_typ:
                    if collat_typ == "JUMBO PFANDBRIEF":
                        bond_type_val = 'Jumbo Pfandbrief';
                    elif collat_typ == "PFANDBRIEFE" :
                        bond_type_val = 'Pfandbrief'
                    elif collat_typ in ["ASSET BACKED", "COLLATERAL TRUST"]:
                        bond_type_val = 'ABS'
                    elif collat_typ in ["1ST MORTGAGE", "MORTGAGE", "MORTGAGE BACKED", "1ST REF MORTGAGE"]:
                        bond_type_val = 'MBS'
                    elif collat_typ == 'BILLS' and bullet and bullet == 'Y':
                        bond_type_val = 'Bill'
                if (not bond_type_val) and is_covered and is_covered == "Y":
                    bond_type_val = 'Covered Bond'
                if (not bond_type_val) and industry_sector and security_typ2:
                    if industry_sector == "Mortgage Securities":
                        if security_typ2 == "Pool":
                            bond_type_val = 'Pool'
                        elif security_typ2 == "CMO":
                            bond_type_val = 'CMO'
                        elif security_typ2 == "Whole Loan":
                            bond_type_val = 'Whole Loan'
                    elif industry_sector == 'Asset Backed Securities':
                        bond_type_val = 'ABS'
                if (not bond_type_val) and security_typ and security_typ2:
                    if security_typ == "US GOVERNMENT":
                        if security_typ2 == 'Bill':
                            bond_type_val = 'TBill'
                        if security_typ2 == 'Bond':
                            bond_type_val = 'TBond'
                        if security_typ2 == 'Note':
                            bond_type_val = 'TNote'
                if (not bond_type_val) and security_typ2 and security_typ2 == 'CP':
                    bond_type_val = 'Commercial Paper'
                if (not bond_type_val) and security_typ:
                    if security_typ == 'Agncy CMO IO':  # INTEREST_ONLY
                        bond_type_val = 'Interest Only (PO) Strips'
                    if security_typ == 'Agncy CMO PO':  # PRINCIPAL_ONLY
                        bond_type_val = 'Principal Only (IO) Strips'
                if (not bond_type_val) and bullet:
                    if bullet == 'Y':
                        bond_type_val = 'Bullet'
                    elif bullet == 'N':
                        bond_type_val = 'Non Bullet'
                if (not bond_type_val) and inflation_linked_indicator and inflation_linked_indicator == "Y":
                    bond_type_val = 'TIPS'  # this need to be checked
                if (not bond_type_val) and catastrophe and catastrophe == 'Y':
                    bond_type_val = 'CAT'
                if (not bond_type_val) and market_sector_des and market_sector_des == 'Equity':
                    bond_type_val = ''
                else:
                    bond_type_val = 'Other Bond'
            if bond_type_val:
                bond_type_val = FRegulatoryLibUtils.BondTypeEnum().number(bond_type_val)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its bond_type")      
        return bond_type_val

    def is_government_guaranteed(self, instrument=None):
        """returns True if it is a government guaranteed bond else False"""
        is_govt_guaranteed = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                market_sector_des = instrument.GetProviderDataFieldValue('MARKET_SECTOR_DES')
                if market_sector_des:
                    if 'GOVT' in market_sector_des.upper() or\
                        'MUNI' in market_sector_des.upper() or\
                        'CORP' in market_sector_des.upper():
                        is_govt_guaranteed = True
                    else:
                        is_govt_guaranteed = False
            return FRegulatoryLibUtils.get_tristate_choiceList(is_govt_guaranteed)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_government_guaranteed")

    def is_covered(self, instrument=None):
        """returns True if it is a covered instrument and False if it is not.
        If this value is not present on the instrument, it returns None"""
        instrument = self.__get_instrument(instrument)
        if instrument:
            is_covered = None
            if FRegulatoryLibUtils.get_provider_data_exists():
                is_covered = instrument.GetProviderDataFieldValue('IS_COVERED')
                if is_covered == 'Y':
                    is_covered = True
                elif is_covered == 'N':
                    is_covered = False
            return FRegulatoryLibUtils.get_tristate_choiceList(is_covered)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its is_covered")

    def fund_type(self, instrument=None):
        """returns the type of fund"""
        fund_type_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                fund_type_val = instrument.GetProviderDataFieldValue('FUND_TYP')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its fund_type")
        return fund_type_val 

    def main_trading_place(self, instrument=None):
        """returns the main trading place that this instrument is traded at"""
        main_trd_place = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            isin = self.Isin(instrument)
            if isin:
                if isin.startswith('XS'):
                    main_trd_place = 'ALL'
                elif isin.startswith('EU'):
                    main_trd_place = 'EB'
            if not main_trd_place:
                if FRegulatoryLibUtils.get_provider_data_exists():
                    main_trd_place = instrument.GetProviderDataFieldValue('EQY_PRIM_SECURITY_COMP_EXCH')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its main_trading_place")
        return main_trd_place

    def sftr_security_type(self, instrument=None):
        """returns the SFTR classification for the selected security if present in database"""
        sftr_security_type_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                sftr_security_type_val = instrument.GetProviderDataFieldValue('SFTR_SECURITY_TYPE')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its sftr_security_type")
        return sftr_security_type_val
    
    def moodys_rating(self, instrument=None):
        """returns the Moody's rating on the instrument"""
        moodys_rating_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            moodys_rating_val = FRegulatoryLibUtils.get_rating(instrument, 'Moodys')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its moodys_rating")
        return moodys_rating_val

    def snp_rating(self, instrument=None):
        snp_rating_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            snp_rating_val = FRegulatoryLibUtils.get_rating(instrument, 'SnP')
            if not snp_rating_val:
                snp_rating_val = FRegulatoryLibUtils.get_rating(instrument, 'StandardsAndPoor')
            if not snp_rating_val:
                snp_rating_val = FRegulatoryLibUtils.get_rating(instrument, 'S&P')
            if not snp_rating_val:
                snp_rating_val = FRegulatoryLibUtils.get_rating(instrument, 'Standards&Poor')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its snp_rating")
        return snp_rating_val

    def fitch_rating(self, instrument=None):
        fitch_rating_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            fitch_rating_val = FRegulatoryLibUtils.get_rating(instrument, 'Fitch')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its fitch_rating")
        return fitch_rating_val

    def outstanding_shares(self, instrument=None):
        outstanding_shares_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                outstanding_shares_val = instrument.GetProviderDataFieldValue('EQY_SH_OUT_REAL')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its outstanding_shares")
        return outstanding_shares_val

    def sf_type(self, instrument=None):
        sf_type_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            sf_type_dict = {'Repo/Reverse' : 'REPO', 'SecurityLoan' : 'SLEB', 'BuySellback' : 'SBSC'}
            ins_type = instrument.InsType()
            if ins_type in sf_type_dict.keys():
                sf_type_val = sf_type_dict[ins_type]
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its sf_type")
        return sf_type_val
    
    def issuer_type(self, instrument=None):
        """returns the type of issuer"""
        issuer_type_val = None
        instrument = self.__get_instrument(instrument)
        if instrument:
            if FRegulatoryLibUtils.get_provider_data_exists():
                issuer_industry_val = instrument.GetProviderDataFieldValue('INDUSTRY_SUBGROUP')
                if issuer_industry_val and issuer_industry_val == 'SUPRA-NATIONAL':
                    issuer_type_val = 'Supranational'
                if not issuer_type_val:
                    market_sector_des_val = instrument.GetProviderDataFieldValue('MARKET_SECTOR_DES')
                    if market_sector_des_val == 'Govt':
                        if issuer_industry_val and issuer_industry_val == 'Central Bank':
                            issuer_type_val = 'Central Bank'
                        else:
                            issuer_type_val = 'Government/Sovereign'
                    elif market_sector_des_val == 'Mtge':
                        mtg_is_agency_backed_val = instrument.GetProviderDataFieldValue('MTG_IS_AGENCY_BACKED')
                        if mtg_is_agency_backed_val == 'Y':
                            issuer_type_val = 'Sovereign Agency'
                    elif market_sector_des_val == 'Muni':
                        issuer_type_val = 'Municipal'
                    elif market_sector_des_val == 'Corp':
                        industry_group_val = instrument.GetProviderDataFieldValue('INDUSTRY_GROUP')
                        if industry_group_val != 'Banks':
                            issuer_type_val = 'Corporate'
                if not issuer_type_val:
                    industry_group_val = instrument.GetProviderDataFieldValue('INDUSTRY_GROUP')
                    if industry_group_val == 'Banks':
                        issuer_type_val = 'Bank'
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid instrument for its issuer_type")
        return issuer_type_val

class MMSLibBase(object):
    def __init__(self, acm_trade=None):
        self.trade = acm_trade
        self.ins_type_lookup = {'Cap' : 'Cap', 'Floor' : 'Floor', 'FRA' : 'FRA'}
        if acm_trade:
            self.instrument = self.trade.Instrument()

    def __get_trade(self, trade=None):
        trd = self.trade
        if trade and trade.IsKindOf(acm.FTrade):
            trd = trade
        return trd

    def asset_class(self, trade=None):
        asset_class_val = None
        trade = self.__get_trade(trade)
        if trade:
            instrument = trade.Instrument()
            if instrument.InsType() in [\
                'Cap', 'Floor', 'FRA', 'CurrSwap', 'Swap'] or\
                (instrument.InsType() == 'Option' and\
                  instrument.Underlying().InsType() == 'Swap'):
                asset_class_val = 'Interest Rate Derivatives'
            elif instrument.InsType() in ['VarianceSwap'] or\
                (instrument.InsType() == 'Option' and\
                  instrument.Underlying().InsType() == 'Stock'):
                asset_class_val = 'Equities'
            elif instrument.InsType() == 'TotalReturnSwap':
                for leg in instrument.Legs():
                    if leg.LegType() == 'Total Return' and\
                     leg.FloatRateReference().InsType() in [\
                        'EquityIndex', 'Stock']:
                        asset_class_val = 'Equities'
            elif instrument.InsType() == 'CreditDefaultSwap':
                asset_class_val = 'Credit Derivatives'
            elif (instrument.InsType() == 'Future/Forward'\
             and instrument.Underlying().InsType() == 'Curr') or \
             instrument.InsType() == 'Curr' or\
             (instrument.InsType() == 'Option'\
             and instrument.Underlying().InsType() == 'Curr') or\
             instrument.InsType() == 'FXOptionDatedFwd':
                asset_class_val = 'Foreign Exchange'
            elif instrument.InsType() in ['PriceSwap', 'Commodity',\
                'Commodity Index', 'Commodity Variant',\
                'Average Future/Forward', 'Average Option'] or\
                (instrument.InsType() == 'Option' and\
                 instrument.Underlying().InsType() in ['Commodity',\
                'Commodity Index', 'Commodity Variant', 'Average Future/Forward']) or\
                (instrument.InsType() == 'Future/Forward' and\
                 instrument.Underlying().InsType() in ['Commodity',\
                'Commodity Index', 'Commodity Variant', 'Average Future/Forward']) :
                asset_class_val = 'Commodities'
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its asset_class")
        return asset_class_val

    def product_sub_group(self, trade=None):
        commodity_base_lookup = {'NRGY' : 'Energy',
                            'METL' : 'Metal',
                            'AGRI' : 'Agriculture',
                            'FRGT' : 'Freight'}
        commodity_sub_lookup = {'COAL': 'Coal',
                                'ELEC': 'Electricity',
                                'NGAS': 'Natural Gas',
                                'OILP': 'Oil',
                                'NPRM': 'Base',
                                'PRME': 'Precious',
                                'EMIS': 'Emissions',}
        product_sub_group_val = None
        trade = self.__get_trade(trade)
        if trade:
            instrument = trade.Instrument()
            if instrument.InsType() == 'Swap':
                ois_ins = False
                float_counter = 0
                for leg in instrument.Legs():
                    if leg.LegType() == 'Float':
                        float_counter = float_counter + 1
                        if leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit() == "Days":
                            ois_ins = True                        
                    elif leg.LegType() == 'Zero Coupon Fixed':
                        product_sub_group_val = 'Zero Coupon Swap'
                if not product_sub_group_val:        
                    if ois_ins:
                        product_sub_group_val = 'OIS (Overnight Index Swap)'
                    elif float_counter == 2:
                        product_sub_group_val = 'Basis Swap'
                    else:
                        product_sub_group_val = 'Interest Rate Swap (Vanilla)'
            elif instrument.InsType() == 'CurrSwap':
                product_sub_group_val = 'Cross Currency Swap'
            elif instrument.InsType() in self.ins_type_lookup.keys():
                product_sub_group_val = self.ins_type_lookup[instrument.InsType()]
            elif instrument.InsType() == 'Option' and instrument.Underlying().InsType() == 'Swap':
                product_sub_group_val = 'Swap Option'
            elif instrument.InsType() in ['VarianceSwap']:
                product_sub_group_val = 'Variance Swap'
            elif (instrument.InsType() == 'Option' and\
                  instrument.Underlying().InsType() == 'Stock'):
                product_sub_group_val = 'Options'
            elif instrument.InsType() == 'TotalReturnSwap':
                for leg in instrument.Legs():
                    if leg.LegType() == 'Total Return' and\
                     leg.FloatRateReference().InsType() in [\
                        'EquityIndex', 'Stock']:
                        product_sub_group_val = 'Equity Swaps'
            elif instrument.InsType() == 'CreditDefaultSwap':
                if instrument.Underlying().InsType() in [\
                    'Bill', 'Bond', 'Convertible',\
                    'Zero', 'FRN', 'IndexLinkedBond', 'PromisLoan']:
                    product_sub_group_val = 'Single Name'
                elif instrument.Underlying().InsType() in ['CreditIndex']:
                    product_sub_group_val = 'Index'
            elif instrument.InsType() == 'Option' and\
             instrument.Underlying().InsType() == 'CreditDefaultSwap':#unit test for this case is pending
                product_sub_group_val = 'Option'
            elif instrument.InsType() == "FxSwap" or (\
                instrument.InsType() == "Curr" and trade.IsFxSwap()):
                product_sub_group_val = 'FX SWAP'
            elif instrument.InsType() == "Curr" and (not trade.IsFxSwap()):
                product_sub_group_val = 'Spot'
            elif (instrument.InsType() == 'Future/Forward' and\
                instrument.Underlying().InsType() == 'Curr') or\
                instrument.InsType() == 'FXOptionDatedFwd':
                product_sub_group_val = 'Forward'
            elif instrument.InsType() == 'Option' and\
                 instrument.Underlying().InsType() == 'Curr':
                product_sub_group_val = 'Option'
            elif instrument.InsType() in ['PriceSwap', 'Average Future/Forward'] or\
                (instrument.InsType() in ['Option', 'Future/Forward'] and\
                  instrument.Underlying().InsType() in ['Commodity',\
                'Commodity Index', 'Commodity Variant', 'Average Future/Forward']):
                product_sub_grp_val = None
                if instrument.InsType() in ['PriceSwap']:
                    product_sub_grp_val = 'Swap'
                elif instrument.InsType() == 'Option' and\
                 instrument.Underlying().InsType() in ['Commodity',\
                'Commodity Index', 'Commodity Variant', 'Average Future/Forward']:
                    product_sub_grp_val = 'Option'
                elif instrument.InsType() == 'Average Future/Forward' or\
                 (instrument.InsType() == 'Future/Forward' and\
                 instrument.Underlying().InsType() in ['Commodity',\
                'Commodity Index', 'Commodity Variant', 'Average Future/Forward']):
                    product_sub_grp_val = 'Forward'
                if instrument.RegulatoryInfo().CommodityProduct():
                    base_product_val = None
                    sub_product_val = None
                    base_product = instrument.RegulatoryInfo().CommodityBaseProduct()
                    sub_product = instrument.RegulatoryInfo().CommoditySubProduct()
                    if base_product.Name() in commodity_base_lookup.keys():
                        base_product_val = commodity_base_lookup[base_product.Name()]
                    if sub_product.Name() in commodity_sub_lookup.keys():
                        sub_product_val = commodity_sub_lookup[sub_product.Name()]
                    
                    if base_product_val:
                        product_sub_group_val = base_product_val
                    else:
                        product_sub_group_val = ''
                    if sub_product_val:
                        product_sub_group_val = product_sub_group_val + ' ' + sub_product_val
                        product_sub_group_val = product_sub_group_val.strip()
                    if product_sub_grp_val:
                        product_sub_group_val = product_sub_group_val + ' ' + product_sub_grp_val
                        product_sub_group_val = product_sub_group_val.strip()
            else:
                FRegulatoryLogger.INFO(logger, "ProductSubGroup is currently not support for <%s> instruments." % instrument.InsType())
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its ProductSubGroup")
        return product_sub_group_val

class SFTRLibBase(object):
    def __init__(self, acm_object=None):
        self.trade = None
        self.instrument = None
        if acm_object and acm_object.IsKindOf(acm.FTrade):
            self.trade = acm_object
            self.instrument = self.trade.Instrument()
        elif acm_object and acm_object.IsKindOf(acm.FInstrument):
            self.instrument = acm_object
        self.sf_type_lookup = {'Repo/Reverse' : 'REPO', 'SecurityLoan' : 'SLEB', 'BuySellback' : 'SBSC'}

    def __get_trade(self, trade=None):
        trd = self.trade
        if trade and trade.IsKindOf(acm.FTrade):
            trd = trade
        return trd
    
    def sftr_type(self, trade=None):
        """returns the sftype of the trade depending upon its underlying instrument"""
        sf_type_val = None
        trade = self.__get_trade(trade)
        if trade:
            if trade.Instrument().InsType() in self.sf_type_lookup:
                sf_type_val = self.sf_type_lookup[trade.Instrument().InsType()]
            else:
                FRegulatoryLogger.INFO(logger, "SFTRType is not supported for trades on instrument of type <%s>" % trade.Instrument().InsType())
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its sftr_type")
        return sf_type_val

    @classmethod
    def date_period_unit(self, date_period_unit_val):
        self.date_period_unit_lookup = {'Months' : 'MNTH', 'Days' : 'DAYS', 'Weeks' : 'WEEK', 'Years' : 'YEAR'}
        date_prd_unit_val = None
        if date_period_unit_val in self.date_period_unit_lookup:
            date_prd_unit_val = self.date_period_unit_lookup[date_period_unit_val]
        return date_prd_unit_val
    
    def sftr_asset_type(self, trade=None):
        sftr_asset_type_val = None
        trade = self.__get_trade(trade)
        if trade:
            if trade.Instrument().InsType() in self.sf_type_lookup:
                if trade.Instrument().Underlying().InsType() in ['Commodity', 'Commodity Variant']:
                    sftr_asset_type_val = 'COMM'
                else:
                    sftr_asset_type_val = 'SECU'
            else:
                FRegulatoryLogger.INFO(logger, "SFTRAssetType is not supported for trades on instrument of type <%s>" % trade.Instrument().InsType())
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its sftr_asset_type")
        return sftr_asset_type_val

    def sftr_security_quality(self, trade=None):
        sftr_security_quality_val = None
        trade = self.__get_trade(trade)
        if trade:
            instrument = trade.Instrument()
            if FRegulatoryLibUtils.get_provider_data_exists():
                sftr_security_quality_val = instrument.GetProviderDataFieldValue('SFTR_SECURITY_QUALITY')
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its sftr_security_quality")
        return sftr_security_quality_val

class ISO3166CountryCodeBase(object):
    def __init__(self, custom_dict={}):
        self.__custom_dict = custom_dict
        self.__default_dict = FRegulatoryLookup.country_code_dict
        self.__city_state_lookup = FRegulatoryLookup.city_state_dict  # this dict can be extended if required here
        self.__subjurisdiction_dict = FRegulatoryLookup.subjurisdiction_codes

    def country_code(self, party):
        """the country code will be returned for the country of the party"""
        party = FRegulatoryLibUtils.get_party_handle(party)
        country_code = None
        if party:
            if party.Country():
                country = party.Country()
                try:
                    if type(country) == unicode:
                        country = unicodedata.normalize('NFKD', country).encode('ascii', 'ignore')
                except:
                    pass
                if self.__custom_dict and country in self.__custom_dict:
                    country_code = self.__custom_dict[country]
                    FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the custom dictionary provided" % country_code)
                if (not country_code) and self.__default_dict and country in self.__default_dict:  # use this as a fall back mechanism
                    country_code = self.__default_dict[country]
                    FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the default dictionary." % country_code)
            if not country_code:
                while party.Parent() and not country_code:
                    party = party.Parent()
                    if party.Country():
                        country_code = self.country_code_from_string(party.Country())
                        if not country_code:
                            FRegulatoryLogger.ERROR(logger, 'The CountryCode for country <%s> on Party <%s> could not be identified' % (party.Country(), party.Name()))
        
        return country_code

    def country_code_from_string(self, country):
            """return country code for the provided country name"""
            try:
                if type(country) == unicode:
                    country = unicodedata.normalize('NFKD', country).encode('ascii', 'ignore')
            except:
                pass
            country_code = None
            if country:
                country = country.strip()
                if self.__custom_dict:
                    for country_val, country_code_val in self.__custom_dict.items():
                        self.__custom_dict.update({country_val.upper(): country_code_val})
                for country_val, country_code_val in self.__default_dict.items():
                    print(country_val.upper(), '    :    ', country_code_val, len(country_val.upper()))
                    self.__default_dict.update({country_val.upper(): country_code_val})
                if self.__custom_dict and country in self.__custom_dict:
                    country_code = self.__custom_dict[country]
                    FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the custom dictionary provided" % country_code)
                if (not country_code) and self.__default_dict and country in self.__default_dict.keys():  # use this as a fall back mechanism
                    country_code = self.__default_dict[country]
                    FRegulatoryLogger.DEBUG(logger, "countryCode <%s> being picked from the default dictionary." % country_code)
            return country_code

    def subJurisdiction(self, country_name, city_name):
        """return the subjurisdiction if applicable"""
        state_code = ''
        sub_jurisdiction = self.country_code_from_string(country_name)

        if not sub_jurisdiction:
            FRegulatoryLogger.WARN(logger, "countryCode not found for country <%s>." % country_name)
        else:
            if city_name in self.__city_state_lookup:
                state = self.__city_state_lookup[city_name]
                if country_name in self.__subjurisdiction_dict:
                    states = self.__subjurisdiction_dict[country_name]
                    if state in states:
                        state_code = states[state]
                    else:
                        FRegulatoryLogger.WARN(logger, "subjurisdiction not found for state <%s> in country <%s>." % (state, country_name))
            else:
                if city_name:
                    FRegulatoryLogger.WARN(logger, "subjurisdiction not found for city <%s> as its state not found in city-state lookup." % (city_name))
                else:
                    FRegulatoryLogger.WARN(logger, "subjurisdiction not found as city details are not present")
            if state_code:
                sub_jurisdiction = sub_jurisdiction + '-' + state_code
        return sub_jurisdiction

    def city_code(self, country_name, city_name, override_dict=None):
        """generates the business center code for a given city in a country on the basis of the country code and the name of the city"""
        city_code_val = ''
        lookup_dict = override_dict
        if not lookup_dict:
            lookup_dict = FRegulatoryLookup.city_code_lookup
        if country_name in list(lookup_dict.keys()):
            if city_name in list(lookup_dict[country_name].keys()):
                city_code_val = (lookup_dict[country_name])[city_name]
        if not city_code_val:
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
                FRegulatoryLogger.WARN(logger, "Cannot infer the country code as the country code for <%s> is not available in the lookup. Kindly add it to the custom_dict" % (country_name))
        return city_code_val

class PartyRegInfoBase(object):
    def __init__(self, party=None):        
        self.party = party
        self.default_jurisdiction_dic = {'ESMA': ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'GR', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'GB'],
            'SEC': ['US'],
            'CSRC': ['CN'],
            'ASIC': ['AU'],
            'SEBI': ['IN'],
            'FMA': ['NZ'],
            'FSA': ['JP'],
            }
        self.parent_list = []

    def __get_party(self, party=None):
        party_obj = self.party
        if party:
            party_obj = FRegulatoryLibUtils.get_party_handle(party)
            if (not party_obj) and (isinstance(party, str)):
                FRegulatoryLogger.ERROR(logger, "Party of name <%s> does not exist in ADS"%party)
        return party_obj

    def country(self, party=None):
        """get the country of the party"""
        country_val = None
        self.parent_list = []
        party = self.__get_party(party)
        if party:
            original_party = party
            if party.Country():
                country_val = party.RiskCountry()
                if not country_val:
                    country_val = party.Country()
                try:
                    if type(country_val) == unicode:
                        country_val = unicodedata.normalize('NFKD', country_val).encode('ascii', 'ignore')
                except:
                    pass
            if not country_val:
                while party.Parent() and not country_val:
                    if party.Parent().Name() not in self.parent_list:
                        party = party.Parent()
                        country_val = party.RiskCountry()
                        if not country_val:
                            country_val = party.Country()
                        self.parent_list.append(party.Parent().Name())
                    else:
                        FRegulatoryLogger.ERROR(logger, "Cannot get country for party <%s> as there is a setup issue with cyclic dependency while configuring party parent."%original_party.Name())
                        break
        else:
            FRegulatoryLogger.ERROR(logger, "A valid party in ADS needs to be passed to get its country")
        return country_val
 
    def jurisdiction(self, party=None):
        """returns the 2 character JurisdictionCountryCode of the party, irrespective of language"""
        jurisdiction = None
        party = self.__get_party(party)
        if party:
            jurisdiction = party.JurisdictionCountryCode()
            if not jurisdiction:
                try:
                    jurisdiction = party.AdditionalInfo().JurisdictionCountryCode()
                except:  # it means the JurisdictionCountryCode AdditionalInfo doesnt exist on the Party
                    FRegulatoryLogger.WARN(logger, "The JurisdictionCountryCode AdditionalInfo is not set on the Party")
                    iso_obj = ISO3166CountryCodeBase()
                    jurisdiction = iso_obj.country_code(party)
        else:
            FRegulatoryLogger.WARN(logger, "Kindly provide a valid Party to retrieve it's jurisdiction")
        return jurisdiction

    def swift_jurisdiction(self, party=None, customer_dic={}):
        """returns group jurisdiction, like ESMA"""
        party = self.__get_party(party)
        if party:
            jurisdiction = self.jurisdiction(party)
            swift_jurisdiction = None
            if jurisdiction:
                if customer_dic:
                    rever_customer_dic = FRegulatoryLibUtils.reverse_dict(customer_dic)
                    if jurisdiction in rever_customer_dic:
                        swift_jurisdiction = rever_customer_dic[jurisdiction]
                if (not swift_jurisdiction) and self.default_jurisdiction_dic:
                    reverse_default_dic = FRegulatoryLibUtils.reverse_dict(self.default_jurisdiction_dic)
                    if jurisdiction in reverse_default_dic:
                        swift_jurisdiction = reverse_default_dic[jurisdiction]
            else:
                if party:
                    FRegulatoryLogger.WARN(logger, "The jurisdiction is not present on the party <%s>. Hence, the swift code cannot be inferrred" % self.party.Name())
        else:
            FRegulatoryLogger.WARN(logger, "A valid party will have a jurisdiction")
        return swift_jurisdiction

    def MIC(self, party=None):
        """returns the MIC alias on the party"""
        mic_code = None
        party_val = party
        party = self.__get_party(party)
        if party:
            if party.Aliases():
                for alias in party.Aliases():
                    if alias.Type().Name() == 'MIC':
                        FRegulatoryLogger.DEBUG(logger, "MIC <%s> being picked from party alias MIC on party <%s>" % (alias.Name(), party.Name()))
                        mic_code = alias.Name()
            if not mic_code and party.Free1():
                FRegulatoryLogger.DEBUG(logger, "MIC being mapped from Free Text 1")
                mic_code = party.Free1()
        elif party_val and isinstance(party_val, str):
                FRegulatoryLogger.WARN(logger, "Party <%s> is not a valid party in ADS. Cannot infer its MIC"%party_val)
        return mic_code

    def LEI(self, party=None):
        """returns the LEI of the party. If not present, then it traverses up the hierarchy to look for LEI"""
        lei = None
        party_val = party
        party = self.__get_party(party)
        if party:
            lei = FRegulatoryLibUtils.get_lei(party)
        elif party_val and isinstance(party_val, str):
                FRegulatoryLogger.WARN(logger, "Party <%s> is not a valid party in ADS. Cannot infer its LEI"%party_val)
        return lei

    def subJurisdiction(self, party=None):
        """returns the subjuridiction on the basis of the country and the city details on the party"""
        sub_jurisdiction = None
        iso_cc = ISO3166CountryCodeBase()
        party_val = party
        party = self.__get_party(party)
        if party:
            sub_jurisdiction = iso_cc.subJurisdiction(party.Country(), party.City())
        elif party_val and isinstance(party_val, str):
                FRegulatoryLogger.WARN(logger, "Party <%s> is not a valid party in ADS. Cannot infer its subJurisdiction"%party_val)
        return sub_jurisdiction

    def ultimate_parent(self, party=None):
        """returns the top node of a Party hierarchy"""
        party_val = party
        party = self.__get_party(party)
        original_party = party       
        if party:
            self.parent_list = []
            while party.Parent():
                if party.Parent():
                    if party.Parent().Name() not in self.parent_list:
                        self.parent_list.append(party.Parent().Name())
                        party = party.Parent()
                    else:
                        FRegulatoryLogger.ERROR(logger, "Cannot get the ultimate parent for party <%s> as there is a setup issue with cyclic dependency while configuring party parent."%original_party.Name())
                        break
            if party and party != self.party:
                FRegulatoryLogger.DEBUG(logger, "The ultimate parent of party <%s> is: <%s>" % (party.Name(), party.Name()))
            else:
                msg = ''
                if self.party.Parent():#it means there is a cyclic dependency
                    msg = 'or has a cyclic dependency upon it'
                FRegulatoryLogger.DEBUG(logger, "Party <%s> is at the topmost node in the Party hierarchy %s" % (party.Name(), msg))
        elif party_val and isinstance(party_val, str):
            FRegulatoryLogger.WARN(logger, "Party <%s> is not a valid party in ADS. Cannot infer its ultimateParent"%party_val)
        return party

    @classmethod
    def countryCodeFromMIC(self, mic_val):
        """return the country code of the party which has the given MIC value"""
        country_code = None
        party = FRegulatoryLibUtils.getPartyFromMIC(mic_val)
        if party:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> Found in ADS with MIC <%s>" % (party.Name(), mic_val))
            country_code_obj = ISO3166CountryCodeBase()
            country_code = country_code_obj.country_code(party)
        else:
            FRegulatoryLogger.INFO(logger, "No Party with MIC <%s> present in ADS" % (mic_val))
        return country_code

    @classmethod
    def partyFromLEI(self, lei_val):
        """return the party which has the given LEI value"""
        party = FRegulatoryLibUtils.getPartyFromLEI(lei_val)
        if party:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> found in ADS with LEI <%s>" % (party.Name(), lei_val))
        else:
            FRegulatoryLogger.INFO(logger, "No Party with LEI <%s> present in ADS" % (lei_val))
        return party

    @classmethod
    def partyFromMIC(self, mic_val):
        """return the party which has the given MIC value"""
        party = FRegulatoryLibUtils.getPartyFromMIC(mic_val)
        if party:
            FRegulatoryLogger.DEBUG(logger, "Party <%s> Found in ADS with MIC <%s>" % (party.Name(), mic_val))
        else:
            FRegulatoryLogger.INFO(logger, "No Party with MIC <%s> present in ADS" % (mic_val))
        return party

    @classmethod
    def isValidLEI(self, lei_val):
        """verify that the given lei follows ISO7064 and that the last two digits are check digits"""
        return FRegulatoryLibUtils.isValidLEI(lei_val)

    @classmethod
    def generateLEIWithCheckSum(self, lei_val):
        """generate the checkSum for the given lei of 18 characters"""
        return FRegulatoryLibUtils.generateLEIWithCheckSum(lei_val)

    def is_jurisdiction(self, jurisdiction, party=None, jurisdiction_lookup=None):
        """return True if the country of the party falls within the given jurisdiction, else return False"""
        is_jurisdiction_val = None
        party_val = party
        party = self.__get_party(party)
        if party:
            is_jurisdiction_val = FRegulatoryLibUtils.is_party_in_jurisdiction(party, jurisdiction, jurisdiction_lookup)
            if is_jurisdiction_val == None:
                FRegulatoryLogger.WARN(logger,\
                "IsJurisdiction cannot be inferred for party <%s> as it is not set"\
                %party.Name())
        elif party_val and isinstance(party_val, str):
            FRegulatoryLogger.WARN(logger,\
                "IsJurisdiction cannot be inferred for party <%s> as it is not as valid party in ADS"\
                %party_val)
        return FRegulatoryLibUtils.get_tristate_choiceList(is_jurisdiction_val)

    def is_regulatory_authority(self, regulatory_authority, party=None, regulatory_authority_lookup = None):
        """return True if the party is governed by the given regulatory authority, else return False"""
        regulatory_authority_val = None
        party_val = party
        party = self.__get_party(party)
        if party:
            regulatory_authority_val = FRegulatoryLibUtils.is_party_in_regulatory_authority(party, regulatory_authority, regulatory_authority_lookup)
            if regulatory_authority_val == None:
                FRegulatoryLogger.WARN(logger,\
                "IsRegulatoryAuthority cannot be inferred for party <%s> as it is not set"\
                 %party.Name())
        elif party_val and isinstance(party_val, str):
            FRegulatoryLogger.WARN(logger,\
                "IsRegulatoryAuthority cannot be inferred for party <%s> as it is not a valid party in ADS"\
                %party_val) 
        return FRegulatoryLibUtils.get_tristate_choiceList(regulatory_authority_val)

class TaxonomyBase(object):
    def __init__(self, acm_object=None):
        self.trade = None
        self.instrument = None
        if acm_object and acm_object.IsKindOf('FTrade'):
            self.trade = acm_object
            self.trd_reg_info = self.trade.RegulatoryInfo()
        elif acm_object and acm_object.IsKindOf('FInstrument'):
            self.instrument = acm_object
            self.instr_reg_info = self.instrument.RegulatoryInfo()

    def __get_trade(self, trade=None):
        trd = self.trade
        if trade and trade.IsKindOf(acm.FTrade):
            trd = trade
        return trd

    def cfi(self, acm_object=None, cfi_code=None, generate=True):
        """generates and returns the CFI code for the instrument if not present on it. If already present on the instrument, it returns the existing CFICode"""
        instrument = None
        trade = None
        if acm_object:
            if acm_object.IsKindOf(acm.FTrade):
                trade = acm_object
            elif acm_object.IsKindOf(acm.FInstrument):
                instrument = acm_object
        else:
            instrument = self.instrument
            trade = self.trade
        if instrument:
            instr_reg_info = instrument.RegulatoryInfo()
            if cfi_code:
                instr_reg_info.CfiCode(cfi_code)
            else:
                cfi = instr_reg_info.CfiCode()
                if (not cfi) and generate:
                    cfi = FRegulatoryCfiCodeGeneration.compute_cfi_code(instrument)
                return cfi
        elif trade:
            trd_reg_info = trade.RegulatoryInfo()
            if (trade.Instrument().InsType() == 'Curr') or \
            (trade.Instrument().InsType() in ['Option', 'Future/Forward'] and trade.Instrument().Underlying().InsType() == 'Curr'):
                if cfi_code:
                    trd_reg_info.CfiCode(cfi_code)
                else:
                    cfi = trd_reg_info.CfiCode()
                    if (not cfi) and generate:
                        cfi = FRegulatoryCfiCodeGeneration.compute_cfi_code(trade)
                    return cfi
            else:
                FRegulatoryLogger.ERROR(logger, "CfiCode for trades is available for FX trades only.")
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid instrument")

    def upi(self, trade=None):
        """return or generate UPI"""
        upi = None
        trade = self.__get_trade(trade)
        if trade:
            upi = FRegulatoryLibUtils.upi(trade)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade")
        return upi

class TradeRegInfoBase(object):
    def __init__(self, trade=None):
        """class that maintains all data related to the regulatory on the FTrade"""
        self.trade = trade
        pass

    def __get_trade(self, trade=None):
        trd = self.trade
        if trade and trade.IsKindOf(acm.FTrade):
            trd = trade
        return trd

    def sftr_is_collateral_provider(self, trade=None):
        """infers if the instrument has the IsCollateralProvider flag set to True or False"""
        is_collateral_provider = None
        trade = self.__get_trade(trade)
        if trade:
            if trade.Instrument().InsType() in ['Repo/Reverse', 'BuySellback', 'SecurityLoan']:
                if trade.Premium() > 0:
                    if trade.Instrument().InsType() in ['Repo/Reverse', 'BuySellback']:
                        is_collateral_provider = True
                    else:
                        is_collateral_provider = False
                else:
                    if trade.Instrument().InsType() in ['Repo/Reverse', 'BuySellback']:
                        is_collateral_provider = False
                    else:
                        is_collateral_provider = True
            else:
                FRegulatoryLogger.WARN(logger, "SFTRIsCollateralProvider is not supported for InsType <%s>"%trade.Instrument().InsType())
            is_collateral_provider = FRegulatoryLibUtils.get_tristate_choiceList(is_collateral_provider)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its SFTRIsCollateralProvider")
        return is_collateral_provider

    def tech_record_identification(self, trade=None):
        """function that returns the technical record identification if present on the trade. If not present, it generates and returns this value"""
        tech_record_identification_val = None
        trade = self.__get_trade(trade)
        if trade:
            tech_record_identification_val = FRegulatoryLibUtils.tech_record_identification(trade)
        else:
            FRegulatoryLogger.WARN(logger, "Please provide a valid trade for its tech_record_identification")
        return tech_record_identification_val

    def buyer(self, trade=None):
        """returns the buyer on the deal. It is often the acquirer or the counterparty on the trade depending on the direction of the transaction"""
        buyer = None
        trade = self.__get_trade(trade)
        if trade:
            us_buyer = FRegulatoryLibUtils.us_buyer(trade)
            if us_buyer:
                buyer = FRegulatoryLibUtils.our_org(trade)
                if not buyer:
                    if trade.RegulatoryInfo().OurOrganisation():
                        buyer = trade.RegulatoryInfo().OurOrganisation()
                    else:
                        buyer = trade.Acquirer()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on buyer <%s> or its linked parent party." % buyer.Name())
            else:
                buyer = FRegulatoryLibUtils.their_org(trade)  # self.trade.RegulatoryInfo().TheirOrg()
                if not buyer:
                    if trade.RegulatoryInfo().TheirOrganisation():
                        buyer = trade.RegulatoryInfo().TheirOrganisation()
                    else:
                        buyer = trade.Counterparty()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on buyer <%s> or its linked parent party." % buyer.Name())
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its buyer")
        return buyer

    def us_buyer(self, trade=None):
        """returns True if we are the buyer of the trade"""
        us_buyer_val = None
        trade = self.__get_trade(trade)
        if trade:
            us_buyer_val = FRegulatoryLibUtils.us_buyer(trade)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its us_buyer")
        return us_buyer_val

    def us_seller(self, trade=None):
        """returns True if we are the seller of the trade"""
        is_us_seller = None
        trade = self.__get_trade(trade)
        if trade:
            is_us_seller = False
            if not FRegulatoryLibUtils.us_buyer(trade):
                is_us_seller = True
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its us_seller")
        return is_us_seller

    def seller(self, trade=None):
        """returns the seller on the deal It is often the acquirer or the counterparty on the trade depending on the direction of the transaction"""
        seller = None
        trade = self.__get_trade(trade)
        if trade:
            us_buyer = FRegulatoryLibUtils.us_buyer(trade)
            if us_buyer:
                seller = FRegulatoryLibUtils.their_org(trade)  # self.trade.RegulatoryInfo().TheirOrg()
                if not seller:  # it means the LEI is not present and hence was not found
                    if trade.RegulatoryInfo().TheirOrganisation():
                        seller = trade.RegulatoryInfo().TheirOrganisation()
                    else:
                        seller = trade.Counterparty()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on seller <%s> or its linked parent party." % seller.Name())
            else:
                seller = FRegulatoryLibUtils.our_org(trade)  # self.trade.RegulatoryInfo().OurOrg()
                if not seller:
                    if trade.RegulatoryInfo().OurOrganisation():
                        seller = trade.RegulatoryInfo().OurOrganisation()
                    else:
                        seller = trade.Acquirer()
                    FRegulatoryLogger.ERROR(logger, "LEI is not present on seller <%s> or its linked parent party." % seller.Name())
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its seller")
        return seller

    def is_increase(self, trade=None):
        """return if the trade implies an increase or decrease of notional"""
        is_increase_decrease = None
        trade = self.__get_trade(trade)
        if trade:
            if trade.Contract().Oid() != trade.Oid():
                trade_nominal = trade.Nominal()
                contract_nominal = trade.Contract().Nominal()
                if trade_nominal > contract_nominal:
                    is_increase_decrease = 'INCR'
                elif trade_nominal < contract_nominal:
                    is_increase_decrease = 'DECR'
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its is_increase")
        return is_increase_decrease

    def country_of_branch(self, trade=None):
        """return country of the branch membership field"""
        country_of_branch = None
        branch_membership = None
        trade = self.__get_trade(trade)
        if trade:
            regulatory_info = trade.RegulatoryInfo()
            branch_membership = regulatory_info.BranchMembership()
            if branch_membership:
                country_of_branch = branch_membership.Country()
            else:
                FRegulatoryLogger.INFO(logger, "BranchMembership is not defined on trade <%d>" % trade.Oid())
            if branch_membership and not country_of_branch:
                FRegulatoryLogger.INFO(logger, "Country is not defined on party <%s> assigned as BranchMembership on trade <%d>" % (branch_membership.Name(), trade.Oid()))
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its country_of_branch")
        return country_of_branch

    def country_code_of_branch(self, trade=None):
        """return country code of the branch membership field"""
        country_code_of_branch = None
        country_of_branch = self.country_of_branch(trade)
        if not country_of_branch:
            FRegulatoryLogger.INFO(logger, "Country is not defined. Hence country code cannot be inferred.")
        else:
            iso_obj = ISO3166CountryCodeBase()
            country_code_of_branch = iso_obj.country_code_from_string(country_of_branch)
        return country_code_of_branch

    def complex_trade_component_id(self, trade=None):
        """Generates and returns the complex trade component id on the trade (if not present), else it returns the regComplexTrdCmptId AddInfo value on the Trade"""
        complex_cmpt_id = None
        trade = self.__get_trade(trade)
        if trade:
            complex_cmpt_id = trade.RegulatoryInfo().AdditionalInfo().RegComplexTrdCmptId()
            if not complex_cmpt_id:
                complex_cmpt_id = FRegulatoryLibUtils.generate_complex_trade_comp_id(trade)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its complex_trade_component_id")
        return complex_cmpt_id

    def trading_capacity(self, trade=None):
        """what role do we have in the deal, investor, broker, and so on"""
        trading_capacity = None
        trade = self.__get_trade(trade)
        if trade:
            trading_capacity = trade.RegulatoryInfo().TradingCapacity()
            if (not trading_capacity) or trading_capacity == 'None':
                trading_capacity = 'DEAL'
                reporting_entity = trade.RegulatoryInfo().ReportingEntity()
                if reporting_entity:
                    if trade.Acquirer():
                        if trade.Acquirer() != reporting_entity:
                            trading_capacity = 'AOTC'
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its trading_capacity")
        return trading_capacity

    def cfi_code(self, trade=None, set_cfi_code=False):
        """generates and returns the CFI code of the Trade (if not present), else it returns the CFI code on the Trade. This is applicable only in case of FX Trades"""
        cfi_code = None
        trade = self.__get_trade(trade)
        if trade:
            taxonomy = TaxonomyBase(trade)
            cfi_code = taxonomy.cfi(None, None, set_cfi_code)
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its cfi_code")
        return cfi_code

    def notional_amount(self, trade=None):
        """ Returns notional amount for trade"""
        notional_amt = None
        trade = self.__get_trade(trade)
        if trade:
            notional_amt = FRegulatoryNotionalAmount.FRegulatoryNotionalAmount(trade).notional_amount()
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its notional_amount")
        return notional_amt

    def is_fx_forward(self, trade=None):
        """returns True if the trade is an FXForward"""
        fx_forward = None
        trade = self.__get_trade(trade)
        if trade:
            fx_forward = False
            try:
                if trade.IsFxForward():
                    fx_forward = True
            except:
                pass
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its is_fx_forward")
        return fx_forward

    def is_fx_swap(self, trade=None):
        """returns True if the trade is one of the legs in an FXSwap"""
        fx_swap = None
        trade = self.__get_trade(trade)
        if trade:
            fx_swap = False
            try:
                if trade.FxSwapFarLeg():
                    fx_swap = True
                if trade.FxSwapNearLeg():
                    fx_swap = True
            except:
                pass
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its is_fx_swap")
        return fx_swap

    def is_near_leg_fx_swap(self, trade=None):
        """returns True if the trade is the near leg of an FXSwap"""
        fx_swap = None
        trade = self.__get_trade(trade)
        if trade:
            fx_swap = False
            try:
                if trade.FxSwapFarLeg():
                    fx_swap = True
            except:
                pass
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its is_near_leg_fx_swap")
        return fx_swap

    def Isin(self, trade=None):
        """returns the Isin on the trade if present, else fallback to Isin on the instrument and then similarIsin on the instrument's RegulatoryInfo"""
        isin = None
        trade = self.__get_trade(trade)
        if trade:
            try:
                if trade.RegulatoryInfo().AdditionalInfo().RegInsIsin():
                    isin = trade.RegulatoryInfo().AdditionalInfo().RegInsIsin()
            except:
                if trade.AdditionalInfo().RegInsIsin():
                    isin = trade.RegulatoryInfo().RegInsIsin()
            if not isin:
                ins = trade.Instrument()
                ins_reg = InstrumentRegInfoBase(ins)
                isin = ins_reg.Isin()
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its isin")
        return isin

    def reported_price(self):  # this is the clean price
        # TODO:
        pass

    def price(self, trade=None):
        """returns the Transaction Price amount of the trade"""
        price = None
        trade = self.__get_trade(trade)
        if trade:
            instrument = trade.Instrument()
            ins_type = instrument.InsType()
            if (ins_type in ['Bill', 'Bond', 'Convertible', \
                             'DualCurrBond', 'FRN', 'PromisLoan', \
                             'Zero', 'Flexi Bond', 'IndexLinkedBond']):
                if instrument.Quotation().Name() == 'Yield':
                    price = trade.Price() / instrument.Quotation().QuotationFactor()
                else:
                    price = trade.Price() * instrument.Quotation().QuotationFactor() * 100
            elif ins_type in ['Stock', 'Deposit', \
                              'CD', 'MBS/ABS', 'Commodity Index', \
                'Future/Forward', 'FreeDefCF'] or (ins_type == 'Curr' and (self.is_fx_forward(trade))):
                price = trade.Price()
            elif ins_type in ['IndexLinkedSwap', 'TotalReturnSwap', 'Swap'] and \
                            FRegulatoryLibUtils.get_swap_type(instrument) in ['Fixed Fixed Swap', 'Vanilla Swap']:
                fixed_rate = 0
                for leg in trade.Instrument().Legs():
                    if FRegulatoryLibUtils.get_swap_type(instrument) == 'Fixed Fixed Swap':
                        if leg.LegType() == 'Fixed':
                            if fixed_rate:
                                fixed_rate = fixed_rate - leg.FixedRate()
                            else:
                                fixed_rate = leg.FixedRate()
                    else:
                        fixed_rate = instrument.FirstFixedLeg().FixedRate()
                price = fixed_rate
            elif ins_type in ['Swap', 'IndexLinkedSwap', 'TotalReturnSwap', 'CurrSwap'] and \
                            FRegulatoryLibUtils.get_swap_type(instrument) == 'Basis Swap':
                float_rate = 0
                for leg in trade.Instrument().Legs():
                    if leg.Spread():
                        if not float_rate:
                            float_rate = leg.Spread()
                            price = float_rate
                        else:
                            msg = "Cannot infer the Price for trade <%d> on instrument <%s> as it has spread on both the legs." % (trade.Oid(), instrument.Name())
                            FRegulatoryLogger.ERROR(logger, msg)
                            raise Exception(msg)
            elif ins_type in ['CurrSwap'] and FRegulatoryLibUtils.get_swap_type(instrument) in ['Vanilla Swap']:
                price = instrument.FirstFixedLeg().FixedRate()
            elif ins_type in ['FRA']:
                price = (trade.Instrument().Legs()[0].FixedRate())
            elif ins_type in ['CreditDefaultSwap']:
                # decorater = acm.FTradeLogicDecorator(self.trade, None)
                # price = decorater.ViceVersa()
                # price = (price) * 100
                price = trade.Instrument().FirstFixedLeg().FixedRate()
            elif ins_type == 'Curr' and self.is_fx_swap(trade):
                both_trades = True
                if config_param:
                    if config_param.get_paramvalue('FREGULATORY_FXSWAP_TRADES') and \
                                    config_param.get_paramvalue('FREGULATORY_FXSWAP_TRADES').upper() == 'SINGLE':
                        both_trades = False
                if both_trades:
                    price = trade.Price()
                else:
                    currency1 = instrument.Name()
                    currency2 = trade.Currency().Name()
    
                    conversion_factor, curr_pair = InstrumentRegInfoBase.get_conversion_factor(currency1, currency2)
                    if not curr_pair:
                        FRegulatoryLogger.ERROR(logger, "PriceAmount could not be calculated for trade <%d> as the currency pair for <%s> and <%s> is not available in ADS" % (trade.Oid(), currency1, currency2))
                    if conversion_factor:
                        price = (trade.Price() - trade.FxSwapFarLeg().Price()) / conversion_factor
                        price = (price)
            elif ins_type in ['Option']:
                if instrument.Underlying().InsType() == 'Curr':
                    call_currency = instrument.Underlying().Name()
                    premium_currency = trade.Currency().Name()
                    if call_currency != premium_currency:
                        conversion_factor, curr_pair = InstrumentRegInfoBase.get_conversion_factor(call_currency, premium_currency)
                        if not curr_pair:
                            FRegulatoryLogger.ERROR(logger, "PriceAmount could not be calculated for trade <%d> as the currency pair for <%s> and <%s> is not available in ADS" % (trade.Oid(), call_currency, premium_currency))
                        if conversion_factor:
                            price = trade.Price() * conversion_factor
                    else:
                        price = trade.Price()
                else:
                    price = trade.Price()
            elif ins_type in ['Cap', 'Floor']:
                price = trade.Price()
                if 'Per Unit' in trade.Instrument().Quotation().QuotationType():
                    price = price * trade.Instrument().Quotation().QuotationFactor()
                elif 'Factor' in trade.Instrument().Quotation().QuotationType():
                    price = price * 100 * trade.Instrument().Quotation().QuotationFactor()
            elif ins_type in ['FXOptionDatedFwd']:
                if trade.Instrument().ExerciseEvents():
                    price = trade.Instrument().ExerciseEvents()[0].Strike()
            else:
                FRegulatoryLogger.ERROR(logger, "Price could not be inferred for trade <%d> as instrument type <%s> is currently not supported" % (trade.Oid(), trade.Instrument().InsType()))
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its price")
        return price

    def ISITC_type_code(self, trade=None):
        """"returns the ISIT classification code for the FXTrade"""
        trade = self.__get_trade(trade)
        ISITC_type_code_val = None
        if trade:
            isitic_code_obj = FRegulatoryISITCode.ISITCodeType(trade)
            ISITC_type_code_val = isitic_code_obj.get_isitic_classification()
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its ISITC_type_code")
        return ISITC_type_code_val

    def is_cleared(self, trade=None):
        """return True of the trade is cleared at clearing house, else False"""
        trade = self.__get_trade(trade)
        is_cleared_trd = None
        if trade:
            if trade.RegulatoryInfo() and trade.RegulatoryInfo().ClearingHouse():
                is_cleared_trd = True
            else:
                is_cleared_trd = False
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its is_cleared")
        return is_cleared_trd

    def implied_volatility(self):#TODO:
        """returns the implied volatility of the trade"""
        global space
        space.Clear()
        return self.instrument.Calculation().ImpliedVolatility(space)

class PersonRegInfoBase(object):
    def __init__(self, person):
        self.contact = None
        self.person = None
        try:
            if person.IsKindOf(acm.FContact):
                self.contact = person
            elif person.IsKindOf(acm.FPerson):
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
                    except Exception as e:
                        FRegulatoryLogger.ERROR(logger, "Error while getting the date of birth from Person. Error: <%s>" % str(e)) 

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

    def __init__(self, acm_trade=None, installation='Prod', system='FrontArena', utiCategory="E02", useChecksum=True):
        # Store installation, system, utiCtegory and useChecksum
        # Store them statically since they should be initialized at "Organization" level
        UniqueTradeIdentifierBase.uti_installation = installation
        UniqueTradeIdentifierBase.uti_system = system
        UniqueTradeIdentifierBase.uti_category = utiCategory
        UniqueTradeIdentifierBase.uti_user_check_sum = useChecksum
        self.trade = acm_trade

    def __get_trade(self, trade=None):
        trd = self.trade
        if trade:
            trd = trade
        return trd

    def check_sum(self, utiVal):
        """generate check sum for a UTI"""
        return FRegulatoryLibUtils.check_sum(utiVal)

    def generateUTI(self, trade=None, uti_category=None, uti_system=None, uti_installation=None):
        """generate a UTI, with a bank-defined, structure, to be used across the bank"""
        uti = None
        trade = self.__get_trade(trade)
        if uti_category:
            UniqueTradeIdentifierBase.uti_category = uti_category
        if uti_system:
            UniqueTradeIdentifierBase.uti_system = uti_system
        if uti_installation:
            UniqueTradeIdentifierBase.uti_installation = uti_installation
        our_org = FRegulatoryLibUtils.our_org(trade)
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

    def uti(self, trade=None, generateIfNotExists=False):
        """Generates and returns the UTI for the trade if not present on it. If already present on the trade, it returns the existing UTI"""
        uti = None
        trade = self.__get_trade(trade)
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
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its UTI")
        return uti

    def is_correct_check_sum(self, uti_val):
        """validate the check sum"""
        b_correct_check_sum = None
        if uti_val:
            b_correct_check_sum = FRegulatoryLibUtils.is_valid_check_sum(uti_val)
        else:
            FRegulatoryLogger.INFO(logger, "Please provide a UTI value to verify checksum")
        return b_correct_check_sum

    def trade_UTI_has_correct_check_sum(self, trade=None):
        """validate the check sum of a UTI"""
        b_correct_check_sum = None
        trade = self.__get_trade(trade)
        if trade:
            uti_val = self.uti(trade)
            b_correct_check_sum = False
            if uti_val:
                b_correct_check_sum = FRegulatoryLibUtils.is_valid_check_sum(uti_val)
            else:
                FRegulatoryLogger.INFO(logger, "Trade <%d> does not have UTI on it" % trade.Oid())
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its trade_UTI_has_correct_check_sum")
        return b_correct_check_sum

    def have_we_generated_UTI(self, trade=None):
        """was this UTI generated by the bank, or imported"""
        b_generated_uti = None
        trade = self.__get_trade(trade)
        if trade:
            b_generated_uti = False
            if self.uti(trade) == self.generateUTI(trade):
                b_generated_uti = True
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid trade for its have_we_generated_UTI")
        return b_generated_uti

