""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FPersonRegulatoryInfo.py"
"""------------------------------------------------------------------------
MODULE
    FPersonRegulatoryInfo -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Person which has all the RegulatoryInfo related methods
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import FPersonRegulatoryInfoBase
import FRegulatoryUtils
logger = 'FPersonRegulatoryInfo'
VALUE_NOT_SET = ()

class FPersonRegulatoryInfo(FPersonRegulatoryInfoBase.FPersonRegulatoryInfoBase):
    def __init__(self, acm_object = None):
        """class that maintains all data related to the regulatory on the FPerson"""
        FPersonRegulatoryInfoBase.FPersonRegulatoryInfoBase.__init__(self, acm_object)
        self.reg_person = acm_object

    def Person(self):
        """The person to which all the FPersonRegulatoryInfoBase attributes belong"""
        return super(FPersonRegulatoryInfo, self).Person()

    def Contact(self):
        """The contact to which all the FPersonRegulatoryInfoBase attributes belong"""
        return super(FPersonRegulatoryInfo, self).Contact()
    
    def DateOfBirth(self, date_of_birth = VALUE_NOT_SET):
        return super(FPersonRegulatoryInfo, self).DateOfBirth(date_of_birth)
  
    def FirstName(self, first_name = VALUE_NOT_SET):
        """First name of the concerned natural person"""
        return super(FPersonRegulatoryInfo, self).FirstName(first_name)

    def LastName(self, last_name = VALUE_NOT_SET):
        """Last name of the concerned natural person"""
        return super(FPersonRegulatoryInfo, self).LastName(last_name)

    def NationalId(self, national_id = VALUE_NOT_SET):
        """NationalId of the concerned natural person"""
        return super(FPersonRegulatoryInfo, self).NationalId(national_id)

    def CrmId(self, crm_id = VALUE_NOT_SET):
        """CrmId of the concerned natural person"""
        return super(FPersonRegulatoryInfo, self).CrmId(crm_id)
    
    def ExchangeId(self, exchange_id = VALUE_NOT_SET):
        """The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged."""
        return super(FPersonRegulatoryInfo, self).ExchangeId(exchange_id)

    def ClientType(self):
        """returns the ClientType based on where the CrmId is found on the linked objects"""
        return super(FPersonRegulatoryInfo, self).ClientType()

    def __setattr__(self, attr, val):
        return super(FPersonRegulatoryInfo, self).__setattr__(attr, val)

    def Commit(self):
        """Committing this instance automatically commits all the attributes related to the reporting on the PersonRegulatoryInfo in the ADS"""
        super(FPersonRegulatoryInfo, self).Commit()

    def Delete(self):
        """Deleting this instance automatically deletes all the attributes related to the reporting on the PersonRegulatoryInfo in the ADS"""
        super(FPersonRegulatoryInfo, self).Delete() 

def RegulatoryInfo(self):
    personRegInfo = FPersonRegulatoryInfo(self)
    return personRegInfo

def Select(query):
    """Return a collection of FPersonRegulatoryInfo instances matching the constraint specified in the Select query"""
    return_result = FRegulatoryUtils.Select(query, "FContact")
    return return_result
