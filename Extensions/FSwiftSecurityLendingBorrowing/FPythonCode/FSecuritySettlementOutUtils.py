"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementOutUtils

DESCRIPTION:
    A module for common functions used across FXTrade Focnfirmation outgoing
    solution.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

from pyxb.exceptions_ import ValidationError
from FMTSettlementWrapper import FMTSettlementWrapper
from FExternalObject import FExternalObject
import FSwiftMLUtils
import FSwiftWriterUtils
import re
import ast
import acm
import os
import tempfile
import pyxb
import FUxCore
import xml.dom.minidom as dom
from functools import wraps


#from FSettlementEnums import RelationType, PartialSettlementType
import FSwiftWriterLogger
#from FOperationsEnums import InsType
#from FSettlementEnums import SettlementType
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')

import FSwiftOperationsAPI
import itertools
from FSettlementXML import FSettlementXML
try:
    #from FSettlementEnums import RelationType, SettlementStatus
    RelationType = FSwiftOperationsAPI.GetRelationTypeEnum()
    PartialSettlementType = FSwiftOperationsAPI.GetPartialSettlementTypeEnum()
    InsType = FSwiftOperationsAPI.GetInsTypeEnum()
    SettlementType = FSwiftOperationsAPI.GetSettlementTypeEnum()
    SettlementStatus = FSwiftOperationsAPI.GetSettlementStatusEnum()
except:
    pass
from FSecurityLendingBorrowingOutUtils import get_additionalinfo_value_for
from FSBLCalculator import PAYMENT_TYPES

writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

class PreviewOutgoingMTMsgSecuritySettlementMenuItem(FUxCore.MenuItem):
    """MenuItem for displaying outgoing message from confirmation object"""
    def __init__(self, eii, state_chart_names):
        self._eii = eii
        self.active_sheet = FSwiftMLUtils.get_active_sheet(eii)
        if type(state_chart_names) == type([]):
            self.state_chart_names = state_chart_names
        else:
            self.state_chart_names = [state_chart_names]

    def Enabled(self):
        return True

    def Invoke(self, _eii):
        self._view_mt_settlement_msg()

    def Applicable(self):
        return self._is_enabled()

    def _is_enabled(self):
        is_enabled = False
        try:
            if self.active_sheet:
                for cell in self.active_sheet.Selection().SelectedCells():
                    if cell.IsHeaderCell():
                        acm_obj = cell.RowObject()
                        typ_of_msg = FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj)
                        if acm_obj.Status() == 'Authorised' and typ_of_msg != '0':
                            is_enabled = True
                            break
        except Exception as e:
            mt_type = 'MT' + str(typ_of_msg)
            notifier.ERROR("%s Exception occurred in PreviewOutgoingMTMsgSecuritySettlementMenuItem._is_enabled : %s" %
                           (mt_type, str(e)))
        return bool(is_enabled)

    def _view_mt_settlement_msg(self):
        try:
            for cell in self.active_sheet.Selection().SelectedCells():
                if cell.IsHeaderCell():
                    acm_obj = cell.RowObject()
                    xml_str = FSettlementXML(acm_obj).GenerateXmlFromTemplate()
                    meta_data_xml_dom = dom.parseString(xml_str)
                    msg_type = 'MT' + str(FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj))
                    swift_message, mt_py_object, exceptions, getter_values = FSwiftWriterUtils.generate_swift_message(acm_obj, msg_type, meta_data_xml_dom)
                    if not exceptions:
                        swift_data = swift_message
                        mt_msg_type = msg_type
                        temp_dir = tempfile.gettempdir()
                        out_file = os.path.join(temp_dir, '%s_PreviewOutgoing.txt'%(mt_msg_type))
                        f = open(out_file, 'w')
                        f.write(swift_data)
                        f.close()
                        os.startfile(out_file)

        except Exception as e:
            notifier.ERROR("%s Exception occurred in \
            PreviewOutgoingMTMsgSecuritySettlementMenuItem._view_mt_settlement_msg : %s" % (msg_type, str(e)))


def create_preview_outgoing_mt_msg_security_settlement_menuitem(eii):
    return PreviewOutgoingMTMsgSecuritySettlementMenuItem(eii, ['FSwiftSecuritySettlementOut'])



def decorate_all_setter(setter_method):
    ''' Class decorator method for decorating all callable attributes of class and
        returns a decorated method, decorated with setter_method , in this case '''
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

def get_message_version_number(fObject):
    msg_version_number = fObject.VersionId()
    return str(msg_version_number)

def validateAmount(amt, length, field):
    #amt should be in the swift format i.e. should contain one mandatory decimal comma
    validation_errors = []
    if str(amt).count(',') != 1:
        validation_errors.append('%s field must contain one decimal comma.' %field)
    if len(str(amt)) > length:
        validation_errors.append('Length of %s field should not be more than %s.'%(field, length))

    if validation_errors:
        raise ValidationError(message = ''.join(validation_errors))


def get_amount_from_currency_amount(currency_amount):
    '''
        1. takes the currency amount as input
        2. parse the input using regex
        3. check if N is present at the start of input,
                a. if present, replaces comma(,) with dot(.) in the amount field and returns the negative of amount
                b. if not present, replaces comma(,) with dot(.) in the amount field and returns the amount
    '''
    parsed_data = re.findall(r'([N])?[A-Za-z][A-Za-z][A-Za-z](.+)', currency_amount)[0]
    if parsed_data[0] == 'N':
        return '-' + parsed_data[1].replace(',', '.')
    elif parsed_data[0] == '':
        return parsed_data[1].replace(',', '.')

def get_currency_from_currency_amount(currency_amount):
    '''
        1. takes the currency amount as input
        2. parse the input using regex
        3. returns the currency
    '''
    curr = re.findall(r'[N]?([A-Za-z][A-Za-z][A-Za-z]).+', currency_amount)[0]
    return curr

def validate_terms_and_conditions(text, field):
    ''' Applicable for MT300.
        If code VALD is used:
            1. it must appear in the first 6 characters of the first line, and in no other place, followed by a date expressed as YYYYMMDD
                and the end of line separator (that is  :77D:/VALD/YYYYMMDDCrLf)  (Error code(s): C58).
            2. the second line must be present and contain the code SETC, followed by a valid ISO 4217 currency code and the
                end of line separator (that is  /SETC/currencyCrLf) (Error code(s): C59).
        Conversely, if the first six characters of the second line are equal to /SETC/, then the first six characters of the first line must be equal to /VALD/  (Error code(s): C59).
        The code /SETC/ is not allowed in other places than the first six characters of the second line  (Error code(s): C59).
        If the first six characters of the third line are /SRCE/, then the first six characters of the second line must be /SETC/  (Error code(s): C59).
        The code /SRCE/ is not allowed in any other place than the first six characters of the third line  (Error code(s): C59). '''
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
    '''validates if text start or end with a slash '/' and does not contain two consecutive slashes '//'  (Error code(s): T26).'''
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
    validation_error = []
    mt_message = value.split('\n')[0]
    try:
        if not int(mt_message) in range(100, 999):
            validation_error.append("MT Number must be in range 100-200 in %s field." %field)
    except Exception as e:
        notifier.ERROR("Error in validate_mt_and_date_of_original_message : %s "%str(e))

    if validation_error:
        raise ValidationError(message = ''.join(validation_error))


def represent_negetive_currency_amount(curr, amount):
    '''
        1. takes the currency amount as input
        2. replaces hyphen(-) with N when if amount is non zero
        3. removes hyphen(-) if amount is 0
        4. replaces dot(.) with comma(,) in the amount field
        Error code T14
    '''
    amount = str(amount)
    if abs(float(amount))>0 and amount.startswith('-'):
        return 'N' + curr + FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))
    else:
        return curr + FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))

def represent_negative_amount(amount):
    '''
        1. takes the amount as input
        2. replaces hyphen(-) with N when if amount is non zero
        3. remove hyphen(-) if amount is 0
        4. replaces dot(.) with comma(,) in the amount field
    '''
    amount = str(amount)
    if abs(float(amount))>0 and amount.startswith('-'):
        return FSwiftMLUtils.float_to_swiftmt(amount.replace('-', 'N'))
    else:
        return FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))

def represent_amount_in_four_digits(amount):
    '''
        1. take the rightmost non zero digit.
        2. attach 3 digits to the left of it
        3. If there are no digits left then attach 0 to the left till the length is 4
        4. return amount_part of length 4
        Error code T22
    '''
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
    ''' takes the value of Swift 451 tag from the message '''
    ack_or_nack_flag = int(re.findall(r"{451:(.+?)}", msg)[0])
    if ack_or_nack_flag == 1:
        return "Nack"
    elif ack_or_nack_flag == 0:
        return "Ack"

def get_settlement_number_from_msg(msg):
    return msg.split('-')[1]

def apply_currency_precision(curr, amount):
    ''' Round decimal amount according to the precision for a currency stated
        in RoundPerCurrency'''

    #fx_trade_conf_out_config = FSwiftMLUtils.Parameters('FFxTradeConfOutgoingMsg_Config')
    swiftwriter_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
    #round_per_currency = ast.literal_eval(fx_trade_conf_out_config.RoundPerCurrency)
    round_per_currency = ast.literal_eval(getattr(swiftwriter_config, 'RoundPerCurrency', "{'EUR':2, 'USD':2, 'JPY':0, 'KRW':0,\
     'TRY':0, 'KWD':3, 'AED':2, 'ARS':2, 'AUD':2, 'BAM':2, 'BRL':2, 'BGN':2, 'CAD':2, 'CNY':2, 'CZK':2, 'DKK':2, 'GBP':2, 'HKD':2,\
      'HRK':2, 'HUF':2, 'ISK':2, 'INR':2, 'IDR':2, 'LVL':2, 'MYR':2, 'MXN':2, 'MXV':2, 'NZD':2, 'NOK':2, 'PHP':2, 'SAR':2, 'SGD':2, 'ZAR':2, 'SEK':2, 'CHF':2, 'TWD':2, 'THB':2}"))
    roundingPrecision = round_per_currency.get(curr, 2)
    if roundingPrecision == 0:
        amountToRound = int(amount)
    else:
        amountToRound = amount
    ret = round(amountToRound, roundingPrecision)
    return ret

def validate_instruction_code(instruction_codes):
    '''Unit tests done:
       instruction_code = ['PHON\nABDF', 'PHOD']  - Success
       instruction_code = ['PHON\nABDF', 'PHOB']  - Fail
       instruction_code = ['PHOB', 'PHOI\nsdftrrt', 'TELI'] - Success
       instruction_code = ['TELI', 'SDVA'] - Fail
       instruction_code = ['SDVA', 'CORT', 'TELI'] - Success
       instruction_code = ['INTC', 'HOLD', 'TELE', 'SDVA'] - Fail
       instruction_code = ['INTC', 'HOLD', 'TELE', 'INTC'] - Fail'''

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
    for order, each in enumerate(instruction_codes):
        instruction_code = each
        code = instruction_code.value()[0:4]
        if code not in ['PHON', 'PHOB', 'PHOI', 'TELE', 'TELB', 'TELI', 'HOLD', 'REPA'] and len(instruction_code) > 4:
            raise ValidationError("Additional Information is only allowed when Instruction Code consists of one of the following codes: PHON, PHOB, PHOI, TELE, TELB, TELI, HOLD or REPA")
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

def GetRelatedSettlement(settlement):
    if IsCancellation(settlement):
        return settlement.Children()[0]
    elif IsNakCancellation(settlement):
        return settlement
    return None

def IsCancellation(settlement):
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        return settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT]
    else:
        return settlement.RelationType() in ['Cancellation', 'Cancel Correct']

def IsNakCancellation(settlement):
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        return settlement.Status() == SettlementStatus.PENDING_CANCELLATION
    else:
        return settlement.Status() == 'Pending Cancellation'

def validate_remittance_info(remittance_info):
    exp = re.compile("/(INV|IPI|RFB|ROC|TSU)/")
    if not exp.findall(remittance_info):
        raise ValidationError("One of the codes INV/IPI/RFB/ROC/TSU may be used, placed between slashes")

def _check_for_val(tag, current_tag, format, qualifier):
    if format:
        current_field = current_tag + '_' + format
    else:
        current_field = current_tag
    if getattr(tag, current_field):
        for i in getattr(tag, current_field):
            if i.value()[1:].startswith(qualifier):
                return True
    return False

def check_qualifier_exists(parent_tag, current_tag, qualifier, format_lst):
    if type(parent_tag) == pyxb.binding.content._PluralBinding:
        for child in parent_tag:
            if format_lst:
                for format in format_lst:
                    qualifier_exists = _check_for_val(child, current_tag, format, qualifier)
                    if qualifier_exists:
                        return True
            else:
                return _check_for_val(child, current_tag, '', qualifier)
    else:
        if format_lst:
            for format in format_lst:
                qualifier_exists = _check_for_val(parent_tag, current_tag, format, qualifier)
                if qualifier_exists:
                    return True
        else:
            return _check_for_val(parent_tag, current_tag, '', qualifier)

    return False

def qualifier_count(parent_tag, current_tag, qualifier, format_lst):
    count = 0
    if type(parent_tag) == pyxb.binding.content._PluralBinding:
        for parties in parent_tag:
            if format_lst:
                for format in format_lst:
                    current_field = current_tag + '_' + format
                    if getattr(parties, current_field):
                        for i in getattr(parties, current_field):
                            if i.value()[1:].startswith(qualifier):
                                count = count + 1
            else:
                current_field = current_tag
                if getattr(parties, current_field):
                    for i in getattr(parties, current_field):
                        if i.value()[1:].startswith(qualifier):
                            count = count + 1
    else:
        if format_lst:
            for format in format_lst:
                current_field = current_tag + '_' + format
                if getattr(parent_tag, current_field):
                    for i in getattr(parent_tag, current_field):
                        if i.value()[1:].startswith(qualifier):
                            count = count + 1
        else:
            current_field = current_tag
            if getattr(parent_tag, current_field):
                for i in getattr(parent_tag, current_field):
                    if i.value()[1:].startswith(qualifier):
                        count = count + 1

    return count

def check_duplicate_qualifier(parent_tag, current_tag, qualifier_lst, format_lst, current_tag_as_list=True):
    duplicate_qualifiers = []
    for parties in parent_tag:
        for format in format_lst:
            current_field = current_tag + '_' + format
            for qualifier in qualifier_lst:
                count = 0
                if getattr(parties, current_field):
                    for i in getattr(parties, current_field):
                        if i.value()[1:].startswith(qualifier):
                            if count:
                                duplicate_qualifiers.append(qualifier)
                                break
                            count = count + 1
    return duplicate_qualifiers

def get_version_for_sent_message_on(acm_obj, msg_type):
    try:
        #ext_obj = FExternalObject.ExtReferences(subject= acm_obj, subtype=msg_type, source="ACM").Last()
        ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, msg_typ=msg_type, integration_type='Outgoing')
        #data = FSwiftMLUtils.get_external_value_using_ael(ext_obj.ReconciliationItem())
        #swift_message = data.At('swift_data')
        swift_message = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
        reg_exp = re.compile(":20C::SEME//FA[C|S]-[0-9]*-[0-9]*")
        senders_reference_field = reg_exp.findall(swift_message)[0]
        return senders_reference_field.split('-')[-1]
    except AttributeError as e:
        return 0


def is_cancellation_settlement(settlement):
    isSecuritySettlement = True if settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT] else False
    return isSecuritySettlement

def get_function_of_message(settlement):
    '''This is a mandatory field 23G in seq A'''

    if is_cancellation_settlement(settlement):
        return 'CANC'
    else:
        return 'NEWM'

def get_related_ref(settlement):
    relatedRef = ''
    relatedSettlement = settlement.Children()[0]
    relatedSettlementMessage = FSwiftMLUtils.get_related_entity_message(relatedSettlement)
    field = '20C'
    fieldValue = FSwiftMLUtils.get_field_value(relatedSettlementMessage, field)
    start = fieldValue.find("FAS-")
    relatedRef = fieldValue[start:]

def get_linkage_qualifier(settlement):
    if is_cancellation_settlement(settlement):
        return 'PREV'
    else:
        return ''

def get_linkage_reference(settlement):
    if is_cancellation_settlement(settlement):
        return get_related_ref(settlement)
    else:
        return ''

def get_preparation_datetime_option(settlement):
    return 'C'


def get_preparation_datetime_qualifier():
    return 'PREP'
    
def get_settlement_datetime_option(settlement):
    return FSwiftWriterUtils.get_option_value('SettlementDateTime_98a', settlement)

def get_settlement_datetime_qualifier():
    return 'SETT'

def get_settlement_datetime_date(settlement):
    swift_addinfo = get_additionalinfo_value_for(settlement.Trade(), 'SL_SWIFT')
    if swift_addinfo == 'DOM' and settlement.Type() in PAYMENT_TYPES:
        if settlement.Trade():
            return settlement.Trade().ValueDay()
    return settlement.ValueDay()

def get_trade_datetime_qualifier():
    return 'TRAD'

def _get_trade_value_days(settlement, allDates):
    if settlement.Trade():
        allDates.add(acm.Time.AsDate(settlement.Trade().TradeTime()))
    else:
        for s in settlement.Children():
            _get_trade_value_days(s, allDates)
        if settlement.SplitParent():
            _get_trade_value_days(settlement.SplitParent(), allDates)

def get_trade_datetime_date(settlement):
    allDates = set()
    _get_trade_value_days(settlement, allDates)
    return sorted(allDates, reverse=True).pop()

def get_maturity_datetime_qualifier():
    """returns maturity qualifier"""
    return 'MATU'

def get_issue_datetime_qualifier():
    """returns issue date qualifier"""
    return 'ISSU'

def get_rate_qualifier():
    """returns rate qualifier"""
    return 'INTR'

def get_instrument_type_qualifier():
    """returns instrument type qualifier"""
    return 'CLAS'

def get_cfi_code(settlement):
    """returns CFI Code of the instrument"""
    instrument = get_instrument(settlement)
    cfi_code = None
    if instrument:
        try:
            cfi_code = instrument.RegulatoryInfo().CfiCode()
        except Exception as e:
            notifier.ERROR("Error in function get_cfi_code : %s "%str(e))
    return cfi_code

def get_isitc_code(settlement):
    """returns ISITC Code of the instrument"""
    isitc_code = None
    try:
        import FRegulatoryLib
        instrument = get_instrument(settlement)
        if instrument:
            isitc_code = FRegulatoryLib.InstrumentRegInfo(instrument).ISITC_type_code()
    except ImportError as e:
        log_statement = "'Type of Financial Instrument' (12A), is based on the ISITC code. RegulatoryLib is\
         required for generation of ISITC code. Ensure Regulatory package (external/built-in) is imported."
        notifier.WARN(log_statement)
    return isitc_code

def get_maturity_datetime_date(settlement):
    """returns maturity date"""
    instrument = get_instrument(settlement)
    maturity_date = None
    if instrument:
        maturity_date = instrument.ExpiryDate()
    return maturity_date

def get_issue_datetime_date(settlement):
    """returns issue date"""
    issue_date = None
    instrument = get_instrument(settlement)
    if instrument:
        issue_date = instrument.IssueDay()
        if not issue_date:
            try:
                issue_date = instrument.GetProviderDataFieldValue('Bloomberg', 'ISSUE_DT')
            except Exception as e:
                notifier.DEBUG("DataLoader API GetProviderDataFieldValue not found on instrument.")
            if not issue_date:
                issue_date = instrument.StartDate()
    return issue_date

def get_rate(settlement):
    """returns rate for the instrument"""
    instrument = get_instrument(settlement)
    rate = None
    if instrument:
        for leg in instrument.Legs():
            rate = leg.FixedRate()
    return rate

def get_instrument(settlement):
    trade = settlement.Trade()
    if trade:
        return trade.Instrument()
    else:
        return settlement.Instrument()

def get_instrument_ISIN(settlement):
    ''' Mandatory field 35B in seq B '''
    instrument = get_instrument(settlement)
    if instrument.Isin() == "" and instrument.Underlying():
        return 'ISIN ' + instrument.Underlying().Isin()
    else:
        return 'ISIN ' + instrument.Isin()

def get_description_of_security(settlement):
    assert settlement.Instrument(), "Settlement has no security instrument or trade referenced by the settlement has no instrument"
    productType = settlement.Instrument().ProductTypeChlItem()
    if productType:
        return productType.Name()
    else:
        return ''


def get_quantity_type_code(settlement):
    if settlement.Instrument().InsType() == 'SecurityLoan':
        if settlement.Instrument().Underlying() and settlement.Instrument().Underlying().InsType() == 'Stock':
            return 'UNIT'
    if settlement.Instrument().InsType() == 'Stock' and settlement.Trade().TradeCategory() == 'Collateral':
        return 'UNIT'
    return 'FAMT'

def get_quantity(settlement):
    '''
    if settlement.Instrument().InsType() == 'SecurityLoan' and settlement.Instrument().Underlying():
        if settlement.Instrument().Underlying().InsType() == 'Stock' and settlement.Trade():
            if str(abs(settlement.Trade().FaceValue()))[-2:] == '.0':
                return str(abs(settlement.Trade().FaceValue()))[:-1] 
    if settlement.Instrument().InsType() == 'Stock' and settlement.Trade().TradeCategory() == 'Collateral':
        if str(abs(settlement.Trade().FaceValue()))[-2:] == '.0':
            return str(abs(settlement.Trade().FaceValue()))[:-1] 
    '''
    swift_addinfo = get_additionalinfo_value_for(settlement.Trade(), 'SL_SWIFT')
    val = get_additionalinfo_value_for(settlement.Trade(), 'SL_ReturnedQty')
    if swift_addinfo == 'DOM':
        if val:
            if str(abs(val))[-2:] == '.0':
                return str(abs(val))[:-1] 
            return val
    return abs(settlement.Amount())

def get_account_option(settlement):
    return FSwiftWriterUtils.get_option_value('Account_97a', settlement)

def get_account_qualifier():
    return 'SAFE'

def get_account_number(settlement):
    return settlement.AcquirerAccount()

def get_place_of_safekeeping_option(settlement):
    return FSwiftWriterUtils.get_option_value('PlaceOfSafeKeeping_94a', settlement)

def get_place_of_safekeeping_qualifier():
    return ''

def get_place_of_safekeeping_place_code():
    return ''

def get_place_of_safekeeping_identifier_code():
    return ''

def get_qualifier(pair):
    return pair.First()

def get_indicator(pair):
    return pair.Second()


def get_indicators(settlement):
    indicatorsList = acm.FList()
    partialSettlementType = settlement.PartialSettlementType()

    if(partialSettlementType != PartialSettlementType.NONE):
        pair = acm.FPair()
        first = acm.FSymbol(get_partial_settlement_type_qualifier())
        second = acm.FSymbol(get_partial_settlement_type_text())
        pair.First(first)
        pair.Second(second)
        indicatorsList.Add(pair)

    pair = acm.FPair()
    first = acm.FSymbol(get_mandatory_qualifier())
    second = acm.FSymbol(get_mandatory_indicator(settlement))
    pair.First(first)
    pair.Second(second)
    indicatorsList.Add(pair)

    return indicatorsList

def get_partial_settlement_type_qualifier():
    return 'BENE'
 
def get_partial_settlement_type_text():
    return 'NBEN'
   
def get_mandatory_qualifier():
    return 'SETR'

def parent_or_all_children_have_instrument_type(settlement, instrumentType):
    parentHasInstrument = False
    if instrumentType == InsType.COLLATERAL:
        if settlement.Trade() != None:
            if settlement.Trade().TradeInstrumentType() == InsType.COLLATERAL:
                parentHasInstrument = True
    else:
        assert settlement.Instrument(), "Settlement has no security instrument or trade referenced by the settlement has no instrument"
        if settlement.Instrument().InsType() == instrumentType:
            parentHasInstrument = True

    if parentHasInstrument:
        return parentHasInstrument

    if len(settlement.Children()) == 0:
        childrenHasInstrument = False
    else:
        childrenHasInstrument = True

    for child in settlement.Children():
        childrenHasInstrument = childrenHasInstrument and parent_or_all_children_have_instrument_type(child, instrumentType)

    return childrenHasInstrument


def get_mandatory_indicator(settlement):
    if settlement.Instrument() != None:
        if parent_or_all_children_have_instrument_type(settlement, InsType.REPO_REVERSE):
            if settlement.Trade():
                if settlement.Trade().Quantity() >= 0:
                    return 'RVPO'
                else:
                    return 'REPU'
        elif parent_or_all_children_have_instrument_type(settlement, InsType.SECURITY_LOAN):
            if settlement.Amount() >= 0:
                return 'SECL'
            else:
                return 'SECB'
        elif parent_or_all_children_have_instrument_type(settlement, InsType.COLLATERAL):
            if settlement.Amount() >= 0:
                return 'COLI'
            else:
                return 'COLO'

    return 'TRAD'

def get_party_option(dummyPartyDetails, party_option):
    ret_option = party_option
    if dummyPartyDetails['qualifier'] in ['BUYR', 'SELL']:
        ret_option = 'P'
    elif dummyPartyDetails['datasourcescheme'] != '':
        ret_option = 'R'

    return ret_option


def get_party_info(qualifier, bic, party, account, dataSourceScheme, safekeepingAccount):
    partyInfo = dict()
    sec_settlement_out_config = FSwiftMLUtils.Parameters('FSecuritySettlementOut_Config')
    use_party_full_name = getattr(sec_settlement_out_config, 'UsePartyFullName', None)
    if not use_party_full_name:
        use_party_full_name = getattr(writer_config, 'UsePartyFullName', False)
    partyInfo['qualifier'] = qualifier
    partyInfo['bic'] = bic
    partyInfo['countrycode'] = bic[4:6]
    partyInfo['partyproprietarycode'] = account
    partyInfo['datasourcescheme'] = dataSourceScheme
    partyInfo['name'] = FSwiftMLUtils.get_party_full_name(party, bool(use_party_full_name))
    partyInfo['address'] = FSwiftMLUtils.get_party_address(party)
    partyInfo['safekeepingaccount'] = safekeepingAccount
    partyInfo['address_details'] = get_party_address_details(party)
    partyInfo['LEI'] = party_LEI(party)
    return partyInfo

def party_LEI(party):
    return party.LEI()

def get_party_address_details(party):
    adress_dict = {}
    if party:
        adress_dict['address_line'] = FSwiftMLUtils.get_party_street_and_number(party)
        adress_dict['zip_code'] = party.ZipCode()
        country_code = ''
        try:
            import FRegulatoryLib
            obj = FRegulatoryLib.ISO3166CountryCode()
            country_code = obj.country_code(party)
        except ImportError as e:
            log_statement = "RegulatoryLib is required for Country code. Ensure Regulatory package (external/built-in) is imported."
            notifier.WARN(log_statement)
        adress_dict['country'] = country_code
    return adress_dict

def get_custodian_account(settlement):
    """Account&Party in which acquirer will receive funds from counterparty"""
    party_account = settlement.AcquirerAccountRef().Account()
    return party_account

def get_instrument_quotation(settlement):
    try:
        quotation = settlement.Trade().Instrument().Quotation().Name()
    except:
        quotation = ''
    return quotation

def get_trade_price(settlement):
    return settlement.Trade().Price()

def get_price_value_type(settlement):
    price_type = ''
    quot = get_instrument_quotation(settlement)
    price = get_trade_price(settlement)
    if quot in ['Clean', 'Pct of Nominal', 'Per 1000 Clean', 'Per 1000 of Nom', 'Per Contract', 'Per Unit']:
        price_type = 'PARV'
    return price_type

def get_price(settlement):
    price = 0
    trade_price = settlement.Trade().Price()
    nominal_amount = settlement.Trade().Instrument().NominalAmount()
    quot = get_instrument_quotation(settlement)
    if quot in ['Yield', 'Clean', 'Per Unit']:
        price =  trade_price
    elif quot in ['Per Contract']:
        price = trade_price/nominal_amount
    elif quot in ['Pct of Nominal']:
        price = trade_price/100
    elif quot in ['Per 1000 Clean', 'Per 1000 of Nom']:
        price = trade_price/1000
    return price

def set_initiating_party_details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''

    party = account.Party()
    bic = FSwiftMLUtils.get_party_bic(account)
    if account.DataSourceScheme():
        dss = account.DataSourceScheme().Alias()
    partyproprietarycode = account.Account()
    partyInfo = get_party_info(qualifier, bic, party, partyproprietarycode if dss != '' else '', dss, partyproprietarycode)
    details.append(partyInfo)

def set_custodian_details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank3():

        if account.DataSourceScheme2():
            partyproprietarycode = account.Account2()
            dss = account.DataSourceScheme2().Alias()
        else:
            if account.Bic():
                bic = account.Bic().Alias()
            safekeepingaccount = account.Account2()
        party = account.CorrespondentBank()

        partyInfo = get_party_info(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
        details.append(partyInfo)

def set_intermediate_1_details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank5() or account.CorrespondentBank4():
        if account.CorrespondentBank4():
            if account.DataSourceScheme3():
                partyproprietarycode = account.Account3()
                dss = account.DataSourceScheme3().Alias()
            else:
                if account.Bic2():
                    bic = account.Bic2().Alias()
                safekeepingaccount = account.Account3()
            party = account.CorrespondentBank2()

            partyInfo = get_party_info(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
            details.append(partyInfo)

def set_intermediate_2_details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank5():
        if account.CorrespondentBank4() and account.DataSourceScheme4():
            partyproprietarycode = account.Account4()
            dss = account.DataSourceScheme4().Alias()
        else:
            if account.Bic3():
                bic = account.Bic3().Alias()
            safekeepingaccount = account.Account4()
        party = account.CorrespondentBank3()

        partyInfo = get_party_info(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
        details.append(partyInfo)

def set_agent_details(qualifier, account, details):
    bic = ''
    party = ''
    partyproprietarycode = ''
    dss = ''
    safekeepingaccount = ''

    if account.CorrespondentBank5():
        if account.DataSourceScheme5():
            partyproprietarycode = account.Account5()
            dss = account.DataSourceScheme5().Alias()
        else:
            safekeepingaccount = account.Account5()
            if account.Bic4():
                bic = account.Bic4().Alias()
        party = account.CorrespondentBank4()

    elif account.CorrespondentBank4():
        if account.DataSourceScheme4():
            partyproprietarycode = account.Account4()
            dss = account.DataSourceScheme4().Alias()
        else:
            safekeepingaccount = account.Account4()
            if account.Bic3():
                bic = account.Bic3().Alias()
        party = account.CorrespondentBank3()

    elif account.CorrespondentBank3():
        if account.DataSourceScheme3():
            partyproprietarycode = account.Account3()
            dss = account.DataSourceScheme3().Alias()
        else:
            safekeepingaccount = account.Account3()
            if account.Bic2():
                bic = account.Bic2().Alias()
        party = account.CorrespondentBank2()

    elif account.CorrespondentBank2():
        if account.DataSourceScheme2():
            partyproprietarycode = account.Account2()
            dss = account.DataSourceScheme2().Alias()
        else:
            safekeepingaccount = account.Account2()
            if account.Bic():
                bic = account.Bic().Alias()
        party = account.CorrespondentBank()

    elif account.CorrespondentBank():
        if account.DataSourceScheme():
            partyproprietarycode = account.Account()
            dss = account.DataSourceScheme().Alias()
        else:
            safekeepingaccount = account.Account()
            if account.NetworkAlias():
                bic = account.NetworkAlias().Alias()
        party = account.CorrespondentBank()

    partyInfo = get_party_info(qualifier, bic, party, partyproprietarycode, dss, safekeepingaccount)
    details.append(partyInfo)

def set_PSET_details(qualifier, account, details):
    bic = ''
    party = ''

    if account.Bic5():
        bic = account.Bic5().Alias()
        party = account.CorrespondentBank5()
    elif account.Bic4():
        bic = account.Bic4().Alias()
        party = account.CorrespondentBank4()
    elif account.Bic3():
        bic = account.Bic3().Alias()
        party = account.CorrespondentBank3()
    elif account.Bic2():
        bic = account.Bic2().Alias()
        party = account.CorrespondentBank2()
    elif account.Bic():
        bic = account.Bic().Alias()
        party = account.CorrespondentBank()

    partyInfo = get_party_info(qualifier, bic, party, '', '', '')
    details.append(partyInfo)

def get_applicable_party_details(option, partyDetails):
    applicablePartyDetails = list()
    for partyInfo in partyDetails:
        applicablePartyInfo = dict.fromkeys(['countrycode', 'bic', 'name', 'address', 'safekeepingaccount', 'datasourcescheme', 'partyproprietarycode', 'LEI'], '')
        applicablePartyInfo['qualifier'] = partyInfo['qualifier']

        if applicablePartyInfo['qualifier'] in ['SELL', 'BUYR']:
            applicablePartyInfo['bic'] = partyInfo['bic']
            applicablePartyInfo['safekeepingaccount'] = partyInfo['safekeepingaccount']
        if option == 'C':
            applicablePartyInfo['countrycode'] = partyInfo['countrycode']
        elif option == 'P':
            if partyInfo['datasourcescheme'] != '':
                applicablePartyInfo['datasourcescheme'] = partyInfo['datasourcescheme']
                applicablePartyInfo['partyproprietarycode'] = partyInfo['partyproprietarycode']
            else:
                applicablePartyInfo['bic'] = partyInfo['bic']
                applicablePartyInfo['safekeepingaccount'] = partyInfo['safekeepingaccount']
        elif option == 'Q':
            applicablePartyInfo['name'] = partyInfo['name']
            applicablePartyInfo['address'] = partyInfo['address']
        elif option == 'L':
            applicablePartyInfo['LEI'] = partyInfo['LEI']
        applicablePartyDetails.append(applicablePartyInfo)

    return applicablePartyDetails

def get_applicable_party_details_mx(partyDetails):
    applicablePartyDetails = list()
    for partyInfo in partyDetails:
        applicablePartyInfo = dict.fromkeys(['countrycode', 'bic', 'name', 'address', 'safekeepingaccount', 'datasourcescheme', 'partyproprietarycode'], '')
        applicablePartyInfo['qualifier'] = partyInfo['qualifier']
        applicablePartyInfo['bic'] = partyInfo['bic']
        applicablePartyInfo['safekeepingaccount'] = partyInfo['safekeepingaccount']
        applicablePartyInfo['countrycode'] = partyInfo['countrycode']
        applicablePartyInfo['name'] = partyInfo['name']
        applicablePartyInfo['address'] = partyInfo['address']
        applicablePartyDetails.append(applicablePartyInfo)
    return applicablePartyDetails

def get_party_qualifier(partyDetails):
    return partyDetails['qualifier']

def get_party_identifier_code(partyDetails):
    return partyDetails['bic']

def get_party_country_code(partyDetails):
    return partyDetails['countrycode']

def get_party_name(partyDetails):
    return partyDetails['name']

def get_party_address(partyDetails):
    return partyDetails['address']

def get_party_data_source_scheme(partyDetails):
    return partyDetails['datasourcescheme']

def get_party_proprietary_code(partyDetails):
    return partyDetails['partyproprietarycode']

def get_party_safekeeping_option(dummyPartyDetails, settlement):
    return FSwiftWriterUtils.get_option_value('SafekeepingAccount_97a', settlement)

def get_party_safekeeping_account(partyDetails):
    return partyDetails['safekeepingaccount']

def get_party_safekeeping_qualifier(partyDetails):
    if partyDetails['safekeepingaccount'] != '':
        return 'SAFE'
    else:
        return ''

def get_party_lei(partyDetails):
    return partyDetails['LEI']

def get_senders_bic(settlement):
    '''Returns SWIFT bic code of the Acquirer of the settlement.
    This field goes into {1: Basic Header Block} -- Address of the Sender'''
    sec_settlement_out_config = FSwiftMLUtils.Parameters('FSecuritySettlementOut_Config')
    swift_loopback = getattr(sec_settlement_out_config, 'SwiftLoopBack', 'None')
    sender_bic_loopback = getattr(sec_settlement_out_config, 'SenderBICLoopBack', 'None')
    if swift_loopback == 'None' and sender_bic_loopback == 'None':
        swift_loopback = getattr(writer_config, 'SwiftLoopBack', 'None')
        sender_bic_loopback = getattr(writer_config, 'SenderBICLoopBack', 'None')

    if swift_loopback and eval(swift_loopback) and eval(swift_loopback) == True:
        if sender_bic_loopback and eval(sender_bic_loopback):
            return eval(sender_bic_loopback)

    account = settlement.AcquirerAccountRef()
    if account:
        if account.NetworkAlias():
            return account.NetworkAlias().Alias()
    assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"
    assert settlement.AcquirerAccountRef().Party(), "The acquirer account referenced by the settlement has no party"
    return account.Party().Swift()

def get_receivers_bic(settlement):
    '''Returns SWIFT bic code of settlement receiver.
    This field goes into {2:Application Header Block} -- Receiver Information.'''

    receiverBic = ''
    sec_settlement_out_config = FSwiftMLUtils.Parameters('FSecuritySettlementOut_Config')
    swift_loopback = getattr(sec_settlement_out_config, 'SwiftLoopBack', 'None')
    receiver_bic_loopback = getattr(sec_settlement_out_config, 'ReceiverBICLoopBack', 'None')
    if swift_loopback == 'None' and receiver_bic_loopback == 'None':
        swift_loopback = getattr(writer_config, 'SwiftLoopBack', 'None')
        receiver_bic_loopback = getattr(writer_config, 'ReceiverBICLoopBack', 'None')

    if swift_loopback and eval(swift_loopback) and  eval(swift_loopback) == True:
        if receiver_bic_loopback and eval(receiver_bic_loopback):
            return eval(receiver_bic_loopback)

    acquireAccount = settlement.AcquirerAccountRef()
    counterPartyAccount = settlement.CounterpartyAccountRef()
    if counterPartyAccount:
        if settlement.CounterpartyAccountSubNetworkName() in ('TARGET2', 'EBA'):
            if counterPartyAccount.Bic2():
                receiverBic = counterPartyAccount.Bic2().Alias()
            elif counterPartyAccount.Bic():
                receiverBic = counterPartyAccount.Bic().Alias()
    if receiverBic == '':
        if acquireAccount:
            if acquireAccount.Bic():
                receiverBic = acquireAccount.Bic().Alias()

    return receiverBic


def get_accrued_interest(settlement):
    """ Get accrued interest from the settlement """
    interest = 0.0
    try:
        if settlement.Trade():
            interest = settlement.Trade().Calculation().AccruedInterestSpotOverrideSource(
                FSwiftMLUtils.get_calculation_space(),
                acm.Time().SmallDate(),
                settlement.Trade().ValueDay(), 2).Value().Number()
    except Exception as e:
        notifier.INFO("Unable to get accrued interest from the trade")

    return interest


def get_amount_qualifier():
    """ Mandatory field 19A in sub seq E3 """
    return 'SETT'


def _premium_amount(settlement):
    if settlement.Trade():
        return settlement.Trade().Premium()
    else:
        amount = 0.0
        for child in settlement.Children():
            amount = amount + _premium_amount(child)
        return amount

def get_credit_debit_code(settlement):
    return 'DBIT' if _premium_amount(settlement) <0 else 'CRDT'

def calculate_cash_amount(settlement):
    amount = 0
    if settlement.Type() == SettlementType.SECURITY_DVP:
        amount = settlement.CashAmount()
    else:
        amount = _premium_amount(settlement)
    curr = settlement.Currency().Name()
    return apply_currency_precision(curr, amount)


def get_amount_sign(settlement):
    if calculate_cash_amount(settlement) <= 0:
        return ''
    else:
        return 'N'


def get_sign_from_amount(amount, mt_type):
    """ Get sign for the amount"""
    sign = ''
    if float(amount) <= 0:
        if not mt_type == "MT541":
            return 'N'
    else:
        if mt_type == "MT541":
            return 'N'
    return sign


def get_currency_code(settlement):
    assert settlement.CashCurrency(), "Settlement has no cash currency"
    return settlement.CashCurrency().Name()

def get_payment_type_from_additional_payments(mt_type, qualifier_name, qualifier_payment_type):
    """ Get payment type for the qualifier.
    :param mt_type: MT type to read corresponding config file
    :param qualifier_name: name of the qualifier to get payment type
    :param qualifier_payment_type: default payment type for the qualifier

    :return: payment type for the qualifier
    """

    if mt_type and qualifier_name and qualifier_payment_type:
        config = FSwiftWriterUtils.get_config_from_fparameter('F%sOut_Config' % mt_type)
        additional_pay_fparam = str(getattr(config, 'AdditionalPayToSwiftQualifier', None))
        if additional_pay_fparam:
            try:
                qualifier_dict = ast.literal_eval(additional_pay_fparam)
                payment_type = qualifier_dict.get(qualifier_name, qualifier_payment_type)
                if payment_type:
                    qualifier_payment_type = payment_type
            except Exception as e:
                notifier.DEBUG('Unable to read qualifier %s from AdditionalPayToSwiftQualifier taking default payment type '
                               '%s for the qualifier' % (qualifier_name, qualifier_payment_type))

    return qualifier_payment_type


def get_amount_for_payment_type(settlement, payment_type):
    """ Get amount for the payment type """
    amount = 0.0
    # for payment in settlement.Trade().Payments():
    #    if payment.Type() == payment_type and payment.Currency().Name() == settlement.Currency().Name():
    #        amount += payment.Amount()
    # return amount

    for child in settlement.Children():
        if child.Type() == payment_type and child.Status() == 'Void' and child.Amount():
            amount += child.Amount()
    return amount


def get_amount_for_qualifier(settlement, qualifier, mt_type):
    """ get amount for the qualifier, field 19A
    :param settlement: FSettlement object
    :param qualifier: name of the qualifier to get the amount
    :param mt_type: MT type of the meesage to be generated
    :return:
    """
    amount = 0.0
    is_accruing = settlement.Instrument().IsAccruing()
    accurued_interest = get_accrued_interest(settlement)
    if qualifier == 'SETT':
        amount = calculate_cash_amount(settlement)
    elif qualifier == 'ACRU' and is_accruing:
        amount = accurued_interest
    elif qualifier == 'STAM' and settlement.Trade() and settlement.Trade().Payments():
        payment_type = get_payment_type_from_additional_payments(mt_type, 'STAM', 'Stamp Duty')
        amount = get_amount_for_payment_type(settlement, payment_type)
    elif qualifier == 'DEAL':
        if is_accruing:
            amount = abs(_premium_amount(settlement)) - abs(accurued_interest)
        else:
            amount = _premium_amount(settlement)
    elif qualifier == 'CHAR' and settlement.Trade().Payments():
        payment_type = get_payment_type_from_additional_payments(mt_type, 'CHAR', 'Payment Cash')
        amount = get_amount_for_payment_type(settlement, payment_type)

    return amount


def get_amount(settlement):
    return abs(calculate_cash_amount(settlement))


def get_amount_details(settlement, mt_type):
    """ Get amount details from the trade lined to given settlement

    :param settlement: FSettlement object
    :return: list of dict of the different qualifiers.
    """
    qualifier_list = ['SETT', 'ACRU', 'CHAR', 'DEAL', 'STAM']
    list_of_payouts = []

    for qualifier in qualifier_list:
        amount = get_amount_for_qualifier(settlement, qualifier, mt_type)
        if abs(amount) > 0.0:
            val_dict = dict()
            val_dict['AMOUNT_QUALIFIER'] = qualifier
            val_dict['AMOUNT_CURRENCY_CODE'] = get_currency_code(settlement)
            val_dict['AMOUNT_AMOUNT'] = abs(apply_currency_precision(val_dict['AMOUNT_CURRENCY_CODE'], amount))
            val_dict['AMOUNT_SIGN'] = get_sign_from_amount(amount, mt_type)

            list_of_payouts.append(val_dict)

    return list_of_payouts


def get_amount_flags(settlement, mt_type):
    """get valid flag names for field 17B
    :param settlement: FSettlement object
    :param mt_type: MT type of the message
    """
    flag_list = list()
    accrued_interest = get_accrued_interest(settlement)
    payment_type = get_payment_type_from_additional_payments(mt_type, 'STAM', 'Stamp Duty')
    stamp_duty = get_amount_for_payment_type(settlement, payment_type)

    if accrued_interest:
        flag_list.append({'QUALIFIER' :'ACRU', 'FLAG': 'Y'})
    if stamp_duty:
        flag_list.append({'QUALIFIER' :'STAM', 'FLAG': 'Y'})

    return  flag_list


def get_settlement_reference_prefix():
    sec_settlement_conf_out_config = FSwiftWriterUtils.get_config_from_fparameter('FSecuritySettlementOut_Config')
    if str(getattr(sec_settlement_conf_out_config, 'FAS', "")) == "":
        return str(getattr(writer_config, 'FAS', "FAS"))
    return str(getattr(sec_settlement_conf_out_config, 'FAS', None))

def get_seq_ref():
    '''SEQREF together with SEQNBR builds field 20, Senders reference '''
    ref = ''
    swiftwriter_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
    FAS = getattr(swiftwriter_config, 'FAS', 'None')
    if FAS:
        ref = FAS
    return ref

def get_delivering_party_details_mx(settlement):
    """Get delivering party details for mx messages"""
    party_details = list()
    acquirerAccount = settlement.AcquirerAccountRef()
    counterPartyAccount = settlement.CounterpartyAccountRef()
    delivery_type_type = get_mx_delivery_type(settlement)
    party_qualifiers = ['PSET', 'DEAG', 'DEI2', 'DEI1', 'DECU', 'SELL']
    if delivery_type_type == 'DELI':
        get_receving_correspondent_party_details(acquirerAccount, party_details)
    else:
        get_receving_correspondent_party_details(counterPartyAccount, party_details)
    party_dict = get_mx_party_tags(party_qualifiers, party_details)
    return party_dict

def get_receiving_party_details_mx(settlement):
    """Get receiving party details for mx messages"""
    party_details = list()
    acquirerAccount = settlement.AcquirerAccountRef()
    counterPartyAccount = settlement.CounterpartyAccountRef()
    delivery_type_type = get_mx_delivery_type(settlement)
    party_qualifiers = ['PSET', 'REAG', 'REI2', 'REI1', 'RECU', 'BUYR']
    if delivery_type_type == 'RECE':
        get_delivering_correspondent_party_details(acquirerAccount, party_details)
    else:
        get_delivering_correspondent_party_details(counterPartyAccount, party_details)
    party_dict = get_mx_party_tags(party_qualifiers, party_details)
    return party_dict

def get_mx_party_tags(party_qualifiers, party_details):
    party_dict = {}
    party_count = 0
    for party_qualifier in party_qualifiers:
        for each_party in party_details:
            if each_party['qualifier'] == party_qualifier:
                party_dict['party{}'.format(party_count)] = each_party
                party_count += 1
                break
    return party_dict

def get_receving_correspondent_party_details(party, party_details):
    """Collect details of all the correspondent parties"""
    set_initiating_party_details('SELL', party, party_details)
    set_custodian_details('DECU', party, party_details)
    set_intermediate_1_details('DEI1', party, party_details)
    set_intermediate_2_details('DEI2', party, party_details)
    set_agent_details('DEAG', party, party_details)
    set_PSET_details('PSET', party, party_details)

def get_delivering_correspondent_party_details(party, party_details):
    """Collect details of all the correspondent parties"""
    set_initiating_party_details('BUYR', party, party_details)
    set_custodian_details('RECU', party, party_details)
    set_intermediate_1_details('REI1', party, party_details)
    set_intermediate_2_details('REI2', party, party_details)
    set_agent_details('REAG', party, party_details)
    set_PSET_details('PSET', party, party_details)

def get_mx_delivery_type(settlement):
    delivery_type = ''
    amount = settlement.Amount()
    delivery_type = settlement.DeliveryType()
    if delivery_type in ['Delivery Free of Payment', 'Delivery versus Payment'] and amount > 0:
        delivery_type = 'RECE'
    elif delivery_type in ['Delivery Free of Payment', 'Delivery versus Payment'] and amount < 0:
        delivery_type = 'DELI'
    return delivery_type

def get_mx_payment_type(settlement):
    payment_type = ''
    amount = settlement.Amount()
    delivery_type = settlement.DeliveryType()
    if delivery_type in ['Delivery Free of Payment']:
        payment_type = 'FREE'
    elif delivery_type in ['Delivery versus Payment']:
        payment_type = 'APMT'
    return payment_type

def get_party_details(settlement, option):
    partyDetails = acm.FList()
    set_party_details(settlement, partyDetails, option)
    return partyDetails

def set_party_details(settlement, partyDetails, option = 'P'):
    details = list()
    if option and option not in ['P', 'C', 'Q', 'R']:
        notifier.ERROR("Option %s is not supported for tag %s. Mapping default option: P" % (option, 'Party_95a'))
        option = 'P'
    counterPartyAccount = settlement.CounterpartyAccountRef()
    if option == 'C':
        set_PSET_details('PSET', counterPartyAccount, details)
    else:
        #set_initiating_party_details('SELL', counterPartyAccount, details)
        #set_custodian_details('DECU', counterPartyAccount, details)
        set_intermediate_1_details('DEI1', counterPartyAccount, details)
        set_intermediate_2_details('DEI2', counterPartyAccount, details)
        set_agent_details('DEAG', counterPartyAccount, details)
        set_initiating_party_details('SELL', counterPartyAccount, details)
        set_PSET_details('PSET', counterPartyAccount, details)

    applicablePartyDetails = get_applicable_party_details(option, details)
    add_elements_to_party_details(applicablePartyDetails, partyDetails)


def get_party_details_MT542(settlement, option):
    partyDetails = acm.FList()
    set_party_details_MT542(settlement, partyDetails, option)
    return partyDetails

def set_party_details_MT542(settlement, partyDetails, option):
    details = list()
    if option and option not in ['P', 'C', 'Q', 'R']:
        notifier.ERROR("Option %s is not supported for tag %s. Mapping default option: P" % (option, 'Party_95a'))
        option = 'P'
    counterPartyAccount = settlement.CounterpartyAccountRef()

    #set_initiating_party_details('BUYR', counterPartyAccount, details)
    #set_custodian_details('RECU', counterPartyAccount, details)
    set_intermediate_1_details('REI1', counterPartyAccount, details)
    set_intermediate_2_details('REI2', counterPartyAccount, details)
    set_agent_details('REAG', counterPartyAccount, details)
    set_initiating_party_details('BUYR', counterPartyAccount, details)
    set_PSET_details('PSET', counterPartyAccount, details)

    applicablePartyDetails = get_applicable_party_details(option, details)
    add_elements_to_party_details(applicablePartyDetails, partyDetails)


def add_elements_to_party_details(elementList, partyDetails):
    for element in elementList:
        partyDetails.Add(element)

def get_amount_sign_MT543(settlement):
    if calculate_cash_amount(settlement) >= 0:
        return ''
    else:
        return 'N'
