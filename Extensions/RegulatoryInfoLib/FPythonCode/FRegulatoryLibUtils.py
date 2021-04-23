"""------------------------------------------------------------------------
MODULE
    FRegulatoryLibUtils -
DESCRIPTION:
    This file consists of the actual implementation of the API open to customizations to users in the FRegulatoryLib
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import acm
import ael
import FRegulatoryLogger
import FIntegrationUtils
import FRegulatoryLookup
import FRegulatoryCfiCodeGeneration
import operator
import re
logger = "FRegulatoryLibUtils"
day_count_convention_lookup = {
'1/1':   '1/1',
'30/360':   '30/360', 
'30/360GERMAN':   '30/360GERMAN', 
'30/360SIA':   '30/360SIA', 
'30/365':   '30/365', 
'30E/360':   '30E/360', 
'30E/365':   '30E/365', 
'30U/360':   '30U/360', 
'Act/360':   'A004',
'Act/364':   'Act/364', 
'Act/365':   'Act/365', 
'Act/365L':   'Act/365L', 
'Act/ActAFB':   'A010',
'Act/ActISDA':   'A008',
'Act/ActISMA (Act/ActICMA)':   'A006',
'Bus/252':   'Bus/252', 
'NL/360':   'NL/360', 
'NL/365':   'NL/365', 
'NL/ActISDA':   'NL/ActISDA', 
}

def get_party_handle(party_val):
    """get the actual party object from the given input - either string or party obj"""
    party_handle = None
    try:
        if isinstance(party_val, str):
            party_handle = acm.FParty[party_val]
        elif party_val.IsKindOf(acm.FParty):
            party_handle = party_val
    except Exception as e:
        # this exception is hit when the IsKindOf is called on a None party object that is being sent
        pass
    return party_handle
def day_count_method(day_count_method_val):
    """returns the corresponding DayCountMethod for that in PRIME"""
    daycount_method = None
    if day_count_method_val in day_count_convention_lookup.keys():
        day_count_convention_lookup[day_count_method_val]
    else:
        FRegulatoryLogger.ERROR(logger, "DayCountMethod <%s> is not supported in SFTR Codes"%day_count_method_val)
    return daycount_method

def get_provider_data_exists():
    """returns True if the DataLoader's GetProviderDataFieldValue
     API is available in the ADS, else False"""
    get_provider_data_api_exists = False
    try:
        if acm.FInstrument.GetMethod('GetProviderDataFieldValue', 1):
            get_provider_data_api_exists = True
    except:
        pass
    return get_provider_data_api_exists

def get_country(party):
    """gets the list of countries on a given party
     - Country of Risk and Country set on it"""
    countries = []
    if party.RiskCountry():
        countries.append(party.RiskCountry().Name())
    if party.Country():
        countries.append(party.Country())
    if not countries:
        FRegulatoryLogger.WARN(logger,\
            "CountryOfRisk/Country is not set on %s"%(party.Name()))
    return countries

def get_countrycode(country):
    """gets the country code for the given country"""
    country_code = None
    for country_val, country_code in FRegulatoryLookup.country_code_dict.items():
        FRegulatoryLookup.country_code_dict.update({country_val.upper(): country_code})

    if country.upper() in FRegulatoryLookup.country_code_dict.keys():
        country_code = FRegulatoryLookup.country_code_dict[country.upper()]
    return country_code

def __get_modified_jurisdiction_lookup(jurisdiction_lookup=None):
    if not jurisdiction_lookup:
        jurisdiction_lookup = FRegulatoryLookup.jurisdiction_codes
    else:#complement your dict with the incoming dict values
        for each_key in jurisdiction_lookup:
            if each_key in FRegulatoryLookup.jurisdiction_codes:
                country_codes = FRegulatoryLookup.jurisdiction_codes[each_key]
                override_country_codes = jurisdiction_lookup[each_key]
                for each_country_code in override_country_codes:
                    if each_country_code.find('-') == 0:#it means it needs to be removed from the list
                        country_code_val = each_country_code.replace('-', '')
                        if country_code_val in country_codes:
                            country_codes.remove(country_code_val)
                    else:
                        country_codes.append(each_country_code)
                FRegulatoryLookup.jurisdiction_codes[each_key] = country_codes
                jurisdiction_lookup = FRegulatoryLookup.jurisdiction_codes
    return jurisdiction_lookup

def is_jurisdiction(jurisdiction, country_code, jurisdiction_lookup=None):
    """returns True if the given country code is applicable for
     the given jurisdiction, else False. If it cannot be inferred
     returns False """
    is_jurisdiction_val = None
    jurisdiction_lookup = __get_modified_jurisdiction_lookup(jurisdiction_lookup)
    if jurisdiction in jurisdiction_lookup.keys():
        country_codes = jurisdiction_lookup[jurisdiction]
        if jurisdiction == 'EEA':
            country_codes.extend(jurisdiction_lookup['EU'])
        if country_code in country_codes:
            is_jurisdiction_val = True
        else:
            is_jurisdiction_val = False
    else:
        FRegulatoryLogger.WARN(logger,\
            "Jurisdiction <%s> is currently not supported in the library."%jurisdiction)
    return is_jurisdiction_val

def is_party_in_regulatory_authority(party, regulatory_authority, regulatory_authority_lookup=None, jurisdiction_lookup=None):
    """returns True if the given party is applicable for the
     given Regulatory Authority, else False. Returns None
      if it cannot be inferred"""
    is_regulatory_authority = None
    country_code = None
    countries = get_country(party)
    for country in countries:
        country_code = get_countrycode(country)
        if country_code:
            if not regulatory_authority_lookup:
                regulatory_authority_lookup = FRegulatoryLookup.regulatory_authority
            jurisdiction_val = get_jurisdiction(country_code, jurisdiction_lookup)
            if jurisdiction_val:
                if jurisdiction_val in regulatory_authority_lookup.keys():
                    if regulatory_authority_lookup[jurisdiction_val] == regulatory_authority:
                        is_regulatory_authority = True
                    else:
                        is_regulatory_authority = False
                else:
                    if country_code in regulatory_authority_lookup.keys():
                        if regulatory_authority_lookup[country_code] == regulatory_authority:
                            is_regulatory_authority = True
                        else:
                            is_regulatory_authority = False
                    else:
                        FRegulatoryLogger.WARN(logger,\
                        "The regulatory authority cannot be inferred for Country <%s>/jurisdiction <%s> "%(country, jurisdiction_val))
            else:
                if country_code in regulatory_authority_lookup.keys():
                    if regulatory_authority_lookup[country_code] == regulatory_authority:
                        is_regulatory_authority = True
                    else:
                        is_regulatory_authority = False
                else:
                    FRegulatoryLogger.WARN(logger,\
                    "The regulatory authority cannot be inferred for country <%s>"%country)
        else:
            FRegulatoryLogger.WARN(logger,\
            "Unable to infer the country code for country <%s> set on party <%s>"\
            %(country, party.Name()))
    if not country:
        FRegulatoryLogger.WARN(logger,\
            "IsJurisdiction cannot be inferred for Party <%s> as it does not have the CountryOfRisk/Country set on it"%(party.Name()))
    return is_regulatory_authority

def is_party_in_jurisdiction(party, jurisdiction, jurisdiction_lookup=None):
    """returns True if the given party is applicable for the
     given jurisdiction, else False. Returns None
      if it cannot be inferred"""
    is_jurisdiction_val = None
    countries = get_country(party)
    if countries:
        for country in countries:
            country_code = get_countrycode(country)
            if country_code:
                is_jurisdiction_val = is_jurisdiction(jurisdiction, country_code, jurisdiction_lookup)
                if is_jurisdiction_val != None:
                    break
            else:
                FRegulatoryLogger.WARN(logger,\
                "Unable to infer the country code for Country <%s> set on Party <%s>"\
                %(country, party.Name()))
    else:
        FRegulatoryLogger.WARN(logger,\
            "IsJurisdiction cannot be inferred for Party <%s> as it does not have the CountryOfRisk/Country set on it"%(party.Name()))
    return is_jurisdiction_val
      
def get_jurisdiction(country_code, jurisdiction_lookup=None):
    """returns the juridiction for the given country code"""
    jurisdiction_val = None
    jurisdiction_lookup = __get_modified_jurisdiction_lookup(jurisdiction_lookup)
    for jurisdiction in jurisdiction_lookup.keys():
        country_codes = jurisdiction_lookup[jurisdiction]
        if country_code in country_codes:
            jurisdiction_val = jurisdiction
            break
    return jurisdiction_val

class BondTypeEnum():
    enumeration =   (
                     'ABS',    # 0. 
                     'MBS',    # 1.
                     'CDO',    # 2.
                     'CBO',    # 3.
                     'CLO',    # 4.
                     'CMO',    # 5.
                     'TIPS',    # 6.
                     'Covered Bond',    # 7.
                     'Jumbo Pfandbrief',    # 8.
                     'Pfandbrief',    # 9.
                     'Bill',    # 10.
                     'Bullet',    # 11.
                     'TBill',    # 12.
                     'TBond',    # 13.
                     'TNote',    # 14.
                     'Commercial Paper',    # 15.
                     'Pool',    # 16.
                     'Whole Loan',    # 17.
                     'Non Bullet',    # 18.
                     'Other Bond',    # 19.
                     'LoC',    # 20.
                     'CAT',    # 21.
                     'Interest Only (PO) Strips',    # 22.
                     'Principal Only (IO) Strips',    # 23.
                     'ABS Senior',    # 24.
                     'ABS Mezzanine',    # 25.
                     'ABS First Loss'    # 26.
                    )
    def name(self, val):
        try:

            name = self.enumeration[val]
        except IndexError:
            name = self.enumeration[len(self.enumeration) - 1]
        return name

    def number(self, val):
        try:
            index = self.enumeration.index(val)
        except (TypeError, ValueError):
            index = (len(self.enumeration) - 1)
        return index

def get_tristate_choiceList(cl_val):
    """get the Tristate choicelist object for the value being passed"""
    cl_obj = acm.FChoiceList.Select01("list = 'Tristate' and name = '%s'"%str(cl_val), None)
    if not cl_obj:
        FRegulatoryLogger.ERROR(logger, "ChoiseList of name Tristate with values True, False and None should to be present in ADS for expected behaviour")
    return cl_obj

def get_isin_from_alias(instrument):
    """check if there is an alias of the name ISIN in DB and return the value if present on the instrument"""
    isin = None
    try:
        isin = instrument.Alias('Isin')
    except:
        pass
    return isin

def get_isin_from_addinfo(instrument):
    """check if there is an AddInfo on the name ISIN on the instrument. If present, then return this value"""
    isin = None
    try:
        isin = instrument.AdditionalInfo().Isin()
    except:
        pass
    return isin

def get_isin_from_similar_isin(instrument):
    """check if there is an AddInfo on the name ISIN on the instrument. If present, then return this value"""
    isin = None
    try:
        isin = instrument.RegulatoryInfo().SimilarIsin()
    except:
        pass
    return isin

def get_ins_category(instrument):
    ins_type_category = {
                    'CREDIT': ('CreditDefaultSwap', 'CLN', 'Bill', 'Bond', 'Credit Balance', 'CreditIndex', \
                                    'DualCurrBond', 'Flexi Bond', 'FRN', 'MBS/ABS', 'PromisLoan', 'Zero',),
                    'IR': ('Portfolio Swap', 'BasketSecurityLoan', 'Repo/Reverse', 'BasketRepo/Reverse', \
                                    'Swap', 'RateIndex', 'PriceIndex', 'IndexLinkedBond', \
                                    'IndexLinkedSwap', 'Floor', 'FRA', 'CurrSwap', 'FreeDefCF', 'Collateral', \
                                    'Cap', 'BuySellback',),
                    'COMMODITY': ('Average Future/Forward', 'Commodity Index', 'Commodity Variant', 'Commodity', \
                                    'PriceSwap', 'Rolling Schedule',),
                    'EQUITY': ('Certificate', 'Depositary Receipt', 'Dividend Point Index', 'EquityIndex', \
                                    'ETF', 'SecurityLoan', 'Stock', 'VarianceSwap', 'VolatilitySwap', 'Warrant', 'Fund',),
                    'FX': ('Curr', 'FXOptionDatedFwd', 'FxSwap', 'CD', 'Fx Rate',),
                    }
    ins_category = None
    ins_type = instrument.InsType()
    ins_categroy_rev_dict = dict(list(zip(list(ins_type_category.values()), list(ins_type_category.keys()))))
    for each_val in ins_categroy_rev_dict:
        if ins_type in each_val:
            ins_category = ins_categroy_rev_dict[each_val]
            break
    ins_with_underlyers = ['Combination', 'Convertible', 'Future/Forward', 'Option', 'CFD', 'TotalReturnSwap',]
    if not ins_category and instrument.InsType() == 'Deposit':
        if instrument.Legs()[0].LegType() not in ['Call Fixed', 'Call Float', 'Call Fixed Adjustable']:
            ins_category = 'IR'
        else:
            ins_category = 'FX'
    if (not ins_category) and instrument.InsType() in ins_with_underlyers:
        ins = instrument.Underlying()
        if not ins:
            if instrument.InsType() == 'Combination':
                ins = instrument.InstrumentMaps()[0].Instrument()
            elif instrument.InsType() == 'TotalReturnSwap':
                for leg in instrument.Legs():
                    if leg.LegType() == 'Total Return':
                        ins = leg.IndexRef()
        if ins:
            ins_category = get_ins_category(ins)
    return ins_category

def reverse_dict(dictionary):
    reverse_dict = {}
    for key, value in dictionary.items():
        if not isinstance(value, (list, tuple)):
            value = [value]
        for val in value:
            reverse_dict[val] = reverse_dict.get(val, [])
            reverse_dict[val].append(key)
    for key, value in reverse_dict.items():
        if len(value) == 1:
            reverse_dict[key] = value[0]
    return reverse_dict

def generate_complex_trade_comp_id(trade):
    """generate the complexTradeComponentId, prefixed with DP for a DealPackage, TP for a TradePackage 
    and CR for trade.connected_reference. If none of these connected, return None"""
    complex_trade_comp_id = None
    if trade.DealPackageTradeLinks():
        deal_package = trade.DealPackageTradeLinks()[0].DealPackage()
        complex_trade_comp_id = "DP" + deal_package
    elif trade.TradePackage():
        complex_trade_comp_id = "TP" + str(trade.TradePackage().Oid())
    elif trade.ConnectedTrade().Oid() != trade.Oid():
        complex_trade_comp_id = "CR" + str(trade.ConnectedTrade().Oid())
    return complex_trade_comp_id

def get_instrument_sub_type(trade):
    """specific classification of instrument type"""
    ins_type = None
    if trade:
        if trade.Instrument().InsType() == 'Swap':
            leg_type = {}
            for leg in trade.Instrument().Legs():
                val = 0
                if leg.LegType() in leg_type:
                    val = leg_type[leg.LegType()]
                leg_type[leg.LegType()] = val + 1
            if 'Float' in leg_type:
                leg_count = leg_type['Float']
                if leg_count == 2:
                    ins_type = 'Basis Swap'
                elif leg_count == 1 and  'Fixed' in leg_type and leg_type['Fixed'] == 1 :
                    ins_type = 'Fixed Float Swap'
                elif leg_count == 1 and  'Fixed Accretive' in leg_type and leg_type['Fixed Accretive'] == 1 :
                    ins_type = 'Fixed Float Swap'
                else:
                    FRegulatoryLogger.WARN(logger, "We are currently supporting only Fixed/Fixed Accretive Float IRS, Basis Swap and Stock")
        elif trade.Instrument().InsType() == 'Future/Forward':
            ins_type = 'Future/Forward'
            if trade.Instrument().Underlying().Cid()=='Curr':
                ins_type='Future/Forward-Curr'
        else:
            ins_type=trade.Instrument().InsType()
    else:
        FRegulatoryLogger.ERROR(logger, "Please provide a valid Trade to infer its Instrument Sub Type")
    return ins_type

def is_settle_ccy_major(trade):
    settle_in_major_ccy = False
    currency1 = trade.Currency().Name()
    currency2 = trade.Instrument().Underlying().Name()
    ccy_pair = acm.FCurrencyPair.Select01("currency1 = '%s' and currency2 = '%s'"%(currency1, currency2), None)
    if not ccy_pair:
        ccy_pair = acm.FCurrencyPair.Select01("currency1 = '%s' and currency2 = '%s'"%(currency2, currency1), None)
    if ccy_pair:
        major_ccy = ccy_pair.Name().split('/')[0] 
        #minor_ccy = ccy_pair.Name().split('/')[1]
        if currency1 == major_ccy:
            settle_in_major_ccy = True
    return settle_in_major_ccy

def us_buyer(trade):
    weBuyer = False
    ins_type = get_instrument_sub_type(trade)
    if ins_type == 'Basis Swap':
        counter = 0
        for leg in trade.Instrument().Legs():
            if (trade.Nominal() > 0 and leg.PayLeg()) or (trade.Nominal() < 0 and (not leg.PayLeg())):
                leg_nbr = operator.xor(1, counter)
                spread = leg.Spread()
                spread1 = trade.Instrument().Legs()[leg_nbr].Spread()
                if (spread1 == 0.0 and spread != 0.0) or (spread - spread1 > 0):
                    weBuyer = True
            counter += 1
    elif ins_type == 'Fixed Float Swap':
        if (trade.Instrument().FirstFixedLeg().PayLeg() and trade.Nominal() > 0) or (not trade.Instrument().FirstFixedLeg().PayLeg() and trade.Nominal() < 0) :
            weBuyer = True
    elif ins_type in ['TotalReturnSwap']:
        for leg in trade.Instrument().Legs():
            if (not leg.PayLeg() and trade.Nominal() > 0) or (leg.PayLeg() and trade.Nominal() < 0):
                if (leg.LegType() == 'Total Return' and ins_type == 'TotalReturnSwap'):                    
                    weBuyer = True

    elif ins_type in ['CreditDefaultSwap']:
        for leg in trade.Instrument().Legs():
            if (not leg.PayLeg() and trade.Nominal() < 0) or (leg.PayLeg() and trade.Nominal() > 0):
                if (leg.LegType() == 'Fixed'):
                    weBuyer = True
    elif ins_type == 'Future/Forward-Curr':
        if trade.BaseCostDirty() > 0 or trade.Nominal() > 0:
            if trade.BaseCostDirty() > 0:
                weBuyer = True
                if trade.Nominal() < 0 and abs(trade.Nominal()) == abs(trade.BaseCostDirty()):
                    weBuyer = False
            elif not is_settle_ccy_major(trade):
                weBuyer = True
        else:#if the nominal/basecost dirty is negative and the trade currency is the major currency, it means we are buyer
            currency1 = trade.Currency().Name()
            currency2 = trade.Instrument().Underlying().Name()
            ccy_pair = acm.FCurrencyPair.Select01("currency1 = '%s' and currency2 = '%s'"%(currency1, currency2), None)
            if not ccy_pair:
                ccy_pair = acm.FCurrencyPair.Select01("currency1 = '%s' and currency2 = '%s'"%(currency2, currency1), None)
            if ccy_pair:
                if is_settle_ccy_major(trade):
                    weBuyer = True
    elif ins_type == 'CurrSwap':
        leg=trade.Instrument().Legs()[0]
        pay_leg = None
        receive_leg = None
        if leg.PayLeg():
            pay_leg = leg
            receive_leg = trade.Instrument().Legs()[1]
        else:
            pay_leg=trade.Instrument().Legs()[1]
            receive_leg=leg
        if receive_leg.Currency().Name() < pay_leg.Currency().Name():
            if trade.Nominal() > 0:
                weBuyer = True
        else:
            if trade.Nominal() < 0:
                weBuyer = True
    elif ins_type == 'Curr':
        if trade.BaseCostDirty() > 0 or trade.Nominal() > 0:
            weBuyer = True
    elif ins_type == 'FXOptionDatedFwd':
        if trade.Quantity() < 0:
            weBuyer = True
    elif ins_type in ['BasketRepo/Reverse', 'BasketSecurityLoan', 'Portfolio Swap']:        
        if trade.Quantity() > 0:
            weBuyer = True  
    elif ins_type == 'Deposit':
        if trade.Nominal() < 0:
            weBuyer = True  
    else:
        if trade.Nominal() > 0:
            weBuyer = True
    return weBuyer

def get_uti_from_trade_attribute(trade):
    uti = None
    try:
        uti = trade.UniqueTradeIdentifier()
    except:#it means that this attribute is not present on trade because it is being run on a lower version of acm
        pass
    if not uti:
        FRegulatoryLogger.INFO(logger, "UniqueTradeIdentifier is not present on trade <%d>"%trade.Oid())
    return uti

def get_uti_from_trade_alais(trade):
    uti = None
    try:
        aliasType = 'UTI'
        aliases = acm.FTradeAlias.Select("type = '%s' and trade = %d"%(aliasType, trade.Oid()))
        if aliases:
            uti = aliases[0].Alias()
        if not uti:
            FRegulatoryLogger.INFO(logger, "UTI TradeAlias is not present on trade <%d>"%trade.Oid())
    except Exception as e:
        FRegulatoryLogger.ERROR(logger, "Error in get_uti_from_trade_alais. Error: <%s>"%str(e))
    return uti

def get_uti_from_trade_addinfo(trade):
    uti = None
    try:
        uti = trade.AdditionalInfo().UTI_1part() + trade.AdditionalInfo().UTI_2part()
        return uti
    except:#it means these AddInfos are not present on the trade
        pass

def get_check_sum(str_val):
    checkSum = None
    numeric_val = getNumericConversion(str_val)
    numeric_val = numeric_val + '00'
    checkSum = str(98 - int(numeric_val) % 97)
    return checkSum

def is_valid_check_sum(str_val):
    b_correct_check_sum = False
    if str_val[-2:] == get_check_sum(str_val[:-2]):
        b_correct_check_sum = True
    if not b_correct_check_sum and str_val[-1:] == get_check_sum(str_val[:-1]):
        b_correct_check_sum = True
    return b_correct_check_sum

def getNumericConversion(lei_val):
    numeric_lei = ''
    if not lei_val.isdigit():
        for each_char in lei_val:
            if each_char.isalpha():
                numeric_lei += str(ord(each_char.upper()) - 55)
            elif each_char.isdigit():
                numeric_lei += each_char
    else:
        numeric_lei = lei_val
    return numeric_lei

def isValidLEI(lei_val, expected_len = 20):
    'Verify that lei follows ISO7064 and last two digits are check digits'
    bValidLei = False
    msg = None
    if len(lei_val) == expected_len:
        check_sum_val = lei_val[-2:]
        if check_sum_val.isdigit():
            numeric_lei = getNumericConversion(lei_val)
            if int(numeric_lei) % 97 == 1:
                bValidLei = True
            else:
                msg = "the checkSum is incorrect."
        else:
            msg = "the last 2 characters are not numeric."
    else:
        msg = "it is of length <%d> characters. The expected length is <%d> characters."%(len(lei_val), expected_len)
    if not bValidLei:
        log_msg = 'The given LEI <%s> is invalid as '%lei_val 
        log_msg = log_msg + msg
        FRegulatoryLogger.INFO(logger, log_msg)
    return bValidLei

def generateLEIWithCheckSum(lei_val, expected_len = 18):
    """generate the checkSum for the given lei"""
    checkSum = None
    if len(lei_val) == expected_len:
        numeric_lei = ''
        if lei_val.isalnum():
            checkSum = get_check_sum(lei_val)
        else:
            raise Exception("The provided lei <%s> is not a valid alphanumeric value."%lei_val)
    else:
        raise Exception("Wrong length with <%d> characters for lei <%s>. Expected length to generate checkSum is <%d> characters."%(len(lei_val), lei_val, expected_len))
    return lei_val + checkSum, checkSum

def isValidIsin(isin_val):
    """verify that ISIN structure is valid, and checksum correct"""
    bValidISIN = False
    if isin_val:
        isin_val = isin_val.strip().upper()
        charmap = dict([(i, ord(i)-55) for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'] + [(i, int(i)) for i in '0123456789'])
        if re.match('^([A-Z][A-Z])([A-Z0-9]{9}\d)$', isin_val):
            try:
                sum_digits_str = ''.join([str(charmap[each_char]) for each_char in isin_val[:11]])
                total_sum = 0
                parity = len(sum_digits_str) % 2
                for n, c in enumerate(sum_digits_str):
                    a = int(c)
                    if n % 2 != parity:
                        a = a * 2
                    total_sum += a / 10
                    total_sum += a % 10
                check_digit = (10 - (total_sum % 10)) % 10
                if isin_val[11] == str(check_digit):
                    bValidISIN = True
            except KeyError:
                pass
    return bValidISIN

def getPartyFromLEI(lei_val):
    party_obj = None
    if lei_val:
        party_obj = acm.FParty.Select01("legalEntityId = '%s'"%lei_val, None)
    return party_obj
        
def getPartyFromMIC(mic_val):
    party_obj = None
    alias_obj = None    
    alias_typ_spec = acm.FPartyAliasType['MIC']
    if not alias_typ_spec:
        raise Exception('<MIC> is not a valid PartyAliasType')
    else:
        alias_obj = acm.FPartyAlias.Select01("type=%d and name = '%s'"%(alias_typ_spec.Oid(), mic_val), None)
    if alias_obj:
        party_obj = alias_obj.Party()
    return party_obj

def check_sum(utiVal):
    """generate check sum for a UTI"""
    if utiVal:
        utiVal = utiVal + get_check_sum(utiVal)
    return utiVal

def upi(instrument):
    return ""

def get_lei(party):
    parent_list = []
    lei = ''
    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.1:
        lei = party.LEI()
        if lei:
            FRegulatoryLogger.DEBUG(logger, "Party LEI <%s> being directly picked up for party <%s>"%(lei, party.Name()))
    if not lei:
        lei = party.LegalEntityId()
        orig_party = party
        if not lei:
            if party.Parent():
                    while party.Parent() and not lei:
                        if party.Parent().Name() not in parent_list:
                            parent_list.append(party.Parent().Name())
                            party = party.Parent()
                            lei = party.LegalEntityId()
                            if lei:
                                FRegulatoryLogger.DEBUG(logger, "The LEI <%s> being selected for party <%s> is from parent <%s> in its hierarchy"%(lei, orig_party.Name(), party.Name()))
                        else:
                            FRegulatoryLogger.ERROR(logger, "The LEI for party <%s> cannot be determined as there is a cyclic dependency upon it."%(orig_party.Name()))
                            break
    return lei

def tech_record_identification(trade):
    """function that returns the technical record identification if present on the trade. If not present, it generates and returns this value"""
    tech_record_identification = ''
    if trade:
        lei = ''
        reporting_entity = trade.RegulatoryInfo().ReportingEntity()
        if reporting_entity:
            lei = get_lei(reporting_entity)
        value_day = (ael.date_from_string(trade.ValueDay())).to_string(ael.DATE_ISO)
        value_day = value_day.replace('-', '')
        buff = ''
        if len(lei + value_day + str(trade.Oid())) < 35:
            buff_len = 35 - len(lei + value_day + str(trade.Oid()))
            buff = '0' * buff_len
        tech_record_identification = lei + value_day + buff + str(trade.Oid())
        tech_record_identification = tech_record_identification[0:35]
    return tech_record_identification

def get_regulatory_instance(add_info_recs):
    acm_object = None
    if add_info_recs:
        if len(add_info_recs) > 1:
            pass
            #FRegulatoryLogger.WARN(logger, "There are multiple records with the value <%s> on <%s>. Returning the first found instance."%(str(add_info_recs[0].FieldValue()), add_info_recs[0].RecType()))
        add_info_rec = add_info_recs[0]
        recType = None
        try:
            recType = add_info_rec.RecType()
        except:#this condition is hit for versions below 15.3 where the RecType function was not directly available on the AddInfo object
            recType = add_info_rec.AddInf().RecType() 
        if recType == 'Contact':
            acm_object = acm.FContact[add_info_rec.Recaddr()]
        elif recType == 'Party':
            acm_object = acm.FParty[add_info_rec.Recaddr()]
    return acm_object

def getObjectFromCrmId(crm_id):
    acm_object = None
    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5:
        acm_object = acm.FPerson.Select01("crmId  = '%s'"%crm_id, None)
    if not acm_object:
        add_info_recs = acm.FAdditionalInfo.Select("addInf=%d and fieldValue ='%s'"\
                    %(acm.FAdditionalInfoSpec['regContactCrmId'].Oid(),  crm_id)) 
        acm_object = get_regulatory_instance(add_info_recs)
    if not acm_object:
        add_info_recs = acm.FAdditionalInfo.Select("addInf=%d and fieldValue ='%s'"\
                    %(acm.FAdditionalInfoSpec['regPtyCrmId'].Oid(),  crm_id)) 
        acm_object = get_regulatory_instance(add_info_recs)
    return acm_object

def getObjectFromExchangeId(exchange_id):
    acm_object = None
    try:
        if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.2:
            acm_object = acm.FPerson.Select01("exchangeId  = %d"%exchange_id, None)
        if not acm_object:
            add_info_recs = acm.FAdditionalInfo.Select('addInf=%d and fieldValue =%d'\
                        %(acm.FAdditionalInfoSpec['regContExchangeId'].Oid(),  int(exchange_id))) 
            acm_object = get_regulatory_instance(add_info_recs)
        if not acm_object:
            add_info_recs = acm.FAdditionalInfo.Select('addInf=%d and fieldValue =%d'\
                        %(acm.FAdditionalInfoSpec['regPtyExchangeId'].Oid(),  int(exchange_id)))
            acm_object = get_regulatory_instance(add_info_recs)
    except ValueError as e:
        raise ValueError("Kindly provide a valid value for the ExchangeId. %s"%e)
    return acm_object

rts_28_ins_type_dict = {
    'Stock': 'Equities - Shares & Depositary Receipts',
    'Depositary Receipt': 'Equities - Shares & Depositary Receipts',
    'ETF': 'Exchange traded products (Exchange traded funds, exchange traded notes and exchange traded commodities)',
    'MBS/ABS': 'Structured finance instruments', 
    'CLN': 'Structured finance instruments',
    'Bill': 'Debt instruments - Money markets instruments',
    'IndexLinkedBond': 'Debt instruments - Bonds',
    'DualCurrBond': 'Debt instruments - Bonds',
    'Convertible': 'Other instruments',
    'Flexi Bond': 'Other instruments',
    'Warrant': 'Securitized Derivatives - Warrants and Certificate Derivatives',
    'Rolling Schedule': 'Commodities derivatives and emission allowances Derivatives - Other commodities derivatives and emission allowances derivatives',
    'Swap': 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives',
    'CurrSwap': 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives',
    'IndexLinkedSwap': 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives',
    'FRA': 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives',
    'Cap': 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue',
    'Floor': 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue',
    'PriceSwap': 'Commodities derivatives and emission allowances Derivatives - Other commodities derivatives and emission allowances derivatives', 
    'CreditDefaultSwap': 'Credit Derivatives - Other credit derivatives',
    'Bond': 'DERIVE_FROM_TENOR',
    'FRN': 'DERIVE_FROM_TENOR',
    'PromisLoan': 'DERIVE_FROM_TENOR',
    'Zero': 'DERIVE_FROM_TENOR',
}


'''
def get_rts28(instrument):
    cfi_code = instrument.RegulatoryInfo().CfiCode()
    if not cfi_code:
        cfi_code = FRegulatoryCfiCodeGeneration.compute_cfi_code(instrument) 
    rts28_ins_type = get_rts28_from_cfi_code(cfi_code)
    return rts28_ins_type
'''

def __derive_rts28_from_tenor(instrument):
    rts_28_ins_type = 'Debt instruments - Bonds'
    if instrument.Issuer() and instrument.Issuer().BusinessStatus() and 'MUNICIPAL' in instrument.Issuer().BusinessStatus().Name().upper():
        pass
    else:
        tenure = FRegulatoryCfiCodeGeneration.get_tenure(instrument)
        if tenure <= 366:
            rts_28_ins_type = 'Debt instruments - Money markets instruments'
    return rts_28_ins_type

def get_rts28(instrument, rts28_lookup_dict = None, base_instrument = False, counter = 0):
    if not rts28_lookup_dict:
        rts28_lookup_dict = rts_28_ins_type_dict
    rts_28_ins_type = 'Other instruments'
    
    if instrument.InsType() in rts28_lookup_dict:
        counter = counter + 1
        val = rts28_lookup_dict[instrument.InsType()]
        if val == 'DERIVE_FROM_TENOR':
            rts_28_ins_type = __derive_rts28_from_tenor(instrument)
        else:
            rts_28_ins_type = rts28_lookup_dict[instrument.InsType()]
    else:
        if instrument.InsType() in ['Option']:
            if not FRegulatoryCfiCodeGeneration.is_otc_option(instrument):
                if instrument.Underlying().InsType() in ['Curr']:
                    rts_28_ins_type = 'Currency derivatives - Futures and options admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Cap', 'Floor']:
                    rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['FRA']:
                    rts_28_ins_type = 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives'
                elif instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
                    rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Average Future/Forward',]:
                    rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                
            else:
                if instrument.Underlying().InsType() in ['CreditDefaultSwap', 'CLN']:
                    rts_28_ins_type = 'Credit Derivatives - Futures and options admitted to trading on a trading venue'
                elif instrument.Underlying() and instrument.Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt', 'Dividend Point Index'] or \
                    (instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock', 'EquityIndex']) or \
                    (instrument.Underlying() and instrument.Underlying().InsType() in ['VarianceSwap'] and \
                    instrument.Underlying().Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt',]) or \
                    (instrument.Underlying() and instrument.Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt', 'Dividend Point Index']) or \
                    (instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock', 'EquityIndex']) or \
                    (instrument.Underlying() and instrument.Underlying().InsType() in ['Option', 'Warrant', 'CFD'] and instrument.Underlying().Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt', 'Dividend Point Index'] or \
                    (instrument.Underlying() and instrument.Underlying().Underlying() and instrument.Underlying().Underlying().InsType() in ['CFD'] and \
                    instrument.Underlying().Underlying().Underlying().InsType() in ['Stock', 'EquityIndex'])) or \
                    (instrument.Underlying() and instrument.Underlying().InsType() in ['Future/Forward'] and instrument.Underlying().Underlying().InsType() in ['Dividend Point Index', 'EquityIndex', 'Stock', 'Depositary Receipt']):
                    rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Curr'] or (instrument.Underlying().Underlying() and instrument.Underlying().Underlying().InsType() in ['Curr']):
                    rts_28_ins_type = 'Currency derivatives - Futures and options admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Bill', 'Bond', 'FRN', 'Convertible', 'Deposit',  'Zero', 'PromisLoan', 'Swap', \
                        'IndexLinkedSwap', 'Cap', 'Floor', 'FRA', 'CurrSwap', 'RateIndex'] or (instrument.Underlying().Underlying() and instrument.Underlying().Underlying().InsType() in \
                        ['Bill', 'Bond', 'Convertible', 'Deposit', 'FRA', 'FRN', 'RateIndex', 'Zero', 'IndexLinkedBond', 'Swap', 'PromisLoan']):
                    rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', 'Average Future/Forward'] or \
                    (instrument.Underlying().Underlying() and instrument.Underlying().Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', 'Average Future/Forward']):
                        rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Future/Forward']:
                    underlyer = instrument.Underlying().Underlying()
                    if underlyer.InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Variant', 'Commodity Index']:
                        rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                    elif underlyer.InsType() in ['Bill', 'Bond', 'Convertible', 'Deposit', 'FRA', 'FRN', 'RateIndex', 'Zero', 'IndexLinkedBond', 'Swap', 'PromisLoan']:
                        rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
                    elif underlyer.InsType() in ['Combination']:
                        code = FRegulatoryCfiCodeGeneration.get_combination_classification_char(underlyer)
                        if code == 'T':
                            rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                        elif code == 'E':
                            rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                        elif code == 'C':
                            rts_28_ins_type = 'Credit Derivatives - Futures and options admitted to trading on a trading venue'
                        elif code == 'F':
                            rts_28_ins_type = 'Currency derivatives - Futures and options admitted to trading on a trading venue'
                        elif code == 'R':
                            rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
                    elif underlyer.InsType() in ['CreditDefaultSwap', 'CLN', ]:
                        rts_28_ins_type = 'Credit Derivatives - Futures and options admitted to trading on a trading venue'
                    elif underlyer.InsType() in ['Curr']:
                        rts_28_ins_type = 'Currency derivatives - Futures and options admitted to trading on a trading venue'
                    elif underlyer.InsType() in ['Dividend Point Index', 'EquityIndex', 'Stock', 'Depositary Receipt']:
                        rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                elif instrument.Underlying().InsType() in ['Combination', 'TotalReturnSwap']:
                    code = None
                    if instrument.Underlying().InsType() in ['Combination']:
                        code = FRegulatoryCfiCodeGeneration.get_combination_classification_char(instrument.Underlying())
                    else:
                        for leg in instrument.Underlying().Legs():
                            if leg.LegType() == 'Total Return':
                                code = FRegulatoryCfiCodeGeneration.get_TRS_float_rate_ref_classification(leg.FloatRateReference())
                                break
                    if code == 'T':
                        rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                    elif code == 'E':
                        rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                    elif code == 'C':
                        rts_28_ins_type = 'Credit Derivatives - Futures and options admitted to trading on a trading venue'
                    elif code == 'F':
                        rts_28_ins_type = 'Currency derivatives - Futures and options admitted to trading on a trading venue'
                    elif code == 'R':
                        rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
        elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward', 'CFD']:
            if (not instrument.Otc()):
                if instrument.InsType() in ['Average Future/Forward']:
                    rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                if instrument.Underlying() and instrument.Underlying().InsType() in ['Combination']:
                    if FRegulatoryCfiCodeGeneration.get_combination_classification(instrument.Underlying())[1]:
                        rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue'
                    else:
                        rts_28_ins_type = 'Other instruments'
                elif instrument.Underlying() and instrument.Underlying().InsType() in ['ETF', 'Bill', 'Bond', 'FRN', 'Convertible', \
                    'Deposit', 'Zero', 'PromisLoan', 'IndexLinkedBond', 'EquityIndex', 'Commodity Index', \
                    'Dividend Point Index', 'Average Future/Forward', 'Commodity', 'Commodity Variant']:
                    rts_28_ins_type = 'Other instruments'
                elif instrument.Underlying() and instrument.Underlying().InsType() in ['Curr']:
                    rts_28_ins_type = 'Currency derivatives - Swaps, forwards, and other currency derivatives'
                elif instrument.Underlying() and instrument.Underlying().InsType() in ['RateIndex']:
                    rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
                elif instrument.Underlying() and instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
                    rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
            else:
                underlyer = None
                if instrument.InsType() == 'Average Future/Forward':
                    underlyer = instrument.Legs()[0].FloatRateReference()
                else:
                    underlyer = instrument.Underlying()
                if underlyer.InsType() in ['CreditDefaultSwap', 'CLN']:
                    rts_28_ins_type = 'Credit Derivatives - Futures and options admitted to trading on a trading venue'
                elif (underlyer.InsType() in ['Stock', 'EquityIndex', 'Dividend Point Index', 'Depositary Receipt']) or \
                        (instrument.InsType() in ['CFD'] and underlyer.InsType() in ['Stock', 'EquityIndex']):
                    rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                    if instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock', 'EquityIndex'] and (instrument.Otc()):
                        rts_28_ins_type = 'Contracts for difference'
                elif underlyer.InsType() in ['Curr']:
                    rts_28_ins_type = 'Currency derivatives - Swaps, forwards, and other currency derivatives'
                elif underlyer.InsType() in ['RateIndex', 'Bill', 'Bond', 'FRN', 'Deposit', 'Zero', 'PromisLoan', 'FRA', 'IndexLinkedBond', 'Convertible', 'Swap']:
                    rts_28_ins_type = 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives'
                elif underlyer.InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', \
                                            'Average Future/Forward', 'Precious Metal Rate', 'Rolling Schedule']:
                    rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Other commodities derivatives and emission allowances derivatives'
                elif underlyer.InsType() in ['CFD'] and underlyer.Underlying().InsType() in ['Stock', 'EquityIndex'] and (instrument.Otc()):
                    rts_28_ins_type = 'Contracts for difference'
                elif underlyer.InsType() in ['Combination']:
                    code = FRegulatoryCfiCodeGeneration.get_combination_classification_char(underlyer)
                    if code == 'T':
                        rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Other commodities derivatives and emission allowances derivatives'
                    elif code == 'E':
                        rts_28_ins_type = 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'
                    elif code == 'C':
                        rts_28_ins_type = 'Credit Derivatives - Futures and options admitted to trading on a trading venue'
                    elif code == 'F':
                        rts_28_ins_type = 'Currency derivatives - Swaps, forwards, and other currency derivatives'
                    elif code == 'R':
                        rts_28_ins_type = 'Interest Rates Derivatives - Futures and options admitted to trading on a trading venue'
        elif instrument.InsType() in ['TotalReturnSwap']:
            classification_char = None
            for leg in instrument.Legs():
                if leg.LegType() == 'Total Return':
                    classification_char = FRegulatoryCfiCodeGeneration.get_TRS_float_rate_ref_classification(leg.FloatRateReference())
                    if classification_char == 'C':
                        rts_28_ins_type = 'Credit Derivatives - Other credit derivatives'
                    elif classification_char == 'E':
                        rts_28_ins_type = 'Equity Derivatives - Swaps and other equity derivatives'
                    elif classification_char == 'R':
                        rts_28_ins_type = 'Interest Rates Derivatives - Swaps, forwards, and other interest rates derivatives'
                    elif classification_char == 'T':
                        rts_28_ins_type = 'Commodities derivatives and emission allowances Derivatives - Other commodities derivatives and emission allowances derivatives'
                    elif classification_char == 'F':
                        rts_28_ins_type = 'Currency derivatives - Swaps, forwards, and other currency derivatives'
        elif instrument.InsType() in ['VarianceSwap', 'VolatilitySwap']:
            rts_28_ins_type = 'Other instruments'
            if instrument.Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt'] or \
                (instrument.Underlying().InsType() in ['Combination'] and FRegulatoryCfiCodeGeneration.get_combination_classification(instrument.Underlying())[0]):
                rts_28_ins_type = 'Equity Derivatives - Swaps and other equity derivatives'
    return rts_28_ins_type

def get_rts28_from_cfi_code(cfi_code):
    counter = 0
    cfi_char_dict = FRegulatoryLookup.cfi_char_dict
    rts28_ins_type = None
    try:
        while not rts28_ins_type:
            if cfi_code[counter] in cfi_char_dict:
                key_val = cfi_code[counter]
            else:
                key_val = '*'
            dict_val = cfi_char_dict[key_val]
            if isinstance(dict_val, str):
                rts28_ins_type = dict_val
            else:
                cfi_char_dict = dict_val
                counter = counter + 1
    except:
        pass
    if not rts28_ins_type:
        rts28_ins_type = 'Other instruments'
    return rts28_ins_type

def their_org(trade):
    their_org = None
    import FRegulatoryLib
    if trade.RegulatoryInfo().TheirOrganisation():
        lei = FRegulatoryLib.PartyRegInfo(trade.RegulatoryInfo().TheirOrganisation()).LEI()
        if lei:
            their_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
        if their_org:
            if their_org != trade.RegulatoryInfo().TheirOrganisation():
                FRegulatoryLogger.INFO(logger, "TheirOrganisation <%s> on trade <%d> does not have an LEI on it. Hence TheirOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                trade.RegulatoryInfo().TheirOrganisation().Name(), trade.Oid(), their_org.Name(), trade.RegulatoryInfo().TheirOrganisation().Name()))
        else:
            FRegulatoryLogger.INFO(logger, "No LEI found on TheirOrganisation <%s>. Hence verifying Counterparty"%trade.RegulatoryInfo().TheirOrganisation().Name())
    if (not their_org) and trade.Counterparty():
        lei = FRegulatoryLib.PartyRegInfo(trade.Counterparty()).LEI()
        if lei:
            their_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
        if their_org:
            if their_org != trade.Counterparty():
                FRegulatoryLogger.INFO(logger, "Counterparty <%s> on trade <%d> does not have an LEI on it. Hence TheirOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                trade.Counterparty().Name(), trade.Oid(), their_org.Name(), trade.Counterparty().Name()))
    if not their_org:
        FRegulatoryLogger.INFO(logger, "Neither TheirOrganisation nor Counterparty are set on the trade or do not have LEI. Hence TheirOrg is None")
    return their_org

def our_org(trade):
    our_org = None
    import FRegulatoryLib
    if trade.RegulatoryInfo().OurOrganisation():
        lei = FRegulatoryLib.PartyRegInfo(trade.RegulatoryInfo().OurOrganisation()).LEI()
        if lei:
            our_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
        if our_org:
            if our_org != trade.RegulatoryInfo().OurOrganisation():
                FRegulatoryLogger.INFO(logger, "OurOrganisation <%s> on trade <%d> does not have an LEI on it. Hence OurOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                trade.RegulatoryInfo().OurOrganisation().Name(), trade.Oid(), our_org.Name(), trade.RegulatoryInfo().OurOrganisation().Name()))
        else:
            FRegulatoryLogger.INFO(logger, "No LEI found on OurOrganisation <%s>. Hence verifying Acquirer"%trade.RegulatoryInfo().OurOrganisation().Name())
    if (not our_org) and trade.Acquirer():
        lei = FRegulatoryLib.PartyRegInfo(trade.Acquirer()).LEI()
        if lei:
            our_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
        if our_org:
            if our_org != trade.Acquirer():
                FRegulatoryLogger.INFO(logger, "Acquirer <%s> on trade <%d> does not have an LEI on it. Hence OurOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                trade.Acquirer().Name(), trade.Oid(), our_org.Name(), trade.Acquirer().Name()))
    if not our_org:
        FRegulatoryLogger.INFO(logger, "Neither OurOrganisation nor Acquirer are set on the trade or do not have LEI. Hence OurOrg is None")
    return our_org

def get_swap_type(instrument):
    float_leg_counter = 0
    fixed_leg_counter = 0
    swap_type = None
    for leg in instrument.Legs():
        if leg.LegType() in ['Fixed', 'Fixed Accretive', 'Zero Coupon Fixed']:
            fixed_leg_counter = fixed_leg_counter + 1
        elif leg.LegType() in ['Float', 'Total Return']:
            float_leg_counter = float_leg_counter + 1
    if float_leg_counter == 2:
        swap_type = 'Basis Swap'
    elif float_leg_counter == 1 and fixed_leg_counter == 1:
        swap_type = 'Vanilla Swap'
    if fixed_leg_counter == 2:
        swap_type = 'Fixed Fixed Swap'
    return swap_type

def set_rating(acm_object, rating_name, rating_val):
    choicelist = acm.FChoiceList.Select01("list = 'Ratings' and name = '%s'"%rating_name, None)
    if choicelist:
        sort_order = choicelist.SortOrder()
        try:
            if acm_object.IsKindOf(acm.FParty):
                eval('acm_object.Rating' + str(sort_order) + '(' + str(rating_val) +')')
            elif acm_object.IsKindOf(acm.FInstrument):
                eval('acm_object.Rating' + str(sort_order) + 'ChlItem(' + str(rating_val) +')')
        except:
            pass

def get_rating(acm_object, rating_name):
    """return the rating value on the acm object requested"""
    rating_val = None
    choicelist = acm.FChoiceList.Select01("list = 'Ratings' and name = '%s'"%rating_name, None)
    if choicelist:
        sort_order = choicelist.SortOrder()
        try:
            if acm_object.IsKindOf(acm.FParty):
                rating_val = eval('acm_object.Rating' + str(sort_order) + '()')
            elif acm_object.IsKindOf(acm.FInstrument):
                rating_val = eval('acm_object.Rating' + str(sort_order) + 'ChlItem()')
        except:
            pass
    return rating_val

    
