"""------------------------------------------------------------------------
MODULE
    FRegulatoryISITICCode -
DESCRIPTION:
    This file consists the approach to infer the ISITIC classification code for the given instrument
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import FRegulatoryLogger
logger = 'FRegulatoryISITICCode'
ins_type_isitc_code = {        'Option':   'OPT',
                               'Warrant':   'WAR',
                               'FRN':   'FRN',
                               'CD':   'CD',
                               'Deposit':   'TD',
                               'FRA':   'FRA',
                               'Swap':   'NULL',
                               'CurrSwap':   'NULL',
                               'Cap':   'NULL',
                               'Floor':   'NULL',
                               'Curr':   'NULL',
                               'EquityIndex':   'NULL',
                               'RateIndex':   'NULL',
                               'SecurityLoan':   'NULL',
                               'BuySellback':   'NULL',
                               'PriceIndex':   'NULL',
                               'TotalReturnSwap':   'NULL',
                               'CreditDefaultSwap':   'NULL',
                               'Commodity':   'NULL',
                               'UnKnown':   'NULL',
                               'CLN':   'NULL',
                               'BasketRepo/Reverse':   'NULL',
                               'CreditIndex':   'NULL',
                               'IndexLinkedSwap':   'NULL',
                               'BasketSecurityLoan':   'NULL',
                               'CFD':   'NULL',
                               'VarianceSwap':   'NULL',
                               'Depositary Receipt':   'NULL',
                               'FXOptionDatedFwd':   'NULL',
                               'Portfolio Swap':   'NULL',
                               'ETF':   'ETF',
                               'Stock':   'FUNCTION', 
                               'Bond':   'FUNCTION',
                               'Future/Forward':   'FUNCTION',
                               'Zero':   'FUNCTION',
                               'Bill':   'FUNCTION',
                               'Convertible':   'FUNCTION',
                               'Repo/Reverse':   'FUNCTION',
                               'IndexLinkedBond':   'FUNCTION',
                               'DualCurrBond':   'FUNCTION',
                               'Fund':   'MF',
                               'Depositary Receipt':   'CS',
                               'Flexi Bond':   'FUNCTION',
                               'Average Future/Forward':   'FUNCTION',
                               'Curr':   'FUNCTION',
                               'MBS/ABS':   'FUNCTION',
                               }
class ISITCodeType(object):
    def __init__(self, acm_object):
        self.__trade = None
        self.__instrument = None
        try:
            if acm_object and acm_object.IsKindOf('FTrade'):
                self.__trade = acm_object
                self.__instrument = acm_object.Instrument()
            elif acm_object and acm_object.IsKindOf('FInstrument'):
                self.__instrument = acm_object.Instrument()
            else:
                FRegulatoryLogger.WARN(logger, "Please provide the valid acm object either of FTrade or FInstrument type")
        except Exception as e:
            FRegulatoryLogger.ERROR(logger, "Please provide the valid acm object either of FTrade or FInstrument type")

    def get_isitic_classification(self):
        """get the isitic classification for a given instrument"""
        ins_type = None
        if self.__instrument:
            ins_type = self.__instrument.InsType()
        elif self.__trade:
            ins_type = self.__trade.Instrument().InsType()
        isitc_classification_code = None
        if ins_type in ins_type_isitc_code:
            isitc_classification_code = ins_type_isitc_code[ins_type]
        if isitc_classification_code == 'FUNCTION':
            function_call = ins_type.replace('/', '_')
            function_call = function_call.replace(' ', '_')
            isitc_classification_code = eval('self.' + function_call + '()')
        if isitc_classification_code and isitc_classification_code == 'NULL':
            isitc_classification_code = None
        return isitc_classification_code

    def __get_provider_data(self, field_name):
        """get the provider data if available for the given field name"""
        field_value = None
        try:
            field_value = self.__instrument.GetProviderDataFieldValue('Bloomberg', field_name)
        except:
            FRegulatoryLogger.DEBUG(logger, "DataLoader Bloomberg needs to be installed to get the %s."%field_name)
        return field_value

    def MUTUAL_FUND(self):
        """infer the isitc code for mutual fund based on the SECURITY_TYP field in Provider data"""
        isitic_code = None
        security_type = self.__get_provider_data('SECURITY_TYP')
        if security_type:
            if security_type == 'ETP':
                isitic_code = 'ETF'
        else:
            isitic_code = 'MF'
        return isitic_code

    def Stock(self):
        """infer the isitc code for Stock instrument type"""
        Stock_dict =  { 'PFD'       :       'PS', 
                        'EQUITY'    :       {'PREFERENCE'           : 'PS',
                                             'PREFERRED STOCK'      : 'PS', 
                                             'RIGHT'                : 'RTS',
                                             'COMMON STOCK'         : 'CS', 
                                             'MUTUAL FUND'          : 'FUNCTION',
                                             'WARRANT'              : 'WAR'}
              }
        isitic_code = 'CS'
        market_sec = self.__get_provider_data('MARKET_SECTOR_DES')
        if market_sec:
            if market_sec.upper() in Stock_dict:
                sec_type2 = Stock_dict[market_sec.upper()]
                if isinstance(sec_type2, dict):
                    sec_type = self.__get_provider_data('SECURITY_TYP2')
                    if sec_type and sec_type.upper() in sec_type2:
                        isitic_code = sec_type2[sec_type.upper()]
                        if isitic_code == 'FUNCTION':
                            function_name = sec_type.replace(' ', '_')
                            isitic_code = eval('self.' + function_name.upper() + '()')
                else:
                    isitic_code =  sec_type2
        return isitic_code

    def Future_Forward(self):
        """infer the isitc code for Futute/Forward instrument type"""
        isitic_code = None
        if self.__instrument:
            if self.__instrument.PayType() == 'Future':
                isitic_code = 'FUT'
            elif self.__instrument.PayType() == 'Forward':
                if self.__instrument.Underlying().InsType() == 'Bond':
                    isitic_code = 'BFW'
        elif self.__trade:
            if self.__trade.Instrument().Underlying().InsType() == 'Curr':
                isitic_code = 'FXF'
        return isitic_code

    def Bond(self):
        """infer the isitc code for Bond instrument type"""
        isitic_code = None
        floater = self.__get_provider_data('FLOATER')
        if floater and floater != 'Y':
            isitic_code = self.__isitic_from_market_sector()
        if not isitic_code:
            security_type2 = self.__get_provider_data('SECURITY_TYP2')
            security_type = self.__get_provider_data('SECURITY_TYP')
            if security_type2 and security_type2.upper() == 'NOTE' and security_type and security_type.upper() == 'US GOVERNMENT':
                isitic_code = 'TN'
        if not isitic_code:
            isitic_code = self.__get_isitic_from_issuer_bis()
        return isitic_code

    def __get_isitic_from_mkt_sector_issuer_bis(self):
        """infer the isitc code on the basis of market sector or issuer on the instrument"""
        isitic_code = self.__isitic_from_market_sector()
        if not isitic_code:
            isitic_code = self.__get_isitic_from_issuer_bis()
        return isitic_code

    def __get_isitic_from_issuer_bis(self):
        """infer the isitc code on the basis of the issuer on the instrument"""
        isitic_code = None
        if self.__instrument.Issuer():
            if self.__instrument.Issuer().BisStatus() in ['OECD Government',  'Non-OECD Government']:
                isitic_code = 'GOVT'
            else:
                isitic_code = 'CORP'
        return isitic_code

    def Zero(self):
        """infer the isitc code for Zero instrument type"""
        isitic_code = None
        zero_coupon = self.__get_provider_data('ZERO_CPN')
        if zero_coupon and zero_coupon == 'Y':
            isitic_code = self.__isitic_from_market_sector()
        if not isitic_code:
            isitic_code = self.__get_isitic_from_issuer_bis()
        return isitic_code

    def Bill(self):
        """infer the isitc code for Bill instrument type"""
        isitic_code = None
        security_type = self.__get_provider_data('SECURITY_TYP')
        security_type2 = self.__get_provider_data('SECURITY_TYP2')
        if security_type and security_type.upper() == 'US GOVERNMENT' and security_type2 and security_type2.upper() == 'BILL':
            isitic_code = 'USTB'
        if (not isitic_code) and self.__instrument.Currency().Name() == 'USD' and \
            self.__instrument.Issuer() and \
            self.__instrument.Issuer().BisStatus() in ['OECD Government',  'Non-OECD Government']:
            isitic_code = 'USTB'
        return isitic_code

    def Convertible(self):
        """infer the isitc code for Convertible instrument type"""
        isitic_code = None
        convertible = self.__get_provider_data('CONVERTIBLE')
        if convertible and convertible == 'Y':
            isitic_code = self.__isitic_from_market_sector()
        if not isitic_code:
            isitic_code = self.__get_isitic_from_issuer_bis()
        return isitic_code

    def __isitic_from_market_sector(self):
        """infer the isitc code on the basis of the market sector des available in provider data"""
        isitic_code = None
        market_sec = self.__get_provider_data('MARKET_SECTOR_DES')
        isitic_lookup = {'CORP' : 'CORP', 'MUNI' : 'MUNI', 'GOVT' : 'GOVT'}
        if market_sec and market_sec.upper() in isitic_lookup:
            isitic_code = isitic_lookup[market_sec.upper()]
        return isitic_code

    def IndexLinkedBond(self):
        """infer the isitc code for IndexLinkedBond instrument type"""
        isitic_code = None
        inflation_lined_indicator = self.__get_provider_data('INFLATION_LINKED_INDICATOR')
        if inflation_lined_indicator and inflation_lined_indicator == 'Y':
            isitic_code = self.__isitic_from_market_sector()
        if not isitic_code:
            isitic_code = self.__get_isitic_from_issuer_bis()
        return isitic_code

    def DualCurrBond(self):
        """infer the isitc code for DualCurrBond instrument type"""
        return self.__get_isitic_from_mkt_sector_issuer_bis()

    def MBS_ABS(self):
        """infer the isitc code for MBS/ABS instrument type"""
        isitic_code = None
        security_type2 = self.__get_provider_data('SECURITY_TYP2')
        secutiry_type2_dict = { 'RMBS CDO'              :      'CDO',
                                'MEZZ DEBT CDO'         :      'CDO',
                                'IG DEBT CDO'           :      'CDO',
                                'HY DEBT CDO'           :      'CDO',
                                'EM DEBT CDO'           :      'CDO',
                                'CDS-CRP CDO'           :      'CDO',
                                'CDS-ABS CDO'           :      'CDO',
                                'CDS CDO'               :      'CDO',
                                'CDO SQUARE'            :      'CDO',
                                'MEZZ ABS CDO'          :      'CDO',
                                'HIGH GRADE ABS CDO'    :      'CDO',
                                'ABS CDO'               :      'CDO',
                                'CLO'                   :      'CLO',
                                'SME MEZZANINE CLO'     :      'CLO',
                                'SME CLO'               :      'CLO',
                                'MIDDLE MARKET CLO'     :      'CLO',
                                'LEVERAGED LOAN CLO'    :      'CLO',
                                'CMO'                   :      'CMO',
                                'WHOLE LOAN'            :      'CMO'}
        if security_type2 and security_type2.upper() in secutiry_type2_dict:
            isitic_code = secutiry_type2_dict[security_type2.upper()]
        if not isitic_code:
            issuer = self.__get_provider_data('ISSUER')
            issuer_dict =  {'GOVERNMENT NATIONAL MORTGAGE A'            : 'GN',
                            'GOVERNMENT NATIONAL MORTGAGE ASSOCIATION'  : 'GN',
                            'FEDERAL HOME LOAN BANKS'                   : 'FHL',
                            'FANNIE MAE'                                : 'FN'}
            if issuer and issuer.upper() in issuer_dict:
                isitic_code = issuer_dict[issuer.upper()]
        if not isitic_code:
            isitic_code = 'FHA'
        return isitic_code

    def Repo_Reverse(self):
        """infer the isitc code for Repo/Reverse instrument type"""
        isitic_code = None
        if self.__trade:
            if self.__trade.Nominal() > 0:
                isitic_code = 'RVRP'
            else:
                isitic_code = 'RP'
        return isitic_code

    def Flexi_Bond(self):
        """infer the isitc code for FlexiBond instrument type"""
        isitic_code = self.__isitic_from_market_sector()
        if not isitic_code:
            isitic_code = self.__get_isitic_from_issuer_bis()
        return isitic_code

    def Average_Future_Forward(self):
        """infer the isitc code for Average Future/Forward instrument type"""
        isitic_code = None
        if self.__instrument:
            if self.__instrument.PayType() == 'Future':
                isitic_code = 'FUT'
            elif self.__instrument.PayType() == 'Forward':
                if self.__instrument.Legs()[0].FloatRateReference().InsType()== 'Bond':
                    isitic_code = 'BFW'
        return isitic_code

    def Curr(self):
        """infer the isitc code for all FX trades and Curr instrument type"""
        isitic_code = None
        if self.__trade:
            if self.__trade.IsFxForward():
                isitic_code = 'FXF'
            elif self.__trade.IsFxSpot():
                isitic_code = 'FXS'
            #elif self.__trade.IsFxSwap():
        return isitic_code

