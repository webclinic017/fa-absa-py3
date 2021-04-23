"""----------------------------------------------------------------------------
MODULE:
    FCashOutUtils

DESCRIPTION:
    A module for common functions used across Cash outgoing
    solution.

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import pyxb
from pyxb.exceptions_ import ValidationError
import FSwiftMLUtils
import FSwiftWriterUtils
import re
import ast
import os
import acm
import tempfile
import FUxCore
import xml.dom.minidom as dom
from functools import wraps
import FSwiftWriterLogger
import itertools
from FSettlementXML import FSettlementXML
import FSwiftOperationsAPI
from FMTSettlementWrapper import FMTSettlementWrapper
import FIntegrationUtils

notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSettlemnt', 'FCashOutNotify_Config')
cash_settlement_out_config = FSwiftMLUtils.Parameters('FCashOut_Config')

try:
    #from FSettlementEnums import RelationType, SettlementStatus
    RelationType = FSwiftOperationsAPI.GetRelationTypeEnum()
    SettlementStatus = FSwiftOperationsAPI.GetSettlementStatusEnum()
    DocumentStatus = FSwiftOperationsAPI.GetOperationsDocumentStatusEnum()
except:
    pass

from FSwiftSettlementWrapper import FSwiftSettlement
writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

class PreviewOutgoingMTMsgCashSettlementMenuItem(FUxCore.MenuItem):
    """MenuItem for displaying outgoing message from confirmation object"""
    def __init__(self, eii, state_chart_names):
        self._eii = eii
        if type(state_chart_names) == type([]):
            self.state_chart_names = state_chart_names
        else:
            self.state_chart_names = [state_chart_names]
        self.active_sheet = FSwiftMLUtils.get_active_sheet(eii)

    def Enabled(self):
        return True

    def Invoke(self, _eii):
        self._view_mt_settlement_msg()

    def Applicable(self):
        return self._is_enabled()

    def _is_enabled(self):
        """
        Method is to check whether particular submenu should be activated for particular object (sett/conf/bpr)
        :return: None
        """
        typ_of_msg = ''
        is_enabled = False
        try:
            if self.active_sheet:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj)
                        if acm_obj.Status() == 'Authorised' and typ_of_msg != '0':
                            #bpr_obj = FSwiftMLUtils.get_business_process(acm_obj)
                            #if bpr_obj:
                            is_enabled = True
                            break
        except Exception as e:
            mt_type = "MT" + str(typ_of_msg)
            notifier.ERROR("%s Exception occurred in PreviewOutgoingMTMsgCashSettlementMenuItem._is_enabled : %s" % (mt_type, str(e)))
        return bool(is_enabled)

    def _view_mt_settlement_msg(self):
        """
        Method to show MT message associated with a settlement
        :return: None
        """
        msg_type = ''
        try:
            for cell in self.active_sheet.Selection().SelectedCells():
                if cell.IsHeaderCell():
                    msg_list = []
                    settl_obj = cell.RowObject()
                    typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(settl_obj)
                    msg_list.append(typ_of_msg)
                    if typ_of_msg in ('199', '299'):
                        if settl_obj.Children():
                            for child_obj in settl_obj.Children():
                                typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(child_obj)
                                msg_list.append(typ_of_msg)
                    for msg_type in msg_list:
                        msg_type = 'MT' + str(msg_type)
                        msg_config = FSwiftMLUtils.Parameters('F%sOut_Config'%(msg_type))
                        use_operations_xml = getattr(msg_config, 'F%sOut_UseOperationsXML'%(msg_type))
                        if use_operations_xml:
                            xml_str = FSettlementXML(settl_obj).GenerateXmlFromTemplate()
                            meta_data_xml_dom = dom.parseString(xml_str)
                            swift_message, mt_py_object, exceptions, getter_values = FSwiftWriterUtils.generate_swift_message(settl_obj, msg_type, meta_data_xml_dom)
                        else:
                            swift_message, mt_py_object, exceptions, getter_values = FSwiftWriterUtils.generate_swift_message(settl_obj, msg_type)
                        if not exceptions:
                            swift_data = swift_message
                            mt_msg_type = msg_type
                            temp_dir = tempfile.gettempdir()
                            out_file = os.path.join(temp_dir, '%s_PreviewOutgoing.txt'%(str(mt_msg_type)))
                            f = open(out_file, 'w')
                            f.write(swift_data)
                            f.close()
                            os.startfile(out_file)
        except Exception as e:
            notifier.ERROR("%s Exception occurred in PreviewOutgoingMTMsgCashSettlementMenuItem._view_mt_settlement_msg : %s" % (msg_type, str(e)))

def create_preview_outgoing_mt_msg_cash_settlement_menuitem(eii):
    """
    :param eii: shell object passed from FMenuExtension
    :return: object of class handling the menu
    """
    return PreviewOutgoingMTMsgCashSettlementMenuItem(eii, ['FSwiftCashOut'])

def decorate_all_setter(setter_method):
    """
    Class decorator method for decorating all callable attributes of class and
    returns a decorated method, decorated with setter_method , in this case
    :param setter_method: method to be decorated
    :return: Decorated method
    """
    def decorator(cls):
        for name, obj in list(vars(cls).items()):
            if callable(obj):
                try:
                    obj = obj.__func__
                except AttributeError:
                    pass
                setattr(cls, name, setter_method(obj))
        return cls
    return decorator

def call_setter_validator(func):
    """
    Method to call validator of a setter method after setter method is called.
    :param func: method to be decorated
    :return: decorated method
    """
    @wraps(func)
    def wrapper(*args, **kw):
        res = None
        if func.__name__ and func.__name__.startswith('set_') and func.__name__ not in ['set_attributes']:
            validation_method = 'validate_' + func.__name__.replace('set_', '')  # Generating name for validator method
            try:
                res = func(*args, **kw)  # Calling Setter method
                getattr(args[0], validation_method)()  # Calling validator method
            except AttributeError:  # If validator method is not implemented, it is ignored
                pass
        else:
            res = func(*args, **kw)
        return res
    return wrapper

def get_message_version_number(fObject, is_free_text_msg = False, child_mt_type=''):
    '''
    Method to get the message version number
    :param fObject: object from which message version number is to be fetched
    :param is_free_text_msg: flag indicating is_free_text_msg
    :return: message version number
    '''
    msg_version_number = fObject.VersionId()
    if is_free_text_msg:
        msg_version_number = str(msg_version_number)
        if child_mt_type and child_mt_type in ['MT199', 'MT299']:
            msg_version_number = str(msg_version_number) + 'F'
    return str(msg_version_number)

def validateAmount(amt, length, field):
    """
    Method to validate the amount field to be sent in the outgoing MT message
    :param amt: amount
    :param length:
    :param field:
    :return: Validation_error is 'amt' is invalid as per swift spec.
    """
    #amt should be in the swift format i.e. should contain one mandatory decimal comma
    validation_errors = []
    if str(amt).count(',') != 1:
        validation_errors.append('%s field must contain one decimal comma.' %field)
    if len(str(amt)) > length:
        validation_errors.append('Length of %s field should not be more than %s.'%(field, length))

    if validation_errors:
        raise ValidationError(message = ''.join(validation_errors))


def get_amount_from_currency_amount(currency_amount):
    """
        1. takes the currency amount as input
        2. parse the input using regex
        3. check if N is present at the start of input,
                a. if present, replaces comma(,) with dot(.) in the amount field and returns the negative of amount
                b. if not present, replaces comma(,) with dot(.) in the amount field and returns the amount
    """
    parsed_data = re.findall(r'([N])?[A-Za-z][A-Za-z][A-Za-z](.+)', currency_amount)[0]
    if parsed_data[0] == 'N':
        return '-' + parsed_data[1].replace(',', '.')
    elif parsed_data[0] == '':
        return parsed_data[1].replace(',', '.')


def get_currency_from_currency_amount(currency_amount):
    """
        1. takes the currency amount as input
        2. parse the input using regex
        3. returns the currency
    """
    curr = re.findall(r'[N]?([A-Za-z][A-Za-z][A-Za-z]).+', currency_amount)[0]
    return curr


def validate_terms_and_conditions(text, field):
    """ Applicable for MT300.
        If code VALD is used:
            1. it must appear in the first 6 characters of the first line, and in no other place, followed by a date expressed as YYYYMMDD
                and the end of line separator (that is  :77D:/VALD/YYYYMMDDCrLf)  (Error code(s): C58).
            2. the second line must be present and contain the code SETC, followed by a valid ISO 4217 currency code and the
                end of line separator (that is  /SETC/currencyCrLf) (Error code(s): C59).
        Conversely, if the first six characters of the second line are equal to /SETC/, then the first six characters of the first line must be equal to /VALD/  (Error code(s): C59).
        The code /SETC/ is not allowed in other places than the first six characters of the second line  (Error code(s): C59).
        If the first six characters of the third line are /SRCE/, then the first six characters of the second line must be /SETC/  (Error code(s): C59).
        The code /SRCE/ is not allowed in any other place than the first six characters of the third line  (Error code(s): C59). """
    t_n_c = text.split('\n')
    validation_errors = []
    try:
        assert not (t_n_c[0].startswith('/VALD/') and not t_n_c[1].startswith('/SETC/'))
    except AssertionError:
        validation_errors.append("When /VALD/ appears in first line of %s field, then /SETC/ is mandatory in second line." %field)
    except IndexError:
        if t_n_c[0].startswith('/VALD/'):
            validation_errors.append("When /VALD/ appears in first line of %s field, then /SETC/ is mandatory in second line." %field)
    try:
        assert not (not t_n_c[0].startswith('/VALD/') and '/SETC/' in text)
    except AssertionError:
        validation_errors.append("/SETC/ is not allowed without /VALD/ in the first line of %s field." %field)
    try:
        assert not (not t_n_c[1].startswith('/SETC/') and '/SRCE/' in text)
    except AssertionError:
        validation_errors.append("/SRCE/ is not allowed without /SETC/ in the second line of %s field." %field)
    except IndexError:
        if '/SRCE/' in text:
            validation_errors.append("/SRCE/ is not allowed without /SETC/ in the second line of %s field." %field)
    try:
        if t_n_c[0].startswith('/VALD/'):
            try:
                assert re.findall(r'/VALD/[0-9]{8}', str(t_n_c[0]))
            except AssertionError:
                validation_errors.append("/VALD/ is not followed by a date expressed in YYYYMMDD format in %s field." %field)
    except IndexError:
        pass
    if validation_errors:
        raise ValidationError(message = ''.join(validation_errors))

def validate_slash_and_double_slash(text, field):
    """validates if text start or end with a slash '/' and does not contain two consecutive slashes '//'  (Error code(s): T26)."""
    validation_errors = []
    try:
        assert re.findall(r'^[^/].*?[^/]$', str(text))
    except AssertionError:
        validation_errors.append("%s field must not start or end with a slash '/'." %field)
    try:
        assert not '//' in str(text)
    except AssertionError:
        validation_errors.append("Two consecutive slashes are not allowed in %s field." %field)
    if validation_errors:
        raise ValidationError(message = ''.join(validation_errors))

def validate_currency_amount(currency_amount, field):
    """
    Method to validate currency amount field that is sent in MT message
    :param currency_amount:
    :param field:
    :return: Validation_error is the field is not valid as per swift specification
    """
    validation_errors = []
    try:
        currency_codes_not_allowed = ['XAU', 'XAG', 'XPD', 'XPT']
        for each in currency_codes_not_allowed:
            assert not str(currency_amount).startswith(each)
    except AssertionError:
        validation_errors.append("Currency codes XAU, XAG, XPD and XPT not allowed in %s field." %field)
    if validation_errors:
        raise ValidationError(message = ''.join(validation_errors))

def validate_mt_and_date_of_original_message(value, field):
    """
    Method to validate the MTandDate of original message
    :param value:
    :param field:
    :return: ValidationError if the value is not valid as per swift specification
    """
    validation_error = []
    mt_message = value.split('\n')[0]
    try:
        if not int(mt_message) in range(100, 999):
            validation_error.append("MT Number must be in range 100-200 in %s field." %field)
    except Exception as e:
        notifier.ERROR("Error in validate_mt_and_date_of_original_message : %s "%str(e))

    if validation_error:
        raise ValidationError(message = ''.join(validation_error))


def represent_negative_currency_amount(curr, amount):
    """
        1. takes the currency amount as input
        2. replaces hyphen(-) with N if amount is non zero
        3. removes hyphen(-) if amount is 0
        4. replaces dot(.) with comma(,) in the amount field
        Error code T14
    """
    amount = str(amount)
    if abs(float(amount))>0 and amount.startswith('-'):
        return 'N' + curr + FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))
    else:
        return curr + FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))

def represent_amount_in_four_digits(amount):
    """
        1. take the rightmost non zero digit.
        2. attach 3 digits to the left of it
        3. If there are no digits left then attach 0 to the left till the length is 4
        4. return amount_part of length 4
        Error code T22
    """
    amount_part = []
    got_rightmost_non_zero_digit = False
    for each_char in reversed(amount):
        if each_char not in ['0', '.'] and not got_rightmost_non_zero_digit:
            amount_part.insert(0, each_char)
            got_rightmost_non_zero_digit = True
        elif got_rightmost_non_zero_digit and each_char != '.':
            amount_part.insert(0, each_char)
    while len(amount_part) < 4:
        amount_part.insert(0, '0')
    return ''.join(amount_part[-4:])


def get_swift_status(msg):
    """ takes the value of Swift 451 tag from the message """
    ack_or_nack_flag = int(re.findall(r"{451:(.+?)}", msg)[0])
    if ack_or_nack_flag == 1:
        return "Nack"
    elif ack_or_nack_flag == 0:
        return "Ack"

def get_settlement_number_from_msg(msg):
    """ get settlement number from message field string """
    return msg.split('-')[1]

def apply_currency_precision(curr, amount):
    """ Round decimal amount according to the precision for a currency stated
        in RoundPerCurrency"""

    #fx_trade_conf_out_config = FSwiftMLUtils.Parameters('FFxTradeConfOutgoingMsg_Config')
    swiftwriter_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
    #round_per_currency = ast.literal_eval(fx_trade_conf_out_config.RoundPerCurrency)
    round_per_currency = ast.literal_eval(getattr(swiftwriter_config, 'RoundPerCurrency', "{'EUR':2, 'USD':2, 'JPY':0, 'KRW':0,\
     'TRY':0, 'KWD':3, 'AED':2, 'ARS':2, 'AUD':2, 'BAM':2, 'BRL':2, 'BGN':2, 'CAD':2, 'CNY':2, 'CZK':2, 'DKK':2, 'GBP':2, 'HKD':2,\
      'HRK':2, 'HUF':2, 'ISK':2, 'INR':2, 'IDR':2, 'LVL':2, 'MYR':2, 'MXN':2, 'MXV':2, 'NZD':2, 'NOK':2, 'PHP':2, 'SAR':2, 'SGD':2, 'ZAR':2, 'SEK':2, 'CHF':2, 'TWD':2, 'THB':2}"))
    rounding_precision = round_per_currency.get(curr, 2)
    if rounding_precision == 0:
        amount_to_round = int(amount)
    else:
        amount_to_round = amount
    ret = round(amount_to_round, rounding_precision)
    return ret

def validate_instruction_code(instruction_codes):
    """Unit tests done:
       instruction_code = ['PHON\nABDF', 'PHOD']  - Success
       instruction_code = ['PHON\nABDF', 'PHOB']  - Fail
       instruction_code = ['PHOB', 'PHOI\nsdftrrt', 'TELI'] - Success
       instruction_code = ['TELI', 'SDVA'] - Fail
       instruction_code = ['SDVA', 'CORT', 'TELI'] - Success
       instruction_code = ['INTC', 'HOLD', 'TELE', 'SDVA'] - Fail
       instruction_code = ['INTC', 'HOLD', 'TELE', 'INTC'] - Fail"""

    codes_in_order = ['SDVA', 'INTC', 'REPA', 'CORT', 'HOLD', 'CHQB', 'PHOB', 'TELB', 'PHON', 'TELE', 'PHOI', 'TELI']
    invalid_code_pairs = { 'SDVA' : ['HOLD', 'CHQB'],
                           'INTC' : ['HOLD', 'CHQB'],
                           'REPA' : ['HOLD', 'CHQB', 'CORT'],
                           'CORT' : ['HOLD', 'CHQB'],
                           'HOLD' : ['CHQB'],
                           'PHOB' : ['TELB'],
                           'PHON' : ['TELE'],
                           'PHOI' : ['TELI']}
    codes_and_order = dict(list(zip(codes_in_order, [-1]*len(codes_in_order))))
    for order, code in enumerate(instruction_codes):
        #instruction_code = each
        #code = instruction_code.value()[0:4]
        #code = each
        if code not in ['PHON', 'PHOB', 'PHOI', 'TELE', 'TELB', 'TELI', 'HOLD', 'REPA'] and len(code) > 4:
            raise ValidationError("Additional information is only allowed when Instruction Code consists of one of the following codes: PHON, PHOB, PHOI, TELE, TELB, TELI, HOLD or REPA")
        if code in codes_and_order and codes_and_order[code] != -1:
            raise ValidationError("Code should not be repeated")
        codes_and_order[code] = order
    for index, code1 in enumerate(codes_in_order):
        order_of_code1 = codes_and_order[code1]
        if order_of_code1 != -1:
            for code2 in itertools.islice(codes_in_order, index+1, len(codes_in_order)):
                if codes_and_order[code2] != -1:
                    if order_of_code1 > codes_and_order[code2]:
                        raise ValidationError("Codes must appear in order SDVA, INTC, REPA, CORT, HOLD, CHQB, PHQB, TELB, PHON, TELE, PHOI, TELI")
                    if code2 in invalid_code_pairs[code1]:
                        raise ValidationError("Codes %s and %s are not allowed in combination" % str(code1, code2))

def get_related_settlement(settlement):
    """
    Method to get the related settlement
    :param settlement:
    :return:
    """
    if is_cancellation(settlement):
        return settlement.Children()[0]
    elif is_nak_cancellation(settlement):
        return settlement
    return None

def is_cancellation(settlement):
    if FIntegrationUtils.FIntegrationUtils.get_acm_version() >= 2016.4:
        return settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT]
    else:
        return settlement.RelationType() in ['Cancellation', 'Cancel Correct']

def is_nak_cancellation(settlement):
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        return settlement.Status() == SettlementStatus.PENDING_CANCELLATION
    else:
        return settlement.Status() == 'Pending Cancellation'

def validate_remittance_info(remittance_info):
    exp = re.compile("/(INV|IPI|RFB|ROC|TSU)/")
    if not exp.findall(remittance_info):
        raise ValidationError("One of the codes INV/IPI/RFB/ROC/TSU may be used, placed between slashes")


def split_line_with_limited_characters(text, character_limit, prefix_text=''):
    """
    Split the given string with character limit specified and add given prefix to it.
    :param text: Text to be splitted
    :param character_limit: limit of the each line
    :param prefix_text: prefix to be attached to each line.
    :return: string.
    """
    import textwrap
    line_length = int(character_limit) - int(len(prefix_text))
    str_lines = textwrap.wrap(text, character_limit)
    value_txt = ''
    for line in str_lines:
        value_txt += '\n' + str(prefix_text) + line

    return value_txt.strip('\n')

def get_party_details(party, party_account, intermediary_or_correspondent = None):
    """
    Method to fetch the party details from given party object
    :param party:
    :param party_account:
    :param intermediary_or_correspondent:
    :return: dictionary of party_details
    """
    party_details = {}
    if party_account:
        #The account defined on the same row is an account in that bank, but its held on behalf of the party "above".
        if intermediary_or_correspondent == 'INTERMEDIARY':
            party_details['ACCOUNT'] = party_account.Account2()
        else:
            party_details['ACCOUNT'] = party_account.Account()
        party_details['BIC'] = get_party_bic(party_account, intermediary_or_correspondent)
    if party:
        party_details['NAME'] = get_party_full_name(party)
        party_details['ADDRESS'] = get_party_address(party)
        party_details['COUNTRY_CODE'] = get_party_country_code(party)
        party_details['TOWN'] = get_party_town(party)
        party_details['ZIP_CODE'] = get_party_zipcode(party)
    return party_details

def get_party_bic(account, intermediary_or_correspondent=None):
    """
    Method to get party bic from the account object
    :param account:
    :param intermediary_or_correspondent:
    :return: bic of the account
    """
    #The account defined on the same row is an account in that bank, but its held on behalf of the party "above".
    if intermediary_or_correspondent == 'INTERMEDIARY':
        bic2 = account.Bic2()
        if bic2:
            return bic2.Alias()
    elif intermediary_or_correspondent == 'CORRESPONDENT':
        bic = account.Bic()
        if bic:
            return bic.Alias()
    else:
        if account.NetworkAlias():
            return account.NetworkAlias().Alias()
        else:
            assert account.Party(), "The account has no party reference"
            return account.Party().Swift()

def get_party_full_name(party):
    """
    Method to get party full name considering the FParameter UsePartyFullName
    :param party:
    :return: party full name
    """
    use_party_full_name = getattr(cash_settlement_out_config, 'UsePartyFullName', None)
    if not use_party_full_name:
        use_party_full_name = getattr(writer_config, 'UsePartyFullName', False)
    return FSwiftMLUtils.get_party_full_name(party, bool(use_party_full_name))

def get_party_address(party):
    """
    Method to get party Address
    :param party:
    :return: party address
    """
    address = party.Address()
    if party.Address() != party.Address2():
        address = address + party.Address2()
    address = "%s %s %s" % (address, party.City(), party.Country())
    return address

def get_party_zipcode(party):
    """ Method to return party zipcode """
    return party.ZipCode()

def get_party_town(party):
    """ Method to return party town """
    return party.City()

def get_party_country_code(party):
    """ Method to return party country code """
    return party.JurisdictionCountryCode()

def get_acquirer_details(settlement):
    """ Method to return acquirer details from the settlement object """
    acquirer = settlement.Acquirer()
    acquirer_account = settlement.AcquirerAccountRef()
    return get_party_details(acquirer, acquirer_account)

def get_acquirer_correpondent_details(settlement):
    """ Method to return acquirer correspondent details from settlement object """
    acquirer = settlement.AcquirerAccountRef().CorrespondentBank()
    acquirer_account = settlement.AcquirerAccountRef()
    return get_party_details(acquirer, acquirer_account, "CORRESPONDENT")

def get_counterparty_details(settlement):
    """ Method to return counterParty details from settlement object """
    party = settlement.Counterparty()
    party_account = settlement.CounterpartyAccountRef()
    return get_party_details(party, party_account)

def get_counterpartys_intermediary_details(settlement):
    """ Method to return counterPartys intermediary details from given settlement """
    party = settlement.CounterpartyAccountRef().CorrespondentBank2()
    party_account = settlement.CounterpartyAccountRef()
    return get_party_details(party, party_account, 'INTERMEDIARY')

def get_counterpartys_correspondent_details(settlement):
    """ Method to return counterparty correspondent details from given settlement """
    party = settlement.CounterpartyAccountRef().CorrespondentBank()
    party_account = settlement.CounterpartyAccountRef()
    return get_party_details(party, party_account, 'CORRESPONDENT')

def is_netted_settlement(settlement):
    """ check if the given settlement is netted settlement """
    if settlement.RelationType() in (RelationType.AD_HOC_NET, RelationType.NET):
        return True
    return False

def get_least_net_trade(settlement):
    """ Method to get the least netted trade on given settlement """
    children = settlement.Children()
    children = [child for child in children if child.Trade() != None]

    if len(children) == 0:
        return None

    return min(children, key = lambda child: child.Trade().Oid())

def get_receivers_bic(settlement):
    """Returns SWIFT bic code of settlement receiver.
    This field goes into {2:Application Header Block} -- Receiver Information."""

    receiver_bic = ''

    swift_loopback = getattr(cash_settlement_out_config, 'SwiftLoopBack', 'None')
    receiver_bic_loopback = getattr(cash_settlement_out_config, 'ReceiverBICLoopBack', 'None')
    if swift_loopback == 'None' and receiver_bic_loopback == 'None':
        swift_loopback = getattr(writer_config, 'SwiftLoopBack', 'None')
        receiver_bic_loopback = getattr(writer_config, 'ReceiverBICLoopBack', 'None')

    if swift_loopback and eval(swift_loopback) and  eval(swift_loopback) == True:
        if receiver_bic_loopback and eval(receiver_bic_loopback):
            return eval(receiver_bic_loopback)

    acquire_account = settlement.AcquirerAccountRef()
    counterparty_account = settlement.CounterpartyAccountRef()
    if counterparty_account:
        if settlement.CounterpartyAccountSubNetworkName() in ('TARGET2', 'EBA'):
            if counterparty_account.Bic2():
                receiver_bic = counterparty_account.Bic2().Alias()
            elif counterparty_account.Bic():
                receiver_bic = counterparty_account.Bic().Alias()
    if receiver_bic == '':
        if acquire_account:
            if acquire_account.Bic():
                receiver_bic = acquire_account.Bic().Alias()

    return receiver_bic

def get_senders_bic(settlement):
    """Returns SWIFT bic code of the Acquirer of the settlement.
    This field goes into {1: Basic Header Block} -- Address of the Sender"""

    swift_loopback = getattr(cash_settlement_out_config, 'SwiftLoopBack', 'None')
    sender_bic_loopback = getattr(cash_settlement_out_config, 'SenderBICLoopBack', 'None')
    if swift_loopback == 'None' and sender_bic_loopback == 'None':
        swift_loopback = getattr(writer_config, 'SwiftLoopBack', 'None')
        sender_bic_loopback = getattr(writer_config, 'SenderBICLoopBack', 'None')

    if swift_loopback and eval(swift_loopback) and eval(swift_loopback) == True:
        if sender_bic_loopback and eval(sender_bic_loopback):
            return eval(sender_bic_loopback)

    account = settlement.AcquirerAccountRef()
    if account and account.NetworkAlias():
        return account.NetworkAlias().Alias()
    assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"
    assert settlement.AcquirerAccountRef().Party(), "The acquirer account referenced by the settlement has no party"
    return account.Party().Swift()

def get_sub_network(settlement):
    """ Returns the swift sub network. Extra validation is performed for
    TARGET2 and EBA """
    ret_val = ""
    valid_sub_networks = getattr(cash_settlement_out_config, 'SubNetwork', 'None')
    if valid_sub_networks:
        valid_sub_networks = eval(valid_sub_networks)
    swift_settlement = FSwiftSettlement(settlement)
    if valid_sub_networks:
        counter_party_account_subnetwork = settlement.CounterpartyAccountSubNetworkName()
        if counter_party_account_subnetwork in valid_sub_networks:
            if counter_party_account_subnetwork == "TARGET2":
                if swift_settlement.IsTargetTwo():
                    ret_val = counter_party_account_subnetwork
            elif counter_party_account_subnetwork == "EBA":
                if swift_settlement.IsEba():
                    ret_val = counter_party_account_subnetwork
            else:
                ret_val = counter_party_account_subnetwork
    return ret_val

def get_swift_service_code(settlement):
    """ Returns the swift_service_code value """
    ret_val = ''
    swift_service_codes = getattr(cash_settlement_out_config, 'SwiftServiceCode', 'None')
    if swift_service_codes:
        swift_service_codes = eval(swift_service_codes)
    sub_network = get_sub_network(settlement)
    if swift_service_codes and sub_network in swift_service_codes:
        ret_val = swift_service_codes[sub_network]
    return ret_val

def get_banking_priority(settlement):
    """ Returns the banking priority value """
    ret_val = ''
    valid_banking_priorities = getattr(cash_settlement_out_config, 'BankingPriority', 'None')
    if valid_banking_priorities:
        valid_banking_priorities = eval(valid_banking_priorities)
    sub_network = get_sub_network(settlement)
    if valid_banking_priorities and sub_network in valid_banking_priorities:
        ret_val = valid_banking_priorities[sub_network]
    return ret_val

def get_national_clearing_system(settlement):
    """ get mapped value for national clearing system based on FParameter value """
    clearing_system = ""
    national_clearing_systems = getattr(cash_settlement_out_config, 'NationalClearingSystem', 'None')
    if national_clearing_systems:
        national_clearing_systems = eval(national_clearing_systems)
    account = settlement.CounterpartyAccountRef()
    if account:
        clearing_system_chl_item = account.NationalClearingSystemChlItem()
        if clearing_system_chl_item:
            clearing_system_full_name = clearing_system_chl_item.Name()
            if clearing_system_full_name in national_clearing_systems:
                clearing_system = national_clearing_systems[clearing_system_full_name]
            else:
                notifier.WARN("The value '%s' could not be found in parameter NationalClearingSystem." % clearing_system_full_name)
    return clearing_system

def get_national_clearing_code(settlement):
    """ get national clearing code for the account """
    clearing_code = ""
    account = settlement.CounterpartyAccountRef()
    if account:
        clearing_code = account.NationalClearingCode()
    return clearing_code

def get_sequence_number(settlement):
    """
    Get the sequence number for the Settlement
    :return:
    """
    seq_number = ''
    if settlement:
        seq_number = settlement.Oid()
    return seq_number

def get_bank_operation_code():
    """ Mandatory field 23B """

    return 'CRED'

def get_instruction_code():
    """ Mandatory field 23E """

    return 'PHOB'

def get_value_date(settlement):
    """This together with interbank_settled_amount forms the
     mandatory field 32A in 103 and 202.
    Also it is a mandatory field 30 for 210.
    Returns the value day for settlement.
    """

    return settlement.ValueDay()

def get_date_of_original_message(settlement, fmtclass_mttype, child_mt_type=''):
    '''Returns the date of the original message for which
    MT292 was sent.
    '''
    if settlement.RelationType() != 'Cancellation':
        child_settlement = settlement
    else:
        child_settlement = settlement.Children()[-1]

    external_objects = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=child_settlement, integration_type='Outgoing', all_records=True)
    for ext_obj in external_objects:
        integration_sub_type = ext_obj.IntegrationSubtype()
        mt_type = integration_sub_type.split('-')[0]
        if child_mt_type and child_mt_type == mt_type:
            bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
            if bpr:
                date_of_original_message = FSwiftMLUtils.get_param_val_from_bpr(bpr, "Sent", "SentDate")
                return date_of_original_message

def get_your_ref(settlement):
    """
    Method to get yourref field on trade
    :param settlement:
    :return: YourRef field on trade else NONREF
    """
    trade = settlement.Trade()
    if is_netted_settlement(settlement):
        trade = get_least_net_trade(settlement)
    if trade != None:
        if trade.YourRef():
            return trade.YourRef()[:16]
    return 'NONREF'

def get_settlement_reference_prefix():
    """
    Method to get settlement reference prefix to be sent in the MT message
    """
    cash_settlement_out_config = FSwiftWriterUtils.get_config_from_fparameter('FCashOut_Config')
    if str(getattr(cash_settlement_out_config, 'FAS', "")) == "":
        return str(getattr(writer_config, 'FAS', "FAS"))
    return str(getattr(cash_settlement_out_config, 'FAS', None))

def get_narrative_description(settlement, mt_type=None):
    """Optional field 79 for n92 Settlement. """
    narrative_description = ''
    if mt_type in ['MT199', 'MT299']:
        ccy = settlement.Currency().Name()
        amount = str(abs(settlement.Amount()))
        value_date = settlement.ValueDay()
        original_value_day = settlement.Children()[-1].ValueDay()
        related_ref = "%s-%s-%s" % (str(get_settlement_reference_prefix()), str(settlement.Oid()), str(get_message_version_number(settlement)))
        narrative_description = """TODAY WE HAVE SENT YOU A PAYMENT INSTRUCTION UNDER REFERENCE {0} FOR {1} {2} WITH VALUE DATE {3}.WITH REGARDS TO THIS PAYMENT WE HEREBY INSTRUCT YOU TO ARRANGE A BACKVALUATION FROM VALUE DATE {3} TO VALUE DATE {4}.""".format(related_ref, ccy, amount, value_date, original_value_day)
    else:
        if is_cancellation(settlement):
            related_settlement = get_related_settlement(settlement)
            narrative_description = 'Settlement Id %s was due to %s' % (related_settlement.Oid(), related_settlement.ValueDay())
        elif is_nak_cancellation(settlement):
            narrative_description = 'Cancelling previous MT%s' % (get_original_message_type(settlement))

    return narrative_description


def get_documents_to_cancel(settlement):
    """
    Method to return documents to be cancelled
    :param settlement:
    :return: document list which are eligible for cancellation
    """
    documents = settlement.Documents()
    documents_to_cancel = []
    if is_nak_cancellation(settlement):
        for doc in documents:
            if doc.Status() == DocumentStatus.SENT_SUCCESSFULLY:
                documents_to_cancel.append(doc)
    return documents_to_cancel


def get_original_message_type(settlement):
    """
    Method to return the original message type
    :param settlement:
    :return: MT type of original message
    """
    documents_to_cancel = get_documents_to_cancel(settlement)
    mt_type = ''
    for doc in documents_to_cancel:
        mt_type = doc.SwiftMessageType()
    return mt_type


def get_ordering_customer_account(settlement):
    """
    Method to get ordering customer account
    :param settlement:
    :return:
    """
    ordering_customer_account = None
    if settlement.Counterparty().Type() == 'Client' or settlement.Counterparty().Type() == 'Broker':
        return settlement.CounterpartyAccount()
    return ordering_customer_account

def get_ordering_customer_bic(settlement):
    """
    Method to get ordering customer bic value from settlement object
    :param settlement:
    :return: ordering customer bic
    """
    counterparty_party_account = settlement.CounterpartyAccountRef()
    ordering_customer_bic = None
    if counterparty_party_account != None and (settlement.Counterparty().Type() == 'Client' or settlement.Counterparty().Type() == 'Broker'):
        ordering_customer_bic = get_party_bic(counterparty_party_account)
    return ordering_customer_bic

def get_ordering_customer_name(settlement):
    """
    Method to get ordering customer name from settlement object
    :param settlement:
    :return: ordering customer name
    """
    ordering_customer_name = None
    if settlement.Counterparty().Type() == 'Client' or settlement.Counterparty().Type() == 'Broker':
        ordering_customer_name = get_party_full_name(settlement.Counterparty())
    return ordering_customer_name

def get_ordering_customer_address(settlement):
    """
    Method to get ordering customer address from settlement object
    :param settlement:
    :return: ordering customer address
    """
    ordering_customer_address = None
    if settlement.Counterparty().Type() == 'Client' or settlement.Counterparty().Type() == 'Broker':
        ordering_customer_address = get_party_address(settlement.Counterparty())
    return ordering_customer_address

def get_ordering_institution_account(settlement):
    """
    Method to get ordering institution account from settlement object
    :param settlement:
    :return: ordering institution account
    """
    counterparty_account = None
    if settlement.Counterparty().Type() == 'Counterparty' or settlement.Counterparty().Type() == 'Broker' or settlement.Counterparty().Type() == 'Client':
        counterparty_account = settlement.CounterpartyAccount()
    return counterparty_account

def get_ordering_institution_bic(settlement):
    """
    Method to get ordering institution bic from settlement object
    :param settlement:
    :return: ordering institution bic
    """
    counterparty_party_account = settlement.CounterpartyAccountRef()
    ordering_institution_bic = None
    if counterparty_party_account and counterparty_party_account.Bic() and (settlement.Counterparty().Type() == 'Counterparty' or settlement.Counterparty().Type() == 'Broker' or settlement.Counterparty().Type() == 'Client'):
        ordering_institution_bic = counterparty_party_account.Bic().Alias()
    return ordering_institution_bic

def get_ordering_institution_name(settlement):
    """
    Method to get ordering institution name from given settlement object
    :param settlement:
    :return: ordering institution name
    """
    ordering_institution_name = None
    if settlement.Counterparty().Type() == 'Counterparty' or settlement.Counterparty().Type() == 'Broker' or settlement.Counterparty().Type() == 'Client':
        ordering_institution_name = get_party_full_name(settlement.Counterparty())
    return ordering_institution_name

def get_ordering_institution_address(settlement):
    """
    Method to get ordering institution address
    :param settlement:
    :return: ordering institution address
    """
    ordering_institution_address = None
    if settlement.Counterparty().Type() == 'Counterparty' or settlement.Counterparty().Type() == 'Broker' or settlement.Counterparty().Type() == 'Client':
        ordering_institution_address = get_party_address(settlement.Counterparty())
    return ordering_institution_address

def get_counterpartys_intermediary_account(settlement):
    """
    Method to get counterpartys indtermediary account from given settlement
    :param settlement:
    :return: counterparty intermediary account
    """
    intermediary_account = None
    cp_account = settlement.CounterpartyAccountRef()
    if cp_account:
        intermediary_account = cp_account.Account2()
    return intermediary_account

def get_gpi_identifier(settlement):
    """
    Method to get gpi identifier from settlement object
    :param settlement:
    :return: gpi identifier
    """
    gpi_identifier = None
    account = acm.FAccount.Select01('name ="%s" and party = "%s"'%(settlement.AcquirerAccName(), settlement.Acquirer().Name()), None)
    if account:
        gpi_identifier = account.AdditionalInfo().GPI_Identifier()
    return gpi_identifier

def get_corresponding_mt_type_of_canc_paygood(acm_obj, swift_message_type, canc_or_paygood):
    """
    Method to get corresponding MT Type in case of the canc or paygood scenarios
    :param acm_obj: settlement object
    :param swift_message_type: MT type from parent settlement line
    :param canc_or_paygood: flag indicating whether its a cancellation or paygoodvalue scenario
    :return:
    """
    msg_typ = FSwiftWriterUtils.get_mt_type_from_acm_obj(acm_obj.Children()[-1])
    try :
        import FCashOutMain
        dict = FCashOutMain.message_type_and_corresponding_messages.get(msg_typ)
        if dict: #{'103':['199','192'],'202COV':['299','292']}
            parent_msg_type = str(swift_message_type)[2:]
            for child_msg_type, (paygood, canc) in dict.items():
                if ("canc" == canc_or_paygood and canc == parent_msg_type) or ("paygood" == canc_or_paygood and paygood == parent_msg_type):
                    msg_typ = child_msg_type
                    return msg_typ
                else:
                    return msg_typ
    except Exception as e:
        notifier.WARN('Exception in method get_corresponding_mt_type_of_canc_paygood: {}'.format(e))
    return msg_typ


def get_version_for_sent_message_on(acm_obj, msg_type):
    try:
        ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_obj, integration_type = 'Outgoing')
        swift_message = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
        reg_exp = re.compile("20:FA[C|S]-[0-9]*-[0-9]*")
        senders_reference_field = reg_exp.findall(swift_message)[0]
        return senders_reference_field.split('-')[-1]
    except AttributeError as e:
        return 0


def get_counterparty_delivery_agent_details(settlement):
    """Account&Party from which counterparty will transfer funds to acquirer"""
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    buy_money_flow = sett_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not buy_money_flow:
        buy_money_flow = sett_wrapper_obj.money_flow()
    if buy_money_flow:
        party = buy_money_flow.CounterpartyAccount().CorrespondentBank()
        party_account = buy_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details

def get_counterparty_intermediary_details(settlement):
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    sell_money_flow = sett_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = sett_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().CorrespondentBank2()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account, "INTERMEDIARY")
    return party_details

def get_counterparty_receiving_agent_details(settlement):
    """Account&Party in which acquirer will receive funds from counterparty"""
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    sell_money_flow = sett_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = sett_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().CorrespondentBank()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details


def get_acquirer_delivery_agent_details(settlement):
    """Account&Party from which acquirer will transfer funds to counterparty"""
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    sell_money_flow = sett_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = sett_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.AcquirerAccount().CorrespondentBank()
        party_account = sell_money_flow.AcquirerAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details

def get_acquirer_intermediary_details(settlement):
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    buy_money_flow = sett_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not buy_money_flow:
        buy_money_flow = sett_wrapper_obj.money_flow()
    if buy_money_flow:
        party = buy_money_flow.AcquirerAccount().CorrespondentBank2()
        party_account = buy_money_flow.AcquirerAccount()
        return get_party_details(party, party_account, "INTERMEDIARY")
    return party_details

def get_acquirer_receiving_agent_details(settlement):
    """Account&Party in which counterparty will receive funds from acquirer"""
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    buy_money_flow = sett_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not buy_money_flow:
        buy_money_flow = sett_wrapper_obj.money_flow()
    if buy_money_flow:
        party = buy_money_flow.AcquirerAccount().CorrespondentBank()
        party_account = buy_money_flow.AcquirerAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details

def get_beneficiary_institution_details(settlement):
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    sell_money_flow = sett_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = sett_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().CorrespondentBank()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account)
    return party_details

def get_buy_amount(settlement):
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    return sett_wrapper_obj.buy_amount()

def get_buy_currency(settlement):
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    return sett_wrapper_obj.buy_money_flow().Currency().Name()

def get_sell_amount(settlement):
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    return sett_wrapper_obj.sell_amount()

def get_sell_currency(settlement):
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    return sett_wrapper_obj.sell_money_flow().Currency().Name()

def get_exchange_rate(settlement):
    rate = ''
    trade = settlement.Trade()
    if trade:
        rate = trade.Price()
    return rate

def get_trade_date(settlement):
    """ get the trade date """
    return settlement.Trade().TradeTime()[:10]


def get_party_a_details(settlement):
    """ Changed accroding to discussions so the logic is:
        Party A should use the account for the amount to be paid (sold amount)
        and Party B should use the account for the amount to be received (buy amount) (buy/sell direction seen from sender of MT300 = acquirer)  """
    party_details = {}
    sett_wrapper_obj = FMTSettlementWrapper(settlement)
    money_flow = sett_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not money_flow:
        money_flow = sett_wrapper_obj.money_flow()
    if money_flow:
        acquirer = money_flow.Acquirer()
        acquirer_account = money_flow.AcquirerAccount()
        return get_party_details(acquirer, acquirer_account)
    return party_details



def get_bic_from_party(party):
    """ Method to retrieve BIC from party object """
    bic = ''
    for alias in party.Aliases():
        if alias.Type().Name() == 'SWIFT':
            bic = alias.Name()
    if not bic:
        bic = party.Swift()
    return bic


def get_fund_manager_details(fund_manager):
    """ Get fund manager details like name, address, bic from party object """
    fund_manager_details = {}
    if fund_manager:
        fund_manager_obj = acm.FParty[fund_manager]
        if fund_manager_obj:
            fund_manager_details = get_party_details(fund_manager_obj, None)
            bic = get_bic_from_party(fund_manager_obj)
            if bic:
                fund_manager_details['BIC'] = bic
            if fund_manager_details:
                fund_manager_details = fund_manager_details
        else:
            notifier.WARN("No party with name '%s' found in database"%fund_manager)
    else:
        notifier.WARN("FundManager is mandatory in fund_manager_82A/D/J")
    return fund_manager_details


def get_executing_broker(acm_obj):
    """ Method to retrieve executing broker"""
    executing_broker = ''
    if acm_obj.Trade() and acm_obj.Trade().Broker():
        executing_broker = acm_obj.Trade().Broker().Name()
    return executing_broker


def get_executing_broker_details(executing_broker):
    """ Method to retrieve executing broker details like name, address, bic """
    executing_broker_details = {}
    if executing_broker:
        executing_broker_obj = acm.FParty[executing_broker]
        if executing_broker_obj:
            executing_broker_details = get_party_details(executing_broker_obj, None)
            bic = get_bic_from_party(executing_broker_obj)
            if bic:
                executing_broker_details['BIC'] = bic
            if executing_broker_details:
                executing_broker_details = executing_broker_details
        else:
            notifier.WARN("No party with name '%s' found in database" % executing_broker)
    else:
        notifier.WARN("ExecutingBroker is mandatory in executing_broker_87A/D/J")
    return executing_broker_details

def calculate_currency_amount(acm_obj):
    """ Method to retrieve gain indicator, currency and amount"""
    currency_amount = {}
    trade = acm_obj.Trade()
    original_trade_number = trade.ContractTrdnbr()
    current_trade_number = trade.Oid()

    if current_trade_number != original_trade_number:
        original_price = acm.FTrade[original_trade_number].Price()
        current_price =  acm.FTrade[current_trade_number].Price()
        difference = original_price - current_price
        base_currency = acm.FTrade[original_trade_number].Instrument().Name()
        total_price = difference * trade.Quantity()
        profit_or_loss = total_price / original_price
        if base_currency and str(profit_or_loss):
            currency_amount['AMOUNT'] = profit_or_loss
            currency_amount['CURRENCY'] = base_currency
    return currency_amount


def base_currency(acm_obj):
    trade = acm_obj.Trade()
    trade_number = trade.ContractTrdnbr()
    base_currency = acm.FTrade[trade_number].Instrument().Name()
    return base_currency


def gain_indicator(acm_obj):
    """ Method to return gain indication """
    gain_or_loss = calculate_currency_amount(acm_obj)
    gain_or_loss = gain_or_loss['AMOUNT']
    if gain_or_loss > 0:
        indicator = 'Y'
    elif gain_or_loss < 0:
        indicator = 'N'
    else:
        indicator = 'Y'
    return indicator


def reference_of_previous_deals(acm_obj):
    """ Method to retrieve trades related to the given acm_obj """
    parent_trade = acm_obj.Trade().ContractTrdnbr()
    current_trade = acm_obj.Trade().Oid()
    if current_trade != parent_trade:
        query = "contractTrdnbr=%d" %(parent_trade)
        trades  = acm.FTrade.Select(query)
        settlement_list = []
        for trade in trades:
            for sett in trade.Settlements():
                if sett.Type() in ['Premium', 'Premium 2']:
                    settlement_list.append(sett)

        ref_of_previous_deals = []
        for settlement_obj in settlement_list:
            swift_message = FSwiftMLUtils.get_outgoing_mt_message(settlement_obj)
            if swift_message:

                senders_reference = FSwiftMLUtils.get_field_value(swift_message, '20')
                ref_of_previous_deals.append(senders_reference)
        return ref_of_previous_deals


def get_bic(party_details):
    bic = None
    if 'BIC' in party_details:
        bic = party_details['BIC']

    return bic

def sibling_message_generation_failed(message_list, msg_type, acm_obj, state):
    for raw_message_type in message_list:
        message_type = 'MT' + str(raw_message_type)
        if str(message_type.split('-')[0]) != str(msg_type):
            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_obj, msg_typ=str(message_type), integration_type='Outgoing')
            business_pro = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
            if business_pro and business_pro.CurrentStateName() == state:
                return True

