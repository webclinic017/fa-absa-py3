"""----------------------------------------------------------------------------
MODULE:
    FTreasuryOutBase

DESCRIPTION:
    A module for common getter formatter functions used across treasury out base files

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FMTOutBase import FMTOutBase

try:
    from FFXMMConfirmationOutUtils import *
except Exception as e:
    from FIRDConfirmationOutUtils import *

import FSwiftConfirmationUtils
import FIntegrationUtils


class FTreasuryOutBase(FMTOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FTreasuryOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    #Method to handle the cancellation of messages
    def handle_cancellation_message(self, swift_message, message_type, acm_object):
        '''Returns cancellation message and python object'''
        try:
            canc_message = ''
            swift_obj = None
            utils_obj = FIntegrationUtils.FIntegrationUtils()
            module = utils_obj.import_module_from_string(message_type)

            swift_obj = FSwiftWriterUtils.create_pyobj_from_swift_msg(swift_message)
            if swift_obj:
                val = swift_obj.SequenceA_GeneralInformation.SendersReference.value()
                swift_obj.SequenceA_GeneralInformation.RelatedReference = eval("module.%s_SequenceA_GeneralInformation_21_Type('%s')"%(message_type, val))
                swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

                swift_obj.SequenceA_GeneralInformation.TypeOfOperation = eval("module.%s_SequenceA_GeneralInformation_22A_Type('CANC')"%(message_type))
                swift_obj.SequenceA_GeneralInformation.TypeOfOperation.swiftTag = "22A"

                swift_obj.SequenceA_GeneralInformation.SendersReference = eval("module.%s_SequenceA_GeneralInformation_20_Type('%s')"%(message_type, get_confirmation_reference_prefix() + '-' + str(acm_object.Oid()) + '-' + str(acm_object.VersionId())))
                swift_obj.SequenceA_GeneralInformation.SendersReference.swiftTag = "20"

                canc_message = FSwiftWriterUtils.create_swift_msg_from_pyobj(swift_obj)

                #fmt_swift_header_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_header_object(message_type, acm_object, mt_message, None)
                #canc_message = fmt_swift_header_class_obj.swift_message_with_header()

        except Exception as e:
            raise e
        return canc_message, swift_obj

    # ------- partyA - 82A ----------------------------------
    # getter
    def partyA_82A(self):
        ''' Returns a dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'PARTY_A_ACCOUNT'])
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_A_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_party_a_details(self.acm_obj)

    # formatter
    def _format_partyA_82A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # ------- partyA - 82D ----------------------------------
    # getter
    def partyA_82D(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_A_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'PARTY_A_ADDRESS'])
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'PARTY_A_ACCOUNT'])
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            return get_party_a_details(self.acm_obj)

    # formatter
    def _format_partyA_82D(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # ------- partyA - 82J ----------------------------------
    # getter
    def partyA_82J(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_A_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                ['SWIFT', 'PARTY_A_ADDRESS'])
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                ['SWIFT', 'PARTY_A_ACCOUNT'])
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                ['SWIFT', 'PARTY_A_BIC'])
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_party_a_details(self.acm_obj)


    # formatter
    def _format_partyA_82J(self, val):
        return self._format_Option_J(val)
    # ------- partyB - 87A ----------------------------------
    # getter
    def partyB_87A(self):
        ''' Returns a dictionary with keys 'ACCOUNT', 'BIC' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'PARTY_B_ACCOUNT'])
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_B_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_party_b_details(self.acm_obj)


    # formatter
    def _format_partyB_87A(self, val):
        bic = val.get('BIC')
        account = val.get('ACCOUNT')
        if bic:
            val = str(bic)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # ------- partyB - 87D  ----------------------------------
    # getter
    def partyB_87D(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_B_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'PARTY_B_ADDRESS'])
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'PARTY_B_ACCOUNT'])
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            return values_dict
        else:
            return get_party_b_details(self.acm_obj)


    # formatter
    def _format_partyB_87D(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                val = "/" + str(account) + "\n" + str(val)
            return val

    # ------- partyB - 87J  ----------------------------------
    # getter
    def partyB_87J(self):
        '''Returns dictionary with keys 'NAME', 'ACCOUNT', 'ADDRESS' and their corresponding values '''
        if self.use_operations_xml:
            values_dict = {}
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_B_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                ['SWIFT', 'PARTY_B_ADDRESS'])
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                ['SWIFT', 'PARTY_B_ACCOUNT'])
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_B_BIC'])
            values_dict['NAME'] = name
            values_dict['ADDRESS'] = address
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_party_b_details(self.acm_obj)


    # formatter
    def _format_partyB_87J(self, val):
        return self._format_Option_J(val)

    # ------- formatter for Option J-----------------------------
    def _format_Option_J(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        bic = val.get('BIC')

        if name:
            val = '/ABIC/' + (bic or 'UKWN')
            if account:
                val = val + "/ACCT/" + account
            if address:
                val = val + '/ADD1/' + address
            val = str(val) + '/NAME/' + str(name)
            lines = FSwiftWriterUtils.split_text_on_character_limit(val, 40)
            val = FSwiftWriterUtils.allocate_space_for_n_lines(5, lines)
            return val

    # ------- Senders reference ----------------------------------
    def senders_reference_20(self):
        """ Expected return type : A string containing senders's reference"""
        if self.swift_metadata_xml_dom:
            senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['CONFIRMATION', 'SEQNBR'])
        else:
            senders_reference = str(self.acm_obj.Oid())

        return senders_reference

    def _format_senders_reference_20(self, val):
        if val:
            conf_obj = acm.FConfirmation[str(val)]
            val = "%s-%s-%s" % (
            get_confirmation_reference_prefix(), str(val), str(get_message_version_number(conf_obj)))
            return val

    # ------- Trade date - 30T----------------------------------
    def trade_date_30T(self):
        if self.swift_metadata_xml_dom:
            trade_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TRADE_DATE'])
        else:
            trade_date = FSwiftConfirmationUtils.get_trade_date(self.acm_obj)
        return trade_date

    def _format_trade_date_30T(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return str(val)

    # ------------------ type_of_operation -----------------------
    # getter
    def type_of_operation_22A(self):
        ''' Returns type of operation code as string  '''
        if self.use_operations_xml:
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'TYPE_OF_OPERATION'])
            return type_of_operation
        else:
            return get_type_of_operation(self.acm_obj)

    # formatter
    def _format_type_of_operation_22A(self, val):
        return val

    # ------------------ scope_of_operation -----------------------
    # getter
    def scope_of_operation_94A(self):
        '''Returns scope of operations code as string '''
        if self.use_operations_xml:
            scope_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'SCOPE_OF_OPERATION'],
                                                                          ignore_absense=True)
            return scope_of_operation
        else:
            return get_scope_of_operation(self.acm_obj)

    # formatter
    def _format_scope_of_operation_94A(self, val):
        return val

