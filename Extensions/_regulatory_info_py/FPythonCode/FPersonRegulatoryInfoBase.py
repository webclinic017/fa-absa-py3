""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FPersonRegulatoryInfoBase.py"
"""------------------------------------------------------------------------
MODULE
    FPersonRegulatoryInfoBase -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Person which has all the RegulatoryInfo related methods
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import string
import acm
import FRegulatoryUtils
import FIntegrationUtils
import FRegulatoryLogger
import FRegulatoryInfoException
import ael
logger = 'FPersonRegulatoryInfoBase'
VALUE_NOT_SET = ()
from datetime import datetime
from datetime import timedelta
from time import mktime
class FPersonRegulatoryInfoBase(object):
    def __init__(self, acm_object = None):
        """class that maintains all data related to the regulatory on the FPerson"""
        self.__integration_utils = FIntegrationUtils.FIntegrationUtils()
        self.__person_dob = None
        self.__person_first_name = None
        self.__person_last_name = None
        self.__person_national_id = None
        self.__person_crm_id = None
        self.__crm_id_source = None
        self.__person_exchg_id = None
        self.__person = None
        self.__client_type = None
        if acm_object:
            self.__refresh(acm_object)

    def __refresh(self, acm_object):
        self.__acm_object = acm_object
        if self.__acm_object.IsKindOf(acm.FContact):
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5:
                if self.__acm_object.Person() and not self.__acm_object.Person().IsInfant():
                    self.__person = self.__acm_object.Person()
                else:
                    if self.__acm_object.AdditionalInfo().NationalId():
                        person = acm.FPerson[self.__acm_object.AdditionalInfo().NationalId()]
                        if person:
                            self.__person = person
                    if not self.__person:
                        self.__person = acm.FPerson()
                    self.__acm_object.Person(self.__person)
                    self.__person.DateOfBirth(self.__acm_object.AdditionalInfo().DateOfBirth())
                    self.__person.FirstName(self.__acm_object.AdditionalInfo().FirstName())
                    self.__person.LastName(self.__acm_object.AdditionalInfo().LastName())
                    self.__person.NationalId(self.__acm_object.AdditionalInfo().NationalId())
                    self.__person.CrmId(self.__acm_object.AdditionalInfo().RegContactCrmId())
                if self.__person.DateOfBirth():
                    self.__person_dob = self.__person.DateOfBirth()
                if self.__person.FirstName():
                    self.__person_first_name = self.__person.FirstName()
                if self.__person.LastName():
                    self.__person_last_name = self.__person.LastName()
                self.__person_national_id = self.__person.NationalId()
                self.__person_crm_id, self.__crm_id_source = FRegulatoryUtils.get_crm_id_from_person(self.__person)
                if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.2:
                    self.__person_exchg_id = FRegulatoryUtils.get_exchange_id_from_person(self.__person)
            else:
                self.__person_dob = self.__acm_object.AdditionalInfo().DateOfBirth()
                self.__person_first_name = self.__acm_object.AdditionalInfo().FirstName()
                self.__person_last_name = self.__acm_object.AdditionalInfo().LastName()
                self.__person_national_id = self.__acm_object.AdditionalInfo().NationalId()
                self.__person_crm_id, self.__crm_id_source = FRegulatoryUtils.get_crm_id_from_contact(self.__acm_object)
                self.__person_exchg_id = FRegulatoryUtils.get_exchange_id_from_contact(self.__acm_object)
                self.__person = self.__acm_object
        elif FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__acm_object.IsKindOf(acm.FPerson):
            self.__person = self.__acm_object
            if self.__acm_object.DateOfBirth():
                self.__person_dob = self.__acm_object.DateOfBirth()
            if self.__acm_object.FirstName():
                self.__person_first_name = self.__acm_object.FirstName()
            if self.__acm_object.LastName():
                self.__person_last_name = self.__acm_object.LastName()
            self.__person_national_id = self.__acm_object.NationalId()
            self.__person_crm_id, self.__crm_id_source = FRegulatoryUtils.get_crm_id_from_person(self.__acm_object)
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.2:
                self.__person_exchg_id = FRegulatoryUtils.get_exchange_id_from_person(self.__person)
            else:
                contacts = acm.FContact.Select('person = %d'%self.__acm_object.Oid())
                self.__person_exchg_id = FRegulatoryUtils.get_exchange_id_from_contacts(contacts)
            self.__person = self.__acm_object

    def DateOfBirth(self, date_of_birth = VALUE_NOT_SET):
        ael_dob = None
        if date_of_birth != VALUE_NOT_SET:
            try:#first check if it is a valid date, else dont set the additionalInfo
                ael_dob = ael.date_from_string(date_of_birth)
            except Exception, e:
                if ael_dob != '' and str(date_of_birth) not in ['None', '']:
                    FRegulatoryLogger.ERROR(logger, "The value <%s> provided for DateOfBirth is invalid and hence will not be set of the DateOfBirth AdditionalInfo"%date_of_birth)
            if ael_dob:
                self.__person_dob = date_of_birth
            else:
                self.__person_dob = None
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__person.IsKindOf(acm.FPerson):
                self.__person.DateOfBirth(self.__person_dob)
            elif self.__person.IsKindOf(acm.FContact):
                try:
                    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2015.4:
                        self.__acm_object.AdditionalInfo().DateOfBirth(self.__person_dob)
                except:
                    pass
        else:
            return self.__person_dob
  
    def FirstName(self, first_name = VALUE_NOT_SET):
        """First name of the concerned natural person"""
        if first_name != VALUE_NOT_SET:
            self.__person_first_name = first_name
            if not self.__person_first_name:
                self.__person_first_name = None
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__person.IsKindOf(acm.FPerson):
                self.__person.FirstName(self.__person_first_name)
            elif self.__person.IsKindOf(acm.FContact):
                try:
                    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2015.4:
                        self.__person.AdditionalInfo().FirstName(self.__person_first_name)
                except:
                    pass
        else:
            return self.__person_first_name

    def LastName(self, last_name = VALUE_NOT_SET):
        """Last name of the concerned natural person"""
        if last_name != VALUE_NOT_SET:
            self.__person_last_name = last_name
            if not self.__person_last_name:
                self.__person_last_name = None
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__person.IsKindOf(acm.FPerson):
                self.__person.LastName(self.__person_last_name)
            elif self.__person.IsKindOf(acm.FContact):
                try:
                    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2015.4:
                        self.__person.AdditionalInfo().LastName(self.__person_last_name)
                except:
                    pass
        else:
            return self.__person_last_name

    def NationalId(self, national_id = VALUE_NOT_SET):
        """NationalId of the concerned natural person"""
        if national_id != VALUE_NOT_SET:
            self.__person_national_id = national_id
            if not self.__person_national_id:
                self.__person_national_id = None
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__person.IsKindOf(acm.FPerson):
                self.__person.NationalId(self.__person_national_id)
            elif self.__person.IsKindOf(acm.FContact):
                try:
                    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2015.4:
                        self.__person.AdditionalInfo().NationalId(self.__person_national_id)
                except:
                    pass
        else:
            return self.__person_national_id

    def CrmId(self, crm_id = VALUE_NOT_SET):
        """CrmId of the concerned natural person"""
        if crm_id != VALUE_NOT_SET:
            self.__person_crm_id = crm_id
            if not self.__person_crm_id:
                self.__person_crm_id = None
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__person.IsKindOf(acm.FPerson):
                self.__person.CrmId(self.__person_crm_id)
            elif self.__person.IsKindOf(acm.FContact):
                try:
                    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2015.4:
                        self.__person.AdditionalInfo().RegContactCrmId(self.__person_crm_id)
                except:
                    pass
        else:
            return self.__person_crm_id
    
    def ExchangeId(self, exchange_id = VALUE_NOT_SET):
        """The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged."""
        if exchange_id != VALUE_NOT_SET:
            if str(exchange_id).isdigit():
                self.__person_exchg_id = int(exchange_id)
            elif str(exchange_id) in ['None', '']:
                self.__person_exchg_id = None
            else:
                msg = "The ExchangeId provided <%s> is not of the expected integer format"%str(exchange_id)
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and self.__person.IsKindOf(acm.FPerson):
                if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.2:
                    self.__person.ExchangeId(self.__person_exchg_id)
                else:
                    self.__acm_object.AdditionalInfo().RegContExchangeId(self.__person_exchg_id)
            elif self.__person.IsKindOf(acm.FContact):
                try:
                    self.__person.AdditionalInfo().RegContExchangeId(self.__person_exchg_id)
                except:
                    pass
        else:
            return self.__person_exchg_id

    def ClientType(self):
        """returns the ClientType based on where the CrmId is found on the linked objects"""
        self.__client_type = FRegulatoryUtils.getClientType(self.__person)
        return self.__client_type

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super(FPersonRegulatoryInfoBase, self).__setattr__(attr, val)
        else:
            if hasattr(self, attr):
                getattr(self, attr)(val)
    
    def Person(self):
        if self.__person.IsKindOf(acm.FPerson) and not self.__person.IsInfant():
            return self.__person

    def Contact(self):
        """get the contact to which the Person is linked"""
        person = None
        if self.__person.IsKindOf(acm.FContact):
            person = self.__person
        elif self.__acm_object.IsKindOf(acm.FContact):
            person = self.__acm_object
        return person

    def Commit(self):
        """Committing this instance automatically commits all the attributes related to the reporting on the PersonRegulatoryInfo in the ADS"""
        try:
            acm.BeginTransaction()
            self.__person.Commit()
            if not self.__person.IsKindOf(acm.FContact):
                if self.__acm_object.IsKindOf(acm.FContact):
                    self.__acm_object.Commit()
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() < 2015.4:
                self.__integration_utils.set_additional_info('DateOfBirth', self.__person, self.__person_dob)
                self.__integration_utils.set_additional_info('FirstName', self.__person, self.__person_first_name)
                self.__integration_utils.set_additional_info('LastName', self.__person, self.__person_last_name)
                self.__integration_utils.set_additional_info('NationalId', self.__person, self.__person_national_id)
                self.__integration_utils.set_additional_info('RegContactCrmId', self.__person, self.__person_crm_id)
                self.__integration_utils.set_additional_info('RegContExchangeId', self.__person, self.__person_exchg_id) 
            acm.CommitTransaction()
        except Exception, e:
            print str(e)
            print "ABORTING TRANSACTION***********"
            acm.AbortTransaction()

    def Attributes(self):
        """returns the attributes on the FPersonRegulatoryInfoBase instance"""
        return FRegulatoryUtils.log_attributes('FPersonRegulatoryInfo', self)

    def Delete(self):
        """Deleting this instance automatically deletes all the attributes related to the reporting on the PersonRegulatoryInfo in the ADS"""
        object_type = 'Contact'
        attributes = 'AdditionalInfos'
        if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5:
            object_type = 'Person'
            attributes = 'Attributes'
        FRegulatoryUtils.Delete(self.__person, object_type)
        FRegulatoryLogger.DEBUG(logger, "Deleted all %s on %s related to Regulatory Reporting"%(attributes, object_type))

def RegulatoryInfo(self):
    pass

def Select(query):
    """Return a collection of FPersonRegulatoryInfoBase instances matching the constraint specified in the Select query"""
    return_result = None
    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() <= 2016.5:
        party = None
        if query.find('and party') != -1:#it means there is an additional condition added
            pos = query.find('and party')
            party_name =  query[(pos + len('and party')):]
            query = query[0:pos]
            party_name =  party_name.replace('=', '').replace("'", '')
            party_name = party_name.strip()
            party = acm.FParty[party_name]
        return_result = FRegulatoryUtils.Select(query, "FContact", party)
    else:
        FRegulatoryLogger.DEBUG(logger, "Select query on PersonRegulatoryInfo is currently not supported")
    return return_result
