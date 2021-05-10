"""------------------------------------------------------------------------
MODULE
    FRegulatorySupportValidateSetup -
DESCRIPTION:
    The module that validates whether the installation
    has all the basic setup required for the expected functioning
     of the component
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import acm
import FRegulatoryLogger
import string
logger = "FRegulatorySupportValidateSetup"

def __get_acm_object_type(acm_object):
    acm_object_type = None
    try:
        if acm_object.IsKindOf(acm.FTrade):
            acm_object_type = 'Trade'
        elif acm_object.IsKindOf(acm.FInstrument):
            acm_object_type = 'Instrument'
        elif acm_object.IsKindOf(acm.FContact):
            acm_object_type = 'Contact'
        elif acm_object.IsKindOf(acm.FParty):
            acm_object_type = 'Party'
        elif acm_object.IsKindOf(acm.FPerson):
            acm_object_type = 'Person'
    except:
        pass
    return acm_object_type

def checkTernaryAPIExists(acm_object, attr_list):
    """check for the presense of the pre-requistes in the ADS required for\
     the functioning for the RegulatorySupport"""
    acm_object_type = __get_acm_object_type(acm_object)
    api_exist = True    
    for each_api in attr_list:
        try:
            eval('acm_object.' + each_api + '()')
            FRegulatoryLogger.DEBUG(logger, "<%s> exists on <%s>"%(each_api, acm_object_type))
        except:
            FRegulatoryLogger.ERROR(logger, "API <%s> is not found on %s"%(\
                            each_api, acm_object_type))
            api_exist = False
    return api_exist

def checkRegulatoryAPIExists(acm_object, attr_list):
    """check for the presense of the pre-requistes in the ADS required for\
     the functioning for the RegulatorySupport"""
    reg_info = None
    regulatory_apis_exist = True
    acm_object_type = __get_acm_object_type(acm_object)
    try:
        reg_info = acm_object.RegulatoryInfo()
    except:
        FRegulatoryLogger.ERROR(logger, "RegulatoryInfo instance on the %s is not accessible. Import\
        the RegulatorySupport package for expected functionality."%acm_object_type)
        regulatory_apis_exist = False
    if reg_info:
        for each_api in attr_list:
            try:
                eval('reg_info.' + each_api + '()')
            except:
                FRegulatoryLogger.ERROR(logger, "API <%s> is not found on %s.RegulatoryInfo"%(\
                                each_api, acm_object_type))
                regulatory_apis_exist = False
    return regulatory_apis_exist

def checkAddInfoSpecExists(acm_class, addinfo_spec_name):
    """returns True if the AdditionalInfoSpec exists on the given class. else returns False """
    addinfo_spec_exists = False
    addinfo_spec = acm.FAdditionalInfoSpec[addinfo_spec_name]
    if addinfo_spec:
        if addinfo_spec.RecType() == acm_class:
            FRegulatoryLogger.DEBUG(logger, "<%s> on <%s> exists in ADS."%(acm_class, addinfo_spec_name))
            addinfo_spec_exists = True
        else:
            FRegulatoryLogger.ERROR(logger, "<%s> exists on <%s> instead of on <%s> in ADS."%(\
                addinfo_spec_name, acm_class, addinfo_spec.RecType()))
    else:
        FRegulatoryLogger.ERROR(logger, "<%s> on <%s> does not exist in ADS"%(addinfo_spec_name, acm_class))
    return addinfo_spec_exists

def checkChoiceLists(choice_list, choice_list_vals):
    """check if the ChoiceList exists along with all the values that are required in it"""
    all_choice_lists_exist = True
    updated_choice_list_vals = []
    for choice_list_val in choice_list_vals:
        update_choice_list = choice_list_val
        if len(choice_list_val) > 39:
            update_choice_list = choice_list_val[0:39]
        updated_choice_list_vals.append(update_choice_list)
    choice_lists_adm = acm.FChoiceList.Select("list = '%s'"%choice_list)
    choice_list_adm_names = []
    for choice_list_adm in choice_lists_adm:
        choice_list_adm_names.append(choice_list_adm.Name())
    if choice_lists_adm:
        if len(choice_lists_adm) < len(choice_list_vals):
            FRegulatoryLogger.WARN(logger, "All ChoiceList values for <%s> does not exist within ADS."%(choice_list))
            all_choice_lists_exist = False
        else:
            for choice_list_val in updated_choice_list_vals:               
                if choice_list_val.strip() not in choice_list_adm_names:
                    FRegulatoryLogger.ERROR(logger, "<%s> is not in ChoiceList <%s> in ADS."%(\
                            choice_list_val.strip(), choice_list))
                    all_choice_lists_exist = False
    else:
        FRegulatoryLogger.ERROR(logger, "ChoiceList <%s> does not exist in ADS"%choice_list)
        all_choice_lists_exist = False
    return all_choice_lists_exist

class FRegulatorySupportValidateSetup(object):
    """validate the RegulatorySupport setup"""
    def __init__(self):
        version = ".".join(acm.ShortVersion().strip(string.ascii_letters).split(".")[0:2])
        version = version.replace('Python', '')
        self.acm_version = float(version)

    def InstrumentRegulatoryAPIs(self):
        """check for the presense of the pre-requistes for Instrument in the ADS required for\
         the functioning for the RegulatorySupport"""
        ins_reg_list = ['TradingTerminationDate', 'FirstTradingTime', 'AdmissionRequestTime',\
                        'AdmissionApprovalTime', 'HasTradingObligation', 'AverageDailyTurnover',\
                        'IsSystematicInternaliser', 'IsLiquid', 'StandardMarketSize',\
                        'SizeSpecificToInstrument', 'LargeInScale', 'CfiCode',\
                        'ClearingIsMandatory', 'CommodityBaseProduct',\
                        'CommoditySubProduct', 'CommodityFurtherSubProduct',\
                        'FinalPriceType', 'TransactionType', 'SimilarIsin',\
                        'IsTradedOnTradingVenue', 'LiquidityBand', 'InstypeRTS2',\
                        'InsSubtypeRTS2', 'PrimaryMarketMic',\
                        'MaterialMarketMic', 'DarkCapMic', 'DarkCapStatus',\
                        'DoubleVolumeCapStatus', 'TickSize', 'IsMiFIDTransparent',\
                        'SizeSpecificToInstrumentInCurrency',\
                        'PostSizeSpecificToInstrument', 'PostSizeSpecificToInstrumentInCurrency',\
                        'LargeInScaleInCurrency', 'PostLargeInScale', 'PostLargeInScaleInCurrency',\
                        'FinancialInstrumentShortName', 'InstypeRTS28', 'IsEquityLike',\
                        'IsBondLike', 'IsInterestRateDerivative', 'IsEquityDerivative',\
                        'IsC10Derivative', 'IsFxDerivative', 'IsCFD']
        instruments = acm.FInstrument.Select('')
        apis_exist = True
        if instruments:
            acm_ins = instruments[0]
            if acm_ins:
                apis_exist = checkRegulatoryAPIExists(acm_ins, ins_reg_list)
        else:
            FRegulatoryLogger.ERROR(logger, "A valid instrument does not exist in ADS. Hence cannot\
                 verify the Regulatory prerequisites on Instrument.")
            apis_exist = False
        return apis_exist

    def TradeRegulatoryAPIs(self):
        """check for the presense of the pre-requistes for Trade in the ADS required for\
        the functioning for the RegulatorySupport"""
        trade_reg_list = ['RepositoryId', 'ClearingBroker', 'ClearingHouse',\
                      'Middleware', 'OriginalCounterparty', 'Repository',\
                      'TradingCapacity', 'ComplexTradeComponentId', 'OurOrganisation',\
                      'OurTransmittingOrganisation', 'OurInvestmentDecider', 'OurTrader',\
                      'ExecutingEntity', 'Venue', 'BranchMembership', 'TheirOrganisation',\
                      'TheirInvestmentDecider', 'TheirTrader', 'Waiver', 'WaiverString',\
                      'OtcPostTradeIndicator', 'OtcPostTradeIndicatorString',\
                      'IsCommodityDerivative', 'IsSecurityFinancingTransaction',\
                      'ReportingEntity', 'ExchangeId', 'AlgoId', 'DirectedOrder',\
                      'IsProvidingLiquidity', 'IsHedge', 'TimePrecision',\
                      'TradeTimeWithPrecision', 'TimePrecisionInUTC', 'ReportDeferToTime',\
                      'ConfirmationTime', 'ClearingTime', 'InvestmentDeciderCrmId', 'Isin',\
                      'CfiCode', 'NearLegIsin', 'FarLegIsin',\
                      'TransmissionOfOrdersIndicator', 'OurOrg', 'TheirOrg']
        trades = acm.FTrade.Select('')
        apis_exist = True
        if trades:
            acm_trd = trades[0]
            if acm_trd:
                apis_exist = checkRegulatoryAPIExists(acm_trd, trade_reg_list)
        else:
            FRegulatoryLogger.ERROR(logger, "A valid trade does not exist in ADS. Hence cannot\
                 verify the Regulatory prerequisites on Trade.")
            apis_exist = False
        return apis_exist

    def PartyRegulatoryAPIs(self):
        """check for the presense of the pre-requistes for Party in the ADS required for\
         the functioning for the RegulatorySupport"""
        party_reg_list = ['IsInvestmentFirm', 'PossibleReporter', 'FinancialCategory', \
                          'MIC', 'IsAlgorithm', 'ExchangeId', 'CrmId', 'MiFIDCategory', \
                          'ClientType', 'IsVenue']
        parties = acm.FParty.Select('')
        apis_exist = True
        if parties:
            acm_party = parties[0]
            if acm_party:
                apis_exist = checkRegulatoryAPIExists(acm_party, party_reg_list)
        else:
            FRegulatoryLogger.ERROR(logger,\
                 "A valid party does not exist in ADS. Hence cannot verify\
                 the Regulatory prerequisites on Party.")
            apis_exist = False
        return apis_exist

    def ContactRegulatoryAPIs(self):
        """check for the presense of the pre-requistes for Contact in the ADS required for\
         the functioning for the RegulatorySupport"""
        contact_reg_list = ['DateOfBirth', 'FirstName', 'LastName', 'NationalId',\
                            'CrmId', 'ExchangeId', 'UniqueName', 'ClientType',\
                             'JointAccount', 'IsGeneralPartner']
        contacts = acm.FContact.Select('')
        apis_exist = True
        if contacts:
            acm_contact = contacts[0]
            if acm_contact:
                apis_exist = checkRegulatoryAPIExists(acm_contact, contact_reg_list)
        else:
            FRegulatoryLogger.ERROR(logger, "A valid contact does not exist in ADS. Hence cannot\
                 verify the Regulatory prerequisites on Contact.")
            apis_exist = False
        return apis_exist

    def PersonRegulatoryInfoAPIs(self):
        """check for the presense of the pre-requistes for Person in the ADS required for\
         the functioning for the RegulatorySupport"""
        person_reg_list = ['DateOfBirth', 'FirstName', 'LastName', 'NationalId', \
                            'CrmId', 'ExchangeId', 'ClientType', 'Contact']
        try:
            persons = acm.FPerson.Select('')
            apis_exist = True
            if persons:
                acm_person = persons[0]
                if acm_person:
                    apis_exist = checkRegulatoryAPIExists(acm_person, person_reg_list)               
            else:
                FRegulatoryLogger.ERROR(logger, "A valid person does not exist in ADS. Hence cannot\
                     verify the Regulatory prerequisites on Person.")
                apis_exist = False
        except:#it means object doesnt exist on this version
            pass
        return apis_exist

    def Trade(self):
        """check for the presense of the AddInfo on the Trade in the ADS required for\
         the functioning for the RegulatorySupport"""
        all_trd_addinfo_specs_exists = True
        trd_add_info_specs, acm_object = self.get_trd_add_info_list()
        orig_acm_object = acm_object
        for add_info_spec in trd_add_info_specs:
            if add_info_spec == 'regShortSell':
                acm_object = 'Trade'
            else:
                acm_object = orig_acm_object
            add_info_spec_exists = checkAddInfoSpecExists(acm_object, add_info_spec)
            if not add_info_spec_exists:
                all_trd_addinfo_specs_exists = False
        return all_trd_addinfo_specs_exists

    def Instrument(self):
        """check for the presense of the AddInfo on the Instrument in the ADS required for\
         the functioning for the RegulatorySupport"""
        all_ins_addinfo_specs_exists = True
        ins_add_info_specs, acm_object = self.get_ins_add_info_list()
        orig_acm_object = acm_object
        for add_info_spec in ins_add_info_specs:
            if add_info_spec == 'ESMAIndex':
                acm_object = 'Instrument'
            else:
                acm_object = orig_acm_object
            add_info_spec_exists = checkAddInfoSpecExists(acm_object, add_info_spec)
            if not add_info_spec_exists:
                all_ins_addinfo_specs_exists = False
        return all_ins_addinfo_specs_exists

    def Contact(self):
        """check for the presense of the AddInfos on Contact in the ADS required for\
         the functioning for the RegulatorySupport"""
        all_contact_addinfo_specs_exists = True
        contact_add_info_specs, acm_object = self.get_contact_add_info_list()
        for add_info_spec in contact_add_info_specs:
            add_info_spec_exists = checkAddInfoSpecExists(acm_object, add_info_spec)
            if not add_info_spec_exists:
                all_contact_addinfo_specs_exists = False
        return all_contact_addinfo_specs_exists

    def Party(self):
        """check for the presense of the AddInfo on the Party in the ADS required for\
         the functioning for the RegulatorySupport"""
        all_party_addinfo_specs_exists = True
        party_add_info_list = ['regIsInvestmentFirm', 'regPossibleReporter', \
                               'regFinancialCategor', 'regIsAlgorithm', 'regPtyExchangeId', \
                               'regPtyCrmId', 'regMifidCategory']
        acm_object = 'Party'
        for add_info_spec in party_add_info_list:
            add_info_spec_exists = checkAddInfoSpecExists(acm_object, add_info_spec)
            if not add_info_spec_exists:
                all_party_addinfo_specs_exists = False
        return all_party_addinfo_specs_exists

    def get_trd_add_info_list(self):
        """get the list of AddInfos on Trade for the version on which\
         the script is being executed"""
        trd_add_info_list = []
        acm_object = 'TradeRegulatoryInfo'
        trd_add_info_17_3 = ['regExchangeId', 'regAlgoId', 'regProvideLiquidity', \
                             'regComplexTrdCmptId', 'regExecutingEntity', 'regVenue', \
                             'regReportingEntity', 'regComdtyDerivInd', 'regSecFinTransInd', \
                             'regRepositoryId', 'regInvesDecidrCrmId', 'regInsCfiCode', \
                             'regInsIsin', 'regLegIsin', 'regTransmOfOrder']
        trd_add_info_17_2 = []
        trd_add_info_17_1 = ['regRptDeferToTime', 'regShortSell']
        trd_add_info_16_5 = ['regConfirmationTime', 'regClearingTime', 'regDirectedOrder', \
                             'regTheirTrader', 'regTheirInvDecider', 'regTheirOrg', \
                             'regOurInvesDecider', 'regBranchMemberShip', 'regOurTransmitOrg',\
                             'regWaiver', 'regOurOrg', 'regTradingCapacity', 'regOTCPostTradeInd']
        trd_add_info_16_4 = ['regIsHedge', 'regClearingBroker', 'regMiddleware', \
                             'regOriginalCpty', 'regRepository',]
        trd_add_info_16_3 = ['regMicroSeconds', 'regClearingHouse', 'regOurTrader']

        trd_add_info_17_2.extend(trd_add_info_17_3)
        trd_add_info_17_1.extend(trd_add_info_17_2)
        trd_add_info_16_5.extend(trd_add_info_17_1)
        trd_add_info_16_4.extend(trd_add_info_16_5)
        trd_add_info_16_3.extend(trd_add_info_16_4)
        if self.acm_version < 2016.4:
            trd_add_info_list = trd_add_info_16_3
            acm_object = 'Trade'
        elif str(self.acm_version) == '2016.4':
            trd_add_info_list = trd_add_info_16_4
            acm_object = 'Trade'
        elif str(self.acm_version) == '2016.5':
            trd_add_info_list = trd_add_info_16_5
        elif str(self.acm_version) == '2017.1':
            trd_add_info_list = trd_add_info_17_1
        elif str(self.acm_version) == '2017.2':
            trd_add_info_list = trd_add_info_17_2
        elif str(self.acm_version) == '2017.3':
            trd_add_info_list = trd_add_info_17_3
        return trd_add_info_list, acm_object

    def get_ins_add_info_list(self):
        """get the list of AddInfos on Instrument for the version on which\
         the script is being executed"""
        ins_add_info_list = []
        acm_object = 'InstrRegulatoryInfo'
        ins_add_info_17_3 = ['regTransactionType', 'regFinalPriceType', \
                             'ESMAIndex', 'regSMS', 'regTrdAdmisAppTime', \
                             'regTrdAdmisReqTime', 'regFirstTradeTime', 'regTrdTerminateDate', \
                             'regHasTrdObligation', 'regSimilarIsin', 'regToTV', \
                             'regLiquidityBand', 'regPrimaryMktMic', 'regMaterialMktMic', \
                             'regDarkCapStatus', 'regDarkCapMic', 'regTickSize', \
                             'regDblVolCapStatus', 'regMiFIDTransparent']
        ins_add_info_17_2 = []
        ins_add_info_17_1 = ['regAvgDailyTO', ]
        ins_add_info_16_5 = ['regIsLiquid', 'regIsSysInternalizr', 'regCmdty']
        ins_add_info_16_4 = ['regLargeInScale', 'regSSTI',]
        ins_add_info_16_3 = ['regClearingIsMandat', 'regCFICode',\
                             'regPostLargeInScale', 'regPostSSTI']

        ins_add_info_17_2.extend(ins_add_info_17_3)
        ins_add_info_17_1.extend(ins_add_info_17_2)
        ins_add_info_16_5.extend(ins_add_info_17_1)
        ins_add_info_16_4.extend(ins_add_info_16_5)
        ins_add_info_16_3.extend(ins_add_info_16_4)
        if self.acm_version < 2016.4:
            ins_add_info_list = ins_add_info_16_3
            acm_object = 'Instrument'
        elif str(self.acm_version) == '2016.4':
            ins_add_info_list = ins_add_info_16_4
            acm_object = 'Instrument'
        elif str(self.acm_version) == '2016.5':
            ins_add_info_list = ins_add_info_16_5
        elif str(self.acm_version) == '2017.1':
            ins_add_info_list = ins_add_info_17_1
        elif str(self.acm_version) == '2017.2':
            ins_add_info_list = ins_add_info_17_2
        elif str(self.acm_version) == '2017.3':
            ins_add_info_list = ins_add_info_17_3
        return ins_add_info_list, acm_object

    def get_contact_add_info_list(self):
        """get the list of AddInfos on Contact for the version on which\
         the script is being executed"""
        contact_add_info_list = []
        acm_object = 'Contact'
        contact_add_info_17_3 = ['dateOfBirth', 'firstName', 'lastName', 'nationalId', \
                               'regContactCrmId', 'regContExchangeId', 'regGeneralPartner']
        contact_add_info_17_2 = []
        contact_add_info_17_1 = ['uniqueName']
        contact_add_info_16_5 = []
        contact_add_info_16_4 = []
        contact_add_info_16_3 = []
        contact_add_info_17_2.extend(contact_add_info_17_3)
        contact_add_info_17_1.extend(contact_add_info_17_2)
        contact_add_info_16_5.extend(contact_add_info_17_1)
        contact_add_info_16_4.extend(contact_add_info_16_5)
        contact_add_info_16_3.extend(contact_add_info_16_4)

        if self.acm_version < 2016.4:
            contact_add_info_list = contact_add_info_16_3
            acm_object = 'Contact'
        elif str(self.acm_version) == '2016.4':
            contact_add_info_list = contact_add_info_16_4
            acm_object = 'Contact'
        elif str(self.acm_version) == '2016.5':
            contact_add_info_list = contact_add_info_16_5
        elif str(self.acm_version) == '2017.1':
            contact_add_info_list = contact_add_info_17_1
        elif str(self.acm_version) == '2017.2':
            contact_add_info_list = contact_add_info_17_2
        elif str(self.acm_version) == '2017.3':
            contact_add_info_list = contact_add_info_17_3
        return contact_add_info_list, acm_object

    def remove_existing_addinfos(self, add_info_list, acm_object):
        """Remove the list of the AddInfos that are not\
         required as ADM columns are present for the versions"""
        add_info_specs = acm.FAdditionalInfoSpec.Select('recType = %s'%acm_object)
        for add_info_spec in add_info_specs:
            if add_info_spec.FieldName() in add_info_list:
                add_info_list.remove(add_info_spec.FieldName())
        return add_info_list

    def TernaryRegulatoryAPIsOnInstrument(self):
        ternary_apis = ['HiQualityLiquidAsset', 'CountryOfIssue', 'BondType',\
                        'BbgCollateralType', 'IsGovernmentGuaranteed',\
                        'IsCovered', 'FundType', 'MainTradingPlace',\
                        'SFTRSecurityType', 'IsEquity', 'OutstandingShares', 'IssuerType']
        instruments = acm.FInstrument.Select('')
        apis_exist = True
        if instruments:
            acm_ins = instruments[0]
            if acm_ins:
                apis_exist = checkTernaryAPIExists(acm_ins, ternary_apis)
        else:
            FRegulatoryLogger.ERROR(logger, "A valid instrument does not exist in ADS. Hence cannot\
                 verify the Regulatory prerequisites on Instrument.")
            apis_exist = False
        return apis_exist

    def TernaryRegulatoryAPIsOnTrade(self):
        ternary_apis = ['IsCleared', 'SFTRIsCollateralProvider',\
                        'SFTRType', 'SFTRAsset', 'SFTRSecurityQuality',\
                        'ISDAMMSProductSubGroup', 'ISDAMMSAssetClass' ]
        trades = acm.FTrade.Select('')
        apis_exist = True
        if trades:
            acm_trd = trades[0]
            if acm_trd:
                apis_exist = checkTernaryAPIExists(acm_trd, ternary_apis)
        else:
            FRegulatoryLogger.ERROR(logger, "A valid trade does not exist in ADS. Hence cannot\
                 verify the Regulatory prerequisites on Trade.")
            apis_exist = False
        return apis_exist

    def TernaryRegulatoryAPIsOnParty(self):
        return True

    def TernaryRegulatoryAPIsOnAccount(self):
        ternary_apis = ['IsAllocated']
        accounts = acm.FAccount.Select('')
        apis_exist = True
        if accounts:
            acm_account = accounts[0]
            if acm_account:
                apis_exist = checkTernaryAPIExists(acm_account, ternary_apis)
        else:
            FRegulatoryLogger.ERROR(logger, "A valid account does not exist in ADS. Hence cannot\
                 verify the Regulatory prerequisites on Account.")
            apis_exist = False
        return apis_exist

    def TernaryRegulatoryAddInfos(self):
        pass
        
    def TestRegulatoryChoiceLists(self):
        """check if the ChoiseLists required for RegulatorySupport is present in ADS"""
        choice_list_vals = {'TradingCapacity' : ['MTCH', 'AOTC', 'DEAL'],\
                            'Waiver' : ['ILQD', 'NLIQ', 'OILQ', 'PRIC', 'RFPT', 'SIZE'],\
                            'OTCPostTradeIndicator' : ['BENC', 'ACTX', 'LRGS', 'ILQD',\
                                'SIZE', 'CANC', 'AMND', 'SDIV', 'RPRI', 'DUPL',\
                                'TNCP', 'TPAC', 'XFPH'],\
                            'CommodityBaseProduct' : ['AGRI', 'NRGY', 'ENVR', 'FRGT',\
                                'FRTL', 'INDP', 'METL', 'MCEX', 'PAPR', 'POLY',\
                                'INFL', 'OEST', 'OTHC', 'OTHR'],\
                            'AGRI' : ['GROS', 'SOFT', 'OOLI', 'DIRY', 'FRST', 'SEAF',\
                                'LSTK', 'GRIN', 'POTA'],\
                            'NRGY' : ['ELEC', 'NGAS', 'OILP', 'COAL',\
                                      'INRG', 'RNNG', 'LGHT', 'DIST'],\
                            'ENVR' : ['EMIS', 'WTHR', 'CRBR'],\
                            'FRGT' : ['WETF', 'DRYF'],\
                            'FRTL' : ['AMMO', 'DAPH', 'PTSH', 'SLPH', 'UREA', 'UAAN'],\
                            'INDP' : ['CSTR', 'MFTG'],\
                            'METL' : ['NPRM', 'PRME'],\
                            'PAPR' : ['CBRD', 'NSPT', 'PULP', 'RCVP'],\
                            'POLY' : ['PLST'],\
                            'GROS' : ['FWHT', 'SOYB', 'CORN', 'RPSD', 'OTHR', 'RICE'],\
                            'SOFT' : ['CCOA', 'ROBU', 'WHSG', 'BRWN', 'OTHR'],\
                            'OOLI' : ['LAMP'],\
                            'GRIN' : ['MWHT'],\
                            'ELEC' : ['BSLD', 'FITR', 'PKLD', 'OFFP', 'OTHR'],\
                            'NGAS' : ['GASP', 'LNGG', 'NBPG', 'NCGG', 'TTFG'],\
                            'OILP' : ['BAKK', 'BDSL', 'BRNT', 'BRNX', 'CNDA',\
                                'COND', 'DSEL', 'DUBA', 'ESPO', 'ETHA', 'FUEL',\
                                'FOIL', 'GOIL', 'GSLN', 'HEAT', 'JTFL', 'KERO',\
                                'LLSO', 'MARS', 'NAPH', 'NGLO', 'TAPI', 'URAL', 'WTIO'],\
                            'EMIS' : ['CERE', 'ERUE', 'EUAE', 'EUAA', 'OTHR'],\
                            'WETF' : ['TNKR'],\
                            'DRYF' : ['DBCR'],\
                            'NPRM' : ['ALUM', 'ALUA', 'CBLT', 'COPR', 'IRON',\
                                'LEAD', 'MOLY', 'NASC', 'NICK', 'STEL', 'TINN',\
                                'ZINC', 'OTHR'],\
                            'PRME' : ['GOLD', 'SLVR', 'PTNM', 'PLDM', 'OTHR'],\
                            'TransactionType' : ['FUTR', 'OPTN', 'TAPO', 'SWAP',\
                                'MINI', 'OTCT', 'ORIT', 'CRCK', 'DIFF', 'OTHR'],\
                            'FinalPriceType' : ['ARGM', 'BLTC', 'EXOF',\
                                                'GBCL', 'IHSM', 'PLAT', 'OTHR'],\
                            'FinancialCategory' : ['FC', 'NFC', 'NFC+', 'NFC-'],\
                            'ESMAIndex' : ['EONA', 'EONS', 'EURI', 'EUUS', 'EUCH',\
                                'GCFR', 'ISDA', 'LIBI', 'LIBO', 'MAAA', 'PFAN',\
                                'TIBO', 'STBO', 'BBSW', 'JIBA', 'BUBO', 'CDOR',\
                                'CIBO', 'MOSP', 'NIBO', 'PRBO', 'TLBO', 'WIBO',\
                                'TREA', 'SWAP', 'FUSW'],\
                            'MiFIDCategory' : ['Professional', 'Retail', 'Eligible'],\
                            'DoubleVolumeCapStatus' : ['Exceeded', 'Near', 'Normal'],\
                            'DarkCapStatus' : ['Exceeded', 'Near', 'Normal'],
                            'ShortSellIndicator' : ['Sell Short', 'Buy Cover',\
                                'Sell Short Exempt', 'Sell Short Undi']}
        all_choice_list_exists = True
        for choice_list in choice_list_vals:
            choice_list_exists = checkChoiceLists(\
                choice_list, choice_list_vals[choice_list])
            if not choice_list_exists:
                all_choice_list_exists = False
        return all_choice_list_exists

