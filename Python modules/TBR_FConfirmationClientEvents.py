""" Compiled: 2009-10-14 04:19:36 """

"""----------------------------------------------------------------------------
MODULE
    FConfirmationClientEventsTempl - Module that includes customer specific
    rules for handling events that effects confirmation records.

    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION    

RENAME this module via Python editor to FConfirmationClientEvents if you want
to override default functionality.

NOTE: It is not recomended to import other default Confirmations scripts 
then FConfirmationGeneral.

Date                : 2011-03-11, 2011-03-17, 2011-03-31
Purpose             : update the validation on the creation of confirmation records to validate against the AMBA message and not against the actual trade in Front,
                      Inserts on parties regenerated confirmations linked to the updated party.,
		      Add check for acquirer and counterparty type object in amendment restrict.
Department and Desk : OPS , IT, IT
Requester           : Miguel da Silva, Heinrich Cronje, Heinrich Cronje
Developer           : Ickin Vural, Pontus Aberg, Heinrich Cronje
CR Number           : C000000595846, 603435,616180


----------------------------------------------------------------------------"""
import amb, ael
import FConfirmationGeneral
import FConfirmationClientEventsUtils as ClientEventsUtils

# This module is called from the core confirmation scripts ones the
# amba message for Trade/Instrument comes in.  This list
# also matters for creation of ammendmens and cancellations of client event
# confirmations. See also function get_trades_from_party where this function 
# is also used.
neglect_trade_status = ['Simulated', 'Confirmed Void', 'Exchange', 'Void']


# --------------
# FIELDS
# --------------
# Changes in the following fields trigger corresponding confirmation update

field_dict = {}

# contact
#field_dict['CONTACT'] = \
#    ['ADDRESS', 'ADDRESS2', 'ATTENTION', 'CITY', 'COUNTRY', 'EMAIL', 'FAX',
#     'FREE1', 'FREE2', 'FULLNAME', 'NETWORK2_ALIAS_SEQNBR',
#     'NETWORK2_ALIAS_TYPE', 'NETWORK_ALIAS_SEQNBR', 'NETWORK_ALIAS_TYPE',
#     'PTYNBR', 'TELEPHONE', 'ZIPCODE']
field_dict['CONTACT'] = []

# contact rule
#field_dict['CONTACTRULE'] = \
#    ['ACQUIRER_PTYNBR', 'CURR', 'EVENT_CHLNBR', 'INSTYPE',
#     'PRODUCT_TYPE_CHLNBR']
field_dict['CONTACTRULE'] = []

# confirmation
field_dict['CONFIRMATION'] = \
    ['CHASER_CUTOFF', 'CHASING_SEQNBR', 'CONFIRMATION_SEQNBR', 
     'CONF_TEMPLATE_CHLNBR', 'DOCUMENT', 'EVENT_CHLNBR', 'MANUAL_MATCH',
     'RESET_RESNBR', 'STATUS', 'STATUS_EXPLANATION', 'TRANSPORT', 'TRDNBR',
     'UPDAT_USRNBR', 'CFWNBR']

#field_dict['SETTLEMENT'] = \
#    ['ACQUIRER_ACCNAME', 'ACQUIRER_ACCOUNT', 'ACQUIRER_ACCOUNT_NETWORK_NAME',
#    'ACQUIRER_PTYID', 'ACQUIRER_PTYNBR', 'AMOUNT', 'CFWNBR', 'COUNTERPARTY_PTYNBR', 
#    'CURR', 'DELIVERY_TYPE', 'DIVIDEND_SEQNBR', 
#    'DOCUMENT', 'FROM_PRFNBR', 'MESSAGE_TYPE', 'NETTING_RULE_SEQNBR', 
#    'NOTIFICATION_DAY', 'ORG_SEC_NOM', 'PARTY_ACCOUNT', 'PARTY_ACCOUNT_NETWORK_NAME', 
#    'PARTY_PTYID', 'PAYNBR', 'POST_SETTLE_ACTION', 'PRIMARY_ISSUANCE', 
#    'REF_PAYNBR', 'REF_SEQNBR', 'REF_TYPE', 'RESTRICT_NET', 'SEC_INSADDR', 
#    'SETTLE_CATEGORY', 'SETTLE_SEQNBR', 'SETTLED_AMOUNT', 
#    'SETTLEINSTRUCTION_SEQNBR', 'STATUS', 'STATUS_EXPLANATION', 
#    'TEXT', 'TO_PRFNBR', 'TRDNBR', 'TYPE', 'VALUE_DAY']
field_dict['SETTLEMENT'] = []

# instrument
field_dict['INSTRUMENT'] = \
    ['BARRIER', 'CALLABLE', 'CALL_OPTION', 'CONTR_SIZE', 'COUPONS',
     'COUP_RATE', 'CURR', 'DAYCOUNT_METHOD', 'DIGITAL', 'EX_COUP_METHOD',
     'EX_COUP_PERIOD', 'EXP_PERIOD', 'EXP_TIME', 'EXERCISE_TYPE',
     'EXOTIC_TYPE', 'EXP_DAY', 'INDEX_FACTOR', 'INSID', 'INSTYPE', 'ISSUE_DAY',
     'ISSUER', 'ISSUER_PTYNBR', 'LAST_COUP_DAY', 'NOTICE_PERIOD', 'OPEN_END',
     'ORIGINAL_CURR', 'ORIGINAL_INSADDR', 'PAY_DAY_OFFSET',
     'PAY_OFFSET_METHOD', 'PAYTYPE', 'PRODUCT_CHLNBR', 'PRODUCT_TYPE_CHLNBR',
     'PUTABLE', 'RATE', 'REBATE', 'SENIORITY_CHLNBR', 'SETTLEMENT', 'START_DAY',
     'STRIKE_CURR', 'STRIKE_PRICE', 'STRIKE_TYPE', 'UND_INSADDR', 'UND_INSTYPE']

# leg
field_dict['LEG'] = \
    ['AMORT_DAYCOUNT_METHOD', 'AMORT_END_DAY', 'AMORT_END_NOMINAL_FACTOR',
     'AMORT_END_PERIOD', 'AMORT_START_DAY', 'AMORT_START_PERIOD', 'AMORT_TYPE',
     'ANNUITY_RATE', 'BARRIER', 'CREDIT_REF', 'CURR', 'DAYCOUNT_METHOD',
     'DIGITAL', 'END_DAY', 'END_PERIOD', 'EXOTIC_TYPE', 'FIXED_COUPON',
     'FIXED_RATE', 'FLOAT_RATE', 'NOMINAL_FACTOR', 'PAYLEG', 'PAY_CALNBR',
     'PAY2_CALNBR', 'PAY3_CALNBR', 'PAY_DAY_METHOD', 'PAY_DAY_OFFSET',
     'RESET_CALNBR', 'RESET2_CALNBR', 'RESET3_CALNBR', 'RESET_DAY_METHOD',
     'RESET_DAY_OFFSET', 'RESET_PERIOD', 'RESET_TYPE', 'ROLLING_BASE_DAY',
     'ROLLING_PERIOD', 'SPREAD', 'START_DAY', 'START_PERIOD', 'STRIKE', 'TYPE']

# cash flow
field_dict['CASHFLOW'] = \
    ['END_DAY', 'EXCLUDE', 'FIXED_AMOUNT', 'FIXED_TIME', 'FLOAT_RATE_FACTOR',
     'FLOAT_RATE_FACTOR2', 'FLOAT_RATE_OFFSET', 'NOMINAL_FACTOR', 'PAY_DAY',
     'RATE', 'SPREAD', 'SPREAD2', 'START_DAY', 'STRIKE_RATE', 'TYPE']

# party
#field_dict['PARTY'] = \
#    ['ADDRESS', 'ADDRESS2', 'ATTENTION', 'CALCAGENT', 'CITY', 'CONTACT1',
#     'CONTACT2', 'CORRESPONDENT_BANK', 'COUNTRY', 'DOCUMENT_DATE',
#     'DOCUMENT_TYPE_CHLNBR', 'EMAIL', 'EXTERNAL_CUTOFF', 'FAX', 'FREE1',
#     'FREE2', 'FREE3', 'FREE4', 'FREE5', 'FREE1_CHLNBR', 'FREE2_CHLNBR',
#     'FREE3_CHLNBR', 'FREE4_CHLNBR', 'FULLNAME', 'FULLNAME2',
#    'GUARANTOR_PTYNBR', 'INTERNAL_CUTOFF', 'ISDA_MEMBER', 'ISSUER',
#     'LEGAL_FORM_CHLNBR', 'NOTIFY_RECEIPT', 'PARENT_PTYNBR', 'PTYID', 'PTYID2',
#     'RED_CODE', 'SWIFT', 'TELEPHONE', 'TELEX', 'TIME_ZONE', 'TYPE', 'ZIPCODE']
field_dict['PARTY'] = []
                                               
# party alias
#field_dict['PARTYALIAS'] = \
#    ['ALIAS', 'PTYNBR', 'TYPE']
field_dict['PARTYALIAS'] = []

# agreement
#field_dict['AGREEMENT'] = \
#    ['COUNTERPARTY_PTYNBR', 'DATED', 'DOCUMENT_TYPE_CHLNBR', 'INSTYPE',
#     'INTERNDEPT_PTYNBR', 'UND_INSTYPE']
field_dict['AGREEMENT'] = []

# account
#field_dict['ACCOUNT'] = \
#    ['ACCOUNT', 'ACCOUNT2', 'ACCOUNT3', 'ACCOUNT4', 'ACCOUNT5', 'CURR', 'NAME',
#     'SWIFT', 'SWIFT2', 'SWIFT3', 'SWIFT4', 'DETAILS_OF_CHARGES', 'BIC_SEQNBR',
#     'BIC2_SEQNBR', 'BIC3_SEQNBR', 'BIC4_SEQNBR', 'BIC5_SEQNBR',
#     'NETWORK_ALIAS_TYPE', 'NETWORK_ALIAS_SEQNBR', 'CORRESPONDENT_BANK_PTYNBR',
#     'CORRESPONDENT_BANK2_PTYNBR', 'CORRESPONDENT_BANK3_PTYNBR',
#     'CORRESPONDENT_BANK4_PTYNBR', 'CORRESPONDENT_BANK5_PTYNBR',
#    'INTERNAL_CUTOFF', 'EXTERNAL_CUTOFF', 'ACCOUNT_TYPE']
field_dict['ACCOUNT'] = []

# reset
#field_dict['RESET'] = \
#    ['CFWNBR', 'DAY', 'END_DAY', 'LEGNBR', 'READ_TIME', 'START_DAY', 'TYPE',
#     'VALUE']
field_dict['RESET'] = []

# trade
field_dict['TRADE'] = \
    ['ACQUIRE_DAY', 'ACQUIRER_PTYNBR', 'BROKER_PTYNBR',
     'CALCAGENT', 'CONNECTED_TRDNBR', 'CONTRACT_TRDNBR', 'CORRECTION_TRDNBR',
     'COUNTERPARTY_PTYNBR', 'CURR', 'DOCUMENT_TYPE_CHLNBR', 'FEE', 'INSADDR',
     'MIRROR_TRDNBR', 'OPTKEY2_CHLNBR', 'OPTKEY1_CHLNBR',
     'OPTKEY3_CHLNBR', 'OPTKEY4_CHLNBR', 'ORIGINAL_CURR', 'PREMIUM', 'PRICE', 
     'QUANTITY', 'QUOTATION_SEQNBR', 'SETTLE_CATEGORY_CHLNBR', 'TIME', 
     'TRADE_CURR', 'TRX_TRDNBR', 'TYPE', 'VALUE_DAY', 'YOUR_REF']


# trade account link
#field_dict['TRADEACCOUNTLINK'] = \
#    ['ACCNBR', 'CURR', 'PARTY_TYPE', 'SEC_ACCNBR', 'SEC_SETTLE_CF_TYPE',
#     'SETTLE_CF_TYPE', 'SETTLE_DELIVERY_TYPE', 'SETTLE_SEQNBR']
field_dict['TRADEACCOUNTLINK'] = []

# payment
field_dict['PAYMENT'] = \
    ['ACCNBR', 'AMOUNT', 'CURR', 'OUR_ACCNBR', 'PAYDAY', 'PTYNBR', 'TEXT',
     'TYPE', 'VALID_FROM']

# exotic
#field_dict['EXOTIC'] = \
#    ['AVERAGE_METHOD_TYPE', 'AVERAGE_STRIKE_TYPE', 'BARRIER_MONITORING',
#     'BARRIER_OPTION_TYPE', 'BARRIER_REBATE_ON_EXPIRY', 'CHOOSER_CALL_STRIKE',
#     'CHOOSER_DATE', 'CHOOSER_PUT_STRIKE', 'CLIQUET_OPTION_TYPE',
#     'COUPON_CREDIT', 'DIGITAL_BARRIER_TYPE', 'DOUBLE_BARRIER',
#     'FORWARD_START_DATE', 'FORWARD_START_TYPE', 'GLOBAL_CAP', 'GLOBAL_FLOOR',
#     'INS_SERIES_TYPE', 'INSADDR', 'LADDER_DISCRETE_MONITORING', 'LOCAL_CAP',
#     'LOCAL_FLOOR', 'LOOKBACK_DISCRETE_MONITORING', 'LOOKBACK_EXTREME_VALUE',
#     'LOOKBACK_OPTION_TYPE', 'POWER_EXPONENT', 'POWER_GEARING',
#     'RAINBOW_OPTION_TYPE', 'RANGE_ACCRUAL_AMOUNT', 'RANGE_ACCRUAL_CAP',
#    'RANGE_ACCRUAL_FLOOR', 'VARIANCE_DIV_ADJ_RETURNS', 'VARIANCE_FACTOR',
#     'VARIANCE_SWAP_TYPE']
field_dict['EXOTIC'] = []

# exotic event
#field_dict['EXOTICEVENT'] = \
#    ['DATE', 'END_DATE', 'INSADDR', 'TYPE', 'VALUE']
field_dict['EXOTICEVENT'] = []

# exercise event
#field_dict['EXERCISEEVENT'] = \
#    ['EXP_TIME', 'DAY', 'NOTICE_DAY', 'NOTICE_PERIOD', 'PERIOD', 'SETTLE_DAY',
#     'SETTLE_PERIOD', 'START_DAY', 'START_PERIOD', 'STRIKE', 'TYPE']
field_dict['EXERCISEEVENT'] = []

# credit event
#field_dict['CREDITEVENTSPEC'] = \
#    ['BANKRUPTCY', 'DEFAULT_DATE', 'DELIV_OBL_INSADDR',
#     'DEL_OBL_CATEGORY_CHLNBR', 'FAILURE_TO_PAY', 'OBL_ACCELERATION',
#     'OBL_CATEGORY_CHLNBR', 'OBL_DEFAULT', 'RECOVERY_RATE', 'REPUDIATION',
#     'RESTRUCTURING_TYPE']
field_dict['CREDITEVENTSPEC'] = []

# combination link
#field_dict['COMBINATIONLINK'] = \
#    ['OWNER_INSADDR', 'MEMBER_INSADDR', 'WEIGHT', 'FIX_FX_RATE',
#     'ORDERBOOK_OID', 'DEFAULT_DATE', 'RECOVERY_RATE', 'RESTRUCTURING_TYPE']
field_dict['COMBINATIONLINK'] = []

def is_new_trade_restrict(message):
    ''' This function is called after the core confirmation scripts has
    classified the message as representing a New Trade event.  This can be
    overridden by returning 0 from this function, i.e. if this function returns
    0 no New Trade confirmation will be generated.'''
    FConfirmationGeneral.log_trace()

    ret = 1
#    Example, only create confirmations for otc instruments:
#    trade = message.mbf_find_object('+TRADE')
#    if trade:
#        insaddr_obj = trade.mbf_find_object('INSADDR')
#        if insaddr_obj:
#            insaddr = int(insaddr_obj.mbf_get_value())
#            ins = ael.Instrument[insaddr]
#            if ins and not ins.otc:            
#                pr = 'trade in non-otc instrument, no New Trade event'
#                FConfirmationGeneral.log(5, pr)
#                ret = 0

    #FA-TLM - IRD Confirmations
    trade  = message.mbf_find_object("TRADE") or message.mbf_find_object("+TRADE") or message.mbf_find_object("!TRADE")
    MsgType = message.mbf_find_object("TYPE")
    AddInfo = trade.mbf_find_object('!ADDITIONALINFO', 'MBFE_BEGININNG') or trade.mbf_find_object('+ADDITIONALINFO', 'MBFE_BEGININNG')


    if trade:
        insaddr_obj = trade.mbf_find_object('INSADDR')
        if insaddr_obj:
            insaddr = int(insaddr_obj.mbf_get_value())
            ins = ael.Instrument[insaddr]
            if ins:
                trd_obj = trade.mbf_find_object('TRDNBR')
                trdnbr = int(trd_obj.mbf_get_value())
                trd = ael.Trade[trdnbr]
                if trd:
                    if trd.acquirer_ptynbr:
                        '''create confirmations for the following instrument types:
                        FRA, SWAP, IndesxLinkedSwap, Cap, Floor, CurrSwap on the
                        following acquirers: IRD DESK'''
                        if trade.mbf_find_object("INSADDR.INSTYPE").mbf_get_value() not in ('FRA', 'Swap', 'IndexLinkedSwap', 'Cap', 'Floor', 'CurrSwap', 'Option') or trade.mbf_find_object("ACQUIRER_PTYNBR.PTYID").mbf_get_value() not in ('IRD DESK'):
                            pr = 'No New Trade event: Instrument or Acquirer violation.'
                            FConfirmationGeneral.log(5, pr)
                            ret = 0
                            return ret
                        else:
                            '''create confirmation for non interdesk trades.'''
                            if trade.mbf_find_object("COUNTERPARTY_PTYNBR"):
                                if trade.mbf_find_object("ACQUIRER_PTYNBR"):
                                    if trade.mbf_find_object("ACQUIRER_PTYNBR.TYPE").mbf_get_value() == trade.mbf_find_object("COUNTERPARTY_PTYNBR.TYPE").mbf_get_value():
                                        pr = 'No New Trade event: Interdesk trade.'
                                        FConfirmationGeneral.log(5, pr)
                                        ret = 0
                                        return ret
                            '''do not create confirmations for trades that have additional
                            info MarkitWire containing "MW"'''
                            while AddInfo:
                                if AddInfo.mbf_find_object("ADDINF_SPECNBR.FIELD_NAME").mbf_get_value() == 'CCPmiddleware_id':
                                    if str(AddInfo.mbf_find_object("VALUE").mbf_get_value()).__contains__('MW'):
                                        pr = 'No New Trade event: MarkitWire trade.'
                                        FConfirmationGeneral.log(5, pr)
                                        ret = 0
                                        return ret
                                trade.mbf_remove_object()
                                AddInfo = trade.mbf_find_object('!ADDITIONALINFO', 'MBFE_CURRENT') or trade.mbf_find_object('+ADDITIONALINFO', 'MBFE_CURRENT')
                                
                            '''Do not create Confirmations for BO-BO Confirmed or Terminated trades.'''
                            if trade.mbf_find_object("STATUS").mbf_get_value() in ('BO-BO Confirmed', 'Terminated'):
                                pr = 'No New Trade event: BO-BO Confirmed or Terminated Trade.'
                                FConfirmationGeneral.log(5, pr)
                                ret = 0
                                return ret
                                
                            '''Do not create Confirmations for Exercised Swaptions.'''
                            if trd.insaddr.instype == 'Option':
                            #if trade.mbf_find_object("INSADDR.INSTYPE").mbf_get_value() == 'Option':
                                if trd.insaddr.und_insaddr.instype == 'Swap':
                                #if trade.mbf_find_object("INSADDR.UND_INSADDR.INSTYPE").mbf_get_value() == 'Swap':
                                    if trd.type == 'Exercise':
                                    #if trade.mbf_find_object("TYPE").mbf_get_value() == 'Exercise':
                                        pr = 'No New Trade event: Exercised Trade.'
                                        FConfirmationGeneral.log(5, pr)
                                        ret = 0
                                        return ret
                                    
    return ret


def is_new_trade_extend(message):
    ''' This function is called after the core confirmation scripts has
    classified the message as not representing a New Trade event.  This can be
    overridden by returning 1 from this function, i.e. if this function returns
    1 a New Trade confirmation will be generated.'''
    FConfirmationGeneral.log_trace()

    ret = 0
#    Example, generate confirmation for status FO Confirmed if acquirer is ABC:
#    status = ''
#    abc_ptynbr = ael.Party['FCS EQUITY'].ptynbr
#    acquirer_ptynbr = 0
#    trade = message.mbf_find_object('+TRADE')
#    if trade:
#        status_obj = trade.mbf_find_object('STATUS')
#        if not status_obj:
#            status_obj = trade.mbf_find_object('!STATUS')
#        if status_obj:
#            status = status_obj.mbf_get_value()
#        acquirer_obj = trade.mbf_find_object('ACQUIRER_PTYNBR')
#        if not acquirer_obj:
#            acquirer_obj = trade.mbf_find_object('!ACQUIRER_PTYNBR')
#        if acquirer_obj:
#            acquirer_ptynbr = int(acquirer_obj.mbf_get_value())
#        if status == 'FO Confirmed' and acquirer_ptyid == 'ABC':
#            pr = 'status FO Confirmed, acquirer ABC, generate New Trade ' \
#                 'confirmation'
#            FConfirmationGeneral.log(5, pr)
#            ret = 1
    return ret

def is_amendment_restrict(message):
    ''' This function is called after the core confirmation scripts has
    classified the message as representing an Amendment event.  This can be
    overridden by returning 0 from this function, i.e. if this function returns
    0 no Amendment confirmation will be generated.

    The message input parameter can represent either a trade, instrument,
    party or contact entiry. '''
    FConfirmationGeneral.log_trace()

    #SunGard Code: If a party was updated, all Confirmations to that party was seen as updates.
    isAmendment = 0
    trade = message.mbf_find_object('!TRADE')
    if trade:
        isAmendment = 1
    instrument = message.mbf_find_object('!INSTRUMENT')
    if instrument:
        isAmendment = 1
    
    if isAmendment == 0:
        FConfirmationGeneral.log(1, "Restricting update to confirmations, no trade or instrument information where changed!")
        return isAmendment

    ret = 1

    trade = message.mbf_find_object('!TRADE') or message.mbf_find_object('TRADE') or message.mbf_find_object('+TRADE')
    
    
    if trade:
        AddInfo = trade.mbf_find_object('!ADDITIONALINFO', 'MBFE_BEGININNG') or trade.mbf_find_object('+ADDITIONALINFO', 'MBFE_BEGININNG')
        
        trd_obj = trade.mbf_find_object('TRDNBR')
        trdnbr = int(trd_obj.mbf_get_value())
        trd = ael.Trade[trdnbr]
        if trdnbr:
            #Don't generate amendment if CP ref is updated:
            cp_ref_obj = trade.mbf_find_object('!YOUR_REF')
            if cp_ref_obj:
                pr = str(trdnbr) + ' CP Ref Updated, no Amendment'
                FConfirmationGeneral.log(5, pr)
                ret = 0
                return ret

            '''Do not create Confirmations for Terminated trades.'''
            if trade.mbf_find_object("STATUS").mbf_get_value() in ('BO-BO Confirmed', 'Terminated'):
                pr = 'No Amendment event: Terminated Trade.'
                FConfirmationGeneral.log(5, pr)
                ret = 0
                return ret
                
            '''create confirmation for non interdesk trades.'''
            cp_obj = trade.mbf_find_object("COUNTERPARTY_PTYNBR.TYPE")
            acq_obj = trade.mbf_find_object("ACQUIRER_PTYNBR.TYPE")
            if cp_obj and acq_obj:
                if acq_obj.mbf_get_value() == cp_obj.mbf_get_value():
                    pr = 'No Amendment event: Interdesk trade.'
                    FConfirmationGeneral.log(5, pr)
                    ret = 0
                    return ret
                    
            '''do not create confirmations for trades that have additional
            info MarkitWire containing "MW"'''
            while AddInfo:
                if AddInfo.mbf_find_object("ADDINF_SPECNBR.FIELD_NAME").mbf_get_value() == 'CCPmiddleware_id':
                    if str(AddInfo.mbf_find_object("VALUE").mbf_get_value()).__contains__('MW'):
                        pr = 'No Amendment event: MarkitWire trade.'
                        FConfirmationGeneral.log(5, pr)
                        ret = 0
                        return ret
                trade.mbf_remove_object()
                AddInfo = trade.mbf_find_object('!ADDITIONALINFO', 'MBFE_CURRENT') or trade.mbf_find_object('+ADDITIONALINFO', 'MBFE_CURRENT')
                
            '''Do not create Confirmations for Terminated trades.'''
            if trade.mbf_find_object("STATUS").mbf_get_value() in ('Terminated'):
                pr = 'No Amendment event: Terminated Trade.'
                FConfirmationGeneral.log(5, pr)
                ret = 0
                return ret
                
            '''Do not create Confirmations for Exercised Swaptions.'''
            if trd.insaddr.instype == 'Option':
            #if trade.mbf_find_object("INSADDR.INSTYPE").mbf_get_value() == 'Option':
                if trd.insaddr.und_insaddr.instype == 'Swap':
                #if trade.mbf_find_object("INSADDR.UND_INSADDR.INSTYPE").mbf_get_value() == 'Swap':
                    if trd.type == 'Exercise':
                    #if trade.mbf_find_object("TYPE").mbf_get_value() == 'Exercise':
                        pr = 'No Amendment event: Exercised Trade.'
                        FConfirmationGeneral.log(5, pr)
                        ret = 0
                        return ret

    '''else:
        #This case below corresponds to the use of the correct trade functionality
        trade = message.mbf_find_object('+TRADE')
        if trade:
            trdnbr_obj = trade.mbf_find_object('TRDNBR')
            if trdnbr_obj:
                trdnbr = trdnbr_obj.mbf_get_value()
                trade = ael.Trade[int(trdnbr)]
                #Don't generate amendment if CP ref is updated:
                if FConfirmationGeneral.trade_is_correction(trade):
                    corr = trade.correction_trdnbr
                    if corr.your_ref != trade.your_ref:
                        pr = trdnbr + ' CP Ref Updated, no Amendment'
                        FConfirmationGeneral.log(3, pr)
                        ret = 0
    '''

#    Example, don't generate amendment if trade key 3 updated:
#    trade = message.mbf_find_object('!TRADE')
#    if trade:
#        tradekey3_obj = trade.mbf_find_object('!OPTKEY3_CHLNBR')
#        if tradekey3_obj:
#            pr = 'trade key 3 updated, no Amendment'
#            FConfirmationGeneral.log(5, pr)
#            ret = 0
#    else:
#    This case below corresponds to the use of the correct trade functionality
#        trade = message.mbf_find_object('+TRADE')
#        if trade:
#            trdnbr_obj = trade.mbf_find_object('TRDNBR')
#            if trdnbr_obj:
#                trdnbr = trdnbr_obj.mbf_get_value()
#                trade = ael.Trade[int(trdnbr)]
#                if FConfirmationGeneral.trade_is_correction(trade):
#                    corr = trade.correction_trdnbr
#                    if corr.optkey3_chlnbr != trade.optkey3_chlnbr:
#                        pr = 'trade key 3 updated, no Amendment'
#                        FConfirmationGeneral.log(3, pr)
#                        ret = 0
#
#    Example, don't generate amendment if status is set to Terminated
#        status_obj = trade.mbf_find_object('STATUS')
#        status_update_obj = trade.mbf_find_object('!STATUS')
#        if status_obj and status_update_obj:
#            status = status_obj.mbf_get_value()
#            if status == 'Terminated':
#                pr = 'status Terminated, no Amendment'
#                FConfirmationGeneral.log(5, pr)
#                ret = 0
    return ret


def is_amendment_extend(message):
    ''' This function is called after the core confirmation scripts has
    classified the message as not representing an Amendment event.  This can
    be overridden by returning 1 from this function, i.e. if this function
    returns 1 an Amendment confirmation will be generated.

    The message input parameter can represent either a trade, instrument,
    party or contact entiry. '''
    FConfirmationGeneral.log_trace()

    ret = 0
#    Example, generate amendment if external id updated:
#    trade = message.mbf_find_object('!TRADE')
#    if trade:
#        externid_obj = trade.mbf_find_object('!OPTIONAL_KEY')
#        if externid_obj:
#            pr = 'external id updated, generate Amendment'
#            FConfirmationGeneral.log(5, pr)
#            ret = 1
    return ret


def is_cancellation_restrict(message):
    ''' This function is called after the core confirmation scripts has
    classified the message as representing a Cancellation event.  This can
    be overridden by returning 0 from this function, i.e. if this function
    returns 0 no Cancellation confirmation will be generated.'''
    FConfirmationGeneral.log_trace()

    ret = 1
    return ret


def is_cancellation_extend(message):
    ''' This function is called after the core confirmation scripts has
    classified the message as not representing a Cancellation event.  This can
    be overridden by returning 1 from this function, i.e. if this function
    returns 1 a Cancellation confirmation will be generated.'''
    FConfirmationGeneral.log_trace()
    
    ret = 0
    return ret
