"""----------------------------------------------------------------------------
MODULE:
    FSecurityConfirmationOutUtils

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
import FRegulatoryLib
import FSecuritySettlementOutUtils

import FSwiftWriterLogger
import collections
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')

import FSwiftOperationsAPI
from FSettlementXML import FSettlementXML
import FMTConfirmationWrapper
try:
    RelationType = FSwiftOperationsAPI.GetRelationTypeEnum()
    PartialSettlementType = FSwiftOperationsAPI.GetPartialSettlementTypeEnum()
    InsType = FSwiftOperationsAPI.GetInsTypeEnum()
    SettlementType = FSwiftOperationsAPI.GetSettlementTypeEnum()
    SettlementStatus = FSwiftOperationsAPI.GetSettlementStatusEnum()
except:
    pass

writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

def decorate_all_setter(setter_method):
    ''' Class decorator method for decorating all callable attributes of class and
        returns a decorated method, decorated with setter_method , in this case '''
    def decorator(cls):
        for name, obj in list(vars(cls).items()):
            if isinstance(obj, collections.Callable):
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

def get_confiration_number_from_msg(msg):
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


def is_cancellation_confirmation(confirmation):
    isCancOperation = True if confirmation.EventChlItem().Name() == 'New Trade' and confirmation.Type() == 'Cancellation' else False
    return isCancOperation

def is_new_confirmation(confirmation):
    isNewOperation = True if confirmation.EventChlItem().Name() == 'New Trade' and confirmation.Type() == 'Default' else False
    return isNewOperation

def is_duplicate_confirmation(confirmation):
    isDuplOperation = True if confirmation.Type() == 'Chaser' else False
    return isDuplOperation

def get_function_of_message(acm_object):
    if is_cancellation_confirmation(acm_object):
        return 'CANC'
    elif is_new_confirmation(acm_object):
        return 'NEWM'

def get_related_ref(settlement):
    relatedRef = ''
    relatedSettlement = settlement.Children()[0]
    relatedSettlementMessage = FSwiftMLUtils.get_related_entity_message(relatedSettlement)
    field = '20C'
    fieldValue = FSwiftMLUtils.get_field_value(relatedSettlementMessage, field)
    start = fieldValue.find("FAS-")
    relatedRef = fieldValue[start:]

def get_linkage_qualifier(confirmation):
    if is_cancellation_confirmation(confirmation):
        return 'PREV'
    else:
        return ''

def get_linkage_reference(confirmation):
    if is_cancellation_confirmation(confirmation):
        return get_related_ref(confirmation)
    else:
        return ''

def get_confirmation_datetime_qualifier():
    return 'SETT'

def get_confirmation_datetime_date(confirmation):
    return confirmation.Trade().ValueDay()

def get_trade_datetime_qualifier():
    return 'TRAD'

def get_transaction_type():
    return 'TRAD'

def get_trade_datetime_date(confirmation):
    return confirmation.Trade().TradeTime()

def get_instrument(confirmation):
    trade = confirmation.Trade()
    if trade:
        return trade.Instrument()

def get_instrument_ISIN(confirmation):
    ''' Mandatory field 35B in seq B '''
    isin = ''
    instrument = get_instrument(confirmation)
    if instrument.Isin() == "" and instrument.Underlying():
        isin = instrument.Underlying().Isin()
    else:
        isin = instrument.Isin()
    if isin:
        isin = 'ISIN ' + isin
    return isin

def get_description_of_security(confirmation):
    description = ''
    instrument = get_instrument(confirmation)
    if instrument:
        productType = instrument.ProductTypeChlItem()
        if productType:
            description =  productType.Name()
    return description

def get_quantity_type_code():
    return 'FAMT'

def get_quantity(confirmation):
    return abs(confirmation.Trade().Quantity())

def get_account_qualifier():
    return 'SAFE'

def get_qualifier(pair):
    return pair.First()

def get_indicator(pair):
    return pair.Second()

def get_indicators(acm_object):
    indicatorsList = acm.FList()
    trade = acm_object.Trade()
    qualifers = get_mandatory_indicator()
    for each_qualifer in qualifers:
        pair = acm.FPair()
        first = acm.FSymbol(each_qualifer)
        second = acm.FSymbol(get_qualifer_code(each_qualifer, acm_object))
        pair.First(first)
        pair.Second(second)
        indicatorsList.Add(pair)

    return indicatorsList

def get_qualifer_code(qualifer, confirmation):
    trade = confirmation.Trade()
    settlement = trade.Settlements()[0] if trade.Settlements() else []
    code = ''
    if qualifer == 'BUSE':
        code = 'BUYI' if confirmation.Trade().Nominal() >= 0 else 'SELL'
    elif qualifer == 'PAYM' and settlement:
        if settlement.Type() == 'Security Nominal' and  settlement.DeliveryType() == 'Delivery versus Payment':
            code = 'APMT'
        elif settlement.Type() == 'Security Nominal' and settlement.DeliveryType() == 'Delivery Free of Payment':
            code = 'FREE'
    return code

def get_mandatory_indicator():
    return ['BUSE', 'PAYM']

def get_party_option(dummyPartyDetails, settlement):
    if dummyPartyDetails.At('qualifier') in ['BUYR', 'SELL']:
        return 'P'
    elif dummyPartyDetails.At('datasourcescheme') != '':
        return 'R'
    else:
        return FSwiftWriterUtils.get_option_value('Party_95a', settlement)

def get_party_bic(account):
    if account.NetworkAlias():
        return account.NetworkAlias().Alias()
    else:
        assert account.Party(), "The account has no party reference"
        return account.Party().Swift()

def get_instrument_quotation(confirmation):
    try:
        quotation = confirmation.Trade().Instrument().Quotation().Name()
    except:
        quotation = ''
    return quotation

def get_trade_price(confirmation):
    return confirmation.Trade().Price()

def get_nominal(confirmation):
    return abs(confirmation.Trade().Nominal())

def get_acquirer_party_details(confirmation):
    party_info = {}
    nominal = get_nominal(confirmation)
    qualifer = 'BUYR' if nominal > 0 else 'SELL'
    conf_wrapper_obj = FMTConfirmationWrapper.FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.money_flow()
    if money_flow:
        acquirer = money_flow.Acquirer()
        acquirer_account = money_flow.AcquirerAccount()
        bic = get_party_bic(acquirer_account)
        party_info = FSecuritySettlementOutUtils.get_party_info(qualifer, bic, acquirer, acquirer_account, '', '')
    return party_info

def get_counter_party_details(confirmation):
    party_info = {}
    nominal = get_nominal(confirmation)
    qualifer  = 'SELL' if nominal > 0 else 'BUYR'
    conf_wrapper_obj = FMTConfirmationWrapper.FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.money_flow()
    if money_flow:
        counterparty = money_flow.Counterparty()
        counterparty_account = money_flow.CounterpartyAccount()
        bic = get_party_bic(counterparty_account)
        party_info = FSecuritySettlementOutUtils.get_party_info(qualifer, bic, counterparty, counterparty_account, '', '')
    return party_info

def get_senders_bic(confirmation):
    '''Returns SWIFT bic code of the Acquirer of the confirmation.
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
    return confirmation.AcquirerAddress()

def get_receivers_bic(confirmation):
    '''Returns SWIFT bic code of confirmation receiver.
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
    return confirmation.CounterpartyAddress()

def get_accrued_interest(confimration):
    """ Get accrued interest from the settlement """
    interest = 0.0
    try:
        if confimration.Trade():
            interest = confimration.Trade().Calculation().AccruedInterestSpotOverrideSource(
                FSwiftMLUtils.get_calculation_space(),
                acm.Time().SmallDate(),
                confimration.Trade().ValueDay(), 2).Value().Number()
    except Exception as e:
        notifier.INFO("Unable to get accrued interest from the trade")
    return interest

def get_amount_qualifier():
    """ Mandatory field 19A in sub seq E3 """
    return 'SETT'

def _premium_amount(confirmation):
    return confirmation.Trade().Premium()

def calculate_payments(confirmation):
    amount = 0.0
    premium_amount = _premium_amount(confirmation)
    curr = confirmation.Trade().Currency().Name()
    for each_payment in confirmation.Trade().Payments():
        if curr == each_payment.Currency().Name():
            amount += each_payment.Amount()
    amount = amount + premium_amount
    return apply_currency_precision(curr, amount)

def calculate_cash_amount(confirmation):
    amount = 0
    amount = _premium_amount(confirmation)
    curr = confirmation.Trade().Currency().Name()
    return apply_currency_precision(curr, amount)

def get_amount_sign(confirmation):
    if calculate_cash_amount(confirmation) <= 0:
        return ''
    else:
        return 'N'

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

def get_currency_code(confirmation):
    assert confirmation.Trade().Currency(), "Confirmation has no cash currency"
    return confirmation.Trade().Currency().Name()

def get_amount_for_payment_type(confirmation, payment_type):
    """ Get amount for the payment type """
    amount = confirmation.Trade().Premium()
    return amount

def get_setttlement_amount(confirmation):
    return calculate_payments(confirmation)

def get_amount_for_qualifier(confirmation, qualifier, mt_type):
    """ get amount for the qualifier, field 19A
    :param confirmation: FConfirmation object
    :param qualifier: name of the qualifier to get the amount
    :param mt_type: MT type of the meesage to be generated
    :return:
    """
    amount = 0.0
    is_accruing = confirmation.Trade().Instrument().IsAccruing()
    accurued_interest = get_accrued_interest(confirmation)
    if qualifier == 'SETT':
        amount = get_setttlement_amount(confirmation)
    elif qualifier == 'ACRU' and is_accruing:
        amount = accurued_interest
    else:
        amount = _premium_amount(confirmation)
    return amount

def get_amount(confirmation):
    return abs(calculate_cash_amount(confirmation))

def get_amount_details(confirmation, mt_type):
    """ Get amount details from the trade lined to given confirmation

    :param confirmation: FConfirmation object
    :return: list of dict of the different qualifiers.
    """
    qualifier_list = ['SETT', 'ACRU']
    list_of_payouts = []

    for qualifier in qualifier_list:
        amount = get_amount_for_qualifier(confirmation, qualifier, mt_type)
        if amount and abs(amount) > 0.0:
            val_dict = dict()
            val_dict['AMOUNT_QUALIFIER'] = qualifier
            val_dict['AMOUNT_CURRENCY_CODE'] = get_currency_code(confirmation)
            val_dict['AMOUNT_AMOUNT'] = abs(apply_currency_precision(val_dict['AMOUNT_CURRENCY_CODE'], amount))
            #val_dict['AMOUNT_SIGN'] = get_sign_from_amount(amount, mt_type)
            list_of_payouts.append(val_dict)
    return list_of_payouts

def get_deal_price_details(confirmation, option):
    #return ':DEAL//PRCT/101,20'
    price_details = dict()
    qualifer = get_deal_price_qualifer(confirmation, option)
    price = deal_price(confirmation, option)
    curr = get_currency_code(confirmation)
    price_details['qualifer'] = qualifer
    price_details['deal_price'] = price
    price_details['currency'] = curr
    return price_details

def deal_price(confirmation, option):
    dealprice = None
    trade = confirmation.Trade()
    price = confirmation.Trade().Price()
    curr = get_currency_code(confirmation)
    quotation = get_instrument_quotation(confirmation)
    if option == 'A':
        if quotation in ['Yield', 'Clean', 'Pct of Nominal']:
            dealprice = price
        if trade.Instrument().InsType() in ['Bond'] and quotation in ['Pct of Nominal']:
            quot_price = FSwiftWriterUtils.quot_price(trade.Instrument(), trade, trade.ValueDay(), price)
            dealprice = quot_price
    elif option == 'B':
        accrued_interest = get_accrued_interest(confirmation)
        premium = _premium_amount(confirmation)
        quantity = get_quantity(confirmation)
        dealprice = (abs(premium) - abs(accrued_interest))/quantity
    if dealprice:
        dealprice = abs(apply_currency_precision(curr, dealprice))
        dealprice = FSwiftMLUtils.float_to_swiftmt(dealprice)
    return dealprice

def get_deal_price_qualifer(confirmation, option):
    qualifer = ''
    quotation = get_instrument_quotation(confirmation)
    if option == 'A':
        if quotation in ['Clean', 'Pct of Nominal', 'Per 1000 Clean', 'Per 1000 of Nom',
                                            'Per Contract', 'Per Unit', 'Per 100 Contracts']:
            qualifer = 'PRCT'
        elif quotation in ['Yield', 'Simple Rate']:
            qualifer = 'YIEL'
        elif quotation in ['Discount Rate', '100-rate']:
            qualifer = 'DISC'
    else:
        qualifer = 'ACTU'
    return qualifer

def get_amount_flags(confirmation, mt_type):
    """get valid flag names for field 17B
    :param confirmation: FConfirmation object
    :param mt_type: MT type of the message
    """
    flag_list = list()
    accrued_interest = get_accrued_interest(confirmation)
    if accrued_interest:
        flag_list.append({'QUALIFIER' :'ACRU', 'FLAG': 'Y'})
    return  flag_list

def get_confirmation_reference_prefix():
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

def get_acquirer_party_account_ref(confirmation):
    acquirer_account = None
    conf_wrapper_obj = FMTConfirmationWrapper.FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.money_flow()
    if money_flow:
        acquirer_account = money_flow.AcquirerAccount()
    return acquirer_account

def get_counter_party_account_ref(confirmation):
    counterparty_account = None
    conf_wrapper_obj = FMTConfirmationWrapper.FMTConfirmationWrapper(confirmation)
    money_flow = conf_wrapper_obj.money_flow()
    if money_flow:
        counterparty_account = money_flow.CounterpartyAccount()
    return counterparty_account

def get_receiving_party_details(partyAccount, details):
    FSecuritySettlementOutUtils.set_initiating_party_details('BUYR', partyAccount, details)
    FSecuritySettlementOutUtils.set_custodian_details('RECU', partyAccount, details)
    FSecuritySettlementOutUtils.set_intermediate_1_details('REI1', partyAccount, details)
    FSecuritySettlementOutUtils.set_intermediate_2_details('REI2', partyAccount, details)
    FSecuritySettlementOutUtils.set_agent_details('REAG', partyAccount, details)
    FSecuritySettlementOutUtils.set_PSET_details('PSET', partyAccount, details)

def get_delivering_party_details(partyAccount, details):
    FSecuritySettlementOutUtils.set_initiating_party_details('SELL', partyAccount, details)
    FSecuritySettlementOutUtils.set_custodian_details('DECU', partyAccount, details)
    FSecuritySettlementOutUtils.set_intermediate_1_details('DEI1', partyAccount, details)
    FSecuritySettlementOutUtils.set_intermediate_2_details('DEI2', partyAccount, details)
    FSecuritySettlementOutUtils.set_agent_details('DEAG', partyAccount, details)
    FSecuritySettlementOutUtils.set_PSET_details('PSET', partyAccount, details)

def set_party_details(partyAccount, qualifer, option = 'P'):
    details = list()
    if option and option not in ['P', 'L', 'Q', 'R', 'S']:
        notifier.ERROR("Option %s is not supported for tag %s. Mapping default option: P" % (option, 'Party_95a'))
        option = 'P'
    if qualifer == 'BUY':
        get_receiving_party_details(partyAccount, details)
    elif qualifer == 'SELL':
        get_delivering_party_details(partyAccount, details)
    applicablePartyDetails = FSecuritySettlementOutUtils.get_applicable_party_details(option, details)
    return applicablePartyDetails

def get_acquirer_party_custodian_details(confirmation, option):
    partyAccount = get_acquirer_party_account_ref(confirmation)
    nominal = get_nominal(confirmation)
    qualifer = 'BUY' if nominal > 0 else 'SELL'
    partyDetails = set_party_details(partyAccount, qualifer, option)
    return partyDetails

def get_counter_party_custodian_details(confirmation, option):
    partyAccount = get_counter_party_account_ref(confirmation)
    nominal = get_nominal(confirmation)
    qualifer = 'SELL' if nominal>0 else 'BUY'
    return set_party_details(partyAccount, qualifer, option)



