"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterUtils

DESCRIPTION:
    ENCRYPTED EXTENSION MODULE
    This module defines the APIs and helper functions common to the SwiftWriter framework.

VERSION: %R%

RESTRICTIONS/LIMITATIONS:
                1. Any modifications to the script/encryted module/clear text code within the core is not supported.
                2. This module is not customizable.
                3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import amb
import time
import acm
import ael
import tempfile
import os
import inspect
import xml.dom.minidom as dom
import xml
import hashlib
import FUxCore
import datetime
import FSwiftWriterHooks
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SwiftWriter', 'FSwiftWriterNotifyConfig')
import FSwiftWriterMTFactory
import FSwiftML
import FSwiftMLUtils
from FConfirmationXML import FConfirmationXML
from FSettlementXML import FSettlementXML
import pyxb
import ast
import re
import FSwiftWriterMessageHeader
from FValidation_core import show_validation_warning
try:
    import FSwiftOperationsAPI
except Exception, e:
    pass
import FSwiftViewerGui
from FSwiftWriterEngine import SwiftWriterEngine, should_use_operations_xml
from FSwiftServiceSelector import bypass_Swift_Solutions, is_unsupported_settlement, was_previously_released_by_adaptiv

from FExternalObject import FExternalObject
# from FConfirmationEnums import ConfirmationType
try:  # for MXRTS22 the released swiftwriter version and ads version could be older than 18.2
    ConfirmationType = FSwiftOperationsAPI.GetConfirmationTypeEnum()
except:
    pass

try:
    # from FSettlementEnums import RelationType, SettlementStatus
    RelationType = FSwiftOperationsAPI.GetRelationTypeEnum()
    SettlementStatus = FSwiftOperationsAPI.GetSettlementStatusEnum()
    DocumentStatus = FSwiftOperationsAPI.GetOperationsDocumentStatusEnum()
except:
    pass

def update_params_dict(fparams_dict, to_add_dict):
    """ add elements to the fparam dict
    :param fparams_dict: current fparam dict
    :param to_add_dict: dict to add new elements to fparam_dict
    :return: dict: updated dict

    """
    new_dict = dict(fparams_dict)
    if to_add_dict:
        new_dict.update(to_add_dict)
    return new_dict

pairing_view_fparams = {
    'AcmObjQuery': {'Mandatory': True},
    'LowerPanelAcmObjType': {'Mandatory': True},
    'LowerPanelName': {'Mandatory': True},
    'LowerPanelSheetTemplate': {'Mandatory': True},
    'LowerPanelSheetType': {'Mandatory': True},
    'UnpairedBPRQuery': {'Mandatory': True},
    'UpperPanelName': {'Mandatory': True},
    'UpperPanelSheetTemplate': {'Mandatory': True},
}
all_in_config_fparams = {
    'EligibilityQuery': {'Mandatory': True},
    'Match': {'Mandatory': True},
    'Pair': {'Mandatory': True},
    'PairingViewAcmObjColumns': {'Mandatory': True},
    'PairingViewAcmObjQuery': {'Mandatory': True},
    'PairingViewBPRColumns': {'Mandatory': True},
    'PairingViewBPRQuery': {'Mandatory': True},
    'StateChart': {'Mandatory': True},
    'UnpairedBPRQuery': {'Mandatory': True},
}

notifier_fparams = {
    'LogLevel': {'Mandatory': True, 'Default': 'INFO', 'possible_values': ['INFO', 'DEBUG', 'ERROR', 'WARN']},
        'NotificationLevel': {'Mandatory': True, 'Default': 'TRACK', 'possible_values': ['TRACK', 'DEBUG', 'WARNING', 'ERROR', 'SUCCESS']},
        'NotificationMedia': {'Mandatory': True, 'Default': 'OFF', 'possible_values': ['OFF', 'PRIME_LOG', 'PRIME_LOG_TRANSIENT']},
    'NotifyUser': {'Mandatory': False},
}

Fparameter_information_dict = {
    'FSecuritySettlementOut_Config': {
        'AutoAcknowledgeMessage': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'SaveCarbonCopySwift': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'AMBSenderSubject': {'Mandatory': True}, # For possible value  as  Any string do  not provide  'possible_values' key
        'SecuritySettlementOut_AMBReceiver': {'Mandatory': True},
        'CarbonCopySwiftPath': {'Mandatory': False}
    },
    'FSecuritySettlementOutGeneration_Config': {
        'FMT540_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT541_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT542_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT543_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
    },
    'FSecuritySettlementOutNotify_Config': notifier_fparams,
    'PairingView54X': {
        'Class': {'Mandatory': True},
        'Module': {'Mandatory': True}
    },
    'FMT54XInPairingView': pairing_view_fparams,
    'FSecuritySettlementInNotify_Config': notifier_fparams,
    'FMT54XIn_Config': {
        'PairingViewAcmObjColumns': {'Mandatory': True},
        'PairingViewAcmObjQuery': {'Mandatory': True},
        'PairingViewBPRColumns': {'Mandatory': True},
        'PairingViewBPRQuery': {'Mandatory': True},
        'SecuritySettlementIn_AMBReceiver': {'Mandatory': True},
        'TransferSettledAmountOperationName': {'Mandatory': True},
    },
    'FMT547In_Config': {
        'EligibilityQuery': {'Mandatory': True},
        'Match': {'Mandatory': True},
        'Pair': {'Mandatory': True},
        'RepoConfirmationsQuery': {'Mandatory': True},
        'RepoConfPair': {'Mandatory': True},
        'SecurityTransferQuery': {'Mandatory': True},
        'SettledAmountTransferQuery': {'Mandatory': True},
        'StateChart': {'Mandatory': True},
        'UnpairedBPRQuery': {'Mandatory': True},
    },
    'FMT546In_Config': {
        'EligibilityQuery': {'Mandatory': True},
        'Match': {'Mandatory': True},
        'Pair': {'Mandatory': True},
        'SecurityTransferQuery': {'Mandatory': True},
        'SettledAmountTransferQuery': {'Mandatory': True},
        'StateChart': {'Mandatory': True},
        'UnpairedBPRQuery': {'Mandatory': True},
    },
    'FMT545In_Config': {
        'EligibilityQuery': {'Mandatory': True},
        'Match': {'Mandatory': True},
        'Pair': {'Mandatory': True},
        'RepoConfirmationsQuery': {'Mandatory': True},
        'RepoConfPair': {'Mandatory': True},
        'SecurityTransferQuery': {'Mandatory': True},
        'SettledAmountTransferQuery': {'Mandatory': True},
        'StateChart': {'Mandatory': True},
        'UnpairedBPRQuery': {'Mandatory': True},
    },
    'FMT544In_Config': {
        'EligibilityQuery': {'Mandatory': True},
        'Match': {'Mandatory': True},
        'Pair': {'Mandatory': True},
        'SecurityTransferQuery': {'Mandatory': True},
        'SettledAmountTransferQuery': {'Mandatory': True},
        'StateChart': {'Mandatory': True},
        'UnpairedBPRQuery': {'Mandatory': True},
    },
    'FIRDConfirmationInNotify_Config': notifier_fparams,
    'FMT361In_Config': all_in_config_fparams,
    'FMT361InPairingView': pairing_view_fparams,
    'FMT300In_Config': update_params_dict(all_in_config_fparams, {'FXMMConfirmationIn_AMBReceiver': {'Mandatory': True}}),
    'FMT300InPairingView': pairing_view_fparams,
    'FMT305In_Config': all_in_config_fparams,
    'FMT305InPairingView': pairing_view_fparams,
    'FMT320In_Config': update_params_dict(all_in_config_fparams, {'FXMMConfirmationIn_AMBReceiver': {'Mandatory': True}}),
    'FMT320InPairingView': pairing_view_fparams,
    'FMT330In_Config': update_params_dict(all_in_config_fparams, {'FXMMConfirmationIn_AMBReceiver': {'Mandatory': True}}),
    'FMT330InPairingView': pairing_view_fparams,
    'PairingView300': {
        'Class': {'Mandatory': False},
        'Module': {'Mandatory': False},
    },
    'PairingView305': {
        'Class': {'Mandatory': False},
        'Module': {'Mandatory': False},
    },
    'FMT564InPairingView': {
        'LowerPanelName': {'Mandatory': True},
        'UnpairedBPRQuery': {'Mandatory': True},
        'UpperPanelName': {'Mandatory': True},
        'UpperPanelSheetTemplate': {'Mandatory': True},
    },
    'FMT564In_Config': {
        'CorporateActionIn_AMBReceiver': {'Mandatory': True},
        'PairingViewBPRColumns': {'Mandatory': True},
        'StateChart': {'Mandatory': True},
        'UnpairedBPRQuery': {'Mandatory': True},
    },
    'FCorporateActionsInNotify_Config': notifier_fparams,
    'FCashOut_Config': {
        'AutoAcknowledgeMessage': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'SaveCarbonCopySwift': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'AMBSenderSubject': {'Mandatory': True}, # For possible value  as  Any string do  not provide  'possible_values' key
        'CashOut_AMBReceiver': {'Mandatory': True},
        'CarbonCopySwiftPath': {'Mandatory': False},
        'NationalClearingSystem': {'Mandatory': False, 'type': dict, 'Default': {'Fedwire': None}},
        'BankingPriority': {'Mandatory': True},
        'SubNetwork': {'Mandatory': True},
        'SwiftServiceCode': {'Mandatory': True}
    },
    'FCashOutGeneration_Config': {
        'FMT103_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT192_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT199_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT200_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT202_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT292_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT299_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT304_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']}
    },
    'FCashOutNotify_Config': notifier_fparams,
    'FFXMMConfirmationOut_Config': {
        'AutoAcknowledgeMessage': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'SaveCarbonCopySwift': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'AMBSenderSubject': {'Mandatory': True}, # For possible value  as  Any string do  not provide  'possible_values' key
        'FXMMConfirmationOut_AMBReceiver': {'Mandatory': True},
        'CarbonCopySwiftPath': {'Mandatory': False},
        'MTChaserFields': {'Mandatory': True, 'type': dict},
        'LocationCode': {'Mandatory': True, 'type': dict},
    },
    'FFXMMConfirmationOutGeneration_Config': {
        'FMT300_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT305_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT306_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT320_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT330_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT395_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
    },
    'FFXMMConfirmationOutNotify_Config': notifier_fparams,
    'FIRDConfirmationOut_Config': {
        'AutoAcknowledgeMessage': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'SaveCarbonCopySwift': {'Mandatory': False, 'Default': False, 'possible_values': ['True', 'False']},
        'AMBSenderSubject': {'Mandatory': True},
        'IRDConfirmationOut_AMBReceiver': {'Mandatory': True},
        'CarbonCopySwiftPath': {'Mandatory': False},
        'MTChaserFields': {'Mandatory': True, 'type': dict},
        'LocationCode': {'Mandatory': True, 'type': dict},
    },
    'FIRDConfirmationOutGeneration_Config': {
        'FMT360_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT361_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT362_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
        'FMT395_GenerationOn': {'Mandatory': False, 'Default': True, 'possible_values': ['True', 'False']},
    },
    'FIRDConfirmationOutNotify_Config': notifier_fparams,
    'FSwiftWriterAMBConfig': {
        'AMBSender': {'Mandatory': True},
    },
    'FSwiftSolutionConfig': {
        'AMBAddress': {'Mandatory': True},
        'AMBASenderSource': {'Mandatory': True},
    },
    'FSwiftWriterConfig': {
        'AckNakSubject': {'Mandatory': True, 'Default': 'ACKNOWLEDGEMENT'},
        'FAC': {'Mandatory': True},
        'FAS': {'Mandatory': True},
        'LAU_Key': {'Mandatory': False},
        'Modules': {'Mandatory': True, 'type': list},
        'ReceiverBICLoopBack': {'Mandatory': False},
        'RoundPerCurrency': {'Mandatory': False, 'type': dict},
        'SenderBICLoopBack': {'Mandatory': False},
        'Separator': {'Mandatory': False},
        'SwiftLoopBack': {'Mandatory': False},
        'UsePartyFullName': {'Mandatory': False},
    },
    'FSwiftWriterNotifyConfig': notifier_fparams,

}
extended_x_char = {60:'<',33:'!',38:'&',124:'|',36:'$',42:'*',59:';',94:'^',37:'%',95:'_',62:'>',96:'`',35:'#',64:'@',61:'=',34:'"',126:'~',91:'[',93:']',123:'{',125:'}', 92:'\\'}
extended_x_char_translation = {'<': '4C', '!': '4F', '&': '50', '|': '5A', '$': '5B', '*': '5C', ';': '5E', '^': '5F', '%': '6C', '_': '6D', '>': '6E', '`': '79', '#': '7B', '@': '7C', '=': '7E', '"': '7F', '~': 'A1', '[': 'AD', ']': 'BD', '{': 'C0', '}': 'D0', '\\': 'E0'}
extended_x_char_rev_translation = {'??BD': ']', '??5E': ';', '??5F': '^', '??5A': '|', '??5C': '*', '??5B': '$', '??7F': '"', '??7E': '=', '??7C': '@', '??7B': '#', '??A1': '~', '??C0': '{', '??E0': '\\', '??AD': '[', '??4F': '!', '??4C': '<', '??79': '`', '??6C': '%', '??6D': '_', '??6E': '>', '??50': '&', '??D0': '}'}




def get_related_settlement(settlement):
    '''
    Method to get the related settlement
    :param settlement:
    :return:
    '''
    if is_cancellation(settlement):
        return settlement.Children()[0]
    elif is_nak_cancellation(settlement):
        return settlement
    return None


def is_cancellation(settlement):
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        return settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT]
    else:
        return settlement.RelationType() in ['Cancellation', 'Cancel Correct']


def is_nak_cancellation(settlement):
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        return settlement.Status() == SettlementStatus.PENDING_CANCELLATION
    else:
        return settlement.Status() == 'Pending Cancellation'


"""------------------------------------------------new addition ------------------------------"""


def get_mt_type_from_acm_obj(acm_obj):
    """
    This API returns the Swift message type for provided acm object
    """
    try:
        return FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj)
    except Exception, e:
        notifier.ERROR("Error in calculating message type for %s:%s %s" % (str(type(acm_obj)), str(acm_obj.Oid()), str(e)))
        notifier.DEBUG(str(e), exc_info=1)
        raise Exception(e)

def swift_format_of_message(mt_type):
    """
    This function returns MT/MX depending on the input message type
    input: mt_type e.g. 202, MT103
    output: MT or MX or None
    """
    mt_type = str(mt_type)

    if re.match(r"^(MT){0,1}\d{3}(COV){0,1}$", mt_type) is not None:
        # Starts optionally with MT. Followed by 3 digits. Ends optionally with COV.
        return 'MT'
    elif re.match(r"^[a-zA-Z]{4}[a-zA-Z0-9]{3}\d{3}\d{2}$",mt_type):
        # Starts with 4 character string. Followed by alphanumeric string of length 3.
        # Followed by 3 digits. Followed by 2 digits.
        return 'MX'
    else:
        return 'MT'

def get_applicable_message_list(acm_object, input_mt_type):
    """
        Input
        Message type as string and confirmation or settlement object.

        Output:
            Returns list of messages belonging to a particular mt type
    """
    confirmation_package_calculators = ['FSwiftCustomMessageCalculator','FCommodityCalculator',
                                        'FFXMMConfirmationCalculator', 'FIRDConfirmationCalculator',
                                        'FCashSettlementCalculator', 'FSecuritySettlementCalculator']
    import FIntegrationUtils
    utils_obj = FIntegrationUtils.FIntegrationUtils()
    messageType = []
    for pkg_calc in confirmation_package_calculators:
        try:
            module = utils_obj.import_module_from_string(pkg_calc)
            mt_type = module.get_applicable_mt_type(acm_object, input_mt_type)
            if mt_type:
                messageType = mt_type
                break
        except ImportError:
            # If package is not installed, ignore it.
            pass
    return messageType

def allocate_space_for_n_lines(n, lines):
    """
    This api will allocate space for n_lines from the input provided
    """
    text = lines[:n]
    value = ('\n').join(text)
    return value


def allocate_space_for_name_address_without_constraint(name=[], address=[]):
    """
    This api does following:
        Step1: Allocates number of lines based on the prefix
        Step2: Takes required data from corresponding lists as per allocated space
    """
    str_with_prefix_1_len = len(name)
    space_for_1, space_for_2 = min(4, str_with_prefix_1_len), 4 - min(4, str_with_prefix_1_len)
    field_value = name[:space_for_1] + address[:space_for_2]
    name_address = ('\n').join(field_value)
    return name_address


def allocate_space_for_name_and_address_with_constraint(name=[], address=[], address_details=[]):
    """
    This api does following:
        Step1: Allocates number of lines based on the prefix
        Step2: Takes required data from corresponding lists as per allocated space
    """
    str_prefix_1_len = len(name)
    str_prefix_2_len = len(address)
    str_prefix_3_len = len(address_details)
    space_for_1, space_for_2, space_for_3 = 0, 0, 0
    if str_prefix_1_len >= 1:
        # Condition: Number 2 must not be used without number 3
        if str_prefix_2_len >= 1 and str_prefix_3_len >= 1:
            # Numbers must appear in numerical order
            if str_prefix_1_len > 1:
                space_for_1 = str_prefix_1_len  # Condition:The first line must start with number 1
                rem_space = 4 - space_for_1
                if rem_space == 2:
                    space_for_2, space_for_3 = 1, 1
                else:
                    space_for_2, space_for_3 = 0, 1
            else:
                space_for_1, space_for_2 = 1, min(str_prefix_2_len, 2)
                space_for_3 = 3 - space_for_2
        else:
            space_for_1, space_for_2, space_for_3 = min(4, str_prefix_1_len), 0, 4 - min(4, str_prefix_1_len)
    field_value = name[:space_for_1] + address[:space_for_2] + address_details[:space_for_3]
    name_address = ('\n').join(field_value)
    return name_address


def split_text_on_character_limit(field_content, character_limit):
    """
    This api is used to split the content based on character limit
    :param self:
    :param field_content: Content to be split
    :param character_limit: Max characters that can be accomodated on single line
    :return: list containing field_content broken down on character limit
    """
    return [field_content[i:i + character_limit] for i in range(0, len(field_content), character_limit)]


def split_text_and_prefix(field_text, character_limit=0, prefix=''):
    """
    This api calls 'split_text_on_character_limit api' and 'prefix_lines_with api'
    """
    splitted_lines = split_text_on_character_limit(field_text, character_limit)
    prefixed_text = prefix_lines_with(splitted_lines, prefix)
    return prefixed_text


def split_text_logically_and_prefix(field_text, character_limit=0, prefix=''):
    """
    This api calls 'split_text_on_character_limit api' and 'prefix_lines_with api'
    """
    splitted_lines = split_text_logically_on_character_limit(field_text, character_limit)
    prefixed_text = prefix_lines_with(splitted_lines, prefix)
    return prefixed_text


def split_text_logically_on_character_limit(text, character_limit):
    """
   This api will split text based on character_limit provided as input
    """
    text_lines = []
    if text:
        text_list = text.split(' ')
        temp_text = ''
        old_temp_text = ''
        for text in text_list:
            old_temp_text = temp_text
            temp_text += text + ' '
            if len(temp_text) > character_limit + 1:
                text = text + ' '
                old_temp_text = old_temp_text.rstrip()
                text_lines.append(old_temp_text)
                old_temp_text = ''
                temp_text = text
        temp_text = temp_text.rstrip()
        text_lines.append(temp_text)
    return text_lines


def prefix_lines_with(lines, prefix):
    """
    This api will add prefix to input
    """
    prefixed_text = []
    for text in lines:
        text = prefix + text
        prefixed_text.append(text)
    return prefixed_text


def format_date(date, date_format):
    y, m, d = acm.Time.DateToYMD(date)
    date_obj = datetime.date(y, m, d)
    return date_obj.strftime(date_format)

def is_viewer_supported(object_list):
    is_viewer_supported = True
    for object in object_list:
        msg_type = ''
        if isinstance(object,str):
            msg_type = object
        elif object.IsKindOf(acm.FExternalObject):
            msg_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(object)

        if swift_format_of_message(msg_type) == 'MX':
            is_viewer_supported = False
            break
    return is_viewer_supported

def get_external_value_using_ael(recon_item):
    """ Get external values stored using ael as with acm version compatibility issue"""
    externalValuesEncoded = recon_item.external_values
    archive = acm.FXmlArchive()
    archive.Load(externalValuesEncoded)
    externalValues = archive.Contents()
    if externalValues and externalValues.At('externalValues'):
        externalValues = externalValues.At('externalValues')
    return externalValues


def get_issuer_bic(acm_obj):
    bic = ''
    bic = acm_obj.Swift()

    return bic


def validate_network_rules(mt_type, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom=None):
    """ Validate network rules for swift message object """
    notifier.DEBUG("{0} Validating network rules".format(mt_type))
    fmt_network_rules_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_network_rules_object(mt_type, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)
    network_rules = [rule for rule in dir(fmt_network_rules_class_obj) if rule.startswith('network_rule_')]
    failed_rules_dict = {}
    success_rules = []
    validation_result = []
    validation_failed = False
    # Sorting based on network rule number, so taking last part of the method name only which should contain digits
    try:
        sorted_network_rules = sorted(network_rules, key=lambda network_rule_number: int(network_rule_number[14:]))
    except Exception, e:
        notifier.WARN("%s Could not sort network rule names for message type %s: %s" % (str(mt_type), str(mt_type), str(e)))
        sorted_network_rules = network_rules

    for rule in sorted_network_rules:
        rule_python_method = getattr(fmt_network_rules_class_obj, rule)
        if inspect.ismethod(rule_python_method):
            res = getattr(fmt_network_rules_class_obj, rule)()
            if res:
                failed_rules_dict[rule] = res
            else:
                success_rules.append(rule)

    for rule in failed_rules_dict:
        validation_failed = True
        result = '%s Failed Network validation Rule %s : %s' % (mt_type, rule.lstrip('network_rule_'), failed_rules_dict[rule])
        notifier.ERROR(result)
        validation_result.append(result)

    for rule in success_rules:
        result = '%s Successfully validated Network Rule %s ' % (mt_type, rule.lstrip('network_rule_'))
        notifier.INFO(result)
        validation_result.append(result)

    validation_rules_dict = format_failed_rules_dict(failed_rules_dict)
    return validation_result, validation_failed, validation_rules_dict


def format_failed_rules_dict(failed_rules_dict):
    """ Format failed rules dict """
    if failed_rules_dict:
        failed_rules_list = []
        for key in failed_rules_dict:
            element = key + ':' + failed_rules_dict[key]
            failed_rules_list.append(element)
        counter = 1
        failed_rules_dict = {}
        for each in failed_rules_list:
            Error_str = 'Error' + str(counter)
            failed_rules_dict[Error_str] = each
            counter += 1
    else:
        failed_rules_dict['Result'] = 'Successfully validated all Network Rules'
    return failed_rules_dict


def generate_python_object(acm_obj, mt_type, swift_metadata_xml_dom=None):
    """ Generates python object """
    pyxb.RequireValidWhenGenerating(True)

    updated_mt_py_obj = None
    notifier.DEBUG("{0} Generating SWIFT python object with mappings".format(mt_type))

    child_mt_type = ''
    split_data = str(mt_type).split('-')
    msg_type = split_data[0]
    if len(split_data) > 1:
        child_mt_type = split_data[1]

    # get FMT class based on mt_type for swift tags mapping
    fmt_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_object(acm_obj, msg_type,
                                                                                  swift_metadata_xml_dom)
    if child_mt_type:
        fmt_class_obj.set_child_mt_type('MT' + child_mt_type)


    # If at all we get fmt_class_obj as None then we need to raise exception.
    # In all other error cases we are raising error directly from create_fmt_object
    if not fmt_class_obj:
        if getattr(acm_obj, 'RecordType', None):
            raise Exception('Failure in generating swift message type %s for %s:%s.' % (str(msg_type), \
                                                                                        str(acm_obj.RecordType()),
                                                                                        str(acm_obj.Oid())))
        else:
            raise Exception('Failure in generating swift message type %s for %s:%s.' % (str(msg_type), \
                                                                                        str(type(acm_obj)),
                                                                                        str(acm_obj)))

    if acm_obj.RecordType() == 'Confirmation' and acm_obj.Type() == 'Cancellation':
        swift_message = FSwiftMLUtils.get_outgoing_mt_message(acm_obj.ConfirmationReference())
        canc_message, updated_mt_py_obj = fmt_class_obj.handle_cancellation_message(swift_message, msg_type, acm_obj)
        getter_values = None
        exceptions_in_mapping = None

    elif acm_obj.RecordType() == 'Settlement' and acm_obj.RelationType() == 'Cancellation' and mt_type == 'MT304':
            swift_message = FSwiftMLUtils.get_outgoing_mt_message(get_related_settlement(acm_obj))

            canc_message, updated_mt_py_obj = fmt_class_obj.handle_cancellation_message(swift_message, mt_type, acm_obj)

            getter_values = None
            exceptions_in_mapping = None
    else:
        # Create Engine Object by passing fmt_class_obj to it. Engine will map all the attributes.
        engine_object = SwiftWriterEngine(fmt_class_obj)
        engine_object.map_attributes()

        exceptions_in_mapping = engine_object._attribute_exception_dict()
        if not exceptions_in_mapping:
            exceptions_in_fmt_init = fmt_class_obj.exception_dict
            exceptions_in_mapping = exceptions_in_fmt_init
        getter_values = engine_object.get_getter_value_dict()
        if hasattr(fmt_class_obj, 'get_user_data'):
            getter_values['user_data'] = fmt_class_obj.get_user_data()

        if exceptions_in_mapping:
            exception_str = exceptions_as_string(exceptions_in_mapping)
            if exception_str:
                notifier.ERROR("%s Exceptions in setting attributes : \n%s" % (msg_type, str(exception_str)))

        if engine_object._swift_python_object() and 'GENERATIONFAILED' not in exceptions_in_mapping:
            mt_swift_py_obj = engine_object._swift_python_object()
            notifier.DEBUG("%s SWIFT python obj from MT class = %s" % (msg_type, str(mt_swift_py_obj)))
            # call export exit hook for user customizations
            updated_mt_py_obj = FSwiftWriterHooks.export_exit_hook(acm_obj, mt_swift_py_obj)
            notifier.DEBUG("%s SWIFT python obj after export exit hook = %s" % (msg_type, str(updated_mt_py_obj)))

    return updated_mt_py_obj, exceptions_in_mapping, getter_values

def validate_outgoing_swift_msg(swift_msg_before, swift_msg_after):
    """
    :param swift_msg_before:
    :param swift_msg_after:
    :return None if swift_msg_after is successfully pyxb validated. Raise exception if not pyxb validated along with error msg.
    """
    try:
        mlobj = FSwiftML.FSwiftML()
        xml = mlobj.swift_to_xml(str(swift_msg_after))
        py_obj = mlobj.xml_to_pyobject(xml)
    except Exception, e:
        notifier.ERROR("Exception in validate_outgoing_swift_msg: %s", str(e))
        diff_tuples_list = list()
        for line1, line2 in zip(str(swift_msg_before).splitlines(), str(swift_msg_after).splitlines()):
            if line1 == line2:
                continue
            else:
                diff_tuples_list.append((line1, line2))
        if diff_tuples_list:
            error_msg = '\nModifications performed in FSwiftWriterHooks.message_exit_hook failed message validation\n'
            error_msg = error_msg + 'Following lines are modified in message_exit_hook:\n'
            for item1, item2 in diff_tuples_list:
                error_msg = error_msg + 'Before' + str(item1) + '\tAfter' + str(item2) + '\n'
            raise Exception(error_msg)


def validate_use_of_extended_x_char_for_counterparty(mt_message):
    """ Now we have to check the destination address (i.e bic) from the header of msg to check
     if destination party (fetched using bic from destination address) does not have value of SWIFTExtXChrNotUsed=True
     if SWIFTExtXChrNotUsed=True then no extended X char are allowed in msg, i.e we have to check for escape sequences in msg """
    mt_type = ''
    bic_list = []
    error_str = ''
    destinationParty = None
    destinationAddress = None

    def CheckBackOfcObject(acm_obj):
        backOfcObj = None
        for extObj in acm_obj.ExternalObjects():
            if extObj.IntegrationType() == 'SwiftWriter' and extObj.IntegrationSubtype():
                mt_type_from_ext_obj = extObj.IntegrationSubtype()
                if (mt_type in mt_type_from_ext_obj) or (mt_type[0] == mt_type_from_ext_obj[2]):  # MT299 and MT202
                    backOfcObj = acm_obj
        return backOfcObj

    if mt_message:
        mt_message = str(mt_message)
        sendersAddress = re.findall(r'''{1:F\d{2}(\w+)}''', mt_message)  # from block2 of mt_message
        sendersAddress = sendersAddress[0]
        destinationMsgDetails = re.findall(r'''{2:[a-zA-Z](\d{3})(\w+)}''', mt_message)  # from block2 of mt_message
        mt_type, destinationAddress = destinationMsgDetails[0]

        for bic_name, address in [('sendersBic', sendersAddress), ('destination_bic', destinationAddress)]:
            bic = (address)[:8]
            branch_code = (address)[9:12]
            if branch_code != 'XXX':
                bic = bic + branch_code
            bic_list.append(bic)

        acm_obj = None
        backOfcObj = None
        conf_or_sett = re.findall(r'''{108:[A-Z]+-(\d+).*}''', mt_message)
        if not backOfcObj and acm.FConfirmation[conf_or_sett[0]]:  # Confirmation
            acm_obj = acm.FConfirmation[conf_or_sett[0]]
            backOfcObj = CheckBackOfcObject(acm_obj)
        if not backOfcObj and acm.FSettlement[conf_or_sett[0]]:  # Settlement
            acm_obj = acm.FSettlement[conf_or_sett[0]]
            backOfcObj = CheckBackOfcObject(acm_obj)
        if not backOfcObj:
            return destinationParty, True, error_str

        if backOfcObj:
            # for settlements if the counterparty does not belong to TARGET2, EBA then receipient is acquirer of msg
            if bic_list[0] == bic_list[1]:  # sendersBic == destinationBic
                destinationParty = backOfcObj.Acquirer()  # acquirer is the receipient
            else:
                destinationParty = backOfcObj.Counterparty()  # counterParty is the receipient
            if destinationParty and destinationParty.AdditionalInfo():
                try:
                    if destinationParty.AdditionalInfo().SWIFTExtXChrNotUsed():  # True = Dont use ext X chars
                        escape_seq_used = list()
                        extended_x_chars_used = list()
                        for escape_seq in extended_x_char_rev_translation.keys():  # check for escape seq in mt message
                            if mt_message.find(escape_seq) != -1:
                                escape_seq_used.append(escape_seq)  # when found the escape seq, append lists
                                extended_x_chars_used.append(extended_x_char_rev_translation[escape_seq])
                        if escape_seq_used and extended_x_chars_used:  # if we find escape seq in lists, then problem raise it
                            error_str = "Use of extended x characters and their respective escape seqeunces are found in generated MT message"
                            error_str = error_str + '\n' + "Extended X characters Used  : %s" % str(extended_x_chars_used)
                            error_str = error_str + '\n' + "Respective Escape Sequences : %s" % str(escape_seq_used)
                            return destinationParty, False, error_str  # invalid use
                except AttributeError, e:
                    notifier.WARN('Exception while checking value of AddInfo <SWIFTExtXChrNotUsed> on Party <%s> : %s' % (destinationParty.Name(), str(e)))
                    notifier.WARN('Ensure dataPrep task has been performed')

    return destinationParty, True, error_str  # valid use


def generate_swift_message_from(acm_obj, mt_type, remove_namespace=True):
    """ Generates swift message from input provided """
    mt_message = ''
    try:
        updated_mt_py_obj, exceptions_in_mapping, getter_values = generate_python_object(acm_obj, mt_type)
        if not getter_values:
            getter_values = {}
        if updated_mt_py_obj:
            # generate message from mapped swift python object
            pyxb.RequireValidWhenParsing(False)
            swiftml_obj = FSwiftML.FSwiftML()
            msg_type = mt_type[0:2].upper()
            if msg_type == 'MX':
                try:
                    xml_msg = swiftml_obj.pyobject_to_xml(updated_mt_py_obj, remove_namespace)
                    notifier.INFO("%s Generated swift message = %s" % (mt_type, xml_msg))
                except Exception, e:
                    xml_msg = None
                return xml_msg, exceptions_in_mapping
            elif msg_type == 'MT':
                mt_message = swiftml_obj.pyobject_to_swift(updated_mt_py_obj)
                if not exceptions_in_mapping:
                    mt_message = remove_non_swift_characters(mt_message)
                if mt_message:
                    notifier.DEBUG("%s Generated swift message without header = %s" % (mt_type, mt_message))

                child_mt_type = ''
                split_data = str(mt_type).split('-')
                #mt_type = split_data[0]
                if len(split_data) > 1:
                    child_mt_type = split_data[1]



                # Set header to the generated swift message
                notifier.DEBUG("{0} Generating header for SWIFT message".format(mt_type))
                fmt_swift_header_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_header_object(
                    mt_type, acm_obj, mt_message)
                if child_mt_type:
                    fmt_swift_header_class_obj.set_child_mt_type('MT' + child_mt_type)

                mt_message = fmt_swift_header_class_obj.swift_message_with_header()
                if mt_message:
                    notifier.INFO("%s Successfully generated <%s> swift message for %s:%s" % (mt_type, mt_type, acm_obj.RecordType(), acm_obj.Oid()))
                # Validate network rules for swift message object
                validate_network_rules(mt_type, updated_mt_py_obj, mt_message, acm_obj)
                # Using it only for SwiftWriter solutions and not for MiFid for now

                notifier.INFO("%s Generated swift message = %s" % (mt_type, mt_message))
                return mt_message, updated_mt_py_obj, exceptions_in_mapping
        else:
            msg_type = mt_type[0:2].upper()
            if msg_type == 'MX':
                return None, {}
            elif msg_type == 'MT':
                return None, None, {}
    except Exception, e:
        if getattr(acm_obj, 'RecordType', None):
            notifier.ERROR('%s Failure in generating swift message type %s for %s:%s.' % (str(mt_type), str(mt_type), \
                                                                                          str(acm_obj.RecordType()),
                                                                                          str(acm_obj.Oid())))
        else:
            notifier.ERROR('%s Failure in generating swift message type %s for %s:%s.' % (str(mt_type), str(mt_type), \
                                                                                          str(type(acm_obj)),
                                                                                          str(acm_obj)))
        notifier.ERROR('%s' % str(e))
        raise e
    notifier.NotifyByMailsAndMessages()


def generate_swift_message(acm_obj, mt_type, swift_metadata_xml_dom=None):
    """ Generates Swift message """
    raw_mt_type = mt_type
    try:
        updated_mt_py_obj, exceptions_in_mapping, getter_values = generate_python_object(acm_obj, mt_type,
                                                                                         swift_metadata_xml_dom)
        if not getter_values:
            getter_values = {}
        mt_type = str(mt_type).split('-')[0]
        mt_message = ''
        swiftml_obj = FSwiftML.FSwiftML()
        if swift_format_of_message(mt_type) == 'MX':
            mt_message =  swiftml_obj.pyobject_to_xml(updated_mt_py_obj, True)
            return mt_message, updated_mt_py_obj, exceptions_in_mapping, getter_values

        if updated_mt_py_obj:
            # generate message from mapped swift python object
            if exceptions_in_mapping:
                pyxb.RequireValidWhenParsing(False)

            mt_message = swiftml_obj.pyobject_to_swift(updated_mt_py_obj)
            if not exceptions_in_mapping:
                mt_message = remove_non_swift_characters(mt_message)
            notifier.DEBUG("%s Generated swift message without header = %s" % (mt_type, mt_message))
            notifier.DEBUG("{0} Generating header for SWIFT message".format(mt_type))

            child_mt_type = ''
            split_data = str(raw_mt_type).split('-')
            #mt_type = split_data[0]
            if len(split_data) > 1:
                child_mt_type = split_data[1]

            if child_mt_type:
                FSwiftWriterMessageHeader.FSwiftWriterMessageHeader.set_child_mt_type('MT' + child_mt_type)

            fmt_swift_header_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_header_object(mt_type, acm_obj,mt_message,swift_metadata_xml_dom)
            mt_message = fmt_swift_header_class_obj.swift_message_with_header()

            #Overriding the core module to get around the validation as it expects that block 3 of the header should have
            #confirmaiton/ settlement reference
            #destinationParty, is_msg_valid, error_str = validate_use_of_extended_x_char_for_counterparty(mt_message)
            is_msg_valid = True
            if mt_message and is_msg_valid:
                notifier.INFO("%s Successfully generated <%s> swift message for %s:%s" % (mt_type, mt_type, acm_obj.RecordType(), str(acm_obj.Oid())))
                notifier.DEBUG("%s Generated swift message = %s" % (mt_type, str(mt_message)))
            elif mt_message and not is_msg_valid:
                notifier.ERROR("%s Generated swift message with extended X characters = %s" % (mt_type, mt_message))
                notifier.ERROR("%s %s" % (mt_type, error_str))
                error_msg = "%s DestinationParty <%s> will not accept this message, as AddInfo <SWIFTExtXChrNotUsed> is 'True' on this party." % (mt_type, destinationParty.Name())
                notifier.ERROR("%s %s" % (mt_type, error_msg))
                exceptions_in_mapping['GENERATIONFAILED'] = error_msg
            return mt_message, updated_mt_py_obj, exceptions_in_mapping, getter_values
    except Exception, e:
        notifier.ERROR(str(e), exc_info=1)
        raise e


def generate_amb_message_from_mt_message(mt_message, msg_id, amb_sender_subject):
    """ Generates amb message from mt message """
    notifier.DEBUG("Generate AMB message from generated MT message")
    message = None

    message = amb.mbf_start_message(None, amb_sender_subject, "1.0", None, "SWIFT_NETWORK")
    mb_msg = message.mbf_start_list("SWIFT_MESSAGE")
    mb_msg.mbf_add_string("DOCUMENT_ID", str(msg_id))
    mb_msg.mbf_add_string("SWIFT", mt_message)
    mb_msg.mbf_end_list()
    message.mbf_end_message()
    notifier.DEBUG("Swift message to AMB = %s" % message.mbf_object_to_string())
    return message


def get_checksum_for_outgoing_message(swift_python_object):
    """ Get checksum for outgoing message """
    swift_ml = FSwiftML.FSwiftML()
    xml = swift_ml.pyobject_to_xml(swift_python_object)
    md5Sum = hashlib.md5(xml)
    return md5Sum.hexdigest()


def get_checksum_for(confirmation_obj):
    """ Get checksum for acm obj provided """
    mt_type = 'MT' + str(FSwiftMLUtils.calculate_mt_type_from_acm_object(confirmation_obj))
    use_xml = None
    try:
        if should_use_operations_xml(mt_type):
            use_xml = dom.parseString(get_operations_xml(confirmation_obj))
    except Exception, e:
        if mt_type == 'MT0':
            pass
    fmt_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_object(confirmation_obj, mt_type, use_xml)
    if not fmt_class_obj:
        raise Exception('Failure in generating checksum for %s:%s.' % (str(confirmation_obj.RecordType()), str(confirmation_obj.Oid())))
    return get_checksum(fmt_class_obj)


def get_checksum(fmt_class_obj):
    """This function calculates checksum by calling the getter methods tagged for checksum in 'attributes_to_compare_for_amendment_generation'
       Since there can be an exception in while calling getter methods, just catching the exception and doing nothing. There are 2 places from which
       getters are called 1. Checksum generation i.e. here 2. Setter methods in FMtXXXOutBase class. Both places are handling the exceptions so there is no
       exception handling in the actual getter methods. """
    engine_object = SwiftWriterEngine(fmt_class_obj)
    attr_names = sorted(engine_object.attributes_to_compare_for_amendment_generation())
    string_for_checksum = ''
    attr_values = []
    for each in attr_names:
        try:
            value = getattr(fmt_class_obj, each)()
        except Exception, e:
            value = ''
        if value:
            attr_values.append(value)
        else:
            attr_values.append('')
    string_for_checksum = ';'.join([str(attr) + str(val) for attr, val in zip(attr_names, attr_values)])
    md5Sum = hashlib.md5(string_for_checksum)
    return md5Sum.hexdigest()


def init_amb_connection(amb_address):
    """ Method to initialize amb connection """
    notifier.DEBUG("Connecting to AMB %s" % amb_address)
    amb_connection = False
    try:
        amb.mb_init(amb_address)
        amb_connection = True
    except:
        error_message = "Could not connect to AMB <%s>" % str(amb_address.split('/')[0])
        notifier.ERROR(error_message)
        raise Exception(error_message)

    return amb_connection


def send_message_over_amb(amb_msg_obj, sender_channel, msg_subject, message_broker):
    """ Method to send messages over amb """
    writer = None
    status = False
    last_mid = None
    amb_connection = False

    try:
        writer = amb.mb_queue_init_writer(sender_channel, _event_cb, None)
    except Exception, e:
        if str(e) == 'Not Connected':
            amb_connection = init_amb_connection(message_broker)
            if amb_connection:
                try:
                    writer = amb.mb_queue_init_writer(sender_channel, _event_cb, None)
                except Exception, e:
                    error_message = "Could not open channel <%s> to send messages over AMB" % sender_channel
                    # notifier.ERROR(error_message)
                    raise Exception(error_message)
        else:
            error_message = "Could not open channel <%s> to send messages over AMB" % sender_channel
            # notifier.ERROR(error_message)
            raise Exception(error_message)


    if writer:
        try:
            buffer = amb.mbf_create_buffer()
            amb_msg_obj.mbf_generate(buffer)

            amb.mb_queue_write(writer, msg_subject, buffer.mbf_get_buffer_data(), \
                               buffer.mbf_get_buffer_data_size(), time.strftime("%Y-%m-%d %H:%M:%S"))
            status = True
        except Exception, e:
            status = False
            raise Exception("Could not write swift mesage to AMB channel %s" % sender_channel)
        last_mid = amb.mb_last_write_message_id(writer)

    return status, last_mid


def _event_cb(channel, event, arg):
    pass


def regenerate_mt_message_from(acm_obj, mt_type):
    """ Using this wrapper so that errors occurring in regenerate could be captured.
       BusinessProcessCallbackContext does not give that control """
    notifier.DEBUG("{0} Regenerate mt message from".format(mt_type))
    mt_msg = ''
    try:
        mt_msg = generate_swift_message_from(acm_obj, mt_type)
    except Exception, e:
        notifier.ERROR("{0} Failed to regenerate {0} message".format(mt_type))
        notifier.ERROR("%s" % str(e))
    return mt_msg


def string_as_list(strng):
    """ Converts string to list """
    lst = []
    if type(strng) == type(''):
        try:
            result = eval(strng)
            if type(result) == type([]):
                lst = result
            elif result:
                lst.append(str(result))
        except Exception:
            strng_split = strng.split(',')
            for data in strng_split:
                if data.strip():
                    lst.append(data.strip())
    elif type(strng) == type([]):
        lst = strng
    return lst


def send_swift_message_to_amb(msg_type, swift_msg, msg_id, pkg_amb_params_fparameter):
    """ Method to send messages to AMB """
    try:
        last_mid = None
        pkg_sender_subject = get_value_of_fparameter_for(pkg_amb_params_fparameter, 'AMBSenderSubject')

        sender_channel = get_value_of_fparameter_for('FSwiftWriterAMBConfig', 'AMBSender')
        message_broker = get_value_of_fparameter_for('FSwiftSolutionConfig', 'AMBAddress')

        amb_msg_obj = generate_amb_message_from_mt_message(swift_msg, msg_id, pkg_sender_subject)

        result, last_mid = send_message_over_amb(amb_msg_obj, sender_channel, pkg_sender_subject, message_broker)

        message_broker_address = message_broker.split('/')[0]
        if result and last_mid:
            notifier.INFO('%s Sent %s message over AMB %s with AMB message id %s' % (str(msg_type), str(msg_type), str(message_broker_address), str(last_mid)))
        else:
            notifier.ERROR('%s Failure in sending %s message over amb %s' % (str(msg_type), str(msg_type), str(message_broker_address)))
    except Exception, e:
        notifier.ERROR('Exception caught:%s' % str(e))
        raise Exception('%s Failure in sending message over amb. %s' % (str(msg_type), str(e)))
        # return None
    return last_mid


def get_config_from_fparameter(fparameter_name):
    """ Method to get config from FParameter """
    return FSwiftMLUtils.Parameters(fparameter_name)


def get_dom_from_xml(swift_xml):
    """ Method to get dom from xml"""
    return dom.parseString(swift_xml)


def get_value_from_xml_tag(xmldom, tag_hierarchy, ignore_absense=False):
    """ Method to get value from xml tag """
    current_parent = xmldom
    if current_parent:
        try:
            for each_tag_name in tag_hierarchy:
                current_parent = current_parent.getElementsByTagName(each_tag_name)[0]
            return current_parent.childNodes[0].data
        except IndexError, e:
            if not ignore_absense:
                raise Exception("Error in getting value from XML tag %s" % tag_hierarchy[-1])
    return None


def get_repetative_xml_tag_value(current_parent, tag_names=None, block_name=None, ignore_absense=False):
    """ Method to get repetitive xml tag value """
    values = []
    try:
        if block_name:
            current_parent = current_parent.getElementsByTagName(block_name)[0]
        max_repetition = len(current_parent.getElementsByTagName(tag_names[0]))
        for num in range(max_repetition):
            current_block = dict.fromkeys(tag_names)
            values.append(current_block)
        for tag in tag_names:
            count = 0
            for repeated_tag in current_parent.getElementsByTagName(tag):
                tag_data = repeated_tag._get_firstChild()
                if tag_data:
                    values[count][tag] = tag_data.data
                count += 1
    except IndexError, e:
        if not ignore_absense:
            raise Exception("Error in getting value from XML tag %s" % tag_names[-1])
    return values


def get_block_xml_tags(current_parent, block_name, tag_names, ignore_absense=False):
    """ Retrieves block xml tags """
    if current_parent:
        values = []
        try:

            blocks = current_parent.getElementsByTagName(block_name)
            for each in blocks:
                d = {}
                for tag in tag_names:
                    if each.getElementsByTagName(tag)[0].childNodes:
                        d[tag] = each.getElementsByTagName(tag)[0].childNodes[0].data
                    else:
                        d[tag] = ""
                values.append(d)
            return values
        except IndexError, e:
            if not ignore_absense:
                raise Exception("Error in getting value from XML tag %s" % block_name)
    return None

def get_type_of_operation(confirmation):
    operation = 'NEWT'

    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        confirmation_types = {ConfirmationType.RESEND: 'NEWT',
                              ConfirmationType.AMENDMENT: 'AMND',
                              ConfirmationType.CANCELLATION: 'CANC',
                              ConfirmationType.CHASER: 'DUPL'
                              }
    else:
        confirmation_types = {"Resend": 'NEWT',
                              "Amendment": 'AMND',
                              "Cancellation": 'CANC',
                              "Chaser": 'DUPL'
                              }

    if confirmation.Type() in confirmation_types:
        operation = confirmation_types[confirmation.Type()]

    return operation

def replace_extended_x_chars_from_tagval(swift_tag_value, swift_tag_class=None):
    swiftwriter_config = get_config_from_fparameter('FSwiftWriterConfig')
    dict_trans_temp = getattr(swiftwriter_config, 'UseExtendedXCharSet', 'True')
    if ast.literal_eval(dict_trans_temp) and swift_tag_class and swift_tag_value:
        mt_type = swift_tag_class.__name__.split('_')[0]
        swift_tag = swift_tag_class.__name__.split('_')[-2]
        if (mt_type == 'MT105' and swift_tag == '77F'):
            return swift_tag_value  # Y character set
        if (mt_type == 'MT568' and swift_tag == '70F') or \
                (mt_type == 'MT563' and swift_tag == '70G') or \
                (mt_type == 'MT103REMIT' and swift_tag == '77T'):
            return swift_tag_value  # Z character set
        for key in extended_x_char_translation.keys():
            swift_tag_value = swift_tag_value.replace(str(key), "??" + extended_x_char_translation[key])

    return swift_tag_value

def replace_extended_x_chars(swift_message):
    for key in extended_x_char_translation.keys():
        swift_message = swift_message.replace(str(key), "??" + extended_x_char_translation[key])

    return swift_message

def remove_non_swift_characters_from_tagval(swift_tag_value, swift_tag_class):
    if isinstance(swift_tag_value, str):
        swift_tag_value = SwiftTrans.Translate(swift_tag_value)
        swift_tag_value = replace_extended_x_chars_from_tagval(swift_tag_value, swift_tag_class)
    return swift_tag_value

def remove_non_swift_characters(swift_message):
    swift_message = SwiftTrans.Translate(swift_message)
    swift_message = replace_extended_x_chars(swift_message)
    return swift_message


class SwiftTrans(object):
    """ Adopts TranslationMap  from FSwiftWriterConfig, Translates non-swift characters
    to characters mentioned in TranslationMap . """

    def __init__(self):
        # Commenting default codepage as default codepage value does not change
        # default_codepage = 'ISO-8859-1'
        default_swift_chars = {10: '\n',13: '\r',39: "'", 40: '(', 41: ')', 43: '+', 44: ',', 45: '-', 46:'.', 47: '/', 48: '0', 49: '1', 50: '2', 51: '3',  52: '4', 53: '5', 54: '6',55: '7', 56: '8', 57: '9', 58: ':',63:'?',65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z',97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}
        accents_diacritic_chars = {192:'A', 193:'A', 194:'A', 195:'A', 196:'A', 197:'A', 198:'A', 199:'C', 200:'E', 201:'E', 202:'E', 203:'E', 204:'I', 205:'I', 206:'I', 207:'I',209: 'N',216: 'O',223: 'S',230: 'a',248: 'o', 210: 'O', 211: 'O', 212: 'O', 213: 'O', 214: 'O',217: 'U', 218: 'U', 219: 'U', 220: 'U', 221: 'Y',224: 'a', 225: 'a', 226: 'a', 227: 'a', 228: 'a', 229: 'a',231: 'c', 232: 'e', 233: 'e', 234: 'e', 235: 'e', 236: 'i', 237: 'i', 238: 'i', 239: 'i',241: 'n', 242: 'o', 243: 'o', 244: 'o', 245: 'o', 246: 'o',249: 'u', 250: 'u', 251: 'u', 252: 'u', 253: 'y',255: 'y'}
        DICT_TRANS = {0: ' ', 1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' ', 11: ' ', 12: ' ', 14: ' ', 15: ' ', 16: ' ', 17: ' ', 18: ' ', 19: ' ', 20: ' ', 21: ' ', 22: ' ', 23: ' ', 24: ' ', 25: ' ', 26: ' ', 27: ' ', 28: ' ', 29: ' ', 30: ' ', 31: ' ', 32: ' ', 127: ' ', 128: ' ', 129: ' ', 130: ' ', 131: ' ', 132: ' ', 133: ' ', 134: ' ', 135: ' ', 136: ' ', 137: ' ', 138: ' ', 139: ' ', 140: ' ', 141: ' ', 142: ' ', 143: ' ', 144: ' ', 145: ' ', 146: ' ', 147: ' ', 148: ' ', 149: ' ', 150: ' ', 151: ' ', 152: ' ', 153: ' ', 154: ' ', 155: ' ', 156: ' ', 157: ' ', 158: ' ', 159: ' ', 160: ' ', 161: ' ', 162: ' ', 163: ' ', 164: ' ', 165: ' ', 166: ' ', 167: ' ', 168: ' ', 169: ' ', 170: ' ', 171: ' ', 172: ' ', 173: ' ', 174: ' ', 175: ' ', 176: ' ', 177: ' ', 178: ' ', 179: ' ', 180: ' ', 181: ' ', 182: ' ', 183: ' ', 184: ' ', 185: ' ', 186: ' ', 187: ' ', 188: ' ', 189: ' ', 190: ' ', 191: ' ', 208: ' ', 215: ' ', 222: ' ', 240: ' ', 247: ' ',254: ' '}

        dict_trans = {}
        for char_dict in (default_swift_chars, accents_diacritic_chars, extended_x_char, DICT_TRANS):
            dict_trans.update(char_dict)

        swiftwriter_config = get_config_from_fparameter('FSwiftWriterConfig')
        dict_trans_temp = getattr(swiftwriter_config, 'TranslationMap', None)

        if dict_trans_temp:
            dict_trans_temp = eval(dict_trans_temp)
            dict_trans.update(dict_trans_temp)
            dict_trans.update(extended_x_char)

        # Check if length of values of dict_trans does not exceed 1
        flag = True
        for val in dict_trans.values():
            if len(val) != 1:
                flag = False

        if len(dict_trans) == 256 and flag:
            self.translate_to = ''.join(dict_trans.values())
            self.translate_to = self.translate_to.decode('ISO-8859-1')

    def Compute(self, data):
        return data.translate(self.translate_to)

    @staticmethod
    def Translate(data):
        swift_trans = SwiftTrans()
        return swift_trans.Compute(data)

class ResendMTMessageConfMenuItem(FUxCore.MenuItem):
    """MenuItem for displaying outgoing message from confirmation object"""
    def __init__(self, activeSheet):
        self.active_sheet = activeSheet
        self.bpr_obj = None

    def Enabled(self):
        return True

    def Invoke(self, _eii):
        if self.bpr_obj.CanHandleEvent('ReSend'):
            self.resend_mt_message()
        else:
            shell = _eii.Parameter('shell')
            acm.UX().Dialogs().MessageBoxInformation(shell, 'You do not have permission to perform '
                                                            'the selected action.')

    def Applicable(self):
        return self._is_enabled()

    def _is_enabled(self):
        is_enabled = False
        if self.active_sheet is not None:
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        self.bpr_obj = FSwiftMLUtils.get_business_process(acm_obj, "Outgoing")
                        if self.bpr_obj and self.bpr_obj.CurrentStep().State().Name() in ['SendFailed'] and acm_obj.Status() in ['Released']:
                            return True
            except Exception, e:
                notifier.ERROR("Exception occurred in ResendMTMessageConfMenuItem._is_enabled : %s" % str(e))
        return is_enabled

    def resend_mt_message(self):
        msg_type = ''
        try:
            notifier.INFO("Resending generated swift message over AMB")
            external_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(self.bpr_obj)
            swift_message = FSwiftMLUtils.get_swift_data_from_bpr(self.bpr_obj)
            swift_message_with_addtional_delimiter = process_aditional_delimiter(swift_message)
            encrypted_swift_message, param_dict = encrypt_message(swift_message_with_addtional_delimiter)
            param_dict["SentDate"] = str(datetime.datetime.now().date())
            msg_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(external_item)
            pkg_name = get_module_name(msg_type)
            config_name = pkg_name + '_Config'
            last_mid = send_swift_message_to_amb(msg_type, str(encrypted_swift_message), external_item.Oid(), config_name)
            FSwiftMLUtils.FSwiftExternalObject.set_channel_details(external_item, 'AMB', last_mid)
            FSwiftMLUtils.trigger_event(self.bpr_obj, 'ReSend', "Resending Swift message", param=param_dict)
        except Exception, e:
            notifier.ERROR("%s Exception handled in ResendMTMessageConfMenuItem.resend_mt_message : %s" % (msg_type, str(e)))

def create_resend_mtmessage_menuitem(eii):
    active_sheet = FSwiftMLUtils.get_active_sheet(eii)
    return ResendMTMessageConfMenuItem(active_sheet)

class DuplicateMTMessageSettMenuItem(FUxCore.MenuItem):
    """MenuItem for generating duplicate message from settlement object"""

    def __init__(self, activeSheet):
        self.active_sheet = activeSheet
        self.bpr_obj = None

    def Enabled(self):
        return True

    def Invoke(self, _eii):
        if self.bpr_obj:
            if self.bpr_obj.CanHandleEvent('Dupl'):

                self.duplicate_mt_message()
            else:
                shell = _eii.Parameter('shell')
                acm.UX().Dialogs().MessageBoxInformation(shell, 'You do not have permission to perform '
                                                            'the selected action.')

    def Applicable(self):
        return self._is_enabled()

    def _is_enabled(self):
        is_enabled = False
        if self.active_sheet is not None:
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        self.acm_obj = cell.RowObject()
                        self.bpr_obj = FSwiftMLUtils.get_business_process(self.acm_obj, "Outgoing")

                        if self.bpr_obj and self.bpr_obj.CanHandleEvent('Dupl'):
                            if self.bpr_obj.CurrentStep().State().Name() in ['Acknowledged', 'Duplicate'] and self.acm_obj .Status() in ['Acknowledged', 'Released']:
                                return True
            except Exception, e:
                notifier.ERROR("Exception occurred in DuplicateMTMessageSettMenuItem._is_enabled : %s" % str(e))
        return is_enabled

    def duplicate_mt_message(self):
        msg_type = ''
        try:
            import FCashOutProcessing
            state_object = FCashOutProcessing.FCashOutProcessing(self.bpr_obj)

            state_object.process_state_duplicate()
        except Exception, e:
            notifier.ERROR(
                "%s Exception handled in DuplicateMTMessageSettMenuItem.duplicate_mt_message : %s" % (msg_type, str(e)))


def create_duplicate_menuitem(eii):
    active_sheet = FSwiftMLUtils.get_active_sheet(eii)
    return DuplicateMTMessageSettMenuItem(active_sheet)

def BPRSubMenuItemCreate(eii):
    import FSwiftMLUtils
    return BPRSubMenuItem(eii, FSwiftMLUtils.active_state_chart_name_out())

try:
    class BPRSubMenuItem(FUxCore.SubMenu):
        def __init__(self, eii, state_chart_names):
            self._eii = eii
            self.active_sheet = FSwiftMLUtils.get_active_sheet(eii)
            self.acm_obj = None
            if type(state_chart_names) == type([]):
                self.state_chart_names = state_chart_names
            else:
                self.state_chart_names = [state_chart_names]

        def Invoke(self, eii):
            menu = None
            if self.active_sheet:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        bpObj = cell.RowObject()
                        if bpObj.IsKindOf(acm.FBusinessProcess):
                            if bpObj.CurrentStep().State().Name() != "Unpaired" and bpObj.StateChart().Name() in self.state_chart_names:
                                self.acm_obj = FSwiftMLUtils.FSwiftExternalObject.get_acm_object_from_ext_object(bpObj.Subject())
                                break
            if self.acm_obj:
                menu = acm.FUxMenu()
                solMenu = menu
                if solMenu:
                    if self.view_acm_object_enabled():
                        solMenu.AddItem(self.view_acm_object, '', "View Acm Object")
                    if self.view_outgoing_mt_message_enabled():
                        bprObj = FSwiftMLUtils.get_business_process(self.acm_obj, "Outgoing")
                        mt_msg_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(bprObj.Subject())

                        solMenu.AddItem(self.view_outgoing_mt_message, '', "View "+swift_format_of_message(mt_msg_type))

                        if is_viewer_supported([mt_msg_type]):
                            if FSwiftMLUtils.get_acm_version() >= 2017.4:
                                solMenu.AddItem(self.view_outgoing_mt_message, 'SwiftViewer', "View MT SwiftViewer")
            return menu

        def Applicable(self):
            return self.view_acm_object_enabled() or self.view_outgoing_mt_message_enabled()

        def Enabled(self):
            return True

        def view_acm_object_enabled(self):  # copied from ViewAcmObjectMenuItem._is_enabled
            is_enabled = False
            try:
                if self.active_sheet:
                    for cell in self.active_sheet.Selection().SelectedCells():
                        if cell.IsHeaderCell():
                            bpObj = cell.RowObject()
                            if bpObj.IsKindOf(acm.FBusinessProcess):
                                # mt_type = bpObj.AdditionalInfo().SwiftMessageType()
                                # sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(mt_type)
                                if bpObj.CurrentStep().State().Name() != "Unpaired" and bpObj.StateChart().Name() in self.state_chart_names:
                                    # self.acm_obj = bpObj.Subject().Subject()
                                    self.acm_obj = FSwiftMLUtils.FSwiftExternalObject.get_acm_object_from_ext_object(bpObj.Subject())
                                    if self.acm_obj:
                                        is_enabled = True
                                        break
            except Exception, e:
                notifier.ERROR("Exception occurred in BPRSubMenuItem.view_acm_object_enabled : %s" % str(e))
            return bool(is_enabled)

        def view_acm_object(self, eii):
            if self.acm_obj.IsKindOf(acm.FSettlement):
                acm.StartApplication("Operations Manager", self.acm_obj)
            elif self.acm_obj.IsKindOf(acm.FConfirmation):
                acm.StartApplication("Operations Manager", self.acm_obj)

        def view_outgoing_mt_message_enabled(self):  # copied from ViewOutgoingMTMsgBprMenuItem._is_enabled
            is_enabled = False
            try:
                if self.active_sheet:
                    for cell in self.active_sheet.Selection().SelectedCells():
                        if cell.IsHeaderCell():
                            bpObj = cell.RowObject()
                            if bpObj.IsKindOf(acm.FBusinessProcess):
                                # mt_type = bpObj.AdditionalInfo().SwiftMessageType()
                                # sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(mt_type)
                                if bpObj.StateChart().Name() in self.state_chart_names and bpObj.CurrentStep().State().Name() not in ['Ready', 'XMLGenerated']:
                                    is_enabled = True
                                    break
            except Exception, e:
                notifier.ERROR("Exception occurred in BPRSubMenuItem.view_outgoing_mt_message_enabled : %s" % str(e))
            return bool(is_enabled)

        def view_outgoing_mt_message(self, eii):
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        bpObj = cell.RowObject()
                        if bpObj.IsKindOf(acm.FBusinessProcess):
                            acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpObj)
                            swift_data = FSwiftMLUtils.get_swift_data_from_bpr(bpObj)
                            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(bpObj)
                            mt_msg_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_obj)
                            if eii == 'SwiftViewer':
                                integration_type = 'SwiftWriter'
                                #mt_msg_type = FSwiftMLUtils.get_mt_type_from_swift(swift_data)
                                FSwiftViewerGui.ReallyStartApplication(self._eii, (acm_obj, swift_data, False, mt_msg_type, integration_type))
                            else:
                                #mt_msg_type = FSwiftMLUtils.get_mt_type_from_swift(swift_data)
                                temp_dir = tempfile.gettempdir()
                                out_file = os.path.join(temp_dir, '%s_Outgoing.txt' % (mt_msg_type))
                                f = open(out_file, 'w')
                                f.write(swift_data)
                                f.close()
                                os.startfile(out_file)
            except Exception, e:
                notifier.ERROR("Exception occurred in BPRSubMenuItem.view_outgoing_mt_message : %s" % str(e))
except Exception, e:  # RTS22 uses 'import FSwiftWriterUtils' but on 16.1 SubMenu is not available hence import fails
    pass

def SubMenuItemCreate(eii):
    import FSwiftMLUtils
    return SubMenuItem(eii, FSwiftMLUtils.active_state_chart_name_out())


try:
    class SubMenuItem(FUxCore.SubMenu):
        def __init__(self, extObj, state_chart_names):
            self.m_extObj = extObj
            self.active_sheet = FSwiftMLUtils.get_active_sheet(extObj)
            if type(state_chart_names) == type([]):
                self.state_chart_names = state_chart_names
            else:
                self.state_chart_names = [state_chart_names]
            self.preview_outgoing_mt_message = False
            self.view_outgoing_mt_message = False
            self.view_outgoing_message_business_process = False
            self.typ_of_msg = None
            self.set_message_params()
                
        def set_message_params(self):
            view_outgoing_message_business_process_found = False
            preview_outgoing_mt_message_found = False
            view_outgoing_mt_message_found = False
            
            try:
                if self.active_sheet:
                    for cell in self.active_sheet.Selection().SelectedCells():
                        if cell.IsHeaderCell():
                            acm_obj = cell.RowObject()
			    if acm_obj.IsKindOf('FSettlement') and acm_obj.Status() == 'Authorised' and not view_outgoing_message_business_process_found:
                                self.view_outgoing_message_business_process = False
                                view_outgoing_message_business_process_found = True
                                
                            typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj)
			    msg_typ = typ_of_msg 
                            mt_list = get_applicable_message_list(acm_obj, typ_of_msg)

                            if swift_format_of_message(typ_of_msg) == 'MT':
                                typ_of_msg = 'MT' + str(typ_of_msg)
                            else:
                                typ_of_msg = str(typ_of_msg)
                            is_msg_supported = is_outgoing_message_supported(typ_of_msg)
                            if is_msg_supported:
                                msg_status = should_message_be_generated_by_adaptivdocs(typ_of_msg) or bypass_Swift_Solutions(acm_obj)
                            else:
				self.view_outgoing_message_business_process = False
				self.preview_outgoing_mt_message = False
				self.view_outgoing_mt_message = False
                                return
                            if msg_status:
                                self.view_outgoing_message_business_process = False
				self.preview_outgoing_mt_message = False
				self.view_outgoing_mt_message = False
                                return
                            
                            if msg_typ != '0' and acm_obj.IsKindOf('FSettlement') and acm_obj.Status() == 'Authorised'and not preview_outgoing_mt_message_found:
                                self.preview_outgoing_mt_message = True
                                preview_outgoing_mt_message_found = True
                            
                            if (acm_obj.IsKindOf('FConfirmation') or acm_obj.IsKindOf('FSettlement')) and not view_outgoing_mt_message_found:
                                for each_mt in mt_list:
                                    if swift_format_of_message(each_mt) == 'MT':
                                        each_mt = 'MT' + each_mt
                                    ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, msg_typ=each_mt, integration_type='Outgoing')
                                    if ext_obj:
                                        bpr_obj = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
                                        if bpr_obj:
                                            if acm_obj.IsKindOf('FConfirmation'):
                                                if bpr_obj.CurrentStep().State().Name() not in ['Ready', 'XMLGenerated']:
                                                    self.view_outgoing_mt_message = True
                                                    view_outgoing_mt_message_found = True
                                            if acm_obj.IsKindOf('FSettlement'):
                                                if bpr_obj.CurrentStep().State().Name() not in ['Ready', 'XMLGenerated'] and acm_obj.Status() != 'Authorised':
                                                    self.view_outgoing_mt_message = True
                                                    view_outgoing_mt_message_found = True
                                                    
                            if not view_outgoing_message_business_process_found:
                                for each_mt in mt_list:
                                    if swift_format_of_message(each_mt) == 'MT':
                                        each_mt = 'MT' + each_mt
                                    ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, msg_typ=each_mt, integration_type='Outgoing')
                                    if ext_obj:
                                        bpr_obj = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
                                        if bpr_obj and bpr_obj.StateChart().Name() in self.state_chart_names:
                                            self.view_outgoing_message_business_process = True
                                            view_outgoing_message_business_process_found = True
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.set_message_params : %s" % str(e))
            return
            
        def Invoke(self, eii):
            # This method is called by the framework every time the menu is shown.
            acm_obj = None
            if not self.active_sheet:
                self.active_sheet = FSwiftMLUtils.get_active_sheet(self.extObj)
            if self.active_sheet:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        break

            if acm_obj:
                solMenu = None
                menu = acm.FUxMenu()
                msgType = str(FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj))
                msg_list = get_applicable_message_list(acm_obj, msgType)
                ext_objects = []
                for msg in msg_list:
                    if swift_format_of_message(msg) == 'MT':
                        msg = 'MT' + msg
                    ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, msg_typ=msg, integration_type='Outgoing')
                    if ext_obj:
                        ext_objects.append(ext_obj)

                for i in ['399', '999', '199-Narrative', '299-Narrative']:
                    ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, msg_typ='MT' + i,
                        integration_type='Outgoing')
                    if ext_obj:
                        ext_objects.append(ext_obj)

                if acm_obj.IsKindOf('FSettlement'):
                    solMenu = menu
                    if solMenu:
                        if self.preview_outgoing_mt_message:
                            #msg_list = self.__get_msg_type_for_preview(acm_obj)

                            menuName = "Preview"
                            if msg_list:
                                # Assuming that a list of message type will not mix MT and MX
                                menuName = menuName + " " + swift_format_of_message(msg_list[0])

                            if len(msg_list) > 1:
                                subMenu = solMenu.AddSubMenu(menuName)
                                for msg in msg_list:
                                    subMenu.AddItem(self.view_mt_settlement_preview_msg, ['', msg], "Preview MT%s" % (msg))
                            else:
                                solMenu.AddItem(self.view_mt_settlement_preview_msg, ['', None], menuName)

                            if FSwiftMLUtils.get_acm_version() >= 2017.4:
                                if is_viewer_supported(msg_list):
                                    if len(msg_list) > 1:
                                        subMenu = solMenu.AddSubMenu("Preview MT SwiftViewer")
                                        for msg in msg_list:
                                            subMenu.AddItem(self.view_mt_settlement_preview_msg, ['SwiftViewer', msg], "Preview %s" % (msg))
                                    else:
                                        solMenu.AddItem(self.view_mt_settlement_preview_msg, ['SwiftViewer', None], "Preview MT SwiftViewer")
                            external_object_for_699 = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_obj, integration_type = 'Outgoing', msg_typ='MT699')
                            if external_object_for_699:
                                self.populate_mt699_menu_items(solMenu, external_object_for_699)
                        if self.view_outgoing_mt_message:
                            #ext_objects = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, integration_type='Outgoing', all_records=True)
                            menuName = "View"
                            if ext_objects:
                                # Assuming that a list of message type will not mix MT and MX
                                #mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_objects[0])
                                mt_type = FSwiftMLUtils.FSwiftExternalObject.get_integration_sub_type(ext_objects[0])
                                menuName = menuName + " " + swift_format_of_message(mt_type)

                            if len(ext_objects) > 1:
                                self.add_sub_menu_item(menuName, solMenu, ext_objects, acm_obj, component='')
                            else:
                                solMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, ['', None], menuName)

                            if FSwiftMLUtils.get_acm_version() >= 2017.4:
                                if is_viewer_supported(ext_objects):
                                    if len(ext_objects) > 1:
                                        self.add_sub_menu_item("View MT SwiftViewer", solMenu, ext_objects, acm_obj, component='SwiftViewer')
                                    else:
                                        solMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, ['SwiftViewer', None], "View MT SwiftViewer")

                        if self.view_outgoing_message_business_process:
                            if len(ext_objects) > 1:
                                subMenu = solMenu.AddSubMenu("View Business Process")
                                for ext_obj in ext_objects:
                                    if ext_obj.IntegrationSubtype() and ext_obj.IntegrationSubtype() not in ['MT699']:
                                        bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
                                        subMenu.AddItem(self.show_bpr, ext_obj, " %s - %s" % (ext_obj.IntegrationSubtype(), str(bpr.CurrentStateName())))
                                self.view_bpr_menuitem_for_mt699(acm_obj, subMenu)
                            else:
                                solMenu.AddItem(self.show_bpr, None, "View Business Process")
                        if self.view_mt699_enabled() and msgType in ['604', '605']:
                            solMenu.AddItem(self.open_mt699, self.m_extObj, 'Send Narrative(MT699)')
                        elif self.view_mtX99_enabled() and (msgType.startswith('1') or msgType.startswith('2')):
                            solMenu.AddItem(self.open_mtX99, self.m_extObj, 'Send Narrative Message')

                if acm_obj.IsKindOf('FConfirmation'):
                    solMenu = menu
                    if solMenu:
                        if self.view_outgoing_mt_message:

                            if FSwiftMLUtils.get_acm_version() >= 2017.4:
                                menuName = "View"
                                if ext_objects:
                                    # Assuming that a list of message type will not mix MT and MX
                                    mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(
                                        ext_objects[0])
                                    menuName = menuName + " " + swift_format_of_message(mt_type)

                                if len(ext_objects) > 1:
                                    self.add_sub_menu_item(menuName, solMenu, ext_objects, acm_obj, component='')
                                else:
                                    solMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, ['', None], menuName)

                                if FSwiftMLUtils.get_acm_version() >= 2017.4:
                                    if is_viewer_supported(ext_objects):
                                        if len(ext_objects) > 1:
                                            self.add_sub_menu_item("View MT SwiftViewer", solMenu, ext_objects, acm_obj,
                                                               component='SwiftViewer')
                                        else:
                                            solMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, ['SwiftViewer',None], "View MT SwiftViewer")

                        if self.view_outgoing_message_business_process:
                            if len(ext_objects) > 1:
                                subMenu = solMenu.AddSubMenu("View Business Process")
                                for ext_obj in ext_objects:
                                    if ext_obj.IntegrationSubtype() and ext_obj.IntegrationSubtype() not in ['MT699']:
                                        subMenu.AddItem(self.show_bpr, ext_obj, "View Business Process %s" % ext_obj.IntegrationSubtype())
                                self.view_bpr_menuitem_for_mt699(acm_obj, subMenu)
                            else:
                                solMenu.AddItem(self.show_bpr, None, "View Business Process")

                        if self.view_mt699_enabled() and msgType in ['600', '620']:
                            solMenu.AddItem(self.open_mt699, self.m_extObj, 'Send Narrative(MT699)')
                        elif self.view_mtX99_enabled() and (msgType.startswith('3')):
                            solMenu.AddItem(self.open_mtX99, self.m_extObj, 'Send Narrative Message')

            return menu

        def add_sub_menu_item(self, menu_text, solMenu, ext_objects, acm_obj, component=''):
            """ Add menu item under the solution menu to view message
            :param menu_text: menu label text to be displayed.
            :param solMenu: solution menu under which sub menu is added
            :param ext_objects: external object list
            :param acm_obj: confirmation/settlement object
            :param component: component to view message
            :return: None
            """
            subMenu = solMenu.AddSubMenu(menu_text)
            for ext_obj in ext_objects:
                if ext_obj.IntegrationSubtype() and ext_obj.IntegrationSubtype() not in ['MT699']:
                    subMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, [component, ext_obj],
                                    "View %s" % ext_obj.IntegrationSubtype())
            self.view_mt699_message_menuitem(acm_obj, subMenu, generate_under=component)


        def Applicable(self):
            applicable = False
            if self.preview_outgoing_mt_message or self.view_outgoing_mt_message or self.view_outgoing_message_business_process:
                applicable = True
            return applicable

        def Enabled(self):
            return True

        def view_mtX99_enabled(self):
            """ Check MT699 view should be enabled or not.
            :return: bool: True, if view need to be enabled else False
            """
            try:
                if self.active_sheet:
                    for cell in self.active_sheet.Selection().SelectedCells():
                        if cell.IsHeaderCell():
                            acm_object = cell.RowObject()
                            typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_object)
                            typ_of_msg = 'MT' + str(typ_of_msg)
                            is_msg_supported = is_outgoing_message_supported(typ_of_msg)
                            if is_msg_supported:
                                return True
                            else:
                                return False
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.view_mtx99 : %s" % str(e))
            return False

        def view_mt699_enabled(self):
            """ Check MT699 view should be enabled or not.
            :return: bool: True, if view need to be enabled else False
            """
            try:
                if self.active_sheet:
                    for cell in self.active_sheet.Selection().SelectedCells():
                        if cell.IsHeaderCell():
                            acm_object = cell.RowObject()
                            typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_object)
                            typ_of_msg = 'MT' + str(typ_of_msg)
                            is_msg_supported = is_outgoing_message_supported(typ_of_msg)
                            if is_msg_supported:
                                return True
                            else:
                                return False
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.view_mt699 : %s" % str(e))
            return False

        def populate_mt699_menu_items(self, solMenu, external_object_for_699):
            """ Add menu item for MT699
            :param solMenu:
            :param external_object_for_699:
            :return:
            """
            subMenu = solMenu.AddSubMenu("View MT")
            subMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, ['', external_object_for_699],
                            "View %s" % external_object_for_699.IntegrationSubtype())
            subMenu = solMenu.AddSubMenu("View MT SwiftViewer")
            subMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, ['SwiftViewer', external_object_for_699],
                            "View %s" % external_object_for_699.IntegrationSubtype())
            subMenu = solMenu.AddSubMenu("View Business Process")
            subMenu.AddItem(self.show_bpr, external_object_for_699,
                            "View Business Process %s" % external_object_for_699.IntegrationSubtype())

        def view_bpr_menuitem_for_mt699(self, acm_obj, subMenu):
            """ Show MT699 menu on View Business Process sub menu
            :param acm_obj: Settlement for confirmation object
            :param subMenu: bpr sub Menu
            :return:
            """
            external_object_for_699 = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj,
                                                                                             integration_type='Outgoing',
                                                                                             msg_typ='MT699')
            if external_object_for_699:
                subMenu.AddItem(self.show_bpr, external_object_for_699,
                                "View Business Process %s" % external_object_for_699.IntegrationSubtype())

        def view_mt699_message_menuitem(self, acm_obj, subMenu, generate_under=''):
            """ Show 'View MT699' menu item under View MT and SwiftViewer sub menu.
            :param acm_obj: Settlement or confirmation object
            :param subMenu: Viewer sub menu
            :param generate_under: menu item to decide under swiftviwer or text viewer.
            :return:
            """

            external_object_for_699 = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj,
                                                                                             integration_type='Outgoing',
                                                                                             msg_typ='MT699')
            if external_object_for_699:
                subMenu.AddItem(self.view_mt_settl_conf_outgoing_msg, [generate_under, external_object_for_699],
                                "View %s" % external_object_for_699.IntegrationSubtype())

        def show_bpr(self, eii):
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_object = cell.RowObject()
                        ext_obj = eii
                        if ext_obj:
                            bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
                            if bpr:
                                acm.StartApplication("Business Process Details", bpr)
                        else:
                            bpr = FSwiftMLUtils.get_business_process(acm_object, "Outgoing")
                            if bpr:
                                acm.StartApplication("Business Process Details", bpr)
            except Exception, e:
               notifier.ERROR("Exception occurred in SubMenuItem.show_bpr : %s" % str(e))

        def view_mt_settlement_preview_msg(self, eii):  # copied from _view_mt_conf_msg
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        msg_list = []
                        settl_obj = cell.RowObject()
                        isSwiftViewerGUI = eii[0]
                        typ_of_msg = eii[1]
                        if typ_of_msg:
                            msg_list.append(typ_of_msg)
                        else:
                            typ_of_msg = str(FSwiftMLUtils.calculate_mt_type_from_acm_object(settl_obj))
                            msg_list.append(typ_of_msg)
                        for raw_msg_type in msg_list:
                            msg_format_type = swift_format_of_message(raw_msg_type)
                            integration_sub_type = raw_msg_type
                            if msg_format_type == 'MT':
                                integration_sub_type = 'MT' + raw_msg_type
                            msg_type = raw_msg_type.split('-')[0]
                            if swift_format_of_message(msg_type) == 'MT':
                                msg_type = 'MT' + str(msg_type)
                            else:
                                msg_type = str(msg_type)

                            msg_config = FSwiftMLUtils.Parameters('F%sOut_Config' % (msg_type))
                            use_operations_xml = getattr(msg_config, 'UseOperationsXML', 'False')
                            if use_operations_xml == 'True':
                                xml_str = FSettlementXML(settl_obj).GenerateXmlFromTemplate()
                                meta_data_xml_dom = dom.parseString(xml_str)
                                swift_message, mt_py_object, exceptions, getter_values = generate_swift_message(settl_obj, integration_sub_type, meta_data_xml_dom)
                            else:
                                swift_message, mt_py_object, exceptions, getter_values = generate_swift_message(settl_obj, integration_sub_type)
                            if swift_message:
                                swift_data = swift_message
                                mt_msg_type = msg_type
                                if isSwiftViewerGUI == 'SwiftViewer':
                                    do_not_navigate = True
                                    FSwiftViewerGui.ReallyStartApplication(self.m_extObj, (settl_obj, swift_data, False, mt_msg_type, None, do_not_navigate))
                                else:
                                    temp_dir = tempfile.gettempdir()
                                    out_file = os.path.join(temp_dir, '%s_PreviewOutgoing.txt' % (str(mt_msg_type)))
                                    f = open(out_file, 'w')
                                    f.write(swift_data)
                                    f.close()
                                    os.startfile(out_file)
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.view_mt_settlement_preview_msg : %s" % str(e))

        def view_mt_settl_conf_outgoing_msg(self, eii):  # copied from _view_mt_conf_msg
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        isSwiftViewerGUI = eii[0]
                        ext_obj = eii[1]
                        if ext_obj:
                            swift_data = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
                            mt_msg_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_obj)
                        else:
                            swift_data, mt_msg_type = FSwiftMLUtils.swift_data_and_mt_type(acm_obj)
                        # adding snippet to show 199(103) and 299(202) messages together.
                        # if mt_msg_type in ['MT103', 'MT199', 'MT202', 'MT299', '202COV']:
                        #    FSwiftMLUtils.show_mt_message_on_file_or_viewergui(eii,acm_obj,self.m_extObj,mt_msg_type)
                        if isSwiftViewerGUI == 'SwiftViewer':
                            integration_type = 'SwiftWriter'

                            FSwiftViewerGui.ReallyStartApplication(self.m_extObj, (acm_obj, swift_data, False, mt_msg_type, integration_type))
                        else:
                            temp_dir = tempfile.gettempdir()
                            out_file = os.path.join(temp_dir, '%s_Outgoing.txt' % (mt_msg_type))
                            temp_file = open(out_file, 'w')
                            temp_file.write(swift_data)
                            temp_file.close()
                            os.startfile(out_file)
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.view_mt_settlement_outgoing_msg : %s" % str(e))

        def open_mt699(self, eii):
            """ Open MT699 GUI
            :return:
            """
            try:
                import MT699GUI
            except ImportError:
                return
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        MT699GUI.StartDialog(eii, acm_obj)
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.open_mt699 : %s" % str(e))

        def open_mtX99(self, eii):
            """ Open MTX99 GUI
            :return:
            """
            try:
                import FMTNarrativeMessageGUI
            except ImportError:
                return
            try:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        FMTNarrativeMessageGUI.StartDialog(eii, acm_obj)
            except Exception, e:
                notifier.ERROR("Exception occurred in SubMenuItem.open_mt699 : %s" % str(e))

        def __get_msg_type_for_preview(self, settl_obj):
            msg_list = []
            typ_of_msg = str(FSwiftMLUtils.calculate_mt_type_from_acm_object(settl_obj))
            msg_list.append(typ_of_msg)
            if typ_of_msg in ('199', '299', '202COV', '192'):
                bFCashOutMain = True
                try:
                    import FCashOutMain
                except Exception, e:
                    bFCashOutMain = False
                if settl_obj.Children():
                    for child_obj in settl_obj.Children():
                        typ_of_child_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(child_obj)
                        if bFCashOutMain and FCashOutMain.message_type_and_corresponding_messages.get(typ_of_child_msg):
                            msg_list = []
                            dict = FCashOutMain.message_type_and_corresponding_messages.get(typ_of_child_msg)
                            if typ_of_msg in ('199'):
                                msg_list.extend([v[0] for v in dict.values()])
                                msg_list.extend(dict.keys())
                            elif typ_of_msg in ('192'):
                                msg_list.extend([v[1] for v in dict.values()])
                        else:
                            msg_list.append(typ_of_child_msg)
                else:
                    if bFCashOutMain:
                        msg_list = FCashOutMain.message_type_and_corresponding_messages.get(typ_of_msg).keys()
            return msg_list

except Exception, e:  # RTS22 uses 'import FSwiftWriterUtils' but on 16.1 SubMenu is not available hence import fails
    pass


def handle_pyxb_exceptions(exception_dict, set_method, error):
    # call the 'details' method to get the extra detailed pyxb message
    error_text = None
    if getattr(error, 'details', None):
        error_text = str(error.details())
        exception_dict[set_method] = error_text
    else:
        notifier.ERROR("Exception in %s : %s" % (set_method, str(error)))
    notifier.DEBUG(str(error), exc_info=1)
    # if not 'GENERATIONFAILED' in exception_dict.keys():
    # exception_dict['GENERATIONFAILED'] = 'Message generation failed'


def linked_external_objects(active_sheet):
    linked_ext_items = []
    try:
        if active_sheet:
            for cell in active_sheet.Selection().SelectedCells():
                if cell.IsHeaderCell():
                    acm_object = cell.RowObject()
                    if acm_object and (acm_object.IsKindOf(acm.FConfirmation) or acm_object.IsKindOf(acm.FSettlement)):
                        # ext_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object()
                        ext_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_object, integration_type='Outgoing')
                        if ext_item:
                            linked_ext_items.append(ext_item)
    except Exception, e:
        notifier.ERROR("Exception occurred in linked_external_objects : %s" % str(e))
    return linked_ext_items


def get_external_obj_for_amb_msg_id(msg_id):
    ext_objs = FExternalObject.ExtReferences(sourceKey=msg_id, sourceType='AMB_MSG_ID')
    return ext_objs[0]

"""
-------------------------------------------------------------------------------------------------
Below are functions copied from Operations codebase.
-------------------------------------------------------------------------------------------------
"""
try:
    # from FSettlementEnums import SettlementStatus
    SettlementStatus = FSwiftOperationsAPI.GetSettlementStatusEnum()
except:
    pass
try:
    # from FConfirmationEnums import ConfirmationStatus
    ConfirmationStatus = FSwiftOperationsAPI.GetConfirmationStatusEnum()
except:
    pass
try:
    # from FOperationsDocumentEnums import OperationsDocumentStatus
    OperationsDocumentStatus = FSwiftOperationsAPI.GetOperationsDocumentStatusEnum()
except:
    pass


def InDocumentCreationStatus(fObject):
    try:
        # import FSwiftOperationsAPI
        return FSwiftOperationsAPI.InDocumentCreationStatus(fObject)
    except ImportError, e:
        if fObject.IsKindOf(acm.FSettlement):
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                if fObject.Status() in [SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
                    return True
            else:
                if fObject.Status() in ['Released', 'Pending Cancellation']:
                    return True
        if fObject.IsKindOf(acm.FConfirmation):
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                if fObject.Status() == ConfirmationStatus.PENDING_DOCUMENT_GENERATION:
                    return True
            else:
                if fObject.Status() == 'Pending Document Generation':
                    return True
        return False


def IsMissingMTDocument(fObject):
    try:
        # import FSwiftOperationsAPI
        return FSwiftOperationsAPI.IsMissingMTDocument(fObject)
    except ImportError, e:
        isMissing = True
        mt = fObject.MTMessages()
        if FSwiftMLUtils.get_acm_version() >= 2016.4:
            if fObject.Status() == SettlementStatus.PENDING_CANCELLATION and mt in ['292', '192']:
                return isMissing
        else:
            if fObject.Status() == 'Pending Cancellation' and mt in ['292', '192']:
                return isMissing
        for document in fObject.Documents():
            if (mt == str(document.SwiftMessageType())):
                isMissing = False
        return isMissing


def InSendDocumentStatus(fObject):
    try:
        # import FSwiftOperationsAPI
        return FSwiftOperationsAPI.InSendDocumentStatus(fObject)
    except ImportError, e:
        if fObject.IsKindOf(acm.FSettlement):
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                if fObject.Status() in [SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
                    return True
            else:
                if fObject.Status() in ['Released', 'Pending Cancellation']:
                    return True
        if fObject.IsKindOf(acm.FConfirmation):
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                if fObject.Status() == ConfirmationStatus.RELEASED:
                    return True
            else:
                if fObject.Status() == 'Released':
                    return True
        return False


def InOperationsDocumentCreationStatus(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        return fObject.IsPreReleased()
    return False


def ShouldDocumentsBeDeleted(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        if FSwiftMLUtils.get_acm_version() >= 2016.4:
            if fObject.IsPreReleased() or fObject.Status() in [SettlementStatus.VOID, SettlementStatus.RELEASED, SettlementStatus.PENDING_CANCELLATION]:
                return True
        else:
            if fObject.IsPreReleased() or fObject.Status() in ['Void', 'Released', 'Pending Cancellation']:
                return True
    if fObject.IsKindOf(acm.FConfirmation):
        if FSwiftMLUtils.get_acm_version() >= 2016.4:
            if fObject.Status() in [ConfirmationStatus.MANUAL_MATCH, ConfirmationStatus.PENDING_DOCUMENT_GENERATION]:
                return True
        else:
            if fObject.Status() in ['Manual Match', 'Pending Document Generation']:
                return True
    return False


def RemoveOperationsDocument(settlementOrConfirmation):

    if settlementOrConfirmation.Status() == "Pending Cancellation":
        return RemoveOperationsDocumentPendingCancellation()
    else:
        return RemoveOperationsDocumentDefault(settlementOrConfirmation)


def RemoveOperationsDocumentDefault(settlementOrConfirmation):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    orNode = query.AddOpNode('OR')

    if settlementOrConfirmation.IsKindOf(acm.FSettlement):
        query.AddAttrNode('Settlement.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    if settlementOrConfirmation.IsKindOf(acm.FConfirmation):
        query.AddAttrNode('Confirmation.Oid', 'EQUAL', settlementOrConfirmation.Oid())
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.EXCEPTION)
        orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SEND_FAILED)
        orNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.GENERATED)
        orNode.AddAttrNode('Status', 'EQUAL',
                           OperationsDocumentStatus.PENDING_GENERATION)  # Since we are changing the OperationDocumentStatus to PENDING_GENERATION
    else:
        orNode.AddAttrNode('Status', 'EQUAL', 'Exception')
        orNode.AddAttrNode('Status', 'EQUAL', 'Send failed')
        orNode.AddAttrNode('Status', 'EQUAL', 'Generated')
        orNode.AddAttrNode('Status', 'EQUAL',
                           'Pending generation')  # Since we are changing the OperationDocumentStatus to PENDING_GENERATION
    AddCancellationNodeTree(orNode)
    return RemoveAckedOpdocsThatAreCancelled(query.Select(), settlementOrConfirmation)


def RemoveOperationsDocumentPendingCancellation():
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    orNode = query.AddOpNode('OR')
    AddCancellationNodeTree(orNode)
    return query.Select()


def AddCancellationNodeTree(parentNode):
    """Tree for finding operations documents belonging to n92 settlements no
    matter if they failed or were successful. This search is needed in order to
    clean opdocs before resending the settlement in status Release/Pending Cancellation."""
    cancellationNode = parentNode.AddOpNode('AND')
    cancellationStatusNode = cancellationNode.AddOpNode('OR')
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        cancellationStatusNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SEND_FAILED)
        cancellationStatusNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)
    else:
        cancellationStatusNode.AddAttrNode('Status', 'EQUAL', 'Send failed')
        cancellationStatusNode.AddAttrNode('Status', 'EQUAL', 'Sent successfully')
    cancellationMtsNode = cancellationNode.AddOpNode('OR')
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 192)
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 192199)
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 292)
    cancellationMtsNode.AddAttrNode('SwiftMessageType', 'EQUAL', 292299)


def RemoveAckedOpdocsThatAreCancelled(selection, rec):
    """Deployed selection-list will be extended with already cancelled opdocs.
    Applies only for settlements."""
    if not rec.IsKindOf(acm.FSettlement):
        return selection
    ackedMTs = []
    cancellationMTs = []
    for opdoc in rec.Documents():
        if (FSwiftMLUtils.get_acm_version() >= 2016.4 and opdoc.Status() == OperationsDocumentStatus.SENT_SUCCESSFULLY) or opdoc.Status() == 'Sent successfully':
            if str(opdoc.SwiftMessageType()).find("92") > -1:
                cancellationMTs.append(opdoc)
            else:
                ackedMTs.append(opdoc)

    if len(ackedMTs) <= len(cancellationMTs):
        # match so that already sent MT is cancelled, then it is ok to remove opdoc
        for mtOrig in ackedMTs:
            if mtOrig not in selection:
                selection.Add(mtOrig)

    return selection


def ZlibAndHex(data):
    """This method needs to be removed"""
    return data.encode("zlib").encode("hex")


def compress_and_hex_xml(xml_str, ops_document):
    compressed_xml = ZlibAndHex(xml_str)
    ops_document.Data(compressed_xml)
    ops_document.Size(len(compressed_xml))
    return ops_document


def CreateOperationsDocument(documentStatus, messageType, documentId, \
                             statusExplanation, xml, documentType, \
                             settlementOrConfirmation):
    """This method needs to be removed"""
    document = None
    try:
        document = acm.FOperationsDocument()

        document.Status(documentStatus)
        document.DocumentId(documentId)
        document.StatusExplanation(statusExplanation)
        if type(messageType) is str: #FOR MT202COV or MT103REM, the messageType comes as 202COV, 103REM; hence fetching only numeric part
            strMessageType = messageType
            try:
                if swift_format_of_message(strMessageType) == 'MT':
                    messageType = int(strMessageType[0:3])
                else:
                    messageType = int(strMessageType[-2:])
            except Exception, e:
                raise Exception('Invalid SwiftMessageType <%s>, inferred from original messageType <%s>' % (strMessageType[0:3],strMessageType))
        document.SwiftMessageType(messageType)
        document.Type(documentType)
        document.Data("")
        document.Size(len(""))
        document.Protection(settlementOrConfirmation.Protection())
        document.Owner(settlementOrConfirmation.Owner())

        if settlementOrConfirmation.IsKindOf(acm.FSettlement):
            document.Settlement(settlementOrConfirmation)
        elif settlementOrConfirmation.IsKindOf(acm.FConfirmation):
            document.Confirmation(settlementOrConfirmation)

        if (settlementOrConfirmation.IsKindOf(acm.FConfirmation) and settlementOrConfirmation.IsApplicableForSWIFT()):
            document = compress_and_hex_xml(xml, document)
    except Exception, exception:
        raise Exception('Failed to create FOperationsDocument %s' % str(exception))
    return document


def exceptions_as_string(exceptions_dict):
    exceptions_str = ''
    for exceptions in exceptions_dict:
        #if exceptions != 'GENERATIONFAILED':
        exceptions_str += exceptions + ' : ' + exceptions_dict[exceptions] + '\n'
    return exceptions_str


def get_external_object_for_acm_object(acm_obj):
    external_objs = []
    # ext_obj = FExternalObject.FExternalObject()
    external_objs = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, all_records=True)
    # external_objs = FExternalObject.ExtReferences(subject=acm_obj)
    if not external_objs:
       notifier.ERROR("No External Object found for %s:%s" % (acm_obj.RecordType(), acm_obj.Oid()))
    return external_objs


def get_subtype_from_ext_obj(ext_obj):
    return FSwiftMLUtils.FSwiftExternalObject.get_integration_sub_type(ext_obj)


def get_stored_data_from_ext_obj(ext_obj, sub_typ):
    return FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, sub_typ)


def get_operations_xml(acm_obj):
    if acm_obj.IsKindOf(acm.FConfirmation):
        return FConfirmationXML(acm_obj).GenerateXmlFromTemplate()
    if acm_obj.IsKindOf(acm.FSettlement):
        return FSettlementXML(acm_obj).GenerateXmlFromTemplate()


def create_business_process_for_parent(fObject, sc):
    """
    This method creates a parent business process which will be driven by its children BPRs
    return : bpr object
    """
    # For MT202COV, parent BPR is created for same settlement as that of children
    notifier.DEBUG("Creating external object and business process for parent")
    value_dict = {'swift_data': ''}
    if fObject.IsKindOf(acm.FConfirmation):
        fObject_type = 'Confirmation'
    if fObject.IsKindOf(acm.FSettlement):
        fObject_type = 'Settlement'
    external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(value_dict, 'FSwiftParent', fObject_type, fObject, "Outgoing")
    # external_obj.Subject(fObject)
    # external_obj.Commit()
    # reconciliation_item = external_obj.ReconciliationItem()
    # create a business process on the recon item
    business_pro = FSwiftMLUtils.get_or_create_business_process(external_obj, sc, '', create_for='Outgoing')
    # Adding Settlement/Conf Id to diary

    # subject_id = business_pro.Subject().Subject().Oid()
    subject_id = fObject.Oid()
    # subjectType = 'SettlementId' if business_pro.Subject().Subject().IsKindOf(acm.FSettlement) else 'ConfirmationId'
    subjectType = 'SettlementId' if fObject.IsKindOf(acm.FSettlement) else 'ConfirmationId'
    entry = business_pro.Diary().GetEntry(business_pro, business_pro.CurrentStep())
    note = subjectType + ": " + str(subject_id)
    entry.Notes([note])
    business_pro.Diary().PutEntry(business_pro, business_pro.CurrentStep(), entry)
    business_pro.Commit()

    notifier.INFO("Created business process %s for message generation on %s %s" % (str(business_pro.Oid()), fObject_type, str(fObject.Oid())))
    return business_pro


def create_business_process_for(fObject, mtType, sc, diary_text='', raw_mt_type='',parent_bpr=''):
    notifier.DEBUG("{0} Creating external object and business process".format(mtType))
    value_dict = {'swift_data': ''}
    
    if fObject.IsKindOf(acm.FConfirmation):
        fObject_type = 'Confirmation'
    elif fObject.IsKindOf(acm.FSettlement):
        if is_unsupported_settlement(fObject) or was_previously_released_by_adaptiv(fObject, mtType):
            message = "{object_type} with ID {id}, should be handled by adaptiv, "
            message += "skipping Business Process creation."
            notifier.INFO(message.format(object_type=fObject.RecordType(), id=fObject.Oid()))
            return
        fObject_type = 'Settlement'
    elif fObject.IsKindOf(acm.FParty):
        fObject_type = 'Party'
    elif fObject.IsKindOf(acm.FTrade):
        fObject_type = 'Trade'
    else:
        notifier.INFO("%s Object is not supported for business process creation" % fObject.RecordType())
        return
    external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(value_dict, mtType, fObject_type, fObject, "Outgoing", raw_mt_type=raw_mt_type,parent_bpr=parent_bpr)
    # create a business process on the recon item
    business_pro = FSwiftMLUtils.get_or_create_business_process(external_obj, sc, mtType, create_for='Outgoing')
    # Adding Settlement/Conf Id to diary
    subject_id = fObject.Oid()
    subjectType = 'SettlementId' if fObject.IsKindOf(acm.FSettlement) else 'ConfirmationId'
    entry = business_pro.Diary().GetEntry(business_pro, business_pro.CurrentStep())
    note = subjectType + ": " + str(subject_id)
    if diary_text:
        if isinstance(diary_text, dict):
            entry.Parameters(diary_text)
        else:
            entry.Parameters({'NarrativeText': diary_text})
    if parent_bpr:
        note = note + '\n' + "Parent BPR Id : " + str(parent_bpr.Oid())
    entry.Notes([note])
    business_pro.Diary().PutEntry(business_pro, business_pro.CurrentStep(), entry)
    business_pro.Commit()

    notifier.INFO("%s Created business process %s for %s message generation on %s %s" % (
        mtType, str(business_pro.Oid()), str(mtType), fObject_type, str(fObject.Oid())))
    return business_pro


def is_valid(val):
    if val in [None, {}, [], '', 'DoNotMap']:
        return False
    if type(val) == type({}):
        # This is to handle cases of dicts like {'bic':'', 'account':''}
        atleast_one_value_present = False
        for _, value in val.iteritems():
            if value:
                atleast_one_value_present = True
                break
        return atleast_one_value_present
    return True


def get_option_value(key, fObject):
    option = ''
    mt = get_mt_type_from_acm_obj(fObject)
    msg_type = "MT" + str(mt)
    return FSwiftMLUtils.get_party_option(msg_type, key, 'Outgoing')


def is_LAU_Applicable():
    param_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

    enable_encryption = getattr(param_config, 'EnableEncryption', None)

    return (enable_encryption is not None) and ((enable_encryption.upper() == 'TRUE') or (enable_encryption.upper() == 'YES'))


def get_ack_nak_subject():
    """ Read Fparam AckNakSubject from FSwiftWriterConfig. Defalut value ACKNOWLEDGEMENT
    :return: str: AckNakSubject
    """
    swiftwriter_config = get_config_from_fparameter('FSwiftWriterConfig')
    ACK_NAK_Subject = getattr(swiftwriter_config, 'AckNakSubject', None)
    if not ACK_NAK_Subject:
        notifier.INFO("FParameter AckNakSubject is not defined. Setting default ACK NAK message Subject to ACKNOWLEDGEMENT")
        ACK_NAK_Subject = 'ACKNOWLEDGEMENT'
    return ACK_NAK_Subject


def encrypt_message(swift_message):
    encrypt_dict = {'MessageEncrypted': 'No'}

    if is_LAU_Applicable():
        lau_signature = FSwiftMLUtils.get_LAU_signature(swift_message)
        if lau_signature is not None:
            swift_message = str(swift_message) + '{S:{MDG:' + lau_signature + '}}'
            encrypt_dict['MessageEncrypted'] = 'Yes'

    return swift_message, encrypt_dict


def process_aditional_delimiter(swift_msg):
    if swift_msg:
        swift_msg = swift_msg.replace('\r\n', '\n')
        swift_msg = swift_msg.replace('\n', '\r\n')
        return swift_msg


def is_outgoing_message_supported(mt_type):
    try:
        mt_mx_type = mt_type.strip('MT')
        if swift_format_of_message(mt_mx_type) == 'MT':
            mt_mx_type = "MT" + mt_mx_type

        if mt_mx_type in ['MT299COV', 'MT292COV']:
            mt_mx_type = mt_mx_type[:-3]

        fparam_name = 'F%sOut_Config' % str(mt_mx_type)
        fparam = get_config_from_fparameter(fparam_name)
    except Exception, e:
        return False
    return True


def get_value_of_fparameter_for(config_name, fparam_name):
    param = get_config_from_fparameter(config_name)
    return getattr(param, fparam_name, False)


def get_module_name(mt_type):
    try:
        """fparam_name = 'F%sOut_Config' % str(mt_type)
        fparam = get_config_from_fparameter(fparam_name)
        return fparam.module_name"""
        import FIntegrationUtils

        module_list = {'FFXMMConfirmationOutMain','FIRDConfirmationOutMain','FCashOutMain','FSecuritySettlementOutMain'
                       ,'FCommodityConfirmationOutMain', 'FCommoditySettlementOutMain',
                       'FSwiftCustomMessageConfirmationOutMain', 'FSwiftCustomMessagesettlementOutMain'}

        swift_writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
        active_modules = eval(getattr(swift_writer_config, 'Modules', []))

        for module in active_modules:
            module_list.add(module)

        for module in module_list:
            try:
                utils_obj = FIntegrationUtils.FIntegrationUtils()
                obj = utils_obj.import_module_from_string(module)
                if mt_type in obj.SUPPORTED_MT_MESSAGE or mt_type in obj.SUPPORTED_MX_MESSAGE:
                    return module[:-4]
            except ImportError:
                pass
    except Exception, e:
        pass


def is_outgoing_message_generation_on_for(mt_type):
    try:
        mt_mx_type = mt_type.strip('MT')
        if swift_format_of_message(mt_mx_type) == 'MT':
            mt_mx_type = "MT" + mt_mx_type

        if mt_mx_type in ['MT292COV', 'MT299COV']:
            mt_mx_type = mt_mx_type[:-3]
        pkg_name = get_module_name(mt_mx_type)
        if pkg_name is None:
            return False
        config_name = pkg_name + 'Generation_Config'
        fparam_name = 'F%s_GenerationOn'% mt_mx_type

        message_generation_on = get_value_of_fparameter_for(config_name, fparam_name)

        return "True" == message_generation_on

    except Exception, e:
        raise Exception("Exception in is_outgoing_message_generation_on_for for %sOut : %s" % (mt_type, str(e)))



def should_message_be_generated_by_adaptivdocs(mt_type):
    value = False
    try:
        mt_mx_type = mt_type.strip('MT')
        if swift_format_of_message(mt_mx_type) == 'MT':
            mt_mx_type = "MT" + mt_mx_type
        if mt_mx_type in ['MT292COV', 'MT299COV']:
            mt_mx_type = mt_mx_type[:-3]
        config_name = 'F%sOut_Config' % mt_mx_type
        fparam_name = 'ShouldBeGeneratedByAdaptivDocs'
        should_be_generated_by_adaptivdocs = get_value_of_fparameter_for(config_name, fparam_name)
        
        if should_be_generated_by_adaptivdocs == "True":
           value = True
         
    except Exception, e:
        raise Exception("Exception in should_message_be_generated_by_adaptivdocs for %sOut : %s" % (mt_type, str(e)))
    return value

def get_swift_status(msg):
    """ Takes value of Swift 451 tag from the message """
    ack_or_nack_flag = int(re.findall(r"{451:(.+?)}", msg)[0])
    if ack_or_nack_flag == 1:
        status = "Nack"
    elif ack_or_nack_flag == 0:
        status = "Ack"
    return status

def get_message_user_reference(swift_data):
    """ Takes value of Swift 108 tag from the message """	
    swift_data = swift_data[swift_data.find('108:') + 4:]
    swift_data = swift_data[:swift_data.find('}')]
    return swift_data


def append_mt_types_added_by_customer(SUPPORTED_MT_MESSAGES, solution_specific_generation_on_config):
    message_generation_on = get_config_from_fparameter(solution_specific_generation_on_config)
    for msg_name, generation_status in vars(message_generation_on).iteritems():
        if 'GenerationOn' not in msg_name:
            continue
        if generation_status == '' or generation_status == 'False':
            continue
        elif generation_status == 'True':
            msg_name = msg_name.split('_')[0]
            msg_name = msg_name[1:]
            if msg_name not in SUPPORTED_MT_MESSAGES:
                SUPPORTED_MT_MESSAGES.append(msg_name)
    return SUPPORTED_MT_MESSAGES


def should_set_document_status(acm_obj):
    Ack = True
    ext_objs = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_obj, integration_type='Outgoing')
    for ext_obj in ext_objs:
        bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
        if bpr.CurrentStateName() != 'Acknowledged':
            Ack = False
            break
    return Ack


def create_swift_msg_from_pyobj(pyObject, swiftFormat='ISO15022'):
    """Input
        python object for which swift message is to be generated
        parameter swiftFormat decides the type of output.
       Output
        swiftForamt ISO20022 returns XML form of swift message
        swiftForamt ISO15022 returns text format of swift message which is by default provided
    """
    obj = FSwiftML.FSwiftML()
    if swiftFormat == 'ISO20022':
        return obj.pyobject_to_xml(pyObject)
    elif swiftFormat == 'ISO15022':
        return obj.pyobject_to_swift(pyObject)
    else:
        return "The provided swift format is not correct. Please provide either ISO15022 or ISO20022"


def create_pyobj_from_swift_msg(swiftMsg):
    """Input
        swift message for which python object is to be generated
       Output
        Python Object
    """
    obj = FSwiftML.FSwiftML()
    try:
        dom.parseString(swiftMsg)
        return obj.xml_to_pyobject(swiftMsg)
    except xml.parsers.expat.ExpatError:
        try:
            return obj.swift_to_pyobject(swiftMsg)
        except Exception, e:
            raise Exception("Error while converting Swift message to Pyobject: %s" % str(e))
    except Exception, e:
        raise Exception(str(e))


def get_acmobj_subtyp_msgtyp(context):
    acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(context.CurrentStep().BusinessProcess())
    sub_typ = FSwiftMLUtils.FSwiftExternalObject.get_integration_sub_type(context.CurrentStep().BusinessProcess().Subject())
    msg_type = 'MT' + str(FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj))
    return acm_obj, sub_typ, msg_type


def get_max_commit_retries():
    swift_writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
    max_retries = getattr(swift_writer_config, 'BPRCommitRetry', 3)
    return max_retries


def format_narrative_retaining_user_fomatting(narrtive_text):
    """ Format accoding to swift specification by keeping user newline characters in the formatted text.
    """
    text = []
    narrative = narrtive_text.split('\n')
    formatted_narrative = ''
    try:
        for values in narrative:
            if values == "":
                line = ['\n']
            else:
                line = split_text_on_character_limit(values, 35)
            text.extend(line)
        formatted_text = ""
        for i in text:
            formatted_text += i
            if i != '\n':
                formatted_text += '\n'

        formatted_narrative = '\n '.join(formatted_text.split('\n')[:50])
    except Exception as e:
        notifier.ERROR(
            "Error in formatting narrative tag: %s. Sending original text " % (str(e)))
    if not formatted_narrative:
        formatted_narrative = narrtive_text
    return formatted_narrative

def save_user_data_as_ext_obj(user_data, parent_ext_obj):
    """ Create external object save user data into it and attach new external object as child to external object on
    acm object. Delete existing child on the parent external object.
    :param user_data: user data dictionary
    :param parent_ext_obj: external object on acm object
    :return: new external object
    """
    user_data_dict = {'CustomData': user_data}
    user_data_ext_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(user_data_dict, "CustomData",
                                                                                  in_or_out="Outgoing")

    for child_obj in parent_ext_obj.Children():
        child_obj.Delete()
    FSwiftMLUtils.FSwiftExternalObject.set_ext_obj_parent(user_data_ext_obj, parent_ext_obj)
    return user_data_ext_obj


def get_custom_data_on_child_external_object(ext_obj):
    """
    :param ext_obj:
    :return:
    """
    custom_data = dict()
    if ext_obj and ext_obj.Children():
        child = ext_obj.Children()[0]
        custom_data = ast.literal_eval(child.Data().Text())
    return custom_data


def get_mt_pyobject_from_confirmation(confirmation):
    """ Get python object for MT class for confirmation. MT class is obtained from the calculator.
    :param confirmation: FConfirmation object
    :return: python object for MT class.
    """
    mt_swift_py_obj = None
    custom_data = dict()
    if confirmation:
        if confirmation.IsInfant() and confirmation.Oid() < 0:
            mt_type = get_mt_type_from_acm_obj(confirmation)
            if mt_type:
                mt_type = "MT" + str(mt_type)
                fmt_class_obj = FSwiftWriterMTFactory.FSwiftWriterMTFactory.create_fmt_object(
                    confirmation, mt_type,
                    swift_metadata_xml_dom=None)
                engine_object = SwiftWriterEngine(fmt_class_obj)
                engine_object.map_attributes()
                if engine_object._swift_python_object():
                    mt_swift_py_obj = engine_object._swift_python_object()
                    custom_data = fmt_class_obj.get_user_data()
            else:
                notifier.INFO("Unable to get MT type for infant confirmation. MT pyobject will not be created.")
        else:
            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=confirmation,
                                                                             integration_type='Outgoing')
            swift_data = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, "swift_data")
            ml_utils_obj = FSwiftML.FSwiftML()
            mt_swift_py_obj = ml_utils_obj.swift_to_pyobject(swift_data)
            custom_data = get_custom_data_on_child_external_object(ext_obj)
    else:
        notifier.INFO("Confirmation object not provided. Please provide FConfirmation object.")

    return mt_swift_py_obj, custom_data

def apply_rounding(currency, amount):
    """ Round decimal amount according to the precision for a currency stated in Fparameter: RoundPerCurrency in FSwiftWriterConfig """
    import FCashOutUtils
    result = FCashOutUtils.apply_currency_precision(currency, amount)
    return result
