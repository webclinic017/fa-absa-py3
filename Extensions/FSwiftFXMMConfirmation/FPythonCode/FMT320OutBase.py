"""----------------------------------------------------------------------------
MODULE:
    FMT320OutBase

DESCRIPTION:
    This module provides the base class for the FMT320 outgoing implementation

CLASS:
    FMT320Base

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftMLUtils
import FSwiftWriterMessageHeader
import MT320
import acm
from FLoanDepositOutBase import FLoanDepositOutBase
from FSwiftWriterEngine import validate_with, should_use_operations_xml

from FFXMMConfirmationOutUtils import *
import FSwiftWriterLogger
import FSwiftWriterUtils
import FSwiftOperationsAPI
import FSwiftConfirmationUtils
notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')


# IMPORTANT: optional sequence E, F, G, H are not supported in Front Arena for MT320 as of now. Whenever we will be
# adding support for those, we need to create optional sequence starting tag e.g 15E in the map_attributes function
# after self._message_sequences() call but before the for loop call.

class FMT320Base(FLoanDepositOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT320"
        self.use_operations_xml = should_use_operations_xml(self.swift_message_type)
        super(FMT320Base, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)


    def _message_sequences(self):
        """
        This function sets the basic attributes of mt message
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation = MT320.MT320_SequenceA_GeneralInformation()
        self.swift_obj.SequenceA_GeneralInformation.swiftTag = "15A"
        self.swift_obj.SequenceA_GeneralInformation.formatTag = "False"

        self.swift_obj.SequenceB_TransactionDetails = MT320.MT320_SequenceB_TransactionDetails()
        self.swift_obj.SequenceB_TransactionDetails.swiftTag = "15B"
        self.swift_obj.SequenceB_TransactionDetails.formatTag = "False"

        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA = MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA()
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.swiftTag = "15C"
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.formatTag = "False"

        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB = MT320.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB()
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.swiftTag = "15D"
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.formatTag = "False"

        self.set_original_trade_attributes()

    def set_original_trade_attributes(self):
        """
        This function retrieves the attributes of related trade.
        :return:
        """
        type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
        self.original_trade_ref = None
        self.original_trade_partyA_role = None
        self.original_value_date = None
        self.original_trade_date = None

        if type_of_event == "MATU" and self.acm_obj.EventType() != "Deposit Maturity":
            original_trade = self.acm_obj.Trade().ContractTrade()
            if original_trade.Type() == "Normal":
                for conf in original_trade.Confirmations():
                    ref_conf = conf
                    original_trade_msg_dict =  self.get_original_trade_tag_list(ref_conf)
                    self.original_trade_ref = original_trade_msg_dict.get('senders_ref')
                    self.original_trade_partyA_role = original_trade_msg_dict.get('partyA_role')
                    self.original_trade_date = original_trade_msg_dict.get('trade_date')
                    self.original_value_date = original_trade_msg_dict.get('value_date')
                    break


    def get_original_trade_tag_list(self, conf_obj):
        """
        This function extracts the swift message of the related confirmation
        :param conf_obj:
        :return:
        """
        ref_number = {}
        swift_message = FSwiftMLUtils.get_outgoing_mt_message(conf_obj)
        if swift_message:
            swift_msg_list = FSwiftMLUtils.swift_message_to_list(swift_message)
            for tag_list in swift_msg_list:
                if tag_list[0] == '20':
                    ref_number['senders_ref'] = tag_list[1]
                elif tag_list[0] == '17R':
                    ref_number['partyA_role'] = tag_list[1]
                elif tag_list[0] == '30T':
                    ref_number['trade_date'] = tag_list[1]
                elif tag_list[0] == '30V':
                    ref_number['value_date'] = tag_list[1]

        return ref_number

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_20_Type)
    def _validate_senders_reference_20(self, val):
        """
        Validator function for senders_reference_20
        :param val:
        :return:
        """
        validate_slash_and_double_slash(val, "Sender's Reference")
        return val

    #setter
    def _set_senders_reference_20(self, val):
        """
        Setter function for senders_reference_20
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.SendersReference = val
        self.swift_obj.SequenceA_GeneralInformation.SendersReference.swiftTag = "20"


    #getter
    def related_reference_21(self):
        """ Expected return type : dictionary with keys 'related_reference' and 'ref_conf' """
        values_dict = {}

        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_EVENT'])
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_OF_OPERATION'])
        else:
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)

            type_of_operation = str(get_type_of_operation(self.acm_obj))


        ref_conf = None
        related_reference = None
        if type_of_event in ['CONF', 'MATU']:
            if type_of_operation in ['AMND', 'CANC', 'DUPL']:

                if self.use_operations_xml:
                    related_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                 ['SWIFT', 'YOUR_REFERENCE'],
                                                                                 ignore_absense=True)
                    conf_id = related_reference.strip("FAC-")
                else:
                    related_reference = get_related_confirmation(self.acm_obj).Oid()
                    conf_id = related_reference


                ref_conf = None
                if related_reference:
                    ref_conf = acm.FConfirmation[str(conf_id)]
                else:
                    if self.use_operations_xml:
                        senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['CONFIRMATION', 'SEQNBR'])
                    else:
                        senders_reference = self.acm_obj.Oid()

                    confirmation = acm.FConfirmation[str(senders_reference)]
                    if FSwiftMLUtils.get_acm_version() >= 2016.4:
                        #from FConfirmationEnums import ConfirmationType
                        ConfirmationType = FSwiftOperationsAPI.GetConfirmationTypeEnum()
                        if confirmation.Type() in (ConfirmationType.AMENDMENT, ConfirmationType.CANCELLATION):
                            ref_conf = confirmation.ConfirmationReference()

                    else:
                        if confirmation.Type() in ("Amendment", "Cancellation"):
                            ref_conf = confirmation.ConfirmationReference()
            else:
                related_reference = self.original_trade_ref
                values_dict['related_reference'] = related_reference
        elif type_of_event == 'ROLL' and type_of_operation:
            if self.use_operations_xml:
                senders_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                                     ['CONFIRMATION', 'SEQNBR'])
            else:
                senders_reference = self.acm_obj.Oid()
            confirmation = acm.FConfirmation[str(senders_reference)]
            connected_confirmations = confirmation.Trade().ContractTrade().Confirmations()
            confirmations = []
            for conf in connected_confirmations:
                if str(FSwiftMLUtils.calculate_mt_type_from_acm_object(conf)) == "320" and\
                        get_event_change_item(conf) != 'Rate Fixing':
                    confirmations.append(conf)
            if confirmations:
                ref_conf = confirmations[-1]


        if related_reference and ref_conf:
            values_dict['related_reference'] = related_reference
            values_dict['ref_conf'] = ref_conf
        return values_dict

    #formatter
    def _format_related_reference_21(self, val):
        """
        Formatter function for related_reference_21
        :param val:
        :return:
        """
        related_reference = val.get('related_reference')
        ref_conf = val.get('ref_conf')
        ret_val = ''

        if ref_conf:
            related_reference = get_confirmation_reference_prefix() + "-" + str(ref_conf.Oid())
            if related_reference:
                ref_conf, related_reference = check_for_valid_related_reference(ref_conf, related_reference)
                version_number_of_related_reference = get_version_for_sent_message_on(ref_conf, 'MT320')
                ret_val = str(related_reference) + "-" + str(version_number_of_related_reference)
        else:
            ret_val = related_reference

        return ret_val

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_21_Type, is_mandatory=True)
    def _validate_related_reference_21(self, val):
        """
        Validator function for related_reference_21
        :param val:
        :return:
        """
        validate_slash_and_double_slash(val, "Sender's Reference")
        return val

    def _check_condition_set_related_reference_21(self):
        """
        This function check the condition to set related_reference_21
        :return:
        """

        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'TYPE_EVENT'])
            type_of_operation = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'TYPE_OF_OPERATION'])
        else:
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)

            type_of_operation = str(get_type_of_operation(self.acm_obj))

        ref_conf = None
        related_reference = None
        if type_of_event == 'CONF':
            if type_of_operation in ['AMND', 'CANC', 'DUPL']:
                return True
        elif type_of_event == 'ROLL' or (type_of_event == 'MATU' and self.acm_obj.EventType() != 'Deposit Maturity'):
            return True
        return False

    #setter
    def _set_related_reference_21(self, val):
        """
        :param val: Setter function for related_reference_21
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference = val
        self.swift_obj.SequenceA_GeneralInformation.RelatedReference.swiftTag = "21"

    #getter
    def type_of_operation_22A(self):
        """
        Getter function for type_of_operation_22A
        :return:
        """
        type_of_operation = ''
        if self.acm_obj.EventType() in ["Close", "Partial Close"]:
            type_of_operation = 'NEWT'
        else:
            type_of_operation = super(FMT320Base, self).type_of_operation_22A()
        return type_of_operation

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_22A_Type)
    def _validate_type_of_operation_22A(self, val):
        """
        Validator function for type_of_operation_22A
        :param val:
        :return:
        """
        return val

    #setter
    def _set_type_of_operation_22A(self, val):
        """
        Setter function for type_of_operation_22A
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfOperation.swiftTag = "22A"

    #getter
    # moved to FLoanDepositOutBase

    #formatter
    def _format_type_of_event_22B(self, val):
        """
        Formatter function for type_of_event_22B
        :param val:
        :return:
        """
        return val

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_22B_Type)
    def _validate_type_of_event_22B(self, val):
        """
        Validator function for type_of_event_22B
        :param val:
        :return:
        """
        return val

    #setter
    def _set_type_of_event_22B(self, val):
        """
        Setter function for type_of_event_22B
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.TypeOfEvent = val
        self.swift_obj.SequenceA_GeneralInformation.TypeOfEvent.swiftTag = "22B"

    #getter
    def common_reference_22C(self):
        """
        Getter function for common_reference_22C
        :return:
        """
        values_dict = {}
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
            interest_rate = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'INTEREST_RATE'])
        else:
            senders_bic = get_senders_bic(self.acm_obj)
            receivers_bic = get_receivers_bic(self.acm_obj)
            interest_rate = get_interest_rate(self.acm_obj)

        values_dict['senders_bic'] = senders_bic
        values_dict['receivers_bic'] = receivers_bic
        values_dict['interest_rate'] = interest_rate

        return values_dict

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_22C_Type)
    def _validate_common_reference_22C(self, val):
        """
        Validater function for common_reference_22C
        :param val:
        :return:
        """
        return val

    #setter
    def _set_common_reference_22C(self, val):
        """
        Setter function for common_reference_22C
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.CommonReference = val
        self.swift_obj.SequenceA_GeneralInformation.CommonReference.swiftTag = "22C"



    # option getter
    def get_partyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_party_A(self):
        """
        Setter function for party_A option
        :return:
        """
        if self.use_operations_xml:
            party_A_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                      ['SWIFT', 'PARTY_A_OPTION'])
        else:
            party_A_option = self.get_partyA_option()

        if party_A_option == "A":
            return 'partyA_82A'
        elif party_A_option == "D":
            return 'partyA_82D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(party_A_option),
                                                                                                 'PartyA_82a'))
            return 'partyA_82A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_82A_Type)
    def _validate_partyA_82A(self, val):
        """
        Validater function for partyA_82A
        :param val:
        :return:
        """
        return val

    #setter
    def _setpartyA_82A(self, val):
        """
        Setter function for partyA_82A
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_A.swiftTag = "82A"

    #getter
    # Moved to FLoanDepositOutBase


    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_82D_Type)
    def _validate_partyA_82D(self, val):
        """
        Validater function for partyA_82D
        :param val:
        :return:
        """
        return val

    #setter
    def _setpartyA_82D(self, val):
        """
        Setter function for partyA_82D
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.PartyA_D = val
        self.swift_obj.SequenceA_GeneralInformation.PartyA_D.swiftTag = "82D"


    # option getter

    def get_partyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_party_B(self):
        """
        Setter functiono for partyB option
        :return:
        """
        if self.use_operations_xml:
            party_B_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                  ['SWIFT', 'PARTY_B_OPTION'])
        else:
            party_B_option = self.get_partyB_option()

        if party_B_option == "A":
            return 'partyB_87A'
        elif party_B_option == "D":
            return 'partyB_87D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,
                                                                                                 str(party_B_option),
                                                                                                 'PartyB_87a'))
            return 'partyB_87A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_87A_Type)
    def _validate_partyB_87A(self, val):
        """
        Validator function for partyB_87A
        :param val:
        :return:
        """
        return val

    #setter
    def _setpartyB_87A(self, val):
        """
        Setter function for partyB_87A
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.PartyB_A = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_A.swiftTag = "87A"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_87D_Type)
    def _validate_partyB_87D(self, val):
        """
        Validater function for partyB_87D
        :param val:
        :return:
        """
        return val

    #setter
    def _setpartyB_87D(self, val):
        """
        Setter function for partyB_87D
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D = val
        self.swift_obj.SequenceA_GeneralInformation.PartyB_D.swiftTag = "87D"

    #getter
    def terms_and_conditions_77D(self):
        """
        Getter function for terms_and_conditions_77D
        :return:
        """
        if self.use_operations_xml:
            terms_and_conditions = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                            ['SWIFT', 'TERMS_CONDITIONS'],
                                                                            ignore_absense=True)
        else:
            terms_and_conditions = get_terms_and_conditions(self.acm_obj, self.swift_message_type)

        return terms_and_conditions


    #formatter
    def _format_terms_and_conditions_77D(self, val):
        """
        Formatter function for terms_and_conditions_77D
        :param val:
        :return:
        """
        lines = FSwiftWriterUtils.split_text_on_character_limit(val, 35)
        val = FSwiftWriterUtils.allocate_space_for_n_lines(6, lines)
        return val


    #validator
    @validate_with(MT320.MT320_SequenceA_GeneralInformation_77D_Type)
    def _validate_terms_and_conditions_77D(self, val):
        """
        Validater function for terms_and_conditions_77D
        :param val:
        :return:
        """
        return val

    #setter
    def _set_terms_and_conditions_77D(self, val):
        """
        Setter function for terms_and_conditions_77D
        :param val:
        :return:
        """
        self.swift_obj.SequenceA_GeneralInformation.TermsAndConditions = val
        self.swift_obj.SequenceA_GeneralInformation.TermsAndConditions.swiftTag = "77D"

    #getter
    def party_As_role_17R(self):
        """
        Getter function for party_As_role_17R
        :return:
        """
        if self.use_operations_xml:
            party_As_role = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'PARTY_A_ROLE'])
        else:
            if self.original_trade_partyA_role is not None:
                party_As_role = self.original_trade_partyA_role
            else:
                party_As_role = get_party_A_role(self.acm_obj)
        return party_As_role


    #formatter
    def _format_party_As_role_17R(self, val):
        """
        Formatter function for party_As_role_17R
        :param val:
        :return:
        """
        return val


    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_17R_Type)
    def _validate_party_As_role_17R(self, val):
        """
        Validater function for party_As_role_17R
        :param val:
        :return:
        """
        return val

    #setter
    def _set_party_As_role_17R(self, val):
        """
        Setter function for party_As_role_17R
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.PartyAsRole = val
        self.swift_obj.SequenceB_TransactionDetails.PartyAsRole.swiftTag = "17R"

    #getter
    def trade_date_30T(self):
        """
        Getter function for trade_date_30T
        :return:
        """
        trade_date = ''
        if self.original_trade_date:
            trade_date = self.original_trade_date
        else:
            trade_date = super(FMT320Base, self).trade_date_30T()

        return trade_date

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_30T_Type)
    def _validate_trade_date_30T(self, val):
        """
        Validater function for trade_date_30T
        :param val:
        :return:
        """
        return val

    #setter
    def _set_trade_date_30T(self, val):
        """
        Setter function for trade_date_30T
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.TradeDate = val
        self.swift_obj.SequenceB_TransactionDetails.TradeDate.swiftTag = "30T"

    #getter
    def value_date_30V(self):
        """
        Getter function for trade_date_30V
        :return:
        """
        value_date = ''
        if self.original_value_date:
            value_date = self.original_value_date
        else:
            value_date = super(FMT320Base, self).value_date_30V()

        return value_date

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_30V_Type)
    def _validate_value_date_30V(self, val):
        """
        Validator function for trade_date_30V
        :param val:
        :return:
        """
        return val

    #setter
    def _set_value_date_30V(self, val):
        """
        Setter function for trade_date_30V
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.ValueDate = val
        self.swift_obj.SequenceB_TransactionDetails.ValueDate.swiftTag = "30V"

    #getter
    def maturity_date_30P(self):
        """
        Getter function for maturity_date_30P
        :return:
        """
        if self.use_operations_xml:
            maturity_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                     ['SWIFT', 'MATURITY_DATE'])
        else:
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
            if type_of_event in ["MATU"] and self.acm_obj.EventType() != 'Deposit Maturity':
                maturity_date = self.acm_obj.Trade().ValueDay()
            else:
                maturity_date = FSwiftConfirmationUtils.get_maturity_date(self.acm_obj)

        return maturity_date

    #formatter
    def _format_maturity_date_30P(self, val):
        """
        Formatter function for maturity_date_30P
        :param val:
        :return:
        """
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return str(val)

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_30P_Type)
    def _validate_maturity_date_30P(self, val):
        """
        Validator function for maturity_date_30P
        :param val:
        :return:
        """
        return val

    #setter
    def _set_maturity_date_30P(self, val):
        """
        Setter function for maturity_date_30P
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.MaturityDate = val
        self.swift_obj.SequenceB_TransactionDetails.MaturityDate.swiftTag = "30P"

    def get_principal_amount_320(self):
        """
        Helper function for get_principal_amount_320
        :return:
        """
        principal_amt = ''
        type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
        if type_of_event in ["MATU"] and self.acm_obj.EventType() != "Deposit Maturity":
            principal_amt = self.acm_obj.Trade().FaceValue()
        else:
            principal_amt = get_principal_amount(self.acm_obj)

        return principal_amt




    #getter
    def currency_principal_amount_32B(self):
        """
        Getter function for currency_principal_amount_32B
        :return:
        """
        values_dict = {}
        if self.use_operations_xml:
            principal_amount = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                        ['SWIFT', 'PRINCIPAL_AMOUNT'])
            principal_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'PRINCIPAL_CURRENCY'])
        else:
            principal_amount = self.get_principal_amount_320()
            principal_currency = get_principal_currency(self.acm_obj)


        values_dict['principal_amount'] = principal_amount
        values_dict['principal_currency'] = principal_currency
        return values_dict

    #formatter
    def _format_currency_principal_amount_32B(self, val):
        """
        Formatter function for currency_principal_amount_32B
        :param val:
        :return:
        """
        principal_amount = val.get('principal_amount')
        principal_currency = val.get('principal_currency')
        if principal_amount and principal_currency:
            principal_amount = abs(principal_amount)
            principal_amount = apply_currency_precision(principal_currency, float(principal_amount))
            val = str(principal_currency) + str(FSwiftMLUtils.float_to_swiftmt(str(principal_amount)))
            return val

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_32B_Type)
    def _validate_currency_principal_amount_32B(self, val):
        """
        Validator function for currency_principal_amount_32B
        :param val:
        :return:
        """
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('-', '').replace('.', ','), 15, "Currency And Principal Amount")
        return val

    #setter
    def _set_currency_principal_amount_32B(self, val):
        """
        Setter function for currency_principal_amount_32B
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.CurrencyAndPrincipalAmount = val
        self.swift_obj.SequenceB_TransactionDetails.CurrencyAndPrincipalAmount.swiftTag = "32B"

    #getter
    def amount_to_be_settled_32H(self):
        """
        Getter function for currency_principal_amount_32H
        :return:
        """
        values_dict = {}
        if self.use_operations_xml:
            settle_amt = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SETTLE_AMT'],
                                                                  ignore_absense=True)
            settle_curr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SETTLE_CURR'],
                                                                   ignore_absense=True)
        else:
            settle_amt = get_settle_amount_MT320(self.acm_obj)

            settle_curr = get_settle_currency_MT320(self.acm_obj)

        if settle_amt and settle_curr:
            values_dict['settle_amt'] = settle_amt
            values_dict['settle_curr'] = settle_curr

        return values_dict

    #formatter
    def _format_amount_to_be_settled_32H(self, val):
        """
        Formatter function for currency_principal_amount_32H
        :param val:
        :return:
        """
        settle_amt = val.get('settle_amt')
        settle_curr = val.get('settle_curr')
        if settle_amt and settle_curr:
            settle_amt = apply_currency_precision(settle_curr, float(settle_amt))
            val = represent_negative_currency_amount(settle_curr, settle_amt)
            return str(val)

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_32H_Type, is_mandatory = True)
    def _validate_amount_to_be_settled_32H(self, val):
        """
        Validator function for currency_principal_amount_32H
        :param val:
        :return:
        """
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('-', '').replace('.', ','), 15, "Amount To Be Settled")
        return val

    def _check_condition_set_amount_to_be_settled_32H(self):
        """
        Function for check the condition if currency_principal_amount_32H is to be set
        :return:
        """
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)

        return type_of_event  == 'ROLL' or ( type_of_event  == 'MATU' and self.acm_obj.EventType() != "Deposit Maturity" )

    #setter
    def _set_amount_to_be_settled_32H(self, val):
        """
        Setter function for amount_to_be_settled_32H
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.AmountToBeSettled = val
        self.swift_obj.SequenceB_TransactionDetails.AmountToBeSettled.swiftTag = "32H"

    #getter
    def next_interest_due_date_30X(self):
        """
        Getter function for amount_to_be_settled_32H
        :return:
        """
        if self.use_operations_xml:
            interest_due_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'NEXT_INTEREST_DUE_DATE'],
                                                                         ignore_absense=True)
        else:
            interest_due_date = get_next_interest_due_date(self.acm_obj)

        return interest_due_date


    #formatter
    def _format_next_interest_due_date_30X(self, val):
        """
        Formatter function for next_interest_due_date_30X
        :param val:
        :return:
        """
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return str(val)

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_30X_Type, is_mandatory = True)
    def _validate_next_interest_due_date_30X(self, val):
        """
        Validator function for next_interest_due_date_30X
        :param val:
        :return:
        """

        return val

    def _check_condition_set_next_interest_due_date_30X(self):
        """
        This function check is next_interest_due_date_30X needs to be set
        :return:
        """
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)

        if type_of_event in ['CONF', 'ROLL']:
            return True
        return False

    #setter
    def _set_next_interest_due_date_30X(self, val):
        """
        Setter function for next_interest_due_date_30X
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.NextInterestDueDate = val
        self.swift_obj.SequenceB_TransactionDetails.NextInterestDueDate.swiftTag = "30X"

    #getter
    def currency_interest_amount_34E(self):
        """
        Getter function for currency_interest_amount_34E
        :return:
        """
        values_dict = {}
        interest_amount = get_interest_amount(self.acm_obj)

        if self.use_operations_xml:
            interest_currency = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                         ['SWIFT', 'INTEREST_CURRENCY'])
        else:
            interest_currency = get_principal_currency(self.acm_obj)

        values_dict['interest_amount'] = interest_amount
        values_dict['interest_currency'] = interest_currency
        return values_dict

    #formatter
    def _format_currency_interest_amount_34E(self, val):
        """
        Formatter function for currency_interest_amount_34E
        :param val:
        :return:
        """
        interest_amount = val.get('interest_amount')
        interest_currency = val.get('interest_currency')
        if (interest_amount in [0, 0.0, '0', '0.0'] or interest_amount) and interest_currency:
            interest_amount = apply_currency_precision(interest_currency, float(interest_amount))
            val = represent_negative_currency_amount(interest_currency, interest_amount)
            return str(val)

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_34E_Type)
    def _validate_currency_interest_amount_34E(self, val):
        """
        Validator function for currency_interest_amount_34E
        :param val:
        :return:
        """
        amount = get_amount_from_currency_amount(val)
        validateAmount(amount.replace('-', '').replace('.', ','), 15, "Currency And Interest Amount")
        return val

    #setter
    def _set_currency_interest_amount_34E(self, val):
        """
        Setter function for currency_interest_amount_34E
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount = val
        self.swift_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount.swiftTag = "34E"

    #getter
    def interest_rate_37G(self):
        """
        Getter function for interest_rate_37G
        :return:
        """
        interest_rate = get_interest_rate(self.acm_obj)
        return interest_rate


    #formatter
    def _format_interest_rate_37G(self, val):
        """
        Formatter function for interest_rate_37G
        :param val:
        :return:
        """
        if val in [0, 0.0, '0', '0.0'] or val:
            val = FSwiftWriterUtils.represent_negative_amount(val)
            return str(val)

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_37G_Type)
    def _validate_interest_rate_37G(self, interest_rate):
        """
        Validater function for interest_rate_37G
        :param interest_rate:
        :return:
        """
        validateAmount(interest_rate.replace('N', ''), 12, "Interest Rate")
        return interest_rate

    #setter
    def _set_interest_rate_37G(self, val):
        """
        Setter function for interest_rate_37G
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.InterestRate = val
        self.swift_obj.SequenceB_TransactionDetails.InterestRate.swiftTag = "37G"

    #getter
    # Moved to FLoanDepositOutBase


    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceB_TransactionDetails_14D_Type)
    def _validate_day_count_fraction_14D(self, val):
        """
        Validator function  for day_count_fraction_14D
        :param val:
        :return:
        """
        return val

    #setter
    def _set_day_count_fraction_14D(self, val):
        """
        Setter function  for day_count_fraction_14D
        :param val:
        :return:
        """
        self.swift_obj.SequenceB_TransactionDetails.DayCountFraction = val
        self.swift_obj.SequenceB_TransactionDetails.DayCountFraction.swiftTag = "14D"



    # option getter
    def get_intermediary_PartyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_intermediary_PartyA(self):
        """
        Setter function  for deciding the option of intermediary_PartyA
        :return:
        """
        if self.use_operations_xml:
            intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'SIA_PARTY_A_INTERMEDIARY_OPTION'],
                                                                           ignore_absense=True)
        else:
            option = self.get_intermediary_PartyA_option()
            intermediary_option = get_SIA_party_intermediary_option(self.acm_obj, 'A', option)


        if intermediary_option == "A":
            return 'intermediary_PartyA_56A'
        elif intermediary_option == "D":
            return 'intermediary_PartyA_56D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type,  str(intermediary_option), 'Intermediary_PartyA_56a'))
            return 'intermediary_PartyA_56A'


    #getter
    def intermediary_PartyA_56A(self):
        """
        Getter function  for intermediary_PartyA_56A
        :return:
        """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_A_INTERMEDIARY_BIC'], ignore_absense=True)
        else:
            account = get_SIA_party_intermediary_account(self.acm_obj, 'A')
            bic = get_SIA_party_intermediary_bic(self.acm_obj, 'A')

        values_dict['account'] = account
        values_dict['bic'] = bic
        return values_dict

    #formatter
    def _format_intermediary_PartyA_56A(self, val):
        """
        Formatter function  for intermediary_PartyA_56A
        :param val:
        :return:
        """
        account = val.get('account')
        bic = val.get('bic')
        if bic:
            field_value = str(bic)
            if account:
                field_value = "/" + str(account) + "\n" + str(field_value)
            return field_value

    #validator
    @validate_with(MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56A_Type)
    def _validate_intermediary_PartyA_56A(self, val):
        """
        Validator function  for intermediary_PartyA_56A
        :param val:
        :return:
        """
        return val


    #setter
    def _setintermediary_PartyA_56A(self, val):
        """
        Setter function  for intermediary_PartyA_56A
        :param val:
        :return:
        """
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A.swiftTag = "56A"

    #getter
    def intermediary_PartyA_56D(self):
        """
        Getter function  for intermediary_PartyA_56D
        :return:
        """
        values_dict = {}

        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_INTERMEDIARY_NAME'],
                                                               ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_INTERMEDIARY_ADDRESS'],
                                                               ignore_absense=True)
        else:
            account = get_SIA_party_intermediary_account(self.acm_obj, 'A')
            name = get_SIA_party_intermediary_name(self.acm_obj, 'A')
            address = get_SIA_party_intermediary_address(self.acm_obj, 'A')

        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    #formatter
    def _format_intermediary_PartyA_56D(self, val):
        """
        Formatter function  for intermediary_PartyA_56D
        :param val:
        :return:
        """
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                field_value = "/" + str(account) + "\n" + str(val)
            return field_value

    #validator
    @validate_with(MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_56D_Type)
    def _validate_intermediary_PartyA_56D(self, val):
        """
        Validator function  for intermediary_PartyA_56D
        :param val:
        :return:
        """
        return val

    #setter
    def _setintermediary_PartyA_56D(self, val):
        """
        Setter function  for intermediary_PartyA_56D
        :param val:
        :return:
        """
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_D = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_D.swiftTag = "56D"

    # option getter
    def get_delivery_agent_PartyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    # setter
    def _set_OPTION_delivery_agent_PartyA(self):
        """
        Setter function for choosing delivery_agent_PartyA option
        :param self:
        :return:
        """
        option = self.get_delivery_agent_PartyA_option()
        delivery_option = get_SIA_party_delivery_agent_option(self.acm_obj, 'A', option)

        if delivery_option == "A":
           return 'delivery_agent_PartyA_53A'
        elif delivery_option == "D":
           return 'delivery_agent_PartyA_53D'
        else:
           notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." %
                         (self.swift_message_type,
                          str(delivery_option), 'delivery_agent_PartyA_53a'))
           return 'delivery_agent_PartyA_53A'

    # getter
    def delivery_agent_PartyA_53A(self):
        """
        Getter function for delivery_agent_PartyA_53A
        :return:
        """
        values_dict = {}
        account = get_SIA_party_delivery_agent_account(self.acm_obj, 'A')
        bic = get_SIA_party_delivery_agent_bic(self.acm_obj, 'A')

        values_dict['account'] = account
        values_dict['bic'] = bic
        return values_dict

    # formatter
    def _format_delivery_agent_PartyA_53A(self, val):
        """
        Formatter function for delivery_agent_PartyA_53A
        :param val:
        :return:
        """
        account = val.get('account')
        bic = val.get('bic')
        if bic:
           field_value = str(bic)
           if account:
               field_value = "/" + str(account) + "\n" + str(field_value)
           return field_value

    # validator
    @validate_with(MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53A_Type)
    def _validate_delivery_agent_PartyA_53A(self, val):
        """
        Validator function for delivery_agent_PartyA_53A
        :param val:
        :return:
        """
        return val

    # setter
    def _setdelivery_agent_PartyA_53A(self, val):
        """
        Setter function for delivery_agent_PartyA_53A
        :param val:
        :return:
        """
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_A.swiftTag = "53A"

    # getter
    def delivery_agent_PartyA_53D(self):
        """
        Getter function for delivery_agent_PartyA_53D
        :return:
        """
        values_dict = {}
        account = get_SIA_party_delivery_agent_account(self.acm_obj, 'A')
        name = get_SIA_party_delivery_agent_name(self.acm_obj, 'A')
        address = get_SIA_party_delivery_agent_address(self.acm_obj, 'A')

        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    # formatter
    def _format_delivery_agent_PartyA_53D(self, val):
        """
        Formatter function for delivery_agent_PartyA_53D
        :param val:
        :return:
        """
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
           name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
           address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
           field_value = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
           if account:
               field_value = "/" + str(account) + "\n" + str(field_value)
           return field_value

    # validator
    @validate_with(MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_53D_Type)
    def _validate_delivery_agent_PartyA_53D(self, val):
        """
        Validatoer function for delivery_agent_PartyA_53D
        :param val:
        :return:
        """
        return val

    # setter
    def _setdelivery_agent_PartyA_53D(self, val):
        """
        Setter function for delivery_agent_PartyA_53D
        :param val:
        :return:
        """
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_D = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.DeliveryAgent_D.swiftTag = "53D"

    # option getter
    def get_receiving_agent_PartyA_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_receiving_agent_PartyA(self):
        """
        This function chooses the option receiving_agent_PartyA
        :return:
        """
        if self.use_operations_xml:
            buy_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_OPTION'])
        else:
            option = self.get_receiving_agent_PartyA_option()
            buy_receiving_agent_option = get_SIA_party_receiving_agent_option('A', self.acm_obj, self.swift_message_type, option)

        if buy_receiving_agent_option == "A":
            return 'receiving_agent_PartyA_57A'
        elif buy_receiving_agent_option == "D":
            return 'receiving_agent_PartyA_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(buy_receiving_agent_option), 'Receiving_agent_PartyA_57a'))
            return 'receiving_agent_PartyA_57A'

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57A_Type)
    def _validate_receiving_agent_PartyA_57A(self, val):
        """
        Validator function for receiving_agent_PartyA_57A
        :param val:
        :return:
        """
        return val

    #setter
    def _setreceiving_agent_PartyA_57A(self, val):
        """
        Setter function for receiving_agent_PartyA_57A
        :param val:
        :return:
        """
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_A.swiftTag = "57A"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase


    #validator
    @validate_with(MT320.MT320_SequenceC_SettlementInstructionsforAmountsPayablebyPartyA_57D_Type)
    def _validate_receiving_agent_PartyA_57D(self, val):
        """
        Validator function for receiving_agent_PartyA_57A
        :param val:
        :return:
        """
        return val

    #setter
    def _setreceiving_agent_PartyA_57D(self, val):
        """
        Setter function for receiving_agent_PartyA_57D
        :param val:
        :return:
        """
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_D = val
        self.swift_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.ReceivingAgent_D.swiftTag = "57D"

    # option getter
    def get_intermediary_PartyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_intermediary_PartyB(self):
        """
        This function selects the option for intermediary_PartyB
        :return:
        """
        if self.use_operations_xml:
            intermediary_option = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                           ['SWIFT', 'SIA_PARTY_B_INTERMEDIARY_OPTION'],
                                                                           ignore_absense=True)
        else:
            option = self.get_intermediary_PartyB_option()
            intermediary_option = get_SIA_party_intermediary_option(self.acm_obj, 'B', option)

        if intermediary_option == "A":
            return 'intermediary_PartyB_56A'
        elif intermediary_option == "D":
            return 'intermediary_PartyB_56D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (
                self.swift_message_type, str(intermediary_option), 'Intermediary_PartyB_56a'))
            return 'intermediary_PartyB_56A'

    #getter
    def intermediary_PartyB_56A(self):
        """
        Getter function for intermediary_PartyB_56A
        :return:
        """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_B_INTERMEDIARY_BIC'], ignore_absense=True)
        else:
            account = get_SIA_party_intermediary_account(self.acm_obj, 'B')
            bic = get_SIA_party_intermediary_bic(self.acm_obj, 'B')

        values_dict['account'] = account
        values_dict['bic'] = bic
        return values_dict

    #formatter
    def _format_intermediary_PartyB_56A(self, val):
        """
        Formatter function for intermediary_PartyB_56A
        :param val:
        :return:
        """
        account = val.get('account')
        bic = val.get('bic')
        if bic:
            field_value = str(bic)
            if account:
                field_value = "/" + str(account) + "\n" + str(field_value)
            return field_value


    #validator
    @validate_with(MT320.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56A_Type)
    def _validate_intermediary_PartyB_56A(self, val):
        """
        Validator function for intermediary_PartyB_56A
        :param val:
        :return:
        """
        return val

    #setter
    def _setintermediary_PartyB_56A(self, val):
        """
        Setter function for intermediary_PartyB_56A
        :param val:
        :return:
        """
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A.swiftTag = "56A"

    #getter
    def intermediary_PartyB_56D(self):
        """
        Getter function for intermediary_PartyB_56D
        :return:
        """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_INTERMEDIARY_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_INTERMEDIARY_NAME'],
                                                               ignore_absense=True)
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_INTERMEDIARY_ADDRESS'],
                                                               ignore_absense=True)
        else:
            account = get_SIA_party_intermediary_account(self.acm_obj, 'B')
            name = get_SIA_party_intermediary_name(self.acm_obj, 'B')
            address = get_SIA_party_intermediary_address(self.acm_obj, 'B')

        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    #formatter
    def _format_intermediary_PartyB_56D(self, val):
        """
        Formatter function for intermediary_PartyB_56D
        :param val:
        :return:
        """
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                field_value = "/" + str(account) + "\n" + str(val)
            return field_value

    #validator
    @validate_with(MT320.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_56D_Type)
    def _validate_intermediary_PartyB_56D(self, val):
        """
        Validator function for intermediary_PartyB_56D
        :param val:
        :return:
        """
        return val

    #setter
    def _setintermediary_PartyB_56D(self, val):
        """
        Setter function for intermediary_PartyB_56D
        :param val:
        :return:
        """
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_D = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_D.swiftTag = "56D"




    # option getter
    def get_receiving_agent_PartyB_option(self):
        """Returns default option if override is not provided"""
        option = 'A'
        return option

    #setter
    def _set_OPTION_receiving_agent_PartyB(self):
        """
        This function selects the option for receiving_agent_PartyB
        :return:
        """
        if self.use_operations_xml:
            buy_receiving_agent_option = FSwiftWriterUtils.get_value_from_xml_tag(
                self.swift_metadata_xml_dom, ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_OPTION'])
        else:
            option = self.get_receiving_agent_PartyB_option()
            buy_receiving_agent_option = get_SIA_party_receiving_agent_option('B', self.acm_obj, self.swift_message_type, option)

        if buy_receiving_agent_option == "A":
            return 'receiving_agent_PartyB_57A'
        elif buy_receiving_agent_option == "D":
            return 'receiving_agent_PartyB_57D'
        else:
            notifier.WARN("%s Option %s is not supported for tag %s. Mapping default option." % (self.swift_message_type, str(buy_receiving_agent_option), 'Receiving_agent_PartyB_57a'))
            return 'receiving_agent_PartyB_57A'

    #getter
    # Moved to FLoanDepositOutBase


    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57A_Type)
    def _validate_receiving_agent_PartyB_57A(self, val):
        """
        Validator function for receiving_agent_PartyB_57A
        :param val:
        :return:
        """
        return val

    #setter
    def _setreceiving_agent_PartyB_57A(self, val):
        """
        Setter function for receiving_agent_PartyB_57A
        :param val:
        :return:
        """
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_A.swiftTag = "57A"

    #getter
    # Moved to FLoanDepositOutBase

    #formatter
    # Moved to FLoanDepositOutBase

    #validator
    @validate_with(MT320.MT320_SequenceD_SettlementInstructionsforAmountsPayablebyPartyB_57D_Type)
    def _validate_receiving_agent_PartyB_57D(self, val):
        """
        Validator function for receiving_agent_PartyB_57D
        :param val:
        :return:
        """
        return val

    #setter
    def _setreceiving_agent_PartyB_57D(self, val):
        """
        Setter function for receiving_agent_PartyB_57D
        :param val:
        :return:
        """
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_D = val
        self.swift_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.ReceivingAgent_D.swiftTag = "57D"


class FMT320OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom = None):
        self.mt_typ = "320"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.use_operations_xml = should_use_operations_xml('MT'+ self.mt_typ)
        super(FMT320OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        """
        Function returns message type
        :return:
        """
        return "320"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
        senders_bic = ''
        if self.use_operations_xml:
            senders_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'SENDER_BIC'])
        else:
            senders_bic = get_senders_bic(self.acm_obj)

        if not senders_bic:
            raise Exception("SENDER_BIC is a mandatory field for Swift message header")
        terminal_address = self.logical_terminal_address(senders_bic, "A")
        return terminal_address

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        terminal_address = ''
        receivers_bic = ''
        if self.use_operations_xml:
            receivers_bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'RECEIVER_BIC'])
        else:
            receivers_bic = get_receivers_bic(self.acm_obj)
        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address

    def logical_terminal_address(self, bic_code, lt_code):
        """
        Function returns logical terminal address
        :param bic_code:
        :param lt_code:
        :return:
        """
        terminal_address = ""
        branch_code = "XXX"
        if bic_code:
            if len(str(bic_code)) == 8:
                terminal_address = str(bic_code) + lt_code + branch_code
            elif len(str(bic_code)) == 11:
                branch_code = bic_code[8:]
                terminal_address = str(bic_code[:8]) + lt_code + branch_code
            else:
                raise Exception("Invalid BIC <%s>)" % bic_code)
        return terminal_address

    def input_or_output(self):
        """
        Function returns input or output
        :return:
        """
        return "I"

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of confirmation-VersionID'''

        if self.use_operations_xml:
            seqnbr = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['CONFIRMATION', 'SEQNBR'])
        else:
            seqnbr = self.acm_obj.Oid()

        return "{108:%s-%s-%s}" % (get_confirmation_reference_prefix(), seqnbr, get_message_version_number(self.acm_obj))


class FMT320OutBaseNetworkRules(object):
    def __init__(self, swift_message_obj, swift_message, acm_obj):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.acm_obj = acm_obj

    def network_rule_C1(self):
        '''In sequence A, the presence of field 21 depends on field 22A and 22B
            Sequence A if field 22B is ...   Sequence A then field 22A is ...    Sequence A then field 21 is ...
            CONF                                NEWT                            Optional
            CONF                                Not NEWT                        Mandatory
            Not CONF                            Any value                       Mandatory'''
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'CONF':
            if not self.swift_message_obj.SequenceA_GeneralInformation.TypeOfOperation.value() == 'NEWT':
                if not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference or not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference.value():
                    return "Field 21 in Sequence A is mandatory if field 22A in Sequence A is not equal to NEWT and field 22B in Sequence A is equal to CONF"
        if not self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'CONF':
            if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfOperation.value():
                if not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference or not self.swift_message_obj.SequenceA_GeneralInformation.RelatedReference.value():
                    return "Field 21 in Sequence A is mandatory if field 22A in Sequence A has any value and field 22B in Sequence A is not equal to CONF"
        return ''

    """def network_rule_C2(self):
        '''In sequence A, if field 94A is present and contains AGNT, then field 21N is mandatory, otherwise field 21N is optional  (Error code(s): D72)
            Sequence A if field 94A is ...   Sequence A then field 21N is ...
            AGNT                                Mandatory
            BILA                                Optional
            BROK                                Optional
            Not Present                         Optional'''
        if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'AGNT':
            if not self.swift_message_obj.SequenceA_GeneralInformation.ContractNumberPartyA or not self.swift_message_obj.SequenceA_GeneralInformation.ContractNumberPartyA.value():
                return "Field 21N in Sequence A is mandatory if field 94A in Sequence A is equal to AGNT"
        return ''"""

    def network_rule_C3(self):
        '''In sequence B, the presence of fields 32H and 30X depends on the value of field 22B in sequence A as follows  (Error code(s): D56)
            Sequence A if field 22B is ...   Sequence B then field 32H..   Sequence B then field 30X is ...
            CONF                                Not Allowed                 Mandatory
            MATU                                Mandatory                   Not Allowed
            ROLL                                Mandatory                   Mandatory'''
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'CONF':
            if (
                self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled and self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled.value()) \
                    or (
                        not self.swift_message_obj.SequenceB_TransactionDetails.NextInterestDueDate or not self.swift_message_obj.SequenceB_TransactionDetails.NextInterestDueDate.value()):
                return "Field 30X in Sequence B is mandatory and Field 32H in Sequence B is not allowed if field 22B in Sequence A is equal to CONF"
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'MATU':
            if (
                not self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled or not self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled.value()) \
                    or (
                        self.swift_message_obj.SequenceB_TransactionDetails.NextInterestDueDate and self.swift_message_obj.SequenceB_TransactionDetails.NextInterestDueDate.value()):
                return "Field 30X in Sequence B is not allowed and Field 32H in Sequence B is mandatory if field 22B in Sequence A is equal to MATU"
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'ROLL':
            if (
                not self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled or not self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled.value()) \
                    or (
                        not self.swift_message_obj.SequenceB_TransactionDetails.NextInterestDueDate or not self.swift_message_obj.SequenceB_TransactionDetails.NextInterestDueDate.value()):
                return "Field 30X and Field 32H in Sequence B are Mandatory if field 22B in Sequence A is equal to ROLL"
        return ''

    def network_rule_C4(self):
        '''In sequence B, the values allowed for subfield 3 of field 32H (if present) depend on the values of fields 22B in sequence A and 17R in sequence B as follows  (Error code(s): D57)
            Sequence A if field 22B is.. Sequence B then field 17R is.. Sequence B then subfield 3 of field 32H must be ...
            MATU                                L                       Negative or zero (*)
            MATU                                B                       Positive or zero (*)
            Not MATU                            Not applicable          Not applicable
            (*) The presence of the letter N (sign) in subfield 1 of field 32H specifies a negative amount.
            The absence of the letter N (sign) in subfield 1 of field 32H specifies a positive amount.
            If the value in subfield 3 of field 32H is zero, then the letter N (sign) in subfield 1 of field 32H is not allowed  (Error code(s): T14).'''
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'MATU':
            AmountToBeSettled = float(get_amount_from_currency_amount(
                self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled.value()))
            if not self.swift_message_obj.SequenceB_TransactionDetails.PartyAsRole.value() == 'B':
                if AmountToBeSettled > 0:
                    return "Field 32H in Sequence B must be Negative or zero"
            if not self.swift_message_obj.SequenceB_TransactionDetails.PartyAsRole.value() == 'L':
                if AmountToBeSettled < 0:
                    return "Field 32H in Sequence B must be Positive or zero"

    def network_rule_C9(self):
        """The currency code in the amount fields 32B, 32H and 34E in sequence B, and field 71F in sequence H must be the same  (Error code(s): C02)."""
        CurrencyAndPrincipalAmount = AmountToBeSettled = CurrencyAndInterestAmount = ''

        if self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndPrincipalAmount:
            CurrencyAndPrincipalAmount = get_currency_from_currency_amount(self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndPrincipalAmount.value())
        if self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled:
            AmountToBeSettled = get_currency_from_currency_amount(self.swift_message_obj.SequenceB_TransactionDetails.AmountToBeSettled.value())
        if self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount:
            CurrencyAndInterestAmount = get_currency_from_currency_amount(self.swift_message_obj.SequenceB_TransactionDetails.CurrencyAndInterestAmount.value())
        # BrokersCommission = get_currency_from_currency_amount(self.swift_message_obj.ADDINFO.BrokersCommission.value())
        unique_values = set([CurrencyAndPrincipalAmount, AmountToBeSettled, CurrencyAndInterestAmount])
        unique_values.discard('')
        if len(unique_values) > 1:
            return "Currency code in the amount fields 32B, 32H and 34E in sequence B, and field 71F in sequence H must be the same"
        return ''

    """def network_rule_C5(self):
        '''In sequence A, if field 22B contains MATU, then field 30F in sequence B is not allowed, otherwise field 30F is optional  (Error code(s): D69)
            Sequence A if field 22B is ...   Sequence B then field 30F is ...
            MATU                                Not Allowed
            Not MATU                            Optional'''
        if self.swift_message_obj.SequenceA_GeneralInformation.TypeOfEvent.value() == 'MATU':
            if not self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheFirstInterestPeriod or not self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheFirstInterestPeriod.value():
                return "Field 30F in Sequence B is not allowed if field 22B in Sequence A is MATU"
        return ''

    def network_rule_C6(self):
        '''In sequence B, if field 30F is present then field 38J is mandatory, otherwise field 38J is not allowed  (Error code(s): D60)
            Sequence B if field 30F is ...   Sequence B then field 38J is ...
            Present                                Mandatory
            Not Present                            Not Allowed'''
        if self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheFirstInterestPeriod or self.swift_message_obj.SequenceB_TransactionDetails.LastDayOfTheFirstInterestPeriod.value():
            if not self.swift_message_obj.SequenceB_TransactionDetails.NumberOfDays or not self.swift_message_obj.SequenceB_TransactionDetails.NumberOfDays.value():
                return "Field 38J in Sequence B is mandatory if field 30F in Sequence B is present"
        return ''

    def network_rule_C7(self):
        '''In sequences C, D, E (if present), F (if present) and I (if present), if field 56a is not present, then field 86a in the same sequence C, D, E, F or I is not allowed,
            otherwise field 86a is optional  (Error code(s): E35)
            Sequence C,D,E,F,I if field 56a is ...   Sequence C,D,E,F,I then field 86a is ...
            Not Present                                 Not Allowed
            Present                                     Optional'''
        if not self.swift_message_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A or not self.swift_message_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary_A.value():
            if self.swift_message_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary2_A and self.swift_message_obj.SequenceC_SettlementInstructionsforAmountsPayablebyPartyA.Intermediary2_A.value():
                return "Field 86a in Sequence C is not allowed if field 56a in Sequence C is not present"
        return ''
        if not self.swift_message_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A or not self.swift_message_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary_A.value():
            if self.swift_message_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary2_A and self.swift_message_obj.SequenceD_SettlementInstructionsforAmountsPayablebyPartyB.Intermediary2_A.value():
                return "Field 86a in Sequence D is not allowed if field 56a in Sequence D is not present"
        return ''

    def network_rule_C8(self):
        '''The presence of sequence H and the presence of fields 88a and 71F in sequence H, depends on the value of field 94A in sequence A as follows  (Error code(s): D74):
            Sequence A if field 94A is ...   Then sequence H is ...     Sequence H and field 88a is ...     Sequence H and field 71F is ...
            Not Present                      Optional                    Optional                            Not Allowed
            AGNT                             Optional                    Optional                            Not Allowed
            BILA                             Optional                    Optional                            Not Allowed
            BROK                             Mandatory                   Mandatory                           Optional'''
        if self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'BROK':
            if not self.swift_message_obj.ADDINFO.BrokerIdentification_A or not self.swift_message_obj.ADDINFO.BrokerIdentification_A.value():
                return "Field 88a in Sequence H is mandatory if field 94A in Sequence A is BROK"
        if not self.swift_message_obj.SequenceA_GeneralInformation.ScopeOfOperation.value() == 'BROK':
            if self.swift_message_obj.ADDINFO.BrokersCommission and self.swift_message_obj.ADDINFO.BrokersCommission.value():
                return "Field 71F in Sequence H is not allowed if field 94A in Sequence A is not BROK "
        return ''

    def network_rule_C10(self):
        '''In sequence H, if field 15H is present, then at least one of the other fields of sequence H must be present  (Error code(s): C98).'''
        return ''

    def network_rule_C11(self):
        '''In all optional sequences, the fields with status M must be present if the sequence is present, and are otherwise not allowed  (Error code(s): C32).'''
        return ''
    """


