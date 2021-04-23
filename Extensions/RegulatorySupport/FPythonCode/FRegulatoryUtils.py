"""------------------------------------------------------------------------
MODULE
    FRegulatoryUtils -
DESCRIPTION:
    This file is used for the generic functionality that is used across RegulatoryReporting component
VERSION: 1.0.25(0.25.7)
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported.
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import FRegulatoryLogger
try:
    import FTradeRegulatoryInfo
    import FInstrumentRegulatoryInfo
except:
    pass
import FPartyRegulatoryInfo
import FContactRegulatoryInfo
import FIntegrationUtils
import acm
import ael
import inspect
from datetime import datetime
from datetime import timedelta
import locale
import time
import re
import FRegulatoryInfoException
integration_utils = FIntegrationUtils.FIntegrationUtils()
logger = 'FRegulatoryUtils'
add_info_dict_16_4 = ['regClearingIsMandatory', 'regClearingIsMandat', 'regCFICode', 'regClearingHouse', 'regMicroSeconds']
add_info_dict_16_5 = ['regSSTI', 'regLargeInScale', 'regClearingBroker', 'regMiddleware', 'regOriginalCpty', 'regIsHedge', 'regRepository']
add_info_dict_17_1 = ['regTradingCapacity', 'regOurOrg', 'regOurTransmitOrg', 'regOurInvesDecider', 'regBranchMemberShip', 'regTheirOrg', 'regTheirInvDecider', 'regTheirTrader', 'regDirectedOrder', 'regConfirmationTime', 'regClearingTime', 'regWaiver', 'regIsLiquid', 'regIsSysInternalizr', 'regCmdty', 'regOTCPostTradeInd', ]
add_info_dict_17_2 = ['uniqueName', 'regRptDeferToTime', 'regAvgDailyTO']

adm_attribute = {
                    'regClearingIsMandatory': 'clearingIsMandatory',
                    'regClearingIsMandat': 'clearingIsMandatory',
                    'regCFICode': 'cfiCode',
                    'regClearingHouse': 'clearingHouse',
                    'regMicroSeconds': 'timePrecision',
                    'regClearingBroker': 'clearingBroker',
                    'regMiddleware': 'middleware',
                    'regOriginalCpty': 'originalCounterparty',
                    'regIsHedge': 'isHedge',
                    'regSSTI': 'sizeSpecificToInstrument',
                    'regLargeInScale': 'largeInScale',
                    'regRepository': 'repository',
                    'regTradingCapacity': 'tradingCapacity',
                    'regWaiver': 'waiver',
                    'regOurOrg': 'ourOrganisation',
                    'regOurTransmitOrg': 'ourTransmittingOrganisation',
                    'regOurInvesDecider': 'ourInvestmentDecider',
                    'regOurTrader': 'ourTrader',
                    'regBranchMemberShip': 'branchMembership',
                    'regTheirOrg': 'theirOrganisation',
                    'regTheirInvDecider': 'theirInvestmentDecider',
                    'regTheirTrader': 'theirTrader',
                    'regDirectedOrder': 'directedOrder',
                    'regConfirmationTime': 'confirmationTime',
                    'regClearingTime': 'clearingTime',
                    'regIsLiquid': 'isLiquid',
                    'regIsSysInternalizr': 'isSystematicInternaliser',
                    'regCmdty': 'commodityProduct',
                    'uniqueName': 'uniqueName',
                    'regRptDeferToTime': 'reportDeferToTime',
                    'regAvgDailyTO': 'averageDailyTurnover',
                    'regOTCPostTradeInd': 'otcPostTradeIndicator',
                }

add_info_Trade = {'clearingBroker': 'regClearingBroker',
'clearingHouse': 'regClearingHouse',
'middleware': 'regMiddleware',
'originalCounterparty': 'regOriginalCpty',
'repository': 'regRepository',
'tradingCapacity': 'regTradingCapacity',
'complexTradeComponentId': 'regComplexTrdCmptId',
'waiver': 'regWaiver',
'waiverString': 'regWaiver',
'ourOrganisation': 'regOurOrg',
'ourTransmittingOrganisation': 'regOurTransmitOrg',
'ourInvestmentDecider': 'regOurInvesDecider',
'ourTrader': 'regOurTrader',
'executingEntity': 'regExecutingEntity',
'venue': 'regVenue',
'branchMembership': 'regBranchMemberShip',
'theirOrganisation': 'regTheirOrg',
'theirInvestmentDecider': 'regTheirInvDecider',
'theirTrader': 'regTheirTrader',
'reportingEntity': 'regReportingEntity',
'otcPostTradeIndicator': 'regOTCPostTradeInd',
'otcPostTradeIndicatorString': 'regOTCPostTradeInd',
'isCommodityDerivative': 'regComdtyDerivInd',
'isSecurityFinancingTransaction': 'regSecFinTransInd',
'timePrecision': 'regMicroSeconds',
'repositoryId': 'regRepositoryId',
'algoId': 'regAlgoId',
'directedOrder': 'regDirectedOrder',
'exchangeId': 'regExchangeId',
'isHedge': 'regIsHedge',
'isProvidingLiquidity': 'regProvideLiquidity',
'confirmationTime': 'regConfirmationTime',
'clearingTime': 'regClearingTime',
'reportDeferToTime': 'regRptDeferToTime',
'investmentDeciderCrmId': 'regInvesDecidrCrmId',
'cfiCode': 'regInsCfiCode',
'isin': 'regInsIsin',
'nearLegIsin': 'regNearLegIsin',
'farLegIsin': 'regFarLegIsin',
'transmissionOfOrdersIndicator': 'regTransmOfOrder',
}

add_info_Instrument = {'cfiCode': 'regCFICode',
             'clearingIsMandatory': 'regClearingIsMandat',
             #'commodityBaseProduct' : 'regCmdtyBaseProduct',
             #'commodityFurtherSubProduct' : 'regCmdtyFurtherSub',
             #'commoditySubProduct' : 'regCmdtySubProduct',
             'commodityBaseProduct': 'regCmdty',
             'commodityFurtherSubProduct': 'regCmdty',
             'commoditySubProduct': 'regCmdty',
             'finalPriceType': 'regFinalPriceType',
             'transactionType': 'regTransactionType',
             'firstTradingTime': 'regFirstTradeTime',
             'isLiquid':       'regIsLiquid',
             'isSystematicInternaliser': 'regIsSysInternalizr',
             'largeInScale': 'regLargeInScale',
             'sizeSpecificToInstrument': 'regSSTI',
             'postLargeInScale': 'regPostLargeInScale',
             'postSizeSpecificToInstrument': 'regPostSSTI',
             'standardMarketSize': 'regSMS',
             'admissionApprovalTime': 'regTrdAdmisAppTime',
             'admissionRequestTime': 'regTrdAdmisReqTime',
             'tradingTerminationDate': 'regTrdTerminateDate',
             #'financialInstrumentShortName' : 'FISN',
             'similarIsin': 'regSimilarIsin',
             'hasTradingObligation': 'regHasTrdObligation',
             'averageDailyTurnover': 'regAvgDailyTO',
             'isTradedOnTradingVenue': 'regToTV',
             'liquidityBand': 'regLiquidityBand',
             'primaryMarketMic': 'regPrimaryMktMic',
             'materialMarketMic': 'regMaterialMktMic',
             'darkCapStatus': 'regDarkCapStatus',
             'doubleVolumeCapStatus': 'regDblVolCapStatus',
             'darkCapMic': 'regDarkCapMic',
             'tickSize': 'regTickSize',
             'isMiFIDTransparent': 'regMiFIDTransparent',
            }


add_info_Party = {'financialCategory' : 'regFinancialCategor',
'isInvestmentFirm' : 'regIsInvestmentFirm',
'possibleReporter' : 'regPossibleReporter',
'mIC' : 'MIC',
'mic' : 'MIC',
'MIC' : 'MIC',
'isAlgorithm' : 'regIsAlgorithm',
'exchangeId' : 'regPtyExchangeId',
'crmId' : 'regPtyCrmId',
'miFIDCategory' : 'regMifidCategory',
'isVenue' : 'regIsVenue'}

add_info_Contact = {
'dateOfBirth' : 'dateOfBirth',
'firstName' : 'firstName',
'lastName' : 'lastName',
'nationalId' : 'nationalId',
'crmId' : 'regContactCrmId',
'exchangeId' : 'regContExchangeId',
'uniqueName' : 'uniqueName',
'isGeneralPartner' : 'regGeneralPartner'}

add_info_Person = {
'dateOfBirth' : 'dateOfBirth',
'firstName' : 'firstName',
'lastName' : 'lastName',
'nationalID' : 'nationalId',
'cRMid' : 'cRMid'}

log_list = {
            'FTradeRegulatoryInfo': {
                                    'IGNORE': ['__init__', '__setattr__', 'Delete', 'Commit', '_FTradeRegulatoryInfo__validate_party', 'Attributes'], \
                                    'NAME': ['Venue', 'TheirOrganisation', 'Repository', 'ReportingEntity', 'OurTransmittingOrganisation', \
                                             'OriginalCounterparty', 'Middleware', 'ExecutingEntity', 'ClearingBroker', 'ClearingHouse', \
                                             'BranchMembership', 'OurOrganisation', 'OurOrg', 'TheirOrg'], \
                                    'OID' : ['Trade'], \
                                    'FULLNAME' : ['TheirInvestmentDecider', 'TheirTrader', 'OurTrader', 'OurInvestmentDecider']
                                    },
            'FInstrumentRegulatoryInfo': {
                                    'IGNORE': ['__init__', '__setattr__', 'Delete', 'Commit', 'Attributes', \
                                               'LargeInScaleInCurrency', 'PostLargeInScaleInCurrency', \
                                               'PostSizeSpecificToInstrumentInCurrency', 'SizeSpecificToInstrumentInCurrency'], \
                                    'OID' : ['Instrument'],
                                    'NAME': ['TransactionType', 'FinalPriceType', 'CommodityBaseProduct', \
                                             'CommoditySubProduct', 'CommodityFurtherSubProduct', 'DarkCapStatus', 'DoubleVolumeCapStatus' ]
                                    },
            'FPartyRegulatoryInfo': {
                                    'IGNORE': ['__init__', '__setattr__', 'Delete', 'Commit', 'Attributes'], \
                                    'OID' : ['Party']
                                    },
            'FContactRegulatoryInfo': {
                                    'IGNORE': ['__init__', '__setattr__', 'Delete', 'Commit', 'Attributes'], \
                                    'OID' : ['Contact']
                                    },
            'FPersonRegulatoryInfo': {
                                    'IGNORE': ['__init__', '__setattr__', 'Delete', 'Commit', 'Attributes'], \
                                    'OID' : ['Contact']
                                    }
            }

class WAIVER:
    NONE, SIZE, RFPT, PRIC, OILQ, NLIQ, ILQD = list(range(7))
class OTCPOSTTRADEINDICATOR:
    NONE, BENC, ACTX, LRGS, ILQD, SIZE, CANC, AMND, SDIV, RPRI, DUPL, TNCP, TPAC, XFPH = list(range(14))

def get_choicelist_pos(choicelist_val, choicelist_name):
    choicelist = eval(choicelist_name)
    reverse_dict = dict(list(zip(list(choicelist.values()), list(choicelist.keys()))))
    if choicelist_val in reverse_dict:
        return reverse_dict[choicelist_val]

def get_choicelist_name(binary_val, choicelist_name):
    addinfo_val = ''
    counter = 0
    arr_names = []
    for eachVal in binary_val:
        if eachVal == '1':
            addinfo_val = eval(choicelist_name + '[' + str(counter) + ']')
            arr_names.append(addinfo_val)
        counter = counter + 1
    arr_names = sorted(arr_names)
    addinfo_val = ','.join(arr_names)
    return addinfo_val.strip()

def get_query(acm_object, obj_oid_reference):
    if 'RegulatoryInfo' in acm_object:
        query = "acm." + acm_object + "[" + obj_oid_reference + "]"
    else:
        query = acm_object + "RegulatoryInfo." + acm_object + "RegulatoryInfo(acm." + acm_object + "[" + obj_oid_reference + "]" + ")"
    return query

def get_query_from_acm_object(acm_object, object):
    query = acm_object + "RegulatoryInfo(object." + acm_object[1:] + "())"
    return query

def Select(query, acm_object, related_acm_object = None):
    query_result = None
    query = query.replace("'", "")
    query = query.replace('"', "")
    return_result = []
    if query == '':#it means we have to pull out data for all
        acm_objects = eval("acm." + acm_object + ".Select('')")
        for acm_object_val in acm_objects:
            query = get_query(acm_object, str(acm_object_val.Oid()))
            reg_info = eval(query)
            return_result.append(reg_info)
    elif query.find('=') == -1:
        FRegulatoryLogger.ERROR(logger, "Kindly provide a valid query. The query <%s> provided is incorrect"%query)
    else:
        query_split = query.split('=')
        ais = query_split[0].strip()

        if acm_object in ['FTrade', 'FTradeRegulatoryInfo']:
            if ais in add_info_Trade:
                ais = add_info_Trade[ais]
        if acm_object in ['FInstrument', 'FInstrumentRegulatoryInfo']:
            if ais in add_info_Instrument:
                ais = add_info_Instrument[ais]
        if acm_object == 'FParty':
            if ais in add_info_Party:
                ais = add_info_Party[ais]
        if acm_object == 'FContact':
            if ais in add_info_Contact:
                ais = add_info_Contact[ais]
        val = query_split[1].strip()
        if str(val).upper() == 'NONE':
            FRegulatoryLogger.ERROR(logger, "Kindly provide a valid value to look for within the query.")
            return
        if ais == 'dateOfBirth':
            aelDateVal = ael.date_from_string(val)
            val = aelDateVal.to_string(ael.DATE_ISO)
        if ais in ['timePrecision', 'regTimePrecision']:
            FRegulatoryLogger.INFO(logger, "Select query on TimePrecision is currently not supported")
            return None
        if ais == 'regCmdty':
            fieldValue = None
            chs = acm.FChoiceList.Select('name = %s'%val)
            for ch in chs:
                if ch.List() != 'MASTER':
                    fieldValue = ch
                    break
            if fieldValue:
                if integration_utils.get_acm_version_override() >= 2017.1:
                    query = "acm." + acm_object + '.Select("' + "commodityProduct = %d" + '"%(int(' + str(fieldValue.Oid()) + ')))'
                    query_result = eval(query)
                else:
                    query_result = acm.FAdditionalInfo.Select(query = "addInf = '%s' and fieldValue = '%s' "%(ais.strip(), str(fieldValue.Oid())))
            else:
                FRegulatoryLogger.ERROR(logger, "There is no valid Choicelist with value <%s>"%val)
        if ais.strip() in ['regWaiver', 'regOTCPostTradeInd'] and (query_split[0]).strip() in ['waiverString', 'otcPostTradeIndicatorString']:
            multiple_choice_string = None
            query_result = []
            multiple_choice_string = (query_split[1]).strip()
            choices = multiple_choice_string.split(',')
            if integration_utils.get_acm_version_override() >= 2017.1 and ais.strip() in ['regWaiver', 'regOTCPostTradeInd']:
                reg_infos = acm.FTradeRegulatoryInfo.Select('')
                for reg_info in reg_infos:
                    counter = 0
                    regInfoChoices = None
                    if ais.strip() == 'regWaiver':
                        regInfoChoices = reg_info.WaiverString()
                    if ais.strip() == 'regOTCPostTradeInd':
                        regInfoChoices = reg_info.OtcPostTradeIndicatorString()
                    for choiceVal in choices:
                        if regInfoChoices and choiceVal.strip() in regInfoChoices:
                            counter = counter + 1
                    if counter == len(choices):
                        query_result.append(reg_info)
            else:
                add_info_list = acm.FAdditionalInfo.Select("addInf = '%s'"%ais.strip())
                for add_info in add_info_list:
                    try:
                        orig_parent = add_info.RecType()
                    except:
                        orig_parent = 'Trade'
                    counter = 0
                    regInfoChoices = None
                    if orig_parent == 'Trade':
                        parent = acm.FTrade[add_info.Recaddr()]
                        if parent:
                            if ais.strip() == 'regWaiver':
                                regInfoChoices = parent.RegulatoryInfo().WaiverString()
                            else:
                                regInfoChoices = parent.RegulatoryInfo().OtcPostTradeIndicatorString()
                    else:
                        parent = None
                        try:
                            parent = acm.FTradeRegulatoryInfo[add_info.Recaddr()]
                            if parent:
                                if ais.strip() == 'regWaiver':
                                    regInfoChoices = parent.WaiverString()
                                else:
                                    regInfoChoices = parent.OtcPostTradeIndicatorString()
                        except:
                            pass
                    if regInfoChoices:
                        for choiceVal in choices:
                            if choiceVal.strip() in regInfoChoices:
                                counter = counter + 1
                        if counter == len(choices):
                            query_result.append(add_info)
        if (not query_result) and ais in add_info_dict_17_2 and integration_utils.get_acm_version_override() >= 2017.2:
            ais = adm_attribute[ais]
            query = None
            if ais == 'averageDailyTurnover':
                query = "acm." + acm_object + '.Select("' + "%s = %f" + '"%("' + ais + '",' + val + '))'
            elif ais == 'reportDeferToTime':
                val = acm.Time().LocalToUtc(val)
                query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '",' + "'" + str(val) + "'))"
            elif ais == 'uniqueName':
                query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '",' + "'" + str(val) + "'))"
            else:
                query = "acm." + acm_object + 'Select("' + "%s = '%s'" + '"%("' + ais + '",' + "'" + val + "'))"
            query_result = eval(query)
        if (not query_result) and ais in add_info_dict_17_1 and integration_utils.get_acm_version_override() >= 2017.1:
            ais = adm_attribute[ais]
            query = None
            if ais in ['directedOrder', 'isLiquid', 'isSystematicInternaliser', 'clearingIsMandatory']:
                infer_val = None
                if integration_utils.get_acm_version_override() == 2017.1:#these flags are boolean
                    if str(val).upper() in ['YES', 'TRUE', '1']:
                        infer_val = 'True'
                    elif str(val).upper() in ['NO', 'FALSE', '0']:
                        infer_val = 'False'
                    else:
                        infer_val = 'None'
                    query = "acm." + acm_object + '.Select("' + "%s = %s" + '"%("' + ais + '",' + infer_val + '))'
                else:
                    if str(val).upper() in ['YES', 'TRUE', '1']:
                        infer_val = '1'
                    elif str(val).upper() in ['NO', 'FALSE', '2']:
                        infer_val = '2'
                    elif str(val).upper() in ['NONE', '0']:
                        infer_val = '0'
                    query = "acm." + acm_object + '.Select("' + "%s = %s" + '"%("' + ais + '",int(' + infer_val + ')))'
            else:
                if ais in ['waiver', 'otcPostTradeIndicator']:
                    query = "acm." + acm_object + '.Select("' + "%s = %d" + '"%("' + ais + '",int(' + val + ')))'
                elif ais in ['confirmationTime', 'clearingTime']:
                    result_utc_datetime = acm.Time().LocalToUtc(val)
                    query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '","' + result_utc_datetime + '"))'
                elif ais in ['theirTrader', 'ourTrader', 'ourInvestmentDecider', 'theirInvestmentDecider'] and (not val.isdigit()):
                    contacts = acm.FContact.Select("fullname = '%s'"%val)
                    if contacts:
                        if len(contacts) > 1:
                            FRegulatoryLogger.ERROR(logger, "There are more than one contacts with name <%s>"%val)
                        val = str(contacts[0].Oid())
                        query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '","' + val + '"))'
                else:
                    query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '","' + val + '"))'
            query_result = eval(query)
        if (not query_result) and ais in add_info_dict_16_5 and integration_utils.get_acm_version_override() >= 2016.5:
            ais = adm_attribute[ais]
            query = None
            if ais in ['isHedge']:
                infer_val = None
                if str(integration_utils.get_acm_version_override()) in ['2016.5', '2017.1']:#these flags are boolean
                    if str(val).upper() in ['YES', 'TRUE', '1']:
                        infer_val = '1'
                    elif str(val).upper() in ['NO', 'FALSE', '0', 'NONE']:
                        infer_val = '0'
                else:
                    if str(val).upper() in ['YES', 'TRUE', '1']:
                        infer_val = '1'
                    elif str(val).upper() in ['NO', 'FALSE', '2']:
                        infer_val = '2'
                    elif str(val).upper() in ['NONE', '0']:
                        infer_val = '0'
                query = "acm." + acm_object + '.Select("' + "%s = %d" + '"%("' + ais + '",int(' + infer_val + ')))'
            elif ais in ['clearingIsMandatory', 'isHedge', 'sizeSpecificToInstrument', 'largeInScale', 'postLargeInScale', 'postSizeSpecificToInstrument']:
                query = "acm." + acm_object + '.Select("' + "%s = %s" + '"%("' + ais + '","' + str(val) + '"))'
            else:
                query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '","' + val + '"))'
            query_result = eval(query)
        if (not query_result) and ais in add_info_dict_16_4 and integration_utils.get_acm_version_override() >= 2016.4:
            ais = adm_attribute[ais]
            query = None
            if ais == 'clearingIsMandatory':
                infer_val = None
                if integration_utils.get_acm_version_override() >= 2017.2:
                    if str(val).upper() in ['YES', 'TRUE', '1']:
                        infer_val = '1'
                    elif str(val).upper() in ['NO', 'FALSE', '2']:
                        infer_val = '2'
                    elif str(val).upper() in ['NONE', '0']:
                        infer_val = '0'
                    query = "acm." + acm_object + '.Select("' + "%s = %d" + '"%("' + ais + '",int(' + infer_val + ')))'
                else:
                    if str(integration_utils.get_acm_version_override()) == '2016.4':
                        query = "acm." + acm_object + 'RegulatoryInfo.Select("' + "%s = %s" + '"%("' + ais + '","' + val + '"))'
                    else:
                        query = "acm." + acm_object + '.Select("' + "%s = %s" + '"%("' + ais + '","' + val + '"))'
            elif ais == 'timePrecision':
                val = int(val)
                if str(integration_utils.get_acm_version_override()) == '2016.4':
                    query = "acm." + acm_object + 'RegulatoryInfo.Select("' + "%s = %d" + '"%("' + ais + '",' + str(val) + '))'
                else:
                    query = "acm." + acm_object + '.Select("' + "%s = %d" + '"%("' + ais + '",' + str(val) + '))'
            else:
                if str(integration_utils.get_acm_version_override()) == '2016.4':
                    query = "acm." + acm_object + 'RegulatoryInfo.Select("' + "%s = '%s'" + '"%("' + ais + '","' + val + '"))'
                else:
                    query = "acm." + acm_object + '.Select("' + "%s = '%s'" + '"%("' + ais + '","' + val + '"))'
            query_result = eval(query)
        elif ais == 'FISN':#it means we need to look in the aliases
            query_result = acm.FInstrumentAlias.Select("type = 'FISN' and alias = '%s'"%val)
        elif ais == 'MIC':#it means we need to look in the aliases
            query_result = acm.FPartyAlias.Select("type = 'MIC' and alias = '%s'"%val)
        elif ais in ['regTrdTerminateDate', 'regFirstTradeTime', 'regTrdAdmisReqTime', 'regTrdAdmisAppTime', 'regRptDeferToTime']:#these have been remoevd to be inline with the way core works. it does not support local value in query and hence wrapper is in sync, 'regConfirmationTime', 'regClearingTime']:
            try:
                result_utc_datetime = None
                if ais in ['regTrdTerminateDate']:
                    result_utc_datetime = acm.Time().AsDate(val)
                else:
                    result_utc_datetime = acm.Time().LocalToUtc(val)
                query = "fieldValue = '%s' and addInf = '%s'" %(result_utc_datetime, ais)
                query_result = acm.FAdditionalInfo.Select(query)
            except Exception as e:
                FRegulatoryLogger.ERROR(logger, str(e))
                FRegulatoryLogger.ERROR(logger, "Expected datetime format not provided for <%s>"%ais)
        elif not query_result:
            if ais in ['regSMS', 'regLargeInScale', 'regSSTI', 'regAvgDailyTO', 'regTickSize', 'regPostLargeInScale', 'regPostSSTI']:
                val = float(val)
                val = str(float(val))
            if ais in ['regDirectedOrder', 'regIsInvestmentFirm', 'regPossibleReporter', \
                        'regClearingIsMandat', 'regIsHedge', 'regProvideLiquidity', \
                        'regIsLiquid', 'regIsSysInternalizr', 'regHasTrdObligation', \
                        'regComdtyDerivInd', 'regSecFinTransInd', \
                        'regIsAlgorithm', 'regToTV', 'regTransmOfOrder', 'regMiFIDTransparent', 'regGeneralPartner', 'regIsVenue']:
                if str(val).upper() in ['YES', 'TRUE', '1']:
                    if integration_utils.get_acm_version_override() >= 2015.4:
                        val = 'Yes'
                    else:
                        val = 'true'
                elif str(val).upper() in ['NO', 'FALSE', '0']:
                    if integration_utils.get_acm_version_override() >= 2015.4:
                        val = 'No'
                    else:
                        val = 'false'
            aisSpec = acm.FAdditionalInfoSpec[ais]
            if not aisSpec:
                FRegulatoryLogger.ERROR(logger, "The addInfoSpec <%s> in the query does not exist on %s"%(ais, acm_object))
            else:
                if ais in ['regConfirmationTime', 'regClearingTime']:
                    result_utc_datetime = acm.Time().LocalToUtc(val)
                    query = "fieldValue = '%s' and addInf = '%s'" %(result_utc_datetime, ais)
                    query_result = acm.FAdditionalInfo.Select(query)
                else:
                    query = "fieldValue = '%s' and addInf = '%s'" %(val, str(ais))
                    query_result = acm.FAdditionalInfo.Select(query)
                    if not query_result and val in ['Yes', 'No', 'true', 'false']:
                        if val == 'Yes':
                            val = 'true'
                        elif val == 'true':
                            val = 'Yes'
                        if val == 'No':
                            val = 'false'
                        elif val == 'false':
                            val = 'No'
                    query = "fieldValue = '%s' and addInf = '%s'" %(val, str(ais))
                    query_result = acm.FAdditionalInfo.Select(query)
                if not query_result and ais in ['regSMS', 'regLargeInScale', 'regSSTI', 'regAvgDailyTO', 'regTickSize', 'regPostLargeInScale', 'regPostSSTI'] and (float(val))%1 == 0:
                    query = "fieldValue = '%s' and addInf = '%s'" %(str(int(float(val))), str(ais))
                    query_result = acm.FAdditionalInfo.Select(query)

    if query_result:
        if query_result[0].IsKindOf('FAdditionalInfo'):
            for each_result in query_result:
                query = get_query(acm_object, str(each_result.Recaddr()))
                reg_info = eval(query)
                if acm_object == 'FContact' and related_acm_object:
                    if reg_info.Contact().Party() == related_acm_object:
                        return_result.append(reg_info)
                else:
                    return_result.append(reg_info)
        elif query_result[0].IsKindOf(acm.FInstrumentAlias):
            for each_result in query_result:
                query = get_query(acm_object, str(each_result.Instrument().Oid()))
                reg_info = eval(query)
                return_result.append(reg_info)
        elif query_result[0].IsKindOf(acm.FPartyAlias):
            for each_result in query_result:
                query = get_query(acm_object, str(each_result.Party().Oid()))
                reg_info = eval(query)
                return_result.append(reg_info)
        elif query_result[0].IsKindOf(acm_object):
            for each_result in query_result:
                return_result.append(each_result)
        elif query_result[0].IsKindOf(acm_object + 'RegulatoryInfo'):
            for each_result in query_result:
                oid = eval("each_result." + acm_object[1:] + "().Oid()")
                query = get_query(acm_object, str(oid))
                return_result.append(eval(query))
    return return_result

def DeleteField(acm_object, add_info):
    ais = acm.FAdditionalInfoSpec[add_info]
    query = 'addInf=%d and recaddr=%d ' % (ais.Oid(), acm_object.Oid())
    aiSel = acm.FAdditionalInfo.Select(query)
    if aiSel:
        integration_utils.update_addtional_info(aiSel[0])
    if integration_utils.get_acm_version_override() >= 2016.4 and add_info in add_info_dict_16_4:
        reg_info = acm_object.RegulatoryInfos()
        if reg_info and add_info in adm_attribute:
            reg_info = reg_info[0]
            add_info = adm_attribute[add_info]
            if add_info == 'timePrecision':
                FRegulatoryLogger.INFO(logger, "TimePrecision attribute cannot be deleted from RegulatoryInfo")
                return
            add_info = add_info[0].capitalize() + add_info[1:]
            query = "reg_info." + add_info + "(None)"
            eval(query)
            reg_info.Commit()

def Delete(acm_object, add_info_dict_key):
    add_infos = eval("add_info_" + add_info_dict_key)
    if add_info_dict_key in 'Person':
        if integration_utils.get_acm_version_override() >= 2016.5 and acm_object.IsKindOf(acm.FPerson):
            acm_object.Delete()
            return
    for add_info in add_infos:
        add_info_val = add_infos[add_info]
        if add_info_val in ['regContExchangeId', 'uniqueName'] and integration_utils.get_acm_version_override() >= 2017.2 and acm_object.IsKindOf(acm.FContact):
            if add_info_val == 'regContExchangeId' and acm_object.Person():
                acm_object.Person().ExchangeId(None)
                acm_object.Person().Commit()
            elif add_info_val == 'uniqueName':
                acm_object.UniqueName(None)
                acm_object.Commit()
        else:
            if add_info_dict_key == "Party" and add_infos[add_info] == 'MIC':
                for alias in acm_object.Aliases():
                    if alias.Type().Name() == 'MIC':
                        alias.Delete()
            else:
                ais = acm.FAdditionalInfoSpec[add_infos[add_info]]
                if ais:
                    aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (ais.Oid(), acm_object.Oid()))
                    if aiSel:
                        integration_utils.update_addtional_info(aiSel[0])
            if integration_utils.get_acm_version_override() >= 2016.4 and (add_infos[add_info] in add_info_dict_16_4 or add_infos[add_info] in add_info_dict_16_5):
                reg_info = acm_object.RegulatoryInfos()
                if reg_info and reg_info[0].Oid() > 0:
                    try:
                        reg_info[0].Delete()
                    except Exception as e:
                        FRegulatoryLogger.ERROR(logger, "Error while deleting********** <%s>"%str(e))

def get_log_message(reg_info, attribute, log_dict, log_val):
    if 'NAME' in log_dict and attribute in log_dict['NAME']:
        try:
            log_val = log_val + '\n' + attribute.strip() + " = " +  eval("reg_info." + attribute + "().Name()")
        except:
            log_val = log_val + '\n' + attribute.strip() + " = None"

    elif 'OID' in log_dict and attribute in log_dict['OID']:
        try:
            log_val = log_val + '\n' + attribute.strip() + " = " +  eval("reg_info." + attribute + "().Name()")
        except:
            log_val = log_val + '\n' + attribute.strip() + " = None"
    elif 'FULLNAME' in log_dict and attribute in log_dict['FULLNAME']:
        try:
            log_val = log_val + '\n' + attribute.strip() + " = " +  eval("reg_info." + attribute + "().Fullname()")
        except:
            log_val = log_val + '\n' + attribute.strip() + " = None"
    else:
        try:
            log_val = log_val + '\n' + attribute.strip() + " = " +  str(eval("reg_info." + attribute + "()"))
        except Exception as e:
            pass
    return log_val

def log_reg_attributes(reg_info):
    """logs the attributes on a given regulatoryInfo instance"""
    log_reg_functions = {
                 'FInstrumentRegulatoryInfo':['TradingTerminationDate', \
                                              'FirstTradingTime', 'AdmissionRequestTime', \
                                              'AdmissionApprovalTime', 'IsSystematicInternaliser',\
                                              'IsLiquid', 'StandardMarketSize', 'SizeSpecificToInstrument',\
                                              'LargeInScale', 'Instrument', 'CfiCode', 'ClearingIsMandatory',\
                                              'CommodityBaseProduct', 'CommodityFurtherSubProduct', \
                                              'CommoditySubProduct', 'FinalPriceType', 'TransactionType',\
                                              'HasTradingObligation', 'AverageDailyTurnover', 'SimilarIsin',\
                                              'IsTradedOnTradingVenue', 'LiquidityBand', 'InstypeRTS2', \
                                              'InsSubtypeRTS2', 'PrimaryMarketMic', 'MaterialMarketMic', \
                                              'DarkCapStatus', 'DoubleVolumeCapStatus', 'DarkCapMic', \
                                              'TickSize', 'IsMiFIDTransparent', 'InstypeRTS28', \
                                              'FinancialInstrumentShortName', 'PostSizeSpecificToInstrument', \
                                              'PostLargeInScale', 'SizeSpecificToInstrumentInCurrency', \
                                              'LargeInScaleInCurrency', 'PostLargeInScaleInCurrency', \
                                              'PostSizeSpecificToInstrumentInCurrency', 'IsEquityLike', \
                                              'IsBondLike', 'IsInterestRateDerivative', 'IsEquityDerivative', \
                                              'IsC10Derivative', 'IsFxDerivative', 'IsCFD'],
                'FTradeRegulatoryInfo' : ['ReportDeferToTime', 'RepositoryId', 'ClearingBroker', \
                        'ClearingHouse', 'Middleware', 'OriginalCounterparty', 'Repository', \
                        'TradingCapacity', 'ComplexTradeComponentId', 'OurOrganisation', \
                        'OurTransmittingOrganisation', 'OurInvestmentDecider', 'ExecutingEntity', \
                        'Venue', 'BranchMembership', 'TheirOrganisation', 'TheirInvestmentDecider', \
                        'TheirTrader', 'Waiver', 'WaiverString', 'OtcPostTradeIndicator', \
                        'OtcPostTradeIndicatorString', 'CommodityDerivativeIndicator', \
                        'IsSecurityFinancingTransaction', 'ReportingEntity', 'ExchangeId', \
                        'AlgoId', 'DirectedOrder', 'IsProvidingLiquidity', 'IsHedge', 'TimePrecision', \
                        'ConfirmationTime', 'ClearingTime', 'InvestmentDeciderCrmId', 'Isin', \
                        'CfiCode', 'NearLegIsin', 'FarLegIsin', 'TransmissionOfOrdersIndicator', 'IsCommodityDerivative', \
                        'TimePrecisionInUTC', 'TradeTimeWithPrecision', 'OurTrader', 'Trade', 'OurOrg', 'TheirOrg', 'Price']
                }
    log_val = ''
    log_dict = None
    class_name = None
    try:
        if reg_info.IsKindOf(acm.FInstrumentRegulatoryInfo):
            class_name = 'FInstrumentRegulatoryInfo'
        elif reg_info.IsKindOf(acm.FTradeRegulatoryInfo):
            class_name = 'FTradeRegulatoryInfo'
    except:
        pass
    if class_name in log_list:
        log_dict = log_list[class_name]
    if class_name in log_reg_functions:
        log_reg_functions = log_reg_functions[class_name]
        for each_function in log_reg_functions:
            if each_function not in log_dict['IGNORE']:
                log_val = get_log_message(reg_info, each_function, log_dict, log_val)
    return log_val.strip()

def log_attributes(class_name, reg_info):
    """logs the attributes on a given regulatoryInfo instance"""
    log_val = ''
    if class_name in log_list:
        log_dict = log_list[class_name]
        completeList = inspect.getmembers(reg_info, predicate = inspect.ismethod)
        for attribute in completeList:
            if attribute[0] not in log_dict['IGNORE']:
                log_val = get_log_message(reg_info, attribute[0], log_dict, log_val)

    return log_val.strip()

def milliseconds_to_utc_datetime(date_in_milliseconds):
    """convert the given milliseconds to utc datetime"""
    utc_date_time = None
    try:
        secs = float(date_in_milliseconds) / 1000.0
        UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
        #utc_date_time = datetime.fromtimestamp(secs) + UTC_OFFSET_TIMEDELTA
        utc_date_time = datetime.fromtimestamp(secs)
        utc_date_time = utc_date_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    except:
        pass
    return utc_date_time

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def locale_datetime_to_milliseconds(date_in_milliseconds):
    """convert the given locale datetime to milliseconds """
    millis = None
    try:
        date_details = date_in_milliseconds.split(' ')
        date_val = ael.date_from_string(date_details[0]).to_string(ael.DATE_ISO)
        date_in_milliseconds = date_val + " " +  date_details[1]
        if date_in_milliseconds.find('.') == -1:
            date_in_milliseconds = date_in_milliseconds + '.000000'
        date_obj = datetime.strptime(date_in_milliseconds, "%Y-%m-%d %H:%M:%S.%f")
        UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
        result_utc_datetime = date_obj
        delta  = result_utc_datetime - datetime.utcfromtimestamp(0)
        #millis = delta.total_seconds() * 1000.0#this function is not being used as it is not supported in python 2.6
        millis = timedelta_total_seconds(delta) * 1000.0
    except:
        pass
    return millis

def utc_datetime_to_milliseconds(date_in_milliseconds):
    """conver the given utc datetime to milliseconds"""
    millis = None
    try:
        date_details = date_in_milliseconds.split('T')
        date_val = ael.date_from_string(date_details[0]).to_string(ael.DATE_ISO)
        date_in_milliseconds = date_val + "T" +  date_details[1]
        if date_in_milliseconds.find('.') == -1:
            date_in_milliseconds_part = date_in_milliseconds.split('Z')
            date_in_milliseconds = date_in_milliseconds_part[0] + '.000000' + 'Z'
        date_obj = datetime.strptime(date_in_milliseconds, "%Y-%m-%dT%H:%M:%S.%fZ")
        UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
        result_utc_datetime = date_obj
        delta  = result_utc_datetime - datetime.utcfromtimestamp(0) - UTC_OFFSET_TIMEDELTA
        millis = timedelta_total_seconds(delta) * 1000.0
    except:
        pass
    return millis

def milliseconds_to_locale_datetime(date_in_milliseconds):
    """convert the given milliseconds to locale datetime"""
    locale = None
    try:
        secs = float(date_in_milliseconds) / 1000.0
        locale_time = datetime.utcfromtimestamp(secs)
        locale = locale_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    except:
        pass
    return locale

def get_string_from_bitmask(bitmask, enum_name):
    """get the corresponding string for the given bitmask"""
    inferred_output = ''
    flag = 0
    if enum_name == 'WAIVER' and bitmask:
        for i in range(1, 7):
            if (bitmask & (1 << (i-1))):
                for enum_val in dir(WAIVER):
                    if eval('WAIVER.'+ str(enum_val)) == i:
                        if flag:
                            inferred_output += ","
                        inferred_output += enum_val
                        flag = 1
    if enum_name == 'OTCPOSTTRADEINDICATOR' and bitmask:
        for i in range(1, 14):
            if (bitmask & (1 << (i-1))):
                for enum_val in dir(OTCPOSTTRADEINDICATOR):
                    if eval('OTCPOSTTRADEINDICATOR.'+ str(enum_val)) == i:
                        if flag:
                            inferred_output += ","
                        inferred_output += enum_val
                        flag = 1
    return inferred_output

def get_bitmask_from_string(str_val, choice_decl):
    """get corresponding integer value for all the waivers selected"""
    bitmask = 0
    if str(str_val):
        for item in str_val.split(","):
            try:
                index = eval(choice_decl + '.' + item)
                if index > 0:
                    bitmask = bitmask | (1 << (index-1) )
            except:
                FRegulatoryLogger.ERROR(logger, "valid values not provided for %s"%choice_decl)
    return bitmask

def get_otc_post_trade_ind(otc_post_trade_ind):
    """get corresponding integer value for all the otcposttradeindicators selected"""
    otc_post_trade_ind_Val = 0
    otc_post_trade_ind_val = format(otc_post_trade_ind_Val, '019b')
    lst_otc_post_trade_ind = list(otc_post_trade_ind_val)
    otc_post_trade_inds = otc_post_trade_ind.split(',')
    for each_otc_post_trade_ind in otc_post_trade_inds:
        if each_otc_post_trade_ind.strip() != '':
            if integration_utils.is_valid_choice_list_val('OTCPostTradeIndicator', each_otc_post_trade_ind.strip()):
                pos = get_choicelist_pos(each_otc_post_trade_ind.strip(), 'OTC_POST_TRADE_INDICATOR')
                lst_otc_post_trade_ind[pos] = '1'
            else:
                msg = '<%s> is not a valid entry in choicelist <OTCPostTradeIndicator>'%(each_otc_post_trade_ind.strip())
                FRegulatoryLogger.ERROR(logger, msg)
                raise ValueError(msg)
    otc_post_trade_ind = ''.join(lst_otc_post_trade_ind)
    otc_post_trade_ind = int(otc_post_trade_ind, 2)
    return otc_post_trade_ind

def get_commodity_product_clssfn(commodity_clssfn, cmmdty_val):
    """get corresponding integer value for all the commodity product classification selected"""
    choice_list_val_id = None
    try:
        if cmmdty_val.IsKindOf(acm.FChoiceList):
            choice_list_val_id = cmmdty_val.Oid()
    except Exception as e:
        choice_list_val = acm.FChoiceList.Select("name = '%s'"%cmmdty_val)
        if len(choice_list_val) > 1:
            FRegulatoryLogger.WARN(logger, "There are more than one choicelist with the same name. Selecting the first found")
        choice_list_val_id = choice_list_val[0].Oid() 
    return choice_list_val_id

def validate_float(field_value, regulatory_function):
    """validate if the given value is a float"""
    field_value_float = None
    if isinstance(field_value, float) or isinstance(field_value, int):
        field_value_float = field_value
    elif field_value.isdigit():
        field_value_float = float(field_value)
    else:
        try:
            field_value_float = float(field_value)
        except:
            pass
    if str(field_value_float) == 'None':
        msg = "The expected value for %s is float. However, <%s> is provided; hence not setting the value of %s"%(regulatory_function, str(field_value), regulatory_function)
        FRegulatoryLogger.ERROR(logger, msg)
        raise ValueError(msg)
    return field_value_float

def validate_enum_bool(field_value, regulatory_function):
    """validate if the given value  is a value in a tristate enum"""
    field_value_bool = None
    try:
        if str(field_value) in ['0', '1', '2']:
            field_value_bool = int(field_value)
        elif 'NONE' in str(field_value).upper():
            field_value_bool = 0
        else:
            field_value_bool = acm.EnumFromString(regulatory_function, field_value)
    except Exception as e:
        msg = "The expected value for %s is Enum. However, <%s> is provided; hence not setting the value of %s"%(regulatory_function, field_value, regulatory_function)
        FRegulatoryLogger.ERROR(logger, msg)
        raise ValueError(msg)
    return field_value_bool

def validate_bool(field_value, regulatory_function):
    """validate if the given value  is a boolean"""
    field_value_bool = None
    try:
        if field_value.IsKindOf(acm.FBoolean):
            field_value_bool = field_value
    except:
        pass
    if str(field_value_bool).upper() == 'NONE' and str(field_value).upper() != 'NONE':
        field_value_bool = integration_utils.isBool(field_value)
        if not isinstance(field_value_bool, bool):
            msg = "The expected value for %s is bool. However, <%s> is provided; hence not setting the value of %s"%(regulatory_function, field_value, regulatory_function)
            FRegulatoryLogger.ERROR(logger, msg)
            raise ValueError(msg)
    return field_value_bool

def validate_party(party_name, regulatory_function):
    """validates if the given party name is present in the ADS"""
    party_object = None
    if party_name:
        party_object = integration_utils.get_party_handle(party_name)
        if not party_object:
            msg = "The party provided for %s: <%s> is not a valid party"%(regulatory_function, party_name)
            FRegulatoryLogger.ERROR(logger, msg)
            raise ValueError(msg)
    return party_object

def validate_instrument(instrument_name, regulatory_function):
    """validates if the given instrument name is present in the ADS"""
    instrument_object = integration_utils.get_instrument_handle(instrument_name)
    if not instrument_object:
        msg = "The instrument provided for %s: <%s> is not a valid instrument"%(regulatory_function, instrument_name)
        FRegulatoryLogger.ERROR(logger, msg)
        raise ValueError(msg)
    return instrument_object

def validate_contact(contact_name, regulatory_function, parent_col_name = None, parent_col_val = None):
    """validates if the given contact name is present in the ADS"""
    contact_object = None
    contacts = []
    if parent_col_val:
        parent_party = None
        try:
            if parent_col_val.IsKindOf(acm.FParty):
                parent_party = parent_col_val
        except:
            parent_party = acm.FParty[parent_col_val]
        if parent_party:
            contacts = parent_party.Contacts()
    else:
        contact_object = acm.FContact[contact_name]
        if not contact_object:
            contacts = acm.FContact.Select('')
    for contact in contacts:
        try:
            if contact_name in [contact.UniqueName(), contact.Fullname()]:
                contact_object = contact
                break
        except:
            if contact_name in [contact.AdditionalInfo().UniqueName(), contact.Fullname()]:
                contact_object = contact
                break
    if not contact_object:
        msg = "The contact provided for %s: <%s> is not a valid contact"%(regulatory_function, contact_name)
        FRegulatoryLogger.ERROR(logger, msg)
        raise ValueError(msg)
    return contact_object

def validate_repository(repository):
    """validates if the given party is for the expected repository party type"""
    warn_msg = None
    if not repository.AdditionalInfo().Is_tdr():
        warn_msg = "<%s>  is not a valid repository party in ADS"%repository.Name()
    return warn_msg

def validate_clearing_broker(clearing_broker):
    """validates if the given party is for the expected clearing broker party type"""
    warn_msg = None
    if not clearing_broker.IsKindOf(acm.FBroker):
        warn_msg = "The party <%s> provided for Clearing Broker is not of type <Broker>. It is of type <%s>"%(clearing_broker.Name(), clearing_broker.Type())
    else:
        if not clearing_broker.ClearingBroker():
            warn_msg = "The party <%s> provided for Clearing Broker is of type <Broker>. However it is not set for being a ClearingBroker"%(clearing_broker.Name())
    return warn_msg

def validate_party_type(party_name, party_type, regulatory_function):
    """validates if the given party is for the expected party type"""
    warn_msg = None
    party_object = integration_utils.get_party_handle(party_name)
    if regulatory_function == 'Repository':
        warn_msg = validate_repository(party_object)
    elif regulatory_function == 'ClearingBroker':
        warn_msg = validate_clearing_broker(party_object)
    else:
        if party_object.Type() not in party_type:
            warn_msg = "The party provided for %s is not of type <%s>. It is of type <%s>"%(regulatory_function, party_type, party_object.Type())
    return warn_msg

def names_of_parties(party_type = None):
    if party_type:
        return [obj.Name() for obj in eval("acm.FParty.Select('type=" + party_type + "')")]
    else:
        return [obj.Name() for obj in eval("acm.FParty.Select('')")]

def names_of_venues():
    if integration_utils.get_acm_version_override() >= 2017.4:
        party_type = 'Venue'
        return [obj.Name() for obj in eval("acm.FParty.Select('type=" + party_type + "')")]
    else:
        venue_names = []
        for party in acm.FParty.Select("type = 'Counterparty'"):
            if party.AdditionalInfo().RegIsVenue() and party.AdditionalInfo().RegIsVenue() == True:
                venue_names.append(party.Name())
        return venue_names   

def validate_trade_time(date_time):
    """validates if the provided datetime field is of the valid format that is supported by this component"""
    bFound = False
    date_time_obj = None
    if not date_time or str(date_time) == 'None':
        return date_time, bFound, date_time_obj
    else:
        date_time = str(date_time)
    msg =   """
                Valid date_time formats are:   \"02-Dec-2016 12:25:00 PM\"
                                                \"2016-12-02 12:25:00\"
                                                \"12/06/2016 12:25:00\"
                                                \"12/06/2016 11:25:00 PM\"
                                                \"02-Dec-16 12:25:00 PM\"
                                                \"02-December-2016 12:25:00 PM\"
    """
    date_time = date_time.replace('Z', '')
    date_time = date_time.replace('T', ' ')
    date_time_val = date_time
    try :

        if not bFound:
            try:
                time.strptime(date_time_val, "%d-%b-%Y %I:%M:%S %p")
                date_time_obj = datetime.strptime(date_time_val, "%d-%b-%Y %I:%M:%S %p")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            try:
                time.strptime(date_time_val, "%Y-%m-%d %H:%M:%S")
                date_time_obj = datetime.strptime(date_time_val, "%Y-%m-%d %H:%M:%S")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            try:
                time.strptime(date_time_val, "%Y-%m-%d %H:%M:%S.%f")
                date_time_obj = datetime.strptime(date_time_val, "%Y-%m-%d %H:%M:%S.%f")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            try:
                time.strptime(date_time_val, "%m/%d/%Y %H:%M:%S %p")
                date_time_obj = datetime.strptime(date_time_val, "%m/%d/%Y %H:%M:%S %p")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            try:
                time.strptime(date_time_val, "%m/%d/%Y %H:%M:%S")
                date_time_obj = datetime.strptime(date_time_val, "%m/%d/%Y %H:%M:%S")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            try:
                time.strptime(date_time_val, "%d-%b-%y %I:%M:%S %p")
                date_time_obj = datetime.strptime(date_time_val, "%d-%b-%y %I:%M:%S %p")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            try:
                time.strptime(date_time_val, "%d-%B-%Y %I:%M:%S %p")
                date_time_obj = datetime.strptime(date_time_val, "%d-%B-%Y %I:%M:%S %p")
                bFound = True
            except ValueError:
                bFound = False
        if not bFound:
            FRegulatoryLogger.INFO(logger, "The provided datetime is not of the type that we have currently supported")
    except Exception as e:
        FRegulatoryLogger.ERROR(logger, str(e))
    return date_time, bFound, date_time_obj

def convertDateTimeToUTC(date_time, date_time_obj):
    utc_date_time_obj = None
    if date_time[-1] == 'Z':
        utc_date_time_obj = date_time_obj
    else:
        UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
        utc_date_time_obj = date_time_obj + UTC_OFFSET_TIMEDELTA
    return utc_date_time_obj

def convertUTCDateTimeToLocale(date_time_obj):
    locale_date_time_obj = None
    UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
    locale_date_time_obj = date_time_obj -+ UTC_OFFSET_TIMEDELTA
    return locale_date_time_obj

def getDateTime(date_time_val):
    date_time_utc = None
    date_time, is_valid, date_time_obj = validate_trade_time(date_time_val)
    if is_valid:
        date_time_utc = convertDateTimeToUTC(date_time, date_time_obj)
        date_time = convertUTCDateTimeToLocale(date_time_utc)
        date_time_utc = str(date_time_utc)
    return date_time, is_valid, date_time_utc

def get_classification_with_clvalue(choicelist_val):
    commodity_base = None
    commodity_sub = None
    commdity_further_sub = None
    msg = None
    commodity_classify = None
    if choicelist_val:
        try:
            if choicelist_val.IsKindOf(acm.FChoiceList):
                choicelist_val = choicelist_val.Name()
        except:
            pass
        choicelists = acm.FChoiceList.Select("name = '%s'"%choicelist_val)
        counter = 0
        for choicelist in choicelists:
            if choicelist.List() != 'MASTER':
                commodity_classify = choicelist
                counter = counter + 1
        if counter == 1:
            commodity_base, commodity_sub, commdity_further_sub = get_commodity_classification(commodity_classify)
        elif counter > 0:
            msg = "There are multiple entires for the %s classification"%(choicelist_val)
    return commodity_base, commodity_sub, commdity_further_sub, msg, commodity_classify

def get_cmdty_classification(choicelist_val, choicelist_parent, classfication_level):
    cmdty_classify = {0 :'CommodityBaseProduct', 1 : 'CommoditySubProduct', 2 : 'CommodityFurtherSubClassification'}
    commodity_base = None
    commodity_sub = None
    commdity_further_sub = None
    commodity_classify = None
    msg = None
    if choicelist_parent:
        if choicelist_val:
            try:
                if choicelist_val.IsKindOf(acm.FChoiceList):
                    choicelist_val = choicelist_val.Name()
            except Exception as e:
                pass
            if integration_utils.is_valid_choice_list_val(choicelist_parent.Name(), choicelist_val):
                FRegulatoryLogger.DEBUG(logger, "%s is being set to <%s>"%(cmdty_classify[classfication_level], choicelist_val))
                commodity_classify = integration_utils.get_choice_list(choicelist_parent.Name(), choicelist_val)
                commodity_base, commodity_sub, commdity_further_sub = get_commodity_classification(commodity_classify)
            else:
                msg = "The value <%s> is not a valid entry in <%s> ChoiceList"%(choicelist_val, cmdty_classify[classfication_level])
        else:
            if choicelist_parent.Name() != 'CommodityBaseProduct':
                #because in case the base is being set to None, it means all the other classifications will automatically become None
                choicelist_val = choicelist_parent
                commodity_classify = choicelist_parent
                commodity_base, commodity_sub, commdity_further_sub = get_commodity_classification(commodity_classify)
    else:
        commodity_base, commodity_sub, commdity_further_sub, msg, commodity_classify = get_classification_with_clvalue(choicelist_val)
    if (not commodity_classify) and choicelist_parent and choicelist_val:
        if choicelist_parent:
            msg = "The value <%s> is not a valid entry in <%s> ChoiceList"%(choicelist_val, choicelist_parent)
        else:
            msg = "The value <%s> is not a valid entry for %s"%(choicelist_val, cmdty_classify[classfication_level])
    cmdty = commodity_classify
    return cmdty, commodity_base, commodity_sub, commdity_further_sub, msg

def get_commodity_classification(cmdty_classify_val):
    cmdty_classification = []
    cmdty_further_sub = None
    cmdty_sub_product = None
    cmdty_base_product = None
    cmdtys = None
    if cmdty_classify_val:
        try:
            if cmdty_classify_val.IsKindOf(acm.FChoiceList):
                cmdty = cmdty_classify_val
        except:
            if str(cmdty_classify_val).isdigit():
                cmdty = acm.FChoiceList[cmdty_classify_val]
            else:
                cmdtys = acm.FChoiceList.Select("name = '%s'"%(cmdty_classify_val))
                for commodity in cmdtys:
                    if commodity.List() != 'MASTER':
                        cmdty = commodity
                        break
        cmdty_classification.append(cmdty)
        while cmdty and cmdty.List() != 'CommodityBaseProduct':
            cmdtys = acm.FChoiceList.Select("name = '%s'"%(cmdty.List()))
            for commodity in cmdtys:
                if commodity.List() != 'MASTER':
                    cmdty = commodity
                    break
            if cmdty not in cmdty_classification:
                cmdty_classification.append(cmdty)
        if cmdty_classification:
            if len(cmdty_classification) == 3:
                cmdty_further_sub = cmdty_classification[0]
                cmdty_sub_product = cmdty_classification[1]
                cmdty_base_product = cmdty_classification[2]
            elif len(cmdty_classification) == 2:
                cmdty_sub_product = cmdty_classification[0]
                cmdty_base_product = cmdty_classification[1]
            elif len(cmdty_classification) == 1:
                cmdty_base_product = cmdty_classification[0]
    return cmdty_base_product, cmdty_sub_product, cmdty_further_sub

def get_micro_seconds(time_precision):
    if time_precision.find('.') > -1:
        time_precision = time_precision.split('.')[1]
    time_precision = time_precision.split('Z')[0]
    if len(time_precision) < 6:
        pad_ctr = len(time_precision)
        while pad_ctr < 6:
            time_precision = time_precision + '0'
            pad_ctr = pad_ctr + 1
    else:
        time_precision = time_precision[0:6]
    return time_precision

def is_unique_name(contact, unique_name):
    is_unique_name = True
    contact_name = None
    for contact_object in contact.Party().Contacts():
        if contact_object.AdditionalInfo().UniqueName() and contact_object.AdditionalInfo().UniqueName() == unique_name and contact_object.Fullname() != contact.Fullname():
            is_unique_name = False
            contact_name = contact_object.Fullname()
            break
    return is_unique_name, contact_name

def get_crm_id_from_person(person):
    crm_id = None
    source = None
    if person.CrmId():
        crm_id = person.CrmId()
        source = person
    return crm_id, source

def get_crm_id_from_contact_old(contact):
    crm_id = None
    source = None
    is_algorithm  = None
    mifid_category = None
    reg_crm_id = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regContactCrmId'].Oid(),  contact.Oid()))
    if reg_crm_id and reg_crm_id[0].Oid() > 0:
        crm_id = contact.AdditionalInfo().RegContactCrmId()
        party = contact.Party()
        try:
            reg_is_algorithm = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regIsAlgorithm'].Oid(),  party.Oid()))
            if reg_is_algorithm and reg_is_algorithm[0].Oid() > 0:
                is_algorithm = party.AdditionalInfo().RegIsAlgorithm()
        except:
            pass
        try:
            reg_mifid_category = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regMifidCategory'].Oid(),  party.Oid()))
            if reg_mifid_category and reg_mifid_category[0].Oid() > 0:
                mifid_category = party.AdditionalInfo().RegMifidCategory()
        except:
            pass
        if (is_algorithm and party.Type() == 'Counterparty') or (mifid_category and mifid_category == 'Retail' and party.Type() == 'Client'):
            source = 'IDM'
        else:
            source = 'Trader'
    return crm_id, source

def get_crm_id_from_contact(contact):
    crm_id = None
    source = None
    reg_crm_id = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regContactCrmId'].Oid(),  contact.Oid()))
    if reg_crm_id and reg_crm_id[0].Oid() > 0:
        crm_id = contact.AdditionalInfo().RegContactCrmId()
        source = contact
    return crm_id, source

def get_crm_id_from_party(party):
    crm_id = None
    source = None
    reg_crm_id = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regPtyCrmId'].Oid(),  party.Oid()))
    if reg_crm_id and reg_crm_id[0].Oid() > 0:
        crm_id = party.AdditionalInfo().RegPtyCrmId()
        source = party
    return crm_id, source

def get_crm_id_from_party_old(party):
    crm_id = None
    source = None
    is_algorithm  = None
    reg_crm_id = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regPtyCrmId'].Oid(),  party.Oid()))
    if reg_crm_id and reg_crm_id[0].Oid() > 0:
        crm_id = party.AdditionalInfo().RegPtyCrmId()
        try:
            reg_is_algorithm = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regIsAlgorithm'].Oid(),  party.Oid()))
            if reg_is_algorithm and reg_is_algorithm[0].Oid() > 0:
                is_algorithm = party.AdditionalInfo().RegIsAlgorithm()
        except:
            pass
        if is_algorithm and party.Type() == 'Counterparty':
            source = 'Algorithm'
        else:
            source = 'CustomerCompany'
    return crm_id, source

def get_crm_id_from_contacts(contacts):
    """get the first found crm_id from the contact from the provided list of contacts"""
    crm_id = None
    source = None
    for contact in contacts:
        crm_id, source = get_crm_id_from_contact(contact)
        if crm_id:
            break
    return crm_id, source

def get_exchange_id_from_party(party):
    exchange_id = None
    reg_exchange_id = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regPtyExchangeId'].Oid(),  party.Oid()))
    if reg_exchange_id and reg_exchange_id[0].Oid() > 0:
        exchange_id = party.AdditionalInfo().RegPtyExchangeId()
    return exchange_id

def get_exchange_id_from_contact(contact):
    exchange_id = None
    reg_exchange_id = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec['regContExchangeId'].Oid(),  contact.Oid()))
    if reg_exchange_id and reg_exchange_id[0].Oid() > 0:
        exchange_id = contact.AdditionalInfo().RegContExchangeId()
    return exchange_id

def get_exchange_id_from_person(person):
    return person.ExchangeId()

def get_exchange_id_from_contacts(contacts):
    """get the first found exchange_id from the contact from the provided list of contacts"""
    exchange_id = None
    for contact in contacts:
        exchange_id = get_exchange_id_from_contact(contact)
        if exchange_id:
            break
    return exchange_id

def get_exchange_id_from_persons(contacts):
    """get the first found exchange_id from the person linked to the contact for the provided list of contacts"""
    exchange_id = None
    if integration_utils.get_acm_version_override() >= 2017.2:
        for contact in contacts:
            if contact.Person():
                exchange_id = get_exchange_id_from_person(contact.Person())
                if exchange_id:
                    break
    return exchange_id

def get_crm_id_add_info(crm_id, crmid_addinfospec):
    parent = None
    add_info = acm.FAdditionalInfo.Select01("addInf = %d and fieldValue = '%s'"%(acm.FAdditionalInfoSpec[crmid_addinfospec].Oid(), crm_id), '')
    if add_info:
        parent = add_info.Parent()
    return parent

def get_party_from_crm_id(crm_id):
    """get the party having the given CrmId"""
    return get_crm_id_add_info(crm_id, 'regPtyCrmId')

def get_contact_from_crm_id(crm_id):
    """get the contact having the given CrmId"""
    return get_crm_id_add_info(crm_id, 'regContactCrmId')

def get_person_from_crm_id(crm_id):
    """get the person having the given CrmId"""
    person_obj = None
    if integration_utils.get_acm_version_override() >= 2016.5:
        person_obj = acm.FPerson.Select01("crmId = '%s'"%crm_id, '')
    return person_obj

def get_crm_id_from_persons(contacts):
    """get the first found crm_id from the person linked to the contact for the provided list of contacts"""
    crm_id = None
    source = None
    if integration_utils.get_acm_version_override() >= 2016.5:
        for contact in contacts:
            if contact.Person():
                crm_id, source = get_crm_id_from_person(contact.Person())
                if crm_id:
                    break
    return crm_id, source

def get_addinfo_value(addinfo_spec, acm_object):
    new_acm_object = None
    if acm_object.IsKindOf(acm.FInstrument):
        new_acm_object = acm.FInstrument[acm_object.Name()]
    elif acm_object.IsKindOf(acm.FTrade):
        new_acm_object = acm.FTrade[acm_object.Oid()]
    elif acm_object.IsKindOf(acm.FParty):
        new_acm_object = acm.FParty[acm_object.Name()]
    elif acm_object.IsKindOf(acm.FContact):
        new_acm_object = acm.FContact[acm_object.Oid()]
    try:
        if acm_object.IsKindOf(acm.FInstrumentRegulatoryInfo):
            new_acm_object = acm.FInstrumentRegulatoryInfo[acm_object.Name()]
        elif acm_object.IsKindOf(acm.FTradeRegulatoryInfo):
            new_acm_object = acm.FTradeRegulatoryInfo[acm_object.Oid()]
    except:
        pass
    if not new_acm_object:
        new_acm_object = acm_object
    add_info_val = None
    try:
        acm_object_oid = new_acm_object.Oid()
        if (not new_acm_object.IsInfant()) and acm_object_oid < 0:#it means you are working on a temp copy of an already stored acm object
            acm_object_oid = new_acm_object.ConnectedTrade().Oid()
        add_info_arr = acm.FAdditionalInfo.Select('addInf=%d and recaddr =%d'%(acm.FAdditionalInfoSpec[addinfo_spec].Oid(),  acm_object_oid))
        if add_info_arr and add_info_arr[0].Oid() > 0:
            add_info_val = eval('acm_object.AdditionalInfo().' + addinfo_spec[0].upper() + addinfo_spec[1:] + '()')
    except:
        pass
    return add_info_val

def get_date_time_addinfo_value(addinfo_spec, acm_object):
    add_info_val = get_addinfo_value(addinfo_spec, acm_object)
    if add_info_val:
        add_info_val = datetime.fromtimestamp(add_info_val)
    return add_info_val

def get_date_time(date_time_val):
    date_time_value = None
    is_valid = True
    if str(date_time_val) not in ['None', '']:
        date_time_value, is_valid, date_time_in_utc = getDateTime(date_time_val)
        if is_valid:
            date_time_value = str(date_time_value)
    return date_time_value, is_valid

def get_bool(bool_val, location):
    bool_value = None
    if str(bool_val) not in ['None', '']:
        bool_value = validate_bool(bool_val, location)
    return bool_value

def get_integer(int_val, location):
    int_value = None
    err_msg = None
    if isinstance(int_value, int):
        int_value = int(int_val)
    elif str(int_val) not in['', 'None']:
        try:
            int_value = int(int_val)
        except:
            msg = "The expected value for %s is integer. However, <%s> is provided; hence not setting the value of %s"%(location, str(int_val), location)
            FRegulatoryLogger.ERROR(logger, msg)
            err_msg = msg
    return int_value, err_msg

def get_float(float_val, location):
    float_value = None
    err_msg = None
    if isinstance(float_val, float) or isinstance(float_val, int):
        float_value = float(float_val)
        if str(float_value) == 'nan':
            float_value = None
    elif str(float_val) not in['', 'None']:
        try:
            float_value = float(float_val)
        except:
            msg = "The expected value for %s is float. However, <%s> is provided; hence not setting the value of %s"%(location, str(float_val), location)
            #FRegulatoryLogger.ERROR(logger, msg)
            err_msg = msg
    return float_value, err_msg

def get_choice_list_val(choice_list_val, location):
    choice_list_value = None
    err_msg = None
    try:
        if choice_list_val.IsKindOf(acm.FChoiceList):
            if choice_list_val.List() == location:
                choice_list_value = choice_list_val
    except:
        pass
    if not choice_list_value:
        if not choice_list_val in [None, '']:
            try:
                if choice_list_val.IsKindOf(acm.FChoiceList):
                    choice_list_val = choice_list_val.Name()
            except:
                pass
            try:
                if location.IsKindOf(acm.FChoiceList):
                    location = location.Name()
            except:
                pass
            if not integration_utils.is_valid_choice_list_val(location, choice_list_val):
                err_msg = "The value <%s> is not a valid entry in <%s> ChoiceList. Hence not setting the %s"%(choice_list_val, location, location)
                FRegulatoryLogger.ERROR(logger, err_msg)
            else:
                choice_list_value = choice_list_val
    return choice_list_value, err_msg

def get_float_reg_val(float_val):
    float_value = None
    if str(float_val) != '0.0':
        float_value = float_val
    return float_value

def set_float_reg_val(float_val):
    float_value = float_val
    if not float_value:
        float_value = 0.0
    return float_value

def get_enum_val(enum_val, location):
    enum_value = None
    err_msg = None
    if enum_val:
        try:
            enum_value = acm.EnumFromString(location, enum_val)
        except:
            err_msg = "The value <%s> is not a valid entry in <%s>. Hence not setting the %s"%(enum_val, location, location)
    else:
        enum_value = 0
    return enum_value, err_msg

def get_reg_date_time(date_time_val):
    date_time_value = None
    if date_time_val and str(date_time_val) != 'None':
        if acm.Time().LocalToUtc(str(date_time_val)) == '1970-01-01 00:00:00':
            date_time_value = None
        else:
            date_time_value = str(date_time_val)
    return date_time_value

def get_id_val(id_val):
    id_value = None
    if id_val:
        id_value = str(id_val)
    return id_value

def get_party(party_val, location, party_type = None ):
    party_value = None
    warn_msg = None
    party_name = 'None'
    party_value = validate_party(party_val, location)
    if party_value and party_type:
        warn_msg = validate_party_type(party_value, party_type, location)
    if party_value:
        party_name = party_value.Name()
    return party_value, warn_msg, party_name

def get_contact(party_obj, contact_name, location, location_parent):
    contact_obj = None
    contact_fullname = None
    err_msg = None
    if contact_name:
        if party_obj:
            if contact_name:
                contact_obj = integration_utils.get_valid_contact(party_obj, contact_name)
                if contact_obj:
                    contact_fullname = contact_obj.Fullname()
                else:
                    err_msg = "The value <%s> is not a valid contact on party <%s>. Hence not setting the <%s>"%(contact_name, party_obj.Name(), location)
        else:
            err_msg = "Cannot set the %s as %s should be set first"%(location, location_parent)
    return contact_obj, contact_fullname, err_msg

def getClientType(acm_object):
    client_type = None
    if acm_object.IsKindOf(acm.FParty):
        reg = acm_object.RegulatoryInfo()
        if reg.IsAlgorithm() and acm_object.Type() == 'Counterparty':
            client_type = 'Algorithm'
        elif acm_object.Type() in ['Counterparty', 'Client', 'Depot']:
            for contact in acm_object.Contacts():
                query = None
                if integration_utils.get_acm_version_override() >= 2016.5 and contact.Person() and acm.FUser.Select01('person = %d'%contact.Person().Oid(), ''):
                    client_type = 'DiscretionaryTrader'
                try:
                    if (not client_type) and \
                        acm.FAdditionalInfo.Select01("addInf=%d and fieldValue ='%s'"%(acm.FAdditionalInfoSpec['regDiscreteTrader'].Oid(),  contact.Fullname()), ''):
                        client_type = 'DiscretionaryTrader'
                        break
                except:
                    pass
        elif acm_object.Type() == 'Intern Dept':#directly setting it to Trader without checking on user and contacts
            client_type = 'Trader'
        if not client_type:#if CRM id is found on the party then this is last possible option
            client_type = 'CustomerCompany'
    elif acm_object.IsKindOf(acm.FContact):
        if acm_object.Party().Type() == 'Intern Dept':
            client_type = 'Trader'
        elif (acm.FUser.Select01('fullName = %s'%acm_object.Fullname(), '')) or \
            (integration_utils.get_acm_version_override() >= 2016.5 and acm_object.Person() \
             and acm.FUser.Select01('person = %d'%acm_object.Person().Oid(), '') or \
             (integration_utils.get_acm_version_override() < 2016.5 and \
              acm.FAdditionalInfo.Select01("addInf=%d and fieldValue ='%s'"%(acm.FAdditionalInfoSpec['regDiscreteTrader'].Oid(),  acm_object.Fullname()), ''))):
            client_type = 'DiscretionaryTrader'
        else:
            client_type = 'CustomerCompany'
    elif integration_utils.get_acm_version_override() >= 2016.5 and acm_object.IsKindOf(acm.FPerson):
        client_type = 'CustomerPerson'
        for contact in acm.FContact.Select(''):
            if contact.Person() and contact.Person() == acm_object and contact.Party().Type() == 'Intern Dept':
                client_type = 'Trader'
                break
    return client_type

def is_mic(mic_val, location):
    err_msg = None
    if mic_val:
        #if any(char.isdigit() for char in mic_val):
        #    err_msg = "MIC <%s> provided for %s is not a valid MIC. It has digits in it."%(mic_val, location)
        #    FRegulatoryLogger.ERROR(logger, err_msg)
        if len(mic_val) != 4:
            msg = "MIC <%s> provided for %s is not a valid MIC."%(mic_val, location)
            if len(mic_val) > 4:
                msg = msg + ' Truncating it to the first 4 characters.'
                mic_val = mic_val[0:4] 
            FRegulatoryLogger.ERROR(logger, msg)
    else:
        mic_val = None
    return mic_val, err_msg


def get_previous_business_day(date_val, calendars):
    #today_date = ael.date_today()
    bNeedToReinterate = True
    previous_business_day = date_val 
    for calendar in calendars:
        previous_business_day = previous_business_day.adjust_to_banking_day(ael.Calendar[calendar.Name()], 'Preceding')
    if previous_business_day != date_val:
        bNeedToReinterate = True
    else:
        bNeedToReinterate = False
    if bNeedToReinterate:
        previous_business_day = get_previous_business_day(previous_business_day, calendars)
    return previous_business_day

def get_calendars(ins_curr):
    calendars = []
    if ins_curr:
        calendars.append(ins_curr.Legs()[0].PayCalendar())
        if ins_curr.Legs()[0].Pay2Calendar():
            calendars.append(ins_curr.Legs()[0].Py2Calendar())
        if ins_curr.Legs()[0].Pay3Calendar():
            calendars.append(ins_curr.Legs()[0].Pay3Calendar())
        if ins_curr.Legs()[0].Pay4Calendar():
            calendars.append(ins_curr.Legs()[0].Pay4Calendar())
        if ins_curr.Legs()[0].Pay5Calendar():
            calendars.append(ins_curr.Legs()[0].Pay5Calendar())
    return calendars

def convert_to_ins_curr(instrument, amt_val, actual_date, source_currency = 'EUR', destination_currency = None, market = "ECBFIX"):
    """converts the given amount in EUR to the currency of the instrument"""
    amt_val = None
    base_currency = acm.FCurrency[source_currency]
    if not base_currency:
        raise Exception("Currency <%s> does not exists in ADS. Hence cannot get the latest FxRate"%source_currency)
    ref_market = acm.FParty[market]
    if not ref_market:
        raise Exception("Market <%s> does not exists in ADS. Hence cannot get the latest FxRate"%market)
    if not destination_currency:
        destination_currency = instrument.Currency()
    for price in base_currency.Prices():
        if price.Market() == ref_market:
            calendars = get_calendars(base_currency)
            calendars.extend(destination_currency)
            date_val = actual_date.add_period('-1d')
            business_day = get_previous_business_day(date_val, calendars)
            price_day = ael.date_from_string(price.Day())
            if price_day == ael.date_from_string(business_day):
                amt_val = amt_val * price.Settle()
    return amt_val

def get_latest_fx_prices_for_date(base_currency, market, actual_date):
    prices = {}
    base_ins = acm.FCurrency[base_currency]
    ref_market = acm.FParty[market]
    for price in base_ins.Prices():
        if price.Market() == ref_market:
            calendars = get_calendars(price.Currency())
            calendars.extend(get_calendars(base_ins))
            date_val = actual_date.add_period('-1d')
            business_day = get_previous_business_day(date_val, calendars)
            price_day = ael.date_from_string(price.Day())
            if price_day == ael.date_from_string(business_day):
                prices[price.Currency().Name()] = {price_day.to_string(ael.DATE_ISO) : price.Settle()}
    latest_fx_rates = {actual_date : prices}
    return latest_fx_rates

def get_fx_converted_value(val, source_currency, destination_currency, market, latest_fx_rate = True):
    fx_val = None
    if str(val) != 'None':
        if source_currency != destination_currency:
            calendars = get_calendars(source_currency)
            calendars.extend(get_calendars(destination_currency))
            date_val = ael.date_today().add_period('-1d')
            business_day = get_previous_business_day(date_val, calendars)
            for price in source_currency.Prices():
                if ael.date_from_string(price.Day()) == ael.date_from_string(business_day) and \
                    price.Currency().Name() == destination_currency.Name() and price.Market() == market:
                    fx_val = val * price.Settle()
                    break
            if not fx_val:
                for price in destination_currency.Prices():
                    if ael.date_from_string(price.Day()) == ael.date_from_string(business_day) and \
                        price.Currency().Name() == source_currency.Name() and price.Market() == market:
                        fx_val = float(val) / price.Settle()
                        break
        else:
            fx_val = val
        if not fx_val:
            FRegulatoryLogger.WARN(logger, "Ensure that the latest prices are available, else the FX value cannot be calculated.")
            
    else:
        FRegulatoryLogger.ERROR(logger, "Value is None, hence its FX value is cannot be calculated.")
    
    return fx_val

def get_currency(currency, location):
    source_currency = None
    err_msg = None
    if currency:
        source_currency = acm.FCurrency[currency]
        if not source_currency:
            err_msg = "The %s <%s> does not exist in ADS"%(location, currency)
    return source_currency, err_msg

def get_market(market):
    mkt = None
    err_msg = None
    if market:
        mkt = acm.FParty[market]
        if not mkt:
            err_msg = "The market <%s> does not exist in ADS."%market
    return mkt, err_msg

def get_fx_value(val, location, currency2, market = 'ECBFIX', currency1 = None, latest_fx_rate = True):
    currency, err_msg = get_currency(currency1, location)
    if currency:
        mkt, err_msg = get_market(market)
        if err_msg:
            raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
        if 'Source' in location:
            fx_value = get_fx_converted_value(val, currency, currency2, mkt, latest_fx_rate)
        else:
            fx_value = get_fx_converted_value(val, currency2, currency, mkt, latest_fx_rate)
        if fx_value:
            val = fx_value
        else:
            FRegulatoryLogger.ERROR(logger, \
                "The latest fx conversion rate between <%s> and <%s> does not exist in ADS for market <%s>. Hence, fx conversion cannot be done."%(\
                currency1, currency2.Name(), market))
    if err_msg:
        raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
    return val

def get_time_in_system_format(trade_time):
    locale.setlocale(locale.LC_ALL, '')
    c = locale.getlocale()
    am_or_pm = ''
    trade_time = datetime.strptime(trade_time, '%Y-%m-%d %H:%M:%S')
    trade_time = trade_time.strftime('%c')
    date_time_am_or_pm = trade_time.split(' ')
    date_val = date_time_am_or_pm[0]
    time_val = date_time_am_or_pm[1]
    if len(date_time_am_or_pm) > 2:
        am_or_pm = date_time_am_or_pm[2]
    return date_val, time_val, am_or_pm

def get_datetime_microseconds(date_time_val):
    date_time_val = date_time_val.replace('T', ' ')
    date_time_val = date_time_val.replace('Z', '')
    date_vals = str(date_time_val).split(' ')
    date_time_val = ''
    micro_seconds = ''
    for each_val in date_vals:
        if each_val.find('.') != -1:
            if len(each_val.split('.')[-1]) == 6: #it means this is the microseconds part
                micro_seconds = each_val.split('.')[-1]
                for val in each_val.split('.'):
                    if val != micro_seconds:
                        date_time_val = date_time_val + ' ' +val
        else:
            date_time_val = date_time_val + ' ' + each_val
    return date_time_val, micro_seconds

def validate_date(date_val):
    date_obj = None
    err_msg = ''
    if date_val:
        try:
            date_obj = ael.date_from_string(date_val)
        except Exception as e:
            err_msg = "<%s> is in an invalid date format. Error: <%s>"%(date_val, str(e))
    return date_obj, err_msg

def get_eu_non_euro_currencies():
    non_euros_dict = {'EU Non-EUR': ['BGN', 'HRK', 'CZK', 'DKK', 'HUF', 'PLN', 'RON', 'SEK', 'GBP']}
    return non_euros_dict
