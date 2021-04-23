""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementAMBAHook - Module that is executed as AEL hook in AMBA

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module is used as an AEL Hook that extends/modifies outgoing as
    well as incoming Settlement AMBA messages. Check the flag
    ael_module_name in the AMBA ini-file for more information.

DATA-PREP
    Note that this file includes variables that are not available
    in FSettlementfVariablesTemplate so you need to configure them in
    this file. After customisation rename the file from
    FSettlementAMBAHookTemp to FSettlementAMBAHook.

    Before starting AMBA verify that all variables are correct because
    FSettlement72 is using this module and vice versa. Note that if
    any further changes are done in this module running AMBA needs to be
    restarted in order to reload the hook.

REFERENCES
    Swift Connectivity Mapping - SCM version 8
    FCA 2105 describes how to incorporate this module with the
    MessageAdaptations

----------------------------------------------------------------------------"""
import ael, amb
# Customerspecific variables, to be edited

# DROP_FIELDS functionality defines which fields KMaster should ignore.
# Only optional fields are allowed.
# Every non free text message type (MT) has it's own drop list
# When for 103 option 'A', if '50A_acc' is present, then account
# will be dropped. Other similar keywords are 50A_acc, 56A_acc, 56D_acc

DROP_FIELDS_103 = ['51', '52', '54']
DROP_FIELDS_202 = ['51', '52', '54']
DROP_FIELDS_210 = ['50']

# Country Codes for countries, which has implemented
# SWIFT TARGET II, the country code mentioned in 5 and 6th
# character will be matched against the dictionary.
# The European Countries for which SWIFT Target need to
# implementated will be included in below list. The message constructed
# for such field will be in new manner i.e. with 'SWIFT_SERVICE_CODE'.

COUNTRY_CODES = [] #['SE', 'US', 'CM', 'JP']

# This field is added to handle SWIFT Target-II implementation.
# The value the code for financial servies used by bank. This
# field is  added to those message which is as a part of SWIFT Target II
# implementation.

SWIFT_SERVICE_CODE = 'TGT'

# This is field 72 tag for MT 103/202 which
# can be customized by Client using value '/ACC/' or
# '/INS/' or '/INT/' or '/INS/'.
# Note : Any of the above mentioned value is compulsory to be
#        prefixed for 72 tag.

PRE_SENDER_TO_RECEIVER_INFO_103 = ''

PRE_SENDER_TO_RECEIVER_INFO = ''

# This field is added to handle the priority bank
# from client perpective.

BANKING_PRIORITY = 'NYNN'

# RESOURCES, this must represented in the the AMBA ini file
# the flag is called -receiver_sources {KMS,INTERPAY}
# where KMS is used for SWIFT/KMaster and INTERPAY for Internal payments
RESOURCES = ['KMS', 'INTERPAY', 'SWIFT']

# State seperator for functions that derive data from different fields
# for example FSettlement72.descr(setl, separator)
# note that all of these functions implement remove_last_separator
FIELD72_SEPARATOR = '|'

# Core STP of Settlement Manager and Scripts requires party account
# If this toggle is true check is done if party account is not set
# then KMaster will not use party account in field 58A of MT 202
FOOL_CORESTP = 1

# Default value of account (accnbr) that otherwise would have been empty.
# Since Core STP rules do not allow this, FOOL_CORESTP_ACCOUNT represents
# default value for example FOOL_CORESTP_ACCOUNT=0
# Field 58 of MT 202 will not be populated if party_account is
# equeal FOOL_CORESTP_ACCOUNT
FOOL_CORESTP_ACCOUNT = '0'

# Variables for e-mail notifications, to be edited before use
# default = 0, means no e-mail notifications
SENDMAIL = 0

# E-mail address to be sent to (define e-mail groups on e-mail
#  server for multiple receivers)
EMAIL_RECEIVER = 'info@bank.com'

# Subject
SUBJECT = 'SWIFT-interface answer: Settlement'

# Message added to current message info (see function sendm_mail)
MESSAGE = 'Check the result in the Settlement Manager.'

# Settlement fields to be validated
validate_non_swift_chars = ['ACQUIRER_ACCNAME', 'ACQUIRER_ACCOUNT', \
'ACQUIRER_PTYID', 'PARTY_ACCNAME', 'PARTY_ACCOUNT', 'PARTY_PTYID', 'TEXT']

# This variable will work as switch for creation of MT 210 and default value
# will be 'False'.

CREATE_MT210 = False

## Options can be defined here ##
OPTIONS = {}

# MT103: ORDERING_CUSTOMER field 50, INTERMEDIARY field 56
# Option F is not supported for ORDERING_CUSTOMER in MT103
# Option C is not supported for INTERMEDIARY in MT103
OPTIONS[103] = {'ORDERING_CUSTOMER':'A', 'INTERMEDIARY':'A'}

# MT202: INTERMEDIARY field 56
OPTIONS[202] = {'INTERMEDIARY':'A'}

# MT210: # ORDERING_CUSTOMER field 50, ORDERING_INSTITUTION field 52, INTERMEDIARY field 56
OPTIONS[210] = {'ORDERING_CUSTOMER':'A', 'ORDERING_INSTITUTION':'A', \
                'INTERMEDIARY':'A'}


#DO NOT EDIT AFTER THIS LINE
# IF YOU DO FCS CAN SUPPORT YOUR CODE
import FSettlement72, FSettlementParams
settlement_params = FSettlementParams.get_default_params()

"""aef-------------------------------------------------------------------------
hook::add_swift_tag

Module:**FSettlementAMBAHook**

FSettlementAMBAHook is a part of the Settlement script package.

Hook function **add_swift_tag** is a part of FSettlementAMBAHook and is used for
populating outgoing AMBA settlement messages. In order to be called as a
sender AMBA hook, the name of this function needs to be stated in the AMBA
ini file as an 'ael_sender_add'.

@category AMBA
@param e:ael_entity An entity - function only handles Settlement
@param op:string Database event such as 'Update', 'Insert' or 'Delete'
@return tuple List that includes added fields. Note that if the List is not
returned, no AMBA message will be sent.
----------------------------------------------------------------------------"""
def add_swift_tag(e, op):
    'The name of this function responds the one stated as \
    -ael_sender_add in the AMBA ini-file.\
    Note that if you are using MessageAdaptation hook then\
    you need to configure it to run this function. For more\
    information see FCA 2105'

    lst = []
    update_status_add = ['Released']
    swift_message_type = ''
    COUNTRY_CODE = ''
    if e:
        if e.record_type == 'Settlement':
            if op == "Update" and e.status in update_status_add and not \
            e.post_settle_action:
                # post settle action not to be sent out
                coresp = None
                setl = e
                ##############################################################
                ########  Varibles defined for field 'SWIFT_MESSAGE_TYPE' ####
                ##############################################################

                SENDER_BIC = ''
                RECEIVER_BIC = ''
                PARTY_BIC = ''
                ACCOUNT_WITH_INSTITUTION = ''
                ACCOUNT_WITH_INSTITUTION_BIC = ''
                AMOUNT_ROUNDED = ''
                NETWORK = ''
                PARTY_TYPE = ''
                VALUE_DAY_SWIFT = ''
                BANK_OPERATION_CODE = ''

                ##############################################################

                senders_corresponding_bic_flag = ''
                senders_corresponding_bic_acq  = ''
                swift_service_code = ''
                cp_bic_code = ''
                inter_bic_flag = 0
                inter_bic_exists = 0

                acc = None
                acq = ael.Party[setl.acquirer_ptyid]
                if acq:
                    acc = get_account(setl, 0)
                    if acc:
                        coresp = acc.correspondent_bank_ptynbr

                # Creation of MT 210 , message sending rules for MT210  ##
                #---- Starts---.#
                if is_mt_210(setl, coresp):
                    #   field 20, TRANS_REF  #
                    trans_ref = get_trans_ref(setl)
                    lst.append(['TRANS_REF', trans_ref])
    
                    #   field 25, ACCOUNT_ID #
                    if setl.acquirer_account:
                        lst.append(['ACCOUNT_ID', setl.acquirer_account])
    
                    # feild 21, RELATED_REF#
                    # For NRW, the value is 'NONREF' #
                    lst.append(['RELATED_REF', 'NONREF'])
    
                    # field 50A, ORDERING_CUSTOMER#
    
                    cust = get_ordering_customer(setl)
                    lst.append(['ORDERING_CUSTOMER', cust])
    
                    # field 52A, ORDERING_INSTITUTION #
    
                    inst = get_ordering_institution(setl)
                    lst.append(['ORDERING_INSTITUTION', inst])
    
                    # field 56A, INTERMEDIARY #
    
                    intermediary = get_intermediary210(setl)
                    lst.append(['INTERMEDIARY', intermediary])
    
                    message = prepare_drop_fields(FSettlement72.\
                                drop_override(setl, DROP_FIELDS_210))
                    lst.append(["DROP_FIELDS_210", message])
    
                    swift_message_type = '210'
                    lst.append(["SWIFT_MESSAGE_TYPE", swift_message_type])

                    # Creation of MT 210 , message sending rules for  ###
                    #  MT210----ends-----.###     

                if acc and coresp and not swift_message_type :
                    code = get_partyalias(coresp, acc, 1)
                    country_code = ''

                    ################ SWIFT TARGET II Code #############
                    # If curr is not EURO , then our corres BIC      ##
                    if country_code not in COUNTRY_CODES \
                        and not COUNTRY_CODES:
                        lst.append(["SENDERS_CORRESPONDENT_BIC", code])
                    senders_corresponding_bic_acq = code
                    if country_code not in COUNTRY_CODES and \
                        setl.curr.insid and \
                        setl.curr.insid.strip() != 'EUR'and \
                        senders_corresponding_bic_acq != '':
                        if ["SENDERS_CORRESPONDENT_BIC", \
                            senders_corresponding_bic_acq] not in lst:
                            lst.append(["SENDERS_CORRESPONDENT_BIC", \
                                       senders_corresponding_bic_acq])

                    #################################################
                    #53a #changed in mapping version 8
                    lst.append(["SENDERS_CORRESPONDENT", \
                    FSettlement72.get_senders_correspondent(setl)])

                SENDER_BIC = get_sender_bic(setl)
                lst.append(["SENDER_BIC", SENDER_BIC])
                code = get_partyalias(coresp, acc, 1)
                # what if more then one swift alias
                RECEIVER_BIC = code
                lst.append(["RECEIVER_BIC", RECEIVER_BIC])

                # MT210, notification
                notify = 'False'
                if coresp.notify_receipt:
                    notify = 'True'
                    lst.append(["SEND_NOTIFICATION_OF_RECIEPT", \
                               FSettlement72.validate(notify)])

                cp = ael.Party[setl.party_ptyid]
                if cp:
                    # 58A MT 202, together with ACCOUNT_WITH_INSTITUTION
                    # in logic for 103 togheter with client type

                    PARTY_BIC = FSettlement72.validate(cp.swift)
                    lst.append(["PARTY_BIC", PARTY_BIC])

                    PARTY_TYPE = FSettlement72.validate(str(cp.type))
                    lst.append(["PARTY_TYPE", PARTY_TYPE])

                    acc = get_account(setl, 1)

                    if acc and not swift_message_type:
                        cores = acc.correspondent_bank_ptynbr
                        if cores:
                            cp_country_code = ''
                            inter_bic_code = ''

                            intermediary = acc.correspondent_bank2_ptynbr
                            if intermediary:
                                inter_bic_code = get_partyalias(intermediary, \
                                                                acc, 2)

                            #57A MT 103, 202 (and 54A of MT 103)
                            cp_bic_code = get_partyalias(cores, acc, 1)

                            ACCOUNT_WITH_INSTITUTION_BIC = cp_bic_code
                            lst.append(["ACCOUNT_WITH_INSTITUTION_BIC", \
                                        ACCOUNT_WITH_INSTITUTION_BIC])

                            if inter_bic_code and inter_bic_code != '' and \
                               len(inter_bic_code) > 6 :
                                #### When intermediary present ####
                                cp_country_code = inter_bic_code[4]+ \
                                                  inter_bic_code[5]
                                if (cp_country_code in COUNTRY_CODES) and \
                                    len(COUNTRY_CODES) > 0:
                                    COUNTRY_CODE = cp_country_code
                                if len(COUNTRY_CODES) > 0 and COUNTRY_CODES:
                                    swift_service_code = SWIFT_SERVICE_CODE
                                    inter_bic_flag = 1
                            elif len(cp_bic_code) > 6 :
                                #### When intermediary not present, then ####
                                #### counterparty correspondent BIC      ####
                                cp_country_code = cp_bic_code[4]+cp_bic_code[5]
                                if len(COUNTRY_CODES) > 0 and COUNTRY_CODES:
                                    swift_service_code = SWIFT_SERVICE_CODE
                                if cp_country_code in COUNTRY_CODES :
                                    COUNTRY_CODE = cp_country_code

                            ################ SWIFT TARGET II #################
                            ####  If the curr is EURO, then there corres BIC #
                            if setl.curr.insid and \
                            setl.curr.insid.strip() == 'EUR' :
                                if swift_service_code:
                                    senders_corresponding_bic_flag = \
                                        cp_bic_code

                            #58A MT 202, together with PARTY_BIC
                            if setl.party_account != FOOL_CORESTP_ACCOUNT:
                                # Ordinary account
                                ACCOUNT_WITH_INSTITUTION = FSettlement72.\
                                                 validate(setl.party_account)
                                lst.append(["ACCOUNT_WITH_INSTITUTION", \
                                   ACCOUNT_WITH_INSTITUTION])
                            elif FOOL_CORESTP:
                                # not valid account, KMaster should ignore it
                                ACCOUNT_WITH_INSTITUTION = ''
                                lst.append(["ACCOUNT_WITH_INSTITUTION", \
                                             ACCOUNT_WITH_INSTITUTION])
                                lst.append(["FOOL_CORESTP", '1'])
                            else:
                                # inspite of not valid account
                                ACCOUNT_WITH_INSTITUTION = FSettlement72.\
                                                   validate(setl.party_account)
                                lst.append(["ACCOUNT_WITH_INSTITUTION", \
                                    ACCOUNT_WITH_INSTITUTION])

                        intermediary = acc.correspondent_bank2_ptynbr
                        if intermediary:
                            code = get_partyalias(intermediary, acc, 2)
                            #56A MT 202, MT 103 56A (old way, INTERMEDIARY_BIC not used)
                            # ALERT, many aliases!
                            lst.append(["INTERMEDIARY_BIC", code])

                            #57A MT 202
                            acc2 = ''
                            if acc.account2:
                                acc2 = str(acc.account2)
                            lst.append(["INTERMEDIARY_ACCOUNT", \
                                       FSettlement72.validate(acc2)])

                # network type flag descides wheter to sent to swift or not!!!
                networktype = get_networktype(setl)
                direction = 'PAY'
                if setl.amount >= 0:
                    direction = 'REC'
                    if networktype == 'SWIFT':
                        if swift_message_type == '':
                            networktype = ''
                       #ael.log('Receives are not to be sent to SWIFT')
                        NETWORK = FSettlement72.validate(networktype)
                        lst.append(["NETWORK", NETWORK])
                else:
                    NETWORK = FSettlement72.validate(networktype)
                    lst.append(["NETWORK", NETWORK])

                lst.append(["DIRECTION", direction])

                tr = setl.trdnbr
                settleid = ''
                if tr:
                    ssi = None
                    if ssi:
                        settleid = str(ssi.settleid)
                lst.append(["SSI", FSettlement72.validate(settleid)])

                # see get_narrative_199 that collects all info
                #lst.append(["SETTLE_SEQNBR.VALUE_DAY",vd])
                #should be rounded per currency
                #lst.append(["AMOUNT_OLD",old_amount])

                #32A of MT 103, 202
                date_format = ael.date_today().to_string('%Y-%m-%d')
                if setl.value_day:
                    date_format = setl.value_day.to_string('%Y-%m-%d')
                VALUE_DAY_SWIFT = FSettlement72.validate(date_format)
                lst.append(["VALUE_DAY_SWIFT", VALUE_DAY_SWIFT])

                #for backward compatibility only
                lst.append(["SWIFT_LOOPBACK", '0'])

                #rounding spr 249648
                #MT 103 Fields 32A, 33B MT 202 field 32A
                AMOUNT_ROUNDED = FSettlement72.round_amount(e)
                lst.append(["AMOUNT_ROUNDED", AMOUNT_ROUNDED])

                #MT 103 Field 59 PARTY_FULLNAME, PARTY_ADDRESS
                lst.append(["PARTY_FULLNAME", FSettlement72.cp_fullname\
                           (e, FSettlement72.FULLNAME)])
                lst.append(["PARTY_ADDRESS", FSettlement72.cp_address(e)])
                #Following fields are used in the KMASTER logic
                #53A ACQUIRER_ACCOUNT
                #DELIVERY_TYPE
                #TYPE
                #SETTLE_CATEGORY

                #21
                #YOUR_REF, 16 chars, cp_ref
                if not swift_message_type:
                    your_ref = FSettlement72.get_your_ref(setl)
                    lst.append(["YOUR_REF", your_ref])

                    #MT 202 field 72
                    #MT 103 field 72

                    message = FSettlement72.descr72_202(setl, FIELD72_SEPARATOR)
                    if message.strip() != '':
                        message = PRE_SENDER_TO_RECEIVER_INFO+message
                    lst.append(["SENDER_TO_RECEIVER_INFO", message])

                    message = ''
                    message = FSettlement72.descr72_103(setl, FIELD72_SEPARATOR)
                    if message.strip() != '' :
                        message = PRE_SENDER_TO_RECEIVER_INFO_103+message
                    lst.append(["SENDER_TO_RECEIVER_INFO_103", message])

                    #MT103 field 23B
                    BANK_OPERATION_CODE = FSettlement72.\
                                      get_bank_operation_code(setl)
                    lst.append(["BANK_OPERATION_CODE", BANK_OPERATION_CODE])

                    #MT103 field 23E
                    lst.append(["INSTRUCTION_CODE", FSettlement72.\
                               get_instruction_code(setl)])
                    #MT103 field 71A
                    lst.append(["DETAILS_OF_CHARGES", FSettlement72.\
                               get_details_of_charges(setl)])
                    #MT103 field 70
                    lst.append(["REMITTANCE_INFO", FSettlement72.\
                              get_remittance_info(setl)])

                    #MT199 field 79
                    message = ''
                    message = FSettlement72.get_narrative199\
                              (setl, 0, FIELD72_SEPARATOR)
                    lst.append(["NARRATIVE199", message])
                    #MT299 field 79
                    message = ''
                    message = FSettlement72.get_narrative299\
                              (setl, 0, FIELD72_SEPARATOR)
                    lst.append(["NARRATIVE299", message])
                    #MT103
                    message = prepare_drop_fields(FSettlement72.\
                              drop_override(setl, DROP_FIELDS_103))
                    lst.append(["DROP_FIELDS_103", message])
                    #MT202
                    message = prepare_drop_fields(FSettlement72.\
                              drop_override(setl, DROP_FIELDS_202))
                    lst.append(["DROP_FIELDS_202", message])


                    ########################################################
                    ## Addition of field 'SWIFT_MESSAGE_TYPE' to message ###
                    ########################################################

                    MT202_ok = 1
                    MT299_ok = 0
                    MT103_ok = 1
                    MT199_ok = 0

                    swift_message_type = ''
                    self_trading = 0
                    validation103_ok = 1
                    validation202_ok = 1

                    if not (setl.type != 'Security Nominal'):
                        MT202_ok = 0
                        MT103_ok = 0

                    if not (setl.delivery_type != 'Delivery versus Payment'):
                        MT202_ok = 0
                        MT103_ok = 0

                    if not((SENDER_BIC != ACCOUNT_WITH_INSTITUTION_BIC) and \
                         (setl.acquirer_account != ACCOUNT_WITH_INSTITUTION)):
                        self_trading = 1
                        if not(setl.acquirer_account != \
                               ACCOUNT_WITH_INSTITUTION):
                            MT202_ok = 0
                            MT103_ok = 0
                            if self_trading :
                                MT202_ok = 1
                                MT103_ok = 1

                    if (setl.settle_category == 'Good Value'):
                        MT299_ok = 1
                        MT199_ok = 1

                    if not(PARTY_TYPE == 'Counterparty' or \
                        (PARTY_TYPE == 'Broker' and PARTY_BIC!='')):
                        MT202_ok = 0

                    if not(PARTY_TYPE == 'Client' or \
                        (PARTY_TYPE == 'Broker' and PARTY_BIC=='')):
                        MT103_ok = 0

                    if not(setl.amount < 0):
                        MT202_ok = 0
                        MT103_ok = 0

                    if not(NETWORK == 'SWIFT'):
                        MT202_ok = 0
                        MT103_ok = 0

                    if NETWORK == '' :
                        validation103_ok = 0
                        validation202_ok = 0

                    if SENDER_BIC == '':
                        validation103_ok = 0
                        validation202_ok = 0

                    if RECEIVER_BIC == '':
                        validation103_ok = 0
                        validation202_ok = 0

                    if PARTY_BIC == '':
                        validation202_ok = 0

                    if AMOUNT_ROUNDED == '':
                        validation103_ok = 0
                        validation202_ok = 0

                    if PARTY_TYPE == '':
                        validation103_ok = 0
                        validation202_ok = 0

                    if VALUE_DAY_SWIFT == '':
                        validation103_ok = 0
                        validation202_ok = 0

                    if BANK_OPERATION_CODE == '':
                        validation103_ok = 0

                    if MT103_ok and validation103_ok :
                        swift_message_type = '103'
                        if MT199_ok:
                            swift_message_type = '103'
                    if MT202_ok and validation202_ok:
                        swift_message_type = '202'
                        if MT299_ok:
                            swift_message_type = '202'

                    # 'SWIFT_MESSAGE_TYPE' is added only for MT 103 and MT 202#
                    #### not for MT 199 and MT299.                           ##
                    if (MT103_ok and validation103_ok and not MT199_ok) or \
                       (MT202_ok and validation202_ok and not MT299_ok):
                        if COUNTRY_CODES and len(COUNTRY_CODES) > 0 and \
                           setl.curr.insid and \
                           setl.curr.insid.strip() == 'EUR' and\
                           swift_service_code:
                            lst.append(["SWIFT_SERVICE_CODE", \
                                        swift_service_code])
                            lst.append(["BANKING_PRIORITY", \
                                        BANKING_PRIORITY])
                        if inter_bic_exists and inter_bic_flag:
                            if senders_corresponding_bic_flag != '':
                                lst.append(["SENDERS_CORRESPONDENT_BIC", \
                                          senders_corresponding_bic_flag])

                        elif inter_bic_exists and not inter_bic_flag:
                            if senders_corresponding_bic_acq != '':
                                if ["SENDERS_CORRESPONDENT_BIC", \
                                    senders_corresponding_bic_acq] not in lst:
                                    lst.append(["SENDERS_CORRESPONDENT_BIC", \
                                    senders_corresponding_bic_acq])

                        else:
                            if senders_corresponding_bic_flag != '':
                                lst.append(["SENDERS_CORRESPONDENT_BIC", \
                                senders_corresponding_bic_flag])
                    else:
                        if senders_corresponding_bic_acq != '':
                            if ["SENDERS_CORRESPONDENT_BIC", \
                            senders_corresponding_bic_acq] not in lst:
                                lst.append(["SENDERS_CORRESPONDENT_BIC", \
                                senders_corresponding_bic_acq])
                    if MT103_ok and validation103_ok: 
                        lst.append(["ORDERING_CUSTOMER", get_ordering_customer(setl)] )
                    lst.append(["SWIFT_MESSAGE_TYPE", swift_message_type])
                    if COUNTRY_CODE and setl.curr.insid and  \
                    setl.curr.insid.strip() == 'EUR':
                        lst.append(["COUNTRY_CODE", COUNTRY_CODE])

                if (swift_message_type == '103' or swift_message_type == '202'):
                    lst.append(["INTERMEDIARY", get_intermediary(setl, swift_message_type)])
                    lst.append(['INTERMEDIARY2', get_intermediary2(setl, swift_message_type)])
                    lst.append(['INTERMEDIARY3', get_intermediary3(setl, swift_message_type)])
                    lst.append(['INTERMEDIARY4', get_intermediary4(setl, swift_message_type)])
                    ########  Code for 'SWIFT_MESSAGE_TYPE' ends here #####
    elif op == "Update" and e.status in update_status_add and \
        e.post_settle_action:
        ael.log('FSettlementAMBAHook catched settlement update but')
        ael.log('no additional SWIFT tags are appended when it is'\
                'post settle action')

    return lst


"""aef-------------------------------------------------------------------------
hook::modify_sender

Module:**FSettlementAMBAHook**

FSettlementAMBAHook is a part of the Settlement script package.

Hook function **modify_sender** is a part of FSettlementAMBAHook and is used for
changing certain fields in the outgoing AMBA messages.
In order to be called as a modify sender AMBA hook, the name of this
function needs to be stated in the AMBA ini file as an 'ael_sender_modify'.

@category AMBA
@param m:AMB_MESSAGE A message in the AMB format.
@param s:string Subject of the message
@return tuple List that includes the message and the subject.
----------------------------------------------------------------------------"""
def modify_sender(m, s):

    result = (m, s)
    type_obj = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    type_value = type_obj.mbf_get_value() 
    if type_value == 'UPDATE_SETTLEMENT':
        result = modify_swift_sender(m, s)
    elif type_value in ['INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT']:
        result = modify_instrument_message(m, s)
    return result


"""aef-------------------------------------------------------------------------
hook::modify_swift_sender

Module:**FSettlementAMBAHook**

FSettlementAMBAHook is a part of the Settlement script package.

Hook function **modify_swift_sender** is a part of FSettlementAMBAHook and is used for
changing certain fields in the outgoing AMBA settlement messages.
In order to be called as a modify sender AMBA hook, the name of this
function needs to be stated in the AMBA ini file as an 'ael_sender_modify'.

Note that this function should be used if you want to replace non swift characters
with the supported ones (see SPR 270241).

@category AMBA
@param m:AMB_MESSAGE A message in the AMB format.
@param s:string Subject of the message (not used for SWIFT purposes)
@return tuple List that includes the message and the subject.
----------------------------------------------------------------------------"""
def modify_swift_sender(m, s):
    '''The name of this function responds the one stated as
    -ael_sender_modify in the AMBA ini-file.
    Note that if you are using MessageAdaptation hook then
    you need to configure it to run this function. For more
    information see FCA 2105.
    '''

    o1 = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if o1.mbf_get_value() in ['UPDATE_SETTLEMENT']:
        o2 = m.mbf_find_object('!SETTLEMENT', 'MBFE_BEGINNING')
        if not o2:
            o2 = m.mbf_find_object('SETTLEMENT', 'MBFE_BEGINNING')
        if o2:
            o3 = o2.mbf_find_object('STATUS', 'MBFE_BEGINNING')
            o4 = o2.mbf_find_object('!STATUS', 'MBFE_BEGINNING')
            if o3 and o4:
                new_status = o3.mbf_get_value()
                old_status = o4.mbf_get_value()
                if old_status == 'Authorised' and new_status == 'Released':
                    # status changed from authorised to released
                    for field in validate_non_swift_chars:
                        ff = o2.mbf_find_object(field, 'MBFE_BEGINNING')
                        if ff:
                            ret = FSettlement72.validate(ff.mbf_get_value())
                            o2.mbf_replace_string(field, ret)

            if o3 and not o4:
                # Make sure to change show_changes in amba ini to 1, if it for SWIFT.
                # released settlement still released, settl is however changed
                # send empty network
                if o3.mbf_get_value() == 'Released':
                    o5 = o2.mbf_find_object('NETWORK', 'MBFE_BEGINNING')
                    if o5:
                        # check on SWIFT migth be done if more then one network
                        o2.mbf_replace_string('NETWORK', '')
                        ael.log("NETWORK emptied, SWIFT message sending prevented")
    return (m, s)

"""----------------------------------------------------------------------------
modify_instrument_message

This function is called by the modify_sender hook.
It modifies instrument AMBA messages by removing cash flows whose pay day are
not within the time window specified in FSettlementVariables.
It also removes cash flows that have additional infos matching the ones
specified in the cash_flow_additional_infos variable in FSettlementVariables.

Also, only messages for instruments listed in valid_instrument_types in 
FSettlementVariables are sent to the AMB.
----------------------------------------------------------------------------"""
def modify_instrument_message(m, s):
    instrument_obj = object_by_name(m, ['', '+', '!'], 'INSTRUMENT')
    if message_can_be_skipped(instrument_obj):
        return
    for leg_obj in objects_by_name(instrument_obj, ['', '+', '!'], 'LEG'):
        currency_obj = leg_obj.mbf_find_object('CURR.INSID')
        if currency_obj:
            currency = currency_obj.mbf_get_value()
            for cash_flow_obj in objects_by_name(leg_obj, ['', '+'], 'CASHFLOW'):
                if cash_flow_can_be_removed_from_message(cash_flow_obj, currency):
                    leg_obj.mbf_remove_object()
    return (m, s)

"""aef-------------------------------------------------------------------------
hook::modify_swift_receiver

Module:**FSettlementAMBAHook**

FSettlementAMBAHook is a part of the Settlement script package.

Hook function **modify_swift_receiver** is a part of FSettlementAMBAHook and is used for
filtering of incoming AMBA settlement messages. In order to be called
as a modify receiver AMBA hook the name of this function needs to be stated
in the AMBA ini file as an 'ael_receiver_modify'.

Note that this function will not execute messages sent by other sources
then those that are defined within the variable 'FSettlementAMBAHook.RESOURCES'.

@category AMBA
@param m:AMB_MESSAGE A message in the AMB format.
@return tuple List that includes the message.
----------------------------------------------------------------------------"""
def modify_swift_receiver(m):
    'This function responds the one that is stated as \
    -ael_receiver_modify in the AMBA ini-file. Note that\
    this function will not execute messages sent on some\
    other source then RESOURCES (see defined variables above).\
    Note that if you are using MessageAdaptation hook then\
    you need to configure it to run this function. For more\
    information see FCA 2105.'

    source = ''
    sourceOK = 0

    o1 = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if o1.mbf_get_value() not in ['UPDATE_SETTLEMENT']:
        return (m)
    else:
        s = m.mbf_find_object('SOURCE')
        if s:
            source = s.mbf_get_value()
            if source in RESOURCES:
                sourceOK = 1
        # SWIFT interface is sending updates to AMBA
        # if not proper source then do not proceede
        if sourceOK == 0:
            return


        # Note that AMBA might send no event prefix
        o2 = m.mbf_find_object('!SETTLEMENT', 'MBFE_BEGINNING')
        if not o2:
            o2 = m.mbf_find_object('SETTLEMENT', 'MBFE_BEGINNING')

        if o2:
            o3 = o2.mbf_find_object('SEQNBR', 'MBFE_BEGINNING')
            if o3:
                seqnbr = o3.mbf_get_value()
                if seqnbr:
                    pr = 'Dealing with incoming Settlement %s' % (seqnbr)
                    ael.log(pr)

                    o4 = o2.mbf_find_object('STATUS', 'MBFE_BEGINNING')
                    if o4:
                        status = o4.mbf_get_value()
                        if status:
                            if status in ['Acknowledged', 'Not Acknowledged']:
                                pr = 'SWIFT-interface answered with a  new '\
                                'settlement status %s:\n Commit will be done.' \
                                      % (status)
                                ael.log(pr)
                                send_email(seqnbr, pr)
                                setl = ael.Settlement[int(seqnbr)]
                                ok = 1
                                if not setl:
                                    ok = 0
                                elif setl.status != 'Released':
                                    pr = 'Settlement %d status not Released'\
                                         '(%s)'  % (int(seqnbr), setl.status)
                                    ael.log(pr)
                                    ok = 0

                                if ok:
                                    clone = setl.clone()
                                    clone.status = status
                                    add_diary(clone, o2)
                                    clone.commit()
                            else:
                                pr = 'SWIFT-interface answered with wrong '\
                                'status %s. Nothing will be committed to the' \
                                'database.' % (status)
                                ael.log(pr)
                                send_email(seqnbr, pr)
                        else:
                            pr = 'No settlement status in the respond from the'\
                            'SWIFT-interface. Nothing will be committed to the'\
                            'database.' % (status)
                            ael.log(pr)
                            send_email(seqnbr, pr)

    return


def get_partyalias(pty,acc,mode=1,*rest):
    '''Retrieve the BIC for the account.
    Mode = 1 returns Correspondent (bic_seqnbr)
    Mode = 2 returns Intermediary 1 (bic2_seqnbr)
    Mode = 3 returns Intermediary 2 (bic3_seqnbr)
    Mode = 4 returns Intermediary 3 (bic4_seqnbr)
    Mode = 5 returns Intermediary 4 (bic5_seqnbr)
    '''
    alias = ''
    if mode == 1 and acc.bic_seqnbr:
        alias = acc.bic_seqnbr.alias
    elif mode == 2 and acc.bic2_seqnbr:
        alias = acc.bic2_seqnbr.alias
    elif mode == 3 and acc.bic3_seqnbr:
        alias = acc.bic3_seqnbr.alias
    elif mode == 4 and acc.bic4_seqnbr:
        alias = acc.bic4_seqnbr.alias
    elif mode == 5 and acc.bic5_seqnbr:
        alias = acc.bic5_seqnbr.alias
        
    return FSettlement72.validate(alias)


def get_networktype(setl,*rest):
    'Acquirers account descides which network to send on.'

    networktype = ''
    if setl:
        p = ael.Party[setl.acquirer_ptyid]
    if not p and setl:
        pr = 'Settlement %d: No network type, party not stated' % (setl.seqnbr)
        ael.log(pr)

    acc = get_account(setl, 0) # 0 = acquirer, 1 = cp
    if acc:
        if not acc.network_alias_type:
            pr = 'Account %s (Party:%s) has no network connected to it.' % \
                (acc.name, acc.ptynbr.ptyid)
            ael.log(pr)
        else:
            for i in p.aliases():
                if acc.network_alias_type == i.type:
                    networktype = i.type.alias_type_name
                    break

            if networktype == '':
                pr = 'Party %s has not Alias for %s' % (acc.ptynbr.ptyid, \
                      acc.network_alias_type.alias_type_name)
                ael.log(pr)

    elif setl:
        pr = 'Settlement %d, No network type, account not stated' % \
             (setl.seqnbr)
        ael.log(pr)

    return FSettlement72.validate(networktype)


def get_account(setl,mode=0,*rest):
    'Returns account entity, if mode=0 acquirer else counterparty account'
    acc = None
    accname = ''
    pty = None
    ptynbr = 0

    if mode == 0:
        #acquirer
        accname = setl.acquirer_accname
        pty = ael.Party[setl.acquirer_ptyid]
        if pty:
            ptynbr = pty.ptynbr
    else:
        #party
        accname = setl.party_accname
        pty = ael.Party[setl.party_ptyid]
        if pty:
            ptynbr = pty.ptynbr

    if ptynbr and accname:
        acc = ael.Account.read("ptynbr=%d and name='%s'" % \
                                    (ptynbr, accname))
        if not acc:
            pr = 'get_account: no account found (%s,%s)' % (pty.ptyid, accname)
            ael.log(pr)
    # validate not needed here
    return acc

def is_net(setl,*rest):
    'Checks if a settlement record is result of netting.'
    net = 0
    if setl:
        if setl.ref_type=='Ad_hoc Net' or setl.ref_type=='Net':
            net = 1
    #validate not needed here
    return net


def least_net_trdnbr(net,mode=0,*rest):
    'Returns the least trade number of netted settlements if mode\
    is zero. If mode is 1 trade entity with least number is returned.\
    If mode is 2 settlement connected to the least trade is returned.'

    trdnbr = 0
    trade = None
    settlement = None

    if net:
        seqnbr = 0
        if net.record_type == 'Settlement' :
            seqnbr = net.seqnbr
        else:
            ael.log('least_net_trdnbr(net,mode=0): input net is not settlement')
        try:
            # netted parts
            sel = ael.Settlement.select('ref_seqnbr=%d' % seqnbr)
            for s in sel:
                if s.seqnbr != seqnbr and s.trdnbr:
                    if s.trdnbr:
                        if s.trdnbr.trdnbr > 0:
                            if s.trdnbr.trdnbr < trdnbr or (trdnbr == 0):
                                # the values are put here, mode descides
                                # what will be returned
                                trdnbr = s.trdnbr.trdnbr
                                trade = s.trdnbr
                                settlement = s
        except:
            sel = []
            ael.log('least_net_trdnbr function failed, zero retured')
    else:
        ael.log('least_net_trdnbr: no input deployed')

    if mode == 0:
        return trdnbr
    elif mode == 1:
        return trade
    else:
        return settlement


def send_email(seqnbr, info):
    'This function send e-mail to predefined receiver.\
    SENDMAIL flag is to be switched on in the beggining of the module.\
    info could be additional information from some line in the code.'

    if SENDMAIL:
        body = 'Settlement '+seqnbr+'\n'+MESSAGE+'\n'+info
        subject = SUBJECT+' '+seqnbr
        ael.sendmail(EMAIL_RECEIVER, subject, body)

def prepare_drop_fields(droplist,*rest):
    'Takes a drop list a returns fiels as a comma separated string'
    ret = ''
    if droplist:
        for f in range(len(droplist)):
            if ret=='':
                ret = droplist[f]
            else:
                ret = ret + ',' + droplist[f]

    return FSettlement72.validate(ret)

def get_sender_bic(setl,*rest):
    '''Returns SWIFT bic code of the Acquirer.'''
    ret = ''
    if setl:
        acq = ael.Party[setl.acquirer_ptyid]
        if acq:
            ret = acq.swift

    return FSettlement72.validate(ret)


def add_diary(clone, amb_msg):
    '''KMaster message includes some fields that are to be placed in the diary.
    New lines need to be taken care of...
    '''
    diary = ''
    o5 = amb_msg.mbf_find_object('SWIFT_EXPLANATION', 'MBFE_BEGINNING')
    if o5:
        d = o5.mbf_get_value()
        diary = r"SWIFT EXPLANATION: %s " % d

    o6 = amb_msg.mbf_find_object('SWIFT_MESSAGE', 'MBFE_BEGINNING')
    if o6:
        d = o6.mbf_get_value()
        d = d.replace('\\r\\n', ' ')
        d = d.replace('\\n', ' ')
        d = d.replace('rn', ' ')
        diary = r"%sSWIFT MESSAGE: %s" % (diary, d)

    if len(diary):
        clone.add_diary_note(diary)


def get_trans_ref(setl):
    ''' Function for MT 210, returns seqnbr.'''

    ret = ''
    if setl:
        ret = 'FA/'+str(setl.seqnbr)
    return ret

def is_mt_210(setl, coresp):
    ''' Return message type for MT210'''

    ret = 0
    if setl:
        if CREATE_MT210 and setl.amount > 0 and coresp:
            if setl.type not in ('Security Nominal', 'End Security', \
                'Aggregate Security', 'Aggregate Cash') and get_networktype(setl) == 'SWIFT' and coresp.notify_receipt == 1:
                ret =1
    return ret
    

def get_ordering_customer(setl):
    ''' Function for field 50 'ORDERING_CUSTOMER' for MT 210 and MT 103
        For MT 210, option '', C, and F
        For MT 103, option A, F, and K  
    '''

    ret = ''
    bic = ''
    acct = ''
    cores_bank = None
    if setl:
        acct = FSettlement72.validate(setl.acquirer_account)
        acq = ael.Party[setl.acquirer_ptyid]
        party_name = FSettlement72.validate(FSettlement72.cp_fullname(setl, FSettlement72.FULLNAME))
        party_addr = FSettlement72.validate(FSettlement72.cp_address(setl))
        if acq:
            acc = get_account(setl, 0)
            if acc :
                cores_bank = acc.correspondent_bank_ptynbr
                if cores_bank:
                    bic = get_partyalias(cores_bank, acc, 1)


    if OPTIONS.has_key(210) and OPTIONS[210].has_key('ORDERING_CUSTOMER') and \
        is_mt_210(setl, cores_bank):
        
        value = OPTIONS[210]['ORDERING_CUSTOMER']
        if value.find(',') > -1 :
            ael.log('More than one value for ORDERING_CUSTOMER option.')
            return
            
        if value == 'A' :
            if acct:
                ret = 'A/ACCT/'+ acct +'/ABIC/'+bic
            else:
                ret = 'A/ABIC/'+bic
        elif value == '' :
            if acct:
                ret = '/ACCT/'+ acct +'/ABIC/'+bic+ \
                      '/NAME/'+party_name+'/ADDR/'+party_addr
            else :
                ret = '/ABIC/'+bic+ \
                      '/NAME/'+party_name+'/ADDR/'+party_addr
        elif value == 'F':
            if acct:
                ret = 'F/ACCT/'+ acct +'/ABIC/'+bic+ \
                      '/NAME/'+party_name+'/ADDR/'+party_addr
            else :
                ret = 'F/ABIC/'+bic+ \
                      '/NAME/'+party_name+'/ADDR/'+party_addr

    elif OPTIONS.has_key(103) and OPTIONS[103].has_key('ORDERING_CUSTOMER'):
        value = OPTIONS[103]['ORDERING_CUSTOMER']
        if value.find(',') > -1 :
            ael.log('More than one value for ORDERING_CUSTOMER option.')
            return
            
        party_name = FSettlement72.validate(FSettlement72.acq_fullname(setl, \
                                            FSettlement72.FULLNAME))
        party_addr = FSettlement72.validate(FSettlement72.acq_address(setl))
        
        bic = get_sender_bic(setl)

        if value == 'A' and bic:
            if ('50A_acc' in DROP_FIELDS_103):
                ret = 'A/ABIC/'+bic
            elif acct:
                ret = 'A/ACCT/'+ acct +'/ABIC/'+bic
            else:
                ret = 'A/ABIC/'+bic            
        elif (value == 'K') and acct: 
            # Option F not supported by KMS
            # Code word NAME should include codeword ADDR
            ret = value+'/ACCT/'+ acct  + \
                  '/NAME/'+party_name+' '+party_addr

    return ret


def get_ordering_institution(setl):
    ''' Function for MT 210, returns ordering institution.'''

    ret = ''
    if OPTIONS.has_key(210) and setl:
        if OPTIONS[210].has_key('ORDERING_INSTITUTION'):
            value = OPTIONS[210]['ORDERING_INSTITUTION']
            if value.find(',') > -1 :
                ael.log('More than one value for ORDERING_INSTITUTION option.')
                return
            bic = ''
            acct = FSettlement72.validate(setl.acquirer_account)
            party_name = FSettlement72.cp_fullname(setl, FSettlement72.FULLNAME)
            party_addr = FSettlement72.cp_address(setl)
            bic = get_sender_bic(setl)
            if not bic :
                bic = 'UNWN'
            if value == 'A' :
                if acct:
                    ret = 'A/ACCT/'+ acct +'/ABIC/'+bic
                else:
                    ret = 'A/ABIC/'+bic
            elif value == 'D':
                if acct:
                    ret = 'D/ACCT/'+ acct +'/ABIC/'+bic+ \
                          '/NAME/'+party_name+'/ADDR/'+party_addr
                else :
                    ret = 'D/ABIC/'+bic+ \
                          '/NAME/'+party_name+'/ADDR/'+party_addr
            else:
                ret = ''
    return ret

def get_intermediary210(setl):
    ''' Function for MT 210, returns intermediary.'''

    ret = ''
    if OPTIONS.has_key(210) and setl:
        if OPTIONS[210].has_key('INTERMEDIARY'):
            value = OPTIONS[210]['INTERMEDIARY']
            if value.find(',') > -1 :
                ael.log('More than one value for INTERMEDIARY option.')
                return

            bic = ''
            acct = ''
            cp = ael.Party[setl.party_ptyid]
            if cp:
                acc = get_account(setl, 1)
                if acc :
                    intermediary = acc.correspondent_bank2_ptynbr
                    if intermediary:
                        bic = get_partyalias(intermediary, acc, 2)
                    if acc.account2:
                        acct = str(acc.account2)
            party_name = FSettlement72.cp_fullname(setl, FSettlement72.FULLNAME)
            party_addr = FSettlement72.cp_address(setl)
            if not bic :
                bic = 'UNWN'
            if value == 'A' :
                if acct:
                    ret = 'A/ACCT/'+ acct +'/ABIC/'+bic
                else:
                    ret = 'A/ABIC/'+bic
            elif value == 'D':
                if acct:
                    ret = 'D/ACCT/'+ acct +'/ABIC/'+bic+ \
                          '/NAME/'+party_name+'/ADDR/'+party_addr
                else :
                    ret = 'D/ABIC/'+bic+ \
                          '/NAME/'+party_name+'/ADDR/'+party_addr
            else:
                ret = ''
    return ret

def get_intermediary(setl, swift_message_type):
    
    '''This is field 56 in SWIFT.
       Returns intermediary's information as per option selected.
       Options A may use codes AT, AU, BL. More codes can
         be found in swift standards guide.
       Options C and D may use codes.
       Use swift guide to exercise different codes for option.
    '''
        
    value = ''
    ret = ''    
    party_name = ''
    party_addr = ''
    no_accA = 0
    no_accD = 0
    
    if(OPTIONS.has_key(103) or OPTIONS.has_key(202))and setl:
        if OPTIONS[103].has_key('INTERMEDIARY') or OPTIONS[202].has_key('INTERMEDIARY'):
            if swift_message_type == '103':
                value = OPTIONS[103]['INTERMEDIARY']
                no_accA = DROP_FIELDS_103.__contains__('56A_acc')
                no_accD = DROP_FIELDS_103.__contains__('56D_acc')
            elif swift_message_type == '202':
                value = OPTIONS[202]['INTERMEDIARY']
                no_accA = DROP_FIELDS_202.__contains__('56A_acc')
                no_accD = DROP_FIELDS_202.__contains__('56D_acc')

            if value.find(',') > -1 :
                ael.log('More than one value for INTERMEDIARY option.')
                return
            acct = ''
            bic = ''
            cp = ael.Party[setl.party_ptyid]
            if cp:
                acc = get_account(setl, 1)
                if acc :
                    intermediary = acc.correspondent_bank2_ptynbr
                    if intermediary:
                        bic = get_partyalias(intermediary, acc, 2)
                    if acc.account2:
                        acct = str(acc.account2)
                        party_name = FSettlement72.validate(intermediary.fullname)
                        party_addr = FSettlement72.validate(intermediary.address)

            if value == 'A' :
                if no_accA or not acct:
                    ret = 'A/ABIC/'+bic
                elif acct:
                    ret = 'A/ACCT/'+ acct +'/ABIC/'+bic

            elif value == 'C' and acct: # not supported by KMaster
                ret = 'C/ACCT/'+ acct

            elif value == 'D':
                if no_accD or not acct:
                    ret = 'D/NAME/'+party_name+' '+party_addr
                elif acct:
                    ret = 'D/ACCT/'+ acct +'/ABIC/'+bic+ \
                          '/NAME/'+party_name+' '+party_addr

        return ret


def get_intermediary2(setl, swift_message_type):
    '''
    Returns intermediary 2 information.
    '''   
    ret  = ''
    acct = ''
    bic = ''
    info = ''
    cp = ael.Party[setl.party_ptyid]
    if cp:
        acc = get_account(setl, 1)
        if acc :
            intermediary = acc.correspondent_bank3_ptynbr
            if intermediary:
                bic = get_partyalias(intermediary, acc, 3)
            if acc.account2:
                acct = str(acc.account3)
            info = get_intermediary_info(acc, 3)
            ret = 'ACCT/' + acct + '/ABIC/' + bic + '/NAME/' + info
    return ret

def get_intermediary3(setl, swift_message_type):
    '''
    Returns intermediary 3 information.
    '''   
    ret  = ''
    acct = ''
    bic = ''
    info = ''
    cp = ael.Party[setl.party_ptyid]
    if cp:
        acc = get_account(setl, 1)
        if acc :
            intermediary = acc.correspondent_bank4_ptynbr
            if intermediary:
                bic = get_partyalias(intermediary, acc, 4)
            if acc.account4:
                acct = str(acc.account4)
            info = get_intermediary_info(acc, 4)
            ret = 'ACCT/' + acct + '/ABIC/' + bic + '/NAME/' + info
    return ret


def get_intermediary4(setl, swift_message_type):
    '''
    Returns intermediary 4 information.
    '''   
    ret  = ''
    acct = ''
    bic = ''
    info = ''
    cp = ael.Party[setl.party_ptyid]
    if cp:
        acc = get_account(setl, 1)
        if acc :
            intermediary = acc.correspondent_bank5_ptynbr
            if intermediary:
                bic = get_partyalias(intermediary, acc, 5)
            if acc.account5:
                acct = str(acc.account5)
            info = get_intermediary_info(acc, 5)
            ret = 'ACCT/' + acct + '/ABIC/' + bic + '/NAME/' + info
    return ret


def get_intermediary_info(acc, mode):
    ''' '''
    name = ''
    addr = ''
    
    if mode == 1 and acc.correspondent_bank_ptynbr:
        name = acc.correspondent_bank_ptynbr.fullname
        addr = acc.correspondent_bank_ptynbr.address
        
    elif mode == 2 and acc.correspondent_bank2_ptynbr:
        name = acc.correspondent_bank2_ptynbr.fullname
        addr = acc.correspondent_bank2_ptynbr.address
        
    elif mode == 3 and acc.correspondent_bank3_ptynbr:
        name = acc.correspondent_bank3_ptynbr.fullname
        addr = acc.correspondent_bank3_ptynbr.address
        
    elif mode == 4 and acc.correspondent_bank4_ptynbr:
        name = acc.correspondent_bank4_ptynbr.fullname
        addr = acc.correspondent_bank4_ptynbr.address
        
    elif mode == 5 and acc.correspondent_bank5_ptynbr:
        name = acc.correspondent_bank5_ptynbr.fullname
        addr = acc.correspondent_bank5_ptynbr.address
            
    return "%s %s" % (FSettlement72.validate(name), FSettlement72.validate(addr))

def objects_by_name(parent_obj, name_prefixes, name):
    obj = parent_obj.mbf_first_object()
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    while obj:
        if obj.mbf_get_name() in names:
            yield obj
        obj = parent_obj.mbf_next_object()
        
def object_by_name(parent_obj, name_prefixes, name):
    for obj in objects_by_name(parent_obj, name_prefixes, name):
        return obj
    return None

def get_days_forward(currency):
    days_forward = 1
    if settlement_params.days_curr.has_key(currency):
        days_forward = settlement_params.days_curr[currency]
    else:
        used_account_currency = ael.used_acc_curr()
        if settlement_params.days_curr.has_key(used_account_currency):
            days_forward = settlement_params.days_curr[used_account_currency]            
    return days_forward
        
def within_time_window(pay_day, currency):
    days_forward = get_days_forward(currency)
    end_day = ael.date_today().add_banking_day(ael.Instrument[currency], days_forward)
    start_day = ael.date_today().add_banking_day(ael.Instrument[currency], (0-settlement_params.days_back))
    return (start_day <= pay_day <= end_day)

def is_remove_cash_flow_add_info(add_info_obj):
    remove = False
    name_obj = add_info_obj.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME', 'MBFE_BEGINNING')
    if name_obj:
        value_obj = add_info_obj.mbf_find_object('VALUE', 'MBFE_BEGINNING')
        if value_obj:
            if (name_obj.mbf_get_value(), value_obj.mbf_get_value()) in settlement_params.cash_flow_additional_infos:
                remove = True
    return remove

def message_can_be_skipped(instrument_obj):
    skip = False
    instrument_type_obj = instrument_obj.mbf_find_object('INSTYPE')
    instrument_type = instrument_type_obj.mbf_get_value()
    if instrument_type not in settlement_params.valid_instrument_types:
        skip = True
    return skip

def cash_flow_can_be_removed_from_message(cash_flow_obj, currency):
    pay_day_obj = cash_flow_obj.mbf_find_object('PAY_DAY')
    if pay_day_obj:
        pay_day = pay_day_obj.mbf_get_value()
        if within_time_window(ael.date(pay_day), currency):
            for add_info_obj in objects_by_name(cash_flow_obj, ['', '+'], 'ADDITIONALINFO'):
                if is_remove_cash_flow_add_info(add_info_obj):
                    return True
        else:
            return True
    return False

