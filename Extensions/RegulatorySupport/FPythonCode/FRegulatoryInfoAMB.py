"""------------------------------------------------------------------------
MODULE
    FRegulatoryInfoAMB -
DESCRIPTION:
    This file is used to generate and AMBA dictionary output for the given RegulatorySupport field.
VERSION: 1.0.25(0.25.7)
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported.
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import FIntegrationUtils
import FRegulatoryUtils
import ael
import amb
import acm
import FRegulatoryLibUtils
import FRegulatoryInfoException
integration_utils = FIntegrationUtils.FIntegrationUtils()
acm_version = integration_utils.get_acm_version_override()
import FRegulatoryLogger
logger = 'FRegulatoryInfoAMB'
trade_attr_dict = {
'RepositoryId': 'regRepositoryId',
'ClearingBroker': 'regClearingBroker',
'ClearingHouse': 'regClearingHouse',
'Middleware': 'regMiddleware',
'OriginalCounterparty': 'regOriginalCpty',
'Repository': 'regRepository',
'TradingCapacity': 'regTradingCapacity',
'ComplexTradeComponentId': 'regComplexTrdCmptId',
'OurOrganisation': 'regOurOrg',
'OurTransmittingOrganisation': 'regOurTransmitOrg',
'OurInvestmentDecider': 'regOurInvesDecider',
'OurTrader': 'regOurTrader',
'ExecutingEntity': 'regExecutingEntity',
'Venue': 'regVenue',
'BranchMembership': 'regBranchMemberShip',
'TheirOrganisation': 'regTheirOrg',
'TheirInvestmentDecider': 'regTheirInvDecider',
'TheirTrader': 'regTheirTrader',
'Waiver': 'regWaiver',
'WaiverString': 'FUNCTION',
'OtcPostTradeIndicator': 'regOTCPostTradeInd',
'OtcPostTradeIndicatorString': 'FUNCTION',
'IsCommodityDerivative': 'regComdtyDerivInd',
'IsSecurityFinancingTransaction': 'regSecFinTransInd',
'ReportingEntity': 'regReportingEntity',
'ExchangeId': 'regExchangeId',
'AlgoId': 'regAlgoId',
'DirectedOrder': 'regDirectedOrder',
'IsProvidingLiquidity': 'regProvideLiquidity',
'IsHedge': 'regIsHedge',
'TimePrecision': 'regMicroSeconds',
'ConfirmationTime': 'regConfirmationTime',
'ClearingTime': 'regClearingTime',
'ReportDeferToTime': 'regRptDeferToTime',
'InvestmentDeciderCrmId': 'regInvesDecidrCrmId',
'NearLegIsin': 'regNearLegIsin',
'FarLegIsin': 'regFarLegIsin',
'Isin': 'regInsIsin',
'CfiCode': 'regInsCfiCode',
'TransmissionOfOrdersIndicator': 'regTransmOfOrder',

}

trade_attr_dict_override = {
'WaiverString': 'regWaiver',
'OtcPostTradeIndicatorString': 'regOTCPostTradeInd',
}

instrument_attr_dict = {
'FinancialInstrumentShortName': 'regFISN',
'TradingTerminationDate': 'regTrdTerminateDate',
'FirstTradingTime': 'regFirstTradeTime',
'AdmissionRequestTime': 'regTrdAdmisReqTime',
'AdmissionApprovalTime': 'regTrdAdmisAppTime',
'IsSystematicInternaliser': 'regIsSysInternalizr',
'IsLiquid': 'regIsLiquid',
'StandardMarketSize': 'regSMS',
'SizeSpecificToInstrument': 'regSSTI',
'LargeInScale': 'regLargeInScale',
'PostSizeSpecificToInstrument': 'regPostSSTI',
'PostLargeInScale': 'regPostLargeInScale',
'CfiCode': 'regCFICode',
'ClearingIsMandatory': 'regClearingIsMandat',
'CommodityBaseProduct': 'FUNCTION',
'CommoditySubProduct': 'FUNCTION',
'CommodityFurtherSubProduct': 'FUNCTION',
'FinalPriceType': 'regFinalPriceType',
'TransactionType': 'regTransactionType',
'LegIsin': 'regLegIsin',
'HasTradingObligation': 'regHasTrdObligation',
'AverageDailyTurnover': 'regAvgDailyTO',
'IsTradedOnTradingVenue': 'regToTV',
'LiquidityBand': 'regLiquidityBand',
'PrimaryMarketMic': 'regPrimaryMktMic',
'MaterialMarketMic': 'regMaterialMktMic',
'DarkCapStatus': 'regDarkCapStatus',
'DoubleVolumeCapStatus': 'regDblVolCapStatus',
'DarkCapMic': 'regDarkCapMic',
'TickSize': 'regTickSize',
'IsMiFIDTransparent': 'regMiFIDTransparent',
'SimilarIsin': 'regSimilarIsin',
}

instrument_attr_dict_override = {
'CommodityBaseProduct': 'regCmdty',
'CommoditySubProduct': 'regCmdty',
'CommodityFurtherSubProduct': 'regCmdty',
}

party_attr_dict = {'FinancialCategory': 'regFinancialCategor',
'IsInvestmentFirm': 'regIsInvestmentFirm',
'PossibleReporter': 'regPossibleReporter',
'MIC': 'MIC',
'IsAlgorithm': 'regIsAlgorithm',
'ExchangeId': 'regPtyExchangeId',
'CrmId': 'regPtyCrmId',
'MiFIDCategory': 'regMifidCategory',
'IsVenue': 'regIsVenue',
}

contact_attr_dict = {
'DateOfBirth' : 'dateOfBirth',
'FirstName' : 'firstName',
'LastName' : 'lastName',
'NationalId' : 'nationalId',
'CrmId' : 'regContactCrmId',
'ExchangeId' : 'regContExchangeId',
'UniqueName' : 'uniqueName',
'IsGeneralPartner' : 'regGeneralPartner'}

contact_attr_dict_override = {
'JointAccount': 'regJointAccount',
}


attr_float_validate = ['AverageDailyTurnover', 'LargeInScale', 'SizeSpecificToInstrument', 'StandardMarketSize', \
                       'TickSize', 'PostLargeInScale', 'PostSizeSpecificToInstrument']
attr_bool_validate = ['IsCommodityDerivative', 'IsSecurityFinancingTransaction', 'DirectedOrder', 'IsProvidingLiquidity', \
                      'IsHedge', 'ClearingIsMandatory', 'IsSystematicInternaliser', 'IsLiquid', 'IsInvestmentFirm', 'PossibleReporter', \
                      'HasTradingObligation', 'IsAlgorithm', 'IsMiFIDTransparent', 'IsGeneralPartner', 'IsVenue']
attr_bool_enum_validate_17_2 = ['ClearingIsMandatory', 'IsHedge', ]
attr_bool_enum_validate_17_1 = ['DirectedOrder', 'IsLiquid', 'IsSystematicInternaliser']
attr_datetime_validate = ['ConfirmationTime', 'ClearingTime', 'FirstTradingTime', 'AdmissionRequestTime',\
                        'AdmissionApprovalTime', 'ReportDeferToTime', 'TradingTerminationDate']
attr_date_validate = ['DateOfBirth']
attr_party_validate = ['ClearingBroker', 'ClearingHouse', 'Middleware', 'OriginalCounterparty', 'Repository', 'OurOrganisation', \
                        'OurTransmittingOrganisation', 'ExecutingEntity', 'Venue', 'BranchMembership', 'TheirOrganisation', \
                        'ReportingEntity']
attr_party_type_validate = {'ClearingBroker': 'Broker', 'ClearingHouse' : 'Clearing House', 'Middleware': 'Middleware' , \
                            'Repository': 'FParty', 'OurOrg':'Intern Dept', 'OurTransmitOrg':'Intern Dept',\
                            'ExecutingEntity' : 'Market', 'TheirOrg':'Counterparty,Intern Dept'}
attr_contact_validate = ['OurInvestmentDecider', 'TheirInvestmentDecider', 'TheirTrader']
attr_ins_validate = ['LegIsin', 'Isin']
attr_limit_len = ['CfiCode']
attr_choice_list = ['TradingCapacity', 'FinalPriceType', 'TransactionType', 'FinancialCategory', 'MiFIDCategory', 'DarkCapStatus', 'DoubleVolumeCapStatus', 'ShortSellIndicator']
remove_prefix = ['TRADING_CAPACITY_', 'DIRECTED_ORDER_', 'IS_LIQUID_', 'SYS_INT_', 'IS_HEDGE_', 'CLEARING_IS_MANDATORY_']

adm_column_name = {
                    'regClearingIsMandatory': 'CLEARING_IS_MANDATORY',
                    'regClearingIsMandat': 'CLEARING_IS_MANDATORY',
                    'regCFICode': 'CFI_CODE',
                    'regClearingHouse': 'CLR_HOUSE_PTYNBR.PTYID',
                    'regMicroSeconds': 'TIME_PRECISION',
                    'regClearingBroker': 'CLR_BROKER_PTYNBR.PTYID',
                    'regMiddleware': 'MIDDLEWARE_PTYNBR.PTYID',
                    'regOriginalCpty': 'ORIGINAL_CPTY_PTYNBR.PTYID',
                    'regRepository': 'REPOSITORY_PTYNBR.PTYID',
                    'regIsHedge': 'IS_HEDGE',
                    'regSSTI': 'SIZE_SPECIFIC_TO_INS',
                    'regLargeInScale': 'LARGE_IN_SCALE',
                    'regIsLiquid': 'IS_LIQUID',
                    'regIsSysInternalizr': 'IS_SYSTEMATIC_INTERNALISER',
                    'regBranchMemberShip': 'BRANCH_MEMBERSHIP_PTYNBR.PTYID',
                    'regTradingCapacity': 'TRADING_CAPACITY',
                    'regWaiver': 'WAIVER',
                    'regOTCPostTradeInd': 'OTC_POST_TRADE_INDICATOR',
                    'regOurTransmitOrg': 'OUR_TRANSMIT_ORG_PTYNBR.PTYID',
                    'regOurInvesDecider': 'OUR_INVEST_DECIDER_SEQNBR',
                    'regOurOrg': 'OUR_ORG_PTYNBR.PTYID',
                    'regTheirOrg': 'THEIR_ORG_PTYNBR.PTYID',
                    'regTheirInvDecider': 'THEIR_INVEST_DECIDER_SEQNBR',
                    'regTheirTrader': 'THEIR_TRADER_SEQNBR',
                    'regDirectedOrder': 'DIRECTED_ORDER',
                    'regConfirmationTime': 'CONFIRMATION_TIME',
                    'regClearingTime': 'CLEARING_TIME',
                    'regCmdty': 'COMMODITY_PRODUCT_CHLNBR.ENTRY,COMMODITY_PRODUCT_CHLNBR.LIST',
                    'regRptDeferToTime': 'REPORT_DEFER_TO_TIME',
                    'regAvgDailyTO': 'AVERAGE_DAILY_TURNOVER',
                    'uniqueName': 'UNIQUE_NAME',
                   }
adm_trade_reg_fields = ['ClearingHouse', 'TimePrecision', 'ClearingBroker', 'Middleware', 'OriginalCounterparty',\
                        'Repository', 'IsHedge', 'BranchMembership', 'TradingCapacity', 'Waiver', \
                        'OtcPostTradeIndicator', 'OurTransmittingOrganisation', 'OurInvestmentDecider', 'OurOrganisation', \
                        'TheirOrganisation', 'TheirInvestmentDecider', 'TheirTrader', 'DirectedOrder', \
                        'ConfirmationTime', 'ClearingTime', 'ReportDeferToTime']
adm_ins_reg_fields = ['CfiCode', 'ClearingIsMandatory', 'LargeInScale', 'SizeSpecificToInstrument', 'IsLiquid', 'IsSystematicInternaliser', \
                      'CommodityBaseProduct', 'CommoditySubProduct', 'CommodityFurtherSubProduct', 'AverageDailyTurnover']
attr_alias_dict = {'MIC':'PARTYALIAS'}
class RegulatoryInfoAMB(object):
    def __get_msg_dict(self, col_name, col_value, attr_dict):
        msgDict = None
        if acm_version >= 2016.4:
            adm_col_name = None
            if acm_version >= 2017.2 and (attr_dict[col_name] in FRegulatoryUtils.add_info_dict_17_2):
                adm_col_name = adm_column_name[attr_dict[col_name]]
            elif acm_version >= 2017.1 and (attr_dict[col_name] in FRegulatoryUtils.add_info_dict_17_1):
                adm_col_name = adm_column_name[attr_dict[col_name]]
            elif acm_version >= 2016.5 and (attr_dict[col_name] in FRegulatoryUtils.add_info_dict_16_4 or attr_dict[col_name] in FRegulatoryUtils.add_info_dict_16_5):
                adm_col_name = adm_column_name[attr_dict[col_name]]
            elif acm_version >= 2016.4 and (attr_dict[col_name] in FRegulatoryUtils.add_info_dict_16_4):
                adm_col_name = adm_column_name[attr_dict[col_name]]
            if adm_col_name == 'CLR_HOUSE_PTYNBR.PTYID' and acm_version == 2016.4:
                adm_col_name = 'CLEARING_HOUSE_PTYNBR.PTYID'
            if adm_col_name:
                if adm_col_name.find(',') != -1:
                    columns = adm_col_name.split(',')
                    msgDict = { columns[0] : acm.FChoiceList[col_value].Name(),
                                columns[1] : acm.FChoiceList[col_value].List()}
                else:
                    msgDict = {adm_col_name : col_value}
        return msgDict

    def reg_info_to_amb(self, col_name, col_value, attr_dict, api_call, parent_col_name = None, parent_col_value = None, parent_required = True, src_currency = None, dest_currency = None, market = 'ECBFIX'):
        """create the AMBA dict for the given regulatorySupport field"""
        msgDict = None
        if col_name not in attr_dict:
            raise NameError(col_name)
        if src_currency and col_name in ['LargeInScale', 'PostLargeInScale', 'SizeSpecificToInstrument', 'PostSizeSpecificToInstrument']:
            source_currency, err_msg = FRegulatoryUtils.get_currency(src_currency, 'Source Currency')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            destination_currency, err_msg = FRegulatoryUtils.get_currency(dest_currency, 'Destination Currency')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            if src_currency:
                mkt, err_msg = FRegulatoryUtils.get_market(market)
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
                fx_value = FRegulatoryUtils.get_fx_converted_value(col_value, source_currency, destination_currency, mkt)
                if fx_value:
                    col_value = fx_value
        if attr_dict[col_name] == 'FUNCTION': # Means: just mapping is not enough, call fn
            msgDict = eval('self.'+ col_name + '(col_value)')
        else:
            if col_name in attr_float_validate:
                col_value = str(FRegulatoryUtils.validate_float(col_value, col_name))
            if col_name in attr_bool_enum_validate_17_2 and acm_version >= 2017.2:
                col_value = FRegulatoryUtils.validate_enum_bool(col_value, col_name)
            elif col_name in attr_bool_enum_validate_17_1 and acm_version >= 2017.1:
                col_value = FRegulatoryUtils.validate_enum_bool(col_value, col_name)
            elif col_name in attr_bool_validate:
                for each_remove_prefix in remove_prefix:
                    if each_remove_prefix in str(col_value):
                        col_value = col_value.replace(each_remove_prefix, '')
                        if col_value == 'FALSE':
                            col_value = 'False'
                        elif col_value == 'TRUE':
                            col_value = 'True'
                        elif col_value == 'NONE':
                            col_value = 'None'
                if str(col_value) == '2':
                    col_value = 'False'
                elif str(col_value) == '0' and \
                (col_name in attr_bool_enum_validate_17_2 or \
                    col_name in attr_bool_enum_validate_17_1):
                    col_value = 'None'
                col_value = FRegulatoryUtils.validate_bool(col_value, col_name)
            elif col_name in attr_datetime_validate:
                if col_name == 'TradingTerminationDate':
                    col_value, err_msg = FRegulatoryUtils.validate_date(col_value)
                    if err_msg:
                        raise ValueError('Invalid value for %s. Expected date value.'%col_name)
                else:
                    col_value, valid_time, col_val_obj = FRegulatoryUtils.validate_trade_time(col_value)
                    if not valid_time:
                        raise ValueError('Invalid value for %s. Expected datetime value.'%col_name)
                    if acm_version >= 2017.2 and (col_name in adm_trade_reg_fields or col_name in adm_ins_reg_fields) and attr_dict[col_name] in FRegulatoryUtils.add_info_dict_17_2:
                        pass
                    elif acm_version >= 2017.1 and (col_name in adm_trade_reg_fields or col_name in adm_ins_reg_fields) and attr_dict[col_name] in FRegulatoryUtils.add_info_dict_17_1:
                        pass
                    else:
                        col_value = acm.Time().LocalToUtc(col_value)
            elif col_name in attr_party_validate:
                FRegulatoryUtils.validate_party(col_value, col_name)
                if col_name in attr_party_type_validate:
                    warn_msg = eval("FRegulatoryUtils.validate_party_type('" + col_value + "','" + attr_party_type_validate[col_name] + "','" + col_name + "')")
                    if warn_msg:
                        FRegulatoryLogger.WARN(logger, warn_msg)
            elif col_name in attr_contact_validate:
                valid_contact = FRegulatoryUtils.validate_contact(col_value, col_name, parent_col_name, parent_col_value)
                if valid_contact:
                    if acm_version >= 2017.1:
                        col_value = valid_contact.Oid()
                    else:
                        col_value = valid_contact.Fullname()
            elif col_name in attr_ins_validate:#TODO:
                if not FRegulatoryLibUtils.isValidIsin(col_value):
                    FRegulatoryLogger.WARN(logger, "The ISIN provided is not a valid ISIN")
            if col_name in attr_limit_len:
                if len(col_value) > 6:
                    FRegulatoryLogger.WARN(logger, "The cfiCode provided <%s> is longer than the expected length of 6 characters. Truncating the CfiCode to <%s>"%(col_value, col_value[0:6]))
                    col_value = col_value[0:6]
            msgDict = self.__get_msg_dict(col_name, col_value, attr_dict)
        if not msgDict and col_name in attr_alias_dict:
            msgDict = self.wrapInAlias(attr_dict[col_name], attr_alias_dict[col_name], col_value)
        if not msgDict:
            msgDict = self.wrapInAddInfo(attr_dict[col_name], col_name, col_value)
            if 'ADDITIONALINFO' in msgDict and acm_version >= 2016.5 and \
                (col_name in trade_attr_dict or col_name in instrument_attr_dict):
                if api_call in ['TRADEREGULATORYINFO', 'INSTRUMENTREGULATORYINFO']:
                    parent = None
                    if col_name in trade_attr_dict and api_call == 'TRADEREGULATORYINFO':
                        if col_name in ['ShortSellIndicator']:
                            parent = 'TRADE'
                        else:
                            parent = 'TRADEREGULATORYINFO'
                    elif col_name in instrument_attr_dict and api_call == 'INSTRUMENTREGULATORYINFO':
                        parent = 'INSTRREGULATORYINFO'
                    msgDict = {parent : msgDict}
        else:
            parent = None
            if col_name in adm_trade_reg_fields:
                if not list(msgDict.keys())[0] == 'TRADEREGULATORYINFO':# this is created in the case of Waiver and should not get created again
                    parent = 'TRADEREGULATORYINFO'
            elif col_name in adm_ins_reg_fields:
                if not list(msgDict.keys())[0] == 'INSTRREGULATORYINFO':# this is created in the case of Commodity classification and should not get created again
                    parent = 'INSTRREGULATORYINFO'
            if parent and ('ADDITIONALINFO' not in msgDict):
                msgDict = {parent : msgDict}
        return msgDict

    def wrapInAlias(self, alias_type, alias_upon, col_value):
        """Return the alias type + alias as a dictionary"""
        msgDict = {alias_upon :
                    {
                     'ALIAS' : col_value,
                     'TYPE.ALIAS_TYPE_NAME' : alias_type
                    }
                }
        return msgDict

    def wrapInAddInfo(self, spec_col_name, col_name, col_value):
        """Return the specName + value of an AddInfo as a dictionary"""
        additional_info_value = str(col_value)
        if col_name in attr_choice_list:
            additional_info_value_cl = ael.ChoiceList.read("list='%s' and entry='%s'"%(col_name, additional_info_value))
            if not additional_info_value_cl:
                raise ValueError('Invalid value for %s. %s is not a valid entry in choicelist %s.'%(col_name, col_value, col_name))
        msgDict = {'ADDITIONALINFO' :
                    {
                    'ADDINF_SPECNBR.FIELD_NAME' : spec_col_name,
                    'VALUE' : additional_info_value
                    }
                }
        return msgDict

    def tradeRegInfo2amb(self, col_name, col_value, parent_col_name = None, parent_col_value = None, parent_required = True):
        """Set Trade RegulatoryInfo column and value related to AMB version. Returns dict"""
        msgDict = self.reg_info_to_amb(col_name, str(col_value), trade_attr_dict, 'TRADEREGULATORYINFO', parent_col_name, parent_col_value)
        if parent_required and ((col_name not in ['ShortSellIndicator'] and acm_version >= 2016.5 ) or (acm_version < 2016.5)):
            msgDict = {'TRADE':msgDict}
        return msgDict

    def instrumentRegInfo2amb(self, col_name, col_value, parent_required = True, src_currency = None, dest_currency = None, market = 'ECBFIX'):
        """Set Instrument RegulatoryInfo column and value related to AMB version. Returns dict"""
        msgDict = self.reg_info_to_amb(col_name, col_value, instrument_attr_dict, 'INSTRUMENTREGULATORYINFO', src_currency = src_currency, dest_currency = dest_currency, market = market)
        if parent_required:
            msgDict = {'INSTRUMENT':msgDict}
        return msgDict

    def partyRegInfo2amb(self, col_name, col_value):
        """Set Party RegulatoryInfo column and value related to AMB version. Returns dict"""
        msgDict = self.reg_info_to_amb(col_name, col_value, party_attr_dict, 'PARTYREGULATORYINFO')
        return {'PARTY':msgDict}

    def contactRegInfo2amb(self, col_name, col_value):
        """Set Contact RegulatoryInfo column and value related to AMB version. Returns dict"""
        msgDict = self.reg_info_to_amb(col_name, col_value, contact_attr_dict, 'CONTACTREGULATORYINFO')
        return {'CONTACT':msgDict}

    def Waiver(self, col_value):
        """returns the corresponding integer for the multiple waivers selected"""
        trade_attr_dict['Waiver'] = trade_attr_dict_override['Waiver']
        #col_value = FRegulatoryUtils.get_waiver(col_value)
        if not str(col_value).isdigit():
            raise ValueError('Invalid value for Waiver. Expected integer value.')
        msgDict = self.reg_info_to_amb('Waiver', col_value, trade_attr_dict, 'TRADEREGULATORYINFO')
        trade_attr_dict['Waiver'] = 'FUNCTION'
        return msgDict

    def OtcPostTradeIndicator(self, col_value):
        """returns the corresponding integer for the multiple OtcPostTradeIndicators selected"""
        trade_attr_dict['OtcPostTradeIndicator'] = trade_attr_dict_override['OtcPostTradeIndicator']
        #col_value = FRegulatoryUtils.get_otc_post_trade_ind(col_value)
        if not str(col_value).isdigit():
            raise ValueError('Invalid value for OtcPostTradeIndicator. Expected integer value.')
        msgDict = self.reg_info_to_amb('OtcPostTradeIndicator', col_value, trade_attr_dict, 'TRADEREGULATORYINFO')
        trade_attr_dict['OtcPostTradeIndicator'] = 'FUNCTION'
        return msgDict

    def WaiverString(self, col_value):
        """returns the corresponding integer for the multiple waivers selected"""
        trade_attr_dict['WaiverString'] = trade_attr_dict_override['WaiverString']
        col_value = FRegulatoryUtils.get_bitmask_from_string(col_value, 'WAIVER')
        msgDict = self.reg_info_to_amb('Waiver', col_value, trade_attr_dict, 'TRADEREGULATORYINFO')
        trade_attr_dict['WaiverString'] = 'FUNCTION'
        return msgDict

    def OtcPostTradeIndicatorString(self, col_value):
        """returns the corresponding integer for the multiple OtcPostTradeIndicators selected"""
        trade_attr_dict['OtcPostTradeIndicatorString'] = trade_attr_dict_override['OtcPostTradeIndicatorString']
        col_value = FRegulatoryUtils.get_bitmask_from_string(col_value, 'OTCPOSTTRADEINDICATOR')
        msgDict = self.reg_info_to_amb('OtcPostTradeIndicator', col_value, trade_attr_dict, 'TRADEREGULATORYINFO')
        trade_attr_dict['OtcPostTradeIndicatorString'] = 'FUNCTION'
        return msgDict

    def CommodityBaseProduct(self, col_value):
        cmmdty_classfication = FRegulatoryUtils.get_commodity_product_clssfn('CommodityBaseProduct', col_value)
        instrument_attr_dict['CommodityBaseProduct'] = instrument_attr_dict_override['CommodityBaseProduct']
        msgDict = self.reg_info_to_amb('CommodityBaseProduct', cmmdty_classfication, instrument_attr_dict, 'INSTRUMENTREGULATORYINFO')
        instrument_attr_dict['CommodityBaseProduct'] = 'FUNCTION'
        return msgDict

    def CommoditySubProduct(self, col_value):
        cmmdty_classfication = FRegulatoryUtils.get_commodity_product_clssfn('CommoditySubProduct', col_value)
        instrument_attr_dict['CommoditySubProduct'] = instrument_attr_dict_override['CommoditySubProduct']
        msgDict = self.reg_info_to_amb('CommoditySubProduct', cmmdty_classfication, instrument_attr_dict, 'INSTRUMENTREGULATORYINFO')
        instrument_attr_dict['CommoditySubProduct'] = 'FUNCTION'
        return msgDict

    def CommodityFurtherSubProduct(self, col_value):
        cmmdty_classfication = FRegulatoryUtils.get_commodity_product_clssfn('CommodityFurtherSubProduct', col_value)
        instrument_attr_dict['CommodityFurtherSubProduct'] = instrument_attr_dict_override['CommodityFurtherSubProduct']
        msgDict = self.reg_info_to_amb('CommodityFurtherSubProduct', cmmdty_classfication, instrument_attr_dict, 'INSTRUMENTREGULATORYINFO')
        instrument_attr_dict['CommodityFurtherSubProduct'] = 'FUNCTION'
        return msgDict

class AMBARegIntoToAddInfoConverter(object):
    def __init__(self, amba_message):
        """class that converts all data related to the regulatory on the FTrade and FInstrument into corresponding AdditionalInfos"""
        self.__amba_message = amba_message
        self.__reg_attr_to_delete = []
        self.__reg_attr_in_amba_msg = []
        self.__reg_info = RegulatoryInfoAMB()
        self.__integration_utils = FIntegrationUtils.FIntegrationUtils()
        self.__acm_version = str(self.__integration_utils.get_acm_version_override())
        if str(self.__acm_version) == '16.4':#need to change the clearing house tag name
            adm_column_name['regClearingHouse'] = 'CLEARING_HOUSE_PTYNBR.PTYID'
        self.__adm_vs_addinfo_dict  = dict(list(zip(list(adm_column_name.values()), list(adm_column_name.keys()))))
        self.__adm_vs_addinfo_dict['CLEARING_HOUSE_PTYNBR.PTYID'] = 'regClearingHouse'
        self.__adm_vs_addinfo_dict['COMMODITY_PRODUCT_CHLNBR.LIST'] = 'regCmdty'
        self.__addinfo_vs_trd_api_dict = dict(list(zip(list(trade_attr_dict.values()), list(trade_attr_dict.keys()))))
        self.__addinfo_vs_ins_api_dict = dict(list(zip(list(instrument_attr_dict.values()), list(instrument_attr_dict.keys()))))
        self.__tag_persist = ['IS_HEDGE', 'DIRECTED_ORDER', 'CLEARING_IS_MANDATORY', 'IS_LIQUID', 'IS_SYSTEMATIC_INTERNALISER']
        self.__tag_name_change = {'CLR_HOUSE_PTYNBR.PTYID' : 'CLEARING_HOUSE_PTYNBR.PTYID'}
        self.__acm_version_lookup = {'2017.2' : ['17_2', '17_1', '16_5', '16_4'], '2017.1' : ['17_1', '16_5', '16_4'], '2016.5' : ['16_5', '16_4'], '2016.4' : ['16_4']}
        self.__remove_prefix = ['TRADING_CAPACITY_', 'DIRECTED_ORDER_', 'IS_LIQUID_', 'SYS_INT_', 'IS_HEDGE_', 'CLEARING_IS_MANDATORY_']
        self.__linked_reg_attr_to_delete = {'THEIR_ORG_PTYNBR.PTYID': 'THEIR_ORG_PTYNBR.LEGAL_ENTITY_ID', \
                                            'OUR_TRANSMIT_ORG_PTYNBR.PTYID': 'OUR_TRANSMIT_ORG_PTYNBR.LEGAL_ENTITY_ID', \
                                            'OUR_ORG_PTYNBR.PTYID': 'OUR_ORG_PTYNBR.LEGAL_ENTITY_ID', \
                                            'ORIGINAL_CPTY_PTYNBR.PTYID': 'ORIGINAL_CPTY_PTYNBR.LEGAL_ENTITY_ID', \
                                            'BRANCH_MEMBERSHIP_PTYNBR.PTYID': 'BRANCH_MEMBERSHIP_PTYNBR.LEGAL_ENTITY_ID', \
                                            'COMMODITY_PRODUCT_CHLNBR.ENTRY': 'COMMODITY_PRODUCT_CHLNBR.LIST', \
                                            'CLR_HOUSE_PTYNBR.PTYID': 'CLR_HOUSE_PTYNBR.LEGAL_ENTITY_ID', \
                                            'CLEARING_HOUSE_PTYNBR.PTYID': 'CLEARING_HOUSE_PTYNBR.LEGAL_ENTITY_ID', \
                                            'OUR_INVEST_DECIDER_SEQNBR': 'OUR_INVEST_DECIDER_SEQNBR.UNIQUE_NAME,OUR_INVEST_DECIDER_SEQNBR.PTYNBR.PTYID,OUR_INVEST_DECIDER_SEQNBR.PTYNBR.LEGAL_ENTITY_ID', \

                                            'THEIR_INVEST_DECIDER_SEQNBR': 'THEIR_INVEST_DECIDER_SEQNBR.PTYNBR.LEGAL_ENTITY_ID,THEIR_INVEST_DECIDER_SEQNBR.PTYNBR.PTYID', \
                                            'THEIR_TRADER_SEQNBR': 'THEIR_TRADER_SEQNBR.PTYNBR.LEGAL_ENTITY_ID,THEIR_TRADER_SEQNBR.PTYNBR.PTYID', }
        self.__all_regs = ['TRADE.TRADEREGULATORYINFO', 'INSTRUMENT.INSTRREGULATORYINFO', 'TRANSACTION.TRADE.TRADEREGULATORYINFO', 'TRANSACTION.INSTRUMENT.INSTRREGULATORYINFO']
        self.__is_trade_reg = False
        self.__is_ins_reg = False
        self.__parent_node = None
        self.__child_reg_node = None

    def insert_into_amba_message(self, amba_message, insert_dict):
        orig_parent = self.__parent_node
        buffer_val = amb.mbf_create_buffer_from_data(amba_message)
        amba_message = buffer_val.mbf_read()
        if not self.__parent_node:
            self.__parent_node = list(insert_dict.keys())[0]
            if self.__parent_node not in ['INSTRREGULATORYINFO', 'TRADEREGULATORYINFO']:
                self.__child_reg_node = list(insert_dict[list(insert_dict.keys())[0]].keys())[0]
            else:
                self.__child_reg_node = self.__parent_node
        mb_node = amba_message.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
        if not mb_node:#it means check for TRANSACTION
            mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
            if mb_node:
                mb_node = mb_node.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
        if self.__parent_node in ['INSTRREGULATORYINFO', 'TRADEREGULATORYINFO']:
            self.__child_reg_node = self.__parent_node
        val = None
        if list(insert_dict.keys()) and list(insert_dict.keys())[0] == self.__parent_node:
            val = insert_dict[list(insert_dict.keys())[0]]
        else:
            vals = insert_dict[orig_parent]
            if list(vals.keys()) and list(vals.keys())[0] == self.__parent_node:
                val = vals[list(vals.keys())[0]]
        mb_msg = None
        if list(val.keys())[0] == 'ADDITIONALINFO':
            bFound = False
            add_key = None
            add_val = None
            if mb_node.mbf_find_object('ADDITIONALINFO', 'MBFE_BEGINNING') :
                handleVal = mb_node.mbf_find_object('ADDITIONALINFO', 'MBFE_BEGINNING')
                child_handleVal = handleVal.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME', 'MBFE_BEGINNING')
                if child_handleVal.mbf_get_value() == list(val.values())[0]['ADDINF_SPECNBR.FIELD_NAME']:#TESTED
                    bFound = True
                    add_info_node_val = self.get_tagvalue(handleVal, 'VALUE')
                    if add_info_node_val != list(val.values())[0]['VALUE']:
                        handleVal.mbf_replace_string('VALUE', str(list(val.values())[0]['VALUE']))
            if not bFound:#TESTED
                mb_msg = mb_node.mbf_start_list(list(val.keys())[0])
                for add_info_val in list(val.values())[0]:
                    mb_msg.mbf_add_string(add_info_val, str(list(val.values())[0][add_info_val]))
                mb_msg.mbf_end_list()
        else:
            if not mb_node.mbf_find_object(self.__child_reg_node, 'MBFE_BEGINNING') and self.__child_reg_node != self.__parent_node:
                mb_msg = mb_node.mbf_start_list(self.__child_reg_node)
                add_key = None
                add_val = None
                if self.__child_reg_node == self.__parent_node:#it means we are directly passing the Reg object
                    add_key = list(val.keys())[0]
                    add_val = list(val.values())[0]
                else:
                    add_key = list(val.values())[0].keys()[0]
                    add_val = str(list(val.values())[0][list(val.values())[0].keys()[0]])
                mb_msg.mbf_add_string(add_key, str(add_val))
                if self.__child_reg_node == 'INSTRUMENTALIAS':
                    mb_msg.mbf_add_string(list(val.values())[0].keys()[1], str(list(val.values())[0][list(val.values())[0].keys()[1]]))
                mb_msg.mbf_end_list()
            else:
                location = None
                key_node = None
                if self.__child_reg_node == self.__parent_node:
                    location = mb_node
                    key_node = list(val.keys())[0]
                else:
                    location = mb_node.mbf_find_object(self.__child_reg_node, 'MBFE_BEGINNING')
                    key_node = list(val.values())[0].keys()[0]
                tagExists = location.mbf_find_object(key_node, 'MBFE_BEGINNING')
                key_nodes = None
                if self.__child_reg_node == self.__parent_node:
                    key_nodes = list(val.keys())
                else:                        
                    key_nodes = list(val.values())[0].keys()
                        
                if tagExists:
                    bFound = False
                    key_node = None
                    node_value = None
                    if self.__child_reg_node == self.__parent_node:
                        key_node = list(val.keys())[0]
                        node_value = list(val.values())[0]
                    else:
                        key_node = list(val.values())[0].keys()[0]
                        node_value = str(list(val.values())[0][list(val.values())[0].keys()[0]])
                    if key_node == 'ADDITIONALINFO':
                        key_vals = list(val.values())[0][list(val.values())[0].keys()[0]].keys()
                        key_val = list(val.values())[0][list(val.values())[0].keys()[0]].keys()[0]
                        val_val = list(val.values())[0][list(val.values())[0].keys()[0]]['ADDINF_SPECNBR.FIELD_NAME']
                        while tagExists:
                            add_info_node_name = self.get_tagvalue(tagExists, 'ADDINF_SPECNBR.FIELD_NAME')
                            add_info_node_val = self.get_tagvalue(tagExists, 'VALUE')
                            if add_info_node_name == val_val:
                                bFound = True
                                if add_info_node_val != list(val.values())[0][list(val.values())[0].keys()[0]]['VALUE']:
                                    tagExists.mbf_replace_string('VALUE', str(list(val.values())[0][list(val.values())[0].keys()[0]]['VALUE']))
                                break
                            else:
                                tagExists = location.mbf_next_object()
                        if not bFound:
                            location = location.mbf_start_list(list(val.values())[0].keys()[0])
                            location.mbf_add_string(key_vals[0], str(list(val.values())[0][list(val.values())[0].keys()[0]].values()[0]))
                            location.mbf_add_string(key_vals[1], str(list(val.values())[0][list(val.values())[0].keys()[0]].values()[1]))
                    else:
                        location.mbf_replace_string(key_node, str(node_value))
                        if len(key_nodes) > 1:
                            if self.__child_reg_node != self.__parent_node:
                                tagExists = location.mbf_find_object(list(val.values())[0].keys()[1], 'MBFE_BEGINNING')
                                if tagExists:
                                    location.mbf_replace_string(list(val.values())[0].keys()[1], str(list(val.values())[0].values()[1]))
                                else:
                                    location.mbf_add_string(list(val.values())[0].keys()[1], str(list(val.values())[0].values()[1]))
                            else:
                                tagExists = location.mbf_find_object(list(val.keys())[1], 'MBFE_BEGINNING')
                                if tagExists:
                                    location.mbf_replace_string(list(val.keys())[1], str(list(val.values())[1]))
                                else:
                                    location.mbf_replace_string(list(val.keys())[1], str(list(val.values())[1]))
                                
                else:
                    if self.__child_reg_node == self.__parent_node:
                        location.mbf_add_string(list(val.keys())[0], str(list(val.values())[0]))
                        if len(key_nodes) > 1:
                            location.mbf_add_string(list(val.keys())[1], str(list(val.values())[1]))
                    else:
                        try:
                            key_vals = list(val.values())[0][list(val.values())[0].keys()[0]].keys()
                            location = location.mbf_start_list(list(val.values())[0].keys()[0])
                            location.mbf_add_string(key_vals[0], str(list(val.values())[0][list(val.values())[0].keys()[0]].values()[0]))
                            location.mbf_add_string(key_vals[1], str(list(val.values())[0][list(val.values())[0].keys()[0]].values()[1]))
                        except:
                            key_vals = list(val.values())[0].keys()
                            for each_key in list(val.values())[0].keys():
                                location.mbf_add_string(each_key, str(list(val.values())[0][each_key]))
                location.mbf_end_list()
        return amba_message.mbf_object_to_string()

    def __is_reg_node_to_delete(self):
        breg_node_delete = False
        if self.__reg_attr_in_amba_msg:
            for each_attr_to_delete in self.__reg_attr_to_delete:
                self.__reg_attr_in_amba_msg.remove(each_attr_to_delete)
            if len(self.__reg_attr_in_amba_msg) == 0:
                breg_node_delete = True
        return breg_node_delete

    def delete_reg_info_tag(self, each_reg_tag):
        buffer_val = amb.mbf_create_buffer_from_data(self.__amba_message)
        amba_message = buffer_val.mbf_read()
        mb_node = amba_message.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
        if not mb_node:#it means TRANSACTION node should be looked for
            mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
            if mb_node:
                mb_node = mb_node.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
        location = mb_node.mbf_find_object(self.__child_reg_node, 'MBFE_BEGINNING')
        if location:
            tagExists = location.mbf_find_object(each_reg_tag, 'MBFE_BEGINNING')
            if tagExists:
                location.mbf_remove_object()
        self.__amba_message = amba_message.mbf_object_to_string()

    def delete_child_node(self):
        buffer_val = amb.mbf_create_buffer_from_data(self.__amba_message)
        amba_message = buffer_val.mbf_read()
        mb_node = amba_message.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
        if not mb_node:#it means TRANSACTION node should be looked for
            mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
            if mb_node:
                mb_node = mb_node.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
        if mb_node:
            location = mb_node.mbf_find_object(self.__child_reg_node, 'MBFE_BEGINNING')
            if location:
                mb_node.mbf_remove_object()
        self.__amba_message = amba_message.mbf_object_to_string()

    def delete_reg_info_tags(self):
        breg_node_delete = self.__is_reg_node_to_delete()
        if breg_node_delete or str(self.__acm_version) in ['2015.1', '2015.2', '2015.3', '2015.4', '2016.1', '2016.2', '2016.3']:
            self.delete_child_node()
        else:
            for each_reg_tag in self.__reg_attr_to_delete:
                self.delete_reg_info_tag(each_reg_tag)

    def get_tagvalue (self, message, tagname):
        """ Get value for tag from the message """
        mb_message = message
        if mb_message:
            tag = mb_message.mbf_find_object(tagname, 'MBFE_BEGINNING')
            if tag:
                val = tag.mbf_get_value()
                if val not in ['N.A.', 'N.S.', 'N.D.', ' ']:
                    return val.strip()
        return ''

    def move_add_info_tags(self, amba_node):
        add_info_dict = {}
        #it means any addinfos on this node also need to be moved onto the parent i.e FInstrument/FTrade
        if str(self.__acm_version) in ['2015.1', '2015.2', '2015.3', '2015.4', '2016.1', '2016.2', '2016.3', '2016.4']:
            add_info_node = amba_node.mbf_find_object('ADDITIONALINFO', 'MBFE_BEGINNING')
            while add_info_node:
                add_info_node_name = self.get_tagvalue(add_info_node, 'ADDINF_SPECNBR.FIELD_NAME')
                add_info_node_val = self.get_tagvalue(add_info_node, 'VALUE')
                add_info_dict[add_info_node_name] = add_info_node_val
                add_info_node = amba_node.mbf_next_object()
        for each_add_info in add_info_dict:
            buffer = amb.mbf_create_buffer_from_data(self.__amba_message)
            amba_message = buffer.mbf_read()
            mb_node = amba_message.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
            if not mb_node:
                mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
                if mb_node:
                    mb_node = mb_node.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
            mb_node = mb_node.mbf_start_list('ADDITIONALINFO')
            mb_node.mbf_add_string('ADDINF_SPECNBR.FIELD_NAME', str(each_add_info))
            mb_node.mbf_add_string('VALUE', str(add_info_dict[each_add_info]))
            mb_node.mbf_end_list()
            self.__amba_message = amba_message.mbf_object_to_string()
        if add_info_dict and str(self.__acm_version) == '2016.4':
            for each_add_info in add_info_dict:
                buffer = amb.mbf_create_buffer_from_data(self.__amba_message)
                amba_message = buffer.mbf_read()
                mb_node = amba_message.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
                if not mb_node:
                    mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
                    if mb_node:
                        mb_node = mb_node.mbf_find_object(self.__parent_node, 'MBFE_BEGINNING')
                if mb_node:
                    mb_node = mb_node.mbf_find_object(self.__child_reg_node, 'MBFE_BEGINNING')
                if mb_node.mbf_find_object('ADDITIONALINFO', 'MBFE_BEGINNING'):
                    handleVal = mb_node.mbf_find_object('ADDITIONALINFO', 'MBFE_BEGINNING')
                    handleVal = handleVal.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME', 'MBFE_BEGINNING')
                    if handleVal.mbf_get_value() == each_add_info:
                        mb_node.mbf_remove_object()
                self.__amba_message = amba_message.mbf_object_to_string()

    def create_add_info_tags(self, amba_node, each_element):
        val  = None
        tagExists = amba_node.mbf_find_object(each_element, 'MBFE_BEGINNING')
        if tagExists:
            self.__reg_attr_in_amba_msg.append(each_element)
            if each_element in self.__linked_reg_attr_to_delete:
                additional_tags = self.__linked_reg_attr_to_delete[each_element].split(',')
                self.__reg_attr_in_amba_msg.extend(additional_tags)
            node_val = tagExists.mbf_get_value()
            b_create_add_info = True
            b_change_reg_name = False
            if self.__acm_version in self.__acm_version_lookup:
                for each_lookup in self.__acm_version_lookup[self.__acm_version]:
                    folderName = 'FRegulatoryUtils.add_info_dict_' + each_lookup
                    if self.__adm_vs_addinfo_dict[each_element] in eval(folderName):
                        b_create_add_info = False
                        if str(self.__acm_version) in ['2016.4', '2016.5', '2017.1'] and each_element in self.__tag_persist:
                            b_change_reg_name = True
                        if str(self.__acm_version) == '2016.4' and each_element == 'CLR_HOUSE_PTYNBR.PTYID' and self.__adm_vs_addinfo_dict[each_element] == 'regClearingHouse':
                            b_change_reg_name = True
            if b_create_add_info or b_change_reg_name:
                if b_change_reg_name and each_element == 'CLR_HOUSE_PTYNBR.PTYID':
                    pass
                elif (each_element not in self.__tag_persist) or ((each_element in self.__tag_persist) and (not b_change_reg_name)):
                    self.__reg_attr_to_delete.append(each_element)
                    if each_element in self.__linked_reg_attr_to_delete:
                        additional_tags = self.__linked_reg_attr_to_delete[each_element].split(',')
                        self.__reg_attr_to_delete.extend(additional_tags)
                for each_replace_val in remove_prefix:
                    node_val = node_val.replace(each_replace_val, '')
                if b_change_reg_name:
                    if self.__is_trade_reg:
                        add_info_val = self.__reg_info.tradeRegInfo2amb(self.__addinfo_vs_trd_api_dict[self.__adm_vs_addinfo_dict[each_element]], node_val)
                        if each_element == 'CLR_HOUSE_PTYNBR.PTYID' and str(self.__acm_version)== '2016.4':#it means we need to delete this one
                            self.__reg_attr_to_delete.append(each_element)
                            if each_element in self.__linked_reg_attr_to_delete:
                                additional_tags = self.__linked_reg_attr_to_delete[each_element].split(',')
                                self.__reg_attr_to_delete.extend(additional_tags)
                                self.__reg_attr_in_amba_msg.append(add_info_val)
                    elif self.__is_ins_reg:
                        key = self.__adm_vs_addinfo_dict[each_element]
                        if key == 'regClearingIsMandatory':
                            key = 'regClearingIsMandat'
                        add_info_val = self.__reg_info.instrumentRegInfo2amb(self.__addinfo_vs_ins_api_dict[key], node_val)
                elif self.__is_trade_reg:
                    add_info_val = self.__reg_info.tradeRegInfo2amb(self.__addinfo_vs_trd_api_dict[self.__adm_vs_addinfo_dict[each_element]], node_val)
                    if each_element == 'CLR_HOUSE_PTYNBR.PTYID' and str(self.__acm_version)== '2016.4':#it means we need to delete this one
                        self.__reg_attr_to_delete.extend(each_element)
                    self.__reg_attr_in_amba_msg.append(add_info_val)#indentation moved outwards for creating singular AddInfo tags also
                elif self.__is_ins_reg:
                    node_key = None
                    key = self.__adm_vs_addinfo_dict[each_element]
                    if key == 'regClearingIsMandatory':
                        key = 'regClearingIsMandat'
                    if key in self.__addinfo_vs_ins_api_dict:
                        node_key = self.__addinfo_vs_ins_api_dict[key]
                    else:
                        node_key = 'CommodityFurtherSubProduct'
                    add_info_val = self.__reg_info.instrumentRegInfo2amb(node_key, node_val)
                    self.__reg_attr_in_amba_msg.append(add_info_val)
                self.__amba_message = self.insert_into_amba_message(self.__amba_message, add_info_val)
            else:
                FRegulatoryLogger.INFO(logger, \
                    "Not creating AddInfo for %s as ADM column exists for this attribute in version %s"%(each_element, self.__acm_version))

    def regulatory_to_add_info_converter(self):
        for each_reg in self.__all_regs:
            amba_node = self.get_amba_node(each_reg)
            if amba_node:
                if each_reg in ['TRADE.TRADEREGULATORYINFO', 'TRANSACTION.TRADE.TRADEREGULATORYINFO']:
                    self.__is_trade_reg = True
                    self.__is_ins_reg = False
                    self.__parent_node = 'TRADE'
                    self.__child_reg_node = 'TRADEREGULATORYINFO'
                    self.__reg_attr_to_delete = []
                    self.__reg_attr_in_amba_msg = []
                    for each_element in self.__adm_vs_addinfo_dict:
                        self.create_add_info_tags(amba_node, each_element)
                    self.move_add_info_tags(amba_node)
                    self.delete_reg_info_tags()
                if each_reg in ['INSTRUMENT.INSTRREGULATORYINFO', 'TRANSACTION.INSTRUMENT.INSTRREGULATORYINFO']:
                    self.__is_trade_reg = False
                    self.__is_ins_reg = True
                    self.__parent_node = 'INSTRUMENT'
                    self.__child_reg_node = 'INSTRREGULATORYINFO'
                    self.__reg_attr_to_delete = []
                    self.__reg_attr_in_amba_msg = []
                    for each_element in self.__adm_vs_addinfo_dict:
                        self.create_add_info_tags(amba_node, each_element)
                    self.move_add_info_tags(amba_node)
                    self.delete_reg_info_tags()
            else:
                buffer = amb.mbf_create_buffer_from_data(self.__amba_message)
                amba_message = buffer.mbf_read()
                if each_reg in ['TRADE.TRADEREGULATORYINFO', 'TRANSACTION.TRADE.TRADEREGULATORYINFO']:
                    mb_node = None
                    if each_reg == 'TRADE.TRADEREGULATORYINFO':
                        mb_node = amba_message.mbf_find_object('TRADE', 'MBFE_BEGINNING')
                    elif each_reg == 'TRANSACTION.TRADE.TRADEREGULATORYINFO':
                        mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
                        if mb_node:
                            mb_node = mb_node.mbf_find_object('TRADE', 'MBFE_BEGINNING')
                    if mb_node:
                        FRegulatoryLogger.INFO(logger, "There are no RegulatoryInfo related attributes on the trade")
                    else:
                        self.__parent_node = 'TRADE'
                        self.__child_reg_node = 'TRADEREGULATORYINFO'
                if each_reg in ['INSTRUMENT.INSTRREGULATORYINFO', 'TRANSACTION.INSTRUMENT.INSTRREGULATORYINFO']:
                    mb_node = None
                    if each_reg == 'INSTRUMENT.INSTRREGULATORYINFO':
                        mb_node = amba_message.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
                    elif each_reg == 'TRANSACTION.INSTRUMENT.INSTRREGULATORYINFO':
                        mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
                        if mb_node:
                            mb_node = mb_node.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
                    if mb_node:
                        FRegulatoryLogger.INFO(logger, "There are no RegulatoryInfo related attributes on the trade")
                    else:
                        self.__parent_node = 'INSTRUMENT'
                        self.__child_reg_node = 'INSTRREGULATORYINFO'
        self.delete_reg_node()
        return self.__amba_message

    def delete_reg_node(self):
        parent_node_dict = {'TRADE' : 'TRADEREGULATORYINFO', 'INSTRUMENT' : 'INSTRREGULATORYINFO'}
        for each_parent in parent_node_dict:
            buffer = amb.mbf_create_buffer_from_data(self.__amba_message)
            amba_message = buffer.mbf_read()
            mb_node = amba_message.mbf_find_object(each_parent, 'MBFE_BEGINNING')
            parent_node = mb_node
            if not mb_node:#it means TRANSACTION node should be looked for
                mb_node = amba_message.mbf_find_object('TRANSACTION', 'MBFE_BEGINNING')
                if mb_node:
                    mb_node = mb_node.mbf_find_object(each_parent, 'MBFE_BEGINNING')
                    parent_node = mb_node
            if parent_node:
                location = mb_node.mbf_find_object(parent_node_dict[each_parent], 'MBFE_BEGINNING')
                if location and (not location.mbf_first_object()):
                    parent_node.mbf_remove_object()
            self.__amba_message = amba_message.mbf_object_to_string()

    def get_amba_node(self, location):
        buffer = amb.mbf_create_buffer_from_data(self.__amba_message)
        amba_message = buffer.mbf_read()
        heirarchy = location.split('.')
        amba_node = None
        for each_level in heirarchy:
            amba_node = amba_message.mbf_find_object(each_level, 'MBFE_BEGINNING')
            if amba_node:
                amba_message = amba_node
        amba_message = amba_node
        return amba_message

def AMBARegulatoryToAddInfoConverter(amba_message):
    amba_converter = AMBARegIntoToAddInfoConverter(amba_message)
    amba_message = amba_converter.regulatory_to_add_info_converter()
    return amba_message

