""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FContactRegulatoryInfo.py"
"""------------------------------------------------------------------------
MODULE
    FContactRegulatoryInfo -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Contact which has all the RegulatoryInfo related methods
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported.
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import string
import acm
import FIntegrationUtils
import FRegulatoryLogger
import ael
import FRegulatoryUtils
import FContactRegulatoryInfoBase
logger = 'FContactRegulatoryInfo'
VALUE_NOT_SET = ()

class FContactRegulatoryInfo(FContactRegulatoryInfoBase.FContactRegulatoryInfoBase):
    def __init__(self, contact = None):
        """class that maintains all data related to the regulatory on the FContact"""
        FContactRegulatoryInfoBase.FContactRegulatoryInfoBase.__init__(self, contact)
        self.__contact = contact

    def Contact(self):
        """returns the contact for which this wrapper has all the addinfo/column values"""
        return super(FContactRegulatoryInfo, self).Contact()

    def DateOfBirth(self, reg_date_of_birth = VALUE_NOT_SET):
        """Date of birth of the concerned natural person"""
        return super(FContactRegulatoryInfo, self).DateOfBirth(reg_date_of_birth)

    def FirstName(self, reg_first_name = VALUE_NOT_SET):
        """First name of the concerned natural person"""
        return super(FContactRegulatoryInfo, self).FirstName(reg_first_name)

    def LastName(self, reg_last_name = VALUE_NOT_SET):
        """Last name of the concerned natural person"""
        return super(FContactRegulatoryInfo, self).LastName(reg_last_name)

    def NationalId(self, reg_national_id = VALUE_NOT_SET):
        """NationalId of the concerned natural person"""
        return super(FContactRegulatoryInfo, self).NationalId(reg_national_id)

    def CrmId(self, reg_crm_id = VALUE_NOT_SET):
        """CrmId of the concerned natural person"""
        return super(FContactRegulatoryInfo, self).CrmId(reg_crm_id)

    def ExchangeId(self, reg_exchange_id = VALUE_NOT_SET):
        """The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged."""
        return super(FContactRegulatoryInfo, self).ExchangeId(reg_exchange_id)

    def UniqueName(self, reg_unique_name = VALUE_NOT_SET):
        """An optional unique name, if specified there can only be one contact with this name for each party."""
        return super(FContactRegulatoryInfo, self).UniqueName(reg_unique_name)

    def ClientType(self):
        """returns the ClientType based on where the CrmId is found on the linked objects"""
        return super(FContactRegulatoryInfo, self).ClientType()

    def JointAccount(self):
        """Another trader that jointly owns the account with this trader"""
        return super(FContactRegulatoryInfo, self).JointAccount()

    def IsGeneralPartner(self, is_general_partner = VALUE_NOT_SET):
        """General partner has responsibility for the actions of the business, can legally bind the business
        and is personally liable for all the business's debts and obligations"""
        return super(FContactRegulatoryInfo, self).IsGeneralPartner(is_general_partner)

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super(FContactRegulatoryInfo, self).__setattr__(attr, val)
        else:
            if hasattr(self, attr):
                getattr(self, attr)(val)

    def Commit(self):
        """Committing this instance will automatically commit all the RegulatorySupport related attributes on the contact"""
        super(FContactRegulatoryInfo, self).Commit()

    def Delete(self):
        """Deleting this instance automatically deletes all the attributes related to the reporting on the instrument or on the ContactRegulatoryInfo in the ADS"""
        super(FContactRegulatoryInfo, self).Delete()

def RegulatoryInfo(self):
    """returns the FContactRegulatoryInfo instance for the given contact"""
    conactRegInfo = FContactRegulatoryInfo(self)
    return conactRegInfo

def Select(query):
    """Return a collection of FContactRegulatoryInfo instances matching constraint specified in the Select query"""
    party = None
    if query.find('and party') != -1:#it means there is an additional condition added
        pos = query.find('and party')
        party_name =  query[(pos + len('and party')):]
        query = query[0:pos]
        party_name =  party_name.replace('=', '').replace("'", '')
        party_name = party_name.strip()
        party = acm.FParty[party_name]
    return_result = FRegulatoryUtils.Select(query, "FContact", party)
    return return_result