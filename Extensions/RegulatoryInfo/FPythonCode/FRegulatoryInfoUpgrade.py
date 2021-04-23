""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FRegulatoryInfoUpgrade.py"
"""------------------------------------------------------------------------
MODULE
    FRegulatoryInfoUpgrade -
DESCRIPTION:
    This file is to be executed when user upgrades from one PRIME version to another. 
    Executing this script will move up all RegulatoryInfo to the respective columns/AddInfos 
    depending upon the version that it is being upgraded to
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import acm
import FIntegrationUtils
import FRegulatoryLogger
import FRegulatoryInfoSpecs
FRegulatoryInfoSpecs.upgrade_for_changes()
logger = 'FRegulatoryInfoUpgrade'
from datetime import datetime
trade_add_info_dict = {'regTransmOfOrder': 'TransmissionOfOrdersIndicator', 'regInvesDecidrCrmId': 'InvestmentDeciderCrmId', 'regProvideLiquidity': 'IsProvidingLiquidity', \
                        'regComplexTrdCmptId': 'ComplexTradeComponentId', 'regRepositoryId': 'RepositoryId', 'regExecutingEntity': 'ExecutingEntity', \
                        'regVenue': 'Venue', 'regReportingEntity': 'ReportingEntity', 'regComdtyDerivInd': 'IsCommodityDerivative', 'regSecFinTransInd': 'IsSecurityFinancingTransaction', \
                        'regExchangeId': 'ExchangeId', 'regAlgoId': 'AlgoId', 'regNearLegIsin': 'NearLegIsin', 'regFarLegIsin': 'FarLegIsin', 'RegInsCfiCode': 'CfiCode', \
                        'regInsIsin': 'Isin', }
trade_add_info_dict_2016_4 = {'regMicroSeconds': 'TimePrecision', 'regClearingHouse': 'ClearingHouse',}
trade_add_info_dict_2016_5_upgrade = {'regClearingBroker': 'ClearingBroker', 'regMiddleware': 'Middleware', 'regOriginalCpty': 'OriginalCounterparty', 'regRepository': 'Repository', 'regIsHedge': 'IsHedge', }
trade_add_info_dict_2016_5 = dict(trade_add_info_dict_2016_5_upgrade, **trade_add_info_dict_2016_4)

trade_add_info_dict_2017_1_upgrade = {'regTradingCapacity': 'TradingCapacity', 'regWaiver': 'Waiver', 'regOTCPostTradeInd': 'OtcPostTradeIndicator', \
                            'regOurOrg': 'OurOrganisation', 'regOurTransmitOrg': 'OurTransmittingOrganisation', 'regOurInvesDecider': 'OurInvestmentDecider', \
                            'regBranchMemberShip': 'BranchMembership', 'regTheirOrg': 'TheirOrganisation', 'regTheirInvDecider': 'TheirInvestmentDecider', \
                            'regTheirTrader': 'TheirTrader', 'regDirectedOrder': 'DirectedOrder', 'regClearingTime': 'ClearingTime', \
                            'regConfirmationTime': 'ConfirmationTime', 'regOurTrader': 'OurTrader', }
trade_add_info_dict_2017_1 = dict(trade_add_info_dict_2017_1_upgrade, **trade_add_info_dict_2016_5)
trade_add_info_dict_2017_2_upgrade = {'regRptDeferToTime' : 'ReportDeferToTime'} 
trade_add_info_dict_2017_2 = dict(trade_add_info_dict_2017_2_upgrade, **trade_add_info_dict_2017_1)
trade_version_list = ['2016_5', '2017_1', '2017_2']

instrument_add_info_dict = {
'regTransactionType': 'TransactionType',
'regFinalPriceType': 'FinalPriceType',
'regDarkCapStatus': 'DarkCapStatus',
'regDblVolCapStatus': 'DoubleVolumeCapStatus',
'regTrdAdmisAppTime': 'AdmissionApprovalTime',
'regTrdAdmisReqTime': 'AdmissionRequestTime',
'regFirstTradeTime': 'FirstTradingTime',
'regTrdTerminateDate': 'TradingTerminationDate',
'regToTV': 'IsTradedOnTradingVenue',
'regHasTrdObligation': 'HasTradingObligation',
'regMiFIDTransparent': 'IsMiFIDTransparent',
'regSimilarIsin': 'SimilarIsin',
'regPrimaryMktMic': 'PrimaryMarketMic',
'regMaterialMktMic': 'MaterialMarketMic',
'regDarkCapMic': 'DarkCapMic',
'regFISN': 'FinancialInstrumentShortName',

'regSMS': 'StandardMarketSize',
'regLiquidityBand': 'LiquidityBand',
'regTickSize': 'TickSize',
'regPostLargeInScale': 'PostLargeInScale',
'regPostSSTI': 'PostSizeSpecificToInstrument',
}
instrument_add_info_dict_2016_4 = {'regClearingIsMandat': 'ClearingIsMandatory', 'regCFICode': 'CfiCode',}
instrument_add_info_dict_2016_5_upgrade = {'regLargeInScale' : 'LargeInScale', 'regSSTI' : 'SizeSpecificToInstrument'}
instrument_add_info_dict_2016_5 = dict(instrument_add_info_dict_2016_5_upgrade, **instrument_add_info_dict_2016_4)
instrument_add_info_dict_2017_1_upgrade = {'regIsLiquid' : 'IsLiquid', 'regIsSysInternalizr' : 'IsSystematicInternaliser', 'regCmdty' : 'CommodityProduct'}
instrument_add_info_dict_2017_1 = dict(instrument_add_info_dict_2017_1_upgrade, **instrument_add_info_dict_2016_5)
instrument_add_info_dict_2017_2_upgrade = {'regAvgDailyTO': 'AverageDailyTurnover', }
instrument_add_info_dict_2017_2 = dict(instrument_add_info_dict_2017_2_upgrade, **instrument_add_info_dict_2017_1)
instrument_version_list = ['2016_5', '2017_1', '2017_2']
contact_add_info_dit_2017_2 = {'uniqueName': 'UniqueName', }
different_handling = {  'uniqueName' : 'UniqueName', 'regOurTrader' : 'OurTrader', \
                        'regTradingCapacity' : 'TradingCapacity', 'regTheirTrader': 'TheirTrader', \
                        'regTheirInvDecider': 'TheirInvestmentDecider', 'regOurInvesDecider': 'OurInvestmentDecider', \
                        'regTransactionType' : 'TransactionType', 'regFinalPriceType' : 'FinalPriceType', \
                        'regDarkCapStatus' : 'DarkCapStatus', 'regDblVolCapStatus' : 'DoubleVolumeCapStatus', \
                        'regCmdty' : 'CommodityProduct'}

float_data_types = ['regSMS', 'regTickSize', 'regPostLargeInScale', 'regPostSSTI', 'regLargeInScale', 'regSSTI', 'regAvgDailyTO']
log_name = ['ClearingBroker', 'ClearingHouse', 'Middleware', 'OriginalCounterparty', 'Repository', 'OurOrganisation', \
            'OurTransmittingOrganisation', 'BranchMembership', 'TheirOrganisation', 'ExecutingEntity', 'Venue', 'ReportingEntity']
log_timestamps = ['ReportDeferToTime', 'ConfirmationTime', 'ClearingTime', 'FirstTradingTime', 'AdmissionApprovalTime', \
                    'AdmissionRequestTime', 'TradingTerminationDate']
log_fullname = ['OurInvestmentDecider', 'TheirInvestmentDecider', 'TheirTrader', 'OurTrader']
obsolete_add_infos = ['regLegIsin', 'regSimilarIns', 'regInsSimilarIsin', 'regJointAccount' ]
no_commit_on_reg_info = ['OurTrader']
short_sell_lookup = {'Buy Cover' : 'Short Security', 'Sell Short' : 'Short Security', 'Sell Short Exempt' : 'Short Sell Exempt', 'Sell Short Undi' : 'Short Sell Undi'}

class FRegulatoryInfoUpgrade(object):
    def __init__(self):
        self.acm_object = None
        self.acm_object_reg_info = None
        self.b_parent = True
        self.object_type = ''
        self.object_id = ''
        self.add_info_dict = None
        self.integration_utils = FIntegrationUtils.FIntegrationUtils()
        self.delete_add_info = {}
        self.renamed_add_infos = {}

    def is_on_parent(self):
        """returns whether the data is being upgraded from parent to RegulatoryInfo or child RegulatoryInfo's AddInfos to ADM column"""
        pass

    def delete_obsolete_add_info_specs(self):
        """delete the AddInfoSpecs that are no longer being used within the Regulatory package"""
        for add_info_spec in list(obsolete_add_infos):
            addInf = acm.FAdditionalInfoSpec[add_info_spec]
            if addInf:
                add_infos = acm.FAdditionalInfo.Select("addInf = %d"%addInf.Oid())
                if not add_infos:
                    FRegulatoryLogger.DEBUG(logger, "Deleting AddInfoSpec <%s>."%add_info_spec)
                    addInf.Delete()
                else:
                    FRegulatoryLogger.WARN(logger, "Cannot delete AddInfoSpec <%s> as reference to this AddInfoSpec still exist."%add_info_spec)

    def set_lookup_dict(self, add_info_dict):
        """set the dictionary of AddInfo vs API that needs to be executed for RegulatoryInfo upgrade"""
        self.add_info_dict = add_info_dict

    def rename_parent_add_info(self):
        """rename the original AddInfo with a prefixed T before upgrading data onto the RegulatoryInfo AddInfos/ADM columns"""
        b_add_info_spec_found = False
        if self.b_parent:
            for add_info in self.add_info_dict.keys():
                add_info_spec = acm.FAdditionalInfoSpec[add_info]
                changed_name = self.get_renamed_add_info(add_info)
                parent_add_info_spec = acm.FAdditionalInfoSpec[changed_name]
                if add_info_spec:
                    if 'RegulatoryInfo' in add_info_spec.RecType():                        
                        if parent_add_info_spec and parent_add_info_spec.RecType() in ['Trade', 'Instrument']:#it means the upgrade has been done
                            b_add_info_spec_found = False
                    else:
                        if not parent_add_info_spec:
                            add_info_spec.Name('T' + add_info_spec.Name())
                            add_info_spec.Commit()
                            b_add_info_spec_found = True
            if b_add_info_spec_found:
                import FRegulatoryInfoSpecs
                FRegulatoryLogger.WARN(logger, "PRIME needs to be restarted to continue further!!!")
        return b_add_info_spec_found

    def get_contact(self, org, contact_name):
        """get the contact object from its name and the party that it belongs to"""
        contact_obj = None
        if org:
            for contact in org.Contacts():
                if contact.Fullname() == contact_name:
                    contact_obj = contact
                    break
        return contact_obj
        
    def copy_parent_add_info_to_child(self, add_info_name, add_info_api, add_info_val, reg_info_api):
        """copies the addinfo from Trade/Instrument to its corresponding RegulatoryInfo instance"""
        if str(add_info_val) != 'None':
            add_info_log_val = self.get_add_info_log_val(add_info_val, reg_info_api)
            try:
                reg_info = self.acm_object.RegulatoryInfo()
                FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo attribute <%s> on <%s> of id/name <%s> with value <%s>."%(reg_info_api, self.object_type, self.object_id, add_info_log_val))#tested
                if reg_info_api in log_name or reg_info_api in log_timestamps:
                    eval('reg_info.' + reg_info_api + "('" + add_info_log_val + "')")
                elif different_handling.has_key(add_info_name):
                    reg_info = eval('self.' + different_handling[add_info_name] + "('" + str(add_info_val) + "', reg_info)")
                else:
                    if reg_info_api not in no_commit_on_reg_info:
                        eval('reg_info.' + reg_info_api + "('" + str(add_info_val) + "')")
                reg_info.Commit()
            except Exception, e:
                FRegulatoryLogger.ERROR(logger, "Error occured while copying <%s> from AddInfo <%s> on <%s> of id/name <%s> to the RegulatoryInfo instance. Error: <%s>"%(add_info_log_val, add_info_name, self.object_type, self.object_id, str(e)))#tested

    def verify_parent_add_info_on_child(self, add_info_name, add_info_api, reg_info_api, b_reg = False):
        """verifies the addinfo on Trade/Instrument is copied to its corresponding RegulatoryInfo instance"""
        reg_info_val = None
        if b_reg:
            acm_object = self.acm_object_reg_info
        else:
            acm_object = self.acm_object
        b_mismatch = True
        add_info_on_parent = None
        try:
            add_info_on_parent = eval('acm_object.AdditionalInfo().' + add_info_api + '()')
        except:
            pass
        reg_info_val = eval('self.acm_object.RegulatoryInfo().' + reg_info_api + '()')
        if add_info_name not in different_handling.keys():
            if add_info_on_parent:
                if add_info_name in float_data_types:
                    reg_info_val = str(format(reg_info_val, ".4f"))#rounding off to 4 decimals, else comparing of floats is not possible
                    add_info_on_parent = str(format(add_info_on_parent, ".4f"))

                if add_info_on_parent == reg_info_val:
                    b_mismatch = False
                elif reg_info_api in log_timestamps:#it means the AddInfo stores it as int and ADM coulmn stores it as a datetime value and there will be mismatch
                    add_info_log_val = self.get_add_info_log_val(add_info_on_parent, reg_info_api)
                    reg_info_log_val = self.get_add_info_log_val(reg_info_val, reg_info_api)
                    if add_info_log_val == reg_info_log_val:
                        b_mismatch = False
                
                if b_mismatch:
                    add_info_log_val = self.get_add_info_log_val(add_info_on_parent, reg_info_api)
                    reg_info_log_val = self.get_add_info_log_val(reg_info_val, reg_info_api)
                    FRegulatoryLogger.ERROR(logger, "Mismatch in values between AddInfo <%s> on <%s> of id/name <%s> with value <%s> and <%s> on its RegulatoryInfo instance."%(add_info_name, self.object_type, self.object_id, add_info_log_val, reg_info_val))
            else:#it means there is no AddInfo value for this Reg Attrbiute
                b_mismatch = False
        else:
            if reg_info_val and add_info_on_parent:
                if reg_info_api == 'OurTrader':
                    parent_party = None
                    try:
                        parent_party = acm_object.AdditionalInfo().RegOurOrg()
                    except:
                        pass
                    if not parent_party:
                        parent_party = self.acm_object_reg_info.OurOrganisation()
                    contact_obj = self.get_contact(parent_party, add_info_on_parent)
                    if contact_obj:
                        if contact_obj.Person():
                            add_info_on_parent = contact_obj.Person()
                            reg_info_val = self.acm_object.Trader().Person()
                if add_info_name in float_data_types:
                    reg_info_val = str(format(reg_info_val, ".4f"))#rounding off to 4 decimals, else comparing of floats is not possible
                    add_info_on_parent = str(format(add_info_on_parent, ".4f"))
                if reg_info_api == 'CommodityProduct':
                    if reg_info_val:
                        reg_info_val = reg_info_val.Oid()
                if reg_info_api in log_fullname and ((reg_info_val.IsKindOf(acm.FContact) and reg_info_val.Fullname() == add_info_on_parent) or (reg_info_val.IsKindOf(acm.FUser) and reg_info_val.FullName() == add_info_on_parent)):
                    b_mismatch = False
                elif reg_info_val == add_info_on_parent:
                    b_mismatch = False
                elif reg_info_val.IsKindOf(acm.FChoiceList) and reg_info_val.Name() == add_info_on_parent:
                    b_mismatch = False
            elif str(add_info_on_parent) == 'None':
                b_mismatch = False
        return b_mismatch

    def delete_parent_add_info_on_child(self, add_info_name, add_info_val, b_reg = False):
        """deletes the addinfo from Trade/Instrument as it is copied to its corresponding RegulatoryInfo instance"""
        acm_object = None
        object_type = None
        object_id = None
        if b_reg:
            if add_info_name.startswith('Treg'):
                b_reg = False
        if b_reg:
            acm_object = self.acm_object_reg_info
            if self.acm_object_reg_info.IsKindOf(acm.FTradeRegulatoryInfo):
                object_type = 'TradeRegulatoryInfo'
            elif self.acm_object_reg_info.IsKindOf(acm.FInstrumentRegulatoryInfo):
                object_type = 'InstrumentRegulatoryInfo'
            object_id = self.acm_object_reg_info.Oid()
        else:
            acm_object = self.acm_object
            object_type = self.object_type
            object_id = self.object_id
        FRegulatoryLogger.DEBUG(logger, "Deleting addInfo <%s> on <%s> of id/name <%s>."%(add_info_name, object_type, object_id))
        ais = acm.FAdditionalInfoSpec[add_info_name]
        aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (ais.Oid(), acm_object.Oid()))
        if aiSel and str(aiSel[0]) != 'None':
            self.integration_utils.update_addtional_info(aiSel[0])

    def copy_child_add_info_to_column(self, add_info_name, add_info_api, add_info_val, reg_info_api):
        """copies the AddInfo on the RegulatoryInfo instance to its ADM column"""
        if str(add_info_val) != 'None':
            add_info_log_val = self.get_add_info_log_val(add_info_val, reg_info_api)
            try:
                FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo attribute <%s> on <%s> of id/name <%s> with value <%s>."%(reg_info_api, self.object_type, self.object_id, add_info_log_val))#tested
                if reg_info_api in log_name or reg_info_api in log_timestamps:
                    eval('self.acm_object_reg_info.' + reg_info_api + "('" + add_info_log_val + "')")
                elif different_handling.has_key(add_info_name):
                    self.acm_object_reg_info = eval('self.' + different_handling[add_info_name] + "('" + add_info_val + "', self.acm_object_reg_info)")
                else:
                    if reg_info_api not in no_commit_on_reg_info:
                        eval('self.acm_object_reg_info.' + reg_info_api + "('" + str(add_info_val) + "')")
                self.acm_object_reg_info.Commit()
            except Exception, e:
                FRegulatoryLogger.ERROR(logger, "Error occured while copying <%s> from AddInfo <%s> on <%s> of id/name <%s> to the RegulatoryInfo instance. Error: <%s>"%(add_info_log_val, add_info_name, self.object_type, self.object_id, str(e)))#tested


    def get_reg_info_api_name(self, add_info_name):
        """get the corresponding RegInfo API from the AddInfo name"""
        return self.add_info_dict[add_info_name]

    def get_add_info_name(self, add_info):
        """get the corresponding AddInfo API from the AddInfo name"""
        return add_info[0].upper() + add_info[1:]
    
    def get_renamed_add_info(self, add_info):
        """get the corresponding renamed AddInfo name before upgrading data"""
        rename_add_info = 'T' + add_info
        rename_add_info = rename_add_info[0:19]
        self.renamed_add_infos[rename_add_info] = ''
        return rename_add_info

    def get_renamed_add_infos_list(self):
        return self.renamed_add_infos

    def get_add_info_log_val(self, add_info_val, add_info_api):
        """get the AddInfo value in logable form"""
        add_info_log_val = add_info_val
        if add_info_val:
            if add_info_api in log_name:
                add_info_log_val = add_info_val.Name()
            elif add_info_api in log_timestamps:
                if '1970-01-01' not in str(add_info_val) and str(add_info_val).isdigit():#it means there is no value in it actually, should be called only for AddInfo and not for Reg values
                        add_info_log_val = str(datetime.fromtimestamp(add_info_val))
                    
            elif add_info_api in log_fullname:
                try:
                    if add_info_api.IsKindOf(acm.FContact):
                        add_info_log_val = add_info_val.Fullname()
                except:
                    pass
        return add_info_log_val

    def upgrade_reg_info(self, add_info_name, parent_object, renamed = False):
        """upgrade the Regulatory Info from parent/child AddInfos to the Regulatory ADM columns"""
        add_info_val = None
        add_info_api = None
        self.acm_object = parent_object
        self.acm_object_reg_info = parent_object.RegulatoryInfo()
        if self.b_parent:
            if renamed:
                add_info_api = self.get_renamed_add_info(add_info_name)
            else:
                add_info_api = self.get_add_info_name(add_info_name)
            reg_info_api = self.get_reg_info_api_name(add_info_name)
            if not acm.FAdditionalInfoSpec[add_info_name]:
                return
            add_info_val = None
            try:
                add_info_val = eval('self.acm_object.AdditionalInfo().' + add_info_api + '()')
            except:
                pass
            self.set_object_type_id()
            self.copy_parent_add_info_to_child(add_info_name, add_info_api, add_info_val, reg_info_api)
            b_mismatch = self.verify_parent_add_info_on_child(add_info_name, add_info_api, reg_info_api)
            if (not b_mismatch) and str(add_info_val) != 'None':#it means, the AddInfo on the parent can be deleted
                if renamed:
                    self.delete_add_info[add_info_api] = add_info_val
                else:
                    self.delete_add_info[add_info_name] = add_info_val
        else:
            add_info_api = self.get_add_info_name(add_info_name)
            reg_info_api = self.get_reg_info_api_name(add_info_name)
            add_info_val = None
            try:
                add_info_val = eval('self.acm_object_reg_info.AdditionalInfo().' + add_info_api + '()')
            except:
                pass
            self.set_object_type_id()
            self.copy_child_add_info_to_column(add_info_name, add_info_api, add_info_val, reg_info_api)
            b_mismatch = self.verify_parent_add_info_on_child(add_info_name, add_info_api, reg_info_api, True)
            if str(add_info_val) != 'None':#it means, the AddInfo on the parent can be deleted
                if (not b_mismatch):
                    self.delete_add_info[add_info_name] = add_info_val
                else:
                    FRegulatoryLogger.ERROR(logger, "Mismtach for <%s>. Hence not deleting it."%add_info_name)

    def delete_parent_add_info(self, b_reg = False):
        """delete the AddInfo value on the parent object once the upgrade is complete"""
        for add_info_name in self.delete_add_info:
            self.delete_parent_add_info_on_child(add_info_name, self.delete_add_info[add_info_name], b_reg)

    def delete_addinfo(self, add_info_spec, acm_object):
        """delete the given AddInfo"""
        ais = acm.FAdditionalInfoSpec[add_info_spec]
        if ais:
            aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (ais.Oid(), acm_object.Oid()))
            if aiSel and str(aiSel[0]) != 'None':
                self.integration_utils.update_addtional_info(aiSel[0])

    def set_object_type_id(self):
        """set the object type to be the parent/child on the basis of the version that the script is being executed upon for upgrade"""
        pass

    def delete_add_info_specs(self):
        """delete the AddInfo specs on the Instrument/RegulatoryInfo instance once the data is upgraded to their corresponding ADM columns/AddInfos"""
        for add_info_spec in self.add_info_dict.keys():
            addInf = acm.FAdditionalInfoSpec[add_info_spec]
            if addInf:
                add_infos = acm.FAdditionalInfo.Select("addInf = %d"%addInf.Oid())
                if not add_infos:
                    FRegulatoryLogger.DEBUG(logger, "Deleting AddInfoSpec <%s> on %s"%(add_info_spec, addInf.RecType()))
                    addInf.Delete()
                else:
                    FRegulatoryLogger.WARN(logger, "Cannot delete AddInfoSpec <%s> on %s as reference to this AddInfoSpec still exist."%(add_info_spec, addInf.RecType()))
                    
class FTradeRegulatoryInfoUpgrade(FRegulatoryInfoUpgrade):
    def __init__(self):
        """class that handles the upgrade of all Regulatory data on the Trade object to its RegulatoryInfo object"""
        FRegulatoryInfoUpgrade.__init__(self)

    def set_object_type_id(self):
        """set the object type to be the parent/child on the basis of the version that the script is being executed upon for upgrade"""
        try:
            if self.acm_object.IsKindOf(acm.FTrade) or self.acm_object_reg_info.IsKindOf(acm.FTradeRegulatoryInfo):
                self.object_type = 'Trade'
                self.object_id = str(self.acm_object.Oid())
        except Exception, e:
            print "Error while attempting to get the object type that the upgrade script is being executed upon"
    
    def is_on_parent(self):
        """returns whether the data is being upgraded from parent Trade to RegulatoryInfo or child RegulatoryInfo's AddInfos to ADM column"""
        try:
            if acm.FAdditionalInfoSpec['regRptDeferToTime'] and acm.FAdditionalInfoSpec['regRptDeferToTime'].RecType() == 'TradeRegulatoryInfo':
                if acm.FAdditionalInfoSpec['TregRptDeferToTime'] and acm.FAdditionalInfoSpec['TregRptDeferToTime'].RecType() == 'Trade':
                    self.b_parent = True
                else:
                    self.b_parent = False
            elif acm.FAdditionalInfoSpec['regRptDeferToTime'] and acm.FAdditionalInfoSpec['regRptDeferToTime'].RecType() == 'Trade':
                self.b_parent = True
        except:#it one tries to run this on 16.2 or below, exception will occur as the Regulatory classes are not available on these versions
            pass

    def ShortSellIndicator(self, acm_object):
        short_sell_indicator = None
        acm_object_add_info_on = None
        try:
            short_sell_indicator = acm_object.AdditionalInfo().RegShortSell()
            acm_object_add_info_on = acm_object
        except:
            pass
        if not short_sell_indicator:
            try:
                short_sell_indicator = acm_object.RegulatoryInfo().AdditionalInfo().RegShortSell()
                acm_object_add_info_on = acm_object.RegulatoryInfo()
            except:
                pass
        if short_sell_indicator and self.integration_utils.get_acm_version_override() >= 2017.2:
            businessEvent = acm.FBusinessEvent()
            event = short_sell_indicator.strip()
            businessEvent = acm_object.CreateShortSecurityBusinessEvent(event)
            businessEvent.Commit()
            short_sell_indicator = short_sell_lookup[short_sell_indicator]
            if acm_object.BusinessEventTradeLinks() and acm_object.BusinessEventTradeLinks()[0].BusinessEvent():
                if acm_object.BusinessEventTradeLinks()[0].BusinessEvent().EventType() == short_sell_indicator:
                    self.delete_addinfo('regShortSell', acm_object_add_info_on)
            else:
                print "There is a mismatch while migrating the ShortSellIndicator. Hence, AddInfo RegShortSell is not being deleted for trade <%d>"%acm_object.Oid()

    def OurTrader(self, add_info_val, reg_info):
        """link the trader on the trade to the Person linked to the contact in OurTrader"""
        parent_party = None
        if self.b_parent:
            try:
                parent_party = self.acm_object.AdditionalInfo().RegOurOrg()
            except:
                pass
        if not parent_party:
            parent_party = reg_info.OurOrganisation()
            if (not parent_party) and self.acm_object_reg_info.AdditionalInfo().RegOurOrg():
                parent_party = self.acm_object_reg_info.AdditionalInfo().RegOurOrg()
        contact_obj = self.get_contact(parent_party, add_info_val)
        if not contact_obj:
            contact_obj = self.get_contact(reg_info.OurOrg(), add_info_val)
        if contact_obj.Person():
            user = self.acm_object.Trader()
            if user.Person():
                if user.Person() != contact_obj.Person():
                    FRegulatoryLogger.WARN(logger, "The OurTrader <%s> on Trade <%d> is linked to Person with NationalId <%s>. However, the trader <%s> is linked to Person with NationalId <%s>. Hence, the OurTrader details cannot be upgraded for trade"%(\
                        add_info_val, self.acm_object.Oid(), contact_obj.Person().NationalId(), user.Name(), user.Person().NationalId()))
            else:
                user.Person(contact_obj.Person())
                user.Commit()
        else:
            FRegulatoryLogger.WARN(logger, "The OurTrader <%s> on Trade <%d> is not linked to a Person. Hence, the OurTrader details cannot be upgraded to the Trader of the trade"%(add_info_val, self.acm_object.Oid()))
        return reg_info

    def TradingCapacity(self, add_info_val, reg_info):
        """tradingCapacity is set from a ChoiceList, however, within core it is set with an Enum value"""
        trading_capacity = acm.EnumFromString('TradingCapacityEnum', str(add_info_val))
        reg_info.TradingCapacity(trading_capacity)
        return reg_info
    
    def OurInvestmentDecider(self, add_info_val, reg_info):
        """save the contact object in the OurInvestmentDecider AddInfo to the RegulatoryInfo table"""
        parent_party = None
        if self.b_parent:
            parent_party = self.acm_object.AdditionalInfo().RegOurOrg()
        else:
            parent_party = reg_info.OurOrganisation()
            if (not parent_party) and self.acm_object_reg_info.AdditionalInfo().RegOurOrg():
                parent_party = self.acm_object_reg_info.AdditionalInfo().RegOurOrg()
        contact_obj = self.get_contact(parent_party, add_info_val)
        if not contact_obj:
            contact_obj = self.get_contact(reg_info.OurOrg(), add_info_val)
        FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo OurInvestmentDecider with value <%s> on <%s> of id/name <%s>"%(contact_obj.Fullname(), reg_info.Trade().Oid()))    
        reg_info.OurInvestmentDecider(contact_obj)
        return reg_info

    def TheirInvestmentDecider(self, add_info_val, reg_info):
        """save the contact object in the TheirInvestmentDecider AddInfo to the RegulatoryInfo table"""
        parent_party = None
        if self.b_parent:
            parent_party = self.acm_object.AdditionalInfo().RegTheirOrg()
        else:
            parent_party = reg_info.TheirOrganisation()
            if (not parent_party) and self.acm_object_reg_info.AdditionalInfo().RegTheirOrg():
                parent_party = self.acm_object_reg_info.AdditionalInfo().RegTheirOrg()
        contact_obj = self.get_contact(parent_party, add_info_val)
        if not contact_obj:
            contact_obj = self.get_contact(reg_info.TheirOrg(), add_info_val)
        FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo TheirInvestmentDecider with value <%s> on <%s> of id/name <%s>"%(contact_obj.Fullname(), reg_info.Trade().Oid()))    
        reg_info.TheirInvestmentDecider(contact_obj)
        return reg_info

    def TheirTrader(self, add_info_val, reg_info):
        """save the contact object in the TheirTrader AddInfo to the RegulatoryInfo table"""
        parent_party = None
        if self.b_parent:
            parent_party = self.acm_object.AdditionalInfo().RegTheirOrg()
        else:
            parent_party = reg_info.TheirOrganisation()
            if (not parent_party) and self.acm_object_reg_info.AdditionalInfo().RegTheirOrg():
                parent_party = self.acm_object_reg_info.AdditionalInfo().RegTheirOrg()
        contact_obj = self.get_contact(parent_party, add_info_val)
        if not contact_obj:
            contact_obj = self.get_contact(reg_info.TheirOrg(), add_info_val)
        FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo TheirTrader with value <%s> on <%s> of id/name <%s>"%(contact_obj.Fullname(), reg_info.Trade().Oid()))    
        reg_info.TheirTrader(contact_obj)
        return reg_info

class FInstrumentRegulatoryInfoUpgrade(FRegulatoryInfoUpgrade):
    def __init__(self):
        """class that handles the upgrade of all Regulatory data on the Instrument class object to its RegulatoryInfo object"""
        FRegulatoryInfoUpgrade.__init__(self)

    def is_on_parent(self):
        """returns whether the data is being upgraded from parent Instrument to RegulatoryInfo or child RegulatoryInfo's AddInfos to ADM column"""
        try:
            if acm.FAdditionalInfoSpec['regAvgDailyTO'] and acm.FAdditionalInfoSpec['regAvgDailyTO'].RecType() == 'InstrRegulatoryInfo':
                if acm.FAdditionalInfoSpec['TregAvgDailyTO'] and acm.FAdditionalInfoSpec['TregAvgDailyTO'].RecType() == 'Instrument':
                    self.b_parent = True
                else:
                    self.b_parent = False
            elif acm.FAdditionalInfoSpec['regAvgDailyTO'] and acm.FAdditionalInfoSpec['regAvgDailyTO'].RecType() == 'Instrument':
                self.b_parent = True
        except:#it one tries to run this on 16.2 or below, exception will occur as the Regulatory classes are not available on these versions
                pass

    def set_object_type_id(self):
        """set the object type to be the parent/child on the basis of the version that the script is being executed upon for upgrade"""
        try:
            if self.acm_object.IsKindOf(acm.FInstrument) or self.acm_object_reg_info.IsKindOf(acm.FInstrumentRegulatoryInfo):
                self.object_type = 'Instrument'
                self.object_id = str(self.acm_object.Name())
        except Exception, e:
            print "Error while attempting to get the object type that the upgrade script is being executed upon"

    def CommodityProduct(self, add_info_val, reg_info):
        """upgrade the commodity classification from AddInfo onto the RegulatoryInfo field"""
        acm_object_type = None
        acm_object_id = None
        if self.b_parent:
            acm_object_type = self.object_type
            acm_object_id = self.object_id
        else:
            acm_object_type = 'InstrumentRegulatoryInfo'
            acm_object_id = self.acm_object_reg_info.Oid()
        commodity_product = acm.FChoiceList[add_info_val]
        if commodity_product:
            try:
                reg_info.CommodityProduct(commodity_product)
                FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo CommodityProduct with value <%s> on <%s> of id/name <%s>"%(commodity_product.Name(), acm_object_type, acm_object_id))
            except:
                reg_info.CommodityFurtherSubProduct(commodity_product)
                FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo CommodityProduct with value <%s> on <%s> of id/name <%s>"%(commodity_product.Name(), acm_object_type, acm_object_id))
        else:
            FRegulatoryLogger.WARN(logger, "Failed to set RegulatoryInfo CommodityProduct with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        return reg_info
        
    def TransactionType(self, add_info_val, reg_info):
        """upgrade the TransactionType from AddInfo onto the RegulatoryInfo field"""
        acm_object_type = None
        acm_object_id = None
        if self.b_parent:
            acm_object_type = self.object_type
            acm_object_id = self.object_id
        else:
            acm_object_type = 'InstrumentRegulatoryInfo'
            acm_object_id = self.acm_object_reg_info.Oid()
        transaction_type = acm.FChoiceList.Select01("name = '%s' and list = 'TransactionType'"%add_info_val, None)
        if transaction_type:
            reg_info.TransactionType(transaction_type)
            FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo TransactionType with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        else:
            FRegulatoryLogger.WARN(logger, "Failed to set RegulatoryInfo TransactionType with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        return reg_info

    def FinalPriceType(self, add_info_val, reg_info):
        """upgrade the FinalPriceType from AddInfo onto the RegulatoryInfo field"""
        acm_object_type = None
        acm_object_id = None
        if self.b_parent:
            acm_object_type = self.object_type
            acm_object_id = self.object_id
        else:
            acm_object_type = 'InstrumentRegulatoryInfo'
            acm_object_id = self.acm_object_reg_info.Oid()
        final_price_type = acm.FChoiceList.Select01("name = '%s' and list = 'FinalPriceType'"%add_info_val, None)
        if final_price_type:
            reg_info.FinalPriceType(final_price_type)
            FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo FinalPriceType with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        else:
            FRegulatoryLogger.WARN(logger, "Failed to set RegulatoryInfo FinalPriceType with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        return reg_info

    def DarkCapStatus(self, add_info_val, reg_info):
        """upgrade the DarkCapStatus from AddInfo onto the RegulatoryInfo field"""
        acm_object_type = None
        acm_object_id = None
        if self.b_parent:
            acm_object_type = self.object_type
            acm_object_id = self.object_id
        else:
            acm_object_type = 'InstrumentRegulatoryInfo'
            acm_object_id = self.acm_object_reg_info.Oid()
        dark_cap_status = acm.FChoiceList.Select01("name = '%s' and list = 'DarkCapStatus'"%add_info_val, None)
        if dark_cap_status:
            reg_info.DarkCapStatus(dark_cap_status)
            FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo DarkCapStatus with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        else:
            FRegulatoryLogger.WARN(logger, "Failed to set RegulatoryInfo DarkCapStatus with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        return reg_info

    def DoubleVolumeCapStatus(self, add_info_val, reg_info):
        """upgrade the DoubleVolumeCapStatus from AddInfo onto the RegulatoryInfo field"""
        acm_object_type = None
        acm_object_id = None
        if self.b_parent:
            acm_object_type = self.object_type
            acm_object_id = self.object_id
        else:
            acm_object_type = 'InstrumentRegulatoryInfo'
            acm_object_id = self.acm_object_reg_info.Oid()
        dbl_vol_cap_status = acm.FChoiceList.Select01("name = '%s' and list = 'DoubleVolumeCapStatus'"%add_info_val, None)
        if dbl_vol_cap_status:
            reg_info.DoubleVolumeCapStatus(dbl_vol_cap_status)
            FRegulatoryLogger.DEBUG(logger, "Setting RegulatoryInfo DoubleVolumeCapStatus with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        else:
            FRegulatoryLogger.WARN(logger, "Failed to set RegulatoryInfo DoubleVolumeCapStatus with value <%s> on <%s> of id/name <%s>"%(add_info_val, acm_object_type, acm_object_id))
        return reg_info

    
            
class FContactRegulatoryInfoUpgrade(FRegulatoryInfoUpgrade):
    def __init__(self):
        """class that handles the upgrade of all Regulatory data on the contact into Person class"""
        FRegulatoryInfoUpgrade.__init__(self)

    def delete_contact_reg_info(self, contact):
        """delete the AddInfo values on the contact object once the upgrade of its data is completed onto the Person object"""
        add_info_specs = ['dateOfBirth', 'firstName', 'lastName', 'nationalId', 'regContactCrmId', 'regContExchangeId']
        if self.integration_utils.get_acm_version_override() >= 2017.2 :
            add_info_specs.append('uniqueName')
        for add_info_spec in add_info_specs:
            FRegulatoryLogger.DEBUG(logger, "Deleting addInfo <%s> on Contact <%s> on Party <%s>."%(add_info_spec, contact.Fullname(), contact.Party().Name()))
            self.delete_addinfo(add_info_spec, contact)

    def delete_contact_add_info_specs(self):
        """delete the AddInfoSpecs on the contact table once the upgrade of all this data is completed onto the Person table"""
        add_info_specs = ['dateOfBirth', 'firstName', 'lastName', 'nationalId', 'regContactCrmId', 'regContExchangeId']
        if self.integration_utils.get_acm_version_override() >= 2017.2 :
            add_info_specs.append('uniqueName')
        for add_info_spec in list(add_info_specs):
            addInf = acm.FAdditionalInfoSpec[add_info_spec]
            if addInf:
                add_infos = acm.FAdditionalInfo.Select("addInf = %d"%addInf.Oid())
                if not add_infos:
                    FRegulatoryLogger.DEBUG(logger, "Deleting AddInfoSpec <%s> on Contact"%add_info_spec)
                    addInf.Delete()
                else:
                    FRegulatoryLogger.WARN(logger, "Cannot delete AddInfoSpec <%s> on Contact as reference to this AddInfoSpec still exist."%add_info_spec)

    def upgrade_unique_name(self, contact):
        """upgrade the AddInfo UniqueName details onto the column UniqueName on Contact table"""
        try:
            if self.integration_utils.get_acm_version_override() >= 2017.2 and contact.AdditionalInfo().UniqueName():
                contact.UniqueName(contact.AdditionalInfo().UniqueName())
                contact.Commit()
                FRegulatoryLogger.DEBUG(logger, "UniqueName on Contact <%s> with Oid <%d> on Party <%s> being set to <%s>"%(contact.Fullname(), contact.Oid(), contact.Party().Name(), contact.AdditionalInfo().UniqueName()))
        except:#exception hit once the uniqueName AddInfo has been removed post upgrade
            pass
            
    def link_contact_to_person(self, contact):
        """link the contact to a person. If Person doesnt exist in ADS, then create it with the ContactRegulatoryInfo details and link it to the Contact"""
        try:
            national_id = contact.RegulatoryInfo().NationalId()
            if contact.Person() and national_id:
                if contact.Person().NationalId() != national_id:
                    print "The contact <%s> with Oid <%d> on Party <%s> with NationalId <%s> is already linked to a Person with NationalId <%s>. Please check the linking."%(\
                    contact.Fullname(), contact.Oid(), contact.Party().Name(), national_id, contact.Person().NationalId())#tested
            elif national_id:
                person = acm.FPerson.Select01("nationalId = '%s'"%national_id, None)
                person_id = None
                if not person:
                    person = acm.FPerson()
                    person.FirstName(contact.RegulatoryInfo().FirstName())
                    person.LastName(contact.RegulatoryInfo().LastName())
                    person.DateOfBirth(contact.RegulatoryInfo().DateOfBirth())
                    person.CrmId(contact.RegulatoryInfo().CrmId())
                    person.ExchangeId(contact.RegulatoryInfo().ExchangeId())
                    person.NationalId(contact.RegulatoryInfo().NationalId())
                    person.Commit()
                    FRegulatoryLogger.INFO(logger, "Creating Person with NationalId <%s> and linking it to Contact  <%s> with Oid <%d> on Party <%s>"%(national_id, contact.Fullname(), contact.Oid(), contact.Party().Name()))#tested
                    person_id = person.Oid()
                if person:
                    person_id = person.Oid()
                if person_id:
                    FRegulatoryLogger.INFO(logger, "Linking contact <%s> with Oid <%d> on Party <%s> with NationalId <%s> to Person with Oid <%d>."%(contact.Fullname(), contact.Oid(), contact.Party().Name(), national_id, person_id))#tested
                    contact.Person(person)
                    contact.Commit()
            elif not contact.Person():
                FRegulatoryLogger.WARN(logger, "The NationalId details for contact <%s> with Oid <%d> on Party <%s> is not available. Hence, cannot link it to a Person object."%(contact.Fullname(), contact.Oid(), contact.Party().Name()))#tested
        except Exception, e:
            pass

    def verify_linked_contact_to_person(self, contact):
        """verify that the contact is linked to a person with the same NationalId"""
        b_mismatch = True
        try:
            if contact.Person():
                if contact.Person().NationalId():
                    if contact.RegulatoryInfo().NationalId():
                        if contact.RegulatoryInfo().NationalId() == contact.Person().NationalId():
                            if (contact.RegulatoryInfo().DateOfBirth() and contact.RegulatoryInfo().DateOfBirth() != contact.Person().DateOfBirth()) or \
                               (contact.RegulatoryInfo().FirstName() and contact.RegulatoryInfo().FirstName() != contact.Person().FirstName()) or \
                               (contact.RegulatoryInfo().LastName() and contact.RegulatoryInfo().LastName() != contact.Person().LastName()) or \
                               (contact.RegulatoryInfo().CrmId() and contact.RegulatoryInfo().CrmId() != contact.Person().CrmId()) or \
                               (contact.RegulatoryInfo().ExchangeId() and contact.RegulatoryInfo().ExchangeId() != contact.Person().ExchangeId()):
                                FRegulatoryLogger.WARN(logger, "Mismatch in Regulatory details on Contact <%s> with Oid <%s> on Party <%s> and linked Person with Oid <%d>"%(\
                                contact.Fullname(), contact.Oid(), contact.Party().Name(), contact.Person().Oid()))
                            else:
                                b_mismatch = False
                        else:
                            FRegulatoryLogger.WARN(logger, "The NationalId on Contact <%s> with Oid <%s> on Party <%s> is set to <%s>. However, it is linked to a Person with NationalId <%s>."%(\
                            contact.Fullname(), contact.Oid(), contact.Party().Name(), contact.RegulatoryInfo().NationalId(), contact.Person().NationalId()))
                    else:
                        b_mismatch = False
                else:
                    FRegulatoryLogger.WARN(logger, "Contact <%s> with Oid <%s> on Party <%s> is linked to a Person with no NationalId set on it."%(contact.Fullname(), contact.Oid(), contact.Party().Name()))
            else:
                FRegulatoryLogger.WARN(logger, "Contact <%s> with Oid <%s> on Party <%s> is not linked to Person."%(contact.Fullname(), contact.Oid(), contact.Party().Name()))
            if self.integration_utils.get_acm_version_override() >= 2017.2 and contact.AdditionalInfo().UniqueName() and contact.AdditionalInfo().UniqueName() != contact.UniqueName():
                b_mismatch = True
        except Exception, e:
            pass
        return b_mismatch

    def migrate_leg_isin_details(self):
        fxswap_near_far_dict = {}
        add_info_spec = acm.FAdditionalInfoSpec['regLegIsin']
        add_infos = acm.FAdditionalInfo.Select('addInf=%d' % (add_info_spec.Oid()))
        for add_info in add_infos:
            if add_info.Parent():
                trade = None
                try:
                    if add_info.Parent().IsKindOf(acm.FTradeRegulatoryInfo()):
                        trade = add_info.Parent().Trade()
                    else:
                        trade = add_info.Parent()
                except:
                    trade = add_info.Parent()
                if trade.FxSwapFarLeg():#it means this is the near leg
                    fxswap_near_far_dict[trade] = trade.FxSwapFarLeg()
                elif trade.FxSwapNearLeg():
                    fxswap_near_far_dict[trade.FxSwapNearLeg()] = trade
        for each_trade in fxswap_near_far_dict:
            near_leg_trade = each_trade
            far_leg_trade = fxswap_near_far_dict[each_trade]
            near_leg_isin = None
            far_leg_isin = None
            try:
                near_leg_isin = near_leg_trade.RegulatoryInfo().AdditionalInfo().RegLegIsin()
            except:
                near_leg_isin = near_leg_trade.AdditionalInfo().RegLegIsin()
            try:
                far_leg_isin = far_leg_trade.RegulatoryInfo().AdditionalInfo().RegLegIsin()
            except:
                far_leg_isin = far_leg_trade.AdditionalInfo().RegLegIsin()
            try:
                near_leg_reg = near_leg_trade.RegulatoryInfo()
                near_leg_reg.NearLegIsin(near_leg_isin)
                near_leg_reg.FarLegIsin(far_leg_isin)
                far_leg_reg = far_leg_trade.RegulatoryInfo()
                far_leg_reg.NearLegIsin(near_leg_isin)
                far_leg_reg.FarLegIsin(far_leg_isin)
                near_leg_reg.Commit()
                far_leg_reg.Commit()
                near_aiSel = None
                far_aiSel = None
                try:
                    near_aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (acm.FAdditionalInfoSpec['regLegIsin'].Oid(), near_leg_trade.RegulatoryInfos()[0].Oid()))
                except:
                    near_aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (acm.FAdditionalInfoSpec['regLegIsin'].Oid(), near_leg_trade.Oid()))
                try:
                    far_aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (acm.FAdditionalInfoSpec['regLegIsin'].Oid(), far_leg_reg.RegulatoryInfos()[0].Oid()))
                except:
                    far_aiSel = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d ' % (acm.FAdditionalInfoSpec['regLegIsin'].Oid(), far_leg_reg.Oid()))
                if near_aiSel and str(near_aiSel[0]) != 'None':
                    self.integration_utils.update_addtional_info(near_aiSel[0])
                if far_aiSel and str(far_aiSel[0]) != 'None':
                    self.integration_utils.update_addtional_info(far_aiSel[0])
            except Exception, e:
                print str(e)
            

acm_version = FIntegrationUtils.FIntegrationUtils().get_acm_version_override()
if acm_version > 2017.2:
    acm_version = 2017.2
elif acm_version < 2016.4:
    acm_version = 2016.4
acm_version_val = str(acm_version).replace('.', '_')

def get_reg_info_dict(object_type):
    add_info_dict = eval(object_type + '_add_info_dict_' + acm_version_val)
    return add_info_dict

def get_rename_reg_info_dict(object_type, orig_add_info_dict):
    add_info_list = eval(object_type + '_version_list')
    add_info_list = add_info_list[add_info_list.index(acm_version_val) + 1:]
    rename_add_info_dict = orig_add_info_dict
    for each_version in add_info_list:
        add_info_dict = eval(object_type + '_add_info_dict_' + each_version + '_upgrade')
        rename_add_info_dict = dict(add_info_dict, **rename_add_info_dict)
    return rename_add_info_dict

def upgrade_trade_reg_info():
    """upgrade all the Trade Regulatory attributes into their corresponding ADM columns"""
    trd_counter = 0
    trades = acm.FTrade.Select('')
    total_trd_counter = len(trades)
    add_info_dict = get_reg_info_dict('trade')
    for trade in trades:
        trd_counter = trd_counter + 1
        upgrade_obj = FTradeRegulatoryInfoUpgrade()
        upgrade_obj.is_on_parent()
        upgrade_obj.set_lookup_dict(add_info_dict)
        for add_info in add_info_dict.keys():
            upgrade_obj.upgrade_reg_info(add_info, trade)
        upgrade_obj.ShortSellIndicator(trade)
        upgrade_obj.delete_parent_add_info()
        global trade_add_info_dict
        trade_add_info_dict = get_rename_reg_info_dict('trade', trade_add_info_dict)
        upgrade_obj.set_lookup_dict(trade_add_info_dict)
        orig_add_info_spec_found = upgrade_obj.rename_parent_add_info()
        if orig_add_info_spec_found:
            return
        else:
            upgrade_obj.set_lookup_dict(trade_add_info_dict)
            for add_info in trade_add_info_dict.keys():
                upgrade_obj.upgrade_reg_info(add_info, trade, True)
            upgrade_obj.ShortSellIndicator(trade)
            upgrade_obj.delete_parent_add_info(True)
        if trd_counter % 1000 == 0:
            FRegulatoryLogger.WARN(logger, "Processing complete for: <%d> trades. Processing in progrees for: <%d> trades"%(trd_counter, total_trd_counter - trd_counter))
    
    add_info_del_dict = upgrade_obj.get_renamed_add_infos_list()
    add_info_del_dict = dict(add_info_del_dict, **add_info_dict)
    upgrade_obj.set_lookup_dict(add_info_del_dict)
    upgrade_obj.delete_add_info_specs()

def upgrade_ins_reg_info():
    """upgrade all the Instrument Regulatory attributes into their corresponding ADM columns"""
    add_info_dict = get_reg_info_dict('instrument')
    ins_counter = 0
    instruments = acm.FInstrument.Select('')
    total_ins_counter = len(instruments)
    for instrument in instruments:
        ins_counter = ins_counter + 1
        upgrade_obj = FInstrumentRegulatoryInfoUpgrade()
        upgrade_obj.is_on_parent()
        upgrade_obj.set_lookup_dict(add_info_dict)
        for add_info in add_info_dict.keys():
            upgrade_obj.upgrade_reg_info(add_info, instrument)
        upgrade_obj.delete_parent_add_info()
        global instrument_add_info_dict
        instrument_add_info_dict = get_rename_reg_info_dict('instrument', instrument_add_info_dict)
        upgrade_obj.set_lookup_dict(instrument_add_info_dict)
        orig_add_info_spec_found = upgrade_obj.rename_parent_add_info()
        if orig_add_info_spec_found:
            return
        else:
            upgrade_obj.set_lookup_dict(instrument_add_info_dict)
            for add_info in instrument_add_info_dict.keys():
                upgrade_obj.upgrade_reg_info(add_info, instrument, True)
            upgrade_obj.delete_parent_add_info(True)
        
        FRegulatoryLogger.INFO(logger, "Processing completed for instrument <%s>"%instrument.Name())
        if ins_counter % 1000 == 0:
            FRegulatoryLogger.INFO(logger, "Processing complete for: <%d> instruments. Processing in progress for: <%d> instruments"%(ins_counter, total_ins_counter - ins_counter))
    
    add_info_del_dict = upgrade_obj.get_renamed_add_infos_list()
    add_info_del_dict = dict(add_info_del_dict, **add_info_dict)
    upgrade_obj.set_lookup_dict(add_info_del_dict)
    upgrade_obj.delete_add_info_specs()

def upgrade_contact_reg_info():
    """this API creates Person object for each contact that has the NationalId details in the ADS"""
    try:
        upgrade_obj = FContactRegulatoryInfoUpgrade()
        for contact in acm.FContact.Select(''):
            upgrade_obj.link_contact_to_person(contact)
            upgrade_obj.upgrade_unique_name(contact)
            b_mismatch = upgrade_obj.verify_linked_contact_to_person(contact)
            if not b_mismatch:
                upgrade_obj.delete_contact_reg_info(contact)
        upgrade_obj.delete_contact_add_info_specs()
    except Exception, e:
        print str(e)

def clean_up_obsolete_data():
    upgrade_obj = FRegulatoryInfoUpgrade()
    upgrade_obj.delete_obsolete_add_info_specs()

def upgrade_regulatory_info():
    upgrade_contact_reg_info()
    upgrade_ins_reg_info()
    upgrade_trade_reg_info()
    clean_up_obsolete_data()
    print "Upgrade Complete!"
