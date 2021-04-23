"""------------------------------------------------------------------------
MODULE
    FRegulatoryAPIs -
DESCRIPTION:
    This file consists of the Regulatory APIs that can be made available on different objects
VERSION: 1.0.25(0.25.7)
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import FRegulatoryLibWrapper
import FRegulatoryLogger
import acm
logger = 'FRegulatoryAPIs'
class RegulatoryMethods(object):
    def __init__(self):
        
        self.apiOnClassDict = {'IsCleared': 'acm.FTrade',
                               'HiQualityLiquidAsset': 'acm.FInstrument',
                               'CountryOfIssue': 'acm.FInstrument',
                               'BondType': 'acm.FInstrument',
                               'BbgCollateralType': 'acm.FInstrument',
                               'IsGovernmentGuaranteed': 'acm.FInstrument',
                               'IsCovered': 'acm.FInstrument',
                               'FundType': 'acm.FInstrument',
                               'MainTradingPlace': 'acm.FInstrument',
                               'SFTRSecurityType': 'acm.FInstrument',
                               'IsEquity': 'acm.FInstrument',
                               'SFTRIsCollateralProvider': 'acm.FTrade',
                               'IsAllocated': 'acm.FAccount',
                               'OutstandingShares': 'acm.FInstrument',
                               'IssuerType': 'acm.FInstrument',
                               'SFTRType': 'acm.FTrade',
                               'DatePeriodUnit': 'acm.FInstrument',
                               'DayCountMethod': 'acm.FInstrument',
                               'SFTRAsset': 'acm.FTrade',
                               'SFTRSecurityQuality': 'acm.FTrade',
                               'ISDAMMSProductSubGroup': 'acm.FTrade',
                               'ISDAMMSAssetClass': 'acm.FTrade',
                               'FloatingRateIndex': 'acm.FInstrument',
                               'IsJurisdiction': ('acm.FInstrument', 'acm.FParty'),
                               'IsRegulatoryAuthority': ('acm.FInstrument', 'acm.FParty'),
                               }

        self.apiGetterSetterFunction = {'IsCleared': ('is_cleared_getter', 'bool const',\
                                                       'is_cleared_setter', '(bool setval)',\
                                                       'FRegulatoryLibWrapper.tradeWrapper'),\
                                        'HiQualityLiquidAsset': ('hi_qlty_liquid_asset_getter', 'string const',\
                                                                  'hi_qlty_liquid_asset_setter', '(string setval)',\
                                                                  'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'CountryOfIssue': ('country_of_issue_getter', 'string const',\
                                                            'country_of_issue_setter', '(string setval)',\
                                                            'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'BondType': ('bond_type_getter', 'string const',\
                                                      'bond_type_setter', '(string setval)', 'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'BbgCollateralType': ('bbg_collateral_type_getter', 'string const',\
                                                            'bbg_collateral_type_setter', '(string setval)',\
                                                            'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'IsGovernmentGuaranteed': ('is_government_guaranteed_getter', 'FChoiceList const',\
                                                                    'is_government_guaranteed_setter', '(FChoiceList setval)',\
                                                                    'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'IsCovered': ('is_covered_getter', 'FChoiceList const',\
                                                       'is_covered_setter', '(FChoiceList setval)',\
                                                       'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'IsEquity': ('is_equity_getter', 'bool const',\
                                                        'is_equity_setter', '(bool setval)',\
                                                        'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'FundType': ('fund_type_getter', 'string const',\
                                                      'fund_type_setter', '(string setval)',\
                                                      'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'MainTradingPlace': ('main_trading_place_getter', 'string const',\
                                                              'main_trading_place_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'SFTRSecurityType': ('sftr_security_type_getter', 'string const',\
                                                              'sftr_security_type_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'IsAllocated': ('is_allocated_getter', 'bool const',\
                                                       'is_allocated_setter', '(bool setval)',
                                                       'FRegulatoryLibWrapper.accountWrapper'),\
                                        'OutstandingShares': ('outstanding_shares_getter', 'string const',\
                                                              'outstanding_shares_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'SFTRIsCollateralProvider': ('sftr_is_collateral_provider_getter', 'FChoiceList const',\
                                                              'sftr_is_collateral_provider_setter', '(FChoiceList setval)',\
                                                              'FRegulatoryLibWrapper.tradeWrapper'),\
                                        'IssuerType': ('issuer_type_getter', 'string const',\
                                                              'issuer_type_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.instrumentWrapper'),\
                                        'SFTRType': ('sftr_type_getter', 'string const',\
                                                              'sftr_type_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.tradeWrapper'),\
                                        'SFTRAsset': ('sftr_asset_getter', 'string const',\
                                                              'sftr_asset_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.tradeWrapper'),\
                                        'SFTRSecurityQuality': ('sftr_security_quality_getter', 'string const',\
                                                              'sftr_security_quality_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.tradeWrapper'),\
                                        'ISDAMMSProductSubGroup': ('product_sub_group_getter', 'string const',\
                                                              'product_sub_group_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.tradeWrapper'),\
                                        'ISDAMMSAssetClass': ('asset_class_getter', 'string const',\
                                                              'asset_class_setter', '(string setval)',\
                                                              'FRegulatoryLibWrapper.tradeWrapper'),\
                                        }

        self.trade_wrapper_obj = FRegulatoryLibWrapper.tradeWrapper()
        self.ins_wrapper_obj = FRegulatoryLibWrapper.instrumentWrapper()
        self.account_wrapper_obj = FRegulatoryLibWrapper.accountWrapper()
        self.sftr_wrapper_obj = FRegulatoryLibWrapper.sftrWrapper()
        self.addInfoDataType = {'regIsCleared': 'Boolean', 'regHiQltyLqdAsset': 'String',\
                                'regCountryOfIssue': 'String', 'regBondType': 'String',\
                                'regCollateralType': 'String', 'regIsGovtGuaranteed': 'FChoiceList',\
                                'regIsCovered': 'Boolean', 'regIsCollatrlPrvdr': 'FChoiceList',\
                                'regFundType': 'String', 'regMainTradingPlace': 'String',\
                                'regIsEquity': 'Boolean', \
                                'regIsCmdtyAllocated': 'Boolean', 'regSFTRSecurityType': 'String',\
                                'regOutStndingShares': 'String', 'regIssuerType': 'String',\
                                'regSFTRType': 'String', 'regSFTRAsset': 'String',\
                                'regSFTRSecurityQlty': 'String', 'regProductSubGroup': 'String',\
                                'regAssetClass': 'String',}
        self.addInfoChoiceListType = {'regIsGovtGuaranteed' : 'Tristate',\
                                      'regIsCovered' : 'Tristate',\
                                      'regIsCollatrlPrvdr' : 'Tristate'}
        self._addInfoStandardDict = {
        'IsCleared': ('regIsCleared', None, self.trade_wrapper_obj.is_cleared, 'bool', 'Is the trade cleared', None),
        'HiQualityLiquidAsset': ('regHiQltyLqdAsset',  None, None, 'String',\
                                  'Categorization of a collateral to judge how willingly one would want to use as collateral. Values like 1, 2A, 2B, 3, NA.', None),
        'CountryOfIssue': ('regCountryOfIssue', None, self.ins_wrapper_obj.country_of_issue, 'string', 'country of issye of the instrument', None),
        'BondType': ('regBondType', None, self.ins_wrapper_obj.bond_type, 'string', 'bond type of the instrument', None),
        'BbgCollateralType': ('regCollateralType', None, self.ins_wrapper_obj.bbg_collateral_type, 'string', 'collateral type of the instrument', None),
        'IsEquity': ('regIsEquity', None, self.ins_wrapper_obj.is_equity, 'bool', 'equity type of the instrument', None),
        'FundType': ('regFundType', None, self.ins_wrapper_obj.fund_type, 'string', 'fund type of the instrument', None),
        'MainTradingPlace': ('regMainTradingPlace', None, self.ins_wrapper_obj.main_trading_place, 'string', 'main trading place of the instrument', None),
        'SFTRSecurityType': ('regSFTRSecurityType', None, self.ins_wrapper_obj.sftr_security_type, 'string', 'SFTR secutiry type of the instrument', None),
        'OutstandingShares': ('regOutStndingShares', None, self.ins_wrapper_obj.outstanding_shares, 'string', 'Market Cap of the instrument', None),
        'IsGovernmentGuaranteed': ('regIsGovtGuaranteed', None, self.ins_wrapper_obj.is_government_guaranteed, 'FChoiceList', 'Is the instrument a government guaranteed instrument', None),
        'IsCovered': ('regIsCovered', None, self.ins_wrapper_obj.is_covered, 'FChoiceList', 'Is the Bond covered or not', None),
        'SFTRIsCollateralProvider': ('regIsCollatrlPrvdr', None, self.trade_wrapper_obj.sftr_is_collateral_provider, 'FChoiceList', 'Is it is collateral provider or not', None),
        'IsAllocated': ('regIsCmdtyAllocated', None, self.account_wrapper_obj.allocated, 'bool', 'Is allocated or not', None),
        'IssuerType': ('regIssuerType', None, self.ins_wrapper_obj.issuer_type, 'string', 'type of issuer of the instrument', None),
        'SFTRType': ('regSFTRType', None, self.trade_wrapper_obj.sftr_type, 'string', 'sftrType of the instrument on which the trade is booked', None),
        'SFTRAsset': ('regSFTRAsset', None, self.trade_wrapper_obj.sftr_asset, 'string', 'sftr asset type of the instrument on which the trade is booked', None),
        'SFTRSecurityQuality': ('regSFTRSecurityQlty', None, self.trade_wrapper_obj.sftr_asset, 'string', 'sftr asset type of the instrument on which the trade is booked', None),
        'ISDAMMSAssetClass': ('regAssetClass', None, self.trade_wrapper_obj.asset_class, 'string', 'asset class of the instrument', None),
        'ISDAMMSProductSubGroup': ('regProductSubGroup', None, self.trade_wrapper_obj.product_sub_group, 'string', 'product sub group of the instrument', None),
        'FloatingRateIndex': (None, None, self.ins_wrapper_obj.floating_rate_index, 'string', 'get the ESMA name for the RateIndex', None),
}
        self._standardMethods = ['IsCleared', 'CountryOfIssue',\
                                 'BondType', 'IsCovered',\
                                 'FundType', 'MainTradingPlace',\
                                 'IsEquity', 'IsAllocated',\
                                 'OutstandingShares', 'IssuerType',\
                                 'FloatingRateIndex', 'IsJurisdiction',\
                                 'IsRegulatoryAuthority']
        self._collateralMethods = ['HiQualityLiquidAsset', 'BbgCollateralType',\
                                   'IsGovernmentGuaranteed', 'ISDAMMSAssetClass',\
                                   'ISDAMMSProductSubGroup']
        self._SFTRMethods = ['SFTRSecurityType', 'SFTRIsCollateralProvider',\
                            'SFTRType', 'SFTRAsset', 'SFTRSecurityQuality',]
        self._alreadyAddedAPIs = {}

    def __createAPI(self, meth):
        retLog = ''
        if meth not in self._addInfoStandardDict:
            if meth.rfind('.') != -1:
                meth = meth[meth.rfind('.') + 1 :]
        details = self._addInfoStandardDict[meth]
        aiName = details[0]
        provName = details[1]
        provFunc = details[2]
        rettyp = details[3]
        if provName:# Return single value of a provider attribute COLLATERL_TYP
            FRegulatoryLogger.INFO(logger, "Currently not supported")
        elif provFunc:
            am = "%s:%s" % (meth, rettyp)
            if isinstance(self.apiOnClassDict[meth], tuple):
                for each_class in self.apiOnClassDict[meth]:
                    eval(each_class + '.AddMethod(am, provFunc)')
                    eval(each_class + '.AddMethod(am, provFunc)')
            else:
                eval(self.apiOnClassDict[meth] + '.AddMethod(am, provFunc)')
            retLog += '%s: Added for "%s"\n' % (meth, str(provFunc))
            self.addToAPIexistsDict(meth, self.apiOnClassDict[meth])
        else:
            retLog += '%s: Missing provider data info (%s)\n' % (meth, str((meth, provName, provFunc, rettyp)))
        return retLog

    def addToAPIexistsDict(self, methodName, methodOnclass):
        if methodOnclass in self._alreadyAddedAPIs:
            apiList = self._alreadyAddedAPIs[methodOnclass]
            if methodName in apiList:
                FRegulatoryLogger.DEBUG(logger, '<%s> already exists on class <%s>'%(methodName, methodOnclass))
            else:
                self._alreadyAddedAPIs[methodOnclass] = apiList.append(methodName)

    def setupMethods(self, apiList = None):
        retLog = ''
        if not apiList:
            apiList = self._addInfoStandardDict.keys()
        for meth in apiList:
            if meth in self.apiOnClassDict:
                if meth in ['IsJurisdiction', 'IsRegulatoryAuthority']:
                    getterWithArguments().setupMethods()
                elif isinstance(self.apiOnClassDict[meth], tuple):
                    function_present = False
                    for each_class in self.apiOnClassDict[meth]:
                        if eval(each_class + '.GetMethod(meth, 0)'):
                            retLog += '%s: Already defined\n' % meth
                            function_present = True
                            continue
                        else:
                            function_present = False
                    if function_present:
                        continue
                else:
                    if eval(self.apiOnClassDict[meth] + '.GetMethod(meth, 0)'):
                        retLog += '%s: Already defined\n' % meth
                        continue
            if meth in self.apiOnClassDict.keys():
                apiOnAddInfo = self.addAPIOnAddInfo(meth, self.apiOnClassDict[meth], self._addInfoStandardDict)
                if not apiOnAddInfo:
                    if meth not in ['IsJurisdiction', 'IsRegulatoryAuthority']:
                        retLog += self.__createAPI(meth)
        acm.UpdatePythonWrappers()
        return retLog

    def addAPIOnAddInfo(self, meth, methodOnclass, dictForLookUp):
        apisAdded = False
        if self.ifAddInfoSpecExists(meth, methodOnclass, dictForLookUp):
            if meth in self.apiGetterSetterFunction:
                methodDetails = self.apiGetterSetterFunction[meth]
                getterMethod = methodDetails[4] + '().' + methodDetails[0]
                setterMethod = methodDetails[4] + '().' + methodDetails[2]
                if meth.rfind('.') != -1:#this is to ensure that acm.FInstrument.MoodysShortRating is changed to MoodysShortRating
                    meth = meth[meth.rfind('.') + 1 : ]
                if isinstance(self.apiOnClassDict[meth], tuple):
                    classes = self.apiOnClassDict[meth]
                    for each_class in classes:
                        eval(each_class + ".AddMethod('" + meth + ':' + methodDetails[1] + "', " + getterMethod + ')')
                        eval(each_class + ".AddMethod('" + meth + methodDetails[3] + "', " + setterMethod + ')')
                        self.addToAPIexistsDict(meth, each_class)
                else:
                    eval(self.apiOnClassDict[meth] + ".AddMethod('" + meth + ':' + methodDetails[1] + "', " + getterMethod + ')')
                    eval(self.apiOnClassDict[meth] + ".AddMethod('" + meth + methodDetails[3] + "', " + setterMethod + ')')
                    self.addToAPIexistsDict(meth, self.apiOnClassDict[meth])
                apisAdded = True
            else:
                FRegulatoryLogger.INFO(logger, "The AdditionalInfo details are not present for API <%s>"%meth)
        return apisAdded

    def ifAddInfoSpecExists(self, meth, methodOnclass, dictForLookUp):
        addInfoSpecExists = False
        if meth in dictForLookUp:
            details = dictForLookUp[meth]
            addInfoName = details[0]
            if addInfoName:
                addInfoSpec = acm.FAdditionalInfoSpec[addInfoName]
                if addInfoSpec:
                    addInfoSpecExists = True
                    if addInfoName in self.addInfoDataType:
                        excType = self.addInfoDataType[addInfoName]
                        if excType in ['FChoiceList']:
                            if addInfoSpec.Description() != self.addInfoChoiceListType[addInfoName]:
                                FRegulatoryLogger.WARN(logger, "AddInfoSpec <%s> exists in ADS. However, it is not of type <%s> for expected functionality"%(addInfoName, self.addInfoChoiceListType[addInfoName]))
                        else:
                            if addInfoSpec.DataTypeType() != acm.FEnumeration['enum(B92StandardType)'].Enumeration(excType.capitalize()):
                                FRegulatoryLogger.WARN(logger, "AddInfoSpec <%s> exists in ADS. However, it is not of type <%s> for expected functionality"%(addInfoName, excType))
                    else:
                        FRegulatoryLogger.WARN(logger, "Details not entered in lookup dict to validate the dataType of AddInfoSpec <%s>"%addInfoName)
        return addInfoSpecExists

    def setupRatingMethod(self, providerMethodList=None):
        if not providerMethodList:
            providerMethodList = self._ratingsMethods
        methLog = self.setupMethods(providerMethodList)
        FRegulatoryLogger.DEBUG(logger, methLog)
        
    def setupStandardMethods(self, providerMethodList=None):
        if not providerMethodList:
            providerMethodList = self._standardMethods
        methLog = self.setupMethods(providerMethodList)
        FRegulatoryLogger.DEBUG(logger, methLog)
    
    def setupCollateralMethods(self, providerMethodList=None):
        if not providerMethodList:
            providerMethodList = self._collateralMethods
        methLog = self.setupMethods(providerMethodList)
        FRegulatoryLogger.DEBUG(logger, methLog)

    def setupSFTRMethods(self, providerMethodList=None):
        if not providerMethodList:
            providerMethodList = self._SFTRMethods
        methLog = self.setupMethods(providerMethodList)
        FRegulatoryLogger.DEBUG(logger, methLog)

class getterWithArguments():
    def __init__(self, jurisdiction_lookup = None, regulatory_authority_lookup = None):
        self.__jurisdiction_lookup = jurisdiction_lookup
        self.__regulatory_authority_lookup = regulatory_authority_lookup

    def setupMethods(self):
        self.__create_methods()

    def __create_methods(self):
        method_list = ['IsJurisdiction',\
                       'IsRegulatoryAuthority']
        for each_method in method_list:
            if each_method == 'IsJurisdiction':
                am = each_method + "(string jurisdiction):FChoiceList const"
                acm.FInstrument.AddMethod(am, FRegulatoryLibWrapper.JurisdictionNRegulatoryAuthority(jurisdiction_lookup=self.__jurisdiction_lookup).isJurisdiction)
                acm.FParty.AddMethod(am, FRegulatoryLibWrapper.JurisdictionNRegulatoryAuthority(jurisdiction_lookup=self.__jurisdiction_lookup).isJurisdiction)
            else:
                am = each_method + "(string regulatory_authority):FChoiceList const"
                acm.FInstrument.AddMethod(am, FRegulatoryLibWrapper.JurisdictionNRegulatoryAuthority(regulatory_authority_lookup=self.__regulatory_authority_lookup).isRegulatoryAuthority)
                acm.FParty.AddMethod(am, FRegulatoryLibWrapper.JurisdictionNRegulatoryAuthority(regulatory_authority_lookup=self.__regulatory_authority_lookup).isRegulatoryAuthority)

class ratingAlias():
    def __init__(self, sortOrder):
        self.sortOrder = sortOrder + 1 # Sort order is 0,1,2 but attr are rating1_chlnbr, rating2_chlnbr and rating3_chlnbr

    def getter(self, acm_object):
        rating_val = None
        if self.sortOrder > 3:
            sortOrder = self.sortOrder - 1
            cl = acm.FChoiceList.Select01("list = 'Ratings' and sortOrder=%d"%sortOrder, None)
            if cl:
                sr = StandardRatings()
                meth = sr.getMethod(cl.Name())
                addinfo_val = sr.getAddInfo(meth, acm_object)
                rating_val = addInfoLookup(addinfo_val).getter(acm_object)

        else:
            if acm_object.IsKindOf(acm.FParty):
                rating_val = eval('acm_object.Rating' + str(self.sortOrder) + '()')
            elif acm_object.IsKindOf(acm.FInstrument):
                rating_val = eval('acm_object.Rating' + str(self.sortOrder) + 'ChlItem()')
        return rating_val
        

    def setter(self, acm_object, setval):
        if self.sortOrder > 3:
            sortOrder = self.sortOrder - 1
            cl = acm.FChoiceList.Select01("list = 'Ratings' and sortOrder=%d"%sortOrder, None)
            if cl:
                sr = StandardRatings()
                meth = sr.getMethod(cl.Name())
                addinfo_val = sr.getAddInfo(meth, acm_object)
                addInfoLookup(addinfo_val).setter(acm_object, setval)
        
        else:
            if acm_object.IsKindOf(acm.FParty):
                eval('acm_object.Rating' + str(self.sortOrder) + '(acm.FChoiceList[' + str(setval.Oid()) + '])')
            elif acm_object.IsKindOf(acm.FInstrument):
                try:
                    eval('acm_object.Rating' + str(self.sortOrder) + 'ChlItem(acm.FChoiceList[' + str(setval.Oid()) + '])')
                except Exception as e:
                    FRegulatoryLogger.ERROR(logger, str(e))
        
        
class addInfoLookup():
    def __init__(self, addInfoName):
        self.addInfoName = addInfoName[0].upper() + addInfoName[1:]

    def getter(self, insOrParty):
        val = eval('insOrParty.AdditionalInfo().' + self.addInfoName + '()')
        clObj = None
        if val:
            cl = acm.FAdditionalInfoSpec[self.addInfoName].Description()
            clObj = acm.FChoiceList.Select01("list = '%s' and name = '%s'"%(cl, val), None)
        return clObj

    def setter(self, insOrParty, setVal):
        eval('insOrParty.AdditionalInfo().' + self.addInfoName + '(acm.FChoiceList[' + str(setVal.Oid()) + '])')

class StandardRatings(object):
    def __init__(self): 
        self._ratingsChlNameDict = { 'Moodys': 'MoodysRating', 'MoodysShort': 'MoodysShortRating',\
                                     'S&P': 'SnPRating', 'SnP': 'SnPRating',\
                                     'S&PShort': "SnPShortRating", "SnPShort": "SnPShortRating",\
                                     'Fitch': 'FitchRating', 'FitchShort': 'FitchShortRating',
                                     'DBRS': 'DBRSRating', 'DBRSShort': 'DBRSShortRating',}
        
        self._ratingMethodsAddInfoDictIns = {'MoodysRating' : 'MoodysRating',
                                             'MoodysShortRating' : 'MoodysShortRating',
                                             'SnPRating' : 'SnPRating',\
                                             'SnPShortRating' : 'SnPShortRating',\
                                             'FitchRating' : 'FitchRating', 
                                             'FitchShortRating' : 'FitchShortRating',
                                             'DBRSRating' : 'DBRSRating',
                                             'DBRSShortRating' : 'DBRSShortRating'}
        self._ratingMethodsAddInfoDictParty = {'MoodysRating' : 'MoodysRtg',\
                                               'MoodysShortRating' : 'MoodysShortRtg',\
                                               'SnPRating' : 'SnPRtg',\
                                               'SnPShortRating' : 'SnPShortRtg',\
                                               'FitchRating' : 'FitchRtg',\
                                               'FitchShortRating' : 'FitchShortRtg',\
                                               'DBRSRating' : 'DBRSRtg',\
                                               'DBRSShortRating' : 'DBRSShortRtg'}
        self._ratings = ['MoodysRating', 'SnPRating', 'FitchRating', 'DBRSRating',\
                         'MoodysShortRating', 'SnPShortRating', 'FitchShortRating']

    def getMethod(self, choiceListName):
        """get the name of the method that needs to be created on the class"""
        methodName = None
        if choiceListName in self._ratingsChlNameDict.keys():
            methodName = self._ratingsChlNameDict[choiceListName]
        return methodName

    def getAddInfo(self, methodName, acm_object):
        """get the AddInfo for the corresponding function on the class"""
        addInfoName = None
        if acm_object.IsKindOf(acm.FParty):
            if methodName in self._ratingMethodsAddInfoDictParty.keys():
                addInfoName = self._ratingMethodsAddInfoDictParty[methodName]
        else:
            if methodName in self._ratingMethodsAddInfoDictIns.keys():
                addInfoName = self._ratingMethodsAddInfoDictIns[methodName]
        return addInfoName

    def __createMethod(self, meth, chlR):
        """create the method being passed as an argument"""
        am = meth + ":FChoiceList const"
        acm.FInstrument.AddMethod(am, ratingAlias(chlR.SortOrder()).getter)
        acm.FParty.AddMethod(am, ratingAlias(chlR.SortOrder()).getter)
        FRegulatoryLogger.DEBUG(logger, "Adding method <%s> on Instrument and Party."%am)
        am = meth + "(FChoiceList const)"
        acm.FInstrument.AddMethod(am, ratingAlias(chlR.SortOrder()).setter)  
        acm.FParty.AddMethod(am, ratingAlias(chlR.SortOrder()).setter)
        FRegulatoryLogger.DEBUG(logger, "Adding method <%s> on Instrument and Party."%am)

    def setupMethods(self, nameList=[]):
        """set up methods"""
        if not nameList: 
            nameList = self._ratings
        alreadyAdded=[]
        cl_dict = {}
        choicelists = acm.FChoiceList.Select('list=Ratings')
        cl_names = []
        for choicelist in choicelists:
            cl_names.append(choicelist.Name())
            cl_dict[choicelist.Name()] = choicelist
        for chlr in self._ratingsChlNameDict.keys():
            if chlr in cl_names:
                meth = self._ratingsChlNameDict[chlr]
                self.__createMethod(meth, cl_dict[chlr])
                alreadyAdded.append(meth)
            else:
                FRegulatoryLogger.DEBUG(logger, "ChoiseList <%s> does not exist in ADS. "
                "Hence cannot create APIS <%s>"%(chlr, str(self._ratingsChlNameDict[chlr])))
        for meth in nameList:
            if meth not in alreadyAdded:
                FRegulatoryLogger.DEBUG(logger, "Creating API <%s> on AddInfo"%meth)
                if meth in self._ratingMethodsAddInfoDictIns.keys():
                    aiName = self._ratingMethodsAddInfoDictIns[meth]
                    if acm.FAdditionalInfoSpec[aiName]: # Is it defined?
                        am = meth + ":FChoiceList const"
                        FRegulatoryLogger.DEBUG(logger, "Adding method <%s> on Instrument."%am)
                        acm.FInstrument.AddMethod(am, addInfoLookup(aiName).getter)  
                        am = meth + "(FChoiceList const)"
                        acm.FInstrument.AddMethod(am, addInfoLookup(aiName).setter)  
                        alreadyAdded.append(meth)
                        FRegulatoryLogger.DEBUG(logger, "Adding method <%s> on Instrument."%am)
                    else:
                        FRegulatoryLogger.INFO(logger, meth + "was not defined. Missing AdditionalInfoSpec (%s)" % aiName)
                if meth in self._ratingMethodsAddInfoDictParty.keys():
                    aiName = self._ratingMethodsAddInfoDictParty[meth]
                    if acm.FAdditionalInfoSpec[aiName]: # Is it defined?
                        am = meth + ":FChoiceList const"
                        FRegulatoryLogger.DEBUG(logger, "Adding method <%s> on Party."%am)
                        acm.FParty.AddMethod(am, addInfoLookup(aiName).getter)
                        am = meth + "(FChoiceList const)"
                        acm.FParty.AddMethod(am, addInfoLookup(aiName).setter)
                        FRegulatoryLogger.DEBUG(logger, "Adding method <%s> on Party."%am)
                        alreadyAdded.append(meth)
                    else:
                        FRegulatoryLogger.DEBUG(logger,\
                                meth + "was not defined. Missing AdditionalInfoSpec (%s)" % aiName)
        acm.UpdatePythonWrappers()
        return alreadyAdded

    def addChoiceListRating(self, instrOrParty, methodname, choiceListName):
        """Add/update RatingAPI on class based on the ChoiceList"""
        if choiceListName in self._ratingsChlNameDict.keys():
            if self._ratingsChlNameDict[choiceListName] != methodname:
                FRegulatoryLogger.DEBUG(logger, "API <%s> currently refers to ChoiceList <%s>\
                 instead of <%s>. This will be overridden with <%s>"%(\
                methodname, self._ratingsChlNameDict[choiceListName],\
                choiceListName, choiceListName))
        self._ratingsChlNameDict[choiceListName] = methodname

    def addAddInfoRating(self, instrOrParty, methodname, addInfSpecName):
        """Add/update RatingAPI on class based on the AddInfoSpec being passed"""
        if 'Instrument' in instrOrParty:
            if methodname in self._ratingMethodsAddInfoDictIns.keys():
                if self._ratingMethodsAddInfoDictIns[methodname] != addInfSpecName:
                    FRegulatoryLogger.DEBUG(logger, "API <%s> on Instrument currently refers to AddInfoSpec <%s>\
                 instead of <%s>. This will be overridden with <%s>"%(methodname,\
                    self._ratingMethodsAddInfoDictIns[methodname], addInfSpecName, addInfSpecName))
                    self._ratingMethodsAddInfoDictIns[methodname] = addInfSpecName
                 
        elif 'Party' in instrOrParty:
            if methodname in self._ratingMethodsAddInfoDictParty.keys():
                if self._ratingMethodsAddInfoDictParty[methodname] != addInfSpecName:
                    FRegulatoryLogger.DEBUG(logger, "API <%s> on Party currently refers to AddInfoSpec <%s>\
                 instead of <%s>. This will be overridden with <%s>"%(methodname,\
                    self._ratingMethodsAddInfoDictParty[methodname], addInfSpecName, addInfSpecName))
                    self._ratingMethodsAddInfoDictParty[methodname] = addInfSpecName
        else:
            FRegulatoryLogger.DEBUG(logger, "Adding of an AddInfoRating is supported for Party and Instrument only")

    def listDefinedMethods(self):
        pass #TODO: TestMe method

