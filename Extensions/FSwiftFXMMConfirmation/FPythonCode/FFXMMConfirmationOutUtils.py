"""----------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationOutUtils

DESCRIPTION:
    A module for common functions used across FXMMConfirmation outgoing
    solution.

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import pyxb
from pyxb.exceptions_ import ValidationError
from FExternalObject import FExternalObject
from FMTConfirmationWrapper import FMTConfirmationWrapper
import FSwiftML
import FSwiftMLUtils
import acm
import ael
import re
import ast
import FSwiftWriterUtils
import FSwiftWriterLogger
import FSwiftOperationsAPI
import FSwiftConfirmationUtils
from functools import wraps
try:
    #from FConfirmationEnums import ConfirmationType, EventType
    #from FOperationsEnums import LegType, SettleType, ExerciseType, BarrierOptionType,\
    #    ExoticEventType, BarrierMonitoring,CashFlowType
    ConfirmationType = FSwiftOperationsAPI.GetConfirmationTypeEnum()
    EventType = FSwiftOperationsAPI.GetEventTypeEnum()
    LegType = FSwiftOperationsAPI.GetLegTypeEnum()
    SettleType = FSwiftOperationsAPI.GetSettleTypeEnum()
    ExerciseType = FSwiftOperationsAPI.GetExerciseTypeEnum()
    BarrierOptionType = FSwiftOperationsAPI.GetBarrierOptionTypeEnum()
    ExoticEventType = FSwiftOperationsAPI.GetExoticEventTypeEnum()
    BarrierMonitoring = FSwiftOperationsAPI.GetBarrierMonitoringEnum()
    CashFlowType = FSwiftOperationsAPI.GetCashFlowTypeEnum()
except:
    pass


notifier = FSwiftWriterLogger.FSwiftWriterLogger('FXMMConfOut', 'FFXMMConfirmationOutNotify_Config')
fxmm_out_msg_config = FSwiftMLUtils.Parameters('FFXMMConfirmationOut_Config')
writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

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

def validate_terms_and_conditions(text, field, codes_allowed = [], codes_not_allowed = []):
    ''' Applicable for MT300 and MT305.
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

    for txt in t_n_c:
        for n_code in codes_not_allowed:
            try:
                assert not (txt.startswith('/%s/'%n_code))
            except AssertionError:
                validation_errors.append("/%s/ must not be present at the start of any line" %n_code)


    '''if "SETC" in codes_allowed:
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

    if "SRCE" in codes_allowed:
        try:
            assert not (not t_n_c[1].startswith('/SETC/') and '/SRCE/' in text)
        except AssertionError:
            validation_errors.append("/SRCE/ is not allowed without /SETC/ in the second line of %s field." %field)
        except IndexError:
            if '/SRCE/' in text:
                validation_errors.append("/SRCE/ is not allowed without /SETC/ in the second line of %s field." %field)

    if "VALD" in codes_allowed:
        try:
            if t_n_c[0].startswith('/VALD/'):
                try:
                    assert re.findall(r'/VALD/[0-9]{8}', str(t_n_c[0]))
                except AssertionError:
                    validation_errors.append("/VALD/ is not followed by a date expressed in YYYYMMDD format in %s field." %field)
        except IndexError:
            pass'''

    '''for codes in codes_not_allowed:
        try:
                try:
                    assert '/' + codes + '/' not in text
                except AssertionError:
                    validation_errors.append("/%s/ is not allowed in %s field." %(codes, field))
        except IndexError:
            pass'''

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

def represent_negative_currency_amount(curr, amount):
    '''
        1. takes the currency amount as input
        2. replaces hyphen(-) with N if amount is non zero
        3. removes hyphen(-) if amount is 0
        4. replaces dot(.) with comma(,) in the amount field
        Error code T14
    '''
    amount = str(amount)
    if abs(float(amount))>0 and amount.startswith('-'):
        return 'N' + curr + FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))
    else:
        return curr + FSwiftMLUtils.float_to_swiftmt(amount.replace('-', ''))

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

def get_confirmation_number_from_msg(msg):
    return msg.split('-')[1]

def apply_currency_precision(currency, amount):
    """ Round decimal amount according to the precision for a currency stated in Fparameter: RoundPerCurrency in FSwiftWriterConfig """
    result = FSwiftWriterUtils.apply_rounding(currency, amount)
    return result

def get_version_for_sent_message_on(acm_obj, msg_type):
    try:
        ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_obj, integration_type = 'Outgoing')
        #ext_obj = FExternalObject.ExtReferences(subject= acm_obj, subtype=msg_type, source="ACM").Last()
        swift_message = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
        #data = FSwiftMLUtils.get_external_value_using_ael(ext_obj.ReconciliationItem())
        #swift_message = data.At('swift_data')
        reg_exp = re.compile("20:FA[C|S]-[0-9]*-[0-9]*")
        senders_reference_field = reg_exp.findall(swift_message)[0]
        return senders_reference_field.split('-')[-1]
    except AttributeError as e:
        return 0


def validate_mt_and_date_of_original_message(value, field):
    validation_error = []
    mt_message = value.split('\n')[0]
    try:
        if not int(mt_message) in range(100, 999):
            validation_error.append("MT Number must be in range 100-999 in %s field." %field)
    except Exception as e:
        notifier.ERROR("Error in validate_mt_and_date_of_original_message : %s "%str(e))

    if validation_error:
        raise ValidationError(message = ''.join(validation_error))

def is_sender_or_receiver(acm_obj):
    ref = str(GetRelatedRef(acm_obj))
    if ref:
        ref_oid = ref.split('-')[1]
        related_conf = acm.FConfirmation[ref_oid]
        if related_conf:
            external_objs = FSwiftWriterUtils.get_external_object_for_acm_object(related_conf)
            for each_obj in external_objs:
                sub_typ = FSwiftWriterUtils.get_subtype_from_ext_obj(each_obj)
                if sub_typ in ['MT300', 'MT305', 'MT306', 'MT320', 'MT330', 'MT362', 'MT395']:
                    acm_object = FSwiftMLUtils.FSwiftExternalObject.get_acm_object_from_ext_object(each_obj)
                    if str(acm_object.Oid()) == ref_oid:
                        source = FSwiftMLUtils.FSwiftExternalObject.get_integration_type(each_obj)
                        if source == 'SwiftWriter':
                            return "Sender"
                        elif source == 'SwiftReader':
                            return "Receiver"

def GetRelatedRef(confirmation):
    relatedRef = ''
    if (FSwiftMLUtils.get_acm_version() >= 2016.4 and confirmation.Type() in (ConfirmationType.CHASER)) or confirmation.Type() in ('Chaser'):
        related_confirmation = confirmation.ChasingConfirmation()
        try:
            msg_type = 'MT' + str(FSwiftMLUtils.calculate_mt_type_from_acm_object(related_confirmation))
            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = related_confirmation, integration_type = 'Outgoing', msg_typ=msg_type)
            swift_message = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
            #ext_obj = FExternalObject.ExtReferences(subject= related_confirmation, subtype=msg_type).Last()
            #data = FSwiftMLUtils.get_external_value_using_ael(ext_obj.ReconciliationItem())
            #swift_message = data.At('swift_data')
            reg_exp = re.compile("20:(FA[C|S]-[0-9]*-[0-9]*)")
            relatedRef = reg_exp.findall(swift_message)[0]
        except Exception as e:
            notifier.ERROR("%s Error in GetRelatedRef : %s " % (msg_type, str(e)))
    return relatedRef

def get_narrative_description(confirmation):
    narrative_desc = ''
    if (FSwiftMLUtils.get_acm_version() >= 2016.4 and confirmation.Type() in (ConfirmationType.CHASER)) or confirmation.Type() in ('Chaser'):
        related_confirmation = confirmation.ChasingConfirmation()
        try:
            msg_type = 'MT' + str(FSwiftMLUtils.calculate_mt_type_from_acm_object(related_confirmation))
            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = related_confirmation, integration_type = 'Outgoing', msg_typ = msg_type)
            swift_message = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_obj, 'swift_data')
            mandatory_field_param = ast.literal_eval(getattr(FSwiftMLUtils.Parameters("FFXMMConfirmationOut_Config"), "MTChaserFields", "{}"))
            related_conf = FSwiftMLUtils.calculate_mt_type_from_acm_object(related_confirmation)
            related_mandatory = mandatory_field_param.get(related_conf)
            if related_mandatory:
                separator = getattr(FSwiftMLUtils.Parameters("FFXMMConfirmationOut_Config"), "Separator", None)
                if not separator:
                    separator = getattr(writer_config, "Separator", 'newline')
                for field in related_mandatory:
                    narrative_desc += ':' + field + ':' + FSwiftMLUtils.get_field_value(swift_message, field) + separator
            else:
                notifier.WARN("{0} 'MTChaserFields' parameter in 'FFXMMConfirmationOut_Config' not specified for {0} ".format(msg_type))
        except Exception as e:
            notifier.ERROR("%s Error in get_narrative_description : %s " % (msg_type, str(e)))
    return narrative_desc

def check_for_valid_related_reference(ref_conf, related_reference):
    """We go on looking for earlier confirmation references untill we find a confirmation for which a swift message is sent/acknowledged i.e. confirmation has an outgoing
    business process in state Acknowledged/Sent"""
    while ref_conf:
        bpr_obj = FSwiftMLUtils.get_business_process(ref_conf, "Outgoing")
        if bpr_obj and bpr_obj.CurrentStep().State().Name() in ['Acknowledged', 'Sent']:
            return ref_conf, related_reference
        ref_conf = ref_conf.ConfirmationReference()
        related_reference = "%s-%s" % (get_confirmation_reference_prefix(), str(ref_conf.Oid()))
    return ref_conf, related_reference

def get_location_code(location):
    code = ''
    if location:
        LOCATION_CODE = ast.literal_eval(getattr(fxmm_out_msg_config, 'LocationCode', "{}"))
        if location in list(LOCATION_CODE.values()):
            code = location
        else:
            code = LOCATION_CODE.get(location.upper())
    if not code:
        notifier.WARN("City name not in ISO country code and the English name of the location mapped list, Add in the\
                      Fparameter LOCATION_CODE")
    return code

def get_related_confirmation(confirmation):
    if FSwiftMLUtils.get_acm_version() >= 2016.4:
        if confirmation.Type() in (ConfirmationType.AMENDMENT, ConfirmationType.CANCELLATION):
            return confirmation.ConfirmationReference()
        elif confirmation.Type() in (ConfirmationType.CHASER):
            return confirmation.ChasingConfirmation()
    else:
        if confirmation.Type() in ("Amendment", "Cancellation"):
            return confirmation.ConfirmationReference()
        elif confirmation.Type() in ("Chaser"):
            return confirmation.ChasingConfirmation()

def get_confirmation_reference_prefix():
    if str(getattr(fxmm_out_msg_config, 'FAC', "")) == "":
        return str(getattr(writer_config, 'FAC', "FAC"))
    return str(getattr(fxmm_out_msg_config, 'FAC', None))

def get_type_of_operation(confirmation):
    return FSwiftWriterUtils.get_type_of_operation(confirmation)

def get_scope_of_operation(confirmation):
    '''This scope is valida across message types MT300, MT306, MT360, MT361, MT362
    No other scope is supported in FA as of now'''
    return "BILA"

def get_senders_bic(confirmation):
    if str(getattr(fxmm_out_msg_config, 'SwiftLoopBack', "")) == 'True':
        return str(getattr(fxmm_out_msg_config, 'SenderBICLoopBack', ""))
    elif str(getattr(writer_config, 'SwiftLoopBack', "")) == 'True':
        return str(getattr(writer_config, 'SenderBICLoopBack', ""))
    return confirmation.AcquirerAddress()

def get_receivers_bic(confirmation):
    if str(getattr(fxmm_out_msg_config, 'SwiftLoopBack', "")) == 'True':
        return str(getattr(fxmm_out_msg_config, 'ReceiverBICLoopBack', ""))
    elif str(getattr(writer_config, 'SwiftLoopBack', "")) == 'True':
        return str(getattr(writer_config, 'ReceiverBICLoopBack', ""))
    return confirmation.CounterpartyAddress()

def get_exchange_rate(confirmation):
    rate = ''
    trade = confirmation.Trade()
    if trade:
        rate = trade.Price()
    return rate

def get_swap_type(confirmation):
    ''' This together with settlement_method forms the mandatory field 23A in seq A of MT361 and MT362
        for MT362 and MT360 supported values are:
        CAPBUYER Party A bought the cap and paid the premium.
        CAPSELLER Party A sold the cap and received the premium.
        COLLARBYER Party A bought the collar and paid the premium.
        COLLARSLLR Party A sold the collar and received the premium.
        FIXEDFIXED IRS or CS where both parties pay fixed rates.
        FIXEDFLOAT IRS or CS where party A pays fixed and receives floating rates.
        FLOATFIXED IRS or CS where, party A pays floating and receives fixed rates.
        FLOATFLOAT IRS or CS where both Parties pay floating rates.
        FLOORBUYER Party A bought the floor and paid the premium.
        FLOORSLLER Party A sold the floor and received the premium.

        for MT361 supported values are:
        FIXEDFIXED    Both parties pay fixed rates
        FIXEDFLOAT    Party A pays fixed and receives floating rates
        FLOATFIXED    Party A pays floating and receives fixed rates
        FLOATFLOAT    Both parties pay floating rates
        VARBUYER    Party A pays the fixed rate of a variation swap.
        VARSELLER    Party A pays the floating amounts of annualised realised variance of the price changes of the underlying product.
        VOLABUYER    Party A pays the fixed rate of a volatility swap.
        VOLASELLER    Party A pays the floating amounts of annualised realised volatility of a given underlying asset.
    '''

    instrument = confirmation.Trade().Instrument()
    trade = confirmation.Trade()
    ins_type = instrument.InsType()
    swap_type = ''
    # if ins_type  == 'Swap':
    #     for leg in instrument.Legs():
    #         leg_type = leg.LegType().upper()
    #         if leg_type in ['COLLARED FLOAT', 'CAPPED FLOAT', 'FLOORED FLOAT']:
    #             leg_type = 'FLOAT'
    #         swap_type += leg_type

    if ins_type == "Swap":
        pay_leg = get_pay_leg(confirmation)
        pay_leg_type = pay_leg.LegType().upper()
        if pay_leg_type in ['COLLARED FLOAT', 'CAPPED FLOAT', 'FLOORED FLOAT']:
            pay_leg_type = 'FLOAT'
        receive_leg = get_receive_leg(confirmation)
        receive_leg_type = receive_leg.LegType().upper()
        if receive_leg_type in ['COLLARED FLOAT', 'CAPPED FLOAT', 'FLOORED FLOAT']:
            receive_leg_type = 'FLOAT'
        swap_type += pay_leg_type + receive_leg_type

    if ins_type == 'CurrSwap':
        pay_leg = get_pay_leg(confirmation)
        pay_leg_type = pay_leg.LegType().upper()
        receive_leg = get_receive_leg(confirmation)
        receive_leg_type = receive_leg.LegType().upper()
        swap_type += pay_leg_type + receive_leg_type

    if ins_type == 'VarianceSwap':
        quantity = trade.Quantity()
        swap_type = ins_type.upper()[:3]
        if quantity > 0:
            swap_type += 'BUYER'
        else:
            swap_type += 'SELLER'

    if ins_type == 'VolatilitySwap':
        quantity = trade.Quantity()
        swap_type = ins_type.upper()[:4]
        if quantity > 0:
            swap_type += 'BUYER'
        else:
            swap_type += 'SELLER'


    if ins_type == 'Cap':
        quantity = trade.Quantity()
        swap_type = ins_type.upper()
        if quantity > 0:
            swap_type += 'BUYER'
        else:
            swap_type += 'SELLER'

    if ins_type == 'Floor':
        quantity = trade.Quantity()
        swap_type = ins_type.upper()
        if quantity > 0:
            swap_type += 'BUYER'
        else:
            swap_type += 'SLLER'

    if instrument.ProductTypeChlItem() == 'Collar':
        swap_type = instrument.ProductTypeChlItem().upper()
        quantity = trade.Quantity()
        if quantity > 0:
            swap_type += 'BYER'
        else:
            swap_type += 'SLLR'

    return swap_type

def get_settlement_method(confirmation):
    '''For MT361 only'''
    return "GROSS"

def get_contract_number_party_a(confirmation):
    return confirmation.Trade().Oid()

def get_block_trade_indicator_for(confirmation):
    '''Optional field 17T.
    This field specifies whether the confirmed deal is a block trade
    and whether an MT 303 Forex/Currency Option Allocation Instruction,
    will be sent by the fund manager. Default value is N. '''
    return "N"

def get_split_settlement_indicator_for(confirmation):
    ''' Optional field 17U. '''
    return "N"

def get_effective_date(confirmation):
    return confirmation.Trade().Instrument().PayLeg().StartDate()

def get_termination_date(confirmation):
    return confirmation.Trade().Instrument().PayLeg().EndDate()

def get_business_day_convention(leg):
    return leg.PayDayMethod()

def get_business_day_convention_code(leg):
    business_day_method_fromFA = get_business_day_convention(leg)
    FA_business_day_to_SWIFT_convention = {'Following' : 'FOLLOWING',
                                           'FRN Convention' : 'FRN',
                                           'Mod. Following' : 'MODIFIEDF',
                                           'Preceding' : 'PRECEDING',
                                           'Mod. Preceding' : 'OTHER',
                                           'EOM' : 'OTHER',
                                           'FOM' : 'OTHER',
                                           'IMM' : 'OTHER',
                                           'Monthly IMM' : 'OTHER',
                                           'IMM-AUD' : 'OTHER',
                                           'CDS Convention' : 'OTHER',
                                           'BMA Convention' : 'OTHER'}
    return FA_business_day_to_SWIFT_convention.get(business_day_method_fromFA, 'OTHER')

def get_pay_leg(confirmation):
    for each_leg in confirmation.Trade().Instrument().Legs():
        if each_leg.PayLeg():
            return each_leg
    return None

def get_receive_leg(confirmation):
    for each_leg in confirmation.Trade().Instrument().Legs():
        if not each_leg.PayLeg():
            return each_leg
    return None

def get_fixed_rate_on_receive_leg(confirmation):
    receive_leg = get_receive_leg(confirmation)
    return receive_leg.FixedRate()

def get_fixed_rate_on_pay_leg(confirmation):
    pay_leg = get_pay_leg(confirmation)
    return pay_leg.FixedRate()

def get_cash_flows_from(leg, cash_flow_type):
    cash_flow_type = cash_flow_type.strip()
    return acm.FCashFlow.Select('leg = %d  and cashFlowType =%s' %(leg.Oid(), cash_flow_type)).SortByProperty('PayDate', ascending = True)

def get_cash_flow_details(leg, cash_flow_type, trade):
    cash_flows = get_cash_flows_from(leg, cash_flow_type)
    cash_flow_details = []
    calc_space = FSwiftMLUtils.get_calculation_space()
    for each_cf in cash_flows:
        cf_detail = {}
        cf_detail['PaymentDate'] = each_cf.PayDate()
        cf_detail['Currency'] = leg.Currency().Name()
        amount = each_cf.Calculation().Projected(calc_space, trade).Value().Number()
        if acm.Operations.IsValueInfNanOrQNan(amount):
            amount = 0
        cf_detail['Amount'] = abs(amount)
        cash_flow_details.append(cf_detail)
    return cash_flow_details

def get_floating_rate_option_from(floating_rate_reference):
    floating_rate_option = floating_rate_reference.FreeText()
    if floating_rate_option:
        return floating_rate_option
    return ""

def get_reset_date_specification_for(leg):
    if leg.ResetInArrear():
        return "LAST"
    else:
        return "FIRST"

def get_floating_ref_maturity_details(float_rate_ref):
    """We are deciding for OIS trades based on EndPeriod of the RateIndex.
       If floating reference is Swap then we look for Rolling frequence of fixed Leg"""
    number = "0"
    period = "D"
    if float_rate_ref.InsType() == "Swap":
        fixed_leg = None
        for each_leg in float_rate_ref.Legs():
            if each_leg.IsFixedLeg():
                fixed_leg = each_leg
                break
        number = fixed_leg.RollingPeriodCount()
        period = fixed_leg.RollingPeriodUnit()
    if float_rate_ref.InsType() == "RateIndex":
        number = str(float_rate_ref.ExpiryPeriod_count())
        period = float_rate_ref.ExpiryPeriod_unit()
    if number == "1" and period == "Days":
        return "0", "O"
    if number == "12" and period == "Months":
        return "1", "Y"
    return number, period[0]

def get_period_end_date_adjustment_indicator(leg):
    if leg.FixedCoupon():
        return "N"
    else:
        return "Y"

def get_number_of_cash_flows(leg, cash_flow_type):
    return len(get_cash_flows_from(leg, cash_flow_type))

def get_financial_centres_on(leg):
    financial_centers = []
    calendar_apis = ['PayCalendar', 'Pay2Calendar', 'Pay3Calendar', 'Pay4Calendar', 'Pay5Calendar']
    for each_calendar_api in calendar_apis:
        calendar = getattr(leg, each_calendar_api)()
        if calendar:
            financial_centers.append(calendar.BusinessCenter())
    return financial_centers

def get_number_of_financial_centres(leg):
    return len(get_financial_centres_on(leg))

def get_party_b_currency(confirmation):
    receive_leg = get_receive_leg(confirmation)
    if receive_leg:
        return receive_leg.Currency().Name()

def get_party_b_notional_amount(confirmation):
    #Getting notional amount from calcualtion space because we will be getting the interest details from
    #calc_space. This will make it consistent.
    receive_leg = get_receive_leg(confirmation)
    ins = confirmation.Trade().Instrument()
    calc_space = FSwiftMLUtils.get_calculation_space()
    value = ins.Calculation().Nominal(calc_space, confirmation.Trade(), None, receive_leg.Currency())
    if value:
        return abs(value.Number())
    return ''

def get_party_a_currency(confirmation):
    pay_leg = get_pay_leg(confirmation)
    if pay_leg:
        return pay_leg.Currency().Name()

def get_party_a_notional_amount(confirmation):
    #Getting notional amount from calculation space because we will be getting the interest details from
    #calc_space. This will make it consistent.
    pay_leg = get_pay_leg(confirmation)
    ins = confirmation.Trade().Instrument()
    calc_space = FSwiftMLUtils.get_calculation_space()
    value = ins.Calculation().Nominal(calc_space, confirmation.Trade(), None, pay_leg.Currency())
    if value:
        return abs(value.Number())
    return ''

##def get_party_details(party, party_account, get_intermediary_details = False):
##    party_details = {}
##    if party_account:
##        if get_intermediary_details:
##            party_details['ACCOUNT'] = party_account.Account2()
##        else:
##            party_details['ACCOUNT'] = party_account.Account()
##        party_details['BIC'] = get_party_bic(party_account, get_intermediary_details)
##    if party:
##        party_details['NAME'] = get_party_full_name(party)
##        party_details['ADDRESS'] = get_party_address(party)
##    return party_details

def get_party_details(party, party_account, intermediary_or_correspondent = None):
    party_details = {}
    if party_account:
        if intermediary_or_correspondent == 'INTERMEDIARY':
            party_details['ACCOUNT'] = party_account.Account2()
        else:
            party_details['ACCOUNT'] = party_account.Account()
        party_details['BIC'] = get_party_bic(party_account, intermediary_or_correspondent)
    if party:
        party_details['NAME'] = get_party_full_name(party)
        party_details['ADDRESS'] = get_party_address(party)
    return party_details


##def get_party_bic(account, get_intermediary_details= False):
##    bic = ''
##    if get_intermediary_details:
##        bic2 = account.Bic2()
##        if bic2:
##            return bic2.Name()
##    else:
##        bic = account.Bic().Name()
##    if account.NetworkAlias():
##        bic = account.NetworkAlias().Alias()
##    if not bic:
##        assert account.Party(), "The account has no party reference"
##        bic = account.Party().Swift()
##    return bic

def get_party_bic(account, intermediary_or_correspondent=None):
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
    use_party_full_name = getattr(fxmm_out_msg_config, 'UsePartyFullName', None)
    if not use_party_full_name:
        use_party_full_name = getattr(writer_config, 'UsePartyFullName', False)
    return FSwiftMLUtils.get_party_full_name(party, bool(use_party_full_name))

def get_terms_and_conditions_option(swift_message_type):
    message_config = FSwiftMLUtils.Parameters('F%sOut_Config' % swift_message_type)
    return str(getattr(message_config, 'TermsConditions', ""))


def get_terms_and_conditions(confirmation, swift_message_type):
    terms_and_conditions = get_terms_and_conditions_option(swift_message_type)
    if swift_message_type == "MT320":
        if confirmation.Trade().Instrument().Legs():
            leg = confirmation.Trade().Instrument().Legs()[0]
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                if leg.LegType() == LegType.FLOAT:
                    terms_and_conditions = '/FLTR/'
            else:
                if leg.LegType() == 'Float':
                    terms_and_conditions = '/FLTR/'
    return  terms_and_conditions


def get_party_address(party):
    address = party.Address()
    if party.Address() != party.Address2():
        address = address + party.Address2()
    address = "%s %s %s" % (address, party.City(), party.Country())
    return address

##def get_party_a_details(confirmation):
##    party_details = {}
##    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
##    money_flow = conf_wrapper_obj.buy_money_flow()
##    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
##    if not money_flow:
##        money_flow = conf_wrapper_obj.money_flow()
##    if money_flow:
##        acquirer = money_flow.Acquirer()
##        acquirer_account = money_flow.AcquirerAccount()
##        return get_party_details(acquirer, acquirer_account)
##    return party_details

def get_party_a_details(confirmation):
    ''' Changed accroding to discussions so the logic is:
        Party A should use the account for the amount to be paid (sold amount)
        and Party B should use the account for the amount to be received (buy amount) (buy/sell direction seen from sender of MT300 = acquirer)  '''
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not money_flow:
        money_flow = conf_wrapper_obj.money_flow()
    if money_flow:
        acquirer = money_flow.Acquirer()
        acquirer_account = money_flow.AcquirerAccount()
        return get_party_details(acquirer, acquirer_account)
    return party_details


##def get_party_b_details(confirmation):
##    party_details = {}
##    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
##    money_flow = conf_wrapper_obj.sell_money_flow()
##    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
##    if not money_flow:
##        money_flow = conf_wrapper_obj.money_flow()
##    if money_flow:
##        counterparty = money_flow.Counterparty()
##        counterparty_account = money_flow.CounterpartyAccount()
##        return get_party_details(counterparty, counterparty_account)
##    return party_details

def get_party_b_details(confirmation):
    ''' Changed accroding to discussions so the logic is:
        Party A should use the account for the amount to be paid (sold amount)
        and Party B should use the account for the amount to be received (buy amount) (buy/sell direction seen from sender of MT300 = acquirer)  '''
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not money_flow:
        money_flow = conf_wrapper_obj.money_flow()
    if money_flow:
        counterparty = money_flow.Counterparty()
        counterparty_account = money_flow.CounterpartyAccount()
        return get_party_details(counterparty, counterparty_account)
    return party_details

def get_principal_amount(confirmation):
    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    curr = confirmation.Trade().Currency().Name()
    amount = confirmation.Trade().Premium()
    return apply_currency_precision(curr, abs(amount))

def get_principal_currency(confirmation):
    assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
    return confirmation.Trade().Currency().Name()

def get_settle_amount(confirmation):
    calc_space = FSwiftMLUtils.get_calculation_space()
    if FSwiftConfirmationUtils.get_event_type(confirmation) == 'ROLL':
        originalTrade = acm.FTrade[confirmation.Trade().ContractTrdnbr()]
        if originalTrade:
            totalAmount = 0
            prolongingAmount = 0
            for moneyFlow in originalTrade.MoneyFlows():
                if moneyFlow.Type() == 'Fixed Amount':
                    number = moneyFlow.Calculation().Projected(calc_space).Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(number):
                        number = 0
                    totalAmount += number
            for moneyFlow in confirmation.Trade().MoneyFlows():
                if moneyFlow.Type() == 'Fixed Amount':
                    number = moneyFlow.Calculation().Projected(calc_space).Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(number):
                        number = 0
                    prolongingAmount += number

            curr = confirmation.Trade().Currency()
            amountDiff = prolongingAmount - totalAmount
            return apply_currency_precision(curr, amountDiff)

    return ''

def get_settle_currency(confirmation):
    if FSwiftConfirmationUtils.get_event_type(confirmation) == 'ROLL':
        assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
        return confirmation.Trade().Currency().Name()
    return ''

def get_next_interest_due_date(confirmation):
    ret_val = ''
    legs = confirmation.Trade().Instrument().Legs()
    dates = []
    for aLeg in legs:
        for aCashFlow in aLeg.CashFlows():
            endDate = aCashFlow.EndDate()
            if endDate and endDate >= acm.Time.DateToday():
                dates.append(endDate)

    if len(dates) > 0:
        dates.sort()

        if dates[0] == acm.Time.DateToday():
            if len(dates) > 1:
                ret_val = dates[1]
            else:
                ret_val = dates[0]
        else:
            ret_val = dates[0]
    else:
        ret_val = confirmation.Trade().Instrument().ExpiryDateOnly()

    return ret_val

def get_SIA_party_receiving_agent_option(party, confirmation, swift_message_type, option):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    if not money_flow:
        option = ''
    return option

def get_SIA_party_receiving_agent_account(party, confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    account = ''
    if money_flow:
        if ('A' == party) and money_flow.CounterpartyAccount():
            account = money_flow.CounterpartyAccount().Account()
        elif ('B' == party) and money_flow.AcquirerAccount():
            account = money_flow.AcquirerAccount().Account()

    return account

def get_SIA_party_receiving_agent_bic(party, confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    bic = ''
    if money_flow:
        if ('A' == party) and money_flow.CounterpartyAccount():
            if money_flow.CounterpartyAccount().Bic():
                bic = money_flow.CounterpartyAccount().Bic().Alias()
        elif ('B' == party) and money_flow.AcquirerAccount():
            if money_flow.AcquirerAccount().Bic():
                bic = money_flow.AcquirerAccount().Bic().Alias()

    return bic

def get_SIA_party_receiving_agent_name(party, confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    name = ''
    if money_flow:
        corrBank = None
        if ('A' == party) and money_flow.CounterpartyAccount():
            corrBank = money_flow.CounterpartyAccount().CorrespondentBank()
        elif ('B' == party) and money_flow.AcquirerAccount():
            corrBank = money_flow.AcquirerAccount().CorrespondentBank()

        if corrBank:
            name = FSwiftMLUtils.get_party_full_name(corrBank)
    return name

def get_SIA_party_receiving_agent_address(party, confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    address = ''
    if money_flow:
        corrBank =None
        if ('A' == party) and money_flow.CounterpartyAccount():
            corrBank = money_flow.CounterpartyAccount().CorrespondentBank()
        elif ('B' == party) and money_flow.AcquirerAccount():
            corrBank = money_flow.AcquirerAccount().CorrespondentBank()

        if corrBank:
            address = get_party_address(corrBank)
    return address

def get_agreement_signed_date(confirmation):
    doc_type = confirmation.Trade().DocumentType().Name()
    agreement_signed_date = None
    for each in confirmation.Trade().Counterparty().Agreements():
        if each.DocumentTypeChlItem().Name() == doc_type:
            agreement_signed_date = each.Dated()
            return agreement_signed_date
    if not agreement_signed_date:
        return FSwiftConfirmationUtils.get_value_date(confirmation)

def get_type_and_version_of_agreement(confirmation):
    agreement_type_details = get_agreement_type_details(confirmation)
    return _parse_agreement_type_and_version(agreement_type_details)

def get_agreement_type_details(confirmation):
    return confirmation.Trade().DocumentType().Name()

def _parse_agreement_type_and_version(agreement_type_details):
    """Here default value for type of agreement is 'OTHER' and
       for version of agreement it is '0000'. If type of agreement is
       'ISDA' and no version is specified then version will be '0000'"""
    agreement_standards_to_check_for = ["AFB", "DERV", "ISDA"]
    reg_exp = "[0-9]{4}"
    reg_obj = re.compile(reg_exp)
    type_of_agreement = "OTHER"
    version_of_agreement = "0000"
    for each in agreement_standards_to_check_for:
        if agreement_type_details.startswith(each):
            type_of_agreement = each
            version_part = re.search(reg_obj, agreement_type_details)
            if version_part:
                version_of_agreement = version_part.group()
            return type_of_agreement, version_of_agreement
    return type_of_agreement, version_of_agreement

def get_buy_amount(confirmation):
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    return conf_wrapper_obj.buy_amount()

def get_buy_currency(confirmation):
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    return conf_wrapper_obj.buy_money_flow().Currency().Name()

def get_sell_amount(confirmation):
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    return conf_wrapper_obj.sell_amount()

def get_sell_currency(confirmation):
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    return conf_wrapper_obj.sell_money_flow().Currency().Name()

def get_counterparty_delivery_agent_details(confirmation):
    '''Account&Party from which counterparty will transfer funds to acquirer'''
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    buy_money_flow = conf_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not buy_money_flow:
        buy_money_flow = conf_wrapper_obj.money_flow()
    if buy_money_flow:
        party = buy_money_flow.CounterpartyAccount().CorrespondentBank()
        party_account = buy_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details

def get_counterparty_intermediary_details(confirmation):
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    sell_money_flow = conf_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = conf_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().CorrespondentBank2()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account, "INTERMEDIARY")
    return party_details

def get_counterparty_receiving_agent_details(confirmation):
    '''Account&Party in which acquirer will receive funds from counterparty'''
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    sell_money_flow = conf_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = conf_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().CorrespondentBank()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details


def get_acquirer_delivery_agent_details(confirmation):
    '''Account&Party from which acquirer will transfer funds to counterparty'''
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    sell_money_flow = conf_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = conf_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.AcquirerAccount().CorrespondentBank()
        party_account = sell_money_flow.AcquirerAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details

def get_acquirer_intermediary_details(confirmation):
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    buy_money_flow = conf_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not buy_money_flow:
        buy_money_flow = conf_wrapper_obj.money_flow()
    if buy_money_flow:
        party = buy_money_flow.AcquirerAccount().CorrespondentBank2()
        party_account = buy_money_flow.AcquirerAccount()
        return get_party_details(party, party_account, "INTERMEDIARY")
    return party_details

def get_acquirer_receiving_agent_details(confirmation):
    '''Account&Party in which counterparty will receive funds from acquirer'''
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    buy_money_flow = conf_wrapper_obj.buy_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not buy_money_flow:
        buy_money_flow = conf_wrapper_obj.money_flow()
    if buy_money_flow:
        party = buy_money_flow.AcquirerAccount().CorrespondentBank()
        party_account = buy_money_flow.AcquirerAccount()
        return get_party_details(party, party_account, "CORRESPONDENT")
    return party_details


def get_beneficiary_institution_details(confirmation):
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    sell_money_flow = conf_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = conf_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().CorrespondentBank()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account)
    return party_details

def get_beneficiary_institution_details_MT300(confirmation):
    party_details = {}
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    sell_money_flow = conf_wrapper_obj.sell_money_flow()
    # buy_money_flow sell_money_flow will populate in multi curr scenario for single curr cases we need money_flow
    if not sell_money_flow:
        sell_money_flow = conf_wrapper_obj.money_flow()
    if sell_money_flow:
        party = sell_money_flow.CounterpartyAccount().Party()
        party_account = sell_money_flow.CounterpartyAccount()
        return get_party_details(party, party_account)
    return party_details

def get_day_count_method(leg):
    return leg.DayCountMethod()

def get_day_count_method_code(leg):
    day_count_mapping = { '30E/360':   '30E/360',
                      '30/360':   '360/360',
                      '30U/360':   '360/360',
                      'NL/360':   '360/360',
                      'NL/365':   'ACT/365',
                      'NL/ActISDA':   'ACT/365',
                      '360/360':   '360/360',
                      'Actual/360': 'ACT/360',
                      'Act/360':   'ACT/360',
                      'Act/365':   'ACT/365',
                      'Act/365L':   'ACT/365',
                      'ACT/ACTISDA':   'ACT/365',
                      'ACT/ACTISMA':   'ACT/365',
                      'ACT/ACTICMA':   'ACT/365',
                      'ACT/ACTAFB':   'ACT/365',}
    day_count_method_fromFA = get_day_count_method(leg)
    return day_count_mapping.get(day_count_method_fromFA, 'ACT/365')

  # ============================ MT362 ============================

def get_IRP_partyB_period_start_date(confirmation):
    """ Field 30X in MT362
    :param confirmation: FConfirmation object
    :return: str:
    """
    start_date = ''
    cashflow = get_IRP_partyB_cashflow(confirmation)
    if cashflow:
        start_date = cashflow.StartDate()
    return start_date

def get_IRP_partyB_cashflow(confirmation):
    """ Get PartyB cashflows
    :param confirmation: FConfirmation object
    :return: FCashflow object
    """
    cash_flow = ''
    trade = confirmation.Trade()
    if trade:
        settlement_method = get_settlement_method_MT362(confirmation)
        if settlement_method == 'GROSS':
            reset_cashflow = get_reset_cashflow(confirmation)
            if (trade.Nominal() > 0 and not reset_cashflow.Leg().PayLeg()) or \
                    (trade.Nominal() < 0 and reset_cashflow.Leg().PayLeg()):
                cash_flow = reset_cashflow
        elif settlement_method == 'NET':
            pay_cashflow, receive_cashflow = get_pay_and_receive_cashflows(confirmation)
            if trade.Nominal() > 0:
                cash_flow = receive_cashflow
            else:
                cash_flow = pay_cashflow
    return cash_flow

def get_settlement_method_MT362(confirmation):
    """ This together with type_swap forms the mandatory field 23A in seq A.
       It is assumed that if a cashFlow on the other leg has the same pay date,
       the payments will be netted'''
    :param confirmation: FConfirmation object
    :return: str: GROSS or NET
    """
    reset_cash_flow = get_reset_cashflow(confirmation)
    settlement_method = 'GROSS'
    if get_cashflow_with_same_paydate_and_currency(confirmation, reset_cash_flow):
        settlement_method = 'NET'
    return settlement_method

def get_reset_cashflow(confirmation):
    """ Get reset cashflow from comfirmation
    :param confirmation:
    :return: FCashflow object
    """
    reset = get_reset(confirmation)
    cash_flow = ''
    if reset:
        cash_flow = reset.CashFlow()
    return cash_flow

def get_reset(confirmation):
    """ Get reset from the confirmation
    :param confirmation:
    :return:
    """
    return confirmation.Reset()

def get_cashflow_with_same_paydate_and_currency(confirmation, cashFlow):
    """ Get other cashflow with same currency and pay date.
    :param confirmation:
    :param cashFlow: FCashflow objet
    :return: FCashflow object
    """
    other_leg = get_other_leg_with_same_currency(confirmation)
    other_cashflow = ''
    if other_leg and cashFlow:
        for cf in other_leg.CashFlows():
            if cf.PayDate() == cashFlow.PayDate():
                if cf.Leg().LegType() == 'Fixed':
                    other_cashflow = cf
                else:
                    for reset in cf.Resets():
                        if reset.FixingValue():
                            other_cashflow = cf
                            break
                break
    return other_cashflow

def get_other_leg_with_same_currency(confirmation):
    """ Get other leg with same currency
    :param confirmation:
    :return:
    """
    leg = get_reset_cashflow_leg(confirmation)
    other_leg = ''
    if leg:
        for l in leg.Instrument().Legs():
            if l != leg and l.Currency() == leg.Currency():
                other_leg = l
                break
    return other_leg

def get_reset_cashflow_leg(confirmation):
    """ Get leg type of the reset cash flow.
    :param confirmation:
    :return: FLeg object
    """
    reset_cashflow_leg = ''
    reset_cashflow = get_reset_cashflow(confirmation)
    if reset_cashflow:
        reset_cashflow_leg = reset_cashflow.Leg()
    return reset_cashflow_leg


def get_pay_and_receive_cashflows(confirmation):
    """ Get pay and receive cashhflow
    :param confirmation:
    :return:
    """
    payCashFlow = ''
    receiveCashFlow = ''
    resetCashFlow = get_reset_cashflow(confirmation)
    otherCashFlow = get_cashflow_with_same_paydate_and_currency(confirmation, resetCashFlow)
    if resetCashFlow.Leg().PayLeg():
        payCashFlow = resetCashFlow
        receiveCashFlow = otherCashFlow
    else:
        payCashFlow = otherCashFlow
        receiveCashFlow = resetCashFlow
    return payCashFlow, receiveCashFlow

def get_partyB_number_repetitions(confirmation):
    ''' Mandatory field 18A in seq C'''
    return 1

def get_nap_partyB_pay_amount(confirmation):
    """This together with nap_party_b_currency forms the mandatory field 32M in seq C.
        If counterparty is not paying '' is returned.
    :param confirmation:
    :return: str: amount
    """
    amount = get_nap_amount(confirmation)
    if amount > 0:
        return abs(amount)
    return ''

def get_nap_amount(confirmation):
    """ Get nap amount from the confirmation cashflows.
    :param confirmation:
    :return:
    """
    amount = 0.0
    cash_flow = get_reset_cashflow(confirmation)
    if cash_flow:
        trade = confirmation.Trade()
        calc_space = FSwiftMLUtils.get_calculation_space()
        projected_calc = cash_flow.Calculation().Projected(calc_space, trade)
        if projected_calc:
            if type(projected_calc) == int:
                amount = float(projected_calc)
            else:
                amount = projected_calc.Value().Number()
                if acm.Operations.IsValueInfNanOrQNan(amount):
                    amount = 0
        other_cashflow = get_cashflow_with_same_paydate_and_currency(confirmation, cash_flow)
        if other_cashflow:
            projected_calc = other_cashflow.Calculation().Projected(calc_space, trade)
            if projected_calc:
                if type(projected_calc) == int:
                    amount = amount + float(projected_calc)
                else:
                    number = projected_calc.Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(amount):
                        number = 0
                    amount = amount + number
        leg = get_reset_cashflow_leg(confirmation)
        if leg:
            currency = leg.Currency()
            currencyName = ''
            if currency:
                currencyName = currency.Name()
            if currencyName:
                amount = apply_currency_precision(currencyName, amount)
    return amount

def get_IRP_partyA_period_start_date(confirmation):
    """ Get period start date for the partyA. Mandatory field 30X in seq D
    :param confirmation:
    :return:
    """
    start_date = ''
    cash_flow = get_IRP_partyA_cashflow(confirmation)
    if cash_flow:
        start_date = cash_flow.StartDate()
    return start_date

def get_IRP_partyA_period_end_date(confirmation):
    """ Get period end date for the partyA. Mandatory field 30Q in seq D
    :param confirmation:
    :return:
    """
    end_date = ''
    cash_flow = get_IRP_partyA_cashflow(confirmation)
    if cash_flow:
        end_date = cash_flow.EndDate()
    return end_date

def get_IRP_partyA_cashflow(confirmation):
    """ Get partyA cashflow details
    :param confirmation:
    :return:
    """
    cashFlow = ''
    trade = confirmation.Trade()
    if trade:
        settlement_method = get_settlement_method_MT362(confirmation)
        if settlement_method == 'GROSS':
            reset_cashflow = get_reset_cashflow(confirmation)
            if (trade.Nominal() > 0 and reset_cashflow.Leg().PayLeg()) or \
                    (trade.Nominal() < 0 and not reset_cashflow.Leg().PayLeg()):
                cashFlow = reset_cashflow
        elif settlement_method == 'NET':
            payCashFlow, receiveCashFlow = get_pay_and_receive_cashflows(confirmation)
            if trade.Nominal() > 0:
                cashFlow = payCashFlow
            else:
                cashFlow = receiveCashFlow
    return cashFlow

def get_PartyA_number_repetitions(confirmation):
    """ Mandatory field 18A in seq E
    :param confirmation:
    :return:
    """
    return 1

def get_nap_partyA_pay_amount(confirmation):
    """This together with nap_party_a_currency forms the mandatory field 32M in seq E.
    If acquirer is not paying '' is returned.
    :param confirmation:
    :return:
    """
    amount = get_nap_amount(confirmation)
    if amount < 0:
        return abs(amount)
    return ''

def get_senders_reference(confirmation):
    """ Get Confirmation Oid as senders reference number.
    :param confirmation:
    :return:
    """
    senders_reference = ''
    if confirmation:
        senders_reference = confirmation.Oid()
    return senders_reference

def get_termination_date_MT362(confirmation):
    """ Get termination date from the reset cashflow leg. 30P in seq A.
    :param confirmation:
    :return:
    """
    term_date = ''
    leg = get_reset_cashflow_leg(confirmation)
    if leg:
        term_date = leg.EndDate()
    return term_date

def get_effective_date_MT362(confirmation):
    """ Mandatory field 30V in seq A, MT362
    :param confirmation:
    :return:
    """
    effective_date = ''
    leg = get_reset_cashflow_leg(confirmation)
    if leg:
        effective_date = leg.StartDate()
    return effective_date

def get_IRP_partyB_curr(confirmation):
    """ Get partyB cuurency from the cashflow
    :param confirmation:
    :return:
    """
    currency = ''
    cash_flow = get_IRP_partyB_cashflow(confirmation)
    if cash_flow:
        currency = cash_flow.Leg().Currency().Name()
    return currency

def get_IRP_partyB_not_amount(confirmation):
    """  This together with irp_party_b_curr forms the mandatory field 33F in seq B.
    :param confirmation:
    :return:
    """
    nominal_amount = ''
    cash_flow = get_IRP_partyB_cashflow(confirmation)
    if cash_flow:
        nominal_amount = abs(get_IRP_nominal_amount(confirmation, cash_flow))
    return nominal_amount

def get_IRP_nominal_amount(confirmation, cash_flow):
    """
    :param confirmation:
    :param cashFlow:
    :return:
    """
    nominal = ''
    trade = confirmation.Trade()
    if cash_flow:
        calc_space = FSwiftMLUtils.get_calculation_space()
        value = cash_flow.Calculation().Nominal(calc_space, trade, cash_flow.Leg().Currency())
        if value:
            nominal = value.Number()
    return nominal

def get_IRP_partyB_period_end_date(confirmation):
    """ Optional field 30Q in seq B
    :param confirmation:
    :return:
    """
    end_date = ''
    cashFlow = get_IRP_partyB_cashflow(confirmation)
    if cashFlow:
        end_date = cashFlow.EndDate()
    return end_date

def get_IRP_partyB_reset_rate_formatted(confirmation):
    """ Mandatory field 37G in seq B
    :param confirmation:
    :return:
    """
    return str(get_IRP_partyB_reset_rate(confirmation))[:13]

def get_IRP_partyB_reset_rate(confirmation):
    """
    :param confirmation:
    :return:
    """
    assert confirmation.Reset(), "The confirmation has no reset"
    fixingValue = 0.0
    cashFlow = get_IRP_partyB_cashflow(confirmation)
    if cashFlow:
        if cashFlow == get_reset_cashflow(confirmation):
            fixingValue = confirmation.Reset().FixingValue()
        if not fixingValue:
            if cashFlow.Leg().LegType() == 'Fixed':
                fixingValue = cashFlow.Leg().FixedRate()
            else:
                for reset in cashFlow.Resets():
                    if reset.FixingValue():
                        fixingValue = reset.FixingValue()
                        break
    return fixingValue

def get_IRP_cap_rate(confirmation):
    """ Optional field 37V in seq B and seq D
    :param confirmation:
    :return:
    """
    instrument = confirmation.Trade().Instrument()
    rate = ''
    if instrument.InsType() == 'Cap':
        rate = str(instrument.Legs()[0].Strike())[:12]
    return rate

def get_IRP_floor_rate(confirmation):
    """ Optional field 37G in seq B and seq D
    :param confirmation:
    :return:
    """
    instrument = confirmation.Trade().Instrument()
    rate = ''
    if instrument.InsType() == 'Floor':
        rate = str(instrument.Legs()[0].Strike())[:12]
    return rate

def get_IRP_partyB_spread(confirmation):
    """ Mandatory field 37R in seq B
    :param confirmation:
    :return:
    """
    spread = 0.0
    cashFlow = get_IRP_partyB_cashflow(confirmation)
    if cashFlow and (cashFlow == get_reset_cashflow(confirmation) or cashFlow.Leg().LegType() == 'Float'):
        spread = cashFlow.Spread()
    return spread

def get_IRP_partyB_total_rate(confirmation):
    """ Mandatory field 37M in seq B and seq D
    :param confirmation:
    :return:
    """
    total_rate = 0.0
    cashFlow = get_IRP_partyB_cashflow(confirmation)
    if cashFlow == get_reset_cashflow(confirmation):
        total_rate = cashFlow.Spread()
    total_rate = str(total_rate + get_IRP_partyB_reset_rate(confirmation))[:13]
    return total_rate

def get_IRP_partyB_payment_date(confirmation):
    """ Mandatory field 30F in seq B
    :param confirmation:
    :return:
    """
    payment_date = ''
    cashFlow = get_IRP_partyB_cashflow(confirmation)
    if cashFlow:
        payment_date = cashFlow.PayDate()
    return payment_date

# def get_partyB_number_repetitions(confirmation):
#     """ Mandatory field 18A in seq C
#     :param confirmation:
#     :return:
#     """
#     return 1

def get_nap_pay_date(confirmation):
    """ Mandatory field 30F in seq C and seq E
    :param confirmation:
    :return:
    """
    pay_date = ''
    cashFlow = get_reset_cashflow(confirmation)
    if cashFlow:
        pay_date = cashFlow.PayDate()
    return pay_date

def get_nap_currency(confirmation):
    """ This together with nap amount forms the mandatory field 32M in seq C and seq E
    :param confirmation:
    :return:
    """
    currency = ''
    leg = get_reset_cashflow_leg(confirmation)
    if leg:
        currency = leg.Currency().Name()
    return currency

def get_IRP_partyA_currency(confirmation):
    """ This together with irp_party_a_amt forms the mandatory field 33F in seq D.
    :param confirmation:
    :return:
    """
    currency = ''
    cashFlow = get_IRP_partyA_cashflow(confirmation)
    if cashFlow:
        currency = cashFlow.Leg().Currency().Name()
    return currency

def get_IRP_partyA_not_amount(confirmation):
    """  This together with IRP_partyA_currency forms the mandatory field 33F in seq B.
    :param confirmation:
    :return:
    """
    nominal_amount = ''
    cash_flow = get_IRP_partyA_cashflow(confirmation)
    if cash_flow:
        nominal_amount = abs(get_IRP_nominal_amount(confirmation, cash_flow))
    return nominal_amount

def get_IRP_partyA_reset_rate_formatted(confirmation):
    """ Mandatory field 37G in seq D
    :param confirmation:
    :return:
    """
    return str(get_IRP_partyA_reset_rate(confirmation))[:13]

def get_IRP_partyA_reset_rate(confirmation):
    """
    :param confirmation:
    :return:
    """
    assert confirmation.Reset(), "The confirmation has no reset"
    fixingValue = 0.0
    cashFlow = get_IRP_partyA_cashflow(confirmation)
    if cashFlow:
        if cashFlow == get_reset_cashflow(confirmation):
            fixingValue = confirmation.Reset().FixingValue()
        if not fixingValue:
            if cashFlow.Leg().LegType() == 'Fixed':
                fixingValue = cashFlow.Leg().FixedRate()
            else:
                for reset in cashFlow.Resets():
                    if reset.FixingValue():
                        fixingValue = reset.FixingValue()
                        break
    return fixingValue

def get_IRP_partyA_spread(confirmation):
    """ Mandatory field 37R in seq D
    :param confirmation:
    :return:
    """
    spread = 0.0
    cashFlow = get_IRP_partyA_cashflow(confirmation)
    if cashFlow and (cashFlow == get_reset_cashflow(confirmation) or cashFlow.Leg().LegType() == 'Float'):
        spread = cashFlow.Spread()
    return spread

def get_IRP_partyA_total_rate(confirmation):
    """ Mandatory field 37M in seq D
    :param confirmation:
    :return:
    """
    total_rate = 0.0
    cashFlow = get_IRP_partyA_cashflow(confirmation)
    if cashFlow == get_reset_cashflow(confirmation):
        total_rate = cashFlow.Spread()
    total_rate = str(total_rate + get_IRP_partyA_reset_rate(confirmation))[:13]
    return total_rate

def get_IRP_partyA_payment_date(confirmation):
    """ Mandatory field 30F in seq D
    :param confirmation:
    :return:
    """
    payment_date = ''
    cashFlow = get_IRP_partyA_cashflow(confirmation)
    if cashFlow:
        payment_date = cashFlow.PayDate()
    return payment_date

def is_buy_or_sell(confirmation):

    if confirmation.Trade().Quantity() >= 0:
        return 'BUY'
    else:
        return 'SELL'


def is_call_or_put(confirmation):

    if confirmation.Trade().Instrument().IsCallOption():
        return 'CALL'
    else:
        return 'PUT'

def get_exercise_type(confirmation):
    return confirmation.Trade().Instrument().ExerciseType()

def get_exercise_date(confirmation):
    return confirmation.Trade().AcquireDay()

def get_earliest_exercise_date(confirmation):
    if confirmation.Trade().Instrument().ExerciseType() == ExerciseType.AMERICAN:
        return confirmation.Trade().ValueDay()
    else:
        return ''

def get_option_expiry_details(confirmation):
    expiry_details = {}
    expiry_details['EXPIRY_DETAILS_DATE'] = confirmation.Trade().Instrument().ExpiryDateOnly()
    expiry_time = ''
    fixing_source = confirmation.Trade().Instrument().FixingSource()
    if fixing_source:
        expiry_time = fixing_source.ExternalCutOff()
    expiry_details['EXPIRY_DETAILS_TIME'] = expiry_time
    loc_code = ''
    fixing_source = confirmation.Trade().Instrument().FixingSource()
    if fixing_source:
        expiry_location = fixing_source.City().upper()
        loc_code = get_location_code(expiry_location)
    expiry_details['EXPIRY_DETAILS_LOCATION'] = loc_code
    return expiry_details

def get_option_expiry_date(confirmation):
    return confirmation.Trade().Instrument().ExpiryDateOnly()

def get_option_expiry_location(confirmation):
    expiry_location = ''
    fixing_source = confirmation.Trade().Instrument().FixingSource()
    if fixing_source:
        expiry_location = fixing_source.City().upper()
    expiry_location_code = get_location_code(expiry_location)
    return expiry_location_code

def get_option_expiry_time(confirmation):
    expiry_time = ''
    fixing_source = confirmation.Trade().Instrument().FixingSource()
    if fixing_source:
        expiry_time = fixing_source.ExternalCutOff()
    return expiry_time

def get_settlement_date(confirmation):
    return confirmation.Trade().Instrument().DeliveryDate()

def get_settlement_type(confirmation):
    type_dict = {SettleType.PHYSICAL_DELIVERY: 'PRINCIPAL', SettleType.CASH: 'NETCASH'}
    settl_type = confirmation.Trade().Instrument().SettlementType()
    return type_dict.get(settl_type, '')

def get_underlying_currency(confirmation):
    '''Currency on which FX option is written'''
    underlying_currency = ''
    underlying_ins = confirmation.Trade().Instrument().Underlying()
    if underlying_ins:
        underlying_currency = underlying_ins.Name()
    return underlying_currency

def get_underlying_amount(confirmation):
    return abs(confirmation.Trade().Quantity())

def get_strike_price(confirmation):
    return confirmation.Trade().Instrument().StrikePrice()

def get_strike_currency(confirmation):
    '''Strike currency and counter currency are same'''
    return confirmation.Trade().Instrument().StrikeCurrency().Name()

def get_counter_amount(confirmation):
    contract_size = confirmation.Trade().Instrument().ContractSize()
    strike_price = confirmation.Trade().Instrument().StrikePrice()
    quantity = confirmation.Trade().Quantity()
    quantity = abs(quantity)
    return contract_size * quantity * strike_price

def get_counter_currency(confirmation):
    '''Currency which will be trading against underlying currency'''
    return confirmation.Trade().Instrument().StrikeCurrency().Name()

def get_premium_price(confirmation):
    return abs(confirmation.Trade().Price())

def get_premium_currency(confirmation):
    '''The currency in which premium for buying option is paid. This can be different from underlying and counter currency'''
    return confirmation.Trade().Currency().Name()

def get_sender_to_recieverinfo(confirmation):
    return 'SENDER TO RECEIVER INFORMATION'

def get_premium_payment_date(confirmation):
    return confirmation.Trade().ValueDay()

def get_premium_payment_currency(confirmation):
    return confirmation.Trade().Currency().Name()

def get_premium_payment_amount(confirmation):
    return abs(confirmation.Trade().Premium())

def get_currency_pair(confirmation):
    curr1 = confirmation.Trade().Instrument().Underlying().Name()
    curr2 = confirmation.Trade().Instrument().StrikeCurrency().Name()
    return "%s/%s" % (curr1, curr2)


def get_trigger_level(confirmation):
    return get_barrier_level(confirmation)

def get_option_style_code(confirmation):
    instrument = confirmation.Trade().Instrument()
    pay_type = instrument.PayType()
    exotic = instrument.Exotic()
    average_price_type = exotic.AveragePriceType()
    average_strike_type = exotic.AverageStrikeType()
    if pay_type == 'Spot' and average_price_type == 'Average' and average_strike_type == 'Fix':
        return 'AVRO'
    elif pay_type == 'Spot' and average_price_type == 'Float' and average_strike_type == 'Average':
        return 'AVSO'
    elif pay_type == 'Spot' and average_price_type == 'Average' and average_strike_type == 'Average':
        return 'DAVO'
    elif 'KIKO' in exotic.BarrierOptionType():
        return 'VANI'
    elif not instrument.Digital() and exotic.BarrierOptionType() in ('Double Out', 'Down & Out', 'Up & Out'):
        return 'NOTO'
    elif not instrument.Digital() and exotic.BarrierOptionType() in ['Double In', 'Down & In', 'Up & In']:
        return 'BINA'
    elif instrument.Digital():
        return 'DIGI'
    else:
        return 'VANI'

def get_contract_no_of_partyA(confirmation):
    event_type = confirmation.EventType()
    if event_type in [EventType.NEW_TRADE, EventType.NEW_TRADE_CANCELLATION]:
        return confirmation.Trade().Oid()
    elif event_type in [EventType.NEW_TRADE_AMENDMENT, EventType.NEW_TRADE_DUPLICATE]:
        return confirmation.Trade().ContractTrdnbr()

def get_option_expiration_style(confirmation):
    expiration_codes = {ExerciseType.AMERICAN: 'AMER', ExerciseType.EUROPEAN: 'EURO'}
    exercise_type = confirmation.Trade().Instrument().ExerciseType()
    return expiration_codes.get(exercise_type, '')

def get_barrier_indicator(confirmation):
    if confirmation.Trade().Instrument().Barrier() > 0:
        return 'Y'
    else:
        return 'N'

def get_non_deliverable_indicator(confirmation):
    if confirmation.Trade().Instrument().SettlementType() == SettleType.PHYSICAL_DELIVERY:
        return 'N'
    else:
        return 'Y'

def get_type_of_event(confirmation):
    event_type = confirmation.EventType()
    if event_type == EventType.NEW_TRADE:
        return 'CONF'
    else:
        return 'OTHR'

def get_type_of_agreement(confirmation):
    document_type = ''
    document_codes = ['AFB', 'DERV', 'FBF', 'FEOMA', 'ICOM', 'IFEMA', 'ISDA']
    trade = confirmation.Trade()

    if trade.DocumentType():
        if trade.DocumentType().Name() in document_codes:
            document_type = trade.DocumentType().Name()

    return document_type

def get_date_of_agreement(confirmation):
    date = ''
    trade = confirmation.Trade()

    if trade.DocumentType():
        trade_document_type = trade.DocumentType().Name()
        cp = confirmation.Counterparty()
        agreements = cp.Agreements()
        agreement_start_dates = []

        for agreement in agreements:
            if agreement.DocumentTypeChlItem().Name() == trade_document_type:
                agreement_start_dates.append(agreement.Dated())

        if agreement_start_dates:
            date = max(agreement_start_dates)

    return date

def get_version_of_agreement(confirmation):
    date = get_date_of_agreement(confirmation)
    year = date.split('-')[0]
    return year

def get_buy_sell_indicator(confirmation):
    if confirmation.Trade().Quantity() >= 0:
        return 'B'
    else:
        return 'S'

def get_option_final_settlement_date(confirmation):
    settlement_date = ''
    expiry_date = confirmation.Trade().Instrument().ExpiryDateOnly()
    if expiry_date:
        offset = confirmation.Trade().Instrument().PayDayOffset()
        settlement_date = ael.date(expiry_date).add_days(offset).to_string("%Y-%m-%d")

    return settlement_date

def get_calculation_agent_bic(confirmation):
    bic = 'UKWN'
    calc_agent = confirmation.Trade().Calcagent()
    if calc_agent == 'CP':
        cp = confirmation.Counterparty()
        if cp:
            bic = confirmation.CounterpartyAddress()
    elif calc_agent == 'We':
        acq = confirmation.Acquirer()
        if acq:
            bic = confirmation.AcquirerAddress()
    elif calc_agent != 'Both':
        bic = 'UKWN'
    return bic

def get_calculation_agent_account(confirmation):
    return ''

def get_calculation_agent_name(confirmation):
    name = ''
    calc_agent = confirmation.Trade().Calcagent()
    if calc_agent == 'CP':
        cp = confirmation.Counterparty()
        if cp:
            name = cp.Name()
    elif calc_agent == 'We':
        acq = confirmation.Acquirer()
        if acq:
            name = acq.Name()
    elif calc_agent == 'Both':
        name = 'JOINT'
    return name

def get_calculation_agent_address(confirmation):
    address = ''
    calc_agent = confirmation.Trade().Calcagent()
    if calc_agent == 'CP':
        cp = confirmation.Counterparty()
        if cp:
            address = get_party_address(cp)
    elif calc_agent == 'We':
        acq = confirmation.Acquirer()
        if acq:
            address = get_party_address(acq)
    return address

def get_calculation_agent_location(confirmation):
    name = get_calculation_agent_name(confirmation)
    city = acm.FParty[name].City()
    return get_location_code(city)


def get_receiving_agent_bic_for_sett_instr_for_premium_payment(confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    bic = ''
    if money_flow:
        if confirmation.Trade().Premium() < 0:
            if money_flow.AcquirerAccount():
                if money_flow.AcquirerAccount().Bic():
                    bic = money_flow.AcquirerAccount().Bic().Alias()
        else:
            if money_flow.CounterpartyAccount():
                if money_flow.CounterpartyAccount().Bic():
                    bic = money_flow.CounterpartyAccount().Bic().Alias()
    return bic

def get_receiving_agent_account_for_sett_instr_for_premium_payment(confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    account = ''
    if money_flow:
        if confirmation.Trade().Premium() < 0:
            if money_flow.AcquirerAccount():
                account = money_flow.AcquirerAccount().Account()
        else:
            if money_flow.CounterpartyAccount():
                account = money_flow.CounterpartyAccount().Account()
    return account

def get_receiving_agent_name_for_sett_instr_for_premium_payment(confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    name = ''
    if money_flow:
        if confirmation.Trade().Premium() < 0:
            if money_flow.AcquirerAccount():
                corrBank = money_flow.AcquirerAccount().CorrespondentBank()
                if corrBank:
                    name = get_party_full_name(corrBank)

        else:
            if money_flow.CounterpartyAccount():
                corrBank = money_flow.CounterpartyAccount().CorrespondentBank()
                if corrBank:
                    name = get_party_full_name(corrBank)
    return name

def get_receiving_agent_address_for_sett_instr_for_premium_payment(confirmation):
    money_flow = FMTConfirmationWrapper(confirmation).money_flow()
    address = ''
    if money_flow:
        if confirmation.Trade().Premium() < 0:
            if money_flow.AcquirerAccount():
                corrBank = money_flow.AcquirerAccount().CorrespondentBank()
                if corrBank:
                    address = get_party_address(corrBank)
        else:
            if money_flow.CounterpartyAccount():
                corrBank = money_flow.CounterpartyAccount().CorrespondentBank()
                if corrBank:
                    address = get_party_address(corrBank)
    return address

def get_payout_receiving_agent_bic(confirmation):
    return 'UKWN'

def get_payout_receiving_agent_name(confirmation):
    return 'UNKNOWN'

def get_type_of_barrier(confirmation):
    type_code = ''
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        barrier_type = excotic.BarrierOptionType()
        if barrier_type == BarrierOptionType.DOUBLE_IN:
            type_code = 'DKIN'
        elif barrier_type == BarrierOptionType.DOUBLE_OUT:
            type_code = 'DKOT'
        elif barrier_type in (BarrierOptionType.DOWN_AND_IN, BarrierOptionType.UP_AND_IN):
            type_code = 'SKIN'
        elif barrier_type in (BarrierOptionType.DOWN_AND_OUT, BarrierOptionType.UP_AND_OUT):
            type_code = 'SKOT'
        elif barrier_type in ['KIKO Up In Down Out', 'KIKO Down In Up Out']:
            type_code = 'KIKO'
        elif barrier_type in ['KIKO Up Out Down In', 'KIKO Down Out Up In']:
            type_code = 'KOKI'
    return type_code

def get_barrier_level(confirmation):
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        return excotic.DoubleBarrier()
    else:
        return confirmation.Trade().Instrument().Barrier()

def get_lower_barrier_level(confirmation):
    barrier = 0
    doubleBarrier = 0

    barrier = confirmation.Trade().Instrument().Barrier()
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        doubleBarrier = excotic.DoubleBarrier()

    return min(barrier, doubleBarrier)

def get_type_of_trigger(confirmation):
    if confirmation.Trade().Instrument().Barrier():
        return 'SITR'
    excotic = confirmation.Trade().Instrument().Exotic()
    if excotic:
        if excotic.DoubleBarrier():
            return 'DBTR'
    return ''

def get_trigger_blocks(confirmation):
    blocks = []
    each_block = {}
    each_block['TYPE_OF_TRIGGER'] = get_type_of_trigger(confirmation)
    each_block['TRIGGER_LEVEL'] = get_trigger_level(confirmation)
    each_block['LOWER_TRIGGER_LEVEL'] = get_lower_barrier_level(confirmation)
    each_block['CURRENCY_PAIR'] = get_currency_pair(confirmation)
    blocks.append(each_block)
    return blocks

def get_sequence_h_settlement_rate_source(confirmation):
    source_list = []
    source = ''
    if confirmation.Trade().Instrument().SettlementType() == SettleType.CASH:
        fixing_source = confirmation.Trade().Instrument().FixingSource()
        if fixing_source:
            source = fixing_source.Name()
            source_list.append(source)
    return source_list

def get_your_reference(confirmation):
    ''' Mandatory field 21 '''

    ref = ''
    refConf = None
    swiftwriter_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
    FAC = getattr(swiftwriter_config, 'FAC', 'None')
    if confirmation.Type() in (ConfirmationType.AMENDMENT, ConfirmationType.CANCELLATION):
        refConf = confirmation.ConfirmationReference()
    elif confirmation.Type() in (ConfirmationType.CHASER):
        refConf = confirmation.ChasingConfirmation()

    if refConf and get_confirmation_reference_prefix():
        ref = get_confirmation_reference_prefix() + '-' + str(refConf.Oid())

def get_queries(confirmation):
    '''A mandatory field 75 '''

    query = ''
    start_tag = '<MT395_ChaserComment>'
    end_tag = '</MT395_ChaserComment>'
    if confirmation.Type() == ConfirmationType.CHASER:
        diary = confirmation.Diary()
        if diary:
            diary_text = diary.Text()
            if diary_text.find(start_tag) > 0:
                startPos = diary_text.find(start_tag) + len(start_tag)
                endPos = diary_text.find(end_tag)
                query = diary_text[startPos:endPos]

    #removing carriage return character
    return query.replace('\r', '\n')


def get_narrative():
    ''' Optional field 77A'''
    return ''

def get_original_message_mt(confirmation):
    ''' Mandatory field 11S '''
    mt = ''
    if confirmation.Type() == ConfirmationType.CHASER:
        relatedConfirmation = confirmation.ChasingConfirmation()
        operationDocuments = relatedConfirmation.Documents()
        if operationDocuments:
            operationDocument = operationDocuments[0]
            mt = str(operationDocument.SwiftMessageType())

    return mt

def get_barrier_windows(confirmation):
    barriers = acm.FArray()
    barrier_windows = []

    exotic = confirmation.Trade().Instrument().Exotic()
    if exotic and exotic.BarrierMonitoring() in [BarrierMonitoring.WINDOW, BarrierMonitoring.DISCRETE]:
        exotic_events = confirmation.Trade().Instrument().ExoticEvents().SortByProperty("Date")
        for exotic_event in exotic_events:
            if exotic_event.Type() == ExoticEventType.BARRIER_DATE:
                barriers.Add(exotic_event)
    else:
        #Create dummy barrier event for default values
        exotic_event = acm.FExoticEvent()
        trade_date = acm.Time.AsDate(confirmation.Trade().TradeTime())
        exotic_event.Date(trade_date)    #change to trade day
        exotic_event.EndDate(confirmation.Trade().Instrument().ExpiryDateOnly())
        barriers.Add(exotic_event)

    is_discrete_monitoring = False
    exotic = confirmation.Trade().Instrument().Exotic()
    if exotic and exotic.BarrierMonitoring() == BarrierMonitoring.DISCRETE:
        is_discrete_monitoring = True
    for each_event in barriers:
        barrier_details = {}
        barrier_details['BARRIER_WIN_START_DATE'] = each_event.Date()
        if is_discrete_monitoring:
            barrier_details['BARRIER_WIN_END_DATE'] = confirmation.Trade().Instrument().ExpiryDateOnly()
        else:
            barrier_details['BARRIER_WIN_END_DATE'] = each_event.EndDate()
        barrier_details['START_DATE_LOCATION'] = get_option_expiry_location(confirmation)
        barrier_details['END_DATE_LOCATION'] = get_option_expiry_location(confirmation)
        barrier_details['START_DATE_TIME'] = '0000'
        barrier_details['END_DATE_TIME'] = '0000'
        barrier_windows.append(barrier_details)

    return barrier_windows

#------------MT320----------------------

def get_party_A_role(confirmation):
    if confirmation.Trade().Premium() < 0:
        return 'L'
    else:
        return 'B'

def get_party_info(option, account, bic, name, address):
    if option == 'J':
        return ('J', '', 'UKWN', '', '')

    conditionForOptionA = (option == 'A' and not bic)
    conditionForOptionD = (option == 'D' and (not name or not address))
    if conditionForOptionA or conditionForOptionD:
        return ('', '', '', '', '')

    return (option, account, bic, name, address)


def get_SIA_party_intermediary_partyInfo(confirmation, party, option=''):
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.money_flow()

    account = bic = name = address = ''
    if not money_flow:
        option = ''

    corrBank = None
    if money_flow:
        if party == 'A' and money_flow.CounterpartyAccount():
            account = money_flow.CounterpartyAccount().Account2()
            if money_flow.CounterpartyAccount().Bic2():
                bic = money_flow.CounterpartyAccount().Bic2().Name()
            corrBank = money_flow.CounterpartyAccount().CorrespondentBank2()
        elif party == 'B' and money_flow.AcquirerAccount():
            account = money_flow.AcquirerAccount().Account2()
            if money_flow.AcquirerAccount().Bic2():
                bic = money_flow.AcquirerAccount().Bic2().Name()
            corrBank = money_flow.AcquirerAccount().CorrespondentBank2()

        if corrBank:
            name = FSwiftMLUtils.get_party_full_name(corrBank)
            address = FSwiftMLUtils.get_party_address(corrBank)

    return get_party_info(option, account, bic, name, address)

def get_SIA_party_intermediary_option(confirmation, party, option):
    return get_SIA_party_intermediary_partyInfo(confirmation, party, option)[0]

def get_SIA_party_intermediary_account(confirmation, party):
    return get_SIA_party_intermediary_partyInfo(confirmation, party)[1]

def get_SIA_party_intermediary_bic(confirmation, party):
    return get_SIA_party_intermediary_partyInfo(confirmation, party)[2]

def get_SIA_party_intermediary_name(confirmation, party):
    return get_SIA_party_intermediary_partyInfo(confirmation, party)[3]

def get_SIA_party_intermediary_address(confirmation, party):
    return get_SIA_party_intermediary_partyInfo(confirmation, party)[4]

def get_SIA_party_delivery_agent_partyInfo(confirmation, party, option=''):
    conf_wrapper_obj = FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.money_flow()

    account = bic = name = address = ''
    corrBank = None
    if not money_flow:
        option = ''

    if money_flow:

        if party == 'B' and money_flow.CounterpartyAccount():
            account = money_flow.CounterpartyAccount().Account()
            if money_flow.CounterpartyAccount().Bic():
                bic = money_flow.CounterpartyAccount().Bic().Name()
            corrBank = money_flow.CounterpartyAccount().CorrespondentBank()
        elif party == 'A' and money_flow.AcquirerAccount():
            account = money_flow.AcquirerAccount().Account()
            if money_flow.AcquirerAccount().Bic():
                bic = money_flow.AcquirerAccount().Bic().Name()
            corrBank = money_flow.AcquirerAccount().CorrespondentBank()

        if corrBank:
            name = FSwiftMLUtils.get_party_full_name(corrBank)
            address = FSwiftMLUtils.get_party_address(corrBank)

    return get_party_info(option, account, bic, name, address)

def get_SIA_party_delivery_agent_option(confirmation, party, option):
    return get_SIA_party_delivery_agent_partyInfo(confirmation, party, option)[0]

def get_SIA_party_delivery_agent_account(confirmation, party):
    return get_SIA_party_delivery_agent_partyInfo(confirmation, party)[1]

def get_SIA_party_delivery_agent_bic(confirmation, party):
    return get_SIA_party_delivery_agent_partyInfo(confirmation, party)[2]

def get_SIA_party_delivery_agent_name(confirmation, party):
    return get_SIA_party_delivery_agent_partyInfo(confirmation, party)[3]

def get_SIA_party_delivery_agent_address(confirmation, party):
    return get_SIA_party_delivery_agent_partyInfo(confirmation, party)[4]


def get_settle_amount_MT320(confirmation):
    """
    This function calculates the settlement amount for the
    confirmation.
    :param confirmation:
    :return: settlement amount
    """
    settle_amount = ''
    calc_space = FSwiftMLUtils.get_calculation_space()
    event_type = FSwiftConfirmationUtils.get_event_type(confirmation)
    if event_type == 'ROLL':
        originalTrade = acm.FTrade[confirmation.Trade().ContractTrdnbr()]
        if originalTrade:
            totalAmount = 0
            prolongingAmount = 0
            for moneyFlow in originalTrade.MoneyFlows():
                if moneyFlow.Type() == 'Fixed Amount':
                    number = moneyFlow.Calculation().Projected(calc_space).Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(number):
                        number = 0
                    totalAmount += number
            for moneyFlow in confirmation.Trade().MoneyFlows():
                if moneyFlow.Type() == 'Fixed Amount':
                    number = moneyFlow.Calculation().Projected(calc_space).Value().Number()
                    if acm.Operations.IsValueInfNanOrQNan(number):
                        number = 0
                    prolongingAmount += number

            curr = confirmation.Trade().Currency()
            amountDiff = prolongingAmount - totalAmount
            settle_amount = apply_currency_precision(curr, amountDiff)
    elif event_type == 'MATU':
        trade_obj = confirmation.Trade()
        if trade_obj:
            settle_amount = trade_obj.EndCash()

    return settle_amount

def get_settle_currency_MT320(confirmation):
    if FSwiftConfirmationUtils.get_event_type(confirmation) in ['ROLL', 'MATU']:
        assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
        return confirmation.Trade().Currency().Name()
    return ''


def get_interest_rate(confirmation):
    '''
    Get the interest rate for the deposit loan, Fix interest rate or (float + spread)
    :param Confirmation: Confirmation acm object for the trade.
    :return: (Float): interest_rate
    '''
    interest_rate = 0.0
    leg_type = get_instrument_leg_type(confirmation)
    if leg_type == LegType.FLOAT:
        reset = get_reset_from_cashflow(confirmation, CashFlowType.FLOAT_RATE)
        if reset:
            float_rate = reset.FixingValue()
            if float_rate:
                cf = get_cash_flow(confirmation, CashFlowType.FLOAT_RATE)
                spread_rate = cf.Spread()
                interest_rate = float(float_rate) + float(spread_rate)
    else:
        cash_flow = get_cash_flow(confirmation, CashFlowType.FIXED_RATE)
        if cash_flow:
            interest_rate = cash_flow.FixedRate()
    if acm.Operations.IsValueInfNanOrQNan(interest_rate):
        interest_rate = 0.0

    return interest_rate

def get_interest_amount(confirmation):
    '''
    Get interest amount with the interest rate.
    :param confirmation:
    :return: (Float) interest amount
    '''

    interest_amount = 0.0
    leg_type = get_instrument_leg_type(confirmation)
    cash_flow = None
    if leg_type == LegType.FLOAT:
        cash_flow = get_cash_flow(confirmation, CashFlowType.FLOAT_RATE)
    else:
        cash_flow = get_cash_flow(confirmation, CashFlowType.FIXED_RATE)
    if cash_flow:
        calc_space = FSwiftMLUtils.get_calculation_space()
        calculated_value = cash_flow.Calculation().Projected(calc_space, confirmation.Trade())
        assert confirmation.Trade().Currency(), "The trade referenced by the confirmation has no currency"
        if calculated_value:
            value = calculated_value.Value().Number()
            if not acm.Operations.IsValueInfNanOrQNan(value):
                interest_amount = value * -1
                interest_amount = apply_currency_precision(confirmation.Trade().Currency().Name(),
                                                                                float(interest_amount))
    return interest_amount

def get_cash_flow_type(confirmation):
    '''
    Get the cash from type from the confirmation
    :param confirmation:
    :return:
    '''
    pass

def get_reset_from_cashflow(confirmation, cash_flow_type):
    '''
    Get the reset for the Confirmation from the cash flow
    :param confirmation: Confirmation acm object for the trade.
    :return reset(acm Reset object): reset for the cash flow of the Confirmation.
    '''
    reset = None
    cash_flow = get_cash_flow(confirmation, cash_flow_type)
    if cash_flow:
        reset = cash_flow.Resets()[0]
    return reset

def get_instrument_leg_type(confirmation):
    '''
    Check the leg type of the instrument.
    :param confirmation:
    :return: (str) : type of leg
    '''
    assert confirmation.Trade().Instrument().Legs(), "The instrument referenced by the trade referenced by the " \
                                                     "confirmation has no legs"
    leg = confirmation.Trade().Instrument().Legs().First()
    return  leg.LegType()

def get_cash_flow(confirmation, cash_flow_type=None):
    '''
    Get cash flow for the confirmations with given type
    :param confirmation:
    :param cash_flow_type:
    :return:
    '''
    leg = confirmation.Trade().Instrument().Legs().First()
    selection = acm.FCashFlow.Select('leg = %d and cashFlowType = "%s"' % (leg.Oid(), cash_flow_type))
    if (selection.Size() > 0):
        return selection.SortByProperty('StartDate').First()
    return None

def get_event_change_item(confirmation):
    '''
    The event causing creation of given confirmation
    :param confirmation: FCondirmation object
    :return: (str) event_name: events sucj as New Trade, Rate fixing....
    '''
    event_name = ''
    if confirmation:
        event_name = confirmation.EventChlItem().Name()
    return event_name

'''
class LegType:
    FLOAT                           = 'Float'
    CALL_FIXED                      = 'Call Fixed'
    CALL_FLOAT                      = 'Call Float'
    CALL_FIXED_ADJUSTABLE           = 'Call Fixed Adjustable'

class CashFlowType:
    FIXED_AMOUNT                    = 'Fixed Amount'
    FIXED_RATE                      = 'Fixed Rate'
    FLOAT_RATE                      = 'Float Rate'
'''
#--------------------MT330 helper methods----------------------

def get_party_A_role_MT330(confirmation):
    if confirmation.Trade().Quantity() < 0:
        return 'L'
    else:
        return 'B'

def get_event_type_MT330(confirmation):
    eventType = 'CONF'

    return eventType

def get_projected_cash_flow(cashFlow, trade):
    value = ''
    calc_space = FSwiftMLUtils.get_calculation_space()
    calcValue = cashFlow.Calculation().Projected(calc_space, trade)
    if type(calcValue) == int:
        value = float(calcValue)
    else:
        value = calcValue.Value().Number()
        if acm.Operations.IsValueInfNanOrQNan(value):
            value = 0
    return value

def get_balance_amount(confirmation):
    ''' This together with balance_currency forms the mandatory field 32B in seq B '''

    legs = confirmation.Trade().Instrument().Legs()
    for aLeg in legs:
        cashFlows = aLeg.CashFlows()
        for aCashFlow in cashFlows:
            if FSwiftMLUtils.get_acm_version() >= 2016.4:
                cash_flow_type = CashFlowType.REDEMPTION_AMOUNT
            else:
                cash_flow_type = 'Redemption Amount'

            if aCashFlow.CashFlowType() == cash_flow_type:
                value = get_projected_cash_flow(aCashFlow, confirmation.Trade())
                return apply_currency_precision(aLeg.Currency().Name(), abs(value))
    return ''

def get_balance_currency(confirmation):
    curr = ''
    legs = confirmation.Trade().Instrument().Legs()
    if legs:
        curr = legs[0].Currency().Name()
    return curr


def get_cash_flow_MT330(confirmation):
    legTocfTypeMappings = { LegType.CALL_FIXED : CashFlowType.CALL_FIXED_RATE,
                    LegType.CALL_FIXED_ADJUSTABLE : CashFlowType.CALL_FIXED_RATE_ADJUSTABLE,
                    LegType.CALL_FLOAT : CashFlowType.CALL_FLOAT_RATE
                     }

    cashflows = {}
    legs = confirmation.Trade().Instrument().Legs()
    for aLeg in legs:
        cfType = legTocfTypeMappings.get(aLeg.LegType(), '')
        if cfType:
            for aCashFlow in aLeg.CashFlows():
                if aCashFlow.CashFlowType() == cfType:
                    cashflows[aCashFlow.StartDate()] = aCashFlow

    cfStartdates = list(cashflows.keys())
    cfStartdates.sort()

    dateToday = acm.Time.DateToday()
    for startDate in cfStartdates:
        endDate = cashflows[startDate].EndDate()
        if startDate <= dateToday <= endDate or startDate > dateToday:
            return cashflows[startDate]

    return ''


def get_interest_rate_MT330(confirmation):
    ''' Mandatory field 37G in seq B '''

    if confirmation.Reset():
        return str(confirmation.Reset().FixingValue())

    interestRate = ''
    cashFlow = get_cash_flow_MT330(confirmation)
    if cashFlow:
        interestRate = cashFlow.FixedRate()
        if not interestRate:
            for aReset in cashFlow.Resets():
                if aReset.FixingValue():
                    interestRate = aReset.FixingValue()
                    break
    return str(interestRate)

def get_period_notice(confirmation):
    unit_map = dict(Days=1, Weeks=7, Months=30, Years=365)
    unit = confirmation.Trade().Instrument().NoticePeriodUnit()
    days = confirmation.Trade().Instrument().NoticePeriodCount() * unit_map[unit]
    if days > 999:
        days = 999
    return '%03d' % days


def get_swift_msg_from_external_object(confirmation, msg_type):
    '''
    Get swift message given msg_type related to given confrimation.
    :param confirmation: FConfirmation object to get the swift meassage
    :param msg_type: Type of MT message to get from the confirmation
    :return: (str) swift_msg: swift message in string format
    '''
    swift_msg = ''
    ext_object = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=confirmation, msg_typ=msg_type, integration_type="Outgoing")

    if ext_object:
        swift_msg = FSwiftMLUtils.FSwiftExternalObject.get_stored_data(ext_object, 'swift_data')
    return swift_msg

def check_for_chng_event_type(confirmation, swift_metadata_xml_dom):
    '''
    Given the confirmation, get the relate confirmation for this AMND confirmation. Check if the field 38A or 32B in
    the swift message from confirmation differ from the NoticePeriodCount or the deposit amount fields on the trade
    instrument.
    :param confirmation: AMND confirmation's FConfirmation object
    :return: (bool) is_chng_event: True, if value differs else, False.
    '''
    related_confirmation = confirmation.ConfirmationReference()
    is_chng_event = False
    if related_confirmation:
        swift_msg_str = get_swift_msg_from_external_object(related_confirmation, "MT330")
        swift_lib = FSwiftML.FSwiftML()
        swift_msg = swift_lib.swift_to_pyobject(swift_msg_str)

        if swift_metadata_xml_dom:
            period_notice = FSwiftWriterUtils.get_value_from_xml_tag(swift_metadata_xml_dom,
                                                     ['SWIFT', 'PERIOD_NOTICE'])
            balance_amount = FSwiftWriterUtils.get_value_from_xml_tag(swift_metadata_xml_dom,
                                                          ['SWIFT', 'BALANCE_AMOUNT'], ignore_absense=True)
        else:
            period_notice = get_period_notice(confirmation)
            balance_amount = get_balance_amount(confirmation)

        if int(swift_msg.SequenceB_TransactionDetails.PeriodOfNotice.value()) != int(period_notice):
            is_chng_event = True
        elif balance_amount and (float(swift_msg.SequenceB_TransactionDetails.CurrencyAndBalance.value()[3:].replace(',', '.')) != float(balance_amount)):
            is_chng_event = True

        change_event_in_past_confirmation = False
        if swift_msg.SequenceA_GeneralInformation.TypeOfEvent.value() == "CHNG":
            change_event_in_past_confirmation = True

        if not change_event_in_past_confirmation:
            all_confirmations = confirmation.Trade().Confirmations()
            # last in the list is current confirmation and previous to it is already checked, so [:-2]
            for conf in all_confirmations[:-2]:
                swift_msg_str = get_swift_msg_from_external_object(conf, "MT330")
                swift_lib = FSwiftML.FSwiftML()
                swift_msg = swift_lib.swift_to_pyobject(swift_msg_str)
                if swift_msg.SequenceA_GeneralInformation.TypeOfEvent.value() == "CHNG":
                    change_event_in_past_confirmation = True
                    break

        info = dict(is_change_event_amnd=change_event_in_past_confirmation, last_amount=swift_msg.SequenceB_TransactionDetails.CurrencyAndBalance.value())

    return is_chng_event, info


def get_total_fixed_amount_from_cashflow(confirmation):
    calc_space = FSwiftMLUtils.get_calculation_space()
    originalTrade = acm.FTrade[confirmation.Trade().ContractTrdnbr()]
    if originalTrade:
        total_amount = 0
        for moneyFlow in originalTrade.MoneyFlows():
            if moneyFlow.Type() == 'Fixed Amount':
                number = moneyFlow.Calculation().Projected(calc_space).Value().Number()
                if acm.Operations.IsValueInfNanOrQNan(number):
                    number = 0
                total_amount += number
        return total_amount
    return ''



