"""---------------------------------------------------------------------------------------------------------------------
HISTORY
================================================================================----------------------------------------
Date            Change no           Developer            Description
------------------------------------------------------------------------------------------------------------------------
2016-08-19      CHNG0003744247      Willie vd Bank       Demat Implementation
2016-11-24      CHNG0004119166      Willie vd Bank       Added ABCAP CRT to _DESKS_TO_CHECK_FX_CURR
2016-02-20      ABITFA-4481         Vojtech Sidorin      Add the SettlementModification hook and _set_cp_account.
2017-08-31                          Ntuthuko Matthews    Fixed an issue in SettlementModification which occured on
                                                         the back end after the FA upgrade
2017-12-11      CHNG0005220511      Willie vd Bank       DIS deployment
2019-03-22      FAOPS-659           Joash Moodley        Generate MT202's for SSA MT54x securities Funding
2020-04-21      FAOPS-700           Cuen Edwards         Improved identification of security settlements.
2020-05-28      FAOPS-683           Joash Moodley        EuroClear Custody Funding (MT210 & MT222(custom 202)).
2020-05-28      FAOPS-740           Joash Moodley        EuroClear Custody Funding (MT200).
2020-09-14      FAOPS-864           Jaysen Naicker       Enable End Cash for Euroclear Repo/Reverse and
                                                         incl BSB ins type in Funding
09-11-2020      FAOPS-931           Tawanda Mukhalela    Added Support for MT298 settlements
05-03-2021      FAOPS-1030/53       Tawanda Mukhalela    Added Support for None type settlements for Euroclear Funding
25-02-2021      FAOPS-977           Ntokozo Skosana      Added functionality to support Euroclear payments.
------------------------------------------------------------------------------------------------------------------------
"""

import sys

import acm

from at_logging import getLogger
from demat_functions import is_demat, is_dis
from SettlementConstants import ABSA_BANK, EURO_COUNTRIES

LOGGER = getLogger(__name__)

TRADE_SETTLE_CATEGORIES = [
    'SSA_BWP_ALL_Custodian',
    'SSA_GHS_ALL_Custodian',
    'SSA_KES_ALL_Custodian',
    'SSA_MUR_ALL_Custodian',
    'SSA_UGX_ALL_Custodian',
    'SSA_ZMW_ALL_Custodian'
]

DELIVERY_TYPE_MAPPING = {
    'Delivery Free of Payment': ['540', '542'],
    'Delivery versus Payment': ['541', '543']
}

_DESKS_TO_CHECK_FX_CURR = ['Gold Desk', 'AFRICA DESK', 'ABCAP CRT']


VALID_INSTRUMENT_TYPES_FOR_222 = ['Curr']
VALID_TRADE_STATUS_FOR_222 = ['BO Confirmed', 'BO-BO Confirmed']
VALID_PAYMENT_TYPE_FOR_222 = ['Cash', 'Internal Fee']
VALID_PAYMENT_CURRENCIES_FOR_222 = ['USD', 'ZAR', 'EUR', 'JPY', 'GBP']
VALID_SETTLEMENT_TYPES_FOR_222 = ['Premium', 'Internal Fee', 'Payment Cash']

def _is_security_settlement(settlement):
    """
    Determine whether or not a settlement represents a transfer of
    a security.

    Note that one would intuitively expect that calling settlement
    .IsSecurity() would be sufficient to determine this.  Unfortun-
    ately, this method appears to only check the settlement type on
    a settlement and does not work for settlements without a type -
    e.g. netted security settlements across settlement types.
    """
    if settlement.Type() != 'None':
        return settlement.IsSecurity()
    if settlement.AccountType() == 'Security':
        return True
    return False


def security_msg_type(settlement, message_type):
    """
    Check the message type for securities
    """
    if settlement.DeliveryType() in DELIVERY_TYPE_MAPPING:
        delivery_type = DELIVERY_TYPE_MAPPING[settlement.DeliveryType()]
        message_type = get_message_type_from_mapping(settlement, delivery_type)

    if is_valid_security_transfer_trade(settlement):
        delivery_type = DELIVERY_TYPE_MAPPING['Delivery Free of Payment']
        message_type = get_message_type_from_mapping(settlement, delivery_type)

    return message_type


def get_message_type_from_mapping(settlement, delivery_type):
    """
    Gets message type for settlement
    """
    if settlement.Amount() > 0:
        return delivery_type[0]
    else:
        return delivery_type[1]


def is_counterparty_bank(Settlement):
    """
    Determines whether counterparty of the settlement is a bank
    """
    try:
        bank_indicator = False
        counterparty = Settlement.Counterparty()

        if Settlement.CounterpartyAccount().__contains__('DIRECT'):
            bank_indicator = True
        elif counterparty.BusinessStatus():
            if counterparty.BusinessStatus().Name() == 'Interbank':
                bank_indicator = True

        return bank_indicator
    except:
        return False


def get_is_internal(Settlement):
    internal = False
    if not is_demat(Settlement):
        if Settlement.TheirCorrBank != '':
            if Settlement.TheirCorrBank() == ABSA_BANK:
                internal = True
    return internal


def is_demat_initial_settmnt(settlement):
    if is_demat(settlement):
        if settlement.Type() != 'Stand Alone Payment':
            return True
    return False


def is_foreign_payment(Settlement, curr):
    """
    Determines whether settlement done with foreign institution
    """
    try:
        # Country code embedded in the 4th and 5th character of BIC code
        if Settlement.TheirCorrBank():
            country = acm.FParty[Settlement.TheirCorrBank()].Swift()[4:6]
            for a in acm.FParty[Settlement.TheirCorrBank()].Aliases():
                if a.Type().Name() == 'SWIFT':
                    country = a.Name()[4:6]
        else:
            return False

        # Euro countries are aspecial case
        if country in EURO_COUNTRIES and curr == 'EUR':
            return False

        # General case
        if country != curr[:2]:
            return True

        return False
    except:
        return False


def GetMTMessage(settlement, messageType):
    """This function hook returns number of the SWIFT message type that should be
       be created for a settlement.

       Args:
         settlement -- FSettlement object.
         mtmessage -- MT message that core engine thinks should be created.

       Returns:
         None or string SWIFT message type that should be created.
    """
    messageType = ''
    if settlement.Acquirer():
        curr = settlement.Currency().Name()
        bank = is_counterparty_bank(settlement)
        cover = is_foreign_payment(settlement, curr)

        if settlement.Trade():
            trade = settlement.Trade()
        else:
            trade = None

        messageType = '103'
        if _is_security_settlement(settlement):
            messageType = security_msg_type(settlement, messageType)
        elif is_demat(settlement) or is_dis(settlement):
            if is_dis(settlement):
                messageType = '202'
                if settlement.RelationType == 'Net':
                    return messageType
            else:
                if is_demat_initial_settmnt(settlement):
                    messageType = '103'
                else:
                    if trade and _is_qualifying_mt298_settlement(settlement):
                        return '298'
                    messageType = '202'

        elif get_is_internal(settlement):
            messageType = '103'
        elif bank:
            messageType = '202'
        elif cover:
            messageType = '402'

        messageType = get_funding_settlement_message_type(settlement, messageType)

    return messageType


def ExcludeTrade(trade):
    """ Exclude FX cash trades which have a different acquirer than specified
    in the _DESKS_TO_CHECK_FX_CURR.

    FX cash = trace currency == instrument currency.
    # ABITFA-2401
    """
    if trade.Instrument().InsType() == 'Stock':
        if trade.Instrument().Currency() and trade.Instrument().Currency().Name() == 'ZAR':
            print('ZAR Stock Trade')
            if trade.Trader() and trade.Trader().Name():
                return trade.Trader() and trade.Trader().Name().upper() == 'EFGUSER'
    if trade.Instrument().InsType() != 'Curr':
        return False
    if trade.Acquirer() is None:
        return False
    fx_trade_allowed = trade.Acquirer().Name() in _DESKS_TO_CHECK_FX_CURR
    if not fx_trade_allowed:
        if trade.Currency() != trade.Instrument().Currency():
            return True
        else:
            return False

    return False


def _set_cp_account(settlement):
    """Set the CP account according to the CP_Account_Ref add info.

    The CP_Account_Ref add info is defined on cashflows and indicates
    the counterparty account that should be used for settling a given
    cashflow.
    """
    account_oid = None
    cashflow = settlement.CashFlow()
    if cashflow:
        account_oid = cashflow.AdditionalInfo().CP_Account_Ref()
    if account_oid:
        diary_note = ''
        try:
            settlement.CounterpartyAccountRef(account_oid)
            diary_note = ("SettlementModification hook: Counterparty account "
                          "set to '{0}' (accnbr {1}).".format(settlement.CounterpartyAccName(),
                                                              settlement.CounterpartyAccountRef().Oid()))
        except:
            diary_note = ("Error: SettlementModification hook: Cannot set "
                          "counterparty account: {0}"
                          .format(sys.exc_info()[1]))
        finally:
            return diary_note

    if is_valid_security_transfer_trade(settlement):
        return change_counterparty_account(settlement)


def SettlementModification(settlement):
    """Hook: Amend the settlement before it is stored.

    Arguments:
    settlement (FSettlement) -- clone of the settlement to be amended

    Return string that will be saved into the settlement diary.
    """
    # NOTE: Be careful with exceptions in this hook. Any unhandled exception
    # raised from the hook out will cause the ATS settlement service to
    # terminate.
    diary_note = ''
    try:
        diary_note = _set_cp_account(settlement)
    except:
        diary_note = ("Error: SettlementModification hook: {0}"
                      .format(sys.exc_info()[1]))
        # LOGGER.exception("SettlementModification hook failed.")
    finally:
        # NOTE: Printing an empty string triggers a low-level memmory access
        # error when running the SettlementEOD task via the ATS binary on a
        # Linux machine. This terminates the task execution.  Therefore, we
        # check if the diary_record is non-empty before we log/print it.
        # if diary_record:
        #    LOGGER.info(diary_record)
        #    return diary_record
        if diary_note:
            return diary_note
        return ""


def is_valid_security_transfer_trade(settlement):
    """
    Defines a valid External Security Transfer Trade
    """
    if not settlement.Trade():
        return False
    trade = settlement.Trade()
    if trade.Status() != 'BO Confirmed':
        return False
    if trade.Type() != 'Security Transfer':
        return False
    if trade.OptKey1AsEnum() != 'External Transfer':
        return False
    instrument = trade.Instrument()
    if instrument.InsType() not in ['Bond', 'FRN', 'IndexLinkedBond', 'Repo/Reverse']:
        return False
    if not instrument.Isin().startswith('ZAG'):
        if instrument.Underlying():
            if not instrument.Underlying().Isin().startswith('ZAG'):
                return False
        else:
            return False

    if instrument.Currency().Name() != 'ZAR':
        return False
    if trade.SettleCategoryChlItem().Name() not in ['Euroclear', 'SA_CUSTODIAN']:
        return False

    return True


def change_counterparty_account(settlement):
    """
    Sets the counterpartyAccountRef for External Security Transfers
    Counterparty
    """
    trade = settlement.Trade()
    settle_catecory = trade.SettleCategoryChlItem().Name()
    party_ssi_effective_rule = None
    if settle_catecory == 'Euroclear':
        party_ssi_effective_rule = get_effective_rule_from_applicable_ssi(trade, 'SA_CUSTODIAN')
        if party_ssi_effective_rule is None:
            error_message = "Could not find applicable SSI for {category}, on party {party}!!"
            LOGGER.exception(error_message.format(category='SA_CUSTODIAN', party=trade.Acquirer().Name()))
            return
    elif settle_catecory == 'SA_CUSTODIAN':
        party_ssi_effective_rule = get_effective_rule_from_applicable_ssi(trade, 'Euroclear')
        if party_ssi_effective_rule is None:
            error_message = "Could not find applicable SSI for {category}, on party {party}!!"
            LOGGER.exception(error_message.format(category='Euroclear', party=trade.Acquirer().Name()))
            return
    else:
        error_message = "Settle Category for trade {trade_oid}, Not supported!!"
        LOGGER.exception(error_message.format(trade_oid=trade.Oid()))
        return

    #   Set Counterparty Account
    party_account = party_ssi_effective_rule.SecAccount()
    diary_note = ''
    try:
        settlement.CounterpartyAccountRef(party_account)
        diary_note = ("SettlementModification hook: Counterparty account "
                      "set to '{0}' (accnbr {1}).".format(settlement.CounterpartyAccName(),
                                                          settlement.CounterpartyAccountRef().Oid()))
    except Exception as e:
        diary_note = ("Error: SettlementModification hook: Cannot change "
                      "counterparty account: {0}"
                      .format(e))
    finally:
        return diary_note


def get_effective_rule_from_applicable_ssi(trade, settle_category):
    """
    Gets most effective Settle Category for External Security Transfers
    """
    party = trade.Acquirer()
    settle_instructions = party.SettleInstructions()
    for settle_instruction in settle_instructions:
        if settle_instruction.Type() != 'Security':
            continue
        if settle_instruction.QueryAttributeTradeSettleCategory() != settle_category:
            continue
        if 'ZAR' not in settle_instruction.QueryAttributeCurrency():
            continue
        settle_instruction_filter_nodes = [
            node.Value().StringKey()
            for node in settle_instruction.QueryFilter().AsqlNodes()
        ]
        optional_key_node = [
            node for node in settle_instruction_filter_nodes
            if 'Trade.OptKey1.Name = ' in node
        ]
        if not optional_key_node:
            continue
        optional_keys = optional_key_node[0].split('= ')[1].split(', ')
        if 'External Transfer' not in optional_keys:
            continue
        for rule in settle_instruction.Rules():
            if rule.EffectiveTo() != '':
                continue
            return rule

    return None


def _is_qualifying_mt298_settlement(settlement):
    """
    Checks is a settlement qualifies for 298
    """
    event_reference = settlement.AdditionalInfo().Call_Confirmation()
    if ':910' not in str(event_reference):
        return False

    return True


def get_funding_settlement_message_type(settlement, message_type):
    """
    Calculates custom message types for funding
    """

    if is_valid_curr_euroclear_payment(settlement):
        return '222'

    trade = settlement.Trade()
    if settlement.Amount() < 0:
        if settlement.Acquirer().Name() == 'AFRICA DESK' and settlement.Counterparty().Name() == 'AFRICA DESK':
            trade_settle_category = settlement.Trade().SettleCategoryChlItem().Name()
            if trade_settle_category and trade_settle_category in TRADE_SETTLE_CATEGORIES:
                if settlement.Type() in ['Premium', 'Payment Premium', 'Broker Fee']:
                    return '222'
                elif settlement.Type() == 'None':
                    return_222 = True
                    for settlement in settlement.Children():
                        if settlement.Type() not in ['Premium', 'Payment Premium', 'Broker Fee']:
                            return_222 = False
                    if return_222:
                        return '222'

    if trade and trade.SettleCategoryChlItem():
        if trade.SettleCategoryChlItem().Name() == 'Euroclear':
            if trade.Instrument().InsType() in ['Bill', 'Bond', 'BuySellback', 'FRN', 'Repo/Reverse',
                                                'IndexLinkedBond']:
                if trade.Status() in ['BO Confirmed', 'BO-BO Confirmed']:
                    if settlement.Type() == 'Stand Alone Payment':
                        return '210'
                    if settlement.Amount() > 0:
                        if settlement.Type() == 'Premium':
                            return '200'
                        if settlement.Type() in ('End Cash', 'None'):
                            return '200'
                    else:
                        if settlement.Type() == 'Premium':
                            return '222'
                        if settlement.Type() in ('End Cash', 'None'):
                            return '222'
    return message_type


def is_valid_curr_euroclear_payment(settlement):
    """
    Determine whether the settlement qualifies as
    Euroclear outgoing settlement.
    """

    trade = settlement.Trade()
    if not _is_valid_trade(trade):
        return False
    if not _is_valid_euroclear_outgoing_settlement(settlement):
        return False
    return True


def _is_valid_trade(trade):
    """
    Checks if the Trade is valid for MT222
    settlement Creation
    """
    if not trade:
        return False
    if trade.Instrument().InsType() not in VALID_INSTRUMENT_TYPES_FOR_222:
        return False
    if not trade.SettleCategoryChlItem():
        return False
    if trade.SettleCategoryChlItem().Name() != 'Euroclear':
        return False
    if not trade.Status() in VALID_TRADE_STATUS_FOR_222:
        return False

    return True


def _is_valid_euroclear_outgoing_settlement(settlement):
    """"
    Checks if the settlement is a valid 'Cash' or 'Internal Fee'
    """
    payment = settlement.Payment()
    if not settlement.Amount() < 0:
        return False
    if not settlement.Type() in VALID_SETTLEMENT_TYPES_FOR_222:
        return False
    currency_name = get_payment_currency_name(payment)
    if not currency_name in VALID_PAYMENT_CURRENCIES_FOR_222:
        return False
    return True


def get_payment_currency_name(payment):
    currency = payment.Currency()
    if not currency:
        return None
    return currency.Name()


