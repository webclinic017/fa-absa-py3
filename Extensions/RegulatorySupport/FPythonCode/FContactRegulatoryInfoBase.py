"""------------------------------------------------------------------------
MODULE
    FContactRegulatoryInfoBase -
DESCRIPTION:
    This file provides the custom instance of RegulatoryInfo on the Contact which has all the RegulatoryInfo related methods
VERSION: 1.0.25(0.25.7)
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
import FRegulatoryInfoException
logger = 'FContactRegulatoryInfoBase'
VALUE_NOT_SET = ()

class FContactRegulatoryInfoBase(object):
    def __init__(self, contact = None):
        """class that maintains all data related to the regulatory on the FContact"""
        try:
            self.__contact = contact
            if not self.__contact:
                FRegulatoryLogger.ERROR(logger, "The name on the contact is the unique identifier of the contact. Kindly provide a valid acm.FContact object")
                return None
            self.__reg_date_of_birth = None
            self.__reg_first_name = None
            self.__reg_last_name = None
            self.__reg_national_id = None
            self.__reg_crm_id = None
            self.__crm_id_source = None
            self.__reg_exchange_id = None
            self.__reg_unique_name = None
            self.__client_type = None
            self.__is_general_partner = None
            if contact:
                self.__refresh(contact)
            self.__integration_utils = FIntegrationUtils.FIntegrationUtils()
        except Exception as e :
            FRegulatoryLogger.ERROR(logger, str(e))

    def __refresh(self, contact):
        self.__reg_date_of_birth = FRegulatoryUtils.get_addinfo_value('dateOfBirth', self.__contact)
        self.__reg_first_name = FRegulatoryUtils.get_addinfo_value('firstName', self.__contact)
        self.__reg_last_name = FRegulatoryUtils.get_addinfo_value('lastName', self.__contact)
        self.__reg_national_id = FRegulatoryUtils.get_addinfo_value('nationalId', self.__contact)
        self.__is_general_partner = FRegulatoryUtils.get_addinfo_value('regGeneralPartner', self.__contact)
        self.__reg_crm_id = FRegulatoryUtils.get_addinfo_value('regContactCrmId', self.__contact)
        self.__reg_exchange_id = FRegulatoryUtils.get_addinfo_value('regContExchangeId', self.__contact)
        try:
            self.__reg_unique_name = self.__contact.UniqueName()
        except:
            self.__reg_unique_name = FRegulatoryUtils.get_addinfo_value('uniqueName', self.__contact)

    def Contact(self):
        """returns the contact for which this wrapper has all the addinfo/column values"""
        return self.__contact

    def DateOfBirth(self, reg_date_of_birth = VALUE_NOT_SET):
        """Date of birth of the concerned natural person"""
        ael_reg_dob = None
        if reg_date_of_birth != VALUE_NOT_SET:
            try:
                ael_reg_dob = ael.date_from_string(reg_date_of_birth)
            except:
                if reg_date_of_birth not in ['', None]:
                    msg = "The value <%s> provided for DateOfBirth is invalid and hence will not be set of the DateOfBirth AdditionalInfo"%reg_date_of_birth
                    FRegulatoryLogger.ERROR(logger, msg)
                    raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            if ael_reg_dob:
                self.__reg_date_of_birth = reg_date_of_birth
            else:
                self.__reg_date_of_birth = None
            try:
                self.__contact.AdditionalInfo().DateOfBirth(self.__reg_date_of_birth)
            except:
                pass
        else:
            return self.__reg_date_of_birth

    def FirstName(self, reg_first_name = VALUE_NOT_SET):
        """First name of the concerned natural person"""
        if reg_first_name != VALUE_NOT_SET:
            self.__reg_first_name = reg_first_name
            try:
                self.__contact.AdditionalInfo().FirstName(self.__reg_first_name)
            except:
                pass
        else:
            if not self.__reg_first_name:
                self.__reg_first_name = None
            return self.__reg_first_name

    def LastName(self, reg_last_name = VALUE_NOT_SET):
        """Last name of the concerned natural person"""
        if reg_last_name != VALUE_NOT_SET:
            self.__reg_last_name = reg_last_name
            try:
                self.__contact.AdditionalInfo().LastName(self.__reg_last_name)
            except:
                pass
        else:
            if not self.__reg_last_name:
                self.__reg_last_name = None
            return self.__reg_last_name

    def NationalId(self, reg_national_id = VALUE_NOT_SET):
        """NationalId of the concerned natural person"""
        if reg_national_id != VALUE_NOT_SET:
            self.__reg_national_id = reg_national_id
            try:
                self.__contact.AdditionalInfo().NationalId(self.__reg_national_id)
            except:
                pass
        else:
            if not self.__reg_national_id:
                self.__reg_national_id = None
            return self.__reg_national_id

    def CrmId(self, crm_id = VALUE_NOT_SET):
        """CrmId of the concerned natural person"""
        if crm_id != VALUE_NOT_SET:
            self.__reg_crm_id = crm_id
            try:
                self.__contact.AdditionalInfo().RegContactCrmId(self.__reg_crm_id)
            except:
                pass
        else:
            if not self.__reg_crm_id:
                self.__reg_crm_id = None
            return self.__reg_crm_id

    def ExchangeId(self, exchange_id = VALUE_NOT_SET):
        """The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged."""
        if exchange_id != VALUE_NOT_SET:
            if str(exchange_id).isdigit():
                self.__reg_exchange_id = int(exchange_id)
            elif str(exchange_id) in ['None', '']:
                self.__reg_exchange_id = None
            else:
                msg = "The ExchangeId provided <%s> is not of the expected integer format"%str(exchange_id)
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            try:
                self.__contact.AdditionalInfo().RegContExchangeId(self.__reg_exchange_id)
            except:
                pass
        else:
            if not self.__reg_exchange_id:
                self.__reg_exchange_id = None
            return self.__reg_exchange_id

    def UniqueName(self, unique_name = VALUE_NOT_SET):
        """An optional unique name, if specified there can only be one contact with this name for each party."""
        if unique_name != VALUE_NOT_SET:
            try:
                if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2017.2:
                    self.__contact.UniqueName(unique_name)
                else:
                    is_unique, contact_name = FRegulatoryUtils.is_unique_name(self.__contact, unique_name)
                    if is_unique:
                        try:
                            self.__contact.AdditionalInfo().UniqueName(unique_name)
                        except:
                            pass
                    else:
                        msg = "The uniqueName <%s> provided for contact <%s> on party <%s> is not unique. Another contact <%s> already has this unique name."%(unique_name, self.__contact.Fullname(), self.__contact.Party().Name(), contact_name)
                        FRegulatoryLogger.ERROR(logger, msg)
                        raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
                self.__reg_unique_name = unique_name
            except Exception as e:
                FRegulatoryLogger.ERROR(logger, str(e))
                raise FRegulatoryInfoException.FRegInfoInvalidData(str(e))
        else:
            if not self.__reg_unique_name:
                self.__reg_unique_name = None
            return self.__reg_unique_name

    def ClientType(self):
        """returns the ClientType based on where the CrmId is found on the linked objects"""
        self.__client_type = FRegulatoryUtils.getClientType(self.__contact)
        return self.__client_type

    def JointAccount(self):
        """Another trader that jointly owns the account with this trader"""
        joint_accounts = []
        if self.IsGeneralPartner():
            for contact in self.__contact.Party().Contacts():            
                if contact.AdditionalInfo().RegGeneralPartner():               
                    joint_accounts.append(contact)
        else:
            FRegulatoryLogger.WARN(logger, "<%s> is not a General Partner. Hence JointAccount is None"%self.__contact.Fullname())
            joint_accounts = None
        return joint_accounts 

    def IsGeneralPartner(self, is_general_partner = VALUE_NOT_SET):
        """General partner has responsibility for the actions of the business, can legally bind
            the business and is personally liable for all the business's debts and obligations."""
        if is_general_partner != VALUE_NOT_SET:
            self.__is_general_partner = FRegulatoryUtils.get_bool(is_general_partner, 'IsGeneralPartner')
            FRegulatoryLogger.DEBUG(logger, "The IsGeneralPartner is being set to <%s>."%(str(self.__is_general_partner)))
            try:
                self.__contact.AdditionalInfo().RegGeneralPartner(self.__is_general_partner)
            except:
                pass

        else:
            if str(self.__is_general_partner) == "None":
                FRegulatoryLogger.DEBUG(logger, "The IsGeneralPartner is None. Hence defaulting it to False")
                self.__is_general_partner = False
            return self.__is_general_partner

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super(FContactRegulatoryInfoBase, self).__setattr__(attr, val)
        else:
            if hasattr(self, attr):
                getattr(self, attr)(val)

    def Commit(self):
        """Committing this instance will automatically commit all the RegulatorySupport related attributes on the contact"""
        try:
            acm.BeginTransaction()
            self.__contact.Commit()
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() < 2015.4:
                self.__integration_utils.set_additional_info('DateOfBirth', self.__contact, self.__reg_date_of_birth)
                self.__integration_utils.set_additional_info('FirstName', self.__contact, self.__reg_first_name)
                self.__integration_utils.set_additional_info('LastName', self.__contact, self.__reg_last_name)
                self.__integration_utils.set_additional_info('NationalId', self.__contact, self.__reg_national_id)
                self.__integration_utils.set_additional_info('RegContactCrmId', self.__contact, self.__reg_crm_id)
                self.__integration_utils.set_additional_info('RegContExchangeId', self.__contact, self.__reg_exchange_id)
                self.__integration_utils.set_additional_info('UniqueName', self.__contact, self.__reg_unique_name)
                self.__integration_utils.set_additional_info('RegGeneralPartner', self.__contact, self.__is_general_partner)
            acm.CommitTransaction()
        except Exception as e:
            FRegulatoryLogger.ERROR(logger, str(e))
            FRegulatoryLogger.ERROR(logger, "ABORTING TRANSACTION***********")
            acm.AbortTransaction()

    def Delete(self):
        """Deleting this instance automatically deletes all the attributes related to the reporting on the instrument or on the ContactRegulatoryInfo in the ADS"""
        FRegulatoryUtils.Delete(self.__contact, "Contact")
        FRegulatoryLogger.DEBUG(logger, "Deleted all AdditionalInfos on Contact related to Regulatory Reporting")

    def Attributes(self):
        """returns the attributes on the FContactRegulatoryInfoBase instance"""
        return FRegulatoryUtils.log_attributes('FContactRegulatoryInfo', self)

def RegulatoryInfo(self):
    """returns the FContactRegulatoryInfoBase instance for the given contact"""
    conactRegInfo = FContactRegulatoryInfo(self)
    return conactRegInfo

def Select(query):
    """Return a collection of FContactRegulatoryInfoBase instances matching constraint specified in the Select query"""
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

