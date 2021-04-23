"""
HISTORY
=====================================================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------------------------------
2021-02-11      FAOPS-1043      Joshua Mvelase          Modified function get_unique_groupref
2021-01-26      FAOPS-977       Faize Adams             -Update get_account_no_for_sbl to read account details 
                                                        -using SSIs instead of directly from Accounts.
                                                        -Enable multiple SSIs for security settlements.
2021-03-26                      Faize Adams             -Update get_safe_custody_account to use settlement object 
                                                         instead of settlement category.
                                                                                   
---------------------------------------------------------------------------------------------------------------------
"""
import FSwiftWriterUtils
import FSwiftMLUtils
import acm
import ael
from sl_functions import getSLPartialReturned, getSLPartialReturnFirstTrade, getSLPartialReturnLastTrade, getSLPartialReturnPrevTrade, getSLPartialReturnAmountReturned
import datetime
from FSettlementEnums import RelationType
from FSwiftMessageValidation import FSwiftMessageValidation
from at_logging import getLogger

LOGGER = getLogger(__name__)


def is_security_loan_settlement(settlement):
    return settlement.Trade().TradeInstrumentType() == 'SecurityLoan'


def is_collateral_settlement(settlement):
    return settlement.Trade().TradeCategory() == 'Collateral'


def get_transaction_reference(settlement, mt_type):
    '''Mapping the Oid of the FExternalObject because SWIFT messages are stored in FExternalObject in FA.
       Cant use Trade or settlement Oid because we have to send 2 messages on single settlement. '''
    external_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=settlement, msg_typ=mt_type,
                                                                          integration_type='Outgoing')
    return settlement.Oid()


def get_transaction_reference_of_cancellation(settlement, mt_type):
    if settlement.RelationType() == RelationType.CANCELLATION:
        org_settlement = settlement.Children()[0]
        swift_message = FSwiftMLUtils.get_outgoing_mt_message(org_settlement)
        pyobj = FSwiftWriterUtils.create_pyobj_from_swift_msg(swift_message)
        return pyobj.TransactionReference.value()


def get_settlement_type_code(settlement):
    """
    Field 23:
    For Security Loans:
      when both of GX are either BP/non-BP we are always mapping the message sender's persepective
      when only one of them is a BP then we map the BP's persepective on both ends.


      if only one of them is BP:

             if new loan and G1 is BP: RFP/RFP
             if new loan adn G2 is BP: DFP/DFP

            if partial/full return and G1 is BP: DFP/DFP
            if partial/full return and G2 is BP: RFP/RFP

      else:
          if new loan and G1 is not BP : RFP
          if new loan and G2 is no BP: DFP

          if partial/full return and G1 is not BP: DFP
          if partial/full return and G2 is not BP: RFP


          if new loan and G1 is BP: RFP
          if new loan adn G2 is BP: DFP

          if partial/full return and G1 is BP: DFP
          if partial/full return and G2 is BP: RFP

    For Collateral:
        IF Counterparty is Business Partner (CSDP_STRATE_BPID is populated) and we Receive Collateral (BUY)
        then produce MT598-131 RFP
        IF Counterparty is Non-Business Partner (CSDP_STRATE_BPID is null) and we Receive Collateral (BUY)
        then produce MT598-130 DFP
        IF Counterparty is Business Partner (CSDP_STRATE_BPID is populated) and we Deliver Collateral (SELL)
        then produce MT598-131 DFP
        IF Counterparty is Non-Business Partner (CSDP_STRATE_BPID is null) and we Deliver Collateral (SELL)
        then produce MT598-130 RFP

    """
    trade = settlement.Trade()
    if is_security_loan_settlement(settlement):
        new_loan = is_new_loan(trade)
        g1_name = get_additionalinfo_value_for(trade, 'SL_G1Counterparty1')
        g2_name = get_additionalinfo_value_for(trade, 'SL_G1Counterparty2')
        g1 = acm.FParty[g1_name]
        g2 = acm.FParty[g2_name]
        g1_is_bp = is_business_partner(g1)
        g2_is_bp = is_business_partner(g2)
        print(g1.Name())
        print(g2.Name())
        if new_loan:
            if settlement.Type() == 'Security Nominal':
                return 'DFP' if g1_is_bp else 'RFP'
            elif settlement.Type() == 'End Security':
                return 'RFP' if g2_is_bp else 'DFP'
        else:
            if settlement.Type() == 'Security Nominal':
                return 'RFP' if g1_is_bp else 'DFP'
            elif settlement.Type() == 'End Security':
                return 'DFP' if g2_is_bp else 'RFP'
    elif is_collateral_settlement(settlement):
        party = get_client_from_settlement(settlement)
        if is_business_partner(party):
            return 'RFP' if trade.Direction() == 'Buy' else 'DFP'
        else:
            return 'DFP' if trade.Direction() == 'Buy' else 'RFP'


def is_new_loan(trade):
    return not getSLPartialReturned(trade)


def is_partial_return(trade):
    return getSLPartialReturned(trade)


def is_full_return(trade):
    return abs(getSLPartialReturnPrevTrade(trade).FaceValue()) == abs(trade.FaceValue())


def only_one_of_them_is_bp(client_is_bp, counterparty_is_bp):
    _only_one_of_them_is_bp = False
    if client_is_bp:
        if not counterparty_is_bp:
            _only_one_of_them_is_bp = True
    if counterparty_is_bp:
        if not client_is_bp:
            _only_one_of_them_is_bp = True
    return _only_one_of_them_is_bp


def get_settlement_date(settlement):
    if is_security_loan_settlement(settlement):
        return str(FSwiftWriterUtils.format_date(settlement.Trade().Instrument().StartDate(), '%Y%m%d'))
    elif is_collateral_settlement(settlement):
        return str(FSwiftWriterUtils.format_date(settlement.Trade().ValueDay(), '%Y%m%d'))


def get_trade_date(settlement):
    return str(FSwiftWriterUtils.format_date(settlement.Trade().TradeTime(), '%Y%m%d'))


def get_face_value_of_trade(settlement):
    """rounding is done for the amount because without it , the fucntion behaves weirdly. Dont know the reason for sure."""
    trade = settlement.Trade()
    if is_new_loan(trade):
        print('Swift 35A: New loan')
        return 'SHS' + str(int(round(abs(settlement.Trade().FaceValue()), 0)))
    if is_partial_return(trade):
        print('Swift 35A: Return')
        if is_full_return(trade):
            print('Swift 35A: Full return')
            return 'SHS' + str(int(round(abs(settlement.Trade().FaceValue()), 0)))
        return 'SHS' + str(getSLPartialReturnAmountReturned(trade))


def get_underlying_isin(settlement):
    if is_security_loan_settlement(settlement):
        return settlement.Trade().Instrument().Underlying().Isin()
    elif is_collateral_settlement(settlement):
        return settlement.Trade().Instrument().Isin()


def get_original_loan_ref(settlement, message_type):
    first_trade = getSLPartialReturnFirstTrade(settlement.Trade())
    original_loan_ref = None
    if first_trade:
        curr_settlement_type = settlement.Type()
        corresponding_settlement = None
        for first_trade_settlement in first_trade.Settlements():
            if first_trade_settlement.Type() == curr_settlement_type and first_trade_settlement.Status() != 'Updated' and first_trade_settlement.Status() in ["Settled",
                                                                                                        "Authorised",
                                                                                                        "Released"]:
                corresponding_settlement = first_trade_settlement
                break
        if corresponding_settlement:
            original_loan_ref = get_unique_SAFIRESloanReference(corresponding_settlement, message_type)

    if original_loan_ref:
        return original_loan_ref
    else:
        raise FSwiftMessageValidation(settlement, "NO_ORIGINAL_LOAN_REF")
    return original_loan_ref


def get_unique_groupref(settlement):
    """
    SecLoans:
        2 settlements on 1 trade need to have the same group ref.
        Trade number is the same so trade.oid % strate limit is used.
    Coll:
        2 settlements on 2 trades (1 per trade) need to have same group ref.
        So the contract ref on both trades need to be set the same value.
        The contract ref value is then used % strate limit.
    """
    trade = settlement.Trade()

    if is_collateral_settlement(settlement):
        contract_trade_number = trade.ContractTrdnbr()
        if contract_trade_number:
            contract_trade = acm.FTrade[contract_trade_number]
            return generate_unique_reference(contract_trade)

    return generate_unique_reference(trade)


def get_next_group_ref():
    try:
        return ael.dbsql('SELECT NEXT VALUE FOR dbo.strate_group_ref')[0][0][0]
    except Exception as error:
        LOGGER.exception(str(error))


def update_groupref_add_info(trade, unique_groupref):
    try:
        trade.AdditionalInfo().Unique_Strate_ID(str(unique_groupref))
        trade.Commit()
    except Exception as error:
        LOGGER.exception(str(error))


def generate_unique_reference(trade):
    groupref_add_info = trade.add_info('Unique_Strate_ID')
    if groupref_add_info:
        return groupref_add_info
    unique_groupref = get_next_group_ref()
    update_groupref_add_info(trade, unique_groupref)
    return unique_groupref


def get_narrative_for_598_131(settlement):
    values = []
    client = get_client_from_settlement(settlement)
    acquirers_bp_id = get_acquirers_bp_id(settlement)
    unique_groupref = get_unique_groupref(settlement)
    values.append(acquirers_bp_id)
    values.append(unique_groupref)

    if is_security_loan_settlement(settlement):
        if is_new_loan(settlement.Trade()):
            return '''/LOANTAX/N
/GRPREF/{0}/{1}
/SLBIND/LOAN'''.format(*values)
        else:
            loan_ref = get_original_loan_ref(settlement, 'MT598_131')
            values.append(str(loan_ref))
            return '''/LOANTAX/N
/GRPREF/{0}/{1}
/SLBIND/RETN
/LOANREF/{2}'''.format(*values)
    elif is_collateral_settlement(settlement):
        if is_new_loan(settlement.Trade()):
            pool_ref = get_strate_pool_ref(client, settlement)
            values.append(str(pool_ref))
            return '''/LOANTAX/N
/GRPREF/{0}/{1}
/SLBIND/DEPO
/POOLREF/{2}'''.format(*values)
        else:
            pool_ref = get_strate_pool_ref(client, settlement)
            values.append(str(pool_ref))
            return '''/LOANTAX/N
/GRPREF/{0}/{1}
/SLBIND/WITH
/POOLREF/{2}'''.format(*values)


def get_narrative_for_598_130(settlement):
    values = []
    client = get_client_from_settlement(settlement)
    values.append(str(client.Swift()))
    values.append(str(get_account_no_for_sbl(client, 'Security', settlement)))
    values.append(str(get_account_no_for_sbl(client, 'Cash', settlement)))
    values.append(str(get_acquirers_bp_id(settlement)))
    values.append(get_unique_groupref(settlement))

    if is_security_loan_settlement(settlement):
        if is_new_loan(settlement.Trade()):
            return '''/CLIE/{0}
//SAFE/{1}
//CASH/{2}
/LOANTAX/N
/GRPREF/{3}/{4}
/SLBIND/LOAN'''.format(*values)
        else:
            loan_ref = get_original_loan_ref(settlement, 'MT598_130')
            values.append(str(loan_ref))
            return '''/CLIE/{0}
//SAFE/{1}
//CASH/{2}
/LOANTAX/N
/GRPREF/{3}/{4}
/SLBIND/RETN
/LOANREF/{5}'''.format(*values)
    elif is_collateral_settlement(settlement):
        if is_new_loan(settlement.Trade()):
            pool_ref = get_strate_pool_ref(client, settlement)
            values.append(str(pool_ref))
            return '''/CLIE/{0}
//SAFE/{1}
//CASH/{2}
/LOANTAX/N
/GRPREF/{3}/{4}
/SLBIND/DEPO
/POOLREF/{5}'''.format(*values)
        else:
            pool_ref = get_strate_pool_ref(client, settlement)
            values.append(str(pool_ref))
            return '''/CLIE/{0}
//SAFE/{1}
//CASH/{2}
/LOANTAX/N
/GRPREF/{3}/{4}
/SLBIND/WITH
/POOLREF/{5}'''.format(*values)


def get_account_no_for_sbl(party, acc_type, settlement, return_object=False):
    account = None
    settlement_instruction = None
    settlement_category = settlement.Trade().SettleCategoryChlItem().Name()
    instrument_type = settlement.Trade().Instrument().InsType()
    settlement_type = settlement.Type()
    settlement_date = get_settlement_date(settlement)
        
    for ssi in party.SettleInstructions():
        if settlement_category == ssi.QueryAttributeTradeSettleCategory() and\
           instrument_type in ssi.QueryAttributeInstrumentType() and\
           settlement_type in ssi.QueryAttributeCashFlowType() and\
           acc_type == ssi.Type() and\
           ssi.IsActive():
           settlement_instruction = ssi
           break
    
    if settlement_instruction:
        for instruction_rule in settlement_instruction.Rules():
            if (instruction_rule.EffectiveFrom() <= settlement_date) and\
               (instruction_rule.EffectiveTo() == "" or settlement_date <= instruction_rule.EffectiveTo()):
                if acc_type == "Cash":
                    account = instruction_rule.CashAccount()
                elif acc_type == "Security": 
                    account = instruction_rule.SecAccount()
                break
    else:
        raise FSwiftMessageValidation(settlement, "NO_CP_ACC_NO")
        
    if account:
        if return_object:
            return account
        else:
            return account.Account()
        
    return "[Exception: NO ACCOUNT NUMBER]"


def get_unique_SAFIRESloanReference(settlement, mt_type):
    '''2a = ZA, 6a= our BP id , 10n = settlement Oid because we are
        going to map the incoming by using this field '''
    our_bp_id = get_acquirers_bp_id(settlement)
    if settlement.RelationType() == RelationType.CANCELLATION:
        org_settlement = settlement.Children()[0]
        transaction_id = org_settlement.Oid()  # get_transaction_reference_of_cancellation(settlement, mt_type)
    else:
        transaction_id = settlement.Oid()  # get_transaction_reference(settlement, mt_type)
    return '{0}/{1}'.format(our_bp_id, transaction_id)


def get_bp_id(party):
    '''use function get_additionalinfo_value_for '''
    csdp_strate_bpid = get_additionalinfo_value_for(party, 'CSDP_STRATE_BPID')
    return csdp_strate_bpid


def get_strate_pool_ref(party, settlement):
    '''use function get_additionalinfo_value_for STRATE_POOL_REF'''
    strate_pool_ref = get_additionalinfo_value_for(party, 'STRATE_POOL_REF')

    if strate_pool_ref:
        return strate_pool_ref
    else:
        raise FSwiftMessageValidation(settlement, "NO_STRATE_POOL_REF")
    return strate_pool_ref


def get_client_from_settlement(settlement):
    """
    Here assumption is that Settlement of type Security Nominal will always correspond to message sent on behalf of
    SL_G1Counterparty1 and Settlement of type End Security will always correspond to message sent on behalf of
    SL_G1Counterparty2
    """
    trade = settlement.Trade()
    party = None
    if is_security_loan_settlement(settlement):
        trading_party_name = ''
        if settlement.Type() == 'Security Nominal':
            trading_party_name = get_additionalinfo_value_for(trade, 'SL_G1Counterparty1')
        if settlement.Type() == 'End Security':
            trading_party_name = get_additionalinfo_value_for(trade, 'SL_G1Counterparty2')
        party = acm.FParty[trading_party_name]
    elif is_collateral_settlement(settlement):
        party = trade.Counterparty()

    if party:
        return party
    else:
        raise FSwiftMessageValidation(settlement, "NO_CP")
    return party


def get_custodian_for(party, settlement):
    account = get_account_no_for_sbl(party, 'Security', settlement, True)

    if account and account.CorrespondentBank():
        return account.CorrespondentBank()
    else:
        raise FSwiftMessageValidation(settlement, "NO_CUSTODIAN")
    return account.CorrespondentBank()


def get_trading_party_data(settlement):
    party = None
    party = get_client_from_settlement(settlement)
    if party:
        custodian = get_custodian_for(party, settlement)
        if custodian:
            return get_bp_id(custodian)
    return None


def get_acquirers_bp_id(settlement):
    party = settlement.Acquirer()
    bp_id = get_bp_id(party)
    if bp_id:
        return str(bp_id)
    else:
        raise FSwiftMessageValidation(settlement, "NO_ACQUIRERS_BP_ID")
    return str(bp_id)


def get_place_of_settlement_for(party, settlement):
    account = get_account_no_for_sbl(party, 'Security', settlement, True)
    if account:
        return account.Account3()
    return account


def get_account_subnetwork_from_settlement_category(settlement_category):
    sub_network = ""
    if settlement_category == 'SL_STRATE':
        sub_network = 'SBLOnMarket'
    elif settlement_category == 'SL_CUSTODIAN':
        sub_network = 'SBLOffMarket'
    return sub_network


def get_safe_custody_account(settlement):
    party = get_client_from_settlement(settlement)
    account = get_place_of_settlement_for(party, settlement)
    return '/' + str(account)


def number_of_repetitive_parts(settlement):
    return '1'


def get_additionalinfo_value_for(fobject, add_info_name):
    try:
        add_inf = getattr(fobject.AdditionalInfo(), add_info_name)
        return add_inf()
    except AttributeError:
        print('AdditionalInfo {0} not defiend on {1} '.format(add_info_name, type(fobject)))
        return ''


def get_senders_bic(settlement):
    account = settlement.AcquirerAccountRef()
    if account:
        if account.NetworkAlias():
            return account.NetworkAlias().Alias()
    assert settlement.AcquirerAccountRef(), "The settlement has no acquirer account reference"
    assert settlement.AcquirerAccountRef().Party(), "The acquirer account referenced by the settlement has no party"
    senders_bic = account.Party().Swift()

    if senders_bic:
        return senders_bic
    else:
        raise FSwiftMessageValidation(settlement, "NO_SENDERS_BIC")
    return senders_bic


def get_receivers_bic(settlement):
    receiverBic = ''
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
    if receiverBic:
        return receiverBic
    else:
        raise FSwiftMessageValidation(settlement, "NO_RECEIVER_BIC")
    return receiverBic


def get_settlement_reference_prefix():
    """ Method to get settlement reference prefix to be sent in the MT message. """
    '''cash_settlement_out_config = FSwiftWriterUtils.get_config_from_fparameter('FCashOut_Config')
    if str(getattr(cash_settlement_out_config, 'FAS',"")) == "":
        return str(getattr(writer_config, 'FAS',"FAS"))
    return str(getattr(cash_settlement_out_config, 'FAS', None))'''
    return 'FAS'


def get_message_version_number(fObject, is_free_text_msg=False):
    """ Method to get the message version number
    :param fObject: object from which message version number is to be fetched
    :param is_free_text_msg: flag indicating is_free_text_msg
    :return: message version number
    """
    msg_version_number = fObject.VersionId()
    if is_free_text_msg:
        msg_version_number = str(msg_version_number) + 'F'
    return str(msg_version_number)


def get_counter_party_data(settlement):
    client = get_client_from_settlement(settlement)
    return get_bp_id(client)


def is_business_partner(party):
    bpid = get_bp_id(party)
    if bpid and len(bpid) > 0:
        return True
    else:
        return False


