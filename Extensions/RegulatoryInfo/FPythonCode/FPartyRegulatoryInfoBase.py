""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FPartyRegulatoryInfoBase.py"
"""------------------------------------------------------------------------
MODULE
    FPartyRegulatoryInfoBase -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Party which has all the RegulatoryInfo related methods
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported.
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import string
import acm
import FRegulatoryLogger
import FIntegrationUtils
import FRegulatoryUtils
import FRegulatoryInfoException
VALUE_NOT_SET = ()
logger = 'FPartyRegulatoryInfoBase'
class FPartyRegulatoryInfoBase(object):
    def __init__(self, party = None):
        """class that maintains all data related to the regulatory on the FParty"""
        if party:
            self.__party = party
            self.__reg_is_investment_firm = None
            self.__reg_possible_reporter = None
            self.__reg_financial_category = None
            self.__mic = None
            self.__mic_alias = None
            self.__reg_is_algorithm = None
            self.__reg_exchange_id = None
            self.__reg_crm_id = None
            self.__mifid_category = None
            self.__client_type = None
            self.__is_venue = None
            self.__integration_utils = FIntegrationUtils.FIntegrationUtils()
            self.__refresh()
        else:
            FRegulatoryLogger.ERROR(logger, "Please provide a valid party")
            return None

    def __refresh(self):
        self.__reg_is_investment_firm = FRegulatoryUtils.get_addinfo_value('regIsInvestmentFirm', self.__party)
        self.__reg_possible_reporter = FRegulatoryUtils.get_addinfo_value('regPossibleReporter', self.__party)
        self.__reg_financial_category = FRegulatoryUtils.get_addinfo_value('regFinancialCategor', self.__party)
        self.__reg_is_algorithm = FRegulatoryUtils.get_addinfo_value('regIsAlgorithm', self.__party)
        self.__mifid_category = FRegulatoryUtils.get_addinfo_value('regMifidCategory', self.__party)
        self.__reg_crm_id = FRegulatoryUtils.get_addinfo_value('regPtyCrmId', self.__party)
        self.__reg_exchange_id = FRegulatoryUtils.get_addinfo_value('regPtyExchangeId', self.__party)
        for alias in self.__party.Aliases():
            if alias.Type().Name() == 'MIC' and alias.Oid() > 0:
                self.__mic = alias.Name()
                self.__mic_alias = alias
                break
        if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.4:
            if self.__party.Type() == 'Venue':
                self.__is_venue = True
            else:
                self.__is_venue = False
        else:
            self.__is_venue = FRegulatoryUtils.get_addinfo_value('regIsVenue', self.__party)

    def Party(self):
        """returns the party for which this wrapper has all the addinfo/column values"""
        return self.__party

    def IsVenue(self, reg_is_venue = VALUE_NOT_SET):
        """Indicates whether the party is a trading venue or not"""
        if reg_is_venue != VALUE_NOT_SET:
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.4:
                FRegulatoryLogger.DEBUG(logger, "The IsVenue attribute cannot be set for version <%s>"%str(FIntegrationUtils.FIntegrationUtils.get_acm_version_override()))
            else:
                reg_is_venue_val = None
                if str(reg_is_venue) not in ['None', '']:
                    reg_is_venue_val = FRegulatoryUtils.validate_bool(reg_is_venue, 'IsVenue')
                    FRegulatoryLogger.DEBUG(logger, "The IsVenue is being set to <%d>."%(reg_is_venue_val))
                    self.__is_venue = reg_is_venue_val
                try:
                    self.__party.AdditionalInfo().RegIsVenue(self.__is_venue)
                except:
                    pass
        else:
            if str(self.__is_venue) == "None":
                FRegulatoryLogger.DEBUG(logger, "The IsVenue is None. Hence defaulting it to False")
                self.__is_venue = False
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.4:
                if self.__party.Type() == 'Venue':
                    self.__is_venue = True
                else:
                    self.__is_venue = False
            return self.__is_venue

    def IsInvestmentFirm(self, reg_investment_firm = VALUE_NOT_SET):
        """Whether the given entity is an investment firm covered by Directive 2004/39/EC or Directive 2014/65/EU (Tag 5)"""
        if reg_investment_firm != VALUE_NOT_SET:
            reg_investment_firm_val = None
            if str(reg_investment_firm) not in ['None', '']:
                reg_investment_firm_val = FRegulatoryUtils.validate_bool(reg_investment_firm, 'IsInvestmentFirm')
                FRegulatoryLogger.DEBUG(logger, "The IsInvestmentFirm is being set to <%d>."%(reg_investment_firm_val))
            self.__reg_is_investment_firm = reg_investment_firm_val
            try:
                self.__party.AdditionalInfo().RegIsInvestmentFirm(self.__reg_is_investment_firm)
            except:
                pass
        else:
            if str(self.__reg_is_investment_firm) == "None":
                FRegulatoryLogger.DEBUG(logger, "The IsInvestmentFirm is None. Hence defaulting it to False")
                self.__reg_is_investment_firm = False
            return self.__reg_is_investment_firm

    def PossibleReporter(self, reg_possible_reporter = VALUE_NOT_SET):
        """Legal Entity Identifier (LEI) of the entity submitting the transaction report to the competent authority in accordance with Article 26(7) of Regulation (EU) 600/2014. (Tag 6)"""
        if reg_possible_reporter != VALUE_NOT_SET:
            reg_possible_reporter_bool = None
            if str(reg_possible_reporter) not in ['None', '']:
                reg_possible_reporter_bool = FRegulatoryUtils.validate_bool(reg_possible_reporter, 'PossibleReporter')
                FRegulatoryLogger.DEBUG(logger, "The PossibleReporter is being set to <%d>."%(reg_possible_reporter_bool))
            self.__reg_possible_reporter = reg_possible_reporter_bool
            try:
                self.__party.AdditionalInfo().RegPossibleReporter(self.__reg_possible_reporter)
            except:
                pass
        else:
            return self.__reg_possible_reporter

    def FinancialCategory(self, reg_financial_category = VALUE_NOT_SET):
        """Categorization of counterparty into Financial Counterparty, Non-Financial Counterparty and a plus or minus to denote level of notional turnover. """
        if reg_financial_category != VALUE_NOT_SET:
            if self.__integration_utils.is_valid_choice_list_val('FinancialCategory', reg_financial_category) or reg_financial_category == '' or reg_financial_category == None:
                self.__reg_financial_category = reg_financial_category
            else:
                msg = "The value <%s> is not a valid entry in <FinancialCategory> ChoiceList. Hence not setting the FinancialCategory on Party <%s>"%(reg_financial_category, self.__party.Name())
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            try:
                self.__party.AdditionalInfo().RegFinancialCategor(self.__reg_financial_category)
            except:
                pass
        else:
            return self.__reg_financial_category

    def MIC(self, mic_val = VALUE_NOT_SET):
        """return the MIC on the party"""
        if mic_val != VALUE_NOT_SET:
            if str(mic_val) in ['', 'None']:
                mic_val = None
            self.__mic = mic_val
        else:
            return self.__mic

    def IsAlgorithm(self, is_algorithm = VALUE_NOT_SET):
        """identifier of whether the party is executing as an algorithm"""
        if is_algorithm != VALUE_NOT_SET:
            reg_is_algorithm = None
            if str(is_algorithm) not in ['None', '']:
                reg_is_algorithm = FRegulatoryUtils.validate_bool(is_algorithm, 'IsAlgorithm')
                FRegulatoryLogger.DEBUG(logger, "The IsAlgorithm is being set to <%d>."%(reg_is_algorithm))
            if self.__party.Type() != 'Counterparty':
                msg = "The IsAlgorithm field can be set only on party of Type Counterparty. However, it is being set on party of Type <%s>"%self.__party.Type()
                FRegulatoryLogger.WARN(logger, msg)
            self.__reg_is_algorithm = reg_is_algorithm
            try:
                self.__party.AdditionalInfo().RegIsAlgorithm(self.__reg_is_algorithm)
            except:
                pass
        else:
            if str(self.__reg_is_algorithm) == "None":
                FRegulatoryLogger.DEBUG(logger, "The IsAlgorithm is None. Hence defaulting it to False")
                self.__reg_is_algorithm = False
            return self.__reg_is_algorithm

    def ExchangeId(self, reg_exchange_id = VALUE_NOT_SET):
        """The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged."""
        if reg_exchange_id != VALUE_NOT_SET:
            if str(reg_exchange_id).isdigit():
                self.__reg_exchange_id = int(reg_exchange_id)
            elif str(reg_exchange_id) in ['None', '']:
                self.__reg_exchange_id = None
            else:
                msg = "The ExchangeId provided <%s> is not of the expected integer format"%str(reg_exchange_id)
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            try:
                self.__party.AdditionalInfo().RegPtyExchangeId(self.__reg_exchange_id)
            except:
                pass
        else:
            if not self.__reg_exchange_id:
                self.__reg_exchange_id = None
            return self.__reg_exchange_id

    def CrmId(self, crm_id = VALUE_NOT_SET):
        """CrmId of the concerned natural person"""
        if crm_id != VALUE_NOT_SET:
            self.__reg_crm_id = crm_id
            try:
                self.__party.AdditionalInfo().RegPtyCrmId(self.__reg_crm_id)
            except:
                pass
        else:
            if not self.__reg_crm_id:
                self.__reg_crm_id = None
            return self.__reg_crm_id

    def MiFIDCategory(self, mifid_category = VALUE_NOT_SET):
        """Category - whether it is Retail/Professional or Eligible"""
        if mifid_category != VALUE_NOT_SET:
            if self.__integration_utils.is_valid_choice_list_val('MiFIDCategory', mifid_category) or mifid_category == '' or mifid_category == None:
                self.__mifid_category = mifid_category
            else:
                msg = "The value <%s> is not a valid entry in <MiFIDCategory> ChoiceList. Hence not setting the MiFIDCategory on Party <%s>"%(mifid_category, self.__party.Name())
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            try:
                self.__party.AdditionalInfo().RegMifidCategory(self.__mifid_category)
            except:
                pass
        else:
            return self.__mifid_category

    def ClientType(self):
        """returns the ClientType based on where the CrmId is found on the linked objects"""
        self.__client_type = FRegulatoryUtils.getClientType(self.__party)
        return self.__client_type

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super(FPartyRegulatoryInfoBase, self).__setattr__(attr, val)
        else:
            if hasattr(self, attr):
                getattr(self, attr)(val)

    def Commit(self):
        try:
            acm.BeginTransaction()
            if self.__mic_alias and (not self.__mic):
                self.__mic_alias.Delete()
            elif self.__mic_alias and self.__mic:
                self.__mic_alias.Name(self.__mic)
            elif self.__mic and (not self.__mic_alias):
                alias = acm.FPartyAlias()
                alias.Alias(self.__mic)
                alias.Type(acm.FPartyAliasType['MIC'])
                self.__party.Aliases().Add(alias)
            self.__party.Commit()
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() < 2015.4:
                self.__integration_utils.set_additional_info('RegIsInvestmentFirm', self.__party, self.__reg_is_investment_firm)
                self.__integration_utils.set_additional_info('RegPossibleReporter', self.__party, self.__reg_possible_reporter)
                self.__integration_utils.set_additional_info('RegFinancialCategor', self.__party, self.__reg_financial_category)
                self.__integration_utils.set_additional_info('RegIsAlgorithm', self.__party, self.__reg_is_algorithm)
                self.__integration_utils.set_additional_info('RegPtyExchangeId', self.__party, self.__reg_exchange_id)
                self.__integration_utils.set_additional_info('RegPtyCrmId', self.__party, self.__reg_crm_id)
                self.__integration_utils.set_additional_info('RegMifidCategory', self.__party, self.__mifid_category)
                self.__integration_utils.set_additional_info('RegIsVenue', self.__party, self.__is_venue)
            FRegulatoryLogger.DEBUG(logger, "Commited all AdditionalInfos on Party related to Regulatory Reporting")
            acm.CommitTransaction()
        except Exception as e:
            FRegulatoryLogger.ERROR(logger, str(e))
            FRegulatoryLogger.ERROR(logger, 'Aborting Transaction')
            acm.AbortTransaction()

    def Delete(self):
        """Deleting this instance automatically deletes all the attributes related to the reporting on the party"""
        FRegulatoryUtils.Delete(self.__party, "Party")
        FRegulatoryLogger.DEBUG(logger, "Deleted all AdditionalInfos on Party related to Regulatory Reporting")

    def Attributes(self):
        """returns the attributes on the FPartyRegulatoryInfo instance"""
        return FRegulatoryUtils.log_attributes('FPartyRegulatoryInfo', self)


def RegulatoryInfo(self):
    partyRegInfo = FPartyRegulatoryInfo(self)
    return partyRegInfo

def Select(query):
    return_result = FRegulatoryUtils.Select(query, "FParty")
    return return_result
