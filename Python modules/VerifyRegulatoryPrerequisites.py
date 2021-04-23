import acm
try:
    import FIntegrationUtils
except:
    raise Exception("Import the RegulatorySupport/built-in RegulatoryInfo module to progress any futher.")
acm_version = FIntegrationUtils.FIntegrationUtils.get_acm_version_override()
def validateRegulatoryPrerequisites(acm_object, attr_list):
    acm_object_type = None
    reg_info = None
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
    try:
        reg_info = acm_object.RegulatoryInfo()
    except:
        print(("RegulatoryInfo instance on the %s is not accessible. Import the RegulatorySupport package for expected functionality."%acm_object_type))
    if reg_info:
        for each_api in attr_list:
            try:
                attr_val = eval('reg_info.' + each_api + '()')
            except:
                print(("API <%s> is not found on %s.RegulatoryInfo"%(each_api, acm_object_type)))

def checkInstrumentRegulatoryPrerequisites():
    ins_reg_list = ['TradingTerminationDate', 'FirstTradingTime', 'AdmissionRequestTime', \
                    'AdmissionApprovalTime', 'HasTradingObligation', 'AverageDailyTurnover', \
                    'IsSystematicInternaliser', 'IsLiquid', 'StandardMarketSize', \
                    'SizeSpecificToInstrument', 'LargeInScale', 'CfiCode', 'ClearingIsMandatory', \
                    'CommodityBaseProduct', 'CommoditySubProduct', 'CommodityFurtherSubProduct', \
                    'FinalPriceType', 'TransactionType', 'SimilarIsin', 'IsTradedOnTradingVenue', \
                    'LiquidityBand', 'InstypeRTS2', 'InsSubtypeRTS2', 'PrimaryMarketMic', \
                    'MaterialMarketMic', 'DarkCapMic', 'DarkCapStatus', 'DoubleVolumeCapStatus', \
                    'TickSize', 'IsMiFIDTransparent', 'SizeSpecificToInstrumentInCurrency', \
                    'PostSizeSpecificToInstrument', 'PostSizeSpecificToInstrumentInCurrency', \
                    'LargeInScaleInCurrency', 'PostLargeInScale', 'PostLargeInScaleInCurrency', \
                    'FinancialInstrumentShortName', 'InstypeRTS28', 'IsEquityLike', 'IsBondLike', \
                    'IsInterestRateDerivative', 'IsEquityDerivative', 'IsC10Derivative', 'IsFxDerivative', 'IsCFD']
    instruments = acm.FInstrument.Select('')
    if instruments:
        acm_ins = instruments[0]
        if acm_ins:
            validateRegulatoryPrerequisites(acm_ins, ins_reg_list)
    else:
        print ("A valid instrument does not exist in ADS. Hence cannot verify the Regulatory prerequisites on Instrument.")

def checkTradeRegulatoryPrerequisites():
    trade_reg_list = ['RepositoryId', 'ClearingBroker', 'ClearingHouse',\
                      'Middleware', 'OriginalCounterparty', 'Repository',\
                      'TradingCapacity', 'ComplexTradeComponentId', 'OurOrganisation',\
                      'OurTransmittingOrganisation', 'OurInvestmentDecider', 'OurTrader',\
                      'ExecutingEntity', 'Venue', 'BranchMembership', 'TheirOrganisation',\
                      'TheirInvestmentDecider', 'TheirTrader', 'Waiver', 'WaiverString',\
                      'OtcPostTradeIndicator', 'OtcPostTradeIndicatorString', 'IsCommodityDerivative',\
                      'IsSecurityFinancingTransaction', 'ReportingEntity', 'ExchangeId',\
                      'AlgoId', 'DirectedOrder', 'IsProvidingLiquidity', 'IsHedge', 'TimePrecision',\
                      'TradeTimeWithPrecision', 'TimePrecisionInUTC', 'ReportDeferToTime',\
                      'ConfirmationTime', 'ClearingTime', 'InvestmentDeciderCrmId', 'Isin',\
                      'CfiCode', 'NearLegIsin', 'FarLegIsin', 'TransmissionOfOrdersIndicator', 'OurOrg', 'TheirOrg']
    trades = acm.FTrade.Select('')
    if trades:
        acm_trd = trades[0]
        if acm_trd:
            validateRegulatoryPrerequisites(acm_trd, trade_reg_list)
    else:
        print ("A valid trade does not exist in ADS. Hence cannot verify the Regulatory prerequisites on Trade.")

def checkPartyRegulatoryPrerequisites():
    party_reg_list = ['IsInvestmentFirm', 'PossibleReporter', 'FinancialCategory', \
                      'MIC', 'IsAlgorithm', 'ExchangeId', 'CrmId', 'MiFIDCategory', \
                      'ClientType', 'IsVenue']
    parties = acm.FParty.Select('')
    if parties:
        acm_party = parties[0]
        if acm_party:
            validateRegulatoryPrerequisites(acm_party, party_reg_list)
    else:
        print ("A valid party does not exist in ADS. Hence cannot verify the Regulatory prerequisites on Party.")

def checkContactRegulatoryPrerequisites():
    contact_reg_list = ['DateOfBirth', 'FirstName', 'LastName', 'NationalId',\
                        'CrmId', 'ExchangeId', 'UniqueName', 'ClientType', 'JointAccount', 'IsGeneralPartner']
    contacts = acm.FContact.Select('')
    if contacts:
        acm_contact = contacts[0] 
        if acm_contact:
            validateRegulatoryPrerequisites(acm_contact, contact_reg_list)
    else:
        print ("A valid contact does not exist in ADS. Hence cannot verify the Regulatory prerequisites on Contact.")

def checkPersonRegulatoryPrerequisites():
    person_reg_list = ['DateOfBirth', 'FirstName', 'LastName', 'NationalId', \
                        'CrmId', 'ExchangeId', 'ClientType', 'Contact']
    try:
        persons = acm.FPerson.Select('')
        if persons:
            acm_person = persons[0] 
            if acm_person:
                validateRegulatoryPrerequisites(acm_person, person_reg_list)
        else:
            print ("A valid person does not exist in ADS. Hence cannot verify the Regulatory prerequisites on Person.")
    except:#it means object doesnt exist on this version
        pass

def get_trd_add_info_list(acm_version):
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
    if acm_version < 2016.4:
        trd_add_info_list = trd_add_info_16_3
        acm_object = 'Trade'
    elif str(acm_version) == '2016.4':
        trd_add_info_list = trd_add_info_16_4
        acm_object = 'Trade'
    elif str(acm_version) == '2016.5':
        trd_add_info_list = trd_add_info_16_5
    elif str(acm_version) == '2017.1':
        trd_add_info_list = trd_add_info_17_1
    elif str(acm_version) == '2017.2':
        trd_add_info_list = trd_add_info_17_2
    elif str(acm_version) == '2017.3':
        trd_add_info_list = trd_add_info_17_3
    return trd_add_info_list, acm_object

def get_ins_add_info_list(acm_version):
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
    ins_add_info_16_3 = ['regClearingIsMandat', 'regCFICode', 'regPostLargeInScale', 'regPostSSTI']
    
    ins_add_info_17_2.extend(ins_add_info_17_3)
    ins_add_info_17_1.extend(ins_add_info_17_2)
    ins_add_info_16_5.extend(ins_add_info_17_1)
    ins_add_info_16_4.extend(ins_add_info_16_5)
    ins_add_info_16_3.extend(ins_add_info_16_4)
    if acm_version < 2016.4:
        ins_add_info_list = ins_add_info_16_3
        acm_object = 'Instrument'
    elif str(acm_version) == '2016.4':
        ins_add_info_list = ins_add_info_16_4
        acm_object = 'Instrument'
    elif str(acm_version) == '2016.5':
        ins_add_info_list = ins_add_info_16_5
    elif str(acm_version) == '2017.1':
        ins_add_info_list = ins_add_info_17_1
    elif str(acm_version) == '2017.2':
        ins_add_info_list = ins_add_info_17_2
    elif str(acm_version) == '2017.3':
        ins_add_info_list = ins_add_info_17_3
    return ins_add_info_list, acm_object

def get_contact_add_info_list(acm_version):
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

    if acm_version < 2016.4:
        contact_add_info_list = contact_add_info_16_3
        acm_object = 'Contact'
    elif str(acm_version) == '2016.4':
        contact_add_info_list = contact_add_info_16_4
        acm_object = 'Contact'
    elif str(acm_version) == '2016.5':
        contact_add_info_list = contact_add_info_16_5
    elif str(acm_version) == '2017.1':
        contact_add_info_list = contact_add_info_17_1
    elif str(acm_version) == '2017.2':
        contact_add_info_list = contact_add_info_17_2
    elif str(acm_version) == '2017.3':
        contact_add_info_list = contact_add_info_17_3
    return contact_add_info_list, acm_object
    
def remove_existing_addinfos(add_info_list, acm_object):
    add_info_specs = acm.FAdditionalInfoSpec.Select('recType = %s'%acm_object)
    for add_info_spec in add_info_specs:
        if add_info_spec.FieldName() in add_info_list:
            add_info_list.remove(add_info_spec.FieldName())
    return add_info_list

def checkInstrumentRegAddInfos():
    ins_add_infos, acm_object = get_ins_add_info_list(acm_version)
    add_info_list = remove_existing_addinfos(ins_add_infos, acm_object)
    for add_info in add_info_list:
        if add_info == 'ESMAIndex' and acm_object == 'InstrRegulatoryInfo':
            acm_object = 'Instrument'
            add_info_specs = acm.FAdditionalInfoSpec.Select('recType = %s'%acm_object)
            for add_info_spec in add_info_specs:
                if add_info_spec.FieldName() in ins_add_infos:
                    add_info_list.remove(add_info_spec.FieldName())

    if len(add_info_list) > 0:
        print ("The following Insrument Regulatory-AddInfos are not present in ADS:")
        for add_info in add_info_list:
            print (add_info)

def checkTradeRegAddInfos():
    trd_add_infos, acm_object = get_trd_add_info_list(acm_version)
    add_info_list = remove_existing_addinfos(trd_add_infos, acm_object)
    for add_info in add_info_list:
        if add_info == 'regShortSell' and acm_object == 'TradeRegulatoryInfo':
            acm_object = 'Trade'
            add_info_specs = acm.FAdditionalInfoSpec.Select('recType = %s'%acm_object)
            for add_info_spec in add_info_specs:
                if add_info_spec.FieldName() in trd_add_infos:
                    add_info_list.remove(add_info_spec.FieldName())
    if len(add_info_list) > 0:
        print ("The following Trade Regulatory-AddInfos are not present in ADS:")
        for add_info in add_info_list:
            print (add_info)

def checkPartyRegAddInfos():
    party_add_info_list = ['regIsInvestmentFirm', 'regPossibleReporter', \
                           'regFinancialCategor', 'regIsAlgorithm', 'regPtyExchangeId', \
                           'regPtyCrmId', 'regMifidCategory']
    acm_object = 'Party'
    add_info_list = remove_existing_addinfos(party_add_info_list, acm_object)
    if len(add_info_list) > 0:
        if len(add_info_list) == 1 and acm_version >= 2017.4 and add_info_list[0] == 'regIsVenue':
            pass
        else:
            print ("The following Party Regulatory-AddInfos are not present in ADS:")
            for add_info in add_info_list:
                if acm_version >= 2017.4 and add_info_list[0] == 'regIsVenue':
                    pass
                else:
                    print (add_info)
    
def checkContactRegAddInfos():
    contact_add_infos, acm_object = get_contact_add_info_list(acm_version)
    add_info_list = remove_existing_addinfos(contact_add_infos, acm_object)
    if len(add_info_list) > 0:
        print ("The following Contact Regulatory-AddInfos are not present in ADS:")
        for add_info in add_info_list:
            print (add_info)

def checkRegulatoryPrerequisites():
    checkInstrumentRegulatoryPrerequisites()
    checkTradeRegulatoryPrerequisites()
    checkPartyRegulatoryPrerequisites()
    checkContactRegulatoryPrerequisites()
    #checkPersonRegulatoryPrerequisites()

def checkRegulatoryAddInfos():
    checkInstrumentRegAddInfos()
    checkTradeRegAddInfos()
    checkPartyRegAddInfos()
    checkContactRegAddInfos()

def checkRegulatoryChoiceLists():
    choice_lists = ['TradingCapacity', 'Waiver', 'OTCPostTradeIndicator', \
                   'CommodityBaseProduct', 'AGRI', 'NRGY', 'ENVR', 'FRGT', \
                   'FRTL', 'INDP', 'METL', 'PAPR', 'POLY', 'GROS', 'SOFT', \
                   'OOLI', 'GRIN', 'ELEC', 'NGAS', 'OILP', 'EMIS', 'WETF', \
                   'DRYF', 'NPRM', 'PRME', 'TransactionType', 'FinalPriceType', \
                   'FinancialCategory', 'ESMAIndex', 'MiFIDCategory', \
                   'DoubleVolumeCapStatus', 'DarkCapStatus']
    for choice_list in choice_lists:
        if not acm.FChoiceList.Select('name = %s'%choice_list):
            print(("ChoiceList <%s> is required for the expected functionality of RegulatorySupport package"%choice_list))
checkRegulatoryPrerequisites()
print ("Verification of APIs complete")
checkRegulatoryAddInfos()
print ("Verification of AddInfos complete")
checkRegulatoryChoiceLists()
print ("Verification of ChoiceLists complete")
print ("**********Verification Complete**********")
