""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FPartyRegulatoryInfo.py"
"""------------------------------------------------------------------------
MODULE
    FPartyRegulatoryInfo -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Party which has all the RegulatoryInfo related methods
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import FRegulatoryUtils
import FPartyRegulatoryInfoBase
logger = 'FPartyRegulatoryInfo'
VALUE_NOT_SET = () 
class FPartyRegulatoryInfo(FPartyRegulatoryInfoBase.FPartyRegulatoryInfoBase):
    def __init__(self, party = None):
        """class that maintains all data related to the regulatory on the FParty"""
        FPartyRegulatoryInfoBase.FPartyRegulatoryInfoBase.__init__(self, party)
        self.__party = party

    def Party(self):
        """returns the party for which this wrapper has all the addinfo/column values"""
        return super(FPartyRegulatoryInfo, self).Party()

    def IsVenue(self, reg_is_venue = VALUE_NOT_SET):
        """Indicates whether the party is a trading venue or not"""
        return super(FPartyRegulatoryInfo, self).IsVenue(reg_is_venue)

    def IsInvestmentFirm(self, reg_investment_firm = VALUE_NOT_SET):
        """Whether the given entity is an investment firm covered by Directive 2004/39/EC or Directive 2014/65/EU (Tag 5)"""
        return super(FPartyRegulatoryInfo, self).IsInvestmentFirm(reg_investment_firm)

    def PossibleReporter(self, reg_possible_reporter = VALUE_NOT_SET):
        """Legal Entity Identifier (LEI) of the entity submitting the transaction report to the competent authority in accordance with Article 26(7) of Regulation (EU) 600/2014. (Tag 6)"""
        return super(FPartyRegulatoryInfo, self).PossibleReporter(reg_possible_reporter) 

    def FinancialCategory(self, reg_financial_category = VALUE_NOT_SET):
        """Categorization of counterparty into Financial Counterparty, Non-Financial Counterparty and a plus or minus to denote level of notional turnover. """
        return super(FPartyRegulatoryInfo, self).FinancialCategory(reg_financial_category)

    def MIC(self, mic_val = VALUE_NOT_SET):
        """return the MIC on the party"""
        return super(FPartyRegulatoryInfo, self).MIC(mic_val)

    def IsAlgorithm(self, is_algorithm = VALUE_NOT_SET):
        """identifier of whether the party is executing as an algorithm"""
        return super(FPartyRegulatoryInfo, self).IsAlgorithm(is_algorithm)

    def ExchangeId(self, reg_exchange_id = VALUE_NOT_SET):
        """The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged."""
        return super(FPartyRegulatoryInfo, self).ExchangeId(reg_exchange_id)

    def CrmId(self, crm_id = VALUE_NOT_SET):
        """CrmId of the concerned natural person"""
        return super(FPartyRegulatoryInfo, self).CrmId(crm_id)

    def MiFIDCategory(self, mifid_category = VALUE_NOT_SET):
        """Category - whether it is Retail/Professional or Eligible"""
        return super(FPartyRegulatoryInfo, self).MiFIDCategory(mifid_category)

    def ClientType(self):
        """returns the ClientType based on where the CrmId is found on the linked objects"""
        return super(FPartyRegulatoryInfo, self).ClientType()

    def __setattr__(self, attr, val):
        super(FPartyRegulatoryInfo, self).__setattr__(attr, val)

    def Commit(self):
        """Committing this instance automatically commits all the attributes related to the reporting on the instrument or on the PartyRegulatoryInfo in the ADS"""
        super(FPartyRegulatoryInfo, self).Commit()
    
    def Delete(self):
        """Deleting this instance automatically deletes all the attributes related to the reporting on the instrument or on the PartyRegulatoryInfo in the ADS"""
        super(FPartyRegulatoryInfo, self).Delete() 

  
def RegulatoryInfo(self):
    partyRegInfo = FPartyRegulatoryInfo(self)
    return partyRegInfo

def Select(query):
    return_result = FRegulatoryUtils.Select(query, "FParty")
    return return_result